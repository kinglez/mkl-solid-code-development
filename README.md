# MKL SOLID Code Development

**Turn business requirements into understandable, extensible, maintainable, and reviewable code.**

An agent skill connecting requirements, conceptual analysis, detailed design, implementation, and two levels of review. It combines Matt Pocock Skills with MKL UML Skills and follows the target project's language and conventions.

[Workflow](#seven-stage-workflow) · [Install](#install-and-verify) · [Use](#start-a-task) · [Outputs](#stage-outputs) · [Verification](#verification-and-boundaries)

## Problems it addresses

| Problem | Workflow response |
| --- | --- |
| Ambiguous requirements become silent coding assumptions. | Resolve concrete scenarios, preserve sources, and establish a requirements baseline. |
| Code has no clear responsibility boundaries. | Analyze concepts and boundary/entity/control responsibilities before allocating technical operations. |
| Diagrams, acceptance, and code describe different behavior. | Trace rules through behavior, responsibilities, interactions, operations, and observable checks. |
| Interfaces and patterns add unnecessary complexity. | Evaluate actual variations, caller needs, semantic substitution, and dependency ownership. |
| Review checks style but misses business deviations. | Review the same fixed change snapshot independently for Spec and Standards. |
| A local improvement creates architectural friction. | Inspect related callers and dependencies, then verify necessary corrections. |

## Seven-stage workflow

![Seven stages, their skills and usable outputs: clarification, requirements baseline, analysis, detailed design, coding, code review, architecture review.](assets/diagrams/workflow.svg)

Preparation establishes scope, the change baseline, installed capabilities, and applicable configuration. Final delivery collects reviewed outcomes and evidence. They wrap the seven stages.

| Stage | Skills and responsibility | Output consumed next |
| --- | --- | --- |
| **1. Requirements clarification** | `grill-with-docs` | Answers with sources, conflicts, proposals, and open questions. |
| **2. Requirements baseline** | This skill coordinates; `mkl-use-case-specifier`; `mkl-uml-use-case-diagram` when useful | Scope, rules, quality constraints, use-case behavior, and independently derived expected outcomes. |
| **3. Analysis** | `mkl-uml-domain-modeler` leads; `domain-modeling` sharpens concepts when needed; `mkl-uml-robustness-diagram`; exit: `mkl-pdr-review` | Shared vocabulary, conceptual relationships, BCE responsibilities, behavior coverage, and analysis review. |
| **4. Detailed design** | `codebase-design`, `mkl-uml-sequence-diagram`, `mkl-uml-design-class-model`, `mkl-cdr-review`; then `to-spec`, `to-tickets` | Reviewed structure, interactions, applicable lifecycle model, contracts, implementation specification, and vertical slices. |
| **5. Coding** | `implement`, `tdd`; named local adapter when needed | Code, actual behavior checks, refactoring decisions, and synchronized design. |
| **6. Code review** | `code-review`; fixed-snapshot two-axis adapter for pending files | Findings, corrections, regression evidence, and reviewed snapshot. |
| **7. Architecture review** | `improve-codebase-architecture` | Scoped change/retain decisions, costs, risks, and reconsideration triggers. |

`grilling` supports clarification; `setup-matt-pocock-skills` supplies configuration when required. Installation does not execute a stage. Respect each skill's invocation contract and name any adapter actually used.

### Keep the stage boundaries clear

The **requirements baseline** states what behavior is required and why. This skill consolidates confirmed sources; the use-case specifier describes normal, alternative, and exception flows. A separate evaluator derives acceptance expectations from requirements, without using implementation output as the answer.

The **implementation specification** records the agreed realization and verification after detailed design. `to-spec` consolidates established decisions; `to-tickets` creates verifiable slices. These may be distinct sections of one maintained document.

Analysis identifies business concepts and responsibilities. MKL leads the conceptual model; Matt's domain-modeling discipline resolves ambiguity in the same shared vocabulary. BCE roles do not require one implementation class each.

Detailed design allocates technical operations and collaboration. New use cases and complex changes normally require a **class model or justified module view**, **sequence diagrams**, and an explicit **state applicability decision**. Produce a state diagram when lifecycle rules determine legal operations or outcomes. Iterate these views together.

![Structure, interactions, lifecycle applicability and contracts are checked together before implementation planning.](assets/diagrams/design-views.svg)

PDR checks analysis consistency; CDR checks detailed-design consistency. Scoped technical review is the default. Formal acceptance needs the applicable evidence and actual decision maker; a validator cannot supply it.

### Return corrections to their source

Missing input returns to its producer. Upstream changes invalidate affected downstream results until rechecked. Coding includes testing and refactoring. If architecture review changes code, revisit affected design, implementation, regression checks, and change review before closing delivery.

Small changes can reuse current results, combine adjacent outputs, or justify skips. Design-only and review-only requests retain their endpoints. **Every task still requires the complete prerequisite installation.** Seven stages do not mean seven files or seven automatic human approval pauses.

## Install and verify

![Install the complete skill set, verify current availability, reuse or configure setup, execute relevant stages, and inspect actual evidence.](assets/diagrams/how-to-use.svg)

### 1. Install this skill and both complete upstream collections

Use the standard [Skills CLI](https://skills.sh/docs/cli) in the target project and select your agent:

```bash
npx skills add kinglez/mkl-solid-code-development
npx skills add mattpocock/skills --skill '*'
npx skills add kinglez/mkl-uml --skill '*'
```

`--skill '*'` selects every skill in each upstream repository; choose your target agent in the installer. Install the complete collections once and reuse a valid installation. The **19 named workflow prerequisites** (11 Matt and 8 MKL, excluding this skill) are the minimum set checked by this workflow, not the total number installed. Additional upstream skills remain available without being automatically executed. State diagrams use the available project UML toolchain; no dedicated MKL state skill is assumed.

Reuse valid installations, preserve customizations, and use one route per agent. Cross-repository dependencies are not installed automatically. Project-scoped installation is the default; add `-g` for user-wide installation. See [dependency and distribution details](references/compatibility.md).

### 2. Verify definitions and session availability

#### Prerequisite checker runtime

From the installed skill directory, prepare the optional checker's PyYAML runtime:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Supply real directories containing `skill-name/SKILL.md`; these are command templates:

```bash
.venv/bin/python scripts/check_prerequisites.py --skills-root path/to/skills
.venv/bin/python scripts/check_prerequisites.py --skills-root path/to/project-skills --skills-root path/to/global-skills --profile full-workflow
```

Default **full-workflow** checks all 19 definitions. Exit `0`: readable matching frontmatter names; `1`: missing/invalid definitions; `2`: invalid input/runtime. It performs no installation or execution and does not prove activation, provenance, setup, or rendering.

Explicit legacy profiles **core** (12) and **detailed-design** (14) remain for compatibility and diagnosis. **Their success does not satisfy the complete workflow prerequisite.** Check session availability separately; plugin installations may use the host's catalog and definition access.

### 3. Reuse or configure repository setup

Read actual project guidance and saved configuration. Explicitly use `setup-matt-pocock-skills` when needed, then check tracker, document conventions, and downstream status vocabulary using the [setup contract](references/repository-setup.md). Reuse valid configuration. Work without tracker-dependent stages does not require a new tracker setup.

## Start a task

Supply requirements, relevant evidence, and the intended endpoint:

> Use mkl-solid-code-development to implement the supplied requirements. Establish the requirements baseline and independent acceptance expectations, review analysis and detailed design, implement verifiable slices, and deliver actual checks, change review, and a scoped architecture review.

Invoke explicit-only skills through the host's supported mechanism when selected; follow the [host launch checklist](references/optional-skills.md#host-launch-checklist). Definition reading, installation, and completed execution are different actions. Identify local adapters accurately. Installation does not authorize tracker publication, commits, pushes, or deployment.

For pending local changes, the [implementation/review adapter](references/local-review.md) fixes the tracked and untracked delivery against a baseline. Both independent reviewers consume the same snapshot, requirements, design, and standards. Use upstream committed-history review when it covers the intended change.

For design-only or review-only work, preserve that endpoint. On resumption, read actual outputs, versions, statuses, and the next consumer before advancing.

## Stage outputs

![A logical output tree with seven branches, from clarification and requirements through analysis, design, code, change review, and architecture conclusions.](assets/diagrams/stage-outputs.svg)

**Every executed stage must produce an inspectable, usable output. Its next consumer must read that output and confirm readiness before advancing. Missing, conflicting, or unready output blocks dependent work.** A stage name, empty directory, completion label, or promise to produce a file is insufficient.

### Task artifact tree

This is the recommended layout in the **target project**, separate from this skill's own repository layout shown later. Reuse established project locations and document the mapping in `handoffs.md`; the required content and producer/consumer links remain mandatory. Existing documents can hold several named sections instead of one new file per item.

```text
target-project/
├── GLOSSARY.md                         Shared vocabulary; reuse existing context layout
├── docs/delivery/<task>/
│   ├── handoffs.md                     Input versions, outputs, readiness and consumers
│   ├── 01-clarification/
│   │   └── clarification.md            Questions, source-based answers and open decisions
│   ├── 02-requirements/
│   │   ├── requirements.md             Rules, scope, constraints and exclusions
│   │   ├── use-cases.md                Basic, alternative and exception flows
│   │   ├── ACCEPTANCE_ORACLE.md        Requirement-derived expected outcomes
│   │   └── use-cases.puml              When an actor/system-boundary view is useful
│   ├── 03-analysis/
│   │   ├── domain.puml                 Conceptual model using shared vocabulary
│   │   ├── robustness.puml             Boundary/entity/control responsibilities
│   │   ├── coverage.md                Behavior and information-source correspondence
│   │   └── pdr-review.md               Findings, corrections and analysis readiness
│   ├── 04-design/
│   │   ├── classes.puml                Or a justified module view
│   │   ├── sequences/                  Principal and relevant failure interactions
│   │   ├── lifecycle-assessment.md     State-model applicability and its reason
│   │   ├── state.puml                  When lifecycle behavior requires it
│   │   ├── contracts.md                Interfaces, dependencies and design trade-offs
│   │   ├── cdr-review.md               Cross-view findings, corrections and readiness
│   │   ├── implementation-spec.md      Realization and verification decisions
│   │   └── tickets/                    Verifiable slices and blocking dependencies
│   ├── 05-coding/
│   │   ├── implementation.md           References to actual code and test locations
│   │   ├── verification.md             Executed checks, results and remaining gaps
│   │   └── refactoring.md              Changes or justified retention; design sync
│   ├── 06-code-review/
│   │   ├── review-input.md             Baseline, immutable snapshot location and identity
│   │   ├── spec-review.md              Requirements conformance
│   │   ├── standards-review.md         Standards and design
│   │   └── corrections.md              Fixes, reruns and review of the changed snapshot
│   ├── 07-architecture-review/
│   │   └── architecture-review.md      Scope, retain/adjust decision, costs and triggers
│   └── delivery-summary.md             Current outcomes and evidence for the user
├── src/                                Actual implementation; follow the project layout
└── tests/                              Actual behavior/contract tests; follow its layout
```

Editable diagram sources and rendered previews stay together where available. A conditional view needs either its actual output or a justified non-applicability decision. `src/`, `tests/`, glossary locations, and filenames follow existing project conventions; coding artifacts are not relocated into documentation. For the Git capture helper, keep immutable snapshot bytes **outside the checkout** and reference them from `review-input.md`. Independently held assessment vectors stay with their evaluator when a blind evaluation is required; the public acceptance contract remains available to downstream stages.

### Producer and next consumer

| Producer | Required output | Next consumer |
| --- | --- | --- |
| 1. Clarification | Answers, sources, conflicts and open decisions | 2 builds the requirements baseline from them. |
| 2. Requirements baseline | Requirements, use-case behavior and independent expected outcomes | 3 analyzes the behavior; design, coding and review retain these sources. |
| 3. Analysis | Shared vocabulary, domain/BCE coverage and PDR result | 4 allocates technical collaborations from the ready analysis. |
| 4. Detailed design | Current views/contracts, CDR, implementation specification and slices | 5 implements an unblocked slice and its acceptance. |
| 5. Coding | Actual code/tests, execution results, refactoring outcome and current design | 6 reviews the delivered change against its requirements and design. |
| 6. Code review | Same-snapshot Spec/Standards reports, corrections and rerun evidence | 7 evaluates the reviewed implementation in its surrounding structure. |
| 7. Architecture review | Scoped conclusion, costs, triggers and verified adjustments | Final delivery and the user consume the current results. |

Record **inputs consumed, actual output, readiness and limits, and next consumer** at every handoff. Reuse requires a current applicability check; a justified skipped stage claims no output; a full seven-stage development run must account for all seven results. Upstream changes invalidate affected consumers until rechecked. See [handoffs](references/workflow-handoffs.md) and the [brief template](assets/templates/implementation-brief.md).

## Optional delivery-record tools

Delivery tools use Python 3.10+ and the standard library; review capture also needs Git. Initialize a draft using actual paths and identifiers:

```bash
python3 scripts/init_delivery.py path/to/delivery --id TASK-1 --summary "Delivery objective" --intent implement --design-profile detailed --with-brief
```

Populate actual rules, view sources, applicability, evidence, and handoffs. Before coding, replace `HANDOFF_ID` with the completed detailed-design producer's actual ID:

```bash
python3 scripts/validate_delivery.py path/to/delivery/delivery-record.json --require-design --require-through HANDOFF_ID
```

`design_ready` checks the design bundle, including confirmation of every selected rule. `through_ready` checks the handoff prefix through that ID, including its upstream inputs. Both must pass before dependent coding; later coding/review may remain pending and `record_ready` may still be false. `--require-design` alone remains a bundle-only check. After implementation, corrections, and reviews:

```bash
python3 scripts/validate_delivery.py path/to/delivery/delivery-record.json --require-design --require-handoffs
```

Initialization refuses overwrites. The validator checks declarations, references and evidence; it never executes recorded commands, interprets UML semantics, or automatically detects stale content. Older records retain their stage names/count and schema meaning. See [delivery records](references/delivery-record.md).

## Verification and boundaries

Run domain-neutral regressions from the skill directory with the checker runtime prepared:

```bash
.venv/bin/python -m unittest discover -s tests -v
```

Checks cover prerequisites, parsing, evidence paths, generic handoffs, scoped readiness, initialization, and local review capture. The [CI workflow](.github/workflows/tests.yml) runs the suite on Linux and macOS with Python 3.10 and 3.14 when pushed or opened as a pull request; configured jobs are distinct from observed CI results. Structural fixtures are synthetic protocol data, not application requirements or actual delivery evidence. See [verification evidence](tests/ACCEPTANCE.md) and the [generic evaluation protocol](tests/behavioral-cases.md).

**This skill's source repository and installed directory, including its tests, are business-independent.** Ordinary task artifacts belong in the user's target application. When maintaining or evaluating this skill itself, keep application requirements, business vectors, named use cases, generated applications, and their end-to-end evidence in separate acceptance workspaces outside the skill repository/package. The target application can contain its own business requirements, code and tests.

Tests, diagrams and records support bounded conclusions, not SOLID certification, whole-system correctness, formal business acceptance, or production readiness. Measure performance before making performance claims; report gaps explicitly.

```text
SKILL.md                  Seven-stage agent entry point
agents/                   Skill metadata
references/               Handoffs, routing, design, setup and tool contracts
scripts/                  Prerequisite checks and delivery tools
assets/diagrams/           Business-independent workflow and output views
assets/templates/          Reusable records and brief
tests/                    Domain-neutral regressions and protocol fixtures
requirements.txt          YAML parser dependency
LICENSE, NOTICE, licenses/ Authorization and third-party notices
```

## License

Apache-2.0; see [LICENSE](LICENSE) and [NOTICE](NOTICE). Independently installed dependencies retain their licenses; see [distribution guidance](references/compatibility.md).
