---
name: retro-qu1r0ra
description: Run comprehensive AIOS coding retrospectives and cadence catch-ups; use upstream retro for explicitly bounded session reviews.
---

# Coding-session retro

Use this wrapper for an AIOS coding retrospective or an AIOS retro cadence.
Inherit upstream [`retro`](../retro/SKILL.md)'s categories, primary-evidence
analysis, severity ordering, and deterministic-check preferences. In other
repositories, follow upstream directly. Upstream remains available for an
explicitly bounded session review in AIOS.

For comprehensive AIOS coverage, replace upstream's current-session default
with all-project, all-known-local-harness coverage over the workflow's frozen
window. Completion requires reviewed evidence, settled candidate dispositions,
and verified spec-and-approved-ticket handoffs; it does not require implementing
those improvements. Keep coding retros separate from Personal Reflection.

Read `governance/privacy-policy.yaml` first, then follow
`capabilities/workflows/retro-qu1r0ra.yaml` and its operational procedure in
`docs/operations/coding-retro.md`. They own preparation, exposure eligibility,
ordered trace review, recovery, decisions, handoffs, and completion. Follow
`docs/agents/domain.md` for domain and owning-repository routing.
If that workflow or runbook is absent from the active AIOS checkout, report the
missing companion delivery and keep comprehensive coverage pending.

For a cadence invocation, also follow `cadence/retro.md` and
`docs/operations/todoist-cadence.md`. Those sources own the exact mapped
occurrence and its verification and completion conditions.
