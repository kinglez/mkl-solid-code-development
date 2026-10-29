# Workflow Prerequisites and Skill Routing

Use [Matt Pocock Skills](https://github.com/mattpocock/skills) with [MKL UML Skills](https://github.com/kinglez/mkl-uml). The core has 12 prerequisites: 11 Matt skills and MKL robustness analysis. Detailed design adds the class/sequence pair below. Installation does not require every task to run every stage or every diagram type.

## Required installation baseline

| Stage or prerequisite | Required skills | Input and outcome |
|---|---|---|
| Configure the target repository once | `setup-matt-pocock-skills` | Confirm the tracker, applicable labels, and domain-document conventions in the target project |
| Clarify business rules and language | `grill-with-docs`, `grilling`, `domain-modeling` | Goals, established rules, conflicts, and open questions; produce confirmed rules and domain meanings |
| Analyze use-case responsibilities | `mkl-uml-robustness-diagram` | Specified behavior and available domain evidence; identify boundary, entity, and control responsibilities, omissions, and model updates |
| Design modules and interfaces | `codebase-design`; detailed-design capabilities below | Responsibilities and actual class/module, sequence and relevant lifecycle views; produce reviewed contracts and trade-offs |
| Consolidate specifications and dependencies | `to-spec`, `to-tickets` | Confirmed rules, design, acceptance scenarios, and verification entry points; produce a specification and verifiable slices |
| Implement and verify behavior | `implement`, `tdd`; named local adapter where needed | The current slice, dependencies, agreed test entry points, and completion criteria; select the [implementation/review route](local-review.md) before starting |
| Review the change | `code-review` for an applicable committed diff; local two-axis adapter for pending changes | A fixed change snapshot, request scope, specification, repository standards, and verification results; include delivered untracked files |
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

### Conditional detailed-design profile

For new use cases and complex changes, read [Design Views](design-views.md) and install the two required detailed-design capabilities:

```bash
npx skills add kinglez/mkl-uml --skill mkl-uml-design-class-model mkl-uml-sequence-diagram
```

This makes 14 definitions for the selected detailed-design profile. Use the class skill for OO structure and the sequence skill for interactions. A justified non-OO module view replaces the class artifact without claiming class-validator coverage. Use the available project UML renderer for required state views; no dedicated MKL state skill is assumed.

## Verify installation and activation

For filesystem installations, run the packaged read-only checker from this skill's root. The following are executable templates; replace each `path/to/...` with a real directory containing `skill-name/SKILL.md`:

```bash
.venv/bin/python scripts/check_prerequisites.py --skills-root path/to/skills
.venv/bin/python scripts/check_prerequisites.py --skills-root path/to/project-skills --skills-root path/to/global-skills
.venv/bin/python scripts/check_prerequisites.py --skills-root path/to/skills --profile detailed-design
```

The checker requires PyYAML from `requirements.txt`; see the [runtime setup](../README.md#prerequisite-checker-runtime). It parses YAML safely, rejects duplicate keys, and compares actual names. Default profile `core` checks 12 definitions; `detailed-design` checks 14. Exit `0` means the selected set is present, `1` means missing/invalid definitions, and `2` means invalid input or checker dependencies. It never downloads, installs, overwrites, or executes a skill.

This is a presence check, not proof of upstream provenance, compatible versions, successful activation, or completed repository setup. For plugin installations without exposed filesystem roots, verify the installed catalog and definitions using the agent's supported mechanism. Confirm that relevant skills can actually be invoked in the current session. If a new installation requires a new session or turn, follow that agent's activation procedure.

When a required skill is missing, install it through the target environment's supported installer where authorized, then repeat the check. If installation or activation cannot be completed, report exactly what is missing and pause only dependent stages. Do not describe a local substitute as execution of the missing skill or claim that the integrated workflow is ready.

## Configure the target repository

After installation, run `setup-matt-pocock-skills` in the target codebase through explicit invocation, following its confirmation process. Then apply the [repository setup completion contract](repository-setup.md). It accounts for the upstream omission of labels when `triage` is absent and defines a local adapter that preserves confirmed repository conventions. Reuse configuration that satisfies the actual downstream consumers rather than rerunning setup for every task.

Installation does not complete setup. Check the project's actual configuration before tracker-dependent specification, ticket, implementation, or review stages. Do not copy the skill publisher's tracker, labels, paths, or teaching business into another project.

## Invocation and authorization

- Read the selected skill's instructions and respect its applicability. Upstream user-invoked skills require explicit invocation; installing them does not make them automatically callable by another skill.
- Use model-invoked skills where appropriate. For explicit-only stages, use the supported user-invocation mechanism rather than silently bypassing it.
- Some workflows require a tracker, approved slices, agreed test seams, delegation, or committing. Run their complete workflow only when those prerequisites and actions match the task's authorization. Select the [local implementation/review adapter](local-review.md) for pending changes or local delivery; distinguish that execution from the original upstream workflow.
- Keep local delivery local when requested. Publishing issues, committing, pushing, creating pull requests, and deploying require authorization for those actions.
- Use subagents only when supported and authorized by the task or applicable skill. Two checks in the same context are not independent reviews.
- Pass relevant rules, artifact locations, scope, and acceptance criteria. Verify returned artifacts and actual evidence. Teaching examples and other skills' samples do not become the current task's business rules or evidence.

## Robustness analysis and optional MKL modeling support

`mkl-uml-robustness-diagram` is required. Read its instructions and use standalone mode by default; a formal MKL workflow or gate requires an explicit request. Missing domain or flow evidence limits verification claims rather than justifying invented business facts.

The following modeling aids remain optional. The class/sequence pair above is conditional on detailed design rather than a universal optional suggestion:

| Work | Optional skills | Outcome |
|---|---|---|
| Specify use cases and analyze responsibilities | `mkl-use-case-specifier` | Use-case behavior, responsibility coverage, ambiguities, and model updates |
| Clarify domain relationships | `mkl-uml-domain-modeler` | Conceptual domain meanings and relationships, distinct from technical design classes |

The included robustness reference provides supporting guidance; it does not replace the required robustness-analysis skill or make every task require a diagram.

## Stage inputs and returned outputs

Use the [stage handoff contract](workflow-handoffs.md) for every selected skill. Supply the actual preceding output and its current source reference, not only a stage name. Inspect the returned result against the next stage's input needs and preserve the result, source, readiness, and consumer in the existing work record. Installation or invocation alone is not a produced artifact.

## Interrupt and resume

Preserve confirmed and unresolved rules, prerequisite checks, relevant setup state, the current slice, changed files, key decisions, actual check results, and next steps in the project's existing task record. Update existing records rather than maintaining parallel specifications unnecessarily.
