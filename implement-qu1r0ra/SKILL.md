---
name: implement-qu1r0ra
description: "Implement a whole spec through upstream orchestration, or selected tickets directly, with integrated review and verified delivery."
disable-model-invocation: true
---

# Implement qu1r0ra

This is the personal implementation entry point. Read the selected upstream
workflow as the implementation procedure; the user has invoked this wrapper,
so do not require a second user-only skill invocation.

## Select the workflow

- A whole spec defaults to [`implement-spec`](../implement-spec/SKILL.md).
  Read [spec orchestration](references/spec-orchestration.md) before dispatch.
  If approved tickets are absent, prepare them in this invocation using
  [`to-tickets-qu1r0ra`](../to-tickets-qu1r0ra/SKILL.md), obtain its breakdown
  approval, then resume. Spec approval alone does not approve the breakdown.
- Selected tickets, a selected batch, or an explicit direct request use
  [`implement`](../implement/SKILL.md). Keep direct execution and its testing
  workflow. The user may request this route even for an entire spec.

Identify the target Git root and follow its implementation and tracker
contracts. For AIOS, read the target checkout's
`docs/agents/implementation-contract.md`; it owns isolation, ownership,
integration progress, verification, and delivery. Outside AIOS, use the owning
repository's rules and upstream mechanics where no contract exists. Resolve
ignored shared skill sources through the supervising primary checkout.

## Integrated review

Commit the complete delivery unit before upstream's `code-review` step. Review
the fixed recorded delivery base to committed HEAD, so the diff contains the
implementation. Commit repairs before re-review. Whole-spec mode reviews the
integrated branch once, followed only by necessary repair review; worker
completion does not add a separate per-ticket PR review loop.

Read [review-policy.md](references/review-policy.md) for leaf-worker adapters,
role routing, the global round budget, and the review receipt. Completion:
both axes account for the committed delivery unit, repairs, rounds, and gates.

## Delivery

Remote-backed whole-spec runs default to a verified PR ready for user review.
Retain the delivery branch/worktree and keep issues open until acceptance.
Explicitly authorized autonomous landing, direct runs, and accepted local-only
delivery use [implementation closeout](references/implementation-closeout.md).
Preserve a requested handoff-only stop and the repository's human gates.

For an AIOS ticket under a `[Spec]` issue, apply the target repository's
parent-spec closeout rule after accepted child delivery; a worker merge is not
child acceptance.

Report the selected route, candidate commits, per-ticket acceptance evidence,
review rounds, checks, PR or local handoff, retained/retired Git state, verified
ticket states, and remaining gates. Completion distinguishes implemented and
ready-for-review from accepted, landed, and closed.
