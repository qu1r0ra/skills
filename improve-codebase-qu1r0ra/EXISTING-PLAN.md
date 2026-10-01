# Existing plan

Use this branch when the repo already has a plan from an earlier audit: a spec, open tickets, or draft ADRs. It extends steps 1 to 4 of `SKILL.md` and adds step 5.

## Step 1: blind workers

Keep the plan out of every worker prompt: no issue numbers, ticket text, or draft-ADR branch. Workers audit the code as it is, so a covered finding is independent confirmation. The parent reads the plan itself and lists every story, ticket, and draft ADR for step 2.

Completion: the parent holds the plan list, and no worker prompt names any item on it.

## Step 2: Covers column

Give each reconciled entry a **Covers** value: the ticket or story that already addresses it, `new`, or `conflicts #N` when the finding contradicts a plan item. A finding that the plan covers only in part is `new` for the uncovered part.

Completion: every entry has a Covers value.

## Step 3: report

Add the Covers column to the ranked table.

## Step 4: grill the gaps

Grill only `new` and `conflicts` entries. Open the grill by listing the covered entries as settled.

## Step 5: update the plan

1. **Choose patch or rebuild.** Count the open tickets that the grill's decisions supersede or restructure. At about a third of the open tickets or more, rebuild through `/to-spec-qu1r0ra` and `/to-tickets-qu1r0ra`. Below that, patch.
2. **Draft the patch** as local files, one per issue body, using the owning repository's format and tracker contract:
   - Draft the spec update. Link the published audit issue, or the saved report when unpublished, and add the new stories and decisions. Use an approved adjacent reference when the spec is frozen.
   - Write each new ticket with its blocked-by links.
   - Add acceptance lines and blocked-by links to existing tickets.
   - Mark superseded tickets to close as not planned. Keep every issue; closing preserves the record.
   - Update the execution map through `to-tickets-qu1r0ra`, keeping it consistent with the proposed blocker edges.
3. **Confirm** the final list of edits, new tickets, and closures with the user before publishing.
4. **Check drift** just before each edit: fetch the live body and compare it with the copy the draft started from, ignoring trailing CR. Stop and reconcile any body that changed.
5. **Publish** under the repository's approval rules: new tickets in dependency order first, then edits to existing tickets, approved closures, and the spec or adjacent reference. Replace provisional map names with actual ticket IDs and verify the blocker edges.

Completion: every confirmed edit, new ticket, and closure is live, and each blocked-by link resolves to an existing issue.
