# Validated Dependencies and Distribution

Use this reference when reproducing an accepted environment, upgrading dependencies, or preparing a customer distribution. It records an observed snapshot, not compatibility with all future upstream revisions.

## Dependency snapshot

| Component | Snapshot used for integration acceptance |
|---|---|
| Matt Pocock Skills, the 11 named in [routing](optional-skills.md) | `mattpocock/skills` at `d1478fcb140db0b93c0c8df17bcfd311844749d0` |
| Robustness analysis | `kinglez/mkl-uml` at `f6f21221ef950371700e0db5860f3e94e077bc07` |
| Skills CLI | `1.7.4`; upstream Node requirement `>=22.20.0` |
| Prerequisite YAML parser | PyYAML `6.0.3`, pinned in `requirements.txt` |

To reproduce the dependency sources using the standard Skills CLI, run these commands in the target project and choose the target agent. They install the same 12 named skills without adding `triage`:

```bash
npx skills@1.7.4 add https://github.com/mattpocock/skills/tree/d1478fcb140db0b93c0c8df17bcfd311844749d0 --skill setup-matt-pocock-skills grill-with-docs grilling domain-modeling codebase-design to-spec to-tickets implement tdd code-review improve-codebase-architecture
npx skills@1.7.4 add https://github.com/kinglez/mkl-uml/tree/f6f21221ef950371700e0db5860f3e94e077bc07 --skill mkl-uml-robustness-diagram
```

Preserve the target project's installation lock and actual file hashes with its acceptance results. On upgrade, compare the relevant upstream contracts and rerun setup, implementation/review, and scope-handling scenarios against the installed definitions. A matching skill name or successful download does not prove compatible behavior.

Script regressions are exercised on macOS with Python 3.12, 3.13, and 3.14. The delivery tools require Python 3.10+; older supported versions and other operating systems need separate validation before a customer-specific support claim. Prompt-driven scenario results cover the tested agent/session only.

## License and third-party notices

This project is licensed under [Apache-2.0](../LICENSE); see [NOTICE](../NOTICE). Independently installed skills retain their own licenses:

- Matt Pocock Skills: MIT, with the original notice preserved in [licenses/mattpocock-skills-MIT.txt](../licenses/mattpocock-skills-MIT.txt).
- MKL UML: Apache-2.0, with source and adaptation attribution preserved in [licenses/mkl-uml-NOTICE.txt](../licenses/mkl-uml-NOTICE.txt). The standard Apache license text is provided in this package's LICENSE.

The project links these dependencies rather than bundling their implementations. If a distributor additionally packages installed skill directories, retain the appropriate license text, copyright notices, applicable NOTICE material, and modification notices with those actual copies. The current Skills CLI may copy a skill leaf directory without its parent repository's MIT file; include the corresponding original notice in that distribution. Retaining this project's NOTICE alone does not replace notices required by an additional third-party copy.

License sources: [Matt snapshot](https://github.com/mattpocock/skills/blob/d1478fcb140db0b93c0c8df17bcfd311844749d0/LICENSE), [MKL snapshot](https://github.com/kinglez/mkl-uml/blob/f6f21221ef950371700e0db5860f3e94e077bc07/LICENSE). CLI requirements and options: [package](https://github.com/vercel-labs/skills/blob/92a9a34ac3bf88e695e468b90c7bf32f163d32c8/package.json), [commands](https://github.com/vercel-labs/skills/blob/92a9a34ac3bf88e695e468b90c7bf32f163d32c8/docs/commands.md).
