# Claude Code harness adapter

Operational rules when running under Claude Code.

## Independent review

Dispatch each Standards and Spec reviewer through the Agent tool with
`subagent_type: "leaf-reviewer"`. That definition
(`~/.claude/agents/leaf-reviewer.md`) pins the Claude Code pair from
`docs/agents/model-routing.md` in its `model` and `effort` frontmatter; the
Agent tool's own `model` parameter carries no effort, so leave it unset. Before
the first dispatch, read the definition and confirm its frontmatter matches the
Claude Code row. If the definition is missing or differs, record the review
lane as unavailable; deterministic parent verification may continue, but the
receipt cannot claim the missing review.

Completion: every review and re-review worker ran as `leaf-reviewer`, and the
receipt records the pair it resolved to.
