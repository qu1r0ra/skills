---
name: to-tickets-qu1r0ra
description: Apply qu1r0ra's coarser-ticket and dependency-map preferences to the upstream to-tickets workflow. Use for ticket breakdowns or approved handoffs to ticketing.
---

# To Tickets qu1r0ra

Follow the [upstream `to-tickets` skill](../to-tickets/SKILL.md) as the authoritative workflow and source of ticket templates. Keep its mechanics unless a preference below changes or extends them.

## Ticket boundaries

- Prefer the fewest useful, cohesive tickets. Group the layers, tests, documentation, and integration work that deliver the same independently verifiable outcome.
- Split for a genuine blocking prerequisite, an independently releasable outcome, or parallel work whose benefit outweighs its coordination cost. Parallel work is optional. This replaces upstream's single-context-window sizing rule: agents can compact and continue.

## Dependency map

Add a compact execution map to upstream's granularity and blocker review. Use one line per batch in dependency order, naming tickets by tracker IDs or local numbers. Mark parallel candidates where no blocker connects them and separate ownership is practical. For example:

```text
Batch 1: A, B (parallel candidates)
Batch 2: C (blocked by A)
```

After breakdown approval, put the lasting map in an editable parent or reference spec. This is a narrow exception to upstream's rule against modifying the parent: update only the approved map, preserving the parent's state and other content. If the document is frozen or unsuitable, use a repository-approved adjacent index. Follow the repository's publication gate for that update. Once tickets exist, replace provisional names with their actual IDs and verify that the map agrees with every blocker edge.

## Repository formats and defaults

Follow repository-defined ticket formats, tracker destinations, and publishing rules when present. When no ticket-body format is defined, use the matching upstream local or hosted template, preserving its headings, field order, and acceptance criteria. Where tracker setup is absent, use the upstream setup gate rather than inventing a destination.

Completion: the approved tickets use the required format, and their blocker edges and lasting execution map agree. All other upstream mechanics remain in force.
