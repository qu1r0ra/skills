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
rule. The ticket's `Recommended run configuration` is the human's
pre-invocation routing aid; apply the contract directly once this skill runs.

## 1. Apply the upstream implementation and review workflow

Read and follow the current upstream skill at:

`C:\Users\Quirora\Documents\qu1r0raOS\agent-skills\skills\implement\SKILL.md`

Treat that file as upstream-owned. Follow its implementation and testing steps.
At its `/code-review` step, apply the review policy below. This upstream call
is the Standards and Spec review for this implementation. Complete the
upstream commit step after that review.

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

After the implementation commit and review, apply the shared closeout procedure
at:

`C:\Users\Quirora\Documents\qu1r0raOS\agent-skills\skills\implement-qu1r0ra\references\implementation-closeout.md`

Do not stop at “committed and reviewed” and ask the user to repeat the landing
request. Unless the user explicitly requested handoff-only retention, continue
through the delivery-mode branch:

- local-only: merge into the supervising branch, publish when possible, remove
  the exact clean implementation worktree, delete its merged local branch, and
  update or close the ticket according to acceptance state;
- remote-backed AIOS control-plane work: follow the direct-to-`main` landing
  path in the shared closeout procedure, verify the pushed commit, retire the
  local feature branch, and update or close the ticket;
- other remote-backed work: publish the feature branch, merge its pull request
  when all required automated gates pass and no human gate remains, verify the
  merge, retire local and permitted remote feature branches, and update or
  close the ticket;
- issue-only: update the coordinating ticket without inventing an
  implementation merge.

Use one retry for a failed Git publication. If publication remains unavailable,
preserve the verified local result, leave the ticket open or in its
publication-follow-up state, and report the exact failure.

Completion: the implementation is landed or has a named unresolved gate, the
secondary worktree/branch state is verified, and the affected ticket receipt
is live and accurate.

## 3. Final receipt

Report implementation commits, review-pair count, tests, landing commit,
publication result, retired worktrees and branches, ticket state, and any
remaining human or technical gate. Do not claim ticket closure from landing
alone.
