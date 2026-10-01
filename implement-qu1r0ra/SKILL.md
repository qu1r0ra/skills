---
name: implement-qu1r0ra
description: "Implement a spec or ticket with the upstream workflow, bounded leaf-subagent review, and autonomous verified closeout."
disable-model-invocation: true
---

# Implement qu1r0ra

Follow [`implement`](../implement/SKILL.md) for implementation, testing, and
review. This wrapper changes execution ownership, review ordering, and
closeout. The invoking agent implements directly; `implement-spec` is a
separate, explicitly selected orchestration workflow.

## Repository route

Identify the target Git root and follow its implementation and tracker
contracts when present. For AIOS tickets, read the
[implementation contract](../../../docs/agents/implementation-contract.md);
it owns isolation and delivery mode. Outside AIOS, use repository-defined
rules, falling back to the upstream workflow where no contract exists. Apply
this wrapper's review and closeout preferences within that delivery mode.

## Review

Commit the complete scoped change before upstream's code-review step, so its
fixed-point-to-HEAD diff contains the implementation. Use the recorded branch
base as the fixed point. Commit repairs before re-review; review the resulting
branch diff rather than an empty or partial diff.

Read [review-policy.md](references/review-policy.md) for the leaf-worker
adapters, model routing, round budget, and required receipt. Completion:
verification evidence and the final commit are recorded, and the review
receipt accounts for both axes, repairs, rounds, and remaining gates.

## Closeout

Continue through the [closeout procedure](references/implementation-closeout.md)
for the selected delivery mode unless the user requested handoff-only
retention. Repository publication and human-acceptance gates still apply.
Completion: the change is landed or has a named gate, temporary Git state is
accounted for, and any affected ticket has a verified, accurate receipt.

Report implementation commits, review-pair count, checks, landing commit,
publication result, retired worktrees and branches, ticket state, and remaining
gates. Ticket closure follows its acceptance evidence.
