# Functional and Quality Requirements

Read during clarification/baseline work and when a design exposes a missing requirement.
Accept conversations, tickets, documents, screenshots, contracts, existing-system evidence
or combinations. No PRD or filename is mandatory. Preserve source identity/version;
current code describes observed behavior, not automatically the intended requirement.

## Read first, then ask consequential questions

1. Extract settled answers and identify conflicting sources. Separate confirmed facts,
   proposals, assumptions and unknowns.
2. Assess the dimensions below as confirmed, open or not applicable with a reason.
   Scope this assessment to the actual task; reuse current project answers.
3. Ask only about gaps that change observable behavior, acceptance or architecture.
   Prioritize the decision and consequence rather than sending an exhaustive questionnaire.
4. Record each unresolved decision's affected work and next owner/source. Continue
   independent work; block dependent work where an answer could change its design.

| Dimension | Inspect or clarify when relevant |
|---|---|
| Functional behavior | Actors/goals, scope, triggers, pre/postconditions, basic/alternative/exception flows |
| Business rules and data | Authoritative information, invariants, units, boundaries, conflicting/duplicate inputs, retention |
| Permissions and integrations | Role/resource boundaries, identity source, external contracts and failure behavior |
| Performance and capacity | Workload shape, response expectations, concurrency, growth and peak conditions |
| Availability and recovery | Critical paths, dependency failures, graceful degradation, recovery and data-loss expectations |
| Consistency and concurrency | Transaction/ordering needs, duplicates, contention, stale reads and retry semantics |
| Security and privacy | Authentication, authorization, tenant/trust boundaries, sensitive data, auditing |
| Observability and operations | Diagnosis, signals, runbooks, ownership, change and rollback constraints |
| Maintainability and extensibility | Supported change scenarios, stable interfaces, replaceable dependencies |
| Compatibility and deployment | Existing stack/database, environment, migration, interoperability and delivery constraints |
| Cost and resources | Budget/resource constraints and operational complexity |

Unknown quality targets remain **open**. Do not invent throughput, latency, capacity,
recovery or cost figures. A conditional architecture proposal can proceed with explicitly
unresolved validation criteria; it is not proof of achieved quality. If an unknown would
change a required architectural choice, leave that choice and dependent work unready.

## Turn qualities into checkable scenarios

For each relevant scenario preserve:

- ID, source/version, priority and confirmed/proposed/open status.
- Context/environment and workload or triggering event.
- Affected artifact/responsibility and expected response.
- Observable criterion; use **to confirm** where the source gives no target.
- Verification method, evidence location and any blocked decision.

The baseline states required outcomes. Architecture records the chosen strategy and
trade-offs. Detailed design allocates interfaces/behavior. Coding and review collect
the actual verification. Keep this chain explicit; an implementation result cannot
retroactively supply an unconfirmed business rule or acceptance target.
