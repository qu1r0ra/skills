---
name: authoring-voice
description: Apply the user's writing voice to prose intended to carry their authorship.
disable-model-invocation: true
---

# Authoring Voice

Use the Authoring Bundle to make author-directed prose consistent without
overriding the task, evidence, audience, or required house style.

## Invocation and scope

Run only when the user explicitly invokes this skill or requests their writing
voice. Drafting prose alone does not authorize the bundle or its Humanizer pass.
Use it for prose intended to carry the user's authorship, such as a paper,
thesis, essay, or personal correspondence.

Engineering artifacts use their technical workflow: code, specifications,
tickets, ADRs, README/setup documentation, commit messages, PR descriptions,
skills, agent instructions, audits, and operations documents. Apply authoring
voice to such an artifact only when the user explicitly requests it for that
artifact. In mixed tasks, apply the bundle only to the requested authored prose.

## Procedure

1. Confirm the explicit request and the prose it covers before loading profiles
   or editorial skills. Quoted third-party text and factual extracts retain
   their source wording or extraction requirements.
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
7. For the authored prose covered by this explicit request, invoke the
   `humanizer` skill after loading this bundle and the applicable mode. Treat
   Humanizer as the final editorial task before delivery. Use Humanizer's
   embedded mode for this internal pass, so this workflow receives only the
   final prose. For a direct user request to inspect Humanizer's patterns or
   humanize pasted text, preserve Humanizer's normal pasted-text output
   instead. Humanizer owns the generic anti-formulaic catalogue; do not
   reproduce or maintain that catalogue here.
8. Run the Humanizer pass only after the substantive draft and applicable
   evidence checks are complete. Apply Humanizer within the conflict order
   above and the active writing mode. Its claim-preservation rule is a
   default, not a ban on correction:
   when supplied or verified evidence shows that a fact, citation, quotation,
   or link target is wrong, correct it and surface any material correction.
   Never invent a replacement fact or citation. If the required final Humanizer
   pass is unavailable, do not claim this workflow is complete; report the
   missing pass.
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
