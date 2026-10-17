---
name: prune-qu1r0ra
description: Prune what costs more than it returns. Triggers - a slow CI job or `just check`; a slow or low-value test; a gate that blocks without benefit; one-off code past its removal criterion.
---

# Prune qu1r0ra

Remove anything whose cost exceeds its benefit. Measure first, cut by stated criteria, keep a safety net, record before and after numbers.

The standing rules live in [implementation-contract.md](../../../docs/agents/implementation-contract.md): right-sized test demand, the `Verification: lightweight | full` declaration, one-off code removal, and landing readiness. Apply them from there. Route structural findings (deepening, drift) to `improve-codebase-qu1r0ra`.

## Triggers and thresholds

Measure against the last five runs or the current local run. Tune the numbers here.

| Branch | Signal | Threshold |
| --- | --- | --- |
| CI | Full PR job | median over 5 min (goal 3 min) |
| CI | Lightweight PR job | over 30 s |
| CI | Local `just test` | over 90 s |
| Tests | Single test | over 10 s |
| Tests | Five slowest tests | over 25% of suite time |
| Gate | Required or preflight condition | failed at least twice in the last ten PRs without catching a defect, or duplicates a ruleset control |
| One-off code | Owner confirmed its run is complete | the contract's removal criterion |

## Authority

- User-invoked: open or use a central issue and follow the implementation contract (worktree, PR, verification). Apply cuts inside the scope the user named; ask before going beyond it.
- Agent-invoked: stop after step 2's ranked proposal and wait for the owner. Edit nothing.
- Confirm-first gate: changes to rulesets, branch protection, or required checks, and any cut that relaxes a required check, need the owner's explicit confirmation in either mode. List them in the proposal as gated and leave them unapplied.

## 1. Measure (read-only)

Run the command for the branch:

- Job run times: `gh run list --workflow checks.yml --limit 5 --json databaseId,createdAt,updatedAt,conclusion`
- Job step timings: `gh run view <id> --json jobs --jq '.jobs[].steps[] | [.name, .startedAt, .completedAt] | @tsv'`
- Slowest tests: `just test --durations=10`
- Gate failures: `gh pr list --state merged --limit 10 --json number`, then `gh pr checks <n>` per PR
- One-off code: the owner's confirmation in the issue or conversation

Completion: each signal has a measured value beside its threshold. If every value is under its threshold, report the numbers and end the skill here.

## 2. Classify

List each candidate (a step, test, gate, or file) with its measured cost, its benefit, and its risk. Rank by cost saved per unit of risk.

Test candidates meet one cut criterion: it pins wording or docs text; it guards removed or one-off code; it duplicates another test. A slow test that stays gets the repository's slow-test marker so the iteration command skips it while full CI and the main push run keep it.

Completion: every candidate carries cost, benefit, risk, and its cut criterion or "keep". The ranked proposal lists, per candidate: the candidate, measured cost, benefit and risk, the cut criterion, the proposed action, and whether it needs the confirm-first gate. An agent-invoked run ends here.

## 3. Cut

Apply the proposal's ungated cuts per the implementation contract.

Completion: each applied cut maps to a proposal row, and the PR body lists every cut with its reason.

## 4. Keep the safety net

Before reducing pre-merge verification, check that `.github/workflows/main-checks.yml` runs the full suite on every push to `main` and that red runs follow [main-ci-triage.md](../../../docs/operations/main-ci-triage.md). If either is absent, establishing it joins the proposal.

Completion: both controls are confirmed present, or their establishment is a proposal row.

## 5. Record

Re-run step 1's commands after the cuts. Put before and after numbers for every measured signal in the PR body.

Completion: the PR body carries a before and after value for each signal that triggered the run.
