---
name: to-tickets-qu1r0ra
description: Apply qu1r0ra's parallel-seam ticket sizing and dependency-map preferences to the upstream to-tickets workflow. Use for ticket breakdowns or approved handoffs to ticketing.
---

# To Tickets qu1r0ra

Follow the [upstream `to-tickets` skill](../to-tickets/SKILL.md) as the authoritative workflow and source of ticket templates. Keep its mechanics unless a preference below changes or extends them.

## Ticket boundaries

- Size tickets for `implement-spec` orchestration: one ticket per **seam** where a separate worker can own a disjoint area (module, layer, or feature) and deliver an independently verifiable outcome. Group the layers, tests, documentation, and integration work that serve the same outcome inside that ticket. Direct `implement` works the same tickets serially, so one default serves both routes.
- Split for a genuine blocking prerequisite, an independently releasable outcome, or a seam whose parallel benefit outweighs its coordination cost (worker cold start, worktree, merge, published issue). Fold a ticket too small to earn that cost, such as rename-only, docs-only, or test-only work, into its nearest neighbor. The ticket count follows from the seams.
- When the user asks for the direct route or a coarse breakdown, prefer the fewest cohesive tickets instead.
- This replaces upstream's single-context-window sizing rule: agents can compact and continue.

## Dependency map

Add a compact execution map to upstream's granularity and blocker review. Use one line per batch in dependency order, naming tickets by tracker IDs or local numbers. Mark a parallel candidate only when no blocker connects it to its batch peers and its owned area is disjoint from theirs. Name each candidate's owned area in the map only; ticket bodies stay path-free. Tickets that share an area get a blocker edge instead. For example:

```text
Batch 1: A [parser], B [renderer] (parallel candidates)
Batch 2: C [cli] (blocked by A)
```

After breakdown approval, put the lasting map in an editable parent or reference spec. This is a narrow exception to upstream's rule against modifying the parent: update only the approved map, preserving the parent's state and other content. If the document is frozen or unsuitable, use a repository-approved adjacent index. For AIOS, the approved map update and validated ticket issues follow the central issue-publication authorization; do not ask again to confirm publication. Once tickets exist, replace provisional names with their actual IDs and verify that the map agrees with every blocker edge.

## Repository formats and defaults

Follow repository-defined ticket formats, tracker destinations, and publishing rules when present. When no ticket-body format is defined, use the matching upstream local or hosted template, preserving its headings, field order, and acceptance criteria. Where tracker setup is absent, use the upstream setup gate rather than inventing a destination.

Completion: the approved tickets use the required format, and their blocker edges and lasting execution map agree. All other upstream mechanics remain in force.
