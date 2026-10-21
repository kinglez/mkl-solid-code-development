---
name: mkl-solid-code-development
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

Read [Workflow prerequisites and skill routing](references/optional-skills.md). Verify all 12 required skills (11 Matt Pocock Skills plus `mkl-uml-robustness-diagram`) in the target environment before starting the integrated workflow. For filesystem installations, use `scripts/check_prerequisites.py` with the actual skill roots; for plugin installations, inspect the agent's installed-skill catalog and resolve the definitions. Installation, availability in the current session, and per-repository setup are separate checks.

Install missing skills through a supported installer within the user's authorization, preserving existing customizations, then check again. If installation or activation is unavailable, report the missing prerequisite and pause dependent stages; continue justified independent work without claiming that the integrated workflow ran. Before stages that need repository configuration, confirm that `setup-matt-pocock-skills` has configured the target project's tracker and domain-document conventions.

Use the installed skills for the stages they cover, read their instructions, and respect explicit-only invocation. A short task still needs only its relevant stages. Installation does not authorize commits, tracker publication, or deployment.

## Establish the scope

Read applicable repository instructions, requirements, terminology, existing code, and verification entry points. Identify the current gap. Before implementation, capture an appropriate change baseline or file state so the review can distinguish existing work from this task's changes. Follow the project's language, structure, and sound existing designs. Match the endpoint to the request: implementation includes code, appropriate verification, and review corrections; design-only and review-only requests end with their respective deliverables.

Choose the depth according to impact, ambiguity, and risk:

- **Small changes:** Reuse established rules and design. Make the local change, run suitable checks, and review the affected scope. Keep necessary explanations in the response or existing task record.
- **New use cases or complex changes:** Establish business rules and acceptance scenarios, resolve responsibility and interface questions, and implement verifiable slices. Add diagrams and documents where they support a decision, handoff, or verification.
- **Changes spanning modules or systems, or involving complex state:** Also examine authoritative sources, state transitions, failure paths, compatibility, and consistency of side effects. Add interaction or state views as needed.

Resolve routine technical choices using established rules, repository conventions, and the user's authorization. For unresolved decisions that affect business meaning, acceptance, or significant design trade-offs, present concrete scenarios, alternatives, and a recommendation for clarification. Pause only the work that depends on the answer; continue justified, independent work. Authorization to implement, refactor, or review does not automatically authorize commits, publication, deployment, or remote writes.

## 1. Turn requirements into verifiable business rules

Identify actors, goals, system scope, authoritative sources, and normal, alternative, and exceptional behavior. Use concrete inputs and outcomes to resolve ambiguity in units, rounding rules, precedence, state, and repeated operations.

Distinguish **confirmed rules, proposals, assumptions, and open questions**, and retain their sources. Surface conflicts and the behavior they affect; existing code is not automatically the business source of truth. Reuse the project's glossary and record newly agreed meanings in the appropriate place. Keep business definitions separate from implementation mappings.

Derive task-specific rules from the current request, applicable project materials, and confirmed decisions. Treat teaching examples, previous tasks, and examples in other skills as illustrations, not default requirements or acceptance criteria.

**Completion criterion:** Behavior within the implementable scope has an explicit basis and acceptance scenarios. The impact of unresolved questions is clear. AI recommendations do not substitute for business answers that are required to proceed.

## 2. Discover responsibilities before choosing code structure

When responsibilities, information sources, or failure handling are unclear, use `mkl-uml-robustness-diagram` with the [robustness analysis guidance](references/robustness-analysis.md). Use its standalone mode unless a cross-artifact MKL handoff or formal gate is requested. Identify boundary interactions, domain information, and control responsibilities. Then check the diagram or responsibility list against the use case to uncover omissions and ambiguity.

Analysis roles suggest responsibilities; they do not map one-to-one to files or classes. Allocate responsibilities to functions, classes, or modules according to actual reasons for change, state constraints, and collaboration. A responsibility list can explain simple behavior; use diagrams for complex collaboration.

Define the interface contract callers need: input meaning, units, constraints, outputs, failure semantics, and relevant side effects or ordering requirements. Encapsulate complexity behind a clear interface. Introduce extension points when justified by actual substitution, external dependencies, test isolation, or comparable needs.

For structural decisions currently being made, read [SOLID and design-pattern trade-offs](references/solid-design.md). Translate principles into concrete change scenarios and review questions.

**Completion criterion:** Relevant business behavior and success and failure outcomes have assigned responsibilities. Sources, contracts, and dependencies are explainable. New abstractions have stated benefits, costs, and limitations.

## 3. Hand off the design and implement verifiable slices

Use an existing task, specification, or concise brief to connect business rules and scope, necessary design constraints, acceptance scenarios, observable public verification entry points, dependencies, and open questions. One document may be sufficient; fixed filenames and a full document set are optional.

Split implementation into verifiable business outcomes, each including the code and checks needed for that outcome. Derive dependencies from actual data, behavior, and integration requirements. Reuse completed work rather than rebuilding it to fit a process.

Where suitable automation exists, use a short feedback loop for significant new or corrected behavior: run a check that exposes the gap, observe a meaningful failure, implement the smallest sufficient change, and run regression checks. Build, dependency, and environment failures are not evidence of a business-behavior failure. Match verification to the task; simple renames and presentation-only changes may warrant other checks instead of mandatory TDD.

**Completion criterion:** Each slice implements its rules and design constraints, with appropriate checks actually run. Unexecuted or uncovered checks and their implications are explicit.

## 4. Refactor and review the actual code

Before choosing a refactoring, locate duplicated decisions, scattered responsibilities, inconsistent contracts, and actual dependency use. Preserve behavior within the request's scope; align intentional behavior changes with business rules. Rerun the necessary affected checks after refactoring.

Review two distinct axes:

- **Requirements conformance:** Are the rules, success and failure behavior, scope, and acceptance scenarios implemented faithfully?
- **Standards and design:** Does the code follow repository standards, terminology, responsibilities, contracts, and agreed dependencies? Follow execution paths to verify that declared abstractions are actually used.

For each actionable finding, provide evidence, a precise location, impact, and a way to verify the correction. Distinguish business defects, design deviations, coverage gaps, and optional improvements. Correct issues within the authorized scope, then check the affected behavior. Missing coverage alone does not establish a defect; matching types alone does not establish substitutability.

**Completion criterion:** Necessary, evidence-backed corrections within scope are resolved or explicitly reported as unfinished. Verification results and remaining limitations are clear.

## 5. Reassess the surrounding architecture and deliver evidence

Examine the final change in the context of related modules and callers. Check that responsibilities, duplication, and dependencies remain coherent. A small change may need only a local reassessment; broader investigation needs an explicit scope or supporting evidence. Retaining the current design is a valid decision: explain its limitations and what would trigger reconsideration. Keep design costs proportional to the problem being solved.

Tailor the final delivery to the task, covering:

- Completed behavior or design and its location.
- Checks actually run and their results, distinguishing **evidence of business behavior** from **evidence about contracts or structure**.
- Unverified areas, unresolved business questions, unfinished work, and their implications.
- Trade-offs that affect maintenance and, where useful, triggers for reconsideration.

Keep completion claims within the evidence. Test counts, diagram validation, and a SOLID checklist do not prove whole-system correctness. Performance claims require measurements. When verification is blocked, report actual progress and limitations rather than marking unexecuted checks as passed.

## Executable tools and templates

For structured handoffs or mechanical traceability checks, read [delivery records and tools](references/delivery-record.md):

- `scripts/check_prerequisites.py` checks required skill definitions in explicitly supplied filesystem roots. It performs no installation or skill execution.
- `scripts/init_delivery.py` initializes a record from packaged templates, optionally creates an implementation brief, and refuses to overwrite existing files.
- `scripts/validate_delivery.py` checks references and declared states across rules, acceptance, design, evidence, and review. It neither executes recorded commands nor determines SOLID compliance.
- `assets/templates/` contains reusable delivery-record and implementation-brief templates. Existing project materials do not need to be migrated into these formats.
- `tests/` contains script regressions, positive and negative fixtures, and forward-testing scenarios. Run regressions when maintaining the scripts; add relevant scenario-based verification when changing the core decision process.

Use these resources when they help; their presence does not require every small change to create additional files.

## Route work to the installed skills

Use [the skill routing table](references/optional-skills.md) to hand off relevant work to the verified Matt Pocock Skills and the required robustness-analysis skill. Read the selected instructions and supply the current rules, scope, artifacts, and acceptance criteria. Required installation does not make every stage or diagram mandatory. Other MKL use-case and UML skills remain optional.

Communicate in the user's language. Follow project conventions for code and document naming. For long tasks, preserve confirmed rules, the current slice, design decisions, actual verification results, and next steps in the existing work record so a later session can resume from the remaining gap.
