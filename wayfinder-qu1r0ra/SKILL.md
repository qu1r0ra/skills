---
name: wayfinder-qu1r0ra
description: Plan a multi-session decision effort with Wayfinder, using the central GitHub issue contract for AIOS maps and the owning tracker elsewhere.
disable-model-invocation: true
---

# Wayfinder qu1r0ra

Follow [`wayfinder`](../wayfinder/SKILL.md) for the destination, map, ticket
types, frontier, chart/work modes, claims, and resolution sequence. This
wrapper changes tracker representation and publication for AIOS work.

Size decision tickets by a coherent decision or investigation, replacing
upstream's token-budget sizing. Agents can compact and continue. Keep
upstream's limit of one non-research resolution per session.

## Owning repository

Use the work's owning tracker and its Wayfinding operations when defined.
Outside AIOS, keep the upstream workflow and its configured-tracker or local
fallback. Apply the repository's publication gates.

## AIOS branch

Read **Wayfinding operations** in the
[central issue contract](../../../docs/agents/issue-tracker.md) and the local
[`aios-github-tickets`](../../../.agents/skills/aios-github-tickets/SKILL.md).
That contract owns headings, labels, sub-issues, native blocker links, and
fallbacks; use it without duplicating the representation here.

Follow **Shaped issue publication** for new maps and children. Verify every
authorized tracker write through its live validation route. Keep upstream's
claim-before-work and resolution sequence, including the decision comment and
title-linked map pointer.

For central AIOS maps and decision children, publish settled, validated packets
under the standing authorization in `AGENTS.md`; do not request a second
approval to publish. Preserve decisions the user still needs to settle.

When the map clears and the user asks for a buildable spec, hand its linked
decisions to [`to-spec-qu1r0ra`](../to-spec-qu1r0ra/SKILL.md).

Completion: the invoked upstream mode is complete or has a named design gate;
every authorized tracker change is verified. Keep invalid or failed-to-publish
drafts identified as non-live; they do not count as live charting or resolution.
