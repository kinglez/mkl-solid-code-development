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

## Record the results

Preserve the original input, actual artifacts, commands and outputs, assessment evidence, and limitations. Test actual decisions rather than exact wording, heading counts, or file counts. This scenario document does not prove that any scenario has been executed.
