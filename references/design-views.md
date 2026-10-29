# Design Views: From Responsibilities to Implementable Contracts

Read this during scope selection, after robustness analysis, and before specification or implementation. Its output is an agreed design supported by actual views and cross-checks, not a list of diagrams to draw later.

## Select the depth from the task

**Detailed design is the default for a new use case or a complex change to responsibilities, interfaces, collaborations, or lifecycle behavior.** Produce or explicitly reuse the structural and interaction views below. Assess lifecycle applicability even when no state diagram is needed.

**Lightweight design** fits a bounded correction that preserves established responsibilities, public contracts, interactions, and lifecycle rules. Read the affected existing design, describe the relevant delta and verification, and explain why new views add no value. A requested diagram remains part of the deliverable even when the code change is small. Reuse means reading and checking the current source; it is not an exemption from design review.

Design-only and review-only requests keep their endpoints. If the user requests response-only work, supply the necessary views and review in the response instead of creating project files. Structured records and file-based checks remain optional.

## Produce the views that answer the design questions

| View | When and what to produce | Next consumer |
|---|---|---|
| Domain concepts | Read the agreed terms, relationships, and invariants. Add a conceptual domain diagram when relationships or boundaries need clarification. Keep implementation types out of the business definitions. | Responsibility analysis |
| Robustness | Use the specified flows to allocate boundary/entity/control responsibilities, authoritative information, and success/failure handling. Reuse a checked existing view where appropriate. | Structure and interaction design |
| Design class model or module view | Required in detailed design. For OO code, show the relevant types, operations, contracts, relationships, and dependency direction. For non-OO code, use an explicitly identified module/component view with public functions and ports instead of inventing classes. | Interaction allocation and implementation |
| Sequence diagrams | Required in detailed design. Show the principal use-case interaction and the relevant specified alternatives/exceptions. Include externally significant ordering, failures, retries, or cancellation only where the rules establish them. Separate views when one becomes unreadable. | Operation allocation, acceptance, and implementation |
| State diagram | Required when an entity or process lifecycle determines legal operations, transitions, or outcomes. Show initial/current/terminal states, events, guards, actions, and specified illegal/repeated-event handling. State applicability that remains unresolved blocks dependent design. | Interaction/operation checks and state-transition tests |
| Other views | Add activity, persistence/ER, component, or deployment views only to resolve a real question within scope. A diagram catalog is not a required output set. | The specific decision or implementation that needs it |

A status field or boolean alone does not establish a lifecycle-modeling need. Check whether its history or transitions change what operations are allowed. Record why a state view is required or not applicable; do not invent business states or silently assume missing transition rules.

## Iterate structure, interactions, and state together

Start with the responsibilities and known contracts. Sketch receiver types/modules, walk the use case through sequences, and refine owned operations and dependencies. If lifecycle behavior is relevant, use the state model to check guards, ordering, results, and side effects. These views constrain one another; they are not a one-pass sequence of independent documents.

For each required flow or rule, keep an explainable trace:

**Rule / use-case behavior → BCE responsibility → interaction → owned operation or event → state effect where applicable → acceptance check.**

Use existing identifiers or a compact cross-reference table. The relationships may be many-to-many; do not invent one class, message, state, or test for every sentence.

Cross-check the actual artifacts:

1. Every relevant normal, alternative, and failure behavior has an assigned responsibility and an interaction or justified existing coverage.
2. Sequence participants map to actual design types/modules or identified external actors/systems. An operation call has a receiver and a compatible operation contract: name, input meaning, return/failure meaning, units, and side effects.
3. Distinguish operation calls from replies, signals, creation, and destruction. Async delivery may use an event/handler mapping; those messages do not all become ordinary receiver methods.
4. State names and events agree across the state model, operations, and interactions. Guards and transition effects respect domain invariants and the confirmed rules, including failure and repeated-event behavior where specified.
5. Dependency direction, abstraction costs, and extension points satisfy the applicable [SOLID questions](solid-design.md). BCE roles do not require a framework controller class or place every invariant in a coordinator.
6. Derive acceptance at stable public seams from behavior, operations, failures, and transitions. Design checks supplement actual behavior tests; they do not replace them.

## Route to available modeling tools

The core prerequisite baseline remains 12 skills. Detailed design additionally requires:

```bash
npx skills add kinglez/mkl-uml --skill mkl-uml-design-class-model mkl-uml-sequence-diagram
```

Verify the selected **14-skill** profile in the target environment. From the installed skill root and prepared Python environment, this is a command template:

```bash
.venv/bin/python scripts/check_prerequisites.py --skills-root path/to/skills --profile detailed-design
```

Use `mkl-uml-design-class-model` for design class models and `mkl-uml-sequence-diagram` for interactions, reading their installed instructions and supported arguments. Their standalone modes remain the default. Supply the actual available use-case, domain, robustness, and related design artifacts; missing sources limit coverage claims. A module view is a stated alternative, not a claim that the class-specific validator verified it. The conceptual domain modeler remains an optional aid when a domain diagram is needed.

For state diagrams, use the project's available UML toolchain, such as PlantUML state syntax and its local renderer. An available `plantuml-skill` can assist, but no dedicated MKL state skill is assumed. Check the renderer separately from skill-definition presence. Preserve source confidentiality and the authorized backend; a missing local renderer does not authorize uploading project sources to a public service.

## Complete and hand off the design

Before specification or implementation consumes it, deliver:

- The selected depth and rationale, state applicability, and confirmed inputs.
- Actual editable view sources or response sections, including version/source references for reuse. Supply rendered previews when available; report an unavailable render as a verification gap and do not claim a visual review.
- Contracts, relevant SOLID/pattern decisions, and the rule-to-view/operation/acceptance cross-references.
- Actual syntax/profile/render results with warnings, skipped coverage layers, manual consistency findings, and unresolved issues. An exit code of zero does not prove every validator layer ran or that the design is semantically correct.

The design is ready only when required views are produced or checked as current, relevant cross-view responsibilities and contracts agree, and implementation-changing questions within its scope are resolved. An unresolved state assessment, missing required view, stale reuse, or unreviewed inconsistency remains unready. Return missing input to its producer and continue only independent work with sufficient inputs.

When using a structured delivery record, see [design-view fields and the pre-implementation gate](delivery-record.md#design-views-and-the-pre-implementation-gate). The mechanical `design_ready` result is separate from final `record_ready`; it checks declarations, local references, and evidence, not UML meaning.

After coding or refactoring, compare the actual implementation to the design. Update affected operation signatures, participants, dependencies, state transitions, and acceptance references; rerun relevant checks and review the final change snapshot. Recheck affected downstream design on an upstream rule change. Final delivery links the current views and the implementation they describe.
