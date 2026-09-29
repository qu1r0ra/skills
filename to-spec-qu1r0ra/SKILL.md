---
name: to-spec-qu1r0ra
description: Turn an AIOS design conversation into a spec and a validated central issue draft when the user asks for a spec or a completed design flow hands off to one.
---

# To Spec qu1r0ra

Use this wrapper for an AIOS-owned specification. This wrapper owns the AIOS
workflow. Read the protected [`to-spec`](../to-spec/SKILL.md) as a reference for
repository exploration, test seams, synthesis, and the spec template. Follow
the central issue contract for publication.

Before creating a central issue, read
[`docs/agents/issue-tracker.md`](../../../docs/agents/issue-tracker.md) and the
local [`aios-github-tickets`](../../../.agents/skills/aios-github-tickets/SKILL.md)
skill. Route an implementation issue to its repository-owned tracker when that
repository has one; use the central tracker for AIOS-owned or coordinating work.

1. Draft the spec from the conversation and relevant domain material. Confirm
   the test seams as the upstream reference requires. Add the central issue
   contract's routing labels, target, scope, blockers, and verification
   expectations. A publishable shaped spec uses `ready-for-agent`. Completion:
   the draft covers every upstream spec section and AIOS issue requirement.
2. Follow the draft validation and packet review steps in **Shaped issue
   publication** in the central issue tracker contract. Completion: the exact
   publication packet passes validation and has been shown to the user.
3. Follow that contract's approval and publication branch. Completion: the user
   has the identified unpublished draft or the verified live issue, with its
   identity and any remaining gate stated.

Spec approval covers this publication packet. Implementation and a later ticket
breakdown require their own instructions.
