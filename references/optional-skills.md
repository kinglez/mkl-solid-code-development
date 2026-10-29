# Workflow Prerequisites and Skill Routing

Use [Matt Pocock Skills](https://github.com/mattpocock/skills) as the preferred execution framework, together with `mkl-uml-robustness-diagram` from [MKL UML Skills](https://github.com/kinglez/mkl-uml) for robustness analysis. Install all 12 prerequisites: 11 Matt Pocock Skills and one MKL robustness-analysis skill. This includes `grilling`, which supports `grill-with-docs`, and the repository setup skill. Installation does not require every task to run every stage or produce a diagram.

## Required installation baseline

| Stage or prerequisite | Required skills | Input and outcome |
|---|---|---|
| Configure the target repository once | `setup-matt-pocock-skills` | Confirm the tracker, applicable labels, and domain-document conventions in the target project |
| Clarify business rules and language | `grill-with-docs`, `grilling`, `domain-modeling` | Goals, established rules, conflicts, and open questions; produce confirmed rules and domain meanings |
| Analyze use-case responsibilities | `mkl-uml-robustness-diagram` | Specified behavior and available domain evidence; identify boundary, entity, and control responsibilities, omissions, and model updates |
| Design modules and interfaces | `codebase-design` | Change scenarios, callers, constraints, and dependencies; produce responsibilities, contracts, and trade-offs |
| Consolidate specifications and dependencies | `to-spec`, `to-tickets` | Confirmed rules, design, acceptance scenarios, and verification entry points; produce a specification and verifiable slices |
| Implement and verify behavior | `implement`, `tdd` | The current slice, dependencies, agreed test entry points, and completion criteria; produce code and actual verification results |
| Review the change | `code-review` | A fixed change baseline, request scope, specification, repository standards, and verification results |
| Reassess architecture when warranted | `improve-codebase-architecture` | Relevant final code, observed friction, and a bounded investigation scope; produce evidence and trade-offs |

Installation instructions and invocation rules come from the [upstream repository](https://github.com/mattpocock/skills#installation-30-second-setup). Use one installation route per agent to avoid duplicate skill copies.

An editable-file installation can use this executable example, taken from the upstream installation guide:

```bash
npx skills add mattpocock/skills
```

For that repository, select the 11 Matt Pocock Skills listed in the table, including `setup-matt-pocock-skills` and `grilling`. Install the required robustness-analysis skill separately with this executable command, which has no placeholder arguments:

```bash
npx skills add kinglez/mkl-uml --skill mkl-uml-robustness-diagram
```

These commands are not executed automatically by this skill. A plugin installation supported by the target agent is also valid. Preserve existing customizations; do not overwrite installed skills merely to satisfy a presence check.

## Verify installation and activation

For filesystem installations, run the packaged read-only checker from this skill's root. The following are executable templates; replace each `path/to/...` with a real directory containing `skill-name/SKILL.md`:

```bash
python3 scripts/check_prerequisites.py --skills-root path/to/skills
python3 scripts/check_prerequisites.py --skills-root path/to/project-skills --skills-root path/to/global-skills
```

The checker verifies readable UTF-8 definitions with the expected frontmatter names across the supplied roots. It returns JSON and exit code `0` when all 12 are present, `1` for missing or invalid definitions, and `2` for invalid roots or command usage. It never downloads, overwrites, installs, or executes a skill.

This is a presence check, not proof of upstream provenance, compatible versions, successful activation, or completed repository setup. For plugin installations without exposed filesystem roots, verify the installed catalog and definitions using the agent's supported mechanism. Confirm that relevant skills can actually be invoked in the current session. If a new installation requires a new session or turn, follow that agent's activation procedure.

When a required skill is missing, install it through the target environment's supported installer where authorized, then repeat the check. If installation or activation cannot be completed, report exactly what is missing and pause only dependent stages. Do not describe a local substitute as execution of the missing skill or claim that the integrated workflow is ready.

## Configure the target repository

After installation, run `setup-matt-pocock-skills` once in the codebase where development will occur, using the agent's supported explicit invocation. Follow its confirmation process for the tracker, labels where applicable, and document layout. Reuse valid existing configuration rather than running setup for every task.

Installation does not complete setup. Check the project's actual configuration before tracker-dependent specification, ticket, implementation, or review stages. Do not copy the skill publisher's tracker, labels, paths, or teaching business into another project.

## Invocation and authorization

- Read the selected skill's instructions and respect its applicability. Upstream user-invoked skills require explicit invocation; installing them does not make them automatically callable by another skill.
- Use model-invoked skills where appropriate. For explicit-only stages, use the supported user-invocation mechanism rather than silently bypassing it.
- Some workflows require a tracker, approved slices, agreed test seams, delegation, or committing. Run their complete workflow only when those prerequisites and actions match the task's authorization. Do not omit required steps and still claim complete execution.
- Keep local delivery local when requested. Publishing issues, committing, pushing, creating pull requests, and deploying require authorization for those actions.
- Use subagents only when supported and authorized by the task or applicable skill. Two checks in the same context are not independent reviews.
- Pass relevant rules, artifact locations, scope, and acceptance criteria. Verify returned artifacts and actual evidence. Teaching examples and other skills' samples do not become the current task's business rules or evidence.

## Robustness analysis and optional MKL modeling support

`mkl-uml-robustness-diagram` is required. Read its instructions and use standalone mode by default; a formal MKL workflow or gate requires an explicit request. Missing domain or flow evidence limits verification claims rather than justifying invented business facts.

The following additional modeling skills remain optional:

| Work | Optional skills | Outcome |
|---|---|---|
| Specify use cases and analyze responsibilities | `mkl-use-case-specifier` | Use-case behavior, responsibility coverage, ambiguities, and model updates |
| Develop necessary domain, static, or interaction views | `mkl-uml-domain-modeler`, `mkl-uml-design-class-model`, `mkl-uml-sequence-diagram` | Views and constraints that answer the current design question |

The included robustness reference provides supporting guidance; it does not replace the required robustness-analysis skill or make every task require a diagram.

## Stage inputs and returned outputs

Use the [stage handoff contract](workflow-handoffs.md) for every selected skill. Supply the actual preceding output and its current source reference, not only a stage name. Inspect the returned result against the next stage's input needs and preserve the result, source, readiness, and consumer in the existing work record. Installation or invocation alone is not a produced artifact.

## Interrupt and resume

Preserve confirmed and unresolved rules, prerequisite checks, relevant setup state, the current slice, changed files, key decisions, actual check results, and next steps in the project's existing task record. Update existing records rather than maintaining parallel specifications unnecessarily.
