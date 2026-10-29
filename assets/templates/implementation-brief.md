# Delivery and Stage-Handoff Brief — Draft

Use this document or the project's existing equivalent. Keep actual results and source references; a completed-looking table is not evidence. Each executed stage produces the next active stage's input. Combine sections for a small change and explain reuse or skips without inventing work.

## Request, scope, and baseline

Record the original request/materials, task intent, relevant repository guidance, change baseline, prerequisite/setup state, and selected stages. Identify the final deliverable and stages outside scope.

## Stage handoff index

For each selected stage, fill in its actual input reference, produced result/location, readiness and limits, and next consumer. Status is pending, completed, reused, skipped, blocked, or invalidated. Replace draft cells with real content; skipped rows need a reason and no claimed result.

| Stage | Inputs consumed | Actual output and location | Status, readiness, and limits | Next consumer |
|---|---|---|---|---|
| Scope and prerequisites | Original request and project evidence | | pending | Business clarification |
| Business clarification | Scope output | | pending | Domain modeling |
| Domain modeling | Confirmed rules and scenarios | | pending | Robustness analysis |
| Robustness analysis | Flows, concepts, and invariants | | pending | Module/interface design |
| Module/interface design | Responsibility coverage and constraints | | pending | Specification |
| Specification | Rules, models, and contracts | | pending | Task slicing |
| Task slicing | Specification and dependencies | | pending | Implementation |
| Implementation and verification | An unblocked slice and its acceptance | | pending | Refactoring |
| Refactoring | Code, contracts, and check results | | pending | Change review |
| Change review and corrections | Final diff, specification, and evidence | | pending | Architecture reassessment |
| Architecture reassessment | Reviewed changes and related callers | | pending | Final delivery |
| Final delivery | Current artifacts, decisions, and evidence | | pending | User |

## Business and domain outputs

Record confirmed rules and their sources, actors and flows, acceptance scenarios, agreed terms, concepts/relationships, and invariants. Separate proposals, assumptions, and open questions. Reuse existing material by linking its relevant section and current version.

## Responsibility and design outputs

Record boundary/entity/control responsibilities and normal/failure coverage, unresolved model deltas, module responsibilities, contracts, dependencies, and justified SOLID/pattern trade-offs. Add diagrams where useful. State what specification and implementation must preserve.

## Specification and slice outputs

Connect rules, design constraints, acceptance, and public verification entry points in the specification. Record verifiable slices, true blocking dependencies, and the current unblocked slice. Keep unresolved decisions and dependent work explicit.

## Implementation, refactoring, and review outputs

Link actual code changes and commands/results. State behavior preserved during refactoring, design decisions or reasons to retain the design, review findings, corrections, rerun evidence, and unresolved issues. Keep each logical output distinguishable even when stored here.

## Architecture and delivery outputs

Record the scoped architecture conclusion, change/retain decisions, trade-offs, and reconsideration triggers. Deliver outcomes with links to current artifacts and real evidence. Distinguish evidence of behavior from evidence about contracts or structure.

## Changes, blockers, and next handoff

Identify changed upstream results, affected consumers, invalidated outputs, necessary rechecks, and independent work that can continue. State the exact current input/output references and next consumer for resumption.
