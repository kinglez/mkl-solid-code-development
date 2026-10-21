# MKL SOLID Code Development

An agent skill for turning business requirements into understandable, extensible, and maintainable code.

The workflow connects confirmed rules, responsibility and interface design, implementation, verification, and review. It is domain-agnostic and works with the target project's language and conventions. Specialized skills are optional.

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

## Install and use

Install this repository with an agent skill installer that accepts GitHub repositories, or clone it into a skills directory supported by your agent.

The following is a runnable installation example, not a command executed by the skill. Run it from your agent's supported skills directory:

```bash
git clone https://github.com/kinglez/mkl-solid-code-development.git
```

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

## Optional specialized skills

This repository is self-contained. When available and appropriate, it can work with Matt Pocock skills for requirements clarification, domain modeling, module design, specifications, implementation, testing, and review, as well as MKL use-case and UML skills.

These skills are not bundled dependencies. Check their availability, instructions, and authorization requirements before use. See [Optional Skill Routing](references/optional-skills.md) for the capability map.

## Repository layout

```text
SKILL.md                  Agent entry point
agents/openai.yaml        Skill metadata and icon references
references/               Analysis, design, tool, and optional-skill guidance
scripts/                  Standard-library delivery-record tools
assets/                   Reusable templates and icon
tests/                    Regression tests, synthetic fixtures, and workflow scenarios
```

Teaching examples and synthetic fixtures illustrate the method. They do not supply default business rules or evidence for another task.

## Verification

Run this command from the repository root. It has no placeholder arguments and was executed when preparing this publication:

```bash
python3 -m unittest discover -s tests -v
```

The published source passed **31 regression tests on Python 3.14.7**. The suite includes the design-readiness gate, invalid UTF-8 input and retry behavior, evidence references, overwrite protection, and command non-execution. The two original defect-reproduction checks also passed before publication.

See [Independent Forward-Testing Scenarios](tests/behavioral-cases.md) for evaluating workflow decisions. Script tests and scenario documents do not establish correctness for every future task.
