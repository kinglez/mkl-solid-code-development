---
name: mkl-solid-code-development
license: Apache-2.0
description: >-
  Develop new features or evolve existing code from business requirements through
  responsibility and interface design, implementation, verification, and review.
  Use when the user needs SOLID code that meets business requirements and is
  understandable, extensible, and maintainable. Scale the work to the change
  and respect design-only and review-only requests.
---

# MKL · Business-Driven SOLID Code Development

Connect business rules, responsibility allocation, code behavior, and verification evidence into a traceable delivery workflow. Use Matt Pocock Skills as the preferred execution framework and `mkl-uml-robustness-diagram` for robustness analysis. Install the required skill set before using the integrated workflow.

## Verify prerequisites

Read [Workflow prerequisites and skill routing](references/optional-skills.md). Verify the 12 core skills (11 Matt Pocock Skills plus `mkl-uml-robustness-diagram`) before the integrated workflow. Detailed design additionally needs the existing MKL design-class and sequence skills: use `scripts/check_prerequisites.py --profile detailed-design` with actual roots to check all 14. For plugin installations, resolve the corresponding installed definitions. Installation, availability in the current session, and per-repository setup are separate checks.

Install missing skills through a supported installer within the user's authorization, preserving existing customizations, then check again. If installation or activation is unavailable, report the missing prerequisite and pause dependent stages; continue justified independent work without claiming that the integrated workflow ran. Before tracker-dependent stages, read [repository setup compatibility](references/repository-setup.md) and check the actual tracker, domain conventions, and status vocabulary consumed downstream. The 12-skill baseline excludes `triage`; the named local setup adapter fills the resulting configuration gap without repeatedly running unchanged setup.

Use the installed skills for the stages they cover, read their instructions, and respect explicit-only invocation. A short task still needs only its relevant stages. Installation does not authorize commits, tracker publication, or deployment.

## Establish the scope

Read applicable repository instructions, requirements, terminology, existing code, and verification entry points. Identify the current gap. Before implementation, capture an appropriate change baseline or file state so the review can distinguish existing work from this task's changes. Follow the project's language, structure, and sound existing designs. Match the endpoint to the request: implementation includes code, appropriate verification, and review corrections; design-only and review-only requests end with their respective deliverables.

Choose the depth according to impact, ambiguity, and risk:

- **Small changes:** Reuse established rules and design. Make the local change, run suitable checks, and review the affected scope. Keep necessary explanations in the response or existing task record.
- **New use cases or complex changes:** Use the detailed-design path: establish business rules and acceptance, resolve responsibility and interface questions through actual structure and interaction views, assess lifecycle behavior, and implement verifiable slices.
- **Changes spanning modules or systems, or involving complex state:** Also examine authoritative sources, state transitions, failure paths, compatibility, and consistency of side effects. Add interaction or state views as needed.

Resolve routine technical choices using established rules, repository conventions, and the user's authorization. For unresolved decisions that affect business meaning, acceptance, or significant design trade-offs, present concrete scenarios, alternatives, and a recommendation for clarification. Pause only the work that depends on the answer; continue justified, independent work. Authorization to implement, refactor, or review does not automatically authorize commits, publication, deployment, or remote writes.

## Produce an output at every stage

Follow [Stage Outputs and Handoffs](references/workflow-handoffs.md). Every executed stage must produce a usable result that becomes the next active stage's input:

| Stage | Output passed forward |
|---|---|
| Scope and prerequisites | Scoped request, baseline, capabilities, and selected stages |
| Business clarification | Confirmed rules, flows, acceptance scenarios, and open questions |
| Domain modeling | Agreed concepts, relationships, terminology, and invariants |
| Robustness analysis | Boundary/entity/control responsibilities and behavior coverage |
| Module and interface design | Class/module and sequence views, state view when applicable, contracts, cross-view review, and justified trade-offs |
| Implementation specification | Implementable scope, design decisions, acceptance, and test seams |
| Task slicing | Verifiable slices, blocking edges, and slice completion criteria |
| Implementation and verification | Code changes, checks actually run, coverage, and remaining gaps |
| Refactoring | Final code and regression evidence, or a justified retain-design decision |
| Change review | Findings, necessary corrections, rerun evidence, and remaining issues |
| Architecture reassessment | Scoped architecture conclusion and maintenance decisions |
| Final delivery | Linked outcomes, current artifacts, evidence, trade-offs, and limitations |

Before the next stage starts, read the actual preceding output, check that it supplies the required information, and record the result reference and readiness. Identify original request/materials for the first active stage. If required input is incomplete, return to its producer instead of silently inventing it. Upstream changes invalidate affected downstream results until rechecked.

Keep these outputs in existing project materials or named sections of one document; they do not require one file per stage. Reused results need a current applicability check. Skipped stages need a reason and produce no invented result. Small changes may combine stages, while design-only and review-only requests retain their endpoints. Every active stage still has explicit inputs, an output, and a consumer; the final consumer is the user.

## 1. Turn requirements into verifiable business rules

Identify actors, goals, system scope, authoritative sources, and normal, alternative, and exceptional behavior. Use concrete inputs and outcomes to resolve ambiguity in units, rounding rules, precedence, state, and repeated operations.

Distinguish **confirmed rules, proposals, assumptions, and open questions**, and retain their sources. Surface conflicts and the behavior they affect; existing code is not automatically the business source of truth. Reuse the project's glossary and record newly agreed meanings in the appropriate place. Keep business definitions separate from implementation mappings.

Derive task-specific rules from the current request, applicable project materials, and confirmed decisions. Treat teaching examples, previous tasks, and examples in other skills as illustrations, not default requirements or acceptance criteria.

**Input:** The scoped request and supplied project evidence. **Output:** Confirmed rules, scenarios, sources, and open questions for domain modeling.

**Completion criterion:** Behavior within the implementable scope has an explicit basis and acceptance scenarios. The impact of unresolved questions is clear. AI recommendations do not substitute for business answers that are required to proceed.

## 2. Discover responsibilities before choosing code structure

First make the domain output explicit: agreed terms, concepts, relationships, and invariants derived from confirmed rules. Update the existing glossary/model or relevant section; keep unresolved meanings visible.

When responsibilities, information sources, or failure handling are unclear, use `mkl-uml-robustness-diagram` with the [robustness analysis guidance](references/robustness-analysis.md). Use its standalone mode unless a cross-artifact MKL handoff or formal gate is requested. Identify boundary interactions, domain information, and control responsibilities. Then check the diagram or responsibility list against the use case to uncover omissions and ambiguity.

Analysis roles suggest responsibilities; they do not map one-to-one to files or classes. Allocate responsibilities to functions, classes, or modules according to actual reasons for change, state constraints, and collaboration. A responsibility list can explain simple behavior; use diagrams for complex collaboration.

Define the interface contract callers need: input meaning, units, constraints, outputs, failure semantics, and relevant side effects or ordering requirements. Encapsulate complexity behind a clear interface. Introduce extension points when justified by actual substitution, external dependencies, test isolation, or comparable needs.

Read [Design Views](references/design-views.md). For detailed design, produce or check current **design class models (or a justified module/component view for non-OO code)** and **sequence diagrams** for the principal and relevant alternative/failure paths. Add a **state diagram** when lifecycle transitions determine legal operations or outcomes; record a reasoned applicability decision and resolve unknown state rules before dependent work. Other views answer specific scoped questions. A bounded correction may use a justified lightweight path; honor any explicitly requested views.

Iterate the actual views together. Trace use-case/BCE responsibilities to interactions, owned operations or events, state effects where applicable, and acceptance. Verify participant/operation contracts and state names, guards, and effects consistently; replies and signals are not mechanically ordinary methods. Use the installed class/sequence skills in standalone mode by default and the available project UML toolchain for state views. Keep edits and missing-render limitations explicit.

For structural decisions currently being made, read [SOLID and design-pattern trade-offs](references/solid-design.md). Translate principles into concrete change scenarios and review questions.

**Inputs:** Rules and domain output. **Outputs:** Robustness coverage, actual applicable design views, contracts, consistency review, and trade-offs for specification.

**Completion criterion:** Required views are present or checked as current; relevant behavior, responsibilities, interactions, contracts, and lifecycle rules agree. No implementation-changing design question in scope remains unresolved. New abstractions have stated benefits, costs, and limitations. With structured records, use `--require-design` to check declared design readiness before coding; it is separate from final delivery readiness and does not establish semantic correctness.

## 3. Hand off the design and implement verifiable slices

Use an existing task, specification, or concise brief to connect business rules and scope, necessary design constraints, acceptance scenarios, observable public verification entry points, dependencies, and open questions. One document may be sufficient; fixed filenames and a full document set are optional.

Select the implementation route before starting. The upstream `implement` workflow reviews before committing, while its selected `code-review` compares committed history. For an implementation with pending local changes, use the [local implementation and two-axis review adapter](references/local-review.md): keep the agreed slices and `tdd`, review a fixed snapshot of the actual delivered changes, and stop at local delivery unless further actions are authorized. Identify this as the adapter rather than claiming unmodified execution of `implement`.

Split implementation into verifiable business outcomes, each including the code and checks needed for that outcome. Derive dependencies from actual data, behavior, and integration requirements. Reuse completed work rather than rebuilding it to fit a process.

Where suitable automation exists, use a short feedback loop for significant new or corrected behavior: run a check that exposes the gap, observe a meaningful failure, implement the smallest sufficient change, and run regression checks. Build, dependency, and environment failures are not evidence of a business-behavior failure. Match verification to the task; simple renames and presentation-only changes may warrant other checks instead of mandatory TDD.

Treat specification, task slicing, and implementation as separate logical handoffs, even when stored together. The specification feeds the task plan; the current unblocked slice feeds implementation; verified code and actual check results feed refactoring.

**Completion criterion:** Each slice implements its rules and design constraints, with appropriate checks actually run. Unexecuted or uncovered checks and their implications are explicit.

## 4. Refactor and review the actual code

Before choosing a refactoring, locate duplicated decisions, scattered responsibilities, inconsistent contracts, and actual dependency use. Preserve behavior within the request's scope; align intentional behavior changes with business rules. Rerun the necessary affected checks after refactoring.

Keep the design views synchronized with the implemented operations, participants, dependencies, and state transitions. A refactor or rule change invalidates affected view reviews until they are rechecked; final delivery includes the current views and their relation to the code.

Review two distinct axes:

- **Requirements conformance:** Are the rules, success and failure behavior, scope, and acceptance scenarios implemented faithfully?
- **Standards and design:** Does the code follow repository standards, terminology, responsibilities, contracts, and agreed dependencies? Follow execution paths to verify that declared abstractions are actually used.

Before review, inspect the current change state and read [local review inputs](references/local-review.md). Use the upstream review only when its committed diff includes the intended delivered changes. For staged, working-tree, or untracked changes, use the named local adapter and pass the same fixed snapshot, specification, and standards to independent reviewers. Confirm task scope rather than attributing every existing local edit to this task. After a correction, capture and review the changed snapshot again.

For each actionable finding, provide evidence, a precise location, impact, and a way to verify the correction. Distinguish business defects, design deviations, coverage gaps, and optional improvements. Correct issues within the authorized scope, then check the affected behavior. Missing coverage alone does not establish a defect; matching types alone does not establish substitutability.

**Inputs:** The working implementation, contracts, and verification baseline. **Outputs:** The refactoring result/decision feeds change review; the review and correction results feed architecture reassessment.

**Completion criterion:** Necessary, evidence-backed corrections within scope are resolved or explicitly reported as unfinished. Verification results and remaining limitations are clear.

## 5. Reassess the surrounding architecture and deliver evidence

Examine the final change in the context of related modules and callers. Check that responsibilities, duplication, and dependencies remain coherent. A small change may need only a local reassessment; broader investigation needs an explicit scope or supporting evidence. Retaining the current design is a valid decision: explain its limitations and what would trigger reconsideration. Keep design costs proportional to the problem being solved.

**Input:** Reviewed changes and their current evidence. **Output:** The architecture conclusion feeds the final delivery package; that package is the user-facing terminal output.

Tailor the final delivery to the task, covering:

- Completed behavior or design and its location.
- Checks actually run and their results, distinguishing **evidence of business behavior** from **evidence about contracts or structure**.
- Unverified areas, unresolved business questions, unfinished work, and their implications.
- Trade-offs that affect maintenance and, where useful, triggers for reconsideration.

Keep completion claims within the evidence. Test counts, diagram validation, and a SOLID checklist do not prove whole-system correctness. Performance claims require measurements. When verification is blocked, report actual progress and limitations rather than marking unexecuted checks as passed.

## Executable tools and templates

For structured handoffs or mechanical traceability checks, read [delivery records and tools](references/delivery-record.md):

- `scripts/check_prerequisites.py` checks the 12-skill core or 14-skill detailed-design profile in explicitly supplied roots. It performs no installation or skill execution.
- `scripts/capture_review.py` captures an explicitly scoped Git change for local review without staging or committing. Read [its contract](references/local-review.md) before use.
- `scripts/init_delivery.py` initializes a record, optionally selects a design profile and creates a brief, and refuses to overwrite existing files.
- `scripts/validate_delivery.py` checks declared references/states and evidence. Use `--require-design` for pre-implementation design readiness and `--require-handoffs` for final stage-chain completion. It neither executes recorded commands nor determines UML/SOLID correctness.
- `assets/templates/` contains reusable delivery-record and implementation-brief templates. Existing project materials do not need to be migrated into these formats.
- `tests/` contains script regressions, positive and negative fixtures, and forward-testing scenarios. Run regressions when maintaining the scripts; add relevant scenario-based verification when changing the core decision process.

Use these resources when they help; their presence does not require every small change to create additional files.

## Route work to the installed skills

Use [the routing table](references/optional-skills.md) to hand off work to the verified core and conditional modeling capabilities. Read their instructions and supply current rules, scope, artifacts, and acceptance. Installation does not select every stage; the chosen design depth determines required views. Beyond the detailed class/sequence pair, further domain/use-case modeling aids remain optional.

Communicate in the user's language. Follow project conventions for code and document naming. For long tasks, preserve confirmed rules, the current slice, design decisions, actual verification results, and next steps in the existing work record so a later session can resume from the remaining gap.
