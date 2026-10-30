# Complete Prerequisites and Stage Routing

Use [Matt Pocock Skills](https://github.com/mattpocock/skills) with [MKL UML Skills](https://github.com/kinglez/mkl-uml). **Every task requires all 19 prerequisite definitions**, even when only selected stages execute. Installation and execution depth are separate decisions.

## Required capabilities

The required workflow subset contains 11 Matt capabilities and eight MKL capabilities. Install both upstream repositories in full; the checker verifies this named subset, not every optional skill in those repositories:

| Purpose / stage | Installed capabilities | Input → result |
|---|---|---|
| Setup | `setup-matt-pocock-skills` | Project choices → usable tracker/domain configuration |
| 1. Requirements clarification | `grill-with-docs`, `grilling`, `domain-modeling` | Sources → clarified answers, terminology and questions |
| 2. Requirements baseline | `mkl-use-case-specifier`, `mkl-uml-use-case-diagram` | Business basis → use-case behavior; actor/boundary view when needed |
| 3. Analysis | `mkl-uml-domain-modeler`, `mkl-uml-robustness-diagram`, `mkl-pdr-review`; `domain-modeling` when meanings change | Baseline → domain model, BCE coverage and PDR |
| 4. Detailed design | `codebase-design`, `mkl-uml-sequence-diagram`, `mkl-uml-design-class-model`, `mkl-cdr-review`, `to-spec`, `to-tickets` | Analysis → reviewed contracts/views, implementation specification and slices |
| 5. Coding | `implement`, `tdd` | Ready slice → code, behavior checks, refactoring and current views |
| 6. Code review | `code-review` | Fixed snapshot → two-axis findings and verified corrections |
| 7. Architecture review | `improve-codebase-architecture` | Reviewed implementation → scoped retain/adjust conclusion |

The coordinating skill produces the requirements baseline and arranges independent derivation of expected outcomes in stage 2. The use-case specifier does not replace those activities; no separately named oracle-generation skill is assumed. MKL leads conceptual modeling; Matt's `domain-modeling` actively sharpens meanings across stages instead of maintaining a competing model.

Install in the target project using the standard route:

```bash
npx skills add mattpocock/skills --skill '*'
npx skills add kinglez/mkl-uml --skill '*'
```

The quoted wildcard selects all skills; choose the target agent through the installer. The checker never runs these commands. A supported plugin installation is valid. Preserve customizations and use one route per agent. Consult the [upstream installation guidance](https://github.com/mattpocock/skills#installation-30-second-setup) when needed.

All MKL definitions are installed; artifacts remain need-based. The use-case diagram answers actor/boundary questions. Domain concepts differ from design classes. Non-OO structure can use a named module view. State diagrams use the project's available UML toolchain; definition presence implies neither a dedicated state skill nor a working renderer.

## Verify presence, activation, and setup

From the installed root and prepared [checker runtime](../README.md#prerequisite-checker-runtime), supply actual directories containing `skill-name/SKILL.md`:

```bash
.venv/bin/python scripts/check_prerequisites.py --skills-root path/to/skills
.venv/bin/python scripts/check_prerequisites.py --skills-root path/to/project-skills --skills-root path/to/global-skills --profile full-workflow
```

Default `full-workflow` checks 19 readable definitions with matching frontmatter names. Exit `0` means that presence check passed; `1` means missing/invalid definitions; `2` means invalid input/checker dependency. The checker does not install, overwrite, invoke skills, configure projects or test renderers.

Explicit legacy `core` (12) and `detailed-design` (14) profiles retain their historical subsets as compatibility/diagnostic modes. **Neither satisfies integrated prerequisites**, even for a small or review-only task.

Presence does not establish provenance, compatible behavior, session availability or setup. For plugins, inspect the actual installed catalog/definitions. Follow host activation procedures when new installations are unavailable in the session.

Install missing capabilities through a supported installer where authorized, then recheck. If installation/activation cannot complete, identify exactly what is missing and pause dependent integrated work. Continue justified independent work without claiming full readiness or execution of unavailable skills.

## Configure the actual consumers

Read [repository setup](repository-setup.md) before tracker/domain configuration is consumed. Reuse valid choices and inspect saved inputs. Installing the complete Matt collection also makes `triage` available. Installation does not execute it. The named local setup adaptation is needed only if required consumer vocabulary is still absent; inspect actual setup outputs instead of assuming an omitted configuration branch.

Installation does not select a tracker, configure a repository, authorize publication or activate explicit-only skills. A task using no tracker needs no unrelated tracker setup.

## Invocation and adaptations

Read selected definitions and use the host's supported invocation mechanism. Explicit-only skills require explicit invocation; the wrapper cannot bypass this silently. Reading or installing is not execution evidence.

Use upstream workflows only when their prerequisites and actions fit. For pending code/local delivery, use the named [implementation and two-axis review adaptation](local-review.md). Preserve actual project configuration/test seams and identify the route that ran.

Separate reviewers in independent contexts establish independence; two passes in one context do not. Missing host features require a limitation or named adaptation rather than a fabricated tool call. Commits, tracker writes, pushes, pull requests and deployment need matching authorization.

Supply current rules, source versions, artifacts, acceptance and scope, then inspect returned results against the [handoff contract](workflow-handoffs.md). Preserve current results and next steps in the existing task record for resumption.

### Host launch checklist

1. **Confirm session access.** After installation, inspect the host's current skill catalog. For Codex, select the installed skill through its skill picker or `$skill-name` mention. In a host exposing slash-command skills, use its actual `/skill-name` command. Follow that host's refresh procedure when an installed definition is absent; a path on disk does not establish current-session availability.
2. **Start with the wrapper and endpoint.** Supply source requirements, project location and the desired endpoint. The wrapper identifies the next producer, reads its available definition, and supplies the actual preceding outputs. Keep installation/setup work separate from stage-completion evidence.
3. **Activate selected explicit-only skills.** The checked Matt snapshot marks the following definitions explicit-only. Invoke the actual installed skill when choosing its original route; the wrapper's own mention does not automatically invoke these dependencies.

| Activation point | Explicit-only skill in the checked snapshot |
|---|---|
| Missing project configuration | `setup-matt-pocock-skills` |
| Unresolved requirements | `grill-with-docs` |
| Ready detailed design to implementation specification | `to-spec` |
| Ready specification to vertical slices | `to-tickets` |
| Unblocked implementation work | `implement` |
| Surrounding architecture investigation | `improve-codebase-architecture` |

4. **Choose a supported route.** When original invocation or tracker/commit actions do not fit authorized local delivery, use the named local adaptation and record that choice. If the host cannot provide a necessary original capability and no applicable adaptation fits, identify that specific blocker before dependent work advances. Do not record upstream execution from a definition read.
5. **Read back the result.** Check the stage output and actual execution evidence before selecting its next consumer. Resume using the saved handoff rather than restarting setup or assuming previous completion.

Check invocation metadata again when upgrading dependencies; this list describes the documented compatibility snapshot, not every future upstream version.

## Domain-independent distribution

The skill's own source repository and installed directory contain workflow mechanisms and neutral structural/protocol data only. Task-specific requirements, code, tests and evidence belong in the authorized target project or external acceptance workspace. During maintenance of this skill, keep application acceptance material outside its repository/package; do not import it as fixtures or defaults. This boundary does not prohibit business artifacts in the target application.
