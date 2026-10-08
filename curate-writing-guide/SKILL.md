---
name: curate-writing-guide
description: Research a writing use case into a graded bank entry plus a self-contained project guide, or revise both. Invoke by name.
disable-model-invocation: true
---

# Curate writing guide

Turn one writing use case into a researched, source-graded entry in the `writing` wiki and a self-contained guide in the project. Read `qu1r0raOS-wikis/writing/AGENTS.md` and `governance/knowledge-profiles/writing-v1.md` first; the profile owns the source-record fields and the grades.

A guide is stale when any of its sources is past `recheck_by`. To keep a guide current, take [Revise](#revise) instead of the steps below.

## Steps

### 1. Frame

Ask the author only what they alone know: the use case, the audience, the purpose, the constraints, and the quality bar (the author's own measure of good writing here, and which readers it serves). Recommend a value for anything they leave flexible, including a venue. A use case with no venue is valid; leave the venue key empty.

Done when the use-case summary names use case, audience, purpose, constraints, quality bar, and venue (or "none"), and the author has confirmed it.

### 2. Research

Run read-only leaf subagents in two rounds. Read `docs/agents/model-routing.md` and use the worker pair pinned for this harness; a lane without an available pair is blocked. Briefs, the lane size limit, and the shared rules are in [lanes.md](references/lanes.md). Give each lane its brief and the use-case summary only: no draft text, no private exemplars.

1. **Sweep:** dispatch the four broad lanes in one turn: Requirements, Conventions, Craft, Exemplars. Split a lane by topic first when its brief exceeds the size limit.
2. **Gap-fill:** when the sweep returns, group its gaps by topic and dispatch one narrow lane per group in one turn. Run this round once.

Done when every gap is answered or sits under Open questions, and each lane has returned findings that meet its evidence standard, or has listed its searches and named results (a lane that finds nothing) or its block. Any blocked lane marks coverage `partial`, reported to the author.

### 3. Reconcile

Merge the findings by precedence: `requirement` over `authoritative guideline` over `empirical` over `convention` over `preference`. Where two rules conflict, the higher grade wins and the lower rule is dropped or scoped. Grade every rule using [entry.md](references/entry.md#grades). Grade a rule `authoritative guideline` only on a `verified` finding; an `unverified` one goes to gap-fill, and after gap-fill grades as `convention`.

Done when every rule carries a grade and a source, and every `authoritative guideline` rule carries a quoted passage from a `verified` finding.

### 4. Bank search

Search the bank only now, after reconciliation: read `guides/index.md`, `practices/index.md`, and the guides it names that share a genre, field, audience, or venue.

- Transfer a past rule only when this research confirms it from a different source domain.
- Lift a rule confirmed by a second guide into `practices/<topic>.md`.
- Link the nearest neighbours.

Done when each past rule is transferred, lifted, or left out, and the neighbours are named.

### 5. Grill

Run `grill-qu1r0ra` once. Scope it to the rules that are contested (sources disagree) or unsourced (only `convention` or `preference` backing).

Done when the author has settled every contested or unsourced rule, and the answers are recorded in the grade or the deviation rule.

### 6. Produce

Write, using [entry.md](references/entry.md) and [project-guide.md](references/project-guide.md):

1. The bank entry `guides/<slug>.md` with its source records and recheck dates.
2. Captured exemplars within the limits in entry.md.
3. The project guide at its default path, with the Existing instructions table.
4. The pointer line in the project's agent instructions.
5. The index rows, `usage/projects.md`, `catalog.json`, and a `log.md` line.

Validate with `uv run python -m qu1r0raOS.validation workspace <root>`; the root is the AIOS checkout. Then run `uv run --no-project python scripts/check_guide.py quotes <entry>` and `parity <entry> <guide>` from this skill's directory.

Done when validation passes, every quoted passage reports `found`, parity prints no `absent`, `grade differs`, or `no such rule` line, the project guide holds every item the template lists, and the pointer line names the guide and not this skill. Fix a `missing` passage or regrade its rule; send an `unchecked` one through the unreachable-page route under Failures.

### 7. Review

Dispatch one read-only Standards reviewer (the role row in `docs/agents/model-routing.md`) with the brief in [review.md](references/review.md). Fix every Blocking finding, then dispatch one re-review limited to the changed files.

Done when the reviewer reports no Blocking finding. A Blocking finding that survives the re-review, and every open Non-blocking one, goes to the author.

## Revise

1. Recheck only sources whose `recheck_by` has passed, any the author names, and any the author supplies for a rule. Run `check_guide.py quotes` on the entry and read the lines for those sources; each `unchecked` line names the likely page to paste. When no source is stale and the author asks only for a quote check, stop after this step and record the result. Update `checked_on`, `recheck_by`, and `status` for each.
2. Re-reconcile only the rules those sources support (step 3), then re-run step 4 for the changed rules.
3. Grill (step 5) on the changes only.
4. Update the entry, the project guide, the revision line, and the log (step 6), then review the changed files (step 7).

Done when every stale source is rechecked or marked `stale`, the entry and the project guide name the same revision, and the project guide's Existing instructions table is gone once the author has settled every row.

## Failures

- **Dead link:** retry once, then search for the document's new location. Keep the rule with its source marked `stale` when none turns up, and report it.
- **Unreachable page** (bot wall, 403, 429, paywall): fetch it through the Wayback route in [lanes.md](references/lanes.md#shared-rules). If that fails, confirm each remaining URL is live with `curl -I`, then ask the author once to paste the page text for all of them. Run pasted text through `check_guide.py quotes --page <url>=<file>` and tag it `verified`.
- **Blocked lane:** report it, mark coverage `partial` in the entry, and list the lane's unanswered questions under Open questions.
- **Failed lane** (API or rate-limit error): redispatch it once after the limit resets, or run its questions inline, and name the choice under Coverage. A lane that fails twice counts as blocked.
- **Validation failure on a fresh entry:** fix the entry and rerun; keep the previous bank and project guide untouched until validation passes. Report the validator's message when two reruns fail.
