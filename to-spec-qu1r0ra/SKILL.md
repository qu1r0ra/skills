---
name: to-spec-qu1r0ra
description: Synthesize a design conversation into a repository-owned spec, using the central draft-validation and publication contract for AIOS work.
---

# To Spec qu1r0ra

Follow [`to-spec`](../to-spec/SKILL.md) for exploration, test-seam confirmation,
synthesis, and the spec template. This wrapper changes the publication route
when the repository defines one; it adds no design interview.

## Owning repository

Identify the nearest Git root and the work's owning tracker. Follow that
repository's spec format and publication contract when defined; otherwise use
upstream's template and tracker route. Keep its tracker-setup gate when no
destination is configured.

## AIOS branch

For AIOS-owned or coordinating work, read the
[central issue contract](../../../docs/agents/issue-tracker.md) and local
[`aios-github-tickets`](../../../.agents/skills/aios-github-tickets/SKILL.md).
Repository-owned implementation work stays on its repository's tracker.

Add the central contract's routing and verification fields to the upstream
spec. Replace upstream's immediate publication with **Shaped issue
publication**: once the design is settled under the upstream workflow, validate
the exact draft, publish it under the standing central AIOS issue-publication
authorization in `AGENTS.md`, and verify the live issue. Do not ask for separate
approval to publish a validated packet. Preserve any approval needed to settle
the design itself. If validation or publication fails, keep the draft and report
the specific failure.

Prefix every AIOS issue title created through this workflow with `[Spec]`,
including decision specs. Follow it with a plain-language description of the
spec's subject or outcome, for example `[Spec] Make specs easier to scan`.

Completion: the user has the verified live spec URL, covering every required
section and test-seam decision, or an identified draft with its validation or
publication failure. Publication authorization does not authorize
implementation; ticket breakdown follows its own instructions.
