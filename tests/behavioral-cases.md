# Independent Forward-Testing Scenarios

These scenarios test the skill's decisions, not the delivery-record scripts. Create an isolated workspace per scenario. Give the request and raw materials to a session or agent without the author's conversation history. Keep assessment criteria with the evaluator rather than revealing them in advance. If delegation is unavailable, use an independent new session.

Scenario-specific business details belong to the test input only. They are not defaults for other tasks.

## A. Small change

**Request:** Correct a late-fee calculation so no fee applies on the due date; retain the existing rule after that date. The existing Python function charges when `today >= due_date`, using `total_cents // 100`. Existing unittest coverage includes dates before and after the due date.

**Assessment:** Correct the boundary behavior while preserving the existing rule. Verify the due date. Avoid unjustified interfaces, patterns, or a full diagram and document set. Actual verification commands must be reproducible.

## B. New feature with unresolved business rules

**Request:** Implement warehouse inventory reservation using an order, SKU, and quantity. Warehouse inventory is authoritative. Notify downstream after success. Duplicate submissions are possible, cancellation is supported, and insufficient inventory must produce an explicit result. Warehouse and messaging adapters are external; no further rules are specified.

**Assessment:** Identify implementation-changing questions about duplicates, cancellation, notification failure, and external atomicity. Separate confirmed facts from proposals. Continue independent analysis or implementation where justified without claiming delivery of the feature. Organize questions by their current impact rather than asking every possible future design question at once.

## C. Design only

**Request:** Propose a design and interface for large-volume CSV export. Do not write code or files. Preserve the existing contract: UTF-8, a header row, deterministic ordering, download after completion, and tenant isolation. There is no measured performance baseline.

**Assessment:** Respect the requested scope and existing contract. Address reading, encoding, result publication, and failures. Propose verification rather than inventing execution results. Make no unmeasured capacity or speed claims.

## D. Resume from a handoff

**Request:** Continue the next unblocked stage using the supplied task record and project artifacts. The prior conversation is unavailable. One referenced upstream result is incomplete, while an independent slice has sufficient confirmed inputs.

**Assessment:** Read the actual referenced outputs, identify missing input and its dependent work, and continue only the justified independent work. Produce a usable next result with explicit input/output references and limits. Do not recreate business decisions from memory or fabricate completed upstream stages.

## E. Revise an upstream result

**Request:** Apply a newly confirmed change to an existing rule or interface contract. The supplied handoff chain includes downstream design, implementation, and review results based on the old version.

**Assessment:** Identify affected consumers, invalidate their previous readiness, revise outputs and input references, and rerun the necessary checks before declaring those consumers complete. Preserve unaffected work and keep source versions and remaining gaps clear. A file-existence check alone cannot establish freshness.

## F. Clean repository setup

**Request:** In a fresh repository with exactly the 12 required skills and no `triage`, explicitly run setup, specification, and ticketing with the user's tracker, label mapping, document layout, and test seam choices supplied. Use a local Markdown tracker and preserve an existing instruction file. Include a custom ready-state mapping.

**Assessment:** Read real setup outputs, complete any omitted consumer configuration through the named adapter, and use that saved configuration in the actual specification and tickets. Preserve the custom mapping and surrounding instructions. Reuse valid setup instead of repeating the same incomplete upstream branch. Installation and prompt reading alone are not completion.

## G. Review pending changes

**Request:** Review a supplied specification against staged, unstaged, and newly added local files. The starting commit is supplied, and no commit or code correction is requested.

**Assessment:** Review the actual selected change, including non-ignored new files, using a fixed local snapshot when committed history does not contain it. Give both axes the same input, preserve Git state and application bytes, and identify real contract deviations. Label the local adapter accurately.

## H. Complete local feature

**Request:** Implement a fully specified feature from raw requirements to local code, tests, and review. Explicitly request the relevant user-invoked stages and provide their necessary choices. Select a test business independent of the skill's teaching history. No commit or remote publication is requested.

**Assessment:** Inspect real rules, domain/responsibility design, specification, slices, code, verification, review input, and corrections. Each active stage must consume actual preceding results. Check observable behavior independently at the public API. The final review must include delivered local code and new files, with accurate invocation, evidence, scope, and completion claims.

## Record the results

For the detailed-design workflow, also exercise these focused cases with independent raw business inputs:

- **Stateful new use case:** Carry an actual lifecycle through rules, BCE, class/module structure, principal/failure sequences, a state view, specification, code, tests, and review. Check declared design readiness before coding and compare actual operations/events/transitions afterward. Missing required views or unresolved lifecycle rules must not pass that design gate.
- **Stateless new use case:** Produce an appropriate module/structure view and interactions without inventing classes or business states. Record state non-applicability from the actual contract. Do not claim a class-specific profile verified a different diagram grammar.
- **Bounded maintenance:** Preserve existing contracts and responsibilities. Justify lightweight reuse or omission rather than automatically generating the full design set; continue to honor an explicitly requested view.
- **Response-only design:** Deliver the appropriate views and consistency assessment in the response while preserving a request that prohibits project writes. Do not force JSON or persisted diagrams merely to satisfy a tool.

Preserve the original input, actual artifacts, commands and outputs, assessment evidence, and limitations. Test actual decisions rather than exact wording, heading counts, or file counts. This scenario document does not prove that any scenario has been executed.
