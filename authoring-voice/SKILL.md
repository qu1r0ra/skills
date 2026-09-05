---
name: authoring-voice
description: Apply the user's Authoring Bundle when drafting, revising, or reviewing substantive prose on the user's behalf; use for English academic or thesis prose as well as other author-directed writing.
---

# Authoring Voice

Use the Authoring Bundle to make author-directed prose consistent without
overriding the task, evidence, audience, or required house style.

## Procedure

1. Confirm that the work is substantive prose written on the author's behalf.
   For code, quoted third-party text, or a purely factual extract, do not load
   this skill unless the task also asks for author-directed prose.
2. Read `qu1r0raOS-wikis/authoring/profiles/core-writing-voice.md`.
3. For English academic or thesis prose, also read
   `qu1r0raOS-wikis/authoring/modes/academic-writing.md`. Read
   `qu1r0raOS-wikis/authoring/references/academic-contrasts.md` only when an
   academic rule remains ambiguous.
4. Resolve conflicts in this order: direct user/task instructions; factual
   accuracy and supplied evidence; audience, template, and house style; active
   writing mode; core profile.
5. Draft or revise. Preserve author-supplied facts and stance; surface rather
   than invent a change to interpretation, scope, evidence, method, or personal
   position.
6. For a substantive academic argument, result summary, abstract, or
   conclusion, perform the mode's claim–evidence–limitation check. Inspect a
   rendered artifact whenever its formatting, cross-references, tables,
   figures, or template behavior affects the result.
7. For every substantive prose draft, review, or revision, invoke the
   `humanizer` skill after loading this bundle and the applicable mode. Use
   Humanizer's embedded mode for this internal pass, so this workflow receives
   only the final prose. For a direct user request to inspect Humanizer's
   patterns or humanize pasted text, preserve Humanizer's normal pasted-text
   output instead. Humanizer owns the generic anti-formulaic catalogue; do not
   reproduce or maintain that catalogue here.
8. Apply Humanizer only within the conflict order above and the active writing
   mode. Its claim-preservation rule is a default, not a ban on correction:
   when supplied or verified evidence shows that a fact, citation, quotation,
   or link target is wrong, correct it and surface any material correction.
   Never invent a replacement fact or citation. If the required Humanizer pass
   is unavailable, do not claim this workflow is complete; report the missing
   pass.
9. Preserve quotations, citations, equations, code, metadata, data, link
   targets, technical terms, author-approved stance, and policy-required
   disclosures unless the user explicitly asks to change them or evidence
   review identifies an error. Keep evidence and claim accuracy ahead of
   stylistic cleanup, and rerun the relevant claim-evidence-limitation check
   after the Humanizer pass.
10. Treat provenance as a separate author-and-evidence review. Humanizer's
    patterns are editorial signals, never evidence that text was AI-written and
    never a basis for an AI score or authorship verdict.

## Profile work

For a proposal to revise the bundle or calibrate it against past writing, read
`docs/research/authoring-writing-guide-index.md` first. Use
`qu1r0raOS-wikis/authoring/protocols/calibration.md` only with explicit author
approval. Keep raw corpus material outside the bundle.

## Completion

Deliver prose that follows the active mode and core profile after the required
Humanizer editorial pass and the final evidence check, while identifying any
material author decision that the available evidence cannot settle.
