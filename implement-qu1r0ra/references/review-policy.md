# Implementation review policy

Read this for the upstream code-review step in `implement-qu1r0ra`.

Before review, read [the shared model-routing policy](../../../../docs/agents/model-routing.md)
and the matching harness adapter:

- Antigravity: `harness-antigravity.md`
- Claude Code: `harness-claude-code.md`
- Codex: `harness-codex.md`

`model-routing.md` is the only preference source for the exact worker model and
effort. The harness adapter supplies the dispatch mechanism and must enforce
the pair listed there; if the current harness has no adapter or the pair is
unavailable, preserve the review lane as blocked.

### Review policy for the upstream `/code-review` step

Request independent Standards and Spec reviews when the
harness provides real leaf workers. Reviewers return one bounded, read-only
report and do not create tasks, chats, threads, forks, worktrees, branches,
handoffs, or further reviewers. The matching adapter defines the reviewer
selector and unavailable-lane receipt for that harness.

Count complete Standards+Spec reviewer pairs as review rounds for the ticket or batch.
The round budget is global, including re-review after a repair:

- Rounds 1 through 3 are allowed review rounds. Reuse the last pair for
  back-and-forth repair/re-review when continuity is useful, and count each
  completed re-review as the next round rather than silently resetting the
  budget.
- After a round reports a P1, repair the finding and re-review the changed
  scope before declaring completion. A round is complete only when both axes
  return their bounded report.
- Round 4 is one backup round after the three-round budget, authorized only
  when Round 3 still has an unresolved P1, or when a critical review lane was
  unavailable or materially conflicted during the allowed rounds. Record the
  trigger and the repair/re-review history before dispatching Round 4.
- If a P1 remains after Round 4, stop the review loop and report the named
  unresolved risk for human or owner intervention. Do not dispatch Round 5 or
  silently create replacement pairs.

Completion: the scoped implementation is committed on its dedicated branch,
verification evidence is available, and the receipt states the total
review-round/pair count, resolved reviewer configuration, each repair and
re-review trigger, final P1 disposition, and any Round 4 trigger.
