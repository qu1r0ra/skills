# Codex harness adapter

Before dispatch, read `docs/agents/model-routing.md` from the active AIOS
checkout, or its supervising checkout when working elsewhere. It owns role
preferences and dispatch evidence; this adapter maps them to Codex controls.

## Launch controls

For Codex-native subagents, set model and reasoning effort in the agent
configuration supported by the installed runtime. Check the current
[subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents)
when configuring that surface; its configuration is distinct from a host's
collaboration API.

When the collaboration API exposes `model`, `reasoning_effort`, and
`fork_turns`, pass the routed model and effort explicitly. Use
`fork_turns: "none"` with a self-contained assignment and context pointers when
full-history forks cannot accept overrides. A task-name response proves
acceptance, not independently resolved model or effort.

## Worker context

Use the normal subagent mechanism for separate Standards and Spec reports.
Give reviewers the fixed comparison, applicable sources, and parent check
results. Follow [review-policy.md](review-policy.md) for review rounds and
completion.

For writing workers, provide the exact checkout and integration base required
by the target repository. A child thread or context fork does not establish
Git isolation; verify the checkout before edits.
