# Implementation review policy

Read this for the selected upstream code-review step in `implement-qu1r0ra`:
the complete integrated branch for whole-spec mode, or the selected ticket or
batch for direct mode. One delivery unit shares one review budget.

Before review, read AIOS `docs/agents/model-routing.md` from the active AIOS
checkout, or its supervising primary checkout when working elsewhere. Follow
its preferences and the matching harness adapter; this skill names no model.

## When to review

Documentation-only, deletion-only, and maintenance changes may skip review.
Every other change gets the review below.

## Review passes

Request one Standards report and one Spec report through the harness's normal
subagent mechanism. Implementation workers do not review their own delivery
unit. Give each reviewer the fixed base-to-HEAD comparison, the
sources for its axis, and the parent's check results. The parent owns candidate
changes and delivery. An unavailable worker mechanism leaves that review lane
unavailable, with the reason recorded.

- Fix every P1 and P2 finding, commit the repair, and run at most one
  re-review of the changed scope on the axes that reported findings.
- Report any P1 or P2 finding that remains after the re-review as a named
  risk for the owner; dispatch no further review.
- Route mechanically decidable rules to deterministic checks; reserve
  standards for judgement.

Completion: the scoped implementation is committed on its dedicated branch,
verification evidence is available, and the receipt states each axis's
findings, the repairs, whether a re-review ran, and any remaining risk.
