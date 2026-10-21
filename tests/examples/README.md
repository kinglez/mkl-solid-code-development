# Delivery-Record Test Fixtures

All examples and files under `evidence/` are explicitly synthetic test data. They are not requirements interviews, actual test runs, or real code-review results. Use them to test parsing, references, coverage, and exit codes; never reuse them as evidence for an actual delivery.

- `ready.json`: Valid structure with complete declared coverage.
- `partial.json`: Valid structure with an unresolved rule and unfinished work.
- `invalid.json`: Duplicate IDs, a dangling rule reference, a passed status inconsistent with the exit code, and a missing evidence file.

Automated tests assert these specific outcomes. A validator that merely avoids crashing must not count an invalid fixture as passed.
