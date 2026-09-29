---
name: grill-qu1r0ra
description: Grill the user through a material, user-owned design decision when asked or when an unresolved choice blocks a reliable outcome; offer an ADR when warranted.
---

# Grill qu1r0ra

Use this personal wrapper when the user asks to be grilled or a material,
user-owned design choice needs an interview. Make routine technical choices
without starting this workflow. It uses the `grilling` interview and reads the
ADR offer criteria from `domain-modeling/ADR-FORMAT.md`.

## 1. Interview

Call the `grilling` skill on the topic. Work the frontier to an empty state and get the user's confirmation, exactly as that skill defines. Send each interview question in ordinary chat prose with your recommendation. Do not use `AskUserQuestion` or other question cards.

## 2. Offer an ADR

Once the interview settles a decision, check it against the offer criteria and template at:

`../domain-modeling/ADR-FORMAT.md`

Offer to write the ADR only when all three criteria hold. Otherwise, say nothing about it.

## Out of scope

This skill never touches `CONTEXT.md` and never challenges terminology. For that, use `grill-with-docs`.
