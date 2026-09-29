---
name: improve-codebase-qu1r0ra
description: "Personal wrapper: audit a whole codebase across correctness, deepening, proof, and drift, report one ranked Markdown list in chat (no HTML), then grill which findings to address and in what batches."
disable-model-invocation: true
---

# Improve Codebase qu1r0ra

Use this personal wrapper for a whole-codebase audit. It keeps the upstream deepening method and replaces its scope, report, and grilling steps.

This wrapper owns the invocation. Read the protected
[`improve-codebase-architecture`](../improve-codebase-architecture/SKILL.md) as
the Deepening method reference. Use its step 1 method inside the Deepening
dimension below; this wrapper replaces its steps 2 and 3.

## 1. Explore by dimension

A named direction from the user narrows every dimension to that module, subsystem, or pain point. Otherwise cover the whole repo; recent history sets the reading order only.

Read the domain material `docs/agents/domain.md` routes to, and the ADRs at the nearest Git root. When the repo already has a plan from an earlier audit (a spec, open tickets, or draft ADRs), read [`EXISTING-PLAN.md`](EXISTING-PLAN.md) before dispatching; it extends steps 1 to 4 and adds step 5. Read `docs/agents/model-routing.md` for the worker pair; it is the only model preference source. Dispatch one read-only leaf subagent per dimension, in parallel. Each worker reports to the parent and stops, using one entry shape: title, dimension, files with `file:line`, evidence.

Each finding has one owning dimension:

| Dimension | Owns | Evidence |
| --- | --- | --- |
| Correctness | wrong now: bugs, silent failures, wrong error handling, unchecked assumptions; build, CI, and scripts count as code | a concrete failing input at `file:line` |
| Deepening | shape: upstream step 1, shallow modules, leaky seams, no locality; a hard-to-test interface counts as interface shape only; use `codebase-design` vocabulary | the deletion test on every suspect |
| Proof | unverified: behaviour with no check, or a check too weak to show that a change to it is safe | the check that exists, or the check that is missing |
| Drift | misdescribed: docs, ADRs, contracts, and comments that disagree with the code | two conflicting quotes; Drift reports the disagreement and hands the finding to Correctness when the code is the side that is wrong |

When a dimension's scope exceeds what one worker can read, shard it by top-level directory. Each shard owes the completion criterion for its directories, and the parent merges shard reports before reconciling.

Completion: every worker report accounts for every top-level module or directory in its scope, with findings or "reviewed, none".

## 2. Reconcile

Merge findings that cite the same defect into one entry with several dimension tags. Where a Deepening finding reshapes code that another finding touches, give the entry a **Sequencing** line: "fix before deepening" or "superseded if deepening lands".

Rate each entry:

- **Impact**: `High` is wrong results or a change that cannot be made safely; `Medium` is ongoing friction or unverified behaviour; `Low` is tidying.
- **Evidence**: `Verified` is re-checked by the parent; `Claimed` is the worker's evidence, not re-checked; `Speculative` is a judgement with no demonstrable evidence.

Re-check every `High` entry yourself by reading the cited lines, and by running the failing input when one command does it. Downgrade or drop a `High` that fails the re-check.

Completion: every `High` entry is `Verified` or downgraded, and every file cited by more than one finding is cross-referenced from each entry that cites it.

## 3. Report in chat

Write Markdown in the session. Open with one ranked table of every finding: rank, title, dimensions, impact, evidence, one-line problem. Order it by impact, then evidence. Follow with full entries for `High` and `Medium` findings in rank order:

- **Files**, **Problem**, **Solution** in plain English, **Benefits** in locality and leverage terms, **Sequencing** when present
- ADR conflicts marked as upstream step 2 marks them

`Low` findings appear as table rows only. End with **Top recommendation**. Propose no interfaces yet.

Save the full report, `Low` entries included, as `architecture-audit-<date>.md` where `git status` stays clean: `.scratch/<effort>/` at the nearest Git root when git ignores it, otherwise the OS temp directory. Tell the user the path. Offer once to publish it to the repo's tracker as an audit issue, and publish only on a yes. A published report opens with a **Decisions** header listing the user's scope calls, so tickets can cite them.

Ask: "Which of these would you like to address?"

Completion: the ranked report and full saved copy agree, the user has its path
and tracker offer, and the selected findings are identified or await a reply.

## 4. Grill

Call `grill-qu1r0ra` on the chosen findings. Open with which findings and in what batches, ordered by the Sequencing lines. Decide technical calls yourself and put scope, claims a fix could change, and irreversible steps to the user. Interface design for AIOS belongs to `to-spec-qu1r0ra`. When the user chooses one finding, grill its design directly.

When the grill finishes, offer `to-spec-qu1r0ra` for an AIOS spec and `/to-tickets` for an approved breakdown. Run neither without the user's request.

Completion: the chosen findings and batch order are settled, and the user has
the applicable next-step offer.
