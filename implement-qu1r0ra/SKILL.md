---
name: implement-qu1r0ra
description: "Implement a spec or ticket with the upstream workflow, bounded leaf-subagent review, and autonomous verified closeout."
disable-model-invocation: true
---

# Implement qu1r0ra

Use this personal wrapper when implementing a defined specification or ticket.
The invoking agent owns the implementation. This wrapper adds the user's
stable review, harness, and delivery policy to the upstream workflow.

## Run owner

Read `docs/agents/implementation-contract.md` for the execution-ownership
rule. Use the live ticket's target, scope, and acceptance criteria to select
the repository and delivery mode.

## 1. Apply the upstream implementation and review workflow

Read the protected [`implement`](../implement/SKILL.md) as the implementation
and review reference. This wrapper owns the invocation and uses its
implementation and testing steps.
For this wrapper, commit the complete scoped change before its `/code-review`
step so the protected review skill's `<fixed-point>...HEAD` diff includes the
implementation. Use the recorded branch base as the fixed point. Commit any
repair before re-review, and review the resulting branch diff. An empty or
incomplete diff is not a completed review. Apply the review policy below, then
record the final commit and review receipt.

Before review, read [`docs/agents/model-routing.md`](../../../docs/agents/model-routing.md)
and the matching harness adapter:

- Antigravity: `references/harness-antigravity.md`
- Claude Code: `references/harness-claude-code.md`
- Codex: `references/harness-codex.md`

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

Count complete Standards+Spec reviewer pairs as review rounds for the ticket.
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

## 2. Complete the implementation closeout

After the implementation commit and review, apply the shared
[implementation closeout procedure](references/implementation-closeout.md).

Do not stop at “committed and reviewed” and ask the user to repeat the landing
request. Unless the user explicitly requested handoff-only retention, continue
through the closeout procedure's selected delivery mode and failure branches.

Completion: the implementation is landed or has a named unresolved gate, the
secondary worktree/branch state is verified, and the affected ticket receipt
is live and accurate.

## 3. Final receipt

Report implementation commits, review-pair count, tests, landing commit,
publication result, retired worktrees and branches, ticket state, and any
remaining human or technical gate. Do not claim ticket closure from landing
alone. Completion: the receipt names every verified result and unresolved gate.
