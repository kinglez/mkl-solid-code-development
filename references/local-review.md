# Review Local Changes Against a Fixed Baseline

Read this reference when the delivered code includes staged, unstaged, or untracked files. It defines a **local two-axis review adaptation**, using the standards/spec vocabulary of Matt Pocock's `code-review`. It does not claim to execute that upstream skill unchanged: its `git diff <baseline>...HEAD` input excludes uncommitted work, while `implement` requests review before its final commit.

## Select the actual review input

Before implementation, record a fixed starting commit and the existing edits. Before review, confirm which paths belong to this task. Capturing all changes since a commit does not automatically attribute them to the task. Scope the capture where needed and disclose pre-existing changes that cannot be separated. Preserve other people's work.

For Git projects, run the packaged helper from the skill directory. These are command templates; replace the project, baseline, output, and path values with the actual task inputs:

```bash
python3 scripts/capture_review.py --repo path/to/project --baseline actual-commit --output path/to/outside-review
python3 scripts/capture_review.py --repo path/to/project --baseline actual-commit --output path/to/outside-review --path src/component --path tests/component
```

`--baseline` resolves once to an exact commit. The comparison is against that commit directly; it does not silently substitute a merge-base. `--path` values are literal repository-relative files or directories, not wildcard expressions. Omit them only when the entire changed scope belongs in the review. The new output directory must be outside the target repository and must not already exist.

The helper produces:

- `manifest.json`: fixed baseline and current HEAD, selected scope, file inventory, current file hashes and types, and capture limits.
- `changes.patch`: tracked changes from the baseline to final working-tree content, including committed, staged and unstaged changes, plus non-ignored untracked files. Binary changes are retained as Git binary patches.
- `files/`: current bytes for each changed regular file, addressed through the manifest. Deleted files are marked absent. Symlinks are stored as link text, never as copies of their targets.

The helper uses Python's standard library and a local Git executable. It does not commit, stage, checkout, change the index, or install anything. It checks the selected source twice and rejects changes observed during capture; this is a consistency check, not a filesystem transaction. It refuses empty captures, unresolved conflicts, invalid commits, output inside the repository, and changed submodules or special file types. Ignored untracked files are excluded; review any intentionally omitted evidence separately and disclose that scope.

Exit `0` returns the snapshot location and baseline as JSON. Exit `2` returns a JSON `input_error` on stderr for an invalid input or capture failure. The snapshot is review material, not an approval or a software-quality certificate.

If the project has no usable Git baseline, use the supplied patch or explicit before/after files with their source references and state the available comparison. This helper cannot synthesize a historical baseline. Design-only requests do not need a code snapshot.

## Perform the two review axes

Give both reviewers the **same snapshot**, originating request/specification, applicable repository standards, and actual verification results. Relevant unchanged callers or dependencies may be read from the repository; identify them and check they still correspond to the captured version. If the source changed after capture, recapture before claiming final coverage.

1. **Standards axis:** inspect the actual code for repository conventions, maintainability, responsibility allocation, contracts, dependency direction, and justified abstractions. Locate each actionable finding in the mapped source path, rather than treating file or class counts as proof of SOLID.
2. **Spec axis:** trace confirmed business rules and acceptance scenarios to the delivered behavior and evidence. Check normal, alternative, and failure paths within scope. Missing requirements or tests remain explicit gaps.

Use separate reviewers with independent contexts where supported and authorized. If only one context is available, perform both passes and label them accurately rather than claiming independence. Preserve real findings and their impact; an empty tool result alone does not prove review quality.

Correct necessary findings, rerun relevant verification, then capture the revised code again. Link the final snapshot and findings/corrections into the existing handoff record. A prior snapshot cannot approve later edits. Commit only if separately authorized; local delivery ends with the reviewed local changes.
