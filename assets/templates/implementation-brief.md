# Eight-Stage Delivery Brief — Draft

Use this document or the project's existing equivalent. Record actual results and sources; a completed-looking table is not evidence. Combine sections or record checked reuse when appropriate.

## Preparation: request, scope, and capabilities

Identify original materials, intended endpoint, relevant repository instructions, change baseline, complete 20-skill availability, current-session access, usable configuration, selected stages and named adaptations. Preserve existing choices; distinguish installation from execution.

## Eight-stage handoff index

For each active stage, identify consumed source/version, usable result/location, readiness/limits and next consumer. A ready, usable output is required before dependent work advances. Map the task artifact tree documented in the installed skill's README to actual project locations; empty paths or completion labels are insufficient. Status is pending, completed, reused, skipped, blocked or invalidated. Skips need reasons and no produced result.

| Stage | Inputs consumed | Actual output and location | Status, readiness and limits | Next consumer |
|---|---|---|---|---|
| 1. Requirements clarification | Original request/materials and scoped preparation | | pending | Requirements baseline |
| 2. Requirements baseline | Clarified sources and decisions | | pending | Analysis |
| 3. Analysis | Baseline, use cases, expectations and vocabulary | | pending | High-level architecture |
| 4. High-level architecture | Ready analysis/PDR, qualities and platform constraints | | pending | Detailed design |
| 5. Detailed design | Ready architecture, quality constraints and analysis/PDR | | pending | Coding |
| 6. Coding | Ready design, specification, unblocked slice and acceptance | | pending | Code review |
| 7. Code review | Fixed delivered-change snapshot and current inputs | | pending | Architecture review |
| 8. Architecture review | Reviewed changes, related modules/callers and evidence | | pending | Final delivery to user |

## Requirements clarification and baseline

Preserve question/answer sources in any supplied form, confirmed rules, constraints, scope/non-goals and remaining uncertainty. Assess functional and non-functional dimensions; reuse settled answers and prioritize only consequential open questions. Record use-case basic/alternative/exception behavior and acceptance expectations derived from requirements. Identify independent evaluation context where available; do not infer expected results from code. Keep test-adapter conventions separate from business decisions.

## Analysis and PDR

Record current domain concepts, shared terminology, invariants and BCE flow/information-source coverage. Link PDR findings, corrections, coverage and technical disposition. Return missing concepts to the model and missing rules to requirements; do not silently fill gaps.

## High-level architecture and quality

Link selected context/container/component/deployment sources, available previews and
checked reuse. Identify authoritative data, access boundaries, communication, ownership,
alternatives, costs and detailed-design constraints. Link quality scenarios with source,
status, observable criterion and verification method. Unknown numeric targets stay open.
Record cross-view review and unresolved decisions with affected work; mark readiness
honestly. System scope normally has context/container views; bounded modules do not need
an invented system. C4 level 4 is code, and deployment is a supporting view.

## Detailed design, CDR, specification and slices

State detailed/lightweight depth and why. Trace relevant requirements/use cases through architecture constraints, responsibilities, interactions, owned operations/events, applicable state effects and acceptance.

| Design result | Actual source or response section | Produced/reused/skipped and why | Check/review evidence and limits | Consumer |
|---|---|---|---|---|
| Class or explicit module structure | | pending | | Interaction/allocation |
| Principal and relevant alternative/failure sequences | | pending | | Operations/acceptance |
| State applicability and necessary lifecycle view | | pending assessment | | Interaction/state checks |
| Contracts, dependencies and SOLID/pattern decisions | | pending | | Cross-view review |
| CDR consistency findings/corrections/disposition | | pending | | Implementation specification |
| Implementation specification and public test seams | | pending | | Vertical slice planning |
| Verifiable slices and real blocking edges | | pending | | Coding |

State applicability is required, not applicable or unresolved, with its source-based reason. Required views and necessary design questions must be resolved before dependent coding. Syntax/render success is not semantic completeness. Record actual technical readiness separately from formal approval.

When using the JSON record, record the detailed-design producer's stable handoff ID and check it with `--require-architecture --require-design --require-through HANDOFF_ID` using the installed validator. The architecture/quality bundle, detailed-design mapping and its producer prefix must be ready; later coding/review may stay pending. Every selected design rule must be confirmed. Preserve the actual command, result and remaining semantic limits.

## Coding, verification and refactoring

Link delivered code, actual commands/results, suitable meaningful red/green checks, coverage and gaps. Record observed design friction and refactoring or justified retain decisions. Synchronize affected views/contracts with implemented operations, dependencies and transitions.

## Code review and corrections

Identify the actual upstream/local route, fixed snapshot and its scope. Give requirements and standards axes the same snapshot/current inputs; record whether contexts are independent. Link located findings, required corrections, reruns and delta review. Later edits need new review coverage.

## Architecture review and final delivery

State inspected modules/callers/dependencies, scoped retain/adjust decisions, costs/risks and reconsideration triggers. Implemented recommendations return through affected design/coding, verification and change review. Deliver linked current outcomes and limitations to the user.

## Changes and resumption

Identify changed upstream results, impacted consumers, invalidated outputs, revised identities/versions, required rechecks, independent work and next unblocked consumer. Preserve historical evidence separately; this index states current readiness.
