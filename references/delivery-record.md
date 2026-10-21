# Optional Delivery Records and Tools

Use structured records when a task needs handoffs between stages, traceability between acceptance and evidence, or input for downstream tools. Small changes may use the response or existing task records; JSON is optional.

The tools require Python 3.10+ and use only the standard library. They do not depend on other skills, a package manager, network access, or a project framework.

## Initialize a record

Run from the skill root. This is an executable command template: replace `path/to/new-delivery`, `TASK-1`, and the summary with task-specific values. The example does not represent an actual task execution.

```bash
python3 scripts/init_delivery.py path/to/new-delivery --id TASK-1 --summary "Delivery objective" --intent implement --with-brief
```

This creates `delivery-record.json`; `--with-brief` also creates an implementation-brief template. The initial status is `in_progress`, with no invented rules or verification results. Existing output files are never overwritten; edit an existing record in place where appropriate.

All output is encoded as UTF-8 before directories or files are created. Unencodable task text is rejected with exit code `2`, leaving no output. If a subsequent file write encounters an I/O error, files created by this invocation are removed while pre-existing files are preserved.

The [delivery-record template](../assets/templates/delivery-record.json) and [implementation-brief template](../assets/templates/implementation-brief.md) can also be used directly. They need not be delivered together.

## Record format: schema version 1

Field names are checked strictly: unknown fields and duplicate JSON keys are errors. Collections may be empty, so an incomplete draft can still pass structural validation. Item IDs must be unique across the record's collections and review findings. Preserve existing IDs when reordering. Example prefixes are for readability, not a naming requirement.

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

Required descriptions, sources, scenarios, and summaries must be nonempty text. Boolean fields use JSON `true/false`. Record the actual basis for a rule in `source`; existing code and AI proposals do not establish business confirmation.

### Evidence

- `kind` distinguishes `behavior`, `contract`, `structure`, `manual_review`, and `design_review`. Behavioral verification and structural inspection answer different questions and do not replace one another.
- `method: command` records actual execution. A passed item requires a nonempty command and integer exit code `0`. A failed item cannot report exit code `0`. A `not_run` item has no exit code; it may include the intended command and explain the blocker.
- `method: inspection` records inspection without a command or exit code. Record observed interface behavior, design assessment, or source inspection honestly instead of presenting it as automated execution.
- `status` is `passed/failed/not_run`. A passed item requires an `artifact` pointing to an existing file within the project root, such as a test log, observation record, or review result. Use relative paths and keep sensitive data out of shareable logs.
- `--project-root` sets the evidence root; otherwise the record's directory is used. Absolute references and references escaping the root through traversal or symlinks are rejected.
- Commands are records only: the validator **never executes them**. Field validation and file existence cannot establish authentic logs, adequate checks, actual business confirmation, or correct code. Human or AI review must assess those claims.

### Coverage and task intent

All intents require the task to be declared `complete`, a completed review linked to passed inspection evidence, and no declared completion-blocking rules or limitations.

- **implement:** Confirmed rules have acceptance scenarios. Acceptance references confirmed rules and passed behavior or contract evidence. Required corrections are resolved. Unsettled future-scope rules may remain nonblocking, but any unresolved rule used by current acceptance still blocks readiness.
- **design:** Design decisions include reasons and trade-offs, linked to design or structural inspection evidence. Required design corrections are resolved; `open` and `deferred` both block readiness. Code and runtime behavior tests are not required.
- **review:** A review report may be complete while its findings remain unresolved. Report completion does not imply that corrections are complete. When implementing corrections is also the task, use an implementation record for that work.
- Recorded design decisions need passed structural or review evidence. Findings marked resolved need passed verification evidence. Retain historical failures when useful; red-phase records need not be deleted.

## Validate a record and interpret exit codes

These are executable templates. Replace `path/to/delivery-record.json` and `path/to/project` with actual paths.

```bash
python3 scripts/validate_delivery.py path/to/delivery-record.json --project-root path/to/project
python3 scripts/validate_delivery.py path/to/delivery-record.json --project-root path/to/project --require-ready
```

The JSON result contains `structure_valid`, `record_ready`, `errors[]`, and `blockers[]`.

- By default, exit code `0` means only that the structure is valid. Also inspect `record_ready` and the blockers.
- With `--require-ready`, structural errors or incomplete declared coverage return exit code `1`. Use it where a readiness gate is required.
- Unreadable input, invalid JSON, duplicate JSON keys, or invalid command usage return exit code `2`.

`record_ready` means only that **the declared record and evidence references satisfy mechanical checks**. It is not software acceptance, architecture approval, or SOLID certification. Labeling an unrelated file as passed does not make it relevant evidence; review must examine that semantic relationship.

## Maintain the tools

Run the following executable command from the skill root; it has no placeholder arguments. It is run when validating a release, with actual results kept outside the distributed skill.

```bash
python3 -m unittest discover -s tests -v
```

Regression tests assert specific defects, exit codes, path constraints, overwrite protection, and non-execution of recorded commands. Validate new workflow behavior through [forward-testing scenarios](../tests/behavioral-cases.md) in isolated workspaces. Passing script tests does not establish the quality of the skill's decisions.
