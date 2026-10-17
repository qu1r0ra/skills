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
`docs/agents/implementation-contract.md`; it owns routes (standard and light),
isolation, test demand, verification, delivery, and the standing delivery
authorization. Outside AIOS, use the owning repository's rules and upstream
mechanics where no contract exists. Resolve ignored shared skill sources
through the supervising primary checkout.

TDD override: apply `tdd` only where the target contract's test-demand rule
calls for a test; verify other criteria with the cheapest sufficient check.

## Integrated review

Commit the complete delivery unit before upstream's `code-review` step, then
review the fixed recorded delivery base to committed HEAD. Commit repairs before
re-review. Read [review-policy.md](references/review-policy.md) for when to
review, the Standards and Spec passes, and the receipt. Whole-spec mode
reviews the integrated branch once; worker completion adds no per-ticket PR
review loop.

## Delivery

Deliver and land through the target contract, and use
[implementation closeout](references/implementation-closeout.md) for the
landing and cleanup branches it does not cover. For an AIOS ticket under a
`[Spec]` issue, a worker merge is not child acceptance; the contract's
lifecycle reference owns parent-spec closeout.

Report the selected route, candidate commits, per-ticket acceptance evidence,
review outcome, checks, PR or local handoff, retained/retired Git state, verified
ticket states, and remaining gates. Completion distinguishes implemented and
ready-for-review from accepted, landed, and closed.
