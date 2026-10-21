# MKL SOLID Code Development

An agent skill for turning business requirements into understandable, extensible, and maintainable code.

The workflow connects confirmed rules, responsibility and interface design, implementation, verification, and review. It is domain-agnostic and works with the target project's language and conventions. The integrated workflow uses Matt Pocock Skills, with an explicit installation baseline and prerequisite checks.

## What it helps you do

| Stage | Outcome |
| --- | --- |
| Clarify requirements | Confirmed rules, authoritative sources, acceptance scenarios, and explicit open questions |
| Design responsibilities | Use-case coverage, suitable contracts, and justified module structure |
| Implement verifiable slices | Working behavior with checks actually run |
| Refactor and review | Corrections assessed against requirements and repository standards |
| Reassess and deliver | A scoped architecture assessment, evidence, trade-offs, and remaining limitations |

Robustness analysis helps identify **boundary, entity, and control** responsibilities where the use case is unclear. SOLID and design patterns guide concrete decisions; they are not mandatory class or interface checklists.

The depth follows the task. A small change does not require a complete diagram set, structured record, or new abstractions. Design-only and review-only requests retain their scope. Communication follows the user's language even though this skill is written in English.

## Prerequisites: Matt Pocock Skills and robustness analysis

Install **12 prerequisite skills** before using the integrated workflow: the following 11 from [mattpocock/skills](https://github.com/mattpocock/skills), plus `mkl-uml-robustness-diagram` from [kinglez/mkl-uml](https://github.com/kinglez/mkl-uml).

| Purpose | Required skills |
| --- | --- |
| Repository setup | `setup-matt-pocock-skills` |
| Business clarification and domain language | `grill-with-docs`, `grilling`, `domain-modeling` |
| Boundary, entity, and control analysis | `mkl-uml-robustness-diagram` |
| Module and interface design | `codebase-design` |
| Specifications and implementation slices | `to-spec`, `to-tickets` |
| Implementation and testing | `implement`, `tdd` |
| Change review | `code-review` |
| Architecture reassessment | `improve-codebase-architecture` |

Use the [upstream installation guide](https://github.com/mattpocock/skills#installation-30-second-setup) for your agent. For an editable-file installation, the following is a runnable example from that guide:

```bash
npx skills add mattpocock/skills
```

Select the 11 Matt Pocock Skills listed above. Install the required robustness-analysis skill separately:

```bash
npx skills add kinglez/mkl-uml --skill mkl-uml-robustness-diagram
```

These are executable installation examples with no placeholder arguments. They are not executed automatically by this skill. Use one installation route per agent to avoid duplicate copies, and preserve existing customizations.

## Install and use

Use the standard [Skills CLI](https://skills.sh/docs/cli). With Node.js and npm available, run this executable command from the target project; it has no placeholder arguments:

```bash
npx skills add kinglez/mkl-solid-code-development
```

The installer lets you select the target agents. Installation is project-scoped by default. For a user-wide installation, use this alternative instead:

```bash
npx skills add kinglez/mkl-solid-code-development -g
```

Install both sets of prerequisites separately with the commands in the previous section. Installing this skill does not automatically install another repository's skills. To inspect the available skill without installing it, run:

```bash
npx skills add kinglez/mkl-solid-code-development --list
```

From the installed `mkl-solid-code-development` directory, verify the prerequisite definitions using their actual installation roots. These are executable templates; replace `path/to/...` with directories containing `skill-name/SKILL.md`:

```bash
python3 scripts/check_prerequisites.py --skills-root path/to/skills
python3 scripts/check_prerequisites.py --skills-root path/to/project-skills --skills-root path/to/global-skills
```

The checker is read-only. Exit code `0` means the 12 named definitions are readable, `1` means some are missing or invalid, and `2` means invalid input. It does not install skills or prove activation or repository setup. For plugin installations, use your agent's installed catalog and definition access instead of assuming a filesystem path.

After installation, confirm that the skills are available to the current session. Run `setup-matt-pocock-skills` once in the **target development repository**, following its confirmation process; reuse valid existing setup. Required installation does not mean every task must run every stage. Explicit-only skills retain their invocation requirements, and tracker writes or commits still require authorization.

Then ask your agent to use `mkl-solid-code-development` for the task. For example:

> Use mkl-solid-code-development to implement this feature from the attached requirements. Clarify any business decisions that block implementation, then deliver verified code and a scoped review.

The entry point is [SKILL.md](SKILL.md). It loads detailed references only when needed.

## Optional delivery-record tools

The tools require **Python 3.10+** and use only the standard library. No package installation or network access is required to run them.

From the repository root, use the following executable examples. Replace `path/to/delivery`, `TASK-1`, and the summary with values for your task; these example initialization and validation commands are not pre-executed:

```bash
python3 scripts/init_delivery.py path/to/delivery --id TASK-1 --summary "Delivery objective" --intent implement --with-brief
python3 scripts/validate_delivery.py path/to/delivery/delivery-record.json --require-ready
```

Initialization refuses to overwrite existing files. Validation checks structure, references, declared evidence coverage, and readiness; it never executes recorded commands. **A ready record is not proof of correct software or SOLID compliance.**

See [Delivery Records and Tools](references/delivery-record.md) for the schema, task intents, evidence requirements, and exit codes.

## Skill routing and optional modeling support

The required Matt Pocock Skills and `mkl-uml-robustness-diagram` provide the preferred execution path. If a prerequisite is missing, install it through a supported installer where authorized and recheck. If installation, activation, or required setup is unavailable, report the gap and pause dependent stages without claiming the integrated workflow ran.

Other MKL use-case and UML skills remain optional for deeper modeling. The included robustness reference supports the required robustness-analysis skill. Installation does not require every task to produce a diagram or enter a formal MKL gate. See [Workflow Prerequisites and Skill Routing](references/optional-skills.md) for handoffs, invocation constraints, and optional modeling capabilities.

## Repository layout

```text
SKILL.md                  Agent entry point
agents/openai.yaml        Skill metadata and icon references
references/               Analysis, design, tool, and optional-skill guidance
scripts/                  Prerequisite checker and delivery-record tools
assets/                   Reusable templates and icon
tests/                    Regression tests, synthetic fixtures, and workflow scenarios
```

Teaching examples and synthetic fixtures illustrate the method. They do not supply default business rules or evidence for another task.

## Verification

Run this command from the repository root. It has no placeholder arguments and was executed when preparing this publication:

```bash
python3 -m unittest discover -s tests -v
```

The published source passed **39 regression tests on Python 3.14.7**. The suite includes prerequisite discovery and failure reporting, the design-readiness gate, invalid UTF-8 input and retry behavior, evidence references, overwrite protection, and command non-execution. The two original defect-reproduction checks also passed before publication.

See [Independent Forward-Testing Scenarios](tests/behavioral-cases.md) for evaluating workflow decisions. Script tests and scenario documents do not establish correctness for every future task.
