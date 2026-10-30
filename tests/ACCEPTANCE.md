# Verification Evidence and Boundaries

This repository contains only domain-independent checks of the skill's tools and operating contracts. Application requirements, illustrative business scenarios, generated applications, independent outcome vectors, and their detailed acceptance evidence are kept in separate workspaces and are not part of this package.

## Current repaired tool contracts

The default prerequisite check is `full-workflow`: 19 named definitions for every task. Explicit `core` (12) and `detailed-design` (14) checks retain their historical diagnostic behavior; success in those partial profiles does not satisfy the current integrated workflow's prerequisite baseline. Installation presence does not prove activation, setup, invocation, or a working renderer.

The suite now covers selected index flags and sparse states being rejected without source/index mutation; explicit rejection of changed submodules despite Git ignore settings; color-free applicable patches for tracked and untracked content; a ready handoff prefix with future work pending; invalidated upstream inputs and repair; confirmation of selected design rules; encoding-safe CLI diagnostics; and existing record compatibility. All fixtures and Git payloads remain neutral protocol data.

Before dependent coding, the current command combines `--require-design` with `--require-through HANDOFF_ID`. The first checks the design bundle; the second checks the selected producer prefix. A valid prefix can pass while `record_ready` is false. An unconfirmed selected rule cannot become ready by changing only its global blocking flag. These are declared mechanical contracts, not proof that a requirement or diagram has correct meaning.

The repository CI configuration selects Linux/macOS and Python 3.10/3.14. A configured matrix is not evidence that those jobs have executed. Preserve actual candidate identity, commands, counts, runtime versions and results in the external verification workspace or corresponding CI run. Distinguish current execution from historical results and do not add repeated interpreter runs into a distinct-test count.

## Historical tool verification

The v2.0.0 script baseline passed 109 distinct regressions on macOS using Python 3.12.14, 3.13.15 and 3.14.7. Its later audit also passed the unchanged 109-test suite on Python 3.10.21, 3.13.15 and 3.14.7, while independently reproducing the six failure modes corrected by this candidate. Those green baseline tests did not cover the newly demonstrated failures.

Before this refactor, the detailed-design candidate passed 101 distinct script regressions on macOS with Python 3.12.14, 3.13.15 and 3.14.7. Earlier verification recorded 75 regressions before detailed-design tools were added. These are historical observations of their respective revisions, not a claim that the current candidate has already passed on those environments.

The retained tool contracts cover YAML identity and parsing; missing definitions; initialization and cleanup; declared evidence and path containment; generic stage links, readiness and invalidation; design readiness separate from final delivery; and capture of scoped tracked/pending/new Git files without committing. They do not interpret UML meaning, execute recorded commands, automatically prove content freshness, or certify SOLID.

## External workflow verification

Use [the forward-testing protocol](behavioral-cases.md) to test real execution in isolated external workspaces. Check each selected stage's actual input, result, consumer, blockers, revisions and correction loop. Record mechanical, behavioral and semantic review evidence separately. An independent review uses an actual independent context and a fixed shared snapshot; repeated self-checks are not independent review.

## Limits

Execution evidence is limited to the reported candidate, environment, inputs and observed checks. Untested hosts, integrations, performance, recovery, and future generated programs need their own relevant verification. Test counts and a declared ready record are not universal correctness or release certificates.
