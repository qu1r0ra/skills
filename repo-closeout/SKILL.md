---
name: repo-closeout
description: "Review task-touched Git repositories, clean verified disposable local worktrees and branches, and report unmerged work for a merge-or-retain decision."
disable-model-invocation: true
---

# Repo Closeout

Use this skill when explicitly invoked as `$repo-closeout` at task handoff.

## Scope

Include every Git repository in which this task changed files or created or
used a task branch or worktree, including separate nested Git roots. Resolve
each path to its nearest Git root. Skip repositories that were only read. Do
not scan unrelated directories or infer that every repository on the machine
belongs to this task.

## Closeout

1. For each in-scope repository, read its agent instructions and the relevant
   delivery or worktree-retirement procedure before cleanup. Follow that
   repository's rules. In AIOS, read the implementation contract and its
   linked closeout and worktree-retirement procedures when they apply.
   **Done when:** the applicable instructions and procedures are identified
   for every in-scope repository, or missing guidance is recorded.
2. From the repository's primary checkout, inventory every registered worktree
   and local branch. For each branch, check whether it is checked out and
   whether it contains commits outside the repository's documented delivery
   base or a base established by its configuration. Apply the repository's
   delivery rules as well: a merged PR may have landed by squash or rebase and
   leave the original commits outside the base's ancestry. Verify the merged
   delivery record and change when needed; ancestry alone does not prove that
   work is unmerged. For task-related worktrees, inspect the branch, commit,
   tracked changes, untracked files, and ignored files. Record the base ref and
   commit used; local remote-tracking refs may be stale. Do not fetch or update
   provider state unless the task or repository rules authorize it. **Done
   when:** the repository base and each worktree and local branch have a
   recorded status, or an incomplete inspection is identified.
3. Remove a worktree only when it is task-owned or repository rules identify it
   as disposable, it is inactive, clean, has no untracked or ignored files,
   and its work is verified as delivered into the trusted base. Check task
   context and repository-documented configuration for known consumers whose
   paths point into the worktree; do not scan unrelated paths. If a known
   consumer points there, re-point it through its own procedure before removal.
   If a required consumer check cannot be completed, retain the worktree and
   report why. Use the repository's cleanup procedure or ordinary `git
   worktree remove`; never force removal. Do not remove the worktree the current
   agent session is using. If its session cannot be released or the cleanup
   context is unclear, retain it and report why. **Done when:** every
   inventoried worktree is removed and verified absent, or retained with its
   observed state and reason.
4. Delete a local branch only when it is not checked out, is not a protected,
   default, or long-lived branch, and all its changes are verified in the
   trusted delivery base by ancestry or the repository's delivery record.
   Use ordinary `git branch -d`; never force-delete. Leave remote branches
   untouched. A branch name or age alone is not proof that it is disposable.
   **Done when:** every inventoried local branch is deleted and verified
   absent, or retained with its observed state and reason.
5. Preserve work with unmerged commits, local changes, untracked or ignored
   files, uncertain ownership, or uncertain delivery status. For unmerged
   work, report the repo, branch and worktree, unique commits when knowable,
   and available delivery evidence. Recommend **merge** or **retain** with a
   short reason, then wait for the user's decision. This workflow does not
   merge, rebase, cherry-pick, push, open or update a PR, or delete remote
   branches. **Done when:** each unmerged item has its status and evidence,
   recommendation, and any pending user decision recorded.

## Report

For each in-scope repository, report the base ref and commit used, then account
for every inventoried worktree and local branch as removed or retained. Give
each item its observed status, disposition reason, and verification result.
For retained unmerged work, include unique commits when knowable, delivery
evidence, and the merge-or-retain recommendation. Identify incomplete
inspections; do not claim closeout is complete while any repository or item is
unaccounted for.

Completion: all applicable steps have recorded results, and any incomplete
inspection or pending user decision is identified.
