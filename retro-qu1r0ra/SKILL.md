---
name: retro-qu1r0ra
description: Run a comprehensive coding-session retrospective with AIOS evidence and handoff safeguards.
---

# Coding-session retro

Use this wrapper when the user asks for a coding retrospective in the AIOS
repository or invokes an AIOS retro cadence. It inherits upstream
[`retro`](../retro/SKILL.md)'s candidate categories and selection rules. In
other repositories, follow upstream `retro` directly.

In AIOS, read `governance/privacy-policy.yaml` first, then read
`capabilities/workflows/retro-qu1r0ra.yaml` and follow it completely. For
repository and domain routing, follow `docs/agents/domain.md` and the selected
domain's `CONTEXT-MAP.md`, glossary, and relevant ADR. For a cadence-triggered
run, read `docs/operations/todoist-cadence.md` and `cadence/retro.md`; the
reminders are manual, and skipped occurrences stay open for catch-up.

## Review flow

Start with `uv run qu1r0raOS retro prepare` from the AIOS root. It freezes the
window since the last completed coverage (or the initial 14-day window),
inventories the configured and known source lanes, and reports the exact
`retro-qu1r0ra` cadence preflight. Use the returned `run_id` for every later
command. Use `retro resume --run-id <run-id>` after interruption or whenever
source state may have changed; read `retro status --run-id <run-id>` before
continuing.

Review every source by its exact `source_id` and `source_revision`. Inspect
before each chunk, establish current authorization for that source and resolve
the semantic hard-exclusion assessment for the exact content. Do not infer
either from the cadence reminder or an earlier chunk. Only after both gates
allow exposure, inspect the next sequential page with `retro trace`, using the
authorized `--authorization-basis` and the assessed
`--semantic-hard-exclusion` values. If either is blocked or unresolved, stop
and do not retry with a weaker value. Acknowledge each returned chunk with
`retro acknowledge` only after reviewing that exact chunk. Continue through
all chunks, then call `retro review` with every acknowledged chunk ID for that
exact source revision. Changed in-window evidence or its bounded surrounding
context requires resume, fresh trace review, and new acknowledgements. A later
append outside the frozen window preserves reviewed coverage when that
evidence and context remain unchanged.

Keep unsupported stores, malformed or untimed evidence, scanner failures, and
analysis-obscuring redactions as visible gaps. Do not clear a gap from a
redaction marker or a claim alone. Use `retro resolve-gap` only with a bounded
local evidence citation and rationale; analysis-obscuring redactions also
require explicit same-revision local review before that source can count as
complete. A missing or unreadable source lane stays unavailable unless its
inactive or outside-window status has supporting local evidence.

Apply upstream `retro`'s candidate categories. For each candidate, record a
short sanitized summary, source evidence references, severity, and a current
repository state check with citations bound to its Git root and full commit
SHA. Refresh source references and current state after an affected evidence or
repository revision change, then settle the disposition again. Record each candidate's
accepted, deferred, dismissed, resolved, or superseded disposition with a
rationale. Present meaningful candidates in severity order; a full review may
produce no accepted changes.

For each accepted new improvement, run `$to-spec-qu1r0ra` and
`$to-tickets-qu1r0ra` through their approval gates, then publish the settled
spec and approved ticket breakdown with `$aios-github-tickets` under
`docs/agents/issue-tracker.md`. Do not implement the accepted finding during
the retrospective. For existing work, record an explicit semantic-equivalence
decision with current issue citations. Then verify the shaped spec and ticket
scope, execution-map entry, ticket-to-spec relationships, blocker edges, and
test seams against current read-only GitHub data. Use the CLI's live handoff
readback and fresh finalization verification; persisted booleans or text
similarity do not establish equivalence. The local CLI only verifies the
tracker and records a sanitized receipt, so complete publication and issue
readback before recording handoffs and finalizing.

When no candidate is accepted, record a no-op only after every source and gap
has complete, evidence-supported coverage. Finalize with
`uv run qu1r0raOS retro finalize --run-id <run-id>` only after all candidates
have dispositions and all accepted handoffs pass fresh verification. The CLI
writes a sanitized receipt before advancing the completed-window checkpoint.
Raw source contents remain in their source locations and are never copied into
durable state or the receipt.

While implementing or reviewing this workflow, do not touch Todoist. During an
actual cadence session, after coverage, dispositions, handoffs, and receipt
finalization are complete, follow `docs/operations/todoist-cadence.md`: verify
the exact mapped title-only task in the AIOS project's `Cadence` section, then
complete only that occurrence. Do not change its recurrence or due date; leave
skipped occurrences open for catch-up.
