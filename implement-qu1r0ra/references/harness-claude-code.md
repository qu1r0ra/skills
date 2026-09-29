# Claude Code harness adapter

Operational rules when running under Claude Code.

## Independent review

Read `docs/agents/model-routing.md` before dispatch. Confirm that the active
Claude Code settings pin the listed worker model through
`CLAUDE_CODE_SUBAGENT_MODEL` and `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1`, and that
the session effort matches the listed effort. Pass no model in the Agent tool
call. If the pair cannot be confirmed or the harness cannot expose it, mark
the review lane unavailable.

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
runs, and record the model, session effort, reviewer type, and any unavailable
lane in the receipt. Completion means each required review and re-review used
the routed pair and returned one bounded, read-only report, or its absence is
explicit in the receipt.
