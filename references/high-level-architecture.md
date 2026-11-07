# High-Level Architecture: Analysis to Detailed Design

Use in stage 4. Read the installed `mkl-uml-c4-architecture` definition and its relevant
references. It owns C4 modeling; this coordinating skill owns the input/output chain.

## Entry and scope

For full development, consume the requirements baseline, quality scenarios, terminology,
domain/BCE models, PDR findings and applicable platform/current-system constraints.
Check their current source versions and unresolved decisions. The PDR result is analysis
evidence, not a C4 review. Return missing policy to requirements and missing concepts to
analysis before dependent decisions become ready.

An architecture-only request can start from supplied requirements or existing-system
evidence. Preserve that endpoint, perform the applicable comparisons, and mark missing
upstream evidence partial. Do not fabricate a completed PDR or require detailed classes,
sequences, code or tracker publication to produce useful scoped architecture work.

## Choose the views

| Scope | Required result | Conditional depth |
|---|---|---|
| System | Context, containers, quality assessment and decisions | Components for important internal allocation; deployment for runtime placement/failure boundaries |
| Bounded module/component | The scoped structure and its checked host context or explicit boundary mapping; quality assessment | Use an actual component/module/code view rather than inventing applications around a library |
| Lightweight correction | Checked architecture reuse, relevant delta and quality-impact assessment | Add a diagram only when the change or request needs it |

The four C4 levels are **context, container, component and code**. Deployment is a
supporting view. A container is an application or data store, not a mandate for Docker,
microservices or a new database. Reuse the existing stack and storage where suitable;
record alternatives, constraints and reasons when a change is justified.

Code-level zoom normally uses UML design classes or a scoped module/function view.
It is optional during high-level work. Sequences explain behavior alongside the static
level-4 structure and are developed in detailed design when that scope is selected.

## Decide and inspect

Allocate responsibilities, external interfaces and communication meaning. Identify data
ownership/source of truth, access/trust boundaries, consistency needs, failure paths,
operational ownership and relevant deployment constraints. Keep stable element identities
across views; repeated labels alone do not establish correspondence.

For each important decision, record its requirement/quality source, alternatives,
selected approach, affected elements, costs, detailed-design constraint and validation
strategy. Use [the requirements assessment](requirements-quality.md) rather than inventing
quality figures. Unknown criteria can remain open when they do not prevent the scoped
decision; required unresolved architecture decisions block their dependent work.

Use the installed C4 validator's supported profile and actual inputs. Prefer authorized
local rendering with bundled `C4/C4_Context`, `C4/C4_Container`, `C4/C4_Component` and
`C4/C4_Deployment` includes. Keep editable sources and available previews together.
Separate literal-profile checks, PlantUML syntax, rendering, visual inspection and
semantic review. An unavailable renderer is an explicit gap; do not silently upload
project sources. A green checker or diagram is not architecture acceptance.

## Exit and next input

Produce an architecture brief or existing equivalent linking:

- Current input identities, scope, selected views and checked reuse.
- Responsibility/data/interface ownership, decision trade-offs and access boundaries.
- Quality scenarios, validation strategy, open targets and blocking decisions.
- Requirement → decision → element/view → detailed-design constraint.
- Actual checks/review, findings/corrections, technical readiness and limitations.

Detailed design reads this result and maps components/responsibilities to technical
modules/types, sequences, owned operations/events and lifecycle behavior. CDR inspects
the actual correspondence within its available coverage. Its current class/sequence
CLI does not validate C4 or accept an invented architecture flag; inspect that layer
semantically and preserve the result. Class-only review keeps its scoped manual route.

For optional records, initialize `--architecture-profile system`, `bounded` or
`lightweight`. A `quality` view links the actual quality assessment document; all
profiles require inspected quality evidence, not invented metrics. Use
`--require-architecture --require-through HANDOFF_ID` at the architecture exit. Before
coding use `--require-architecture --require-design --require-through HANDOFF_ID` with
the detailed-design producer's ID. See [record fields](delivery-record.md#architecture-views-and-readiness).

If sources change, recheck affected decisions/views and invalidate impacted design,
implementation and review results until corrected. Final architecture review compares
the implemented system with this baseline and the actual quality evidence.
