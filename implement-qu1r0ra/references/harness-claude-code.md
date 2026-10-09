# Claude Code harness adapter

Before dispatch, read `docs/agents/model-routing.md` from the active AIOS
checkout, or its supervising checkout when working elsewhere. It owns role
preferences and dispatch evidence.

## Model and effort

Pass the routed full model ID in the Agent call when supported. Family aliases
can resolve to another version; use one only when its mapping to the routed ID
is established. Check effective settings and launching environment for
`CLAUDE_CODE_SUBAGENT_MODEL` and `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` when resolving
overrides. A conflicting force setting or organization model substitution
blocks the lane; respect organization policy.

For explicit effort, pass the routed `effort` parameter to a non-fork Agent
invocation when supported (Claude Code v2.1.292+), or select a subagent
definition with that `effort` field. Check `CLAUDE_CODE_EFFORT_LEVEL`: it takes
precedence over both controls, and a conflicting value blocks the lane.
For inherited effort, omit the child override and record session effort from
`/effort status` when available.

Inspect `/tasks` for observed child model and effort; inherited effort may not
be displayed. Keep session configuration distinct from independently observed
child resolution.

## Worker types and context

Use `general-purpose` for writing workers. Use normal review-capable subagents,
such as `Explore`, for separate Standards and Spec reports, following
[review-policy.md](review-policy.md). `Explore` omits the `CLAUDE.md` hierarchy
and Git status snapshot, and fresh children lack the parent conversation.
Provide the required rules, fixed Git comparison, source pointers, and parent
check results explicitly.

Native `isolation: worktree` starts from the default branch. For a writing
assignment, verify the actual checkout, branch, and integration base against
the target repository's isolation contract before edits.

When checking installed-version behavior, use the official
[subagent](https://code.claude.com/docs/en/sub-agents) and
[model configuration](https://code.claude.com/docs/en/model-config) references.
