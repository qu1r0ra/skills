---
name: qu1r0ra-implement
description: "Implement a spec or ticket with the upstream workflow, bounded leaf-subagent review, and autonomous verified closeout."
disable-model-invocation: true
---

# qu1r0ra-implement

Use this personal wrapper when implementing a defined specification or ticket.
It preserves the upstream implementation workflow while adding the user's
stable review, harness, and delivery policy.

## 1. Apply the upstream implementation workflow

Read and follow the current upstream skill at:

`C:\Users\Quirora\AppData\Roaming\skillshare\skills\implement\SKILL.md`

Treat that file as upstream-owned. Do not edit or replace it. Complete its
implementation, testing, review, and commit steps before proceeding.

Completion: the scoped implementation is committed on its dedicated branch,
and the verification evidence is available.

## 2. Apply the personal review policy

Use the harness's actual leaf-subagent primitive for code review. Reviewers are
read-only leaf workers: they do not create tasks, chats, threads, forks,
worktrees, branches, handoffs, or further reviewers. In Codex, use a true
subagent worker when available; visible Codex tasks, chats, forks, and threads
are not reviewer substitutes. If the worker is unavailable, keep that review
lane in the parent and record the fallback.

### Codex worker model pin

When the harness is Codex, configure every delegated worker in this workflow
with `model=gpt-5.6-luna` and `thinking=high`: implementation workers,
Standards reviewers, Spec reviewers, and any authorized emergency reviewer.
Pass both values explicitly on every dispatch so the worker has an intentional
configuration independent of the supervising agent. Keep the supervising agent
on its current model. Treat an unavailable or rejected Luna High dispatch as a
failed worker lane; continue in the parent only when the harness permits that
fallback, and record it in the receipt.

### Antigravity worker model pin

When the harness is Antigravity, configure every delegated worker in this
workflow through the `agy` CLI with `--model gemini-3.8-flash-medium` and
`--effort medium`: implementation workers, Standards reviewers, Spec
reviewers, and any authorized emergency reviewer. Pass both values explicitly
on every dispatch and record the resolved values in the receipt. Keep the
supervising agent on its current model. Treat an unavailable or rejected
Gemini Flash 3.8 dispatch as a failed worker lane; continue in the parent only
when the harness permits that fallback, and record it in the receipt.

Count complete Standards+Spec reviewer pairs for the ticket:

- Pair 1 and Pair 2 are the normal budget.
- Pair 3 is one pre-authorized emergency pair only when the first two pairs
  leave unresolved critical risk, materially conflict on a critical path, or
  leave a critical review lane unavailable.
- Record the emergency trigger before dispatching Pair 3.
- Pair 4 is outside this workflow. Do not silently create replacement pairs.

Completion: the receipt states the number of review pairs used, the resolved
model and reasoning effort for every Codex or Antigravity worker, and, for
Pair 3, the emergency trigger.

## 3. Complete the implementation closeout

After the implementation commit and review, apply the shared closeout procedure
at:

`C:\Users\Quirora\AppData\Roaming\skillshare\skills\qu1r0ra-implement\references\implementation-closeout.md`

Do not stop at “committed and reviewed” and ask the user to repeat the landing
request. Unless the user explicitly requested handoff-only retention, continue
through the delivery-mode branch:

- local-only: merge into the supervising branch, publish when possible, remove
  the exact clean implementation worktree, delete its merged local branch, and
  update or close the ticket according to acceptance state;
- remote-backed: publish the feature branch, merge the pull request when all
  required automated gates pass and no human gate remains, verify the merge,
  retire local and permitted remote feature branches, and update or close the
  ticket;
- issue-only: update the coordinating ticket without inventing an
  implementation merge.

Use one retry for a failed Git publication. If publication remains unavailable,
preserve the verified local result, leave the ticket open or in its
publication-follow-up state, and report the exact failure.

Completion: the implementation is landed or has a named unresolved gate, the
secondary worktree/branch state is verified, and the affected ticket receipt
is live and accurate.

## 4. Final receipt

Report implementation commits, review-pair count, tests, merge or pull-request
SHA, publication result, retired worktrees and branches, ticket state, and any
remaining human or technical gate. Do not claim ticket closure from a merge
alone.
