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
publication**: validate the exact draft, show the complete packet, obtain
approval, and verify any authorized publication. A draft remains a valid
outcome when publication is awaiting approval.

Completion: the user has the identified unpublished draft or verified live
spec, covering every required section and test-seam decision, with any
remaining gate stated. Spec approval covers only that publication packet;
implementation and ticket breakdown require their own instructions.
