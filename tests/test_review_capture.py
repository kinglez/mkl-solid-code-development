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

    def test_ignored_untracked_files_are_excluded(self):
        (self.repo / "local.txt").write_text("after\n")
        (self.repo / "ignored").mkdir()
        (self.repo / "ignored/secret.txt").write_text("excluded content\n")
        result = self.capture()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([item["path"] for item in self.manifest()["files"]], ["local.txt"])
        self.assertNotIn(b"excluded content", (self.output / "changes.patch").read_bytes())

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
