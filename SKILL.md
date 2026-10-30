---
name: mkl-solid-code-development
license: Apache-2.0
description: >-
  Develop or evolve code through requirements clarification, a requirements
  baseline, analysis, detailed design, coding, change review, and architecture
  review. Use for business-correct SOLID code that remains understandable,
  extensible, maintainable, and reviewable. Scale execution to the task and
  respect design-only, review-only, and local-delivery scope.
---

# MKL · Business-Driven SOLID Code Development

Connect business meaning, responsibilities, executable behavior, and review evidence through seven stages. Each active stage consumes real prior results and produces a usable output. Preparation and final delivery surround the stages; testing and refactoring are part of coding.

## Prepare scope and capabilities

Read [prerequisites and routing](references/optional-skills.md). Install both upstream skill collections in full and reuse valid installations. **Every task using this skill requires all 19 named workflow prerequisites**, including design-only and review-only work; the full collections can contain additional skills. The default `full-workflow` checker profile checks those 19 named minimum definitions, not the entire upstream collections. Explicit legacy `core` and `detailed-design` profiles remain partial compatibility diagnostics; neither establishes integrated-workflow readiness.

Verify installation, session availability, and repository configuration separately. Reuse valid installations/setup. Install missing capabilities through a supported installer within the user's authorization, preserving customizations. If installation or activation is unavailable, identify the missing capability and pause dependent work without claiming the integrated workflow ran. Read [repository setup](references/repository-setup.md) before consumers use tracker or domain configuration.

Read applicable repository instructions, source requirements, terminology, existing code, and verification entry points. Record scope, endpoint, sources, and an appropriate change baseline before implementation. Follow the project's language and established structure. Complete installation does not require complete execution: small corrections can reuse current requirements/design and combine adjacent outputs; new use cases or complex changes normally need the full analysis and detailed-design path.

Read selected skills and respect invocation/authorization rules. Installation or reading a definition is not execution. Use the named local setup/implementation/review adaptations when upstream contracts do not fit the host or local delivery, and identify the actual route. Installation does not authorize commits, tracker publication, pushes, or deployment.

## Maintain the stage chain

Follow [Stage Outputs and Handoffs](references/workflow-handoffs.md). **Every active stage must produce an inspectable, usable result that becomes a later consumer's input. No ready output means no dependent advance.** Before advancing, read the actual preceding result, check current content/source version, and record input, output, readiness, and next consumer. Use the [task artifact tree](README.md#task-artifact-tree) when choosing output locations; reuse established project paths with an explicit mapping.

| Stage | Result passed forward |
|---|---|
| 1. Requirements clarification | Source-based answers, conflicts, candidate rules, and open questions |
| 2. Requirements baseline | Scope, confirmed rules/constraints, use-case behavior, acceptance expectations, and explicit exclusions |
| 3. Analysis | Shared vocabulary, conceptual domain model, BCE coverage, and PDR findings/disposition |
| 4. Detailed design | Structural/sequence/applicable state views, contracts, CDR results, implementation specification, and vertical slices |
| 5. Coding | Working code, actual checks, refactoring result, and synchronized design |
| 6. Code review | Requirements/standards findings, verified corrections, and final reviewed snapshot |
| 7. Architecture review | Scoped structural conclusion, change/retain decisions, costs, and reconsideration triggers |

Missing required input returns to its producer. An upstream change invalidates affected downstream results until rechecked. Reuse requires reading and checking applicability; skips need a reason and produce no fictitious output. These are logical stages, not seven required files or repeated automatic approvals. Final delivery has the user as its consumer.

## 1. Clarify requirements

Use `grill-with-docs` for unresolved business meaning, subject to its invocation rules. Identify actors, goals, authoritative sources, scope, constraints, and normal/alternative/exceptional behavior. Probe ambiguous rules through concrete situations and consequences. `domain-modeling` sharpens terminology as it changes; keep implementation decisions outside the glossary.

Separate **confirmed content, proposals, assumptions, conflicts, and open questions**, retaining their sources. Existing code is not automatically the intended behavior. If supplied materials already settle a question, record the source-based answer; do not invent a live interview, decision maker, or approval.

**Input:** Scoped request and supplied materials.

**Output:** Clarification results and sources for stage 2.

**Exit check:** Uncertainty and its affected work are explicit. Resolve routine technical choices through established conventions; ask about decisions that affect business meaning, acceptance, or significant trade-offs.

## 2. Establish the requirements baseline

This coordinating skill consolidates the **requirements baseline**: goals, scope/non-goals, confirmed rules, constraints, failure behavior, sources, and remaining questions. It states required behavior before technical design, distinct from the implementation specification in stage 4.

Use `mkl-use-case-specifier` to express bounded goals as observable basic, alternative, and exception flows with preconditions, postconditions, and acceptance criteria. Use `mkl-uml-use-case-diagram` when actor participation and system boundaries need a diagram; installation remains required when no such view is needed. Keep baseline and use cases consistent, returning discovered business questions to stage 1.

Derive concrete expected outcomes directly from requirements, independently of implementation results or design choices. When independent evaluation is supported, give a separate evaluator the source requirements and keep its assessment criteria separate from the executor's work. Preserve expected values, derivations, source versions, and coverage limits. If only one context is available, disclose that limitation rather than claim independence. Serialization and test-adapter conventions are later technical contracts, not retroactive business rules. Never derive expected results by calling the code under test.

**Input:** Clarified sources and decisions.

**Output:** Baseline, use-case behavior, and acceptance expectations for analysis and later verification; existing materials or named sections can hold them.

**Exit check:** Current implementable behavior has an explicit basis and necessary business decisions are resolved. Unresolved scope stays specifically blocked or excluded with a reason. AI recommendations do not substitute for required business answers.

## 3. Analyze concepts and responsibilities

Use `mkl-uml-domain-modeler` as the primary conceptual modeling capability. Derive concepts, values, relationships, and invariants from the baseline. Use Matt's `domain-modeling` when terms are ambiguous, conflict with glossary/code, or change during work. Maintain one shared vocabulary/model instead of competing interpretations.

Use `mkl-uml-robustness-diagram` with [robustness guidance](references/robustness-analysis.md) to identify boundary/entity/control responsibilities, authoritative information, and success/failure coverage. Feed missing concepts back into the domain model and missing business policy back to stages 1–2. A discovered responsibility does not authorize inventing a rule.

Use `mkl-pdr-review` for the analysis exit check: compare actual requirements/use-case behavior, concepts, and BCE coverage. Preserve located findings, corrections, coverage and disposition. Default to scoped technical review; formal acceptance needs its applicable evidence and designated decision maker.

**Input:** Current baseline, use cases, expectations, and terminology.

**Output:** Domain/vocabulary, BCE flow coverage, and PDR results for detailed design.

**Exit check:** Relevant behavior has an assigned responsibility and information source; use cases, concepts, and responsibilities agree. Necessary analysis findings are corrected or affected design work remains unready.

## 4. Design the implementation and slices

Use `codebase-design` to allocate responsibilities by actual reasons for change, state constraints, collaboration, and dependency ownership. BCE roles do not map one-to-one to files/classes/controllers. Define input/output meaning, units, preconditions, failures, and relevant side effects/order. Add abstractions for real variation, external dependencies, or justified test seams.

Follow [Design Views](references/design-views.md). In detailed design, use `mkl-uml-sequence-diagram` and `mkl-uml-design-class-model` to refine interactions and operation ownership together. Use an explicitly identified module/component alternative for non-OO code. Assess lifecycle applicability; add a state view when transitions determine legal behavior, otherwise record the source-based reason. Other views answer specific questions.

Trace **requirement/use-case behavior → BCE responsibility → interaction → owned operation/event → relevant state effect → acceptance**. Check principal and relevant alternative/failure paths across actual views. Replies, signals, and internal construction are not mechanically ordinary methods. Apply [SOLID/pattern trade-offs](references/solid-design.md) to concrete changes, caller needs, and semantic substitution.

Use `mkl-cdr-review` to inspect detailed-model, contract, operation-allocation, behavior, and test-design consistency. Separate scoped technical readiness from formal acceptance. Once necessary design findings are resolved, use `to-spec` to consolidate the **implementation specification**: baseline references, design decisions, acceptance, public verification seams, dependencies and blockers. Use `to-tickets` for verifiable vertical slices, real blocking edges and completion criteria. Respect invocation/tracker/publication requirements and identify local adaptations.

**Input:** Ready analysis/PDR results and technical constraints.

**Output:** Current views/contracts, design/CDR decisions, implementation specification, and slices.

**Exit check:** Required views exist or were checked as current, relevant contracts agree, and no implementation-changing design question remains unresolved. Specification and slices consume that ready design. With JSON records, combine `--require-design` with `--require-through` using the actual detailed-design handoff ID before coding. This checks both the design bundle and its ready stage prefix while future coding/review may remain pending; semantic correctness still requires inspection.

## 5. Code, verify, and refactor

Use `implement` and `tdd` through the selected [local or upstream route](references/local-review.md). Pending local changes use the named implementation/two-axis review adaptation, not a claim of unmodified upstream execution.

Work one unblocked business slice at a time. Where suitable automation exists for significant new/corrected behavior, observe a meaningful failing behavior check, implement the smallest sufficient change, and run relevant regression checks. Import, dependency and build failures are not behavioral red evidence. Preserve actual commands, outputs, coverage and gaps.

Refactor observed duplicated decisions, scattered responsibilities, inconsistent contracts, or dependency friction. Preserve intended behavior and rerun affected checks. A justified retain-design decision is valid. Synchronize affected structural, interaction, state, contract and traceability results with code.

**Input:** Ready design, specification, slice, and acceptance expectations.

**Output:** Working code, actual verification/refactoring evidence, and current design for review.

**Exit check:** Implemented slices meet their rules/completion criteria with appropriate checks actually run. Missing or unexecuted checks and implications remain explicit.

## 6. Review the actual change

Use `code-review` when its committed-history input covers the intended delivery; otherwise use the [fixed-snapshot local adapter](references/local-review.md). Both axes receive the same snapshot, requirements/specification, relevant design, standards and verification:

- **Requirements:** faithful scope, rules, success/failure behavior and acceptance.
- **Standards/design:** conventions, terminology, responsibilities, contracts, actual dependency use and justified abstractions.

Use independent contexts when supported; label separate passes honestly otherwise. Confirm task scope and preserve unrelated edits. Give findings a location, evidence, impact and verification approach. Correct necessary issues within scope, rerun affected checks, capture the revised snapshot, and review the delta. Missing coverage alone is not a defect; matching types alone is not substitutability.

**Input:** Delivered change, current requirements/design, and verification baseline.

**Output:** Findings, verified corrections, final snapshot identity and unfinished issues.

**Exit check:** Necessary corrections are closed or explicitly unfinished. Prior snapshots cannot approve later edits. Review-only work may finish with a report while findings remain unresolved.

## 7. Review the surrounding architecture

Use `improve-codebase-architecture` within its invocation contract and the task's scope. Inspect reviewed code with relevant modules, callers and real dependencies. Assess cohesion, scattered decisions, duplication, interface depth, abstraction cost and supported change scenarios. Local changes may warrant local reassessment; broader conclusions need broader evidence.

Record a reasoned **retain or adjust** decision, costs/risks and reconsideration triggers. Architecture was already designed before coding; this stage checks the implemented result in context.

If an architecture recommendation is implemented, return to the affected requirements/analysis/design/coding stage, invalidate impacted results, synchronize views, rerun checks, and repeat change review on the revised snapshot. Close only after this loop or explicitly leave remaining work unready.

**Input:** Reviewed changes, current evidence, related callers/dependencies and remaining issues.

**Output:** Scoped architecture conclusion and current delivery evidence.

**Exit check:** Conclusions match the inspected scope; implemented corrections have current behavior/review evidence.

## Deliver, resume, and use tools

Deliver linked outcomes, current artifacts, checks actually run, correction/review results, trade-offs and unfinished work with implications. Distinguish behavior evidence from structural/contract checks. Test counts, rendered views and declared readiness do not certify correctness or SOLID; performance claims need measurements.

Preserve current sources, readiness, next unblocked stage and questions in the existing task record. On resumption, read those artifacts instead of trusting prior completion claims.

Read [delivery records/tools](references/delivery-record.md) when structured traceability helps. The prerequisite checker reads definitions without installing/executing them; review capture snapshots scoped Git changes without staging/committing; initialization refuses overwrites; validation checks declared references, evidence and readiness without executing commands or interpreting UML meaning. Before coding, use `--require-design --require-through HANDOFF_ID` with the current design producer's ID; use `--require-handoffs` for final selected-stage completion. `--require-design` alone checks only the design bundle. Existing schema-version-1/arbitrary-stage records retain their meanings. The [brief](assets/templates/implementation-brief.md) can hold the index without seven documents.

## Keep this skill package domain-independent

This boundary applies to this skill's own source repository and installed skill directory: its instructions, references, templates, scripts and tests contain reusable workflow mechanisms and neutral structural fixtures only. Store task-specific requirements, expected outcomes, code and tests in the user's target project or authorized acceptance workspace. When evaluating this skill itself, keep that task material outside the skill repository and package. The target application is allowed to contain its own business artifacts; do not copy them back into the skill as defaults or verification fixtures.
