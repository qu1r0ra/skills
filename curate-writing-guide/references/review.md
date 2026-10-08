# Review brief

One read-only Standards reviewer, a leaf: it edits nothing and delegates nothing, and returns one report under 900 words. The brief carries the use-case summary, the paths to the entry and the project guide, the templates ([entry.md](entry.md), [project-guide.md](project-guide.md)), the `humanizer` skill, the project's agent-instruction files, and the author's recorded decisions. The reviewer takes those decisions as settled.

`scripts/check_guide.py` already covers quote presence, entry-to-guide parity, and whether each cited rule number exists. The reviewer judges the rest.

## Checks

1. **Template:** the project guide holds every section and item in project-guide.md, and the entry holds every field in entry.md.
2. **Grades:** each rule's grade follows the precedence order and fits its source type.
3. **Support:** each rule claims no more than its source's passage says. A rule that goes further is cut or graded `preference`.
4. **Cross-references:** each rule number cited in the Humanizer, Deviation, and Existing instructions sections names the rule that says what the citing text claims.
5. **Humanizer:** each pattern cited exists in `agent-skills/skills/humanizer/SKILL.md` under that name and number.
6. **Author decisions:** no rule contradicts a decision recorded in the Deviation rule.
7. **Usability:** read the project's real files and flag any rule that is ambiguous to apply or that conflicts with the project's tooling (packages, templates, build).
8. **Agent writing:** pointer wording, hierarchy, duplication, no-ops, and positive phrasing follow `writing-for-agents`.

## Report

A ranked list. Each finding gives its location (file:line), the defect, a concrete fix, and Blocking or Non-blocking.
