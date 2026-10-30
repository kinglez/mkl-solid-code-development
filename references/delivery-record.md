# Optional Delivery Records and Tools

Use structured records when a task needs handoffs between stages, traceability between acceptance and evidence, or input for downstream tools. Every active stage still needs a usable output for its next consumer. Small changes may record that chain in the response or existing task records; JSON is optional. See [Stage Outputs and Handoffs](workflow-handoffs.md) for the workflow contract.

The tools require Python 3.10+ and use only the standard library. They do not depend on other skills, a package manager, network access, or a project framework.

## Initialize a record

Run from the skill root. This is an executable command template: replace `path/to/new-delivery`, `TASK-1`, and the summary with task-specific values. The template does not represent an actual task execution.

```bash
python3 scripts/init_delivery.py path/to/new-delivery --id TASK-1 --summary "Delivery objective" --intent implement --with-brief
```

This creates `delivery-record.json`; `--with-brief` also creates an implementation-brief template. The initial status is `in_progress`, with no invented rules or verification results. New records include an empty `handoffs` array; populate it with the selected stages as work proceeds. Existing output files are never overwritten; edit an existing record in place where appropriate.

All output is encoded as UTF-8 before directories or files are created. Unencodable task text is rejected with exit code `2`, leaving no output. If a subsequent file write encounters an I/O error, files created by this invocation are removed while pre-existing files are preserved.

The [delivery-record template](../assets/templates/delivery-record.json) and [implementation-brief template](../assets/templates/implementation-brief.md) can also be used directly. They need not be delivered together.

`--design-profile detailed` or `lightweight` optionally adds the [design-view fragment](../assets/templates/design-views.json) to the record. It begins with no views, unresolved lifecycle applicability, and an unperformed review. Replace the draft scope and actual results; initialization does not make a design ready. Omitting the option preserves records without a design bundle.

For that profile, use this initialization alternative rather than the command above:

```bash
python3 scripts/init_delivery.py path/to/new-delivery --id TASK-1 --summary "Delivery objective" --intent implement --design-profile detailed --with-brief
```

## Record format: schema version 1

Field names are checked strictly: unknown fields and duplicate JSON keys are errors. Collections may be empty, so an incomplete draft can still pass structural validation. Item IDs must be unique across the record's collections, review findings, handoff stages, and outputs. Preserve existing IDs when reordering. Identifier prefixes are for readability, not a naming requirement.

| Field | Contents |
|---|---|
| `schema_version` | Integer `1` |
| `task` | `id`, `summary`; `intent`: `implement/design/review`; `status`: `in_progress/partial/complete` |
| `rules[]` | `id`, `text`, `source`, `status`, `blocks_completion`; status: `confirmed/proposed/assumed/open` |
| `acceptance[]` | `id`, `scenario`, `expected`, `rule_ids[]`, `evidence_ids[]` |
| `design[]` | `id`, `decision`, `reason`, `tradeoffs`, `evidence_ids[]` |
| `evidence[]` | `id`, `kind`, `method`, `status`, `summary`; `artifact`, `command`, and `exit_code` where applicable |
| `review` | `status: not_run/completed`, `evidence_ids[]`, `findings[]` |
| `review.findings[]` | `id`, `detail`, `required`, `status: open/resolved/deferred`, `evidence_ids[]` |
| `limitations[]` | `id`, `description`, `blocks_completion` |
| `handoffs[]` | `id`, `stage`, `status`, `input_ids[]`, `outputs[]`, `notes`; present in new records |
| `handoffs[].outputs[]` | `id`, `summary`; optional local `artifact` path |
| `design_views` | Optional declared design bundle and independent pre-implementation readiness check, described below |

Required descriptions, sources, scenarios, and summaries must be nonempty text. Boolean fields use JSON `true/false`. Record the actual basis for a rule in `source`; existing code and AI proposals do not establish business confirmation.

### Evidence

- `kind` distinguishes `behavior`, `contract`, `structure`, `manual_review`, and `design_review`. Behavioral verification and structural inspection answer different questions and do not replace one another.
- `method: command` records actual execution. A passed item requires a nonempty command and integer exit code `0`. A failed item cannot report exit code `0`. A `not_run` item has no exit code; it may include the intended command and explain the blocker.
- `method: inspection` records inspection without a command or exit code. Record observed interface behavior, design assessment, or source inspection honestly instead of presenting it as automated execution.
- `status` is `passed/failed/not_run`. A passed item requires an `artifact` pointing to an existing file within the project root, such as a test log, observation record, or review result. Use relative paths and keep sensitive data out of shareable logs.
- `--project-root` sets the evidence root; otherwise the record's directory is used. Absolute references and references escaping the root through traversal or symlinks are rejected.
- Commands are records only: the validator **never executes them**. Field validation and file existence cannot establish authentic logs, adequate checks, actual business confirmation, or correct code. Human or AI review must assess those claims.

### Coverage and task intent

Final delivery readiness for all intents requires the task to be declared `complete`, a completed review linked to passed inspection evidence, and no declared completion-blocking rules or limitations. Pre-implementation `design_ready` is separate; future implementation/review work need not already be complete.

- **implement:** Confirmed rules have acceptance scenarios. Acceptance references confirmed rules and passed behavior or contract evidence. Required corrections are resolved. Unsettled future-scope rules may remain nonblocking, but any unresolved rule used by current acceptance still blocks readiness.
- **design:** Design decisions include reasons and trade-offs, linked to design or structural inspection evidence. Required design corrections are resolved; `open` and `deferred` both block readiness. Code and runtime behavior tests are not required.
- **review:** A review report may be complete while its findings remain unresolved. Report completion does not imply that corrections are complete. When implementing corrections is also the task, use an implementation record for that work.
- Recorded design decisions need passed structural or review evidence. Findings marked resolved need passed verification evidence. Retain historical failures when useful; red-phase records need not be deleted.

## Stage handoff extension

`handoffs` is an ordered record of the current selected stages. Every entry has a nonempty ID, stage name, notes, an `input_ids` list, an `outputs` list, and one of these statuses:

- `completed`: The current stage produced its usable result.
- `reused`: Existing results were read and checked for applicability; notes identify the source and readiness.
- `pending`, `blocked`, or `invalidated`: Work or revalidation remains; outputs are not ready for consumption.
- `skipped`: Notes explain why the stage is unnecessary for this request. The outputs list must be empty.

A completed or reused entry needs at least one output. Each output has a unique `id` and nonempty `summary`. For an inline result, the summary must contain the usable content rather than just say "done." If the result lives elsewhere, link a relative local file in `artifact` and identify its relevant section/current version in the summary or notes. Use a file path without a fragment in `artifact`; section identifiers belong in the explanatory text. Artifacts must exist within the project root, subject to the same traversal and symlink containment rules as evidence.

`input_ids` references output IDs from earlier handoff entries, not rule or evidence IDs. The first active stage may have no such inputs; its notes identify the supplied request and starting materials. Every next active stage must consume at least one output of its preceding active stage and may also reference other earlier results. Self/forward references are invalid. Inputs from unfinished or invalidated producers block readiness. Skipped entries do not interrupt the actual chain. This extension describes one ordered flow, not an arbitrary task DAG. Aggregate concurrent slice results at the stage level or use separate records for independent chains; retain their real dependency relationships.

Neutral record structure only; the declarations below are not execution evidence:

```json
{
  "handoffs": [
    {
      "id": "H1", "stage": "Requirements clarification", "status": "completed",
      "input_ids": [],
      "outputs": [{"id": "A1", "summary": "Source-based clarification results in the cited brief section", "artifact": "brief.md"}],
      "notes": "Source: current request and supplied answers; the next stage reads the clarification section."
    },
    {
      "id": "H2", "stage": "Requirements baseline", "status": "completed",
      "input_ids": ["A1"],
      "outputs": [{"id": "A2", "summary": "Scope, confirmed requirements and derived acceptance in the baseline section", "artifact": "brief.md"}],
      "notes": "Read A1 and checked its sources before consolidating A2."
    }
  ]
}
```

This neutral fragment is only a prefix of the seven-stage chain; it is not a complete implementation record. Keep unexecuted stages pending rather than copying completed statuses.

Legacy schema-version-1 records without `handoffs` retain their existing validation behavior. They do not establish stage-to-stage traceability. New templates include the extension. Seven-stage execution uses the same arbitrary-label schema; no fixed stage count is imposed on legacy records. Use `--require-handoffs` to require it, including when checking a legacy record; that option also implies `--require-ready`. Older validator releases do not understand this extension.

The checker validates declared references, statuses, and file existence. It does not infer which stages a task needs, verify document sections or source versions, prove that inputs were read, or automatically detect changes to artifact contents. The agent/reviewer must check those semantics and invalidate affected consumers when upstream results change.

## Design views and the pre-implementation gate

Use the optional `design_views` bundle for the scope selected under [Design Views](design-views.md). It adds declared source/evidence checks, not a UML parser or another final-delivery review.

| Field | Contents |
|---|---|
| `profile` | `detailed/lightweight`; view obligations, independent of the prerequisite tool's complete installation profile |
| `reason` | Nonempty task-specific rationale, including justified reuse or lightweight work |
| `rule_ids[]` | Existing rule IDs selected as this design's inputs; detailed design needs a nonempty set |
| `state_model` | `requirement: required/not_applicable/unresolved`, with a nonempty source-based `reason` |
| `views[]` | Each has unique `id`, `kind`, `status`, `notes`, `evidence_ids[]`; optional `artifact`, `preview_artifact` |
| `views[].kind` | `class/module/sequence/state/other`; module is the explicit non-OO structural alternative |
| `views[].status` | `completed/reused/pending/blocked/invalidated/skipped` |
| `consistency_review` | `status`, `view_ids[]`, `evidence_ids[]`, `notes`, `unresolved_issues[]` |
| `consistency_review.status` | `completed/not_run/pending/blocked/invalidated` |
| `consistency_review.unresolved_issues[]` | Outstanding design issues as nonempty strings; an empty array means none declared |

Completed/reused views need a real local source `artifact` and passed `structure`, `manual_review`, or `design_review` evidence. A supplied preview must also exist inside the project root. Notes explain reuse, limits, or skips; skipped views cannot claim source/preview artifacts. Response-only designs do not need conversion into JSON or project files.

Detailed design needs a usable `class` or `module` view and a usable `sequence` view. State requirement `required` needs a usable state view even in lightweight work; `unresolved` blocks readiness. A not-applicable assessment needs a reason. The checker trusts the declared scope and cannot infer lifecycle rules or whether lightweight was justified.

Consistency review must be completed, cover the active views, link passed `manual_review` or `design_review` evidence, and declare no unresolved design issues. Check actual contracts and rule coverage using the semantic guide. Within selected `rule_ids`, unconfirmed completion-blocking rules also block design readiness. Unrelated work outside those inputs and later code-review findings do not automatically block the pre-coding gate.

Run this **before implementation**, while the task may still be `in_progress` and future checks/review/handoffs are pending:

```bash
python3 scripts/validate_delivery.py path/to/delivery-record.json --project-root path/to/project --require-design
```

`design_ready: true` means the declared design bundle passes its own mechanical checks. `record_ready` may be false because implementation or final review is unfinished. `--require-design` returns `0` only for a structurally valid record and ready design; it does not imply final readiness. Combine it with `--require-ready` or `--require-handoffs` to require both gates.

Without a bundle or the new flag, legacy records retain their original behavior and return `design_ready: null` (not evaluated). With `--require-design`, a missing bundle returns false and blocks that gate. A present unready bundle also blocks final record readiness. Completing the task status cannot make missing/stale/unreviewed views ready.

Older validator releases do not understand this optional extension or its CLI flag. Use the validator shipped with the selected skill version rather than silently dropping the bundle to obtain a pass.

Neither gate authenticates evidence, reads UML meaning, automatically detects stale content, executes recorded commands, or certifies complete design/SOLID. Assess and record those semantic limits honestly.

## Validate a record and interpret exit codes

These are executable templates. Replace `path/to/delivery-record.json` and `path/to/project` with actual paths.

```bash
python3 scripts/validate_delivery.py path/to/delivery-record.json --project-root path/to/project
python3 scripts/validate_delivery.py path/to/delivery-record.json --project-root path/to/project --require-ready
python3 scripts/validate_delivery.py path/to/delivery-record.json --project-root path/to/project --require-handoffs
python3 scripts/validate_delivery.py path/to/delivery-record.json --project-root path/to/project --require-design
```

The JSON result contains `structure_valid`, `record_ready`, `design_ready`, `errors[]`, `blockers[]`, and separate `design_blockers[]`.

- By default, exit code `0` means only that the structure is valid. Also inspect `record_ready` and the blockers.
- With `--require-ready`, structural errors or incomplete declared coverage return exit code `1`.
- `--require-handoffs` requires a nonempty, connected chain of usable stage results and implies `--require-ready`. It returns `1` when the record or chain is incomplete.
- `--require-design` independently checks pre-implementation readiness; combined final-readiness options remain cumulative.
- Unreadable input, invalid JSON, duplicate JSON keys, or invalid command usage return exit code `2`.

`record_ready` means only that **the declared record and evidence references satisfy mechanical checks**. It is not software acceptance, architecture approval, or SOLID certification. Labeling an unrelated file as passed does not make it relevant evidence; review must examine that semantic relationship.

## Maintain the tools

Run the following executable command from the skill root; it has no placeholder arguments. It is run when validating a release, with actual results kept outside the distributed skill.

```bash
python3 -m unittest discover -s tests -v
```

Regression tests assert specific defects, exit codes, path constraints, overwrite protection, and non-execution of recorded commands. Validate new workflow behavior through [domain-neutral forward-testing protocol](../tests/behavioral-cases.md) in isolated workspaces. Keep particular business requests and applications outside this repository. Passing structural script tests does not establish the quality of the skill's decisions.
