"""Check a writing-guide entry and its project guide.

Subcommands:
  quotes ENTRY [--page URL=FILE]...  each quoted passage under a "Source:" line
                                     appears in one of the entry's source pages
  parity ENTRY GUIDE                 each entry quote appears in the guide under
                                     the same grade, and each rule number the
                                     guide cites exists

Exit status is 0 when everything passes, 1 when a passage is missing or the two
files differ, and 3 when a passage could only go unchecked (a page was
unreachable).
"""

from __future__ import annotations

import argparse
import html
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

GRADES = (
    "requirement",
    "authoritative guideline",
    "empirical",
    "convention",
    "preference",
)
MIN_PASSAGE = 25
MIN_SEGMENT = 12
MIN_PAGE = 600
USER_AGENT = "Mozilla/5.0 (compatible; check_guide)"
LIST_ITEM = re.compile(r"^\s*(?:\d+\.|[-*])\s")
HEADING = re.compile(r"^#{2,4}\s+(.*?)\s*$")


@dataclass
class Passage:
    text: str
    line: int
    grade: str | None
    label: str = ""

    @property
    def segments(self) -> list[str]:
        parts = re.split(r"…|\.\.\.", self.text)
        compact = (squash(part) for part in parts)
        return [part for part in compact if len(part) >= MIN_SEGMENT]


def straighten(text: str) -> str:
    table = {
        "‘": "'",
        "’": "'",
        "“": '"',
        "”": '"',
        "–": "-",
        "—": "-",
        "−": "-",
        " ": " ",
        "­": "",
    }
    return text.translate(str.maketrans(table))


def squash(text: str) -> str:
    """Keep lowercase letters and digits so layout, quote marks, and glyphs never decide a match."""
    return re.sub(r"[\W_]+", "", straighten(text).lower())


def page_to_text(raw: str) -> str:
    raw = re.sub(
        r"<(script|style)\b.*?</\1>", " ", raw, flags=re.DOTALL | re.IGNORECASE
    )
    return html.unescape(re.sub(r"<[^>]+>", " ", raw))


def read_passages(path: Path) -> list[Passage]:
    lines = path.read_text(encoding="utf-8").splitlines()
    passages: list[Passage] = []
    grade: str | None = None
    index = 0
    while index < len(lines):
        match = HEADING.match(lines[index])
        if match:
            title = match.group(1).strip().lower()
            grade = title if title in GRADES else None
        if "Source:" not in lines[index]:
            index += 1
            continue
        start = index
        block = [lines[index].split("Source:", 1)[1]]
        index += 1
        while (
            index < len(lines)
            and lines[index].strip()
            and not LIST_ITEM.match(lines[index])
        ):
            block.append(lines[index])
            index += 1
        joined = straighten(" ".join(part.strip() for part in block))
        label = joined.split('"', 1)[0]
        for found in re.findall(r'"([^"]+)"', joined):
            if len(found.strip()) >= MIN_PASSAGE:
                passages.append(Passage(found.strip(), start + 1, grade, label))
    return passages


def read_sources(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    front = text.split("\n---", 2)[0] if text.startswith("---") else ""
    return re.findall(r"^\s*-\s+url:\s*(\S+)", front, flags=re.MULTILINE)


def extract(data: bytes, work: Path) -> str | None:
    if data.startswith(b"%PDF"):
        tool = shutil.which("pdftotext")
        if not tool:
            return None
        work.write_bytes(data)
        done = subprocess.run([tool, str(work), "-"], capture_output=True, check=False)
        return done.stdout.decode("utf-8", errors="replace")
    return page_to_text(data.decode("utf-8", errors="replace"))


def fetch(url: str, work: Path) -> str | None:
    """Return a page's text, trying the live URL and then its Wayback copy.

    A bot wall often answers 200 with a stub body, so the extracted text, not the
    status code, decides whether an attempt worked.
    """
    attempts = [url]
    if "web.archive.org" not in url:
        attempts.append(f"https://web.archive.org/web/2026/{url}")
    for attempt in attempts:
        done = subprocess.run(
            [
                "curl",
                "-sL",
                "--compressed",
                "--max-time",
                "60",
                "-A",
                USER_AGENT,
                attempt,
            ],
            capture_output=True,
            check=False,
        )
        if done.returncode != 0:
            continue
        text = extract(done.stdout, work)
        if text and len(squash(text)) >= MIN_PAGE:
            return text
    return None


def likely_page(label: str, urls: list[str]) -> str | None:
    words = {w for w in re.findall(r"[a-z]{4,}", label.lower())}
    scored = [(len(words & set(re.findall(r"[a-z]{4,}", u.lower()))), u) for u in urls]
    best = max(scored, default=(0, None))
    return best[1] if best[0] else None


def run_quotes(entry: Path, overrides: dict[str, Path]) -> int:
    urls = read_sources(entry)
    passages = read_passages(entry)
    pages: dict[str, str | None] = {}
    with tempfile.TemporaryDirectory() as tmp:
        for url in urls:
            if url in overrides:
                pages[url] = page_to_text(overrides[url].read_text(encoding="utf-8"))
            else:
                pages[url] = fetch(url, Path(tmp) / "download.pdf")
    unreachable = [url for url, text in pages.items() if text is None]
    squashed = [squash(text) for text in pages.values() if text]
    counts = {"found": 0, "missing": 0, "unchecked": 0}
    for passage in passages:
        hit = all(any(seg in page for page in squashed) for seg in passage.segments)
        if hit:
            status = "found"
        else:
            status = "unchecked" if unreachable else "missing"
        counts[status] += 1
        if status != "found":
            hint = likely_page(passage.label, unreachable) if unreachable else None
            suffix = f" (likely page: {hint})" if status == "unchecked" and hint else ""
            print(f"{status}: {entry.name}:{passage.line}: {passage.text[:70]}{suffix}")
    for url in unreachable:
        print(f"unreachable: {url}")
    print(
        f"quotes: {counts['found']} found, {counts['missing']} missing, {counts['unchecked']} unchecked"
    )
    if counts["missing"]:
        return 1
    return 3 if counts["unchecked"] else 0


def same_quote(first: Passage, second: Passage) -> bool:
    def inside(small: list[str], big: list[str]) -> bool:
        return bool(small) and all(any(seg in other for other in big) for seg in small)

    return inside(first.segments, second.segments) or inside(
        second.segments, first.segments
    )


def rule_numbers(guide: Path) -> set[int]:
    text = guide.read_text(encoding="utf-8")
    return {int(n) for n in re.findall(r"^(\d+)\.\s+\*\*", text, flags=re.MULTILINE)}


def cited_numbers(guide: Path) -> list[tuple[int, int]]:
    cited: list[tuple[int, int]] = []
    pattern = re.compile(r"\b[Rr]ules?\s+((?:\d+\s*(?:[-–,]|and|to)?\s*)+)")
    for number, line in enumerate(guide.read_text(encoding="utf-8").splitlines(), 1):
        for match in pattern.finditer(line):
            cited.extend((int(n), number) for n in re.findall(r"\d+", match.group(1)))
    return cited


def run_parity(entry: Path, guide: Path) -> int:
    entry_quotes = read_passages(entry)
    guide_quotes = read_passages(guide)
    problems = 0
    reported: set[tuple[int, int]] = set()
    for quote in entry_quotes:
        twins = [other for other in guide_quotes if same_quote(quote, other)]
        if not twins:
            print(f"absent from guide: {entry.name}:{quote.line}: {quote.text[:70]}")
            problems += 1
        elif all(other.grade != quote.grade for other in twins):
            if (quote.line, twins[0].line) in reported:
                continue
            reported.add((quote.line, twins[0].line))
            print(
                f"grade differs: {entry.name}:{quote.line} is {quote.grade}, "
                f"{guide.name}:{twins[0].line} is {twins[0].grade}"
            )
            problems += 1
    for quote in guide_quotes:
        if not any(same_quote(quote, other) for other in entry_quotes):
            print(f"guide only: {guide.name}:{quote.line}: {quote.text[:70]}")
    existing = rule_numbers(guide)
    if existing:
        for number, line in cited_numbers(guide):
            if number not in existing:
                print(f"no such rule: {guide.name}:{line} cites rule {number}")
                problems += 1
    print(f"parity: {problems} difference(s)")
    return 1 if problems else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    quotes = sub.add_parser("quotes")
    quotes.add_argument("entry", type=Path)
    quotes.add_argument("--page", action="append", default=[], metavar="URL=FILE")
    parity = sub.add_parser("parity")
    parity.add_argument("entry", type=Path)
    parity.add_argument("guide", type=Path)
    args = parser.parse_args()
    if args.command == "quotes":
        overrides = {}
        for pair in args.page:
            url, _, file = pair.partition("=")
            overrides[url] = Path(file)
        return run_quotes(args.entry, overrides)
    return run_parity(args.entry, args.guide)


if __name__ == "__main__":
    sys.exit(main())
