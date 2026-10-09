# Claude Code harness adapter

Before dispatch, read `docs/agents/model-routing.md` from the active AIOS
checkout, or its supervising checkout when working elsewhere. It owns role
preferences and dispatch evidence.

## Model and effort

The child model resolves in this order: the Agent call's `model`, the subagent
definition's `model`, `CLAUDE_CODE_SUBAGENT_MODEL` (v2.1.251+), then the session
model. Record which source set the routed model.

Pass the routed full model ID in the call when its schema accepts one. When the
call accepts only aliases, select a subagent definition whose `model` is the
full ID; use an alias only when its mapping to the routed ID is established.
With neither, the lane is blocked. An organization model restriction that
substitutes a fallback model also blocks the lane.

For explicit effort, pass the routed `effort` parameter to a non-fork Agent
call (Claude Code v2.1.292+), or select a subagent definition with that
`effort` field. Check `CLAUDE_CODE_EFFORT_LEVEL`: it takes precedence over both
controls, and a conflicting value blocks the lane. When the build predates
v2.1.292 and no definition carries the routed effort, the lane is blocked.
For inherited effort, omit the child override and record session effort from
`/effort status` when available.

Inspect `/tasks` (v2.1.242+) for observed child model and effort; inherited
effort may not be displayed. Keep session configuration distinct from
independently observed child resolution.

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
