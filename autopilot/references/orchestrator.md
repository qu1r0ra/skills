# Autopilot orchestrator

Run the approved plan in the supplied `brief.md`. Resolve `docs/agents/` paths
against its AIOS checkout. Read its linked approval artifact before execution;
missing approval holds dispatch. CJ's approval is the go signal for every
named ticket and replaces whole-spec mode's user-review gate only for those
tickets. Put scope additions, changed stopping points and unsettled material
choices on the owner-decision list; revisions require separate approval.

## Contracts first

Read every surveyed repository's instructions, implementation contract and
tracker rules before dispatch: establish gates, claims, worktree locations,
PR evidence and review policy. For AIOS, start with
`docs/agents/implementation-contract.md`, its dispatch and lifecycle references,
and `docs/agents/issue-tracker.md`. Record resolved contracts in the report.
Preserve unrelated state and apply the nearest Git root's rules to each edit.

## Authorization

Apply approved tier overrides and each repository's gates. Unsettled
authorization stops only the affected item at a draft or recorded owner decision.

| Tier | What it covers |
| --- | --- |
| Merge | Code, docs and tests after full verification, GitGuardian and the repository's required review |
| Allowed tracker writes | Comments, follow-up issues, ticket publication under the AIOS authorization, closing delivered issues |
| Draft only | Owner content, including wiki pages, Career Ops data, notes and records; live activation of schedules or notifications |
| Never | Credentials, making a repository public, PII in issues or PRs, force-push |

Keep owner content and activation proposals as reviewable drafts at the
approved stopping point. Leave owner-only issues and parent-spec decisions for
CJ; apply the owning maturity and closure contracts rather than inferring
execution authority from a spec label or absence of children.

## Shift report and resume

Create the brief's report, normally `.scratch/autopilot/<date>/report.md`,
before dispatch. Update it after each dispatch, result, integration, merge,
skip, hold or draft. Keep these sections:

- Contracts and approval: run identity, plan link, governing rules and current
  capability/evidence routes, including incomplete or changed evidence.
- Outcomes: accepted deliveries with PRs and exact revisions; partial progress
  with verified capabilities and unmet criteria; drafts and stopping points;
  skips with failure counts. Keep tracker state distinct from implementation.
- Owner decisions: each decision, recommendation, alternatives, required
  authority or capability and what each answer resumes.
- In flight: live-children count; per item, task ID, accepted provider/model
  and exposed controls, branch, worktree, claim and observed status.
- Review tally: per-provider totals and outcomes under
  `docs/agents/model-routing.md` **Provider selection**.
- Frontier: distinguish dispatchable work, active children, pending checks,
  provider retries and owner/contract/capability gates. For each hold record
  evidence, affected dependents, release condition, next retry time if
  recoverable, and the change or event that warrants a wake otherwise.
- Schedules: run-owned IDs, status, thread bindings, next wake and monitor ID.
- Closeout and handover: per-root assessment, retained state and the guide below.

Answer mid-run messages from this report. After compaction, resume or a monitor
wake, reread brief and report, reconcile every in-flight task with live state,
harvest results and update claims, revisions and counts before dispatching again.
Completion: each known task and frontier item has a current state and next action.

## Dispatch loop

1. Refresh live blockers, claims and the capabilities relevant to the next
   dispatch, including required tool schemas and controls. Recheck affected
   routes before proposing a plan amendment. An unavailable route is a named
   hold or approved draft boundary, not a promise of later delivery. Add serial
   edges for newly discovered ownership overlap. Within a spec, use
   [implement-qu1r0ra](../../implement-qu1r0ra/SKILL.md) and its
   [spec orchestration](../../implement-qu1r0ra/references/spec-orchestration.md).
   Completion: the next item has current approval, dependency, ownership and
   capability evidence through its permitted stopping point.
2. Handle coordination and routine reconciliation yourself. For spec-shaped
   work, run the orchestration procedure as sole dispatcher; all children are
   leaf workers explicitly instructed to dispatch no children. Use
   `docs/agents/model-routing.md` for roles, providers, controls, spill, review
   tally, harness mechanics and the child cap. Reconcile the live count before
   each dispatch and record returned task IDs immediately. Delegate hard
   diagnosis, contradictory rules, acceptance/capability disputes and repeated
   failures to the appropriate stronger existing role: Plan reviewer for plan
   gaps, Spec reviewer for acceptance disputes, Doc writer for guidance, or
   Implementer for diagnosis and repair. Use the routed controls rather than
   inventing a model policy; an unavailable required role holds that lane.
   Completion: every dispatch is accounted for under the central routing policy.
3. Follow the owning worker, integration, review and delivery contracts.
   Required review and targeted re-review gate merging; approval waives none
   of them. Reconcile pending checks separately from child and provider waits.
   Apply the partial-progress rule below before releasing a dependent.
   Completion: outcomes cite exact revisions and applicable evidence, with
   unmet criteria and remaining gates kept explicit.
4. Update outcomes, tracker state and all frontiers. Stop B items at their
   approved gates. Count ordinary ticket failures; after two, skip the ticket
   for this run, record the diagnosis and release its claim under tracker
   rules. Escalate repeated failures within that budget; provider exhaustion
   follows routing's recovery path instead of counting as ticket failures.
   Continue other approved ready work without waiting for an owner decision.
   Completion: each result has a recorded disposition and remaining work has
   an accurate next action.

### Partial progress

A dependent may proceed after partial prerequisite delivery only when the
exact required capability is integrated and verified under the repository's
contract, the remaining gaps do not affect that dependency, and approved scope,
safety and review rules still hold. Record the integrated revision, scoped
checks, remaining criteria and why those gaps do not affect the dependent.
Apply approved continuation conditions. When the plan lacks a partial boundary,
derive it from the exact acceptance and dependency evidence within approved
scope; consult a role-routed reviewer when that relationship is unclear. Changes
to required outcomes, safety rules or owner gates need approval. Keep native
edges authoritative: an external unresolved blocker
continues blocking, and an internal integration route must be permitted by the
owning contract. Partial progress neither completes unmet acceptance nor
closes its issue, and never permits bypassing a native edge by early closure.
An invalidated check or changed prerequisite blocks affected dependents again.

### Before stopping on a hold

Before ending a turn on any route or contract hold:

1. Reconcile every known child task and run-owned schedule against live state.
   Harvest completed results, preserve active work, and record task/schedule
   IDs, claims, status, thread binding and next wake. Apply only authorized
   schedule changes; the orchestrator creates no self-scheduled timer.
2. Check the live capability catalog and schemas against the approved plan and
   owning contracts. Distinguish unsupported routes or missing controls from
   provider exhaustion. Complete safe authorized diagnosis and evidence
   corrections now, using the escalation rule above where needed. Keep scope,
   routing, checkout-admission and lifecycle changes as separate owner proposals.
3. Refresh all frontiers and continue every independent dispatchable item to
   its permitted stopping point. Hold only affected lanes and dependents;
   preserve dependency, ownership and review gates.
4. When nothing remains dispatchable, update the report and any existing local
   agenda or authorized wake instructions with precise blockers and evidence.
   For owner gates, give the concrete decision, recommendation, alternatives,
   required contract/capability change and continuation after each answer.
   For recoverable holds, record the bounded retry policy and next due time.

Completion: every remaining item has an evidenced hold, active wait, terminal
outcome or owner gate; tasks and schedules are accounted for; no authorized
independent work remains. A hold is not accepted delivery or a done run.

When both providers are exhausted, retry under routing with bounded backoff
while other work remains: start at five minutes, double to a 30-minute ceiling,
and bound each recovery pass to six hours before recomputing the frontier.
Persist the next retry and result. End the turn only after the before-hold
checks; mark `held, needs wake: <recoverable items and due times>` at the top
of the report and final message when recovery is pending. Recovery belongs to
the separate monitor. An unchanged owner gate has no periodic resume request;
record the decision or evidence change needed to release it.

## Final assessment and handover

At the final run checkpoint, reconcile every approved item's outcome and all
active/recoverable waits. Automatically invoke [repo-closeout](../../repo-closeout/SKILL.md)
for every task-touched Git root, including nested roots. Apply its assessment
and cleanup limits: accepted delivery and retained cleanup are separate facts.
A finished assessment may list named holds; retain each owning repository's
stricter completion verdict and required receipts. Close no unmet or owner-only
issue. Completion: every item and Git root has an evidenced disposition;
cleanup holds identify release or recovery steps without delaying independent work.

Write a handover guide for an owner returning cold:

- **To verify:** each delivered item with PR or issue, one line of evidence and
  one check the owner can run.
- **Needs you:** each human gate with decision, recommendation, exact steps for
  each answer and what resumes afterward; include retained cleanup limits.

Each item takes at most four lines, ordered by what unblocks the most, with no
private data. Markdown is the source of truth. Render the same guide as
`handover.html` beside the report: self-contained, no external assets, light
and dark themes, a card per item, collapsible steps, links and a copy button on
every command. Check with `html_preview` and publish with `html_render` before
the final message; if unavailable, skip the page and record that limitation.
At this natural checkpoint apply `docs/operations/coding-retro.md#suggesting-a-session-retro`:
offer once when concrete reusable session evidence qualifies, and continue
without waiting; start a retro only if accepted.

Mark `Run status: done` only when every approved outcome is delivered, drafted
at its approved gate, or terminally skipped with dependents accounted for, and
no active child, pending check, recoverable lane or unresolved execution gate
remains. Otherwise record `held` with named release conditions. The assessment
and handover can be finished while the run remains held. Report the path,
top handover items and delivery/cleanup verdicts separately.
