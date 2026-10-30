# Seven-Stage Outputs and Handoffs

Every active stage produces a usable result. Its next consumer reads the actual result, checks source version, content, applicability and readiness, and records what it uses. A declaration of completion or a path alone is not a handoff. **No usable, ready output means no dependent advance.** Every executed stage must record its output and the consumer that actually uses it.

## Preparation, stages, and delivery

Preparation identifies scope, endpoint, baseline, all 19 prerequisites, usable repository configuration, selected stages and adapters. It surrounds the seven stages. Final delivery is the terminal output to the user.

| Stage | Input | Required output | Next consumer checks |
|---|---|---|---|
| 1. Requirements clarification | Scoped request and source materials | Source-based answers, conflicts, candidate rules and open questions | Baseline consolidation distinguishes settled content from suggestions |
| 2. Requirements baseline | Clarification and authoritative decisions | Scope/non-goals, confirmed rules/constraints, use-case behavior, independently derived expectations and exclusions/blockers | Analysis has a stable business basis; expected results were not inferred from implementation |
| 3. Analysis | Baseline, use cases, expectations and terminology | Conceptual model, vocabulary/invariants, BCE flow/information-source coverage and PDR results | Detailed design can allocate required behavior without inventing policy |
| 4. Detailed design | Ready analysis/PDR and technical constraints | Class/module and sequence views, applicable state view, contracts/dependencies, SOLID/pattern decisions, CDR results, implementation specification and vertical slices | Coding has consistent design and an unblocked slice with public completion criteria |
| 5. Coding | Ready design, specification, slice and acceptance | Code, actual checks, suitable meaningful red/green, refactoring/retain decision, synchronized design and gaps | Review can inspect delivered behavior and actual dependencies against current inputs |
| 6. Code review | Fixed snapshot, requirements/specification, design, standards and verification | Requirements/standards findings, locations/impact, corrections, rerun evidence, final snapshot and unfinished issues | Architecture review distinguishes verified corrections from unresolved work |
| 7. Architecture review | Reviewed changes, related modules/callers/dependencies and evidence | Scoped conclusion, change/retain decisions, costs/risks, reconsideration triggers and any verified correction loop | Final delivery states the current result and honest limitations |

Follow [routing](optional-skills.md). Installation does not mean execution. This coordinating skill owns requirements-baseline consolidation and independent-expectation preparation; the use-case specifier owns use-case behavior. The later implementation specification preserves references to the business baseline rather than becoming a competing source.

PDR checks the analysis exit; CDR checks the detailed-design exit. Neither replaces post-code requirements/standards review. Scoped technical readiness is distinct from formal acceptance: preserve coverage and decision limits without inventing participants or approval.

Within stage 4, design/CDR → implementation specification → task slices are distinct subresults. Within stage 5, working code/checks → refactoring/current design are distinct subresults. Preserve consumption order even in one document.

## Artifact locations

Use the [task artifact tree](../README.md#task-artifact-tree) for default output names and locations. Keep actual code/tests and shared terminology in established target-project locations. Record each stage's mapping and source versions in the handoff index; an existing document/section is acceptable only when its current content supplies the required result. A full seven-stage run accounts for all seven outputs, with the final consumer being the user.

## Handoff contract

Before advancing, record:

1. **Inputs consumed:** exact preceding results and relevant source versions; the first stage identifies supplied materials.
2. **Result produced:** real rules, model, view, contract, plan, code, check or decision, with source location and usable content.
3. **Readiness:** why the result meets its consumer's needs; distinguish settled content, unresolved questions and verification limits.
4. **Next consumer:** the stage and its required entry checks.

A stage may consume several earlier results as well as its immediate predecessor. Keep original requirements available through design, code and review. For concurrent slices, aggregate stage results or use independent records without inventing task edges to fit a linear index.

Missing or conflicting required input returns to its producer and blocks dependent work. Continue independent work only when its own inputs suffice.

## Scope and result states

Use existing materials, tracker records or named sections of one working document. Diagrams/code/logs stay in appropriate locations; seven stages do not require seven files.

- **Completed:** usable current result and readiness are recorded.
- **Reused:** existing material was read and checked for scope/version; not evidence of a newly executed skill.
- **Skipped:** reasoned non-applicability or scope exclusion, with no claimed output.
- **Pending/blocked:** missing work or input remains explicit; partial results are unready.
- **Invalidated:** source change makes applicability uncertain; recheck before consumption.

Small changes may combine/reuse stages; all tasks still require complete installation. Design-only and review-only requests keep their endpoints. A review report can finish with unresolved findings without claiming implementation completion. A retain-design decision needs reasoning, limitations and reconsideration triggers.

## Change and correction loops

When a rule, concept, view, contract or implementation changes, identify affected consumers, invalidate their results, correct the producer, assign revised output identities/versions, update references and rerun relevant checks. Preserve unaffected work.

Code-review corrections return to the affected producer, behavior verification, design synchronization and snapshot review. Implemented architecture recommendations follow the same loop; an architecture conclusion cannot approve later code that bypassed change review. Final delivery uses the current reviewed result.

The handoff record describes current readiness, not an immutable execution transcript. Keep useful history separately. On resumption, read current inputs, versions, outputs, questions, statuses and next unblocked consumer.

## Mechanical validation and compatibility

Schema-version-1 handoffs accept arbitrary nonempty stage labels. Existing records and historical stage counts retain their behavior; this contract does not require a new schema or exact-count check.

With `--require-handoffs`, the checker requires outputs, valid references/local files, no self/forward references, no consumption of unready outputs, and predecessor-output links between active stages. Skips need reasons and cannot claim results. This is a final-readiness check; pending later stages may correctly leave a pre-code record unready.

Before dependent coding, use `--require-design --require-through HANDOFF_ID` with the actual completed design producer ID. The scoped handoff gate requires ready, connected outputs through that producer; later pending stages do not block it. The design-bundle gate separately requires the selected rules and views to be ready. Final delivery uses `--require-handoffs` for the entire selected chain.

The checker does not select required stages, interpret meaning, establish independent expectations, authenticate freshness, prove inputs were read, or automatically invalidate changed content. Assess those semantics separately. `--require-design` alone retains its design-bundle-only meaning; see [delivery tools](delivery-record.md).
