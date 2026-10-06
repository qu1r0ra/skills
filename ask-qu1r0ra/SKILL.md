---
name: ask-qu1r0ra
description: Choose a local idea-management flow or route engineering work to Ask Matt.
disable-model-invocation: true
---

# Ask qu1r0ra

Recommend the local skill that matches the user's request:

- Unshaped ideas to save for later: use `/capture-ideas`.
- An existing idea portfolio to review or triage: use `/review-ideas`.
- Improvement candidates from recent local work across harnesses: use `/brainstorm-ideas`.
- Engineering work that needs a Matt Pocock skill or flow: read
  [Ask Matt](../ask-matt/SKILL.md) for the route, then apply the wrapper
  substitutions below.
- A specification routed to `/to-spec`: use `/to-spec-qu1r0ra`; it applies
  the owning repository's contract and the central contract for AIOS work.
- An approved design or specification ready for tickets in any repository:
  use `/to-tickets-qu1r0ra` and follow that repository's tracker contract.
- A decision map routed to `/wayfinder`: use `/wayfinder-qu1r0ra`.
- A codebase survey routed to `/improve-codebase-architecture`: recommend
  `/improve-codebase-qu1r0ra`.
- Library documentation lookup: use `/find-docs-qu1r0ra`.
- A design interview routed to `/grill-me` or `/grill-with-docs`: recommend
  `/grill-qu1r0ra`. Keep `/grill-with-docs` when the user explicitly wants
  glossary maintenance or the documented interview workflow.
- Implementation routed to `/implement` or `/implement-spec`: recommend
  `/implement-qu1r0ra`, the single personal entry point. Whole specs default
  to upstream orchestration; selected tickets, batches, and explicit direct
  requests use upstream direct execution. The user may invoke either upstream
  skill directly to choose its behavior without personal overrides.

Keep idea capture, review, and brainstorming separate from engineering workflow
selection. This router names the user's next skill; let the user invoke it.
Completion: the user has a recommended skill or flow and the reason it fits;
the selected workflow awaits their invocation.
