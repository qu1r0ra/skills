# Antigravity harness adapter

Operational rules when running under the Antigravity harness (`agy`).

## Planning execution

Treat the invoked specification or ticket as pre-authorizing implementation:

- When creating an `implementation_plan.md` artifact, set `RequestFeedback: false`
  in `ArtifactMetadata`.
- Proceed immediately from plan generation into implementation and test
  tooling without pausing for user approval.
- Never generate or update `walkthrough.md` artifacts; report completion and
  verification directly in chat output and the final receipt.
- Rely on the skill's paired leaf-subagent review (Section 2) to catch drift
  rather than an interactive planning gate.

Completion: implementation tool calls begin immediately after plan artifact
generation.

## Independent review

Use the harness's actual read-only leaf-worker mechanism for Standards and Spec
review after implementation. Read `docs/agents/model-routing.md`, then verify
that the current `agy --help` and `agy models` output expose the exact
Antigravity pair listed there before dispatching. Pass that pair for every
review and re-review worker. If the pinned pair or the independent review
mechanism is unavailable, record the affected review lane as unavailable;
deterministic parent verification may continue, but the receipt cannot claim
the missing review.

Completion: every dispatched review worker resolves to the exact Antigravity
pair listed in `model-routing.md`, and its resolved values are recorded.
