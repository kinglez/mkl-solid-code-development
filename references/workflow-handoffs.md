# Stage Outputs and Handoffs

Every executed stage produces a usable result. The next active stage reads that result as input, checks its completeness and applicability, and identifies what it will use. A declaration that work is done is not a handoff.

## The delivery chain

The first input is the user's request and applicable project evidence. The final output is delivered to the user. Each row defines a logical result, not a mandatory filename or separate document.

| Stage | Input | Required output | Next consumer checks |
|---|---|---|---|
| 0. Scope and prerequisites | Request, repository guidance, installed capabilities, existing work | Scope, task intent, change baseline, relevant skill/setup availability, and selected stages | Clarification can identify the target behavior and unresolved scope |
| 1. Business clarification | Scope and supplied requirements | Confirmed rules with sources, actors and flows, acceptance scenarios, assumptions, proposals, and open questions | Domain modeling can distinguish agreed business meaning from suggestions |
| 2. Domain modeling | Rules, scenarios, and existing glossary/model | Agreed terms, concepts and relationships, invariants, and unresolved meanings | Robustness analysis can identify domain information without inventing facts |
| 3. Robustness analysis | Flows, rules, domain concepts, and constraints | Boundary/entity/control responsibilities, information sources, success/failure coverage, and model or requirement deltas; a diagram where useful | Interface design can allocate every required behavior, including failure handling |
| 4. Module and interface design | Responsibility coverage, domain constraints, and actual variations | Module responsibilities, interface contracts, dependency direction, relevant static/interaction views, and SOLID/pattern trade-offs | Specification can state implementable decisions and observable verification entry points |
| 5. Implementation specification | Confirmed rules, models, responsibilities, and contracts | Scoped specification with traceable acceptance, design decisions, test seams, dependencies, and unresolved blockers | Ticket planning can divide results without making new business decisions |
| 6. Task slicing | Specification and real dependencies | Verifiable vertical slices, blocking edges, acceptance for each slice, and its verification entry point | Implementation can start an unblocked slice with clear completion criteria |
| 7. Implementation and behavior verification | An unblocked slice plus its referenced rules, design, and acceptance | Actual code changes, rules-to-check coverage, commands/results, relevant red/green evidence, and remaining gaps | Refactoring can identify behavior to preserve and rely on a real verification baseline |
| 8. Refactoring and SOLID assessment | Working code, contracts, baseline results, and observed design friction | Refactored code and regression results with reasons/trade-offs, or an evidence-backed decision to retain the design | Change review can inspect the final diff, behavior, and actual dependency use |
| 9. Change review and corrections | Final diff against a fixed baseline, specification, and verification results | Requirements and standards findings, locations/impact, necessary corrections, rerun results, and remaining issues | Architecture reassessment can distinguish corrected behavior from unresolved work |
| 10. Architecture reassessment | Reviewed changes, callers, dependencies, and remaining issues | A scoped architecture conclusion, change/retain decisions, costs, risks, and reconsideration triggers | Final delivery can state coherent outcomes and honest limitations |
| 11. Final delivery | Reviewed behavior/design, verification, and architecture conclusion | A concise delivery package linking outcomes, current artifacts, evidence, decisions, unfinished work, and maintenance implications | The user can inspect what was delivered and what remains |

Use `grill-with-docs`/`grilling`, `domain-modeling`, `mkl-uml-robustness-diagram`, `codebase-design`, `to-spec`, `to-tickets`, `implement`/`tdd`, `code-review`, and `improve-codebase-architecture` at their corresponding stages, subject to their invocation and authorization requirements. Installation does not mean a stage has executed.

## The handoff contract

Before advancing, record:

1. **Inputs consumed:** exact prior result references and relevant source versions. The first active stage identifies the supplied request/materials instead.
2. **Result produced:** actual rules, model, diagram, contract, plan, code, checks, or decision. Link the source location and include enough content to use it. For a local document, identify the relevant section in the summary; a filename alone is insufficient.
3. **Readiness:** explain why the result meets the next stage's needs. Separate confirmed content, unresolved questions, and verification limits.
4. **Next consumer:** identify which stage uses the result and what it must check before proceeding.

For concurrent slices, aggregate their results in the relevant stage output or use separate records for independent chains. Do not invent task dependencies merely to fit an ordered handoff index.

The recipient reads the referenced material rather than reconstructing it from memory or inventing missing decisions. If required information is missing or inconsistent, return the issue to the producing stage and pause dependent work. Continue independent work only where its inputs are already sufficient.

## Storage and scope

Use the project's existing task/specification, tracker, or a single working document with named sections. Diagrams, code, and logs remain in their appropriate project locations. A small change may use a compact input/output table in the response or task record. These are logical outputs, not a requirement for twelve files.

- **Completed:** Produce the result and record its readiness.
- **Reused:** Read an existing result, check its relevance and current version, and identify it explicitly as reused. Reuse is not evidence of a newly executed skill.
- **Skipped:** Explain why the stage is outside this request or adds no value. Produce no fictitious stage result; the next active stage consumes the last real result.
- **Pending or blocked:** Record the missing input/decision and affected consumers. Partial results remain explicitly unready.
- **Invalidated:** An upstream change has made the result's applicability uncertain; recheck before consuming it.

Design-only requests stop with the requested design and its review. Review-only requests start from the supplied diff/specification and produce findings; unresolved findings do not prevent completion of that review report. A small task may combine adjacent stages in one entry, provided its input, usable output, and next consumer remain explicit. Keep the terminal stage's output for the user even when no later implementation stage is requested.

Refactoring or architecture assessment can conclude that no structural change is warranted. That reasoned conclusion is an output; a blank stage or a bare "no change" is not.

## Changes and resumption

Treat the handoff record as the current plan and result state, not an append-only execution history. When an upstream rule, model, or contract changes, identify affected consumers, mark their results invalidated, and rerun the relevant checks. Give revised results new output IDs and update consumers to those IDs. Preserve useful historical artifacts in the project's existing history or log. Do not leave a consumer completed while its current input is unready.

On resumption, read the saved inputs, result locations, current versions, statuses, open questions, and next consumer. A prior session's completion claim does not replace those materials.

## Optional mechanical validation

When using a delivery record, use the current template's `handoffs` array and validate with `--require-handoffs`. The checker requires completed/reused stages to have outputs, verifies references and local files, rejects forward/self references, blocks unready inputs, and requires each next active stage to consume at least one output of its predecessor. Skips need reasons and cannot claim produced outputs.

The record-level readiness gate is for delivery completion. A draft with pending stages remains unready; use the actual input status and content to decide whether the next stage can start.

This checks the declared chain, not whether a document is semantically complete or whether every required stage has been selected. The agent/reviewer must assess artifact quality, source freshness, scope selection, and whether input was actually read. See [Delivery Records and Tools](delivery-record.md) for fields and compatibility.
