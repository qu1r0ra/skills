# Autopilot orchestrator

Run the approved plan in the supplied `brief.md`. Resolve `docs/agents/` paths
against its AIOS checkout. Read its linked approval artifact before execution;
missing approval holds dispatch. CJ's approval is the go signal for every
named ticket and replaces whole-spec mode's user-review gate only for those
tickets. Scope additions or unsettled choices go to the owner-decision list.

## Contracts first

Read every surveyed repository's instructions, implementation contract and
tracker rules before dispatch: establish its gate, claims, worktree location,
PR evidence and review policy. For AIOS, start with
`docs/agents/implementation-contract.md`, its dispatch and lifecycle references,
and `docs/agents/issue-tracker.md`. Record the resolved contracts in the report.
Preserve unrelated state and apply the nearest Git root's rules to each edit.

## Authorization

Apply the approved run's explicit tier overrides and each repository's gates.
Unsettled authorization stops that item at a draft or recorded owner decision.

| Tier | What it covers |
| --- | --- |
| Merge | Code, docs and tests after full verification, GitGuardian and the repository's required review |
| Allowed tracker writes | Comments, follow-up issues, ticket publication under the AIOS authorization, closing delivered issues |
| Draft only | Owner content, including wiki pages, Career Ops data, notes and records; live activation of schedules or notifications |
| Never | Credentials, making a repository public, PII in issues or PRs, force-push |

Keep owner content and activation proposals as reviewable drafts at the
approved stopping point. Leave owner-only issues and parent specs for CJ.

## Shift report and resume

Create the brief's report, normally `.scratch/autopilot/<date>/report.md`,
before dispatch. Keep it living: update after each dispatch, result, merge,
skip, block or draft. Use these sections:

- Contracts and approval: run identity, approved-plan link and governing rules.
- Merged: completed items with PR links and accepted revisions/evidence.
- Drafts awaiting the owner: artifact paths and stopping points reached.
- Skipped and blocked: items, reasons, failure counts and held-lane retry state.
- Owner decisions: the unresolved decision for each affected item.
- In flight: live-children count; per item, task ID, provider/model, branch,
  worktree and claim.
- Review tally: per-provider totals and dispatch outcomes, maintained under
  `docs/agents/model-routing.md` **Provider selection**.
- Frontier: the remaining items, their dependencies and what can dispatch next.
- Handover guide: completed at Done below.

Answer mid-run messages from this report. After compaction, auto-resume or a
monitor wake, reread the brief and report and check every in-flight task's
status before dispatching it again. Harvest completed results, preserve active
work, and reconcile claims, revisions and counts before continuing.

## Dispatch loop

1. Refresh live blockers and claims; take the approved frontier in dependency
   order. Honor serial edges across specs and add an edge if newly discovered
   overlap would put two workers in the same owned area. Within a spec, use
   the integration and acceptance rules in
   [implement-qu1r0ra](../../implement-qu1r0ra/SKILL.md) and its
   [spec-orchestration reference](../../implement-qu1r0ra/references/spec-orchestration.md).
   An unresolved external blocker holds its dependents.
2. Run that implementation procedure yourself for spec-shaped work. You are
   the only dispatcher; every child receives a leaf assignment and an explicit
   instruction not to dispatch children. Use `docs/agents/model-routing.md`
   **Preferences** for roles, including the Doc writer route, **Provider
   selection** for provider, spill and review rules, and **Dispatch** for the
   cap and blocked-lane handling. Before every dispatch, reconcile and check
   the report's live-children count against that cap or the approved override.
   Keep the review tally there under the centralized policy; do not create a
   second routing policy in the run brief.
3. Follow the routing document's harness mechanics and the target repository's
   worker, integration and review procedure. Record task IDs immediately.
   Required review and targeted re-review results gate merging under those
   contracts; the approved plan does not waive them.
4. Verify outcomes through the owning repository's delivery contract, then
   update the report and frontier. Stop each B item at its approved gate.
   Count ordinary ticket failures; after two, skip the ticket, record the
   reason and release its claim under the tracker rules. Treat provider
   exhaustion through routing's hold path rather than as two ticket failures.
   Record an owner gate or blocked lane and continue other ready work; never
   wait on the owner.

Continue without a deadline until the frontier is empty or every remaining
item needs the owner. A two-failure skip is terminal for this run, with its
dependents recorded as blocked.

When routing holds lanes because both providers are exhausted, stay in the
turn and retry them with bounded backoff while other work remains. Persist the
next retry and result in the report: start at five minutes, double to a
30-minute ceiling, and bound each recovery pass to six hours before recomputing
the frontier. End the turn only when nothing
else is dispatchable. Put `held, needs wake: <items and reason>` at the top of
both the report and final message. Held work is not Done. Recovery belongs to
the separate monitor; the orchestrator creates no self-scheduled timer.

## Done and handover

Confirm every approved item is accepted and delivered, drafted at its stopping
point, skipped after two failures, or waiting on the owner, with no active
children or recoverable held lanes. Retire the `review/*` worktrees you created
through the owning repository's cleanup rules, preserving unresolved work and
reporting any cleanup gate. Close nothing that belongs to the owner.

Write the report's handover guide for an owner returning cold:

- **To verify:** each completed item with its PR or issue link, one line of
  evidence and one check the owner can run.
- **Needs you:** each human-gated item with its decision, recommendation,
  exact steps for each answer and what the orchestrator does afterward.

Each item takes at most four lines, ordered by what unblocks the most, with no
private data. The Markdown guide is the source of truth. Render the same guide
as `handover.html` beside the report: one self-contained page, no external
assets, light and dark themes, a card per item, collapsible steps, links and a
copy button on every command. Add no content absent from the Markdown. Check
with `html_preview` and publish with `html_render` before the final message.
If those tools are unavailable, skip the page and note that in the report.

Mark the report `Run status: done` only after the guide and all outcomes are
recorded. End with the report path and its top handover items; distinguish
delivered work from drafts, skips and owner gates.
