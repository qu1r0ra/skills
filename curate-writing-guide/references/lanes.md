# Research lanes

Read-only leaf subagents, in two rounds: a sweep of four broad lanes, then one gap-fill round of narrow lanes. Every brief carries the use-case summary, this lane's section, and the shared rules.

## Shared rules

- Use public sources only.
- Fetch raw text with `curl` and copy each quote from it: WebFetch returns a summary, and a summary is not a quote. Reach apastyle.apa.org through `https://web.archive.org/web/2026/<url>`, which passes its bot wall.
- Return each finding as: the rule, its source URL, provider, title, a passage, the date fetched, and a tag. `verified` means the passage was copied from raw text you read; `unverified` means a snippet, a summary, or a page you could not open.
- End the report with **Gaps**: each question you could not answer, or answered only `unverified`.
- A lane that finds nothing lists every search it ran and every result it named.
- Keep the report under 1,500 words.

## Lane size

A lane carries at most five questions. Split a broader brief by topic, one lane per topic.

## Sweep lanes

### Requirements

**Question:** What must the writing satisfy: venue rules, institutional or legal requirements, submission limits, mandatory structure?
**Search:** the venue's author instructions, institution handbooks, templates, and mandatory reporting rules.
**Evidence standard:** an official page of the body that imposes the rule, with the passage quoted. Report a rule's absence by naming the pages checked. Grade: `requirement`.

### Conventions

**Question:** What do the field's guidelines and conventions say: reporting guidelines, style manuals, discipline norms?
**Search:** reporting guidelines (EQUATOR-type), style manuals, society guidance, and recent norms the field cites.
**Evidence standard:** a named guideline or manual from a recognised body, with the passage quoted. Field practice seen only in papers is a `convention`. Grades: `authoritative guideline`, `convention`.

### Craft

**Question:** What does research and expert craft say makes this kind of writing work for this audience?
**Search:** empirical studies on readability and comprehension, and expert writing guidance for the genre.
**Evidence standard:** a study (name sample, method, and finding) or an expert source with a named author. Opinion without evidence is a `preference`. Grades: `empirical`, `preference`.

### Exemplars

**Question:** Which real, strong pieces of this kind exist, and what techniques do they share?
**Search:** published examples at the venue or in the field, prioritising open-access, public-domain, or openly licensed pieces.
**Evidence standard:** each exemplar named with URL, licence, and why it qualifies; the techniques it shows, each tied to a quoted passage. State the licence status of every item so the parent can apply the capture limits in [entry.md](entry.md#exemplars).

## Gap-fill lanes

Group the sweep's Gaps by topic. Each gap lane gets one question per gap, the URLs the sweep already found for it, and the evidence standard of the grade its answer would carry. The sweep lane whose topic the gap belongs to supplies the standard.
