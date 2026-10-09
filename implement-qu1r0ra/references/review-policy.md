# Implementation review policy

Read this for the selected upstream code-review step in `implement-qu1r0ra`:
the complete integrated branch for whole-spec mode, or the selected ticket or
batch for direct mode. One delivery unit shares one global round budget.

Before review, read AIOS `docs/agents/model-routing.md` from the active AIOS
checkout, or its supervising primary checkout when working elsewhere. Follow
its preferences, matching harness adapter, and dispatch evidence policy.

### Review policy for the upstream `/code-review` step

Request separate Standards and Spec reports through the harness's normal
subagent mechanism. Give reviewers the comparison and sources for their axis;
the parent owns candidate changes and delivery. An unavailable worker mechanism
leaves that review lane unavailable, with the reason recorded.

Count complete Standards+Spec reviewer pairs as review rounds for the delivery unit.
Before dispatch, record the fixed base, committed candidate, spec source,
standards sources, pair configuration, and round number in one runtime review
checkpoint. Give each reviewer that comparison and the unresolved findings
from its axis. A report remains evidence for that candidate; an amendment is
a new candidate, not a reason to reset the round counter.

For repair review, record the previous candidate and changed paths. Review
the repair and integration effects, carrying forward unchanged findings.
Reuse an unchanged scope's report only when its code, requirements, standards,
and integration assumptions are identical. Review new requirements and
changed integration explicitly. Stop dispatching when both axes have completed
the required review and no finding requires another round. Route mechanically
decidable rules to deterministic checks; reserve standards for judgement.

The round budget is global, including re-review after a repair:

- Rounds 1 through 3 are allowed review rounds. Reuse the last pair for
  back-and-forth repair/re-review when continuity is useful, and count each
  completed re-review as the next round rather than silently resetting the
  budget.
- After a round reports a P1, repair the finding and re-review the changed
  scope before declaring completion. A round is complete only when both axes
  return their bounded report.
- Round 4 is one backup round after the three-round budget, authorized only
  when Round 3 still has an unresolved P1, or when a critical review lane was
  unavailable or materially conflicted during the allowed rounds. Record the
  trigger and the repair/re-review history before dispatching Round 4.
- If a P1 remains after Round 4, stop the review loop and report the named
  unresolved risk for human or owner intervention. Do not dispatch Round 5 or
  silently create replacement pairs.

Completion: the scoped implementation is committed on its dedicated branch,
verification evidence is available, and the receipt states the total
review-round/pair count, reviewer dispatch evidence, each repair and
re-review trigger, final P1 disposition, and any Round 4 trigger.
