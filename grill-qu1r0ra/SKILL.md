---
name: grill-qu1r0ra
description: "Personal wrapper: grill the user through a design decision, then offer an ADR when it clears the bar. No CONTEXT.md, no terminology work — use grill-with-docs for that."
disable-model-invocation: true
---

# grill-qu1r0ra

Use this personal wrapper for design conversations that deserve interrogation but not a glossary. It pairs the `grilling` interview with `domain-modeling`'s ADR-offer gate, nothing else.

## 1. Interview

Call the `grilling` skill on the topic. Work the frontier to an empty state, confirmed by the user, exactly as that skill defines.

## 2. Offer an ADR

Once the interview settles a decision, check it against the offer criteria and template at:

`C:\Users\Quirora\Documents\qu1r0raOS\agent-skills\skills\domain-modeling\ADR-FORMAT.md`

Offer to write the ADR only when all three criteria hold. Otherwise, say nothing about it.

## Out of scope

This skill never touches `CONTEXT.md` and never challenges terminology. For that, use `grill-with-docs`.
