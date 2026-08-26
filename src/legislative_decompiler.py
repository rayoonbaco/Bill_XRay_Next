"""Bill X-Ray Next legislative decompiler.

PASS 36 upgrades the PASS 35 meaning substrate by splitting statutory sections
into atomic before/after operations. It does not write public prose. Its first
obligation is to preserve meaning and admit missing context.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

SECTION_RE = re.compile(r"^SEC\.\s+([0-9A-Z.-]+)\.\s+(.+?)\s*$")
SUB_RE = re.compile(
    r"substitut(?:ing|e)\s+[`'\"]?\$([0-9][0-9,]*(?:\.\d+)?)['`\"]?\s+for\s+[`'\"]?\$([0-9][0-9,]*(?:\.\d+)?)",
    re.I,
)
PERCENT_RE = re.compile(r"(?:shall be|is)\s+(\d+(?:\.\d+)?)\s+percent", re.I)
LABEL_RE = re.compile(
    r"(?:``|\")?\((?:\d+|[A-Z]|[ivxlcdm]+)\)\s+([A-Z][A-Za-z0-9 ,/'-]{2,90}?)\.--",
    re.I,
)


@dataclass
class AtomicMeaningEvent:
    bill_id: str
    event_id: str
    section: str
    official_heading: str
    semantic_label: str
    actor: str
    action: str
    target: str
    before: str | None
    after: str | None
    timing: list[str]
    legal_pointer: str
    context_required: list[str]
    confidence: float
    uncertainty: list[str]
    source_start_line: int
    source_end_line: int
    evidence_excerpt: str

    @property
    def publishable(self) -> bool:
        return self.confidence >= 0.90 and not self.uncertainty and not self.context_required


def _plain_target(heading: str) -> str:
    text = heading.strip().rstrip(".").lower()
    prefixes = (
        "increase in and modification of ", "increase in ", "modification of ",
        "extension of ", "repeal of ", "limitation on ", "elimination of ",
    )
    for prefix in prefixes:
        if text.startswith(prefix):
            text = text[len(prefix):]
            break
    replacements = {
        "child tax credit": "the child tax credit",
        "standard deduction": "the standard deduction",
        "21-percent corporate tax rate": "the corporate income-tax rate",
        "qualified business income": "the qualified-business-income rules",
    }
    return replacements.get(text, text)


def _timing(text: str) -> list[str]:
    if "2018 through 2025" in text or (
        "after December 31, 2017" in text and "before January 1, 2026" in text
    ):
        return ["tax years 2018 through 2025"]
    if "after December 31, 2017" in text:
        return ["tax years beginning after 2017"]
    return []


def sections(lines: list[str]) -> Iterable[tuple[str, str, int, int, list[str]]]:
    starts: list[tuple[int, str, str]] = []
    for i, line in enumerate(lines, start=1):
        match = SECTION_RE.match(line.strip())
        if match:
            starts.append((i, match.group(1), match.group(2)))
    for idx, (start, sec, heading) in enumerate(starts):
        end = starts[idx + 1][0] - 1 if idx + 1 < len(starts) else len(lines)
        yield sec, heading, start, end, lines[start - 1:end]


def _nearest_label(text: str, position: int, fallback: str) -> str:
    candidates = [(m.start(), m.group(1).strip()) for m in LABEL_RE.finditer(text[:position])]
    if not candidates:
        return fallback
    return candidates[-1][1]


def _line_for_offset(body: list[str], section_start: int, offset: int) -> int:
    running = 0
    for idx, raw in enumerate(body):
        piece = raw.strip()
        if not piece:
            continue
        next_running = running + len(piece) + 1
        if offset < next_running:
            return section_start + idx
        running = next_running
    return section_start + max(0, len(body) - 1)


def _pointer_near(text: str, position: int) -> str:
    window = text[max(0, position - 240):position + 80]
    # Preserve the most useful nearby subsection reference without claiming its meaning.
    refs = re.findall(r"(?:subsection|paragraph|subparagraph)\s+\(([A-Za-z0-9]+)\)(?:\(([A-Za-z0-9]+)\))?", window, re.I)
    if not refs:
        return ""
    a, b = refs[-1]
    return f"{a}({b})" if b else a


def decompile_section(
    bill_id: str,
    sec: str,
    heading: str,
    start: int,
    end: int,
    body: list[str],
) -> list[AtomicMeaningEvent]:
    text = " ".join(x.strip() for x in body if x.strip())
    base_target = _plain_target(heading)
    timing = _timing(text)
    events: list[AtomicMeaningEvent] = []

    for n, match in enumerate(SUB_RE.finditer(text), start=1):
        new, old = match.groups()
        label = _nearest_label(text, match.start(), heading.strip().rstrip("."))
        pointer = _pointer_near(text, match.start())
        uncertainty: list[str] = []
        context_required: list[str] = []
        target = base_target
        confidence = 0.93

        # A descriptive statutory subheading can safely narrow the semantic target.
        if label.lower() not in {heading.strip().rstrip(".").lower(), "in general"}:
            target = f"{base_target} — {label.lower()}"

        # A generic cross-reference does not tell us the human category by itself.
        if base_target == "the standard deduction":
            context_required.append("Resolve the referenced pre-amendment Internal Revenue Code category before naming the filing status publicly.")
            confidence = 0.88

        source_line = _line_for_offset(body, start, match.start())
        excerpt = text[max(0, match.start() - 220):min(len(text), match.end() + 220)]
        events.append(
            AtomicMeaningEvent(
                bill_id=bill_id,
                event_id=f"{bill_id}:{sec}:substitution:{n}",
                section="SEC. " + sec,
                official_heading=heading.strip().rstrip("."),
                semantic_label=label,
                actor="Congress",
                action="changes",
                target=target,
                before="$" + old,
                after="$" + new,
                timing=timing,
                legal_pointer=pointer,
                context_required=context_required,
                confidence=confidence,
                uncertainty=uncertainty,
                source_start_line=source_line,
                source_end_line=source_line,
                evidence_excerpt=excerpt,
            )
        )

    if events:
        return events

    percent = PERCENT_RE.search(text)
    if percent:
        source_line = _line_for_offset(body, start, percent.start())
        events.append(
            AtomicMeaningEvent(
                bill_id=bill_id,
                event_id=f"{bill_id}:{sec}:rate:1",
                section="SEC. " + sec,
                official_heading=heading.strip().rstrip("."),
                semantic_label=heading.strip().rstrip("."),
                actor="Congress",
                action="sets",
                target=base_target,
                before=None,
                after=percent.group(1) + "%",
                timing=timing,
                legal_pointer="",
                context_required=["Retrieve the pre-amendment Internal Revenue Code rule before stating the prior corporate rate."],
                confidence=0.88,
                uncertainty=[],
                source_start_line=source_line,
                source_end_line=source_line,
                evidence_excerpt=text[max(0, percent.start() - 220):min(len(text), percent.end() + 220)],
            )
        )
    return events


def decompile_file(path: Path, bill_id: str) -> list[AtomicMeaningEvent]:
    lines = path.read_text(encoding="utf-8").splitlines()
    output: list[AtomicMeaningEvent] = []
    for sec, heading, start, end, body in sections(lines):
        output.extend(decompile_section(bill_id, sec, heading, start, end, body))
    return output


def write_payload(source: Path, bill_id: str, out: Path) -> dict:
    events = decompile_file(source, bill_id)
    payload = {
        "schema_version": "36.0",
        "bill_id": bill_id,
        "doctrine": "atomic_meaning_before_prose",
        "event_count": len(events),
        "publishable_count": sum(e.publishable for e in events),
        "needs_context_count": sum(bool(e.context_required) for e in events),
        "events": [{**asdict(e), "publishable": e.publishable} for e in events],
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("--bill-id", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    payload = write_payload(Path(args.source), args.bill_id, Path(args.out))
    print(
        f"PASS 36: wrote {payload['event_count']} atomic meaning events "
        f"({payload['publishable_count']} publishable; {payload['needs_context_count']} need more context)"
    )


if __name__ == "__main__":
    main()
