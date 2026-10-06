# Whole-spec orchestration preferences

Follow upstream `implement-spec` for its task graph, exploration, background
implementers, merger workers, integration branch, draft PR, and final
`code-review`. These are the personal exceptions and dispatch extensions.

## Before dispatch

Read the target repository's implementation contract, tracker rules, and this
wrapper's matching harness adapter. Read AIOS `docs/agents/model-routing.md`
for every child role; adapters supply capability mechanics, not another model
preference. Resolve an unavailable implementation or merger lane before work
depending on it. Report it as blocked rather than silently substituting direct
execution. The user can explicitly select the direct route.

Pass context pointers plus the ticket's approved scope, acceptance criteria,
public test seams, current integration base, worker worktree/branch, and
authorization boundary. Follow `tdd` at approved seams; obtain a missing seam
decision before test-first implementation. Do not re-open settled test seams
merely because the worker did not attend planning.

Use actual isolated workers and one integration writer at a time. Preserve
unrelated state when checking worker bases: create or rebase a clean scoped
checkout instead of treating upstream's reset instruction as overwrite
permission. Workers implement, test, commit, and reconcile with the current
integration tip; the run owner verifies their evidence and owns delivery.

## Progress and review

Within the active task graph, treat a prerequisite as satisfied only after its
exact worker tip is integrated and scoped acceptance checks pass. Record that
revision and evidence before dispatching dependents. Keep live issues open
until accepted delivery; an external unresolved blocker stays blocking. A
failed integration or invalidated check blocks the affected frontier again.
This replaces using early tracker closure to drive upstream's frontier.

Use upstream's integrated Standards and Spec PR review with
`review-policy.md`; its round budget covers the entire delivery unit. Repair
workers return committed changes for integration before required re-review.
Parent verification and review obligations apply to the final integrated
candidate, rather than multiplying a full delivery workflow per worker.

For remote-backed work, stop at the verified ready-for-review PR unless
autonomous landing is explicitly authorized. Keep final delivery state and
issue closure behind acceptance. Local-only work follows its handoff contract.
This narrows upstream's resolve-ticket completion to the owning tracker’s
accepted-delivery rule.

## AIOS-specific branches

- Save shared exploration notes under the supervising checkout's ignored
  `.scratch/<effort>/` and pass absolute context pointers. This replaces
  upstream's outside-repository research directory. Use a writable exploration
  worker or have the run owner persist its returned notes.
- Use the target checkout's implementation contract for semantic branches,
  managed worktrees, preflight, serialized integration, and PR evidence.
- Retire integrated workers through the worker-retirement branch in
  `docs/operations/worktree-retirement.md`. Keep the integration worktree at the
  user-review gate. Worker retirement preserves evidence and recovery
  branches; final cleanup still requires accepted delivery.

Completion: the full task graph is integrated and verified, the integrated
review and selected delivery gate are satisfied or named, and worker, delivery,
and tracker state each have accurate receipts.
