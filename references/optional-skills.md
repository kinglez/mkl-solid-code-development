# Optional Skill Routing

The core workflow works without installing other skills. When specialized support is useful, discover candidates from the skills or tools actually available in the target environment. Read the selected instructions and respect their scope. The table maps capabilities; it does not guarantee a particular name, path, or invocation interface.

| Work | Optional skills | Handoff |
|---|---|---|
| Clarify requirements and domain language | `grill-with-docs`, `grilling`, `domain-modeling` | Goals, established rules, conflicts, open questions; return confirmed rules and domain meanings |
| Specify use cases and perform robustness analysis | `mkl-use-case-specifier`, `mkl-uml-robustness-diagram` | Target use case, flows, domain concepts; return responsibilities, ambiguities, and model updates |
| Develop necessary domain, static, or interaction views | `mkl-uml-domain-modeler`, `mkl-uml-design-class-model`, `mkl-uml-sequence-diagram` | The design question and existing materials; return the relevant views and constraints |
| Design modules and interfaces | `codebase-design` | Change scenarios, callers, business constraints, existing dependencies; return responsibilities, contracts, and trade-offs |
| Consolidate specifications and task dependencies | `to-spec`, `to-tickets` | Confirmed rules, design, acceptance scenarios, verification entry points; return implementation specifications and verifiable slices |
| Implement specifications with short feedback loops | `implement`, `tdd` | Current slice, dependencies, verification entry points, completion criteria; return code and actual verification results |
| Review requirements conformance and standards | `code-review` | Fixed change baseline, request scope, specification, repository standards, verification results |
| Investigate architecture in greater depth | `improve-codebase-architecture` | Final relevant code, observed problems, investigation scope; return evidence and trade-offs |

## Usage constraints

- Confirm availability, invocation support, and applicability. Listing a name is not evidence that a skill was executed. Respect explicit-only invocation rules in the target environment; where necessary, let the user invoke the skill or perform the required analysis directly.
- A skill may require an issue tracker, a commit workflow, additional tools, or broader investigation. Delegate its complete workflow only when those prerequisites match the task and authorization. Silently dropping required steps does not constitute complete execution.
- If prerequisites are unmet, this skill can perform the necessary local analysis, specification, or checks directly. Describe the work accurately: drafting a local specification does not mean `to-spec` was executed or published.
- Keep local delivery local when requested. Publishing an issue, committing, pushing, creating a pull request, or deploying requires authorization for that action; an optional skill does not expand the task.
- Use subagents only when supported by the environment and authorized by the task or applicable skill. Without delegation, perform the checks directly. Two passes in the same context are not independent reviews.
- Pass only relevant rules, material locations, scope, and acceptance criteria. Inspect returned artifacts and actual evidence. Teaching templates, deductions, and expected outputs are not execution records; examples in another skill do not become the current task's business rules.

## Interrupt and resume

Use the project's existing task record across sessions. Preserve confirmed and unresolved rules, the current slice, changed files, key decisions, actual check results, and next steps. Update existing records rather than maintaining parallel specifications unnecessarily.
