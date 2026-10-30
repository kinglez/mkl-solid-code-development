# Dependency Compatibility and Distribution

Use this reference to reproduce a checked environment, upgrade dependencies, or prepare a distribution. The repository and its verification materials are domain-independent; detailed application acceptance stays in a separate workspace.

## Current dependency snapshot

| Component | Observed snapshot |
| --- | --- |
| Matt Pocock Skills: 11 named definitions | `mattpocock/skills` at `a496f5513d4a4cf889bc48e189e579f4b0bdf6aa` |
| MKL UML: all 8 definitions | `kinglez/mkl-uml` at `a843431ec8a8cf7889e955361e7425d601278eb9` |
| Installation route exercised | Skills CLI `1.7.4`, project-scoped copies for Codex |
| Checker parser | PyYAML `6.0.3`, declared in `requirements.txt` |

The 19 prerequisite definitions were installed with the standard CLI into an isolated local project. All 431 installed dependency files were compared by Git blob identity with the pinned source trees above; they matched. The default `full-workflow` presence check returned exit 0 for all 19. These facts establish copied bytes and readable names, not execution of every skill or host activation.

For ordinary installation, install both upstream repositories in full with the standard wildcard commands in [README](../README.md#install-and-verify). The source-identity observations above describe the earlier named-subset acceptance, not a claim that only 19 skills are installed by the complete-repository route. To reproduce these exact dependency revisions, select the corresponding source revision with the supported installer and preserve the installation lock and file hashes. Do not describe moving `main` as a pinned installation. Upgrading a dependency calls for checking its changed setup, specification, modeling, implementation and review contracts before relying on prior results.

## Complete-collection installation check

The standard wildcard route was exercised on 2026-10-30 in an isolated project: both upstream collections installed successfully, producing 46 definitions (38 Matt and 8 MKL). The `full-workflow` checker then passed its 19 named prerequisites. This is installation/presence evidence, not execution of all optional skills. The older 19-definition source-identity observation above remains scoped to its original subset.

## Capability and legacy profiles

Every integrated task requires **all 19 prerequisites**, regardless of its selected stages. Default `full-workflow` checks that set. Explicit `core` retains its historical 12-definition check; `detailed-design` retains its historical 14-definition check. Those partial modes support old tooling and diagnosis, and do not satisfy the current integrated workflow requirement.

Installation, readable definitions, session availability, repository setup, rendering, and completed workflow execution are separate observations. Reuse valid installation and configuration; preserve existing customization. The checker does not add a `triage` requirement, while complete Matt-repository installation can make it available. A state view uses the project's actual available UML toolchain.

## Delivery-record compatibility

The seven-stage narrative does not rename stored IDs or migrate existing records. Handoffs remain generic and accept older stage counts/names. The additive `--require-through HANDOFF_ID` gate checks a selected producer prefix without requiring later stages to finish; omitting it preserves existing handoff behavior. `--require-design` retains its bundle-only scope, with one intentional correction: every selected rule must now be confirmed regardless of its global blocking flag. Previously accepted design bundles that selected an unconfirmed nonblocking rule must settle or remove that current dependency before becoming ready.

Review capture explicitly rejects selected `skip-worktree` or `assume-unchanged` index states, including sparse paths, rather than returning incomplete bytes. Narrowing scope is valid only when excluded paths are genuinely outside the task. The helper preserves the repository/index and exports color-free patches; it does not automatically materialize sparse files.

Delivery and capture tools require Python 3.10+; the checker additionally requires PyYAML. Historical regression results and fresh candidate results are distinguished in [verification evidence](../tests/ACCEPTANCE.md). Untested interpreters, operating systems, host activation and integrations need their own verification. Renderer syntax, structural profiles and visual inspection have distinct coverage; none proves all design semantics.

## License and third-party notices

This project is licensed under [Apache-2.0](../LICENSE); see [NOTICE](../NOTICE). Independently installed skills retain their own licenses:

- Matt Pocock Skills: MIT, with the original notice preserved in [licenses/mattpocock-skills-MIT.txt](../licenses/mattpocock-skills-MIT.txt).
- MKL UML: Apache-2.0, with source and adaptation attribution preserved in [licenses/mkl-uml-NOTICE.txt](../licenses/mkl-uml-NOTICE.txt). The standard Apache license text is provided in this package's LICENSE.

The project links these dependencies rather than bundling their implementations. If a distributor additionally packages installed skill directories, retain the appropriate license text, copyright notices, applicable NOTICE material, and modification notices with those actual copies. The current Skills CLI may copy a skill leaf directory without its parent repository's MIT file; include the corresponding original notice in that distribution. Retaining this project's NOTICE alone does not replace notices required by an additional third-party copy.

License sources: [Matt snapshot](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/LICENSE), [MKL snapshot](https://github.com/kinglez/mkl-uml/blob/a843431ec8a8cf7889e955361e7425d601278eb9/LICENSE). CLI requirements and options: [package](https://github.com/vercel-labs/skills/blob/92a9a34ac3bf88e695e468b90c7bf32f163d32c8/package.json), [commands](https://github.com/vercel-labs/skills/blob/92a9a34ac3bf88e695e468b90c7bf32f163d32c8/docs/commands.md).
