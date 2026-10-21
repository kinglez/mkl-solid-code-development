# SOLID and Design Patterns: Decisions Backed by Change and Evidence

Use this reference during design, refactoring, or structural review. Apply the principles relevant to the current task. Stable, simple logic can remain a function. Justify new interfaces and classes by their benefits rather than their count or pattern names.

## Turn principles into concrete questions

| Principle | Question for the current task | Useful evidence |
|---|---|---|
| S — Single Responsibility | Which reasons for change are independent? Do they force unrelated behavior to change together? | Where domain logic and interaction adapters change; whether the same rule is duplicated across locations |
| O — Open/Closed | Can known variations be introduced at an appropriate place? Which changes still require coordination or composition changes? | The impact of replacing an implementation; actual edit locations and limitations when adding a variation |
| L — Liskov Substitution | Does each implementation honor the semantic promises its callers rely on? | Compatible preconditions, result meaning, units, invariants, failures, and side effects; relevant contract tests |
| I — Interface Segregation | Must callers depend on capabilities or information they do not need? | The interface surface, configuration, and failure semantics each caller actually needs; avoid mechanically creating an interface per method |
| D — Dependency Inversion | Does policy depend on an appropriate contract, with concrete choices made at a suitable composition point? | Execution-path inspection confirming that the dependency is used; an alternative implementation where useful |

Matching types do not establish matching semantics. Substitutable implementations must preserve the meaning and constraints of their results, not merely return the same type. Contract tests support the promises they cover; they are not a mathematical proof of complete substitutability.

## Evaluate design patterns through trade-offs

Explain candidate designs in this order: **actual variation or complexity → simplest viable solution → candidate organization → benefits, costs, and limitations → verification**.

| Observed problem | Organization to consider | Insufficient justification |
|---|---|---|
| Interchangeable algorithms share input and output semantics | A function parameter or Strategy | Many algorithms might exist someday |
| An external protocol differs from the internal contract | Adapter | Adding a pass-through without hiding a meaningful difference |
| State determines legal operations and branches are becoming inconsistent | An explicit state model or state machine; State if warranted | A state field exists |
| Object composition has real selection or configuration complexity | A composition function; Factory if warranted | Every constructor needs a factory |

These are candidates, not a required pattern checklist. One business change may legitimately affect several locations. Explain why, rather than promising that every future feature can be added without changing existing code.

## Verify structure without overfitting to implementation

Observe behavior and contracts through stable public entry points. If replaceable dependencies are an explicit design requirement, supply a contract-compatible alternative and verify that the caller actually uses it. A constructor parameter or interface declaration alone is insufficient evidence.

Retain valuable source review: responsibility and dependency problems do not always warrant automated tests. Avoid tests that assert only private method names, file or class counts, or fixed internal call sequences, unless those details are themselves a protocol that must be preserved.

For performance work, establish the bottleneck, budget, or measurement need first. Patterns, asynchronous execution, and additional abstractions do not by themselves demonstrate an improvement.
