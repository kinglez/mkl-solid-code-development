# Verification Evidence and Boundaries

This repository contains only domain-independent checks of the skill's tools and operating contracts. Application requirements, illustrative business scenarios, generated applications, independent outcome vectors, and their detailed acceptance evidence are kept in separate workspaces and are not part of this package.

## Current seven-stage candidate

The default prerequisite check is `full-workflow`: 19 named definitions for every task. Explicit `core` (12) and `detailed-design` (14) checks retain their historical diagnostic behavior; success in those partial profiles does not satisfy the current integrated workflow's prerequisite baseline. Installation presence does not prove activation, setup, invocation, or a working renderer.

New prerequisite regressions were executed against the previous implementation and observed the incorrect ready result when newly required definitions were absent. The corrected checker passed all 18 prerequisite tests in the maintainer's local verification workspace. This is tool-contract evidence, not execution of the installed skills.

The current script candidate passed **109 distinct regression tests on Python 3.12.14, 3.13.15, and 3.14.7** on macOS. This includes the 101 historical test methods plus four full-workflow prerequisite tests and four generic seven-stage/legacy-chain tests. The prerequisite tests exercise each newly required definition as a missing-input subcase. Seven-stage tests cover readiness, a blocked producer, revised output identifiers, repaired consumer references, and compatibility with twelve-stage records.

The Python 3.13 run required an isolated environment with the declared PyYAML dependency; an earlier unprepared interpreter run is not a product-regression result. This is the script-suite result only. Documentation, diagram, installation and external workflow checks have separate evidence; they are not inferred from this run. Do not inherit historical counts as current candidate results.

## Historical tool verification

Before this refactor, the detailed-design candidate passed 101 distinct script regressions on macOS with Python 3.12.14, 3.13.15 and 3.14.7. Earlier verification recorded 75 regressions before detailed-design tools were added. These are historical observations of their respective revisions, not a claim that the current candidate has already passed on those environments.

The retained tool contracts cover YAML identity and parsing; missing definitions; initialization and cleanup; declared evidence and path containment; generic stage links, readiness and invalidation; design readiness separate from final delivery; and capture of scoped tracked/pending/new Git files without committing. They do not interpret UML meaning, execute recorded commands, automatically prove content freshness, or certify SOLID.

## External workflow verification

Use [the forward-testing protocol](behavioral-cases.md) to test real execution in isolated external workspaces. Check each selected stage's actual input, result, consumer, blockers, revisions and correction loop. Record mechanical, behavioral and semantic review evidence separately. An independent review uses an actual independent context and a fixed shared snapshot; repeated self-checks are not independent review.

## Limits

Execution evidence is limited to the reported candidate, environment, inputs and observed checks. Untested hosts, integrations, performance, recovery, and future generated programs need their own relevant verification. Test counts and a declared ready record are not universal correctness or release certificates.
