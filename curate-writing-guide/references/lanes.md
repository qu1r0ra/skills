# Research lanes

Caller policy for [research-qu1r0ra](../../research-qu1r0ra/SKILL.md): a sweep of four broad lanes, then one gap-fill round of narrow lanes. Every brief carries the use-case summary, this lane's section, and the restrictions below. The wrapper owns the common read-only worker and evidence-report contract.

## Shared rules

- Use public sources only.
- Fetch public raw text with `curl`; use the wrapper's verification tags. Reach apastyle.apa.org through `https://web.archive.org/web/2026/<url>` when its live page has a bot wall.
- Include questions answered only `unverified` under **Gaps**, along with unanswered questions.
- Keep the report under 1,500 words.

## Lane size

A lane carries at most five questions. Split a broader brief by topic, one lane per topic.

## Sweep lanes

### Requirements

**Question:** What must the writing or presentation satisfy: venue rules, institutional or legal requirements, submission or time limits, mandatory structure?
**Search:** the venue's author or speaker instructions, institution handbooks, templates, and mandatory reporting rules.
**Evidence standard:** an official page of the body that imposes the rule, with the passage quoted. Report a rule's absence by naming the pages checked. Grade: `requirement`.

### Conventions

**Question:** What do the field's guidelines and conventions say: reporting guidelines, style manuals, discipline norms?
**Search:** reporting guidelines (EQUATOR-type), style manuals, society guidance, and recent norms the field cites.
**Evidence standard:** a named guideline or manual from a recognised body, with the passage quoted. Field practice seen only in papers or talks is a `convention`. Grades: `authoritative guideline`, `convention`.

### Craft

**Question:** What does research and expert craft say makes this kind of writing or presentation work for this audience?
**Search:** empirical studies on readability, listening comprehension, and visual communication, and expert writing or presentation guidance for the genre.
**Evidence standard:** a study (name sample, method, and finding) or an expert source with a named author. Opinion without evidence is a `preference`. Grades: `empirical`, `preference`.

### Exemplars

**Question:** Which real, strong pieces of this kind exist, and what techniques do they share?
**Search:** published examples, slides, or public talk transcripts at the venue or in the field, prioritising open-access, public-domain, or openly licensed pieces.
**Evidence standard:** each exemplar named with URL, licence, and why it qualifies; the techniques it shows, each tied to a quoted passage. State the licence status of every item so the parent can apply the capture limits in [entry.md](entry.md#exemplars).

## Gap-fill lanes

Group the sweep's Gaps by topic. Each gap lane gets one question per gap, the URLs the sweep already found for it, and the evidence standard of the grade its answer would carry. The sweep lane whose topic the gap belongs to supplies the standard.
