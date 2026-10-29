# Corrected Candidate Acceptance — 2026-10-29

Baseline: `v1.1.0`, commit `1a8a6a9df980af6cf51029dabb792228edc12067`, plus the local corrections. This records observed results for the candidate; it does not assert that the old remote tag contains these corrections.

## Mechanical verification

- 75 distinct regressions passed on macOS with Python 3.12.14, 3.13.15, and 3.14.7.
- Original name-misidentification and Python 3.12 evidence-symlink failures were reproduced before correction and rejected structurally afterward.
- Local review capture covers real committed, staged, unstaged, deleted, and non-ignored untracked changes. Tests include file/directory replacement, state preservation, scope, symlinks, source changes during capture, and explicit rejection of changed gitlinks.
- Skills CLI 1.7.4 successfully installed the candidate and the exact 12 prerequisites from the [recorded dependency revisions](../references/compatibility.md). No `triage` dependency or global installation was added.
- The package contains Apache-2.0 authorization and original third-party notices. Format validation and local reference checks passed.

## Independent prompt-driven scenarios

The evaluator supplied raw requests and isolated projects to new agent contexts without the author's conversation or evaluator-held answers. Skills were read and applied from their installed filesystem definitions; no unsupported generic Skill API invocation was claimed.

| Scenario | Observed result |
|---|---|
| Complete local feature, including clean setup | Actual stage outputs feed the next consumer; custom ready-role mapping reaches specifications/tickets. Ten author behavior tests and five additional evaluator tests pass. Two independent review axes inspected the same fixed code snapshot. |
| Design only, response only | Requested design delivered; no project bytes or file inventory changed; no unmeasured performance claim. |
| Unresolved rules plus independent correction | Dependent feature remains specifically blocked; independent correction is implemented and verified without inventing business answers. |
| Review only, including untracked code | Actual pending files appear in the fixed review input; seeded behavior error is identified; application and test bytes remain unchanged. |
| Resume after a confirmed rule change | Affected prior results are superseded, revised behavior is verified, current outputs/consumers are linked, and an independent unresolved branch stays blocked. |

Code scenarios used separate independent standards/spec reviewers. Capacity constraints sometimes required sequential execution; this was not represented as parallel execution. No fixture delivery committed, pushed, published an issue, or deployed.

Raw inputs, actual generated artifacts, commands, logs, hashes, and reviewer results are retained in the maintainer's correction-audit workspace, separately from this domain-agnostic package. The scenario requests and business implementations are test evidence, not defaults for future users.

## Limits

These results cover the exercised macOS/agent environment, dependency revisions, and selected scenarios. Python 3.10/3.11, Windows/Linux, other hosts' activation and complete behavior, remote trackers, deployment, and performance were not exercised. Passing these tests does not establish SOLID compliance or correctness for every future generated program. Repeat relevant acceptance on dependency changes; see [the scenario protocol](behavioral-cases.md).
