#!/usr/bin/env python3
"""AI sanity review for harvested renderer requirement matrices.

This pass removes obvious non-requirements, merges orphaned settings/code examples into
nearby requirement notes, marks remaining rows as ai-reviewed, and flags ambiguous rows
for Jeremy/grill-me review.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQ_DIR = ROOT / "docs" / "requirements"
QUEUE = ROOT / "interviews" / "p004-grill-queue.md"

@dataclass
class Row:
    id: str
    area: str
    requirement: str
    source: str
    evidence: str
    link: str
    status: str
    notes: str
    review: str = "Standalone requirement after AI review."

DROP_PATTERNS = [
    (re.compile(r"^!\[", re.I), "image/link artifact, not a requirement"),
    (re.compile(r"^\[[^\]]+\]\(https?://", re.I), "navigation link artifact, not a requirement"),
    (re.compile(r"wiki contains technical details|non-technical overview|working example", re.I), "wiki overview/link text, not a requirement"),
    (re.compile(r"^(users can interact|clicking and dragging.*perform \d+ actions|the following columns are expected|the following table describes|the object below contains|the sections below describe)", re.I), "introductory/aggregate text; covered by more specific rows"),
    (re.compile(r"^\*?\*?returns:\*?\*?", re.I), "API return-type detail; not a user-facing requirement"),
]

ORPHAN_SETTING = re.compile(r"^(`?\{.*\}`?|\{\s|\[\s|[}\]],?\s*$|};?$)")
QUESTION_PATTERNS = [
    (re.compile(r"\bCAT\b|viz-library", re.I), "Legacy CAT/viz-library-specific check; confirm whether it remains in scope for nextgen standalone demos."),
    (re.compile(r"looks good|appears as normal|fits on one page", re.I), "Vague visual acceptance criterion; define concrete browser/visual evidence."),
    (re.compile(r"webcharts|webChart", re.I), "Legacy Webcharts API/detail; preserve behavior only if needed, not implementation dependency."),
    (re.compile(r"normality|p-value|statistical|Wilcoxon|t-test", re.I), "Statistical behavior needs explicit validation stance and acceptable approximation boundary."),
]

def split_row(line: str) -> list[str]:
    assert line.startswith("|") and line.endswith("|")
    cells, cur, esc = [], [], False
    for ch in line[1:-1]:
        if esc:
            cur.append(ch)
            esc = False
        elif ch == "\\":
            cur.append(ch)
            esc = True
        elif ch == "|":
            cells.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
    cells.append("".join(cur).strip())
    return cells

def row_line(cells: list[str]) -> str:
    return "| " + " | ".join(c.replace("|", "\\|") for c in cells) + " |"

def parse_rows(text: str) -> tuple[list[str], list[Row], list[str]]:
    lines = text.splitlines()
    pre, rows, post = [], [], []
    in_rows = False
    for line in lines:
        if line.startswith("| ID | Area |"):
            in_rows = True
            continue
        if in_rows and line.startswith("|---"):
            continue
        if in_rows and line.startswith("| "):
            cells = split_row(line)
            if len(cells) >= 8:
                rows.append(Row(*cells[:8]))
            continue
        if in_rows:
            post.append(line)
        else:
            pre.append(line)
    return pre, rows, post

def review_row(row: Row) -> tuple[str, Row | None]:
    req = row.requirement.strip()
    for pat, reason in DROP_PATTERNS:
        if pat.search(req):
            return reason, None
    if ORPHAN_SETTING.search(req) or (req.startswith("`") and req.endswith("`") and len(req) < 250):
        return "orphaned settings/code example; merge with previous requirement", None

    comments = []
    status = "ai-reviewed"
    for pat, comment in QUESTION_PATTERNS:
        if pat.search(req):
            comments.append(comment)
            status = "needs-jeremy-review"
    if req.endswith(":"):
        comments.append("Requirement ends with a colon and may be an aggregate lead-in; confirm whether child rows cover it.")
        status = "needs-jeremy-review"
    if len(req) > 550:
        comments.append("Long compound row; consider splitting after Jeremy review if it encodes multiple behaviors.")
        status = "needs-jeremy-review"

    row.status = status
    row.notes = "AI reviewed. " + (" ".join(comments) if comments else "Standalone and testable enough for human review.")
    row.review = "Needs Jeremy review." if status == "needs-jeremy-review" else "OK for human review."
    return "keep", row

def process_file(path: Path) -> tuple[int, int, int, list[Row], list[str]]:
    pre, rows, post = parse_rows(path.read_text())
    kept: list[Row] = []
    drops: list[str] = []
    pending_merge: list[str] = []
    for row in rows:
        action, reviewed = review_row(row)
        if reviewed is None:
            if "merge with previous" in action and kept:
                kept[-1].notes += f" Merged harvested artifact {row.id} into this row: {row.requirement}"
            else:
                drops.append(f"- `{row.id}`: {action} — {row.requirement[:220]}")
            continue
        kept.append(reviewed)

    table = [
        "| ID | Area | Requirement | Source | Evidence Type | Test/Evidence Link | Status | AI Review | Notes |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for r in kept:
        table.append(row_line([r.id, r.area, r.requirement, r.source, r.evidence, r.link, r.status, r.review, r.notes]))

    body = pre + ["", "## Requirements", ""] + table + [""]
    body += ["## AI review removals / merges", ""]
    body += drops or ["- None."]
    body += ["", "## Next review tasks", "", "- Jeremy reviews rows marked `needs-jeremy-review`.", "- Confirm evidence type for each `ai-reviewed` row.", "- Add baseline and nextgen demo evidence links during implementation."]
    path.write_text("\n".join(body).rstrip() + "\n")
    flagged = [r for r in kept if r.status == "needs-jeremy-review"]
    return len(rows), len(kept), len(drops), flagged, drops

def main() -> None:
    summary = []
    queue = ["# P004 grill-me queue", "", "Questions and ambiguous requirements surfaced during AI review.", ""]
    for path in sorted(REQ_DIR.glob("*.md")):
        if path.name == "README.md":
            continue
        before, kept, dropped, flagged, drops = process_file(path)
        renderer = path.stem
        summary.append((renderer, before, kept, dropped, len(flagged)))
        if flagged:
            queue.append(f"## {renderer}")
            queue.append("")
            for r in flagged[:20]:
                queue.append(f"- `{r.id}`: {r.requirement}")
                queue.append(f"  - AI comment: {r.notes.replace('AI reviewed. ', '')}")
            if len(flagged) > 20:
                queue.append(f"- ... {len(flagged) - 20} additional flagged rows in `docs/requirements/{renderer}.md`.")
            queue.append("")
    readme = ["# Renderer requirements", "", "Requirement matrices harvested from RhoInc wiki sources and passed through an AI sanity review.", "", "| Renderer | Harvested rows | AI-reviewed rows kept | Removed/merged artifacts | Needs Jeremy review |", "|---|---:|---:|---:|---:|"]
    for renderer, before, kept, dropped, flagged in summary:
        readme.append(f"| [{renderer}](./{renderer}.md) | {before} | {kept} | {dropped} | {flagged} |")
    readme += ["", "## Review sequence", "", "1. AI review marks standalone rows as `ai-reviewed` and ambiguous rows as `needs-jeremy-review`.", "2. Jeremy reviews flagged rows through the grill-me/interview workflow, starting with the renderer that will be implemented next.", "3. After decisions, rows move to `reviewed`, then implementation/evidence statuses."]
    (REQ_DIR / "README.md").write_text("\n".join(readme) + "\n")
    QUEUE.write_text("\n".join(queue).rstrip() + "\n")
    print("renderer,harvested,kept,removed_or_merged,needs_jeremy_review")
    for item in summary:
        print(",".join(map(str, item)))

if __name__ == "__main__":
    main()
