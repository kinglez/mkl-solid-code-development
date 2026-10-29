#!/usr/bin/env python3
"""Capture a local review input without committing, staging, or changing the repository."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys


def git(root: Path, *args: str, allowed=(0,)) -> bytes:
    result = subprocess.run(
        ["git", "--no-optional-locks", *args], cwd=root,
        env=dict(os.environ, GIT_OPTIONAL_LOCKS="0"), capture_output=True,
    )
    if result.returncode not in allowed:
        raise ValueError(result.stderr.decode("utf-8", errors="replace").strip() or "Git command failed.")
    return result.stdout


def pathspecs(paths: list[str]) -> list[str]:
    for value in paths:
        path = Path(value)
        if not value.strip() or path.is_absolute() or ".." in path.parts:
            raise ValueError("Scope paths must be literal repository-relative paths without '..'.")
    return [f":(literal){Path(value).as_posix()}" for value in paths]


def current_file(root: Path, name: str):
    path = root / name
    # A directory replaced by a symlink does not expose files below its target.
    for parent in path.parents:
        if parent == root:
            break
        if parent.is_symlink():
            return {"path": name, "kind": "absent"}, None
    try:
        info = path.lstat()
    except (FileNotFoundError, NotADirectoryError):
        return {"path": name, "kind": "absent"}, None
    if stat.S_ISDIR(info.st_mode):
        # A former file replaced by a directory is deleted at this path;
        # its new children are captured as separate paths. Gitlinks are
        # rejected from Git metadata before inspecting filesystem types.
        return {"path": name, "kind": "absent"}, None
    if stat.S_ISLNK(info.st_mode):
        kind, mode, content = "symlink", "120000", os.fsencode(os.readlink(path))
    elif stat.S_ISREG(info.st_mode):
        kind = "file"
        mode = "100755" if info.st_mode & stat.S_IXUSR else "100644"
        content = path.read_bytes()
    else:
        raise ValueError(f"Unsupported changed file type at {name!r}; review submodules or special files separately.")
    return {"path": name, "kind": kind, "mode": mode,
            "sha256": hashlib.sha256(content).hexdigest()}, content


def read_state(root: Path, baseline: str, scope: list[str]):
    if git(root, "ls-files", "--unmerged", "-z", "--", *scope):
        raise ValueError("The selected scope contains unresolved Git conflicts.")
    diff_args = ("diff", "--no-ext-diff", "--no-textconv", "--no-renames")
    changed = git(root, *diff_args, "--name-only", "-z", baseline, "--", *scope)
    untracked = git(root, "ls-files", "--others", "--exclude-standard", "-z", "--", *scope)
    names = sorted(set(part.decode("utf-8", errors="surrogateescape")
                       for part in changed.split(b"\0") + untracked.split(b"\0") if part))
    if not names:
        raise ValueError("The selected scope has no changes to review.")
    gitlinks = set()
    for listing in (git(root, "ls-files", "--stage", "-z", "--", *scope),
                    git(root, "ls-tree", "-r", "-z", baseline, "--", *scope)):
        for entry in listing.split(b"\0"):
            if entry.startswith(b"160000 "):
                gitlinks.add(entry.split(b"\t", 1)[1].decode("utf-8", errors="surrogateescape"))
    if gitlinks.intersection(names):
        raise ValueError("The selected change contains a submodule; review it separately.")
    files = [current_file(root, name) for name in names]
    patch = git(root, *diff_args, "--binary", "--full-index", baseline, "--", *scope)
    for raw in untracked.split(b"\0"):
        if raw:
            name = raw.decode("utf-8", errors="surrogateescape")
            patch += git(root, "diff", "--no-index", "--no-ext-diff", "--no-textconv",
                         "--binary", "--full-index", "--", os.devnull, name, allowed=(0, 1))
    return {
        "head": git(root, "rev-parse", "--verify", "HEAD^{commit}").decode().strip(),
        "status": git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all", "--", *scope),
        "patch": patch,
        "files": files,
    }


def capture(repo: Path, baseline: str, output: Path, paths: list[str]):
    repo = repo.expanduser().resolve()
    root = Path(git(repo, "rev-parse", "--show-toplevel").decode().rstrip("\n")).resolve()
    output = output.expanduser().absolute()
    if output.resolve().is_relative_to(root):
        raise ValueError("Review output must be outside the target repository.")
    if output.exists() or output.is_symlink():
        raise FileExistsError("Review output already exists; use a new directory.")
    scope = pathspecs(paths)
    fixed = git(root, "rev-parse", "--verify", "--end-of-options", f"{baseline}^{{commit}}").decode().strip()
    state = read_state(root, fixed, scope)
    if read_state(root, fixed, scope) != state:
        raise ValueError("Selected source changed during capture; retry after it is stable.")
    manifest = {
        "format_version": 1,
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "repository": str(root),
        "baseline": fixed,
        "head": state["head"],
        "scope_paths": paths or ["."],
        "comparison": "Exact baseline to selected current tracked content, plus non-ignored untracked files.",
        "attribution": "The caller must confirm task ownership; capture does not distinguish pre-existing edits.",
        "patch": "changes.patch",
        "patch_sha256": hashlib.sha256(state["patch"]).hexdigest(),
        "status": state["status"].decode("utf-8", errors="surrogateescape").split("\0"),
        "files": [],
    }
    payloads = {"changes.patch": state["patch"]}
    for index, (entry, content) in enumerate(state["files"], 1):
        if content is not None:
            entry["snapshot"] = f"files/{index:04d}"
            payloads[entry["snapshot"]] = content
        manifest["files"].append(entry)
    payloads["manifest.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
    output.mkdir(parents=True, exist_ok=False)
    try:
        for name, content in payloads.items():
            destination = output / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open("xb") as stream:
                stream.write(content)
    except OSError:
        shutil.rmtree(output)
        raise
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."), help="Target Git project, not the installed skill.")
    parser.add_argument("--baseline", required=True, help="Explicit commit, tag or branch; resolved once to a commit.")
    parser.add_argument("--output", type=Path, required=True, help="New snapshot directory outside the target repository.")
    parser.add_argument("--path", action="append", default=[], help="Literal repository-relative scope; repeat as needed.")
    args = parser.parse_args(argv)
    try:
        manifest = capture(args.repo, args.baseline, args.output, args.path)
    except (OSError, ValueError, RuntimeError) as exc:
        print(json.dumps({"input_error": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps({"snapshot": str(args.output.absolute()), "baseline": manifest["baseline"],
                      "file_count": len(manifest["files"])}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
