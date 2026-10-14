# Claude Code harness adapter

Before dispatch, read `docs/agents/model-routing.md` from the active AIOS
checkout, or its supervising checkout when working elsewhere. It owns role
preferences and dispatch evidence.

## Model and effort

The child model resolves in this order: the Agent call's `model`, the subagent
definition's `model`, `CLAUDE_CODE_SUBAGENT_MODEL`, then the session
model. Record which source set the routed model.

The Agent call's `model` takes an alias (`haiku`, `sonnet`, `opus`, `fable`),
never a full ID. Pass the alias for the routed ID: `claude-haiku-5-5` is
`haiku`, `claude-sonnet-5-5` is `sonnet`, `claude-opus-5-5` is `opus`. The
alias resolves to the current model of its family, so a child's self-reported
ID is unverified; record it as such. When the alias cannot reach the routed
ID, select a subagent definition whose `model` is the full ID, else the lane is
blocked. An organization model restriction that substitutes a fallback model
also blocks the lane.

Pass the routed `effort` (`low` through `max`) on every non-fork Agent call
(Claude Code v2.1.292+), or select a subagent definition with that `effort`
field. Check `CLAUDE_CODE_EFFORT_LEVEL`: it takes precedence over both
controls, and a conflicting value blocks the lane. When the build predates
v2.1.292 and no definition carries the routed effort, the lane is blocked.
The routed-dispatch ledger binds the call's `effort` to the route.

Inspect `/tasks` (v2.1.242+) for observed child model and effort. Keep session configuration distinct
from independently observed child resolution.

## Worker types and context

Use `general-purpose` for writing workers and for Standards and Spec reviewers,
following [review-policy.md](review-policy.md). `Explore` and `Plan` omit the `CLAUDE.md` hierarchy
and Git status snapshot, and fresh children lack the parent conversation.
Provide the required rules, fixed Git comparison, source pointers, and parent
check results explicitly.

Native `isolation: worktree` starts from the default branch. For a writing
assignment, verify the actual checkout, branch, and integration base against
the target repository's isolation contract before edits.

When checking installed-version behavior, use the official
[subagent](https://code.claude.com/docs/en/sub-agents) and
[model configuration](https://code.claude.com/docs/en/model-config) references.
