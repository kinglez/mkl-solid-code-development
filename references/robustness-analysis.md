# Robustness Analysis: Connecting Use Cases to Responsibility Design

Use robustness analysis to locate responsibilities, verify information sources, or trace normal and exceptional behavior. Establish the system scope and one target use case before modeling; keep the diagram focused on that use case.

## Identify three analysis roles

| Role | Identification question | Typical responsibility or representation |
|---|---|---|
| Boundary | Through what does the system interact with people or external systems? | User interfaces, request entry points, webhook receivers, message consumers, and external-system adapters |
| Entity | What information carries domain meaning, state, or constraints in this use case? | Domain concepts, values, state, and relationships; not automatically database tables or ORM types |
| Control | What coordinates interactions and information to perform the use case's decisions or actions? | Coordinating behavior, checking constraints, and directing outcomes; not automatically framework controller classes |

Nouns and verbs are clues for finding candidates. Fields, transport markers, and supporting actions do not necessarily need separate objects. The same external system can play different roles under different system scopes; state the scope before assigning roles.

## Map behavior to responsibilities, then check the mapping

1. List relevant use-case steps, including inputs, sources, rules, and outcomes.
2. Identify boundary, entity, and control responsibilities step by step. Follow normal, alternative, and exceptional paths to determine what handles each step, returns results, and retains state.
3. Establish the authority and validity of each decision-relevant fact using the current task's requirements. Distinguish submitted data from authoritative facts; clarify the source when it is unresolved.
4. Check in both directions: every responsibility needs support from a use case or confirmed rule, and every required behavior needs an assigned responsibility. Feed newly discovered concepts back into the domain model and unresolved meanings back into requirements clarification.
5. Draw a robustness diagram when it helps explain collaboration. Use other views for timing, concurrency, state changes, and detailed calls.

The minimum useful trace is **use-case behavior → responsibility and information source → acceptance scenario**. Reuse existing identifiers; a simple task does not require a new numbering scheme.

## Connection conventions and limits

Classic ICONIX/BCE analysis views typically show actors interacting through boundaries, boundaries and entities collaborating through control responsibilities, and controls collaborating with other controls. A direct boundary-to-entity connection should trigger a check for a missing processing responsibility.

These are conventions for this analysis view, not universal dependency restrictions for UML or production code. Domain entities may have relationships and collaborate. A robustness diagram does not require all business rules to live in control classes; detailed design should place invariants in the appropriate domain objects or business functions.

## Complete analysis and hand off to detailed design

- Boundaries may become interaction entry points or adapters. Distinguish transport validation from domain constraints.
- Entity candidates may become values, domain objects, or state models, according to their actual invariants.
- Control responsibilities may be allocated to coordinating functions, domain behavior, or module internals. A verb is not a reason to create a class.
- Domain views explain concepts and relationships; static views explain modules, contracts, and dependencies; sequence or state views explain collaboration and where failure stops progress. Choose the view that answers the current question.
- Derive tests from business rules, scenarios, boundary conditions, and state transitions. There is no fixed correspondence between control objects and tests.

Use `mkl-pdr-review` to compare the baseline/use-case flows, conceptual model and robustness coverage before stage 4. Preserve coverage, located findings, required corrections and a scoped technical disposition; absent formal evidence or a decision maker cannot be invented as approval.

When using a diagram validator, report what it actually checks. Valid node connections do not establish complete business coverage, trustworthy facts, or correct exception handling.
