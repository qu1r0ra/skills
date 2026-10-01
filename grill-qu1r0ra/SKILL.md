---
name: grill-qu1r0ra
description: Grill the user through a material, user-owned design decision when asked or when an unresolved choice blocks a reliable outcome; offer an ADR when warranted.
---

# Grill qu1r0ra

Follow [`grilling`](../grilling/SKILL.md) for the interview, frontier, and
confirmation gate. Apply this wrapper when the user asks to be grilled or a
material, user-owned choice blocks a reliable outcome; make routine technical
choices directly.

Send interview questions in ordinary chat prose with recommendations. This
replaces upstream's question formatting; use no question cards.

After the confirmed decision, check the offer criteria in
[`ADR-FORMAT.md`](../domain-modeling/ADR-FORMAT.md). Offer an ADR only when all
three criteria hold; write it only after the user accepts. Keep this interview
free of glossary maintenance. If the user explicitly requests the documented
interview workflow, use [`grill-with-docs`](../grill-with-docs/SKILL.md).

Completion: the decision frontier is empty, the user has confirmed the shared
understanding, and any warranted ADR offer has been made. An unanswered
decision or pending confirmation keeps the interview open.
