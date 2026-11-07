# Dependency Compatibility and Distribution

Use this reference to reproduce a checked environment, upgrade dependencies, or prepare a distribution. The repository and its verification materials are domain-independent; detailed application acceptance stays in a separate workspace.

## Current dependency snapshot

The synchronization targets MKL UML **v1.1.1**, source commit
`064c2e6eea494c68e2684ae58be155d76cbc13fb`: nine skills including
`mkl-uml-c4-architecture`. The wrapper now checks 20 named prerequisites: 11 Matt and
nine MKL definitions. Check the installed definitions and invocation metadata again
when upgrading; installation, host activation and completed execution are separate.

Matt definitions were checked at `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`.
All 516 copied upstream files matched the corresponding tracked sources (413 MKL,
103 Matt); no copied-source mismatch was observed.

The standard wildcard route was exercised locally on 2026-11-07 with Skills CLI 1.7.4:
38 Matt definitions and nine MKL definitions were installed in an isolated project.
The updated `full-workflow` presence check passed all 20 required definitions. This is
installation/presence evidence, not execution of all 47 skills. The task-specific logs,
file identities and forward evaluations stay outside this business-independent package.

Ordinary commands remain unpinned `npx skills add` routes in [README](../README.md#install-and-verify).
Moving `main` is not a reproducible pin. Record source identity/installed hashes for
reproduction rather than claiming the current dependency checker authenticates provenance.
Read the actual updated C4, PDR, class, sequence and CDR instructions; reuse only the
contracts their supported arguments and evidence actually provide.

## Historical installation observations

The earlier 19-definition snapshot used Matt at
`a496f5513d4a4cf889bc48e189e579f4b0bdf6aa` and MKL at
`a843431ec8a8cf7889e955361e7425d601278eb9`. Its 431 compared dependency files and 19-name
presence result are historical. The 2026-10-30 complete-collection check installed 46
skills (38 Matt and eight MKL). Neither observation establishes the new C4 requirement.
PyYAML 6.0.3 remains the parser declared in `requirements.txt`.

## Capability and legacy profiles

Every integrated task requires **all 20 prerequisites**, regardless of its selected stages. Default `full-workflow` checks that set. Explicit `core` retains its historical 12-definition check; `detailed-design` retains its historical 14-definition check. Those partial modes support old tooling and diagnosis, and do not satisfy the current integrated workflow requirement.

Installation, readable definitions, session availability, repository setup, rendering, and completed workflow execution are separate observations. Reuse valid installation and configuration; preserve existing customization. The checker does not add a `triage` requirement, while complete Matt-repository installation can make it available. A state view uses the project's actual available UML toolchain.

## Delivery-record compatibility

The eight-stage narrative does not rename stored IDs or migrate existing records. Handoffs remain generic and accept older stage counts/names. The additive `--require-through HANDOFF_ID` gate checks a selected producer prefix without requiring later stages to finish; omitting it preserves existing handoff behavior. `--require-design` retains its narrow detailed-bundle scope for records without architecture. A declared architecture bundle adds upstream readiness and explicit `architecture_view_ids` coverage; `--require-architecture` can check that bundle alone. This is an additive schema-version-1 extension. Every selected architecture/design rule must be confirmed. The earlier correction remains: every selected rule must now be confirmed regardless of its global blocking flag. Previously accepted design bundles that selected an unconfirmed nonblocking rule must settle or remove that current dependency before becoming ready.

Review capture explicitly rejects selected `skip-worktree` or `assume-unchanged` index states, including sparse paths, rather than returning incomplete bytes. Narrowing scope is valid only when excluded paths are genuinely outside the task. The helper preserves the repository/index and exports color-free patches; it does not automatically materialize sparse files.

Delivery and capture tools require Python 3.10+; the checker additionally requires PyYAML. Historical regression results and fresh candidate results are distinguished in [verification evidence](../tests/ACCEPTANCE.md). Untested interpreters, operating systems, host activation and integrations need their own verification. Renderer syntax, structural profiles and visual inspection have distinct coverage; none proves all design semantics.

## License and third-party notices

This project is licensed under [Apache-2.0](../LICENSE); see [NOTICE](../NOTICE). Independently installed skills retain their own licenses:

- Matt Pocock Skills: MIT, with the original notice preserved in [licenses/mattpocock-skills-MIT.txt](../licenses/mattpocock-skills-MIT.txt).
- MKL UML: Apache-2.0, with source and adaptation attribution preserved in [licenses/mkl-uml-NOTICE.txt](../licenses/mkl-uml-NOTICE.txt). The standard Apache license text is provided in this package's LICENSE.

The project links these dependencies rather than bundling their implementations. If a distributor additionally packages installed skill directories, retain the appropriate license text, copyright notices, applicable NOTICE material, and modification notices with those actual copies. The current Skills CLI may copy a skill leaf directory without its parent repository's MIT file; include the corresponding original notice in that distribution. Retaining this project's NOTICE alone does not replace notices required by an additional third-party copy.

License sources: [Matt snapshot](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/LICENSE), [MKL snapshot](https://github.com/kinglez/mkl-uml/blob/a843431ec8a8cf7889e955361e7425d601278eb9/LICENSE). CLI requirements and options: [package](https://github.com/vercel-labs/skills/blob/92a9a34ac3bf88e695e468b90c7bf32f163d32c8/package.json), [commands](https://github.com/vercel-labs/skills/blob/92a9a34ac3bf88e695e468b90c7bf32f163d32c8/docs/commands.md).
