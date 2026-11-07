"""Real Git checks for review inputs, without committing the implementation."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import importlib.util


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/capture_review.py"


class ReviewCaptureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name)
        self.repo = self.workspace / "project"
        self.repo.mkdir()
        self.git("init", "-q")
        self.git("config", "user.name", "Local test")
        self.git("config", "user.email", "local-test@example.invalid")
        for name in ("committed.txt", "staged.txt", "local.txt", "remove.txt", "literal[1].txt", "literal1.txt"):
            (self.repo / name).write_text("before\n")
        (self.repo / ".gitignore").write_text("ignored/\n")
        self.git("add", ".")
        self.git("commit", "-qm", "Synthetic baseline")
        self.baseline = self.git("rev-parse", "HEAD").decode().strip()
        self.output = self.workspace / "review"

    def git(self, *args):
        return subprocess.run(
            ["git", "--no-optional-locks", *args], cwd=self.repo,
            env=dict(os.environ, GIT_OPTIONAL_LOCKS="0"), capture_output=True, check=True,
        ).stdout

    def capture(self, *args, baseline=None, output=None, repo=None):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--repo", str(repo or self.repo),
             "--baseline", baseline or self.baseline, "--output", str(output or self.output), *args],
            capture_output=True, text=True,
        )

    def manifest(self):
        return json.loads((self.output / "manifest.json").read_text())

    def test_captures_committed_staged_unstaged_deleted_and_new_files_without_git_mutation(self):
        (self.repo / "committed.txt").write_text("committed result\n")
        self.git("add", "committed.txt")
        self.git("commit", "-qm", "Synthetic committed slice")
        (self.repo / "staged.txt").write_text("staged result\n")
        self.git("add", "staged.txt")
        (self.repo / "local.txt").write_text("local result\n")
        (self.repo / "remove.txt").unlink()
        new = self.repo / "brand new\nfile.txt"
        new.write_text("new result\n")
        binary = self.repo / "data.bin"
        binary.write_bytes(b"\x00\x01\xffnew\x00")
        before_status = self.git("status", "--porcelain=v1", "-z", "--untracked-files=all")
        before_index = (self.repo / ".git/index").read_bytes()
        before_head = self.git("rev-parse", "HEAD")
        result = self.capture()
        self.assertEqual(result.returncode, 0, result.stderr)
        manifest = self.manifest()
        self.assertEqual(manifest["baseline"], self.baseline)
        self.assertEqual(manifest["head"], before_head.decode().strip())
        entries = {item["path"]: item for item in manifest["files"]}
        self.assertEqual(set(entries), {"committed.txt", "staged.txt", "local.txt", "remove.txt", "brand new\nfile.txt", "data.bin"})
        self.assertEqual(entries["remove.txt"]["kind"], "absent")
        for name, item in entries.items():
            if item["kind"] == "absent":
                continue
            content = (self.output / item["snapshot"]).read_bytes()
            self.assertEqual(content, (self.repo / name).read_bytes())
            self.assertEqual(item["sha256"], hashlib.sha256(content).hexdigest())
        patch = (self.output / "changes.patch").read_bytes()
        for added in (b"+committed result", b"+staged result", b"+local result", b"+new result", b"GIT binary patch"):
            self.assertIn(added, patch)
        self.assertEqual(before_status, self.git("status", "--porcelain=v1", "-z", "--untracked-files=all"))
        self.assertEqual(before_index, (self.repo / ".git/index").read_bytes())
        self.assertEqual(before_head, self.git("rev-parse", "HEAD"))

    def test_literal_scope_excludes_unrelated_and_similarly_named_paths(self):
        for name in ("literal[1].txt", "literal1.txt", "unrelated.txt"):
            (self.repo / name).write_text("after\n")
        result = self.capture("--path", "literal[1].txt")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([item["path"] for item in self.manifest()["files"]], ["literal[1].txt"])

    def test_index_flags_fail_closed_without_changing_source_or_index(self):
        for flag in ("skip-worktree", "assume-unchanged"):
            with self.subTest(flag=flag):
                self.git("update-index", "--" + flag, "local.txt")
                (self.repo / "local.txt").write_text("hidden changed bytes\n")
                (self.repo / "staged.txt").write_text("visible changed bytes\n")
                index_before = (self.repo / ".git/index").read_bytes()
                source_before = (self.repo / "local.txt").read_bytes()
                output = self.workspace / flag
                try:
                    result = self.capture(output=output)
                    self.assertEqual(result.returncode, 2, result.stderr)
                    message = json.loads(result.stderr)["input_error"]
                    self.assertIn(flag, message)
                    self.assertIn("local.txt", message)
                    self.assertFalse(output.exists())
                    self.assertEqual(index_before, (self.repo / ".git/index").read_bytes())
                    self.assertEqual(source_before, (self.repo / "local.txt").read_bytes())
                finally:
                    self.git("update-index", "--no-" + flag, "local.txt")

    def test_index_flags_outside_selected_scope_do_not_block_capture(self):
        self.git("update-index", "--skip-worktree", "local.txt")
        (self.repo / "local.txt").write_text("outside selected scope\n")
        (self.repo / "staged.txt").write_text("selected changed bytes\n")
        index_before = (self.repo / ".git/index").read_bytes()
        result = self.capture("--path", "staged.txt")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([item["path"] for item in self.manifest()["files"]], ["staged.txt"])
        self.assertEqual(index_before, (self.repo / ".git/index").read_bytes())

    def test_sparse_committed_changes_fail_closed_and_allow_an_explicit_safe_scope(self):
        for name in ("active", "inactive"):
            (self.repo / name).mkdir()
            (self.repo / name / "source.txt").write_text("baseline bytes\n")
        self.git("add", ".")
        self.git("commit", "-qm", "Synthetic sparse baseline")
        baseline = self.git("rev-parse", "HEAD").decode().strip()
        (self.repo / "inactive/source.txt").write_text("committed current bytes\n")
        self.git("add", ".")
        self.git("commit", "-qm", "Synthetic sparse change")
        self.git("sparse-checkout", "init", "--cone")
        self.git("sparse-checkout", "set", "active")
        self.assertFalse((self.repo / "inactive/source.txt").exists())

        self.assertEqual(self.git("show", "HEAD:inactive/source.txt"), b"committed current bytes\n")
        (self.repo / "active/source.txt").write_text("selected current bytes\n")
        index_before = (self.repo / ".git/index").read_bytes()
        head_before = self.git("rev-parse", "HEAD")
        result = self.capture(baseline=baseline)
        self.assertEqual(result.returncode, 2, result.stderr)
        message = json.loads(result.stderr)["input_error"]
        self.assertIn("skip-worktree", message)
        self.assertIn("inactive/source.txt", message)
        self.assertFalse(self.output.exists())
        safe_output = self.workspace / "safe-sparse-scope"
        result = self.capture("--path", "active", baseline=baseline, output=safe_output)
        self.assertEqual(result.returncode, 0, result.stderr)
        entries = json.loads((safe_output / "manifest.json").read_text())["files"]
        self.assertEqual([item["path"] for item in entries], ["active/source.txt"])
        self.assertEqual((safe_output / entries[0]["snapshot"]).read_bytes(), b"selected current bytes\n")
        self.assertEqual(index_before, (self.repo / ".git/index").read_bytes())
        self.assertEqual(head_before, self.git("rev-parse", "HEAD"))
        self.assertFalse((self.repo / "inactive/source.txt").exists())

    def test_machine_patch_ignores_color_and_prefix_presentation_settings(self):
        self.git("config", "color.ui", "always")
        self.git("config", "diff.noprefix", "true")
        self.git("config", "diff.srcPrefix", "old-display/")
        self.git("config", "diff.dstPrefix", "new-display/")
        (self.repo / "local.txt").write_text("tracked changed bytes\n")
        (self.repo / "new.txt").write_text("new changed bytes\n")
        result = self.capture()
        self.assertEqual(result.returncode, 0, result.stderr)
        patch_path = self.output / "changes.patch"
        patch = patch_path.read_bytes()
        self.assertNotIn(b"\x1b[", patch)
        self.assertIn(b"diff --git a/local.txt b/local.txt\n", patch)
        self.assertIn(b"diff --git a/new.txt b/new.txt\n", patch)
        self.git("checkout", "--", "local.txt")
        (self.repo / "new.txt").unlink()
        self.git("apply", "--check", str(patch_path))
        self.git("apply", str(patch_path))
        self.assertEqual((self.repo / "local.txt").read_bytes(), b"tracked changed bytes\n")
        self.assertEqual((self.repo / "new.txt").read_bytes(), b"new changed bytes\n")

    def test_file_replaced_by_directory_preserves_deleted_path_and_new_children(self):
        (self.repo / "local.txt").unlink()
        (self.repo / "local.txt").mkdir()
        (self.repo / "local.txt/child.txt").write_text("new child\n")
        before = self.git("status", "--porcelain=v1", "-z", "--untracked-files=all")
        result = self.capture()
        self.assertEqual(result.returncode, 0, result.stderr)
        entries = {item["path"]: item for item in self.manifest()["files"]}
        self.assertEqual(entries["local.txt"]["kind"], "absent")
        self.assertEqual((self.output / entries["local.txt/child.txt"]["snapshot"]).read_text(), "new child\n")
        self.assertEqual(before, self.git("status", "--porcelain=v1", "-z", "--untracked-files=all"))

    def test_directory_replaced_by_file_preserves_deleted_children_and_new_file(self):
        (self.repo / "folder").mkdir()
        (self.repo / "folder/child.txt").write_text("old child\n")
        self.git("add", "folder")
        self.git("commit", "-qm", "Synthetic directory baseline")
        self.baseline = self.git("rev-parse", "HEAD").decode().strip()
        (self.repo / "folder/child.txt").unlink()
        (self.repo / "folder").rmdir()
        (self.repo / "folder").write_text("new regular file\n")
        before = self.git("status", "--porcelain=v1", "-z", "--untracked-files=all")
        result = self.capture()
        self.assertEqual(result.returncode, 0, result.stderr)
        entries = {item["path"]: item for item in self.manifest()["files"]}
        self.assertEqual(entries["folder/child.txt"]["kind"], "absent")
        self.assertEqual((self.output / entries["folder"]["snapshot"]).read_text(), "new regular file\n")
        self.assertEqual(before, self.git("status", "--porcelain=v1", "-z", "--untracked-files=all"))

    def test_deleted_gitlink_is_explicitly_outside_supported_capture(self):
        self.git("update-index", "--add", "--cacheinfo", "160000," + self.baseline + ",submodule")
        self.git("commit", "-qm", "Synthetic gitlink baseline")
        self.baseline = self.git("rev-parse", "HEAD").decode().strip()
        result = self.capture()
        self.assertEqual(result.returncode, 2)
        self.assertIn("submodule", json.loads(result.stderr)["input_error"])
        self.assertFalse(self.output.exists())

    def test_submodule_ignore_settings_cannot_hide_changes_from_the_selected_scope(self):
        source = self.workspace / "dependency-source"
        source.mkdir()
        for args in (("init", "-q"), ("config", "user.name", "Local test"),
                     ("config", "user.email", "local-test@example.invalid")):
            subprocess.run(["git", *args], cwd=source, capture_output=True, check=True)
        (source / "source.txt").write_text("dependency baseline\n")
        subprocess.run(["git", "add", "."], cwd=source, capture_output=True, check=True)
        subprocess.run(["git", "commit", "-qm", "Synthetic dependency"],
                       cwd=source, capture_output=True, check=True)
        self.git("-c", "protocol.file.allow=always", "submodule", "add", "-q", str(source), "dependency")
        self.git("add", ".")
        self.git("commit", "-qm", "Synthetic submodule baseline")
        baseline = self.git("rev-parse", "HEAD").decode().strip()
        dependency_file = self.repo / "dependency/source.txt"
        dependency_file.write_text("changed dependency bytes\n")
        (self.repo / "local.txt").write_text("changed selected bytes\n")
        settings = (
            ("diff", ("config",), "diff.ignoreSubmodules"),
            ("submodule", ("config",), "submodule.dependency.ignore"),
            ("gitmodules", ("config", "--file", ".gitmodules"), "submodule.dependency.ignore"),
        )
        for label, command, key in settings:
            with self.subTest(setting=label):
                self.git(*command, key, "all")
                index_before = (self.repo / ".git/index").read_bytes()
                try:
                    output = self.workspace / ("ignored-" + label)
                    result = self.capture(baseline=baseline, output=output)
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertIn("submodule", json.loads(result.stderr)["input_error"])
                    self.assertFalse(output.exists())
                    safe_output = self.workspace / ("safe-" + label)
                    safe = self.capture("--path", "local.txt", baseline=baseline, output=safe_output)
                    self.assertEqual(safe.returncode, 0, safe.stderr)
                    entries = json.loads((safe_output / "manifest.json").read_text())["files"]
                    self.assertEqual([item["path"] for item in entries], ["local.txt"])
                    self.assertEqual(index_before, (self.repo / ".git/index").read_bytes())
                    self.assertEqual(dependency_file.read_bytes(), b"changed dependency bytes\n")
                    self.assertEqual(self.git("rev-parse", "HEAD").decode().strip(), baseline)
                finally:
                    self.git(*command, "--unset", key)

    def test_ignored_untracked_files_are_excluded(self):
        (self.repo / "local.txt").write_text("after\n")
        (self.repo / "ignored").mkdir()
        (self.repo / "ignored/secret.txt").write_text("excluded content\n")
        result = self.capture()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([item["path"] for item in self.manifest()["files"]], ["local.txt"])
        self.assertNotIn(b"excluded content", (self.output / "changes.patch").read_bytes())

    def test_index_removal_excludes_ignored_worktree_payloads(self):
        self.git("rm", "--cached", "--quiet", "local.txt")
        (self.repo / ".gitignore").write_text("ignored/\nlocal.txt\n")
        self.git("add", ".gitignore")
        marker = b"IGNORED_LOCAL_ONLY_MARKER\n"
        (self.repo / "local.txt").write_bytes(marker)
        self.assertEqual(self.git("check-ignore", "local.txt"), b"local.txt\n")
        for stage in ("staged", "committed"):
            with self.subTest(stage=stage):
                if stage == "committed":
                    self.git("commit", "-qm", "Synthetic tracking removal")
                output = self.workspace / ("removed-" + stage)
                before_index = (self.repo / ".git/index").read_bytes()
                before_status = self.git("status", "--porcelain=v1", "-z")
                result = self.capture("--path", "local.txt", output=output)
                self.assertEqual(result.returncode, 0, result.stderr)
                item = json.loads((output / "manifest.json").read_text())["files"][0]
                self.assertEqual(item, {"path": "local.txt", "kind": "absent"})
                self.assertIn(b"deleted file mode", (output / "changes.patch").read_bytes())
                for artifact in output.rglob("*"):
                    if artifact.is_file():
                        self.assertNotIn(marker, artifact.read_bytes())
                self.assertEqual((self.repo / "local.txt").read_bytes(), marker)
                self.assertEqual((self.repo / ".git/index").read_bytes(), before_index)
                self.assertEqual(self.git("status", "--porcelain=v1", "-z"), before_status)

    def test_ignore_rules_preserve_tracked_and_allowed_untracked_capture(self):
        (self.repo / ".gitignore").write_text("ignored/\nlocal.txt\n")
        (self.repo / "local.txt").write_bytes(b"tracked current bytes\n")
        (self.repo / "new.txt").write_bytes(b"allowed new bytes\n")
        result = self.capture()
        self.assertEqual(result.returncode, 0, result.stderr)
        items = {item["path"]: item for item in self.manifest()["files"]}
        for name in ("local.txt", "new.txt"):
            self.assertEqual((self.output / items[name]["snapshot"]).read_bytes(),
                             (self.repo / name).read_bytes())

    def test_index_removal_retains_nonignored_worktree_addition(self):
        self.git("rm", "--cached", "--quiet", "local.txt")
        (self.repo / "local.txt").write_bytes(b"allowed current bytes\n")
        result = self.capture("--path", "local.txt")
        self.assertEqual(result.returncode, 0, result.stderr)
        item = self.manifest()["files"][0]
        self.assertEqual(item["kind"], "file")
        self.assertEqual((self.output / item["snapshot"]).read_bytes(), b"allowed current bytes\n")
        self.assertIn(b"+allowed current bytes", (self.output / "changes.patch").read_bytes())

    def test_empty_change_is_an_explicit_error_without_output(self):
        result = self.capture()
        self.assertEqual(result.returncode, 2)
        self.assertIn("input_error", json.loads(result.stderr))
        self.assertFalse(self.output.exists())

    def test_invalid_baseline_is_an_explicit_error_without_output(self):
        result = self.capture(baseline="not-a-real-commit")
        self.assertEqual(result.returncode, 2)
        self.assertIn("input_error", json.loads(result.stderr))
        self.assertFalse(self.output.exists())

    def test_output_cannot_be_inside_the_repository(self):
        (self.repo / "local.txt").write_text("after\n")
        result = self.capture(output=self.repo / "review")
        self.assertEqual(result.returncode, 2)
        self.assertIn("outside", json.loads(result.stderr)["input_error"])
        self.assertFalse((self.repo / "review").exists())

    def test_existing_output_is_preserved(self):
        (self.repo / "local.txt").write_text("after\n")
        self.output.mkdir()
        marker = self.output / "existing.txt"
        marker.write_text("keep\n")
        result = self.capture()
        self.assertEqual(result.returncode, 2)
        self.assertEqual(marker.read_text(), "keep\n")
        self.assertEqual(list(self.output.iterdir()), [marker])

    def test_scope_cannot_escape_or_use_absolute_paths(self):
        for scope in ("../elsewhere", str(self.workspace)):
            with self.subTest(scope=scope):
                result = self.capture("--path", scope)
                self.assertEqual(result.returncode, 2)
                self.assertIn("input_error", json.loads(result.stderr))
                self.assertFalse(self.output.exists())

    def test_non_git_project_is_an_explicit_error(self):
        plain = self.workspace / "plain"
        plain.mkdir()
        result = self.capture(repo=plain)
        self.assertEqual(result.returncode, 2)
        self.assertIn("input_error", json.loads(result.stderr))
        self.assertFalse(self.output.exists())

    @unittest.skipIf(os.name == "nt", "Windows does not allow newline directory names")
    def test_repository_root_preserves_trailing_newlines_with_a_shared_baseline(self):
        requested = self.workspace / "project\n"
        subprocess.run(["git", "clone", "-q", "--no-hardlinks", str(self.repo), str(requested)],
                       capture_output=True, check=True)
        (self.repo / "local.txt").write_bytes(b"unrelated sibling bytes\n")
        (requested / "local.txt").write_bytes(b"requested project bytes\n")
        indices = {root: (root / ".git/index").read_bytes() for root in (self.repo, requested)}
        result = self.capture(repo=requested)
        self.assertEqual(result.returncode, 0, result.stderr)
        manifest = self.manifest()
        self.assertEqual(manifest["repository"], str(requested.resolve()))
        self.assertEqual(manifest["baseline"], self.baseline)
        item = manifest["files"][0]
        self.assertEqual((self.output / item["snapshot"]).read_bytes(), b"requested project bytes\n")
        for root, index in indices.items():
            self.assertEqual((root / ".git/index").read_bytes(), index)
        self.assertEqual((self.repo / "local.txt").read_bytes(), b"unrelated sibling bytes\n")
        self.assertEqual((requested / "local.txt").read_bytes(), b"requested project bytes\n")

    @unittest.skipIf(os.name == "nt", "Windows does not allow newline directory names")
    def test_repository_identity_handles_newlines_and_unicode_without_a_sibling(self):
        for index, name in enumerate(("trailing\n\n", "embedded\nname", "\u76ee\u5f55")):
            with self.subTest(name=name):
                requested = self.workspace / name
                self.repo.rename(requested)
                self.repo = requested
                (requested / "local.txt").write_bytes(b"requested current bytes\n")
                output = self.workspace / ("identity-" + str(index))
                result = self.capture(output=output)
                self.assertEqual(result.returncode, 0, result.stderr)
                manifest = json.loads((output / "manifest.json").read_text())
                self.assertEqual(manifest["repository"], str(requested.resolve()))
                self.assertEqual((output / manifest["files"][0]["snapshot"]).read_bytes(),
                                 b"requested current bytes\n")

    def test_repository_argument_can_name_a_subdirectory_of_the_worktree(self):
        nested = self.repo / "nested/working"
        nested.mkdir(parents=True)
        (self.repo / "local.txt").write_bytes(b"current project bytes\n")
        result = self.capture(repo=nested)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.manifest()["repository"], str(self.repo.resolve()))

    def test_source_change_during_capture_is_rejected_without_output(self):
        spec = importlib.util.spec_from_file_location("capture_review_test", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        (self.repo / "local.txt").write_text("first result\n")
        read_state = module.read_state
        calls = 0

        def change_after_first_read(*args):
            nonlocal calls
            state = read_state(*args)
            calls += 1
            if calls == 1:
                (self.repo / "local.txt").write_text("later result\n")
            return state

        with mock.patch.object(module, "read_state", side_effect=change_after_first_read):
            with self.assertRaisesRegex(ValueError, "changed during capture"):
                module.capture(self.repo, self.baseline, self.output, [])
        self.assertFalse(self.output.exists())

    @unittest.skipUnless(hasattr(os, "symlink"), "Symlinks unavailable")
    def test_directory_symlink_capture_fails_closed_until_git_tracks_the_link(self):
        folder = self.repo / "folder"
        folder.mkdir()
        (folder / "child.txt").write_bytes(b"old child bytes\n")
        self.git("add", "folder")
        self.git("commit", "-qm", "Synthetic directory baseline")
        self.baseline = self.git("rev-parse", "HEAD").decode().strip()
        (folder / "child.txt").unlink()
        folder.rmdir()
        outside = self.workspace / "outside-directory"
        outside.mkdir()
        marker = outside / "marker.txt"
        marker.write_bytes(b"external target bytes\n")
        try:
            folder.symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("Directory symlinks unavailable")
        before_index = (self.repo / ".git/index").read_bytes()
        before_status = self.git("status", "--porcelain=v1", "-z", "--untracked-files=all")
        for child in ("marker.txt", "null"):
            with self.subTest(child=child):
                (outside / child).write_bytes(b"external target bytes\n")
                output = self.workspace / ("directory-link-" + child)
                result = self.capture(output=output)
                self.assertEqual(result.returncode, 2, result.stderr)
                message = json.loads(result.stderr)["input_error"]
                self.assertIn("directory symlink", message)
                self.assertIn("patch", message)
                self.assertFalse(output.exists())
                self.assertEqual((self.repo / ".git/index").read_bytes(), before_index)
                self.assertEqual(self.git("status", "--porcelain=v1", "-z", "--untracked-files=all"), before_status)
        self.assertEqual(marker.read_bytes(), b"external target bytes\n")
        # The normal tracked Git diff represents the link itself safely.
        self.git("add", "-A")
        staged_index = (self.repo / ".git/index").read_bytes()
        result = self.capture()
        self.assertEqual(result.returncode, 0, result.stderr)
        patch = (self.output / "changes.patch").read_bytes()
        self.assertIn(b"new file mode 120000", patch)
        self.assertIn(b"+" + os.fsencode(str(outside)), patch)
        self.assertNotIn(b"external target bytes", patch)
        self.assertEqual((self.repo / ".git/index").read_bytes(), staged_index)

    def test_new_empty_file_still_has_a_reviewable_patch_and_snapshot(self):
        (self.repo / "empty.txt").touch()
        result = self.capture()
        self.assertEqual(result.returncode, 0, result.stderr)
        item = self.manifest()["files"][0]
        self.assertEqual(item["path"], "empty.txt")
        self.assertEqual((self.output / item["snapshot"]).read_bytes(), b"")
        self.assertIn(b"new file mode", (self.output / "changes.patch").read_bytes())

    def test_missing_backend_patch_is_rejected_without_a_snapshot(self):
        spec = importlib.util.spec_from_file_location("capture_missing_patch", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        (self.repo / "new.txt").write_bytes(b"current untracked bytes\n")
        before_index = (self.repo / ".git/index").read_bytes()
        run_git = module.git

        def unavailable_patch(root, *args, **kwargs):
            if "--no-index" in args:
                return b""
            return run_git(root, *args, **kwargs)

        with mock.patch.object(module, "git", side_effect=unavailable_patch):
            with self.assertRaisesRegex(ValueError, "did not produce a review patch"):
                module.capture(self.repo, self.baseline, self.output, [])
        self.assertFalse(self.output.exists())
        self.assertEqual((self.repo / ".git/index").read_bytes(), before_index)
        self.assertEqual((self.repo / "new.txt").read_bytes(), b"current untracked bytes\n")

    @unittest.skipUnless(hasattr(os, "symlink"), "Symlinks unavailable")
    def test_symlink_is_captured_as_link_text_without_following_the_target(self):
        outside = self.workspace / "private.txt"
        outside.write_text("private target content\n")
        (self.repo / "new-link").symlink_to(outside)
        result = self.capture()
        self.assertEqual(result.returncode, 0, result.stderr)
        item = self.manifest()["files"][0]
        self.assertEqual(item["kind"], "symlink")
        self.assertEqual((self.output / item["snapshot"]).read_bytes(), os.fsencode(str(outside)))
        self.assertNotIn(b"private target content", (self.output / "changes.patch").read_bytes())


if __name__ == "__main__":
    unittest.main()
