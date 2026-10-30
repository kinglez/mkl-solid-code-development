# Domain-Independent Forward-Testing Protocol

This protocol evaluates the skill's decisions and producer/consumer contracts. It contains no application scenario, business policy, model, expected business result, or reference implementation. Supply such material independently in an external acceptance workspace; do not copy it into this repository.

## Separate the participants and inputs

1. Freeze the candidate skill and the externally supplied requirement sources. Give an executor only the source requirements, authorized task scope, relevant environment, and candidate skill. Withhold previous solution artifacts and evaluator-held expected outcomes when assessing a fresh execution.
2. An independent evaluator derives or verifies observable expectations from the authoritative requirements without consulting the new implementation. Distinguish reused expectations from freshly derived ones and preserve sources.
3. Give independent requirements and standards reviewers the same fixed final snapshot, source requirements, applicable standards, and actual check evidence. Record the exact scope and any unexamined layers.
4. Keep inputs, generated applications, models, behavioral vectors, logs, snapshots, and detailed reports outside the distributable skill. A repository-level summary may report generic mechanisms and execution boundaries without embedding the external scenario.

## Evaluate the seven-stage chain

| Stage | Observable assessment |
| --- | --- |
| Requirements clarification | Questions target real uncertainty. Answers retain sources. Supplied decisions, proposals, assumptions, and unresolved issues remain distinct; no interview or approval is invented. |
| Requirements baseline | Scope, actors/goals, rules, constraints, use-case behavior, and independent observable expectations have a stated basis. Missing behavior-changing decisions keep dependent work unready. |
| Analysis | Agreed terms, conceptual relationships, BCE responsibilities, and flow coverage agree. PDR findings identify their owning source and are resolved or bounded before dependent detailed design. |
| Detailed design | Applicable structure, interaction and state views, semantic contracts, traceability, and CDR inspection support implementation. Specification and dependency-linked slices consume the current design. |
| Coding | Actual code implements current slices. Meaningful behavioral failure, correction, and regression evidence are distinguished from environment/setup failures. Refactoring preserves established behavior and synchronizes affected designs. |
| Change review | Independent requirements and standards reviews inspect the same delivered snapshot, including pending and new files. Corrections have verification and review coverage for their actual delta. |
| Architecture review | The reviewed result is assessed with its relevant callers and dependencies. Retain/adjust decisions explain costs and reconsideration triggers. Implemented architecture changes return through design, checks, and change review. |

## Check stop, return, and repair behavior

- An unresolved necessary rule or missing required upstream result blocks its dependent consumer, while independent work may continue with sufficient inputs.
- A missing required design view, unresolved lifecycle applicability, or unreviewed cross-view contradiction is not presented as ready. Separate the mechanical declarations checked by scripts from semantic inspection.
- An upstream revision identifies affected consumers, invalidates their readiness, and gives revised outputs new identifiers. Consumers cannot remain complete while referring to unready inputs. Reinspect the actual revised content before restoring readiness.
- Setup/presence success is not invocation, a profile-specific diagram check is not universal semantic verification, and a written test plan is not an executed test.
- All tasks verify the full 19-definition installation baseline. Scoped tasks may execute only relevant stages, combine logical results, reuse current evidence with an applicability check, and stop at design-only or review-only endpoints.
- A resume operation reads saved sources, versions, statuses, outputs, unresolved issues, and next consumers instead of reconstructing missing decisions.
- The pre-coding combination `--require-design --require-through HANDOFF_ID` accepts a ready design prefix while future stages remain pending, rejects a declared invalidated producer or an unconfirmed selected rule, and recovers after the producer/rule is repaired. Unrelated future rules and arbitrary stage labels remain supported.
- Local capture either contains the selected changes consistently or explicitly rejects unsupported index flags and sparse states. Git submodule-ignore settings cannot hide an unsupported changed submodule, and display settings must not contaminate the machine-readable patch. CLI diagnostics remain structured for malformed Unicode identifiers.
- Review-only work preserves source and Git state. Local delivery stays within its authorized actions. Actual invocation adapters are named accurately.

## Record actual results

Preserve input versions, candidate identity, output references, commands, exit codes, inspected snapshots, findings, corrections, and limitations in the external workspace. A finite success supports only the checked scope. A protocol description or a ready delivery record does not establish that forward execution occurred, that every semantic defect was found, or that arbitrary generated software is correct.
