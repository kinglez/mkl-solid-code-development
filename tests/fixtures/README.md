# Structural Test Fixtures

These records contain domain-neutral parser and protocol data only. They are not application examples, requirements interviews, actual command results, or actual review evidence. The files under `evidence/` are synthetic data used to exercise reference and readiness validation.

- `ready.json`: valid structure and complete declared coverage.
- `partial.json`: valid structure with an unresolved required input and unfinished work.
- `invalid.json`: duplicate identifiers, a dangling reference, an inconsistent declared exit code, and a missing evidence file.

The tests assert the corresponding validation results and exit behavior. No command named in a fixture is executed. External end-to-end applications and their inputs, expectations, and results stay outside this repository.
