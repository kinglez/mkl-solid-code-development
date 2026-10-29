# Acceptance Evidence

## Detailed-design candidate — 2026-10-29

Baseline: `v1.2.1`, commit `8a6b4af86e76691363438101a0be9fce137b61a8`, plus the detailed-design changes. This records the local candidate; it does not change the contents of an existing tag.

### Mechanical and installation checks

- **101 distinct regressions pass** on macOS with Python **3.12.14, 3.13.15, and 3.14.7**. They include the previous 75 checks, conditional prerequisites, opt-in design initialization, and 21 design-view regressions.
- Meaningful negative/positive cases cover missing class/sequence/state sources, unfinished applicability and consistency review, unresolved selected inputs, invalidated reuse, evidence/path constraints, and the distinction between pre-code design readiness and final delivery readiness.
- A pre-code record passes `--require-design` while final task, behavior, and review work remain incomplete. Combining it with the final handoff gate correctly fails until those later obligations are met. Nine legacy-fixture/flag comparisons retain the previous fields and exit behavior.
- Skills CLI **1.7.4** installs the candidate through its standard local-source `add` command in an isolated project. Installed package bytes match the candidate. The two conditional modeling skills were also installed with the standard CLI from the [recorded MKL revision](../references/compatibility.md); the selected **14-definition** presence check passes. No global installation is changed.
- Class, sequence, and state sources are checked/rendered locally with PlantUML **1.2026.7**, Java **21.0.9**, and Graphviz **15.1.1**. Relevant MKL profile checks are executed; skipped layers and partial heuristic coverage remain explicit. A non-OO module view is not reported as validated by the class-specific profile.
- Skill format, local Markdown targets, SVG parsing, distribution integrity, and `git diff --check` pass. Four homepage diagrams were regenerated with Fireworks Tech Graph and visually inspected.

### Independent forward execution

An independent author supplied raw business requests and isolated projects before executor agents read the revised skill. Evaluator-held vectors and assessment criteria were withheld. Fresh Standards and Spec reviewers inspected fixed snapshots independently. Business fixtures and their generated applications remain outside this domain-agnostic package.

| Scenario | Actual outputs and verification |
|---|---|
| Stateful new use case | Confirmed rules and domain/BCE analysis feed a design class model, principal/decision/publication sequences, and a seven-state lifecycle. A successful pre-code gate precedes specification, vertical tickets, actual red/green implementation, review, and scoped architecture reassessment. Eighteen author tests and eighteen evaluator vector groups pass, including legal/illegal transitions, explicit retry, side-effect counts, terminal refusal, and public-result isolation. |
| Stateless new use case | A module view and success/failure sequences feed a real specification, slices, code, review, and architecture conclusion. Lifecycle non-applicability is justified without artificial classes/states. Seventeen author tests and eight evaluator tests pass, including an independent interval oracle, validation, boundaries, and input isolation. |
| Bounded correction | A reasoned lightweight path changes only the function and its public regression tests. A real failing boundary case becomes green; six author tests and three evaluator tests pass. Existing responsibilities and contracts are preserved without forced diagrams or setup. |
| Response-only design | The response contains BCE, class, two interaction, and state sources, public contracts, traceability, and explicit implementation-changing questions. All five sources are independently rendered from stdin in memory. The project remains exactly six files / 1,267 bytes at its starting HEAD, with no setup, configuration, spec, ticket, diagram, test, or code writes. The discussion is delivered without claiming the proposed design is ready to implement. |

Both review axes replay the three implementation suites from the fixed snapshots. One Standards terminology finding is corrected from an undefined abbreviation to the actual declared state name; the affected source and preview are regenerated and the exact delta is independently rechecked. No findings remain open. Automatic UML/profile coverage, manual consistency review, and public behavior checks are reported separately.

Raw inputs, current sources/previews, pre-code snapshots, red/green logs, independent behavior checks, review snapshots/deltas, hashes, final handoffs, and scope-preservation evidence are retained in the maintainer's detailed-design acceptance workspace. No fixture commits, pushes, deployments, or remote tracker writes were performed.

### Limits

The JSON gate checks declared views, local references, evidence, and readiness; it does not interpret UML semantics or automatically detect stale content. Syntax/render/profile success is not whole-design certification. These observations cover the tested macOS environment, dependency revisions, agent executions, and selected behaviors. Other operating systems, older interpreters, remote integrations, concurrency, persistence/recovery, performance, and arbitrary future generated programs require their own relevant acceptance.

## Previous corrected candidate — 2026-10-29

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
