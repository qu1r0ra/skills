---
name: to-spec-qu1r0ra
description: Turn an AIOS design conversation into a spec and a validated central issue draft when the user asks for a spec or a completed design flow hands off to one.
---

# To Spec qu1r0ra

Use this wrapper for an AIOS-owned specification. Read and follow the protected
[`to-spec`](../to-spec/SKILL.md) for synthesis, repository exploration, test
seams, and spec content. For AIOS, complete its publication step through the
draft and approval sequence below.

Before creating a central issue, read
[`docs/agents/issue-tracker.md`](../../../docs/agents/issue-tracker.md) and the
local [`aios-github-tickets`](../../../.agents/skills/aios-github-tickets/SKILL.md)
skill. Route an implementation issue to its repository-owned tracker when that
repository has one; use the central tracker for AIOS-owned or coordinating work.

1. Draft the spec from the conversation and relevant domain material. Confirm
   the test seams as upstream requires. Add the central issue contract's
   routing labels, target, scope, blockers, and verification expectations to
   the draft. A publishable shaped spec uses `ready-for-agent`.
2. Validate the complete issue draft with
   `just tickets --validate-draft <path>`. Resolve reported shape or routing
   errors before presenting it. Show the user the issue title, body, labels,
   blocker relationships, and destination for review.
3. Obtain explicit approval for that publication packet. Then use the central
   issue contract's `just tickets --publish-draft <path> --confirm` route.
   Verify the live issue and its labels, body, blockers, and target with `gh`, and run
   `just tickets --validate`. If approval is withheld, leave the validated
   draft unpublished and report its path.

Completion: the user has a validated draft or a verified live issue, with any
publication gate and issue identity stated. Spec approval does not authorize
implementation or a later ticket breakdown.
