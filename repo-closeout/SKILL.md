---
name: repo-closeout
description: "Assess task-touched Git repositories at handoff or run completion; retire eligible disposable local Git state and record retained work and cleanup holds."
---

# Repo Closeout

Invoke at task handoff or final run assessment, including automatically from
an orchestrating workflow. Use the owning repository's delivery and retirement
contracts across repositories and harnesses. Assessment does not expand the
task's cleanup authority or deliver unmerged work.

## Scope and inventory

1. Include every Git root where the task changed files or created or used a
   task branch or worktree, including separate nested roots. Resolve each
   path to its nearest Git root. Skip read-only repositories and unrelated
   directories. Read each root's instructions and relevant delivery/retirement
   procedures. In AIOS, resolve `docs/agents/implementation-contract.md`, its
   lifecycle reference and `docs/operations/worktree-retirement.md` through the
   supervising checkout. Completion: each scoped root and applicable contract
   is identified, with missing guidance recorded.
2. From a supervising checkout, inventory registered worktrees and local
   branches within each scoped root. Record the trusted delivery base and
   exact commit from the repository's contract or configuration; note stale
   local refs. Refresh provider state only when authorized. Check branch tips,
   checkout registrations and commits outside that base. For task-related
   worktrees inspect tracked, untracked and ignored state and task activity.
   Check task context and repository-documented consumers, including app/thread
   bindings and sessions or processes using the target; stay within scoped
   evidence sources. Completion: every inventoried item has observed identity,
   task relationship, delivery, activity and consumer status, or a named
   incomplete inspection. Unrelated refs receive read-only recommendations.

## Eligibility and cleanup

3. Establish cleanup eligibility per target before mutation. Automatic removal
   requires task ownership, or an explicit repository rule identifying that
   target as disposable for this task. Preserve historical, unrelated,
   protected, default and long-lived refs. A name or age proves no ownership.
   Preserve targets with uncertain delivery, unknown consumers, app bindings,
   or live/unknown session or process use. Release bindings only through their
   owning procedure and existing authority; otherwise record release steps.
   The current agent's worktree is retained until its session is released and
   cleanup can run from a supervising checkout. Completion: each target is
   eligible with evidence or retained with the exact missing condition.
4. Verify delivery under the owning contract, not ancestry alone. A squash or
   rebase may leave delivered feature commits outside the trusted base. For
   PR delivery record destination repository/branch, PR URL, tested head/base,
   required-check result and merge SHA; verify merged state and merge ancestry
   on the trusted destination. The local tip must equal or be ancestral to
   the tested head. Rewritten history requires a delivery record binding that
   exact original tip to the verified merged change. Missing or ambiguous
   identity/check evidence retains the target. Use a repository's explicit
   integrated-worker retirement route only when its conditions hold; record
   that integration separately from accepted delivery. Completion: each
   candidate has revision-bound delivery or permitted integration evidence,
   or its missing evidence is recorded.
5. Retire eligible worktrees through the repository's procedure. Without a
   preservation procedure, require a clean inactive worktree with no untracked
   or ignored files and verified accepted delivery; use ordinary
   `git worktree remove`, never forced removal. A repository procedure may
   archive and verify retained content before removal; ignored counts alone
   grant no deletion authority. Verify Git registration and filesystem absence.
   Completion: every candidate is removed with the required receipt, or
   retained with observed result and release/recovery condition.
6. Retire an eligible local branch only when no worktree checks it out and its
   exact tip still matches the verified delivery evidence. Use ordinary
   `git branch -d` when ancestry permits. A squash/rebase `-D` route requires
   the complete step 4 delivery record and the owning contract's permission;
   leave the ref when either is missing. In AIOS follow the separate local
   branch-retirement procedure, including its exact-tip recovery mapping when
   applicable. Leave remote branches untouched. Completion: every candidate
   ref is verified absent or retained with its tip and reason.

## Access failure recovery

Use this branch only when an eligible cleanup target could not be removed.

7. Diagnose the exact failure from its result and current state. Distinguish
   permission/ACL or privilege failures from sharing locks, active sessions,
   bindings, changed identities and incomplete evidence. Reconcile partial or
   unknown results before retrying. Resolve routine authorized causes; preserve
   the target if ownership, delivery, consumer or activity evidence is uncertain.
   Give such targets release or recovery instructions, not a destructive script.
   Completion: the cause and current state are evidenced, or the diagnosis gap
   and safe recovery steps are recorded.
8. When eligibility is established and a diagnosed access problem still
   prevents cleanup, automatically prepare a targeted reviewable script as a
   handoff artifact, under the repository's permitted scratch location. It
   defaults to preview and requires an explicit apply option. Bind its target
   manifest to the exact resolved path, Git root/common directory, worktree
   registration, branch ref and expected tip, trusted delivery revision and
   evidence. Revalidate those identities plus cleanliness, preservation,
   delivery, consumers, bindings and inactivity at preview and immediately
   before each mutation; stop on any changed, missing or unverifiable state.
   Use the repository's retirement helper where required. Restrict every
   operation to the eligible target and keep receipts and recovery material;
   on Windows verify absolute containment before any recursive operation and
   use one shell end to end. Include the diagnosed cause, evidence, exact
   preview/apply instructions and post-action readback in the handoff.
   Elevate only when the diagnosis proves privilege is required for that
   specific action. Elevation never supplies ownership, delivery, binding or
   activity authority; a lock alone is no reason to elevate. Preparation is
   not execution and grants no new apply authority. Completion: a bounded
   preview-first artifact is reviewable, or a named safety/diagnosis gap has
   release instructions instead. Do not generate a generic cleanup utility.

## Assessment and handoff

9. Account for every scoped root, worktree and local branch. Report base ref
   and commit, observed identity/state, disposition, evidence, cleanup results
   and retained limits. For unmerged work include unique commits when knowable,
   delivery evidence and a merge-or-retain recommendation; record only true
   owner decisions, and continue other authorized work without waiting. Give
   unrelated or historical refs read-only recommendations. Run each owning
   repository's required assessment when available and record its actual
   result and named failures. This skill does not merge, rebase, cherry-pick,
   push, open/update PRs or delete remote branches. Completion: each item has a
   disposition, each incomplete inspection is named and each actionable hold
   has release/recovery instructions or its bounded script artifact.

A complete assessment may contain retained targets and named holds. Report
assessment coverage, accepted delivery and cleanup completion separately;
never turn a recorded hold into a repository-contract pass or claim an unmet
issue complete. Preserve stricter repository completion and handoff-only gates.
