# Claude Code harness adapter

Operational rules when running under Claude Code.

## Worker configuration and implementation

Read the active AIOS checkout's `docs/agents/model-routing.md` before each
dispatch, using the supervising AIOS checkout when operating elsewhere.
Check effective settings and the launching environment for both
`CLAUDE_CODE_SUBAGENT_MODEL` and `CLAUDE_CODE_SUBAGENT_MODEL_FORCE`; the routing
policy keeps them unset. An inherited force setting blocks compliant dispatch
until resolved. Do not change an organization policy to bypass it.

Pass the routed full model ID in the Agent call where accepted. If that
surface accepts only a family alias, use its matching alias only when the
resolved child is the exact routed ID; family selection can inherit the
parent's version. Verify the resolved model in `/tasks` and record inherited
session effort. A substituted model leaves the lane unavailable. Check the
installed runtime and account support for the routed model before claiming
that lane usable; use current official model/subagent documentation.

Use a writable `general-purpose` worker for implementation, merging, repairs,
or exploration that must save files. Pass bounded context pointers and the
exact managed worktree and integration base. Native `isolation: worktree`
starts from the default branch, so verify the actual base before edits and
establish the intended clean scoped checkout without overwriting existing
state. The run owner controls integration writers and final delivery.

## Independent review

Use the worker configuration above for each reviewer and re-reviewer; a
global forced pin is not a substitute for explicit role routing.

Dispatch separate Standards and Spec reviews with the built-in read-only
`Explore` subagent when it is available. Give each worker a bounded scope, the
fixed diff, the applicable standards or specification sources, and an explicit
request for one evidence-based report with no edits or further delegation.
The parent owns every build, test, and lint run: pass its command results in
the dispatch, and reviewers judge the code against that evidence and run
nothing.
`Explore` does not inherit `CLAUDE.md` or a Git status snapshot, so include the
needed agent rules and Git scope in the dispatch. If no suitable read-only
worker is available, mark the lane unavailable; deterministic parent
verification may continue, but the receipt cannot claim the missing review.

Check the resolved worker model in Claude Code's task view while the worker
runs, and record the model, the inherited session effort, reviewer type, and
any unavailable lane in the receipt. Completion means each required review and re-review used
the routed pair and returned one bounded, read-only report, or its absence is
explicit in the receipt.

References: [subagents](https://code.claude.com/docs/en/sub-agents) and
[model configuration](https://code.claude.com/docs/en/model-config).
