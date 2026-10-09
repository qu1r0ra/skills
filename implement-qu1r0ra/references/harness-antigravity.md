# Antigravity harness adapter

Before dispatch, read `docs/agents/model-routing.md` from the active AIOS
checkout, or its supervising checkout when working elsewhere. It owns role
preferences and dispatch evidence.

## Native workers

Use the native subagent mechanism with the routed `flash` tier. Set high
effort when the child interface exposes that control; otherwise record effort
as harness-controlled. A tier selector does not establish an exact model
version or resolved effort.

Native children start with fresh context. Pass the task, required rules and
source pointers, and expected output. For writing workers, select an isolated
workspace and verify its actual Git checkout, branch, and integration base
against the target repository's isolation contract before edits.

Use normal harness workers for separate Standards and Spec reports; provide
the fixed comparison and parent check results. Follow
[review-policy.md](review-policy.md) for review rounds and completion.

## Other surfaces

Headless CLI model/effort flags and `agy models` describe a separate launch
surface. They do not establish native child resolution. Paseo ACP provider
settings are another path; use its owning runbook for provider work.

Use native plan and completion artifacts under the active harness review
policy. AIOS design and ticket approvals still apply; the adapter adds no
artifact suppression or metadata override.

For current capabilities, consult official
[subagents](https://antigravity.google/docs/subagents?tab=cli),
[headless CLI](https://antigravity.google/docs/cli/headless/), and
[artifact review](https://antigravity.google/docs/cli/artifacts/) documentation.
