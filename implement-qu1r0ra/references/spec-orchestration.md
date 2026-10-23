# Whole-spec orchestration preferences

Follow upstream `implement-spec` for its task graph, exploration, background
implementers, merger subagents, integration branch, draft PR, and final
`code-review`. These are the personal exceptions and dispatch extensions.

## Before dispatch

Read the target repository's implementation contract, tracker rules, and this
wrapper's matching harness adapter. Read the AIOS
[model-routing policy](../../../../docs/agents/model-routing.md) for every child
role (merge and repair work use the Implementer row); adapters supply capability
mechanics, not another model preference. Follow the
[Provider selection](../../../../docs/agents/model-routing.md#provider-selection)
for provider defaults, exhaustion, and review routing. Follow
[Dispatch](../../../../docs/agents/model-routing.md#dispatch) for the global
child cap and blocked-lane handling.

An explicit direct-ticket request selects upstream `implement` through this
wrapper's [workflow selector](../SKILL.md#select-the-workflow) and retains its
[independent review policy](review-policy.md).

Pass context pointers plus the ticket's approved scope, acceptance criteria,
public test seams, current integration base, worker worktree/branch, and
authorization boundary. Follow `tdd` at approved seams; obtain a missing seam
decision before test-first implementation. Do not re-open settled test seams
merely because the worker did not attend planning.

Take the frontier in dependency-map order. Use actual isolated workers and one
integration writer at a time. Preserve
unrelated state when checking worker bases: create or rebase a clean scoped
checkout instead of treating upstream's reset instruction as overwrite
permission. Workers implement, test, commit, and reconcile with the current
integration tip; the run owner verifies their evidence and owns delivery.

Put these in every worker brief: commit early and often; run
`just format-changed` before each commit; park in-progress work as a temporary
WIP commit, never a bare `git stash`.

## Progress and review

Within the active task graph, treat a prerequisite as satisfied only after its
exact worker tip is integrated and scoped acceptance checks pass. Record that
revision and evidence before dispatching dependents. Keep live issues open
until accepted delivery; an external unresolved blocker stays blocking. A
failed integration or invalidated check blocks the affected frontier again.
This replaces using early tracker closure to drive upstream's frontier.

Use upstream's integrated Standards and Spec PR review with
`review-policy.md`; its single re-review covers the entire delivery unit. Repair
implementers return committed changes for integration before required re-review.
Parent verification and review obligations apply to the final integrated
candidate, rather than multiplying a full delivery workflow per worker.

Deliver through the target repository's implementation contract (for AIOS,
`docs/agents/implementation-contract.md` and its dispatch and lifecycle
references). Local-only work follows its handoff contract.
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
  user-review gate unless an approved autopilot run plan includes this ticket.
  Store the plan as `.scratch/autopilot/<date>/revision-plan.md`; CJ approves it
  in the run kickoff before dispatch. Keep each run's `brief.md` and `report.md`
  under `.scratch/autopilot/<date>-runN/`; the brief is operational context,
  not the approval artifact. The approved plan replaces the user-review gate
  only for tickets it names. Worker retirement preserves evidence and recovery
  branches; final cleanup still requires accepted delivery.
- If a held lane or dispatchable frontier remains when the orchestrator's turn
  ends, the monitor named in `.scratch/autopilot/<date>-runN/monitor-brief.md`
  follows the [autopilot monitor wake rules](../../autopilot/references/monitor.md#observation-and-wake-decisions)
  for hourly observations, due retries and changed release evidence. An unchanged
  owner gate does not warrant repeated resumes; T3 auto-resume is not a recovery
  guarantee.

Completion: the full task graph is integrated and verified, the integrated
review and selected delivery gate are satisfied or named, and worker, delivery,
and tracker state each have accurate receipts.
