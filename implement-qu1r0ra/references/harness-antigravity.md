# Antigravity harness adapter

Operational rules when running under the Antigravity harness (`agy`).

## Planning execution

Treat the invoked specification or ticket as pre-authorizing implementation:

- When creating an `implementation_plan.md` artifact, set `RequestFeedback: false`
  in `ArtifactMetadata`.
- Proceed immediately from plan generation into implementation and test
  tooling after the selected workflow's design and ticket approvals are settled.
- Never generate or update `walkthrough.md` artifacts; report completion and
  verification directly in chat output and the final receipt.
- Rely on the skill's integrated paired leaf-subagent review to catch drift
  rather than an interactive planning gate.

Completion: implementation tool calls begin immediately after plan artifact
generation when prerequisite approvals are settled.

## Implementation workers

Read the active AIOS checkout's `docs/agents/model-routing.md` before dispatch.
Inspect current `agy --help`, `agy models`, and native worker capabilities.
CLI model availability and CLI effort flags do not prove that a native child
accepts those controls. Native `invoke_subagent` definitions may expose only
`inherit`, `flash`, or `pro` tiers. Use a tier only when its resolved child
model and effort match the routed pair; otherwise leave that lane blocked.

Use native isolated worker workspaces for implementation. Verify their Git
registration, managed path, semantic branch, and integration base; a workspace
option alone does not prove these. Pass explicit context pointers because
native workers start with fresh context. Give mergers the integration checkout
and serialize its writers. Give exploration workers write access only for
their notes, or let the parent save their report. Keep review workers as leaves
even when the provider permits nested delegation.

Paseo ACP launch defaults are a different provider path; do not infer native
worker routing from them. References:
[native subagents](https://antigravity.google/docs/subagents) and
[models](https://antigravity.google/docs/models/).

## Independent review

Use the harness's actual read-only leaf-worker mechanism for Standards and Spec
review after implementation. Read `docs/agents/model-routing.md`, then verify
that the current `agy --help` and `agy models` output expose the exact
Antigravity pair listed there before dispatching. Pass that pair for every
review and re-review worker when the native mechanism exposes those controls;
otherwise verify the resolved pair as above. If the pair or independent review
mechanism is unavailable, record the affected review lane as unavailable;
deterministic parent verification may continue, but the receipt cannot claim
the missing review.

Completion: every dispatched review worker resolves to the exact Antigravity
pair listed in `model-routing.md`, and its resolved values are recorded.
