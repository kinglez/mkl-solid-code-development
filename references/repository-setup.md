# Repository Setup for the Integrated Workflow

Read this before a selected stage consumes tracker or domain configuration. The 12-skill installation baseline does not include `triage`. Some versions of `setup-matt-pocock-skills` therefore omit the label vocabulary, even though `to-spec` and `to-tickets` consume it. Complete the required inputs once instead of repeating unchanged setup.

## Reuse the actual repository choices

Read the selected consumers' installed instructions and the project's existing `AGENTS.md` or `CLAUDE.md`, tracker configuration, domain-document conventions, and label mapping. Use the paths those instructions identify; `docs/agents/` is the upstream default, not a required migration for an already configured project.

For the selected stages, establish:

| Consumer | Input that must be available |
|---|---|
| Domain work | The applicable glossary and ADR layout, including the rule for an absent document |
| Specifications and tickets | The tracker, publication location/operations, and canonical-role-to-tracker-label mapping |
| Publication using `ready-for-agent` | Its actual mapped value and, for a remote tracker, evidence that the label exists |

Reuse confirmed choices and valid configuration. Ask only about a missing choice that affects the work. Installation does not select a tracker, authorize remote writes, or activate a user-invoked skill.

## Run setup, then complete any omitted consumer input

1. If repository setup is needed, use the host's supported explicit invocation of `setup-matt-pocock-skills`. Follow its confirmation process. Inspect the files it actually returns rather than treating its completion message as the integration check.
2. Check the consumer inputs above. If `triage` is absent and setup omitted label configuration, complete the following **local setup adaptation**. This is additional integration work by this skill; it is not a claim that upstream setup produced those files or that `triage` ran.
3. Read the installed setup skill's `triage-labels.md` seed. Reuse an existing mapping where applicable. Otherwise use the target project's confirmed mapping, or establish the missing vocabulary with the user; the seed's canonical defaults are a proposal, not a replacement for existing labels.
4. Within the user's authorization, write the mapping at the project's established configuration location. Add or update its context pointer in the same project instruction file that setup uses. Preserve surrounding instructions and custom values; reuse the existing block rather than creating another `AGENTS.md`, `CLAUDE.md`, or duplicate setup section.
5. Read the saved configuration and supply its actual paths and relevant contents to the next consumer. Resolve a canonical role such as `ready-for-agent` through this mapping; preserve the mapped value when producing a local `Status` field or applying a tracker label. An upstream example's literal spelling does not override a configured mapping.

For the local Markdown tracker, no remote label creation is needed. Use its configured publication directory, one file per approved ticket, and blocking references as specified by that tracker. An authorized local adaptation can finish setup even when the optional `triage` skill is not installed.

For a remote tracker, read back the relevant label and access state. Create a missing label or publish an issue only when that action is authorized. If access, mapping, or authorization is unavailable, name that specific blocker and pause dependent publication; do not switch tracker, invent successful writes, or rerun the same unchanged setup as a remedy.

## Completion and handoff

Before specifications or tickets proceed, read the actual configuration and confirm that:

- The selected tracker and domain conventions are usable for this task.
- The consumers have the role vocabulary they require, including the mapped ready state.
- The publication operation and its authorization match the request.

Record the configuration sources, any local adaptation, the relevant mapped values, and the next consumer in the existing task record. This establishes configuration readiness only: approval of test seams, ticket breakdown, and other selected skills' invocation requirements still applies. Subsequent runs reuse this valid configuration; repeat setup only when its choices need to change.
