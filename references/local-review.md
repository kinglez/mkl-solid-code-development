# Local Specification, Implementation and Review Adaptations

Read this reference for local specification/ticketing, pending-code implementation/review, or bounded architecture reassessment. Its **local two-axis review adaptation** uses the standards/spec vocabulary of Matt Pocock's `code-review`. It does not claim to execute that upstream skill unchanged: its `git diff <baseline>...HEAD` input excludes uncommitted work, while `implement` requests review before its final commit.

## Local specification and ticket adaptation

Read the installed `to-spec` and `to-tickets` definitions. Their original flows consume configured tracker/status vocabulary, include user decisions about test seams and breakdown, and publish to the configured location. Use them unchanged when those prerequisites, invocation and actions match the request.

For authorized local delivery that cannot execute that original flow, identify a **local specification and ticket adaptation** rather than claiming unmodified invocation:

1. Read the actual setup outputs, glossary/ADRs, requirements baseline, ready analysis/design/CDR results, and configured publication location/status mapping. The requirements baseline stays the business source; this step synthesizes its implementation handoff.
2. Record the highest useful public verification seams. Reuse already agreed seams or explicitly delegated technical choices; if a required decision remains with the user, pause that dependent work rather than manufacture agreement.
3. Produce the implementation specification with problem/solution, required behavior, implementation decisions, testing decisions, scope exclusions and source references. Do not reconstruct business answers from code or introduce a competing baseline.
4. Produce independently verifiable vertical slices and actual blocking edges. Preserve a previously approved breakdown or the user's explicit delegation; otherwise obtain the required breakdown decision before publication/implementation. Record the decision source honestly.
5. For a configured local tracker, write one file per slice at its saved location and apply its mapped status. A local document output expressly requested without tracker setup remains a named local adaptation, not evidence of tracker publication. Read those real files back before coding.

Do not publish remotely, silently change trackers, fabricate labels/approval, or treat reading these definitions as execution. Missing setup, test-seam or breakdown inputs are specific blockers; repeating unchanged setup does not repair them.

## Local implementation adaptation

Read `implement` and `tdd`, preserve the current specification/slices and agreed public test seams, and execute unblocked slices with suitable behavior feedback and regression checks. The original `implement` closes with review and a commit, while committed-history `code-review` does not include pending local files. For local delivery, replace that final sequence with the fixed-snapshot two-axis review below and stop with reviewed local changes unless committing is authorized. Record this as the local adaptation.

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
- `changes.patch`: tracked changes from the baseline to final working-tree content, including committed, staged and unstaged changes, plus non-ignored untracked files. Binary changes are retained as Git binary patches. Exported diffs explicitly disable terminal color and use conventional `a/` and `b/` prefixes, independent of presentation settings.
- `files/`: current bytes for each changed regular file, addressed through the manifest. Deleted files are marked absent. Symlinks are stored as link text, never as copies of their targets.

The helper uses Python's standard library and a local Git executable. It does not commit, stage, checkout, change the index, or install anything. It checks the selected source twice and rejects changes observed during capture; this is a consistency check, not a filesystem transaction. It refuses empty captures, unresolved conflicts, invalid commits, output inside the repository, and changed submodules or special file types. Ignored untracked files are excluded; review any intentionally omitted evidence separately and disclose that scope.

Diff comparison explicitly overrides submodule-ignore settings, including repository configuration and `.gitmodules`, so a selected changed submodule is rejected rather than hidden. An explicitly excluded submodule does not block the remaining selected paths; preserve and disclose that review scope.

The selected scope must contain no tracked paths marked `skip-worktree` or `assume-unchanged`. These flags can hide modified bytes or omit sparse-checkout content from disk, so the helper rejects them before producing a snapshot, naming the affected paths and flags. This conservative check also rejects flagged paths that Git reports as unchanged. Flags outside an explicit scope do not block that scope. Preserve the user's index: use a narrower justified scope or separately supplied before/after material for those paths, and disclose any remaining uncovered delivery. Do not silently omit required changes to obtain a successful capture.

Exit `0` returns the snapshot location and baseline as JSON. Exit `2` returns a JSON `input_error` on stderr for an invalid input or capture failure. The snapshot is review material, not an approval or a software-quality certificate.

If the project has no usable Git baseline, use the supplied patch or explicit before/after files with their source references and state the available comparison. This helper cannot synthesize a historical baseline. Design-only requests do not need a code snapshot.

## Perform the two review axes

Give both reviewers the **same snapshot**, originating request/specification, applicable repository standards, and actual verification results. Relevant unchanged callers or dependencies may be read from the repository; identify them and check they still correspond to the captured version. If the source changed after capture, recapture before claiming final coverage.

1. **Standards axis:** inspect the actual code for repository conventions, maintainability, responsibility allocation, contracts, dependency direction, and justified abstractions. Locate each actionable finding in the mapped source path, rather than treating file or class counts as proof of SOLID.
2. **Spec axis:** trace confirmed business rules and acceptance scenarios to the delivered behavior and evidence. Check normal, alternative, and failure paths within scope. Missing requirements or tests remain explicit gaps.

Use separate reviewers with independent contexts where supported and authorized. If only one context is available, perform both passes and label them accurately rather than claiming independence. Preserve real findings and their impact; an empty tool result alone does not prove review quality.

Correct necessary findings, rerun relevant verification, then capture the revised code again. Link the final snapshot and findings/corrections into the existing handoff record. A prior snapshot cannot approve later edits. Commit only if separately authorized; local delivery ends with the reviewed local changes.

## Scoped architecture adaptation

Read `improve-codebase-architecture` and `codebase-design`. Use the original candidate-report and decision workflow when its invocation, investigation scope and user choices fit. A bounded final reassessment can instead be explicitly named as a **scoped architecture adaptation**: inspect related modules/callers, actual dependency paths, interface depth, observed friction and real supported variation; produce a retain/adjust decision with evidence and limitations. Do not claim a full upstream scan, independent explorer, candidate selection, or user interview that did not occur. If exploration reveals a consequential undecided trade-off, return that decision to the user while continuing independent work.

Implemented architecture corrections invalidate affected results and return through design synchronization, behavior checks and the fixed-snapshot change-review loop. A candidate report or architecture conclusion alone does not close later code changes.
