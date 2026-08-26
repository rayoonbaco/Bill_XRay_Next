"""PASS 38 - Investigation Engine for Bill X-Ray Next.

This module does not write an exposé and does not accuse anyone of wrongdoing.
It turns verified/decompiled bill material into an *investigation queue*: places
where a human analyst should look harder because the text may involve unusual
specificity, delegated authority, overrides, exceptions, large before/after
changes, or temporary rules.

Doctrine: curiosity may rank a question; only later evidence may support a claim.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

SECTION_RE = re.compile(r"^SEC\.\s+([0-9A-Z.-]+)\.\s*(.*)$", re.I)


@dataclass(frozen=True)
class SignalRule:
    signal: str
    pattern: str
    base_score: int
    why_human_might_care: str
    ordinary_explanation: str
    uncertainty: str


@dataclass
class InvestigationCandidate:
    candidate_id: str
    bill_id: str
    section: str
    section_heading: str
    category: str
    score: int
    source_start_line: int
    source_end_line: int
    evidence_excerpt: str
    why_human_might_care: str
    question_to_investigate: str
    ordinary_explanations: list[str]
    uncertainty: list[str]
    source_basis: str
    public_claim_allowed: bool = False


RULES: tuple[SignalRule, ...] = (
    SignalRule(
        "delegated_authority",
        r"\b(?:Secretary|Administrator|Commission|Board|agency)\s+shall\s+(?:prescribe|promulgate|determine|establish)\b",
        84,
        "Congress may be leaving an important implementation choice to an agency or official.",
        "Detailed administration often has to be delegated because Congress cannot specify every operational rule in statutory text.",
        "The sentence alone does not show how broad the discretion is or whether later text tightly limits it.",
    ),
    SignalRule(
        "override",
        r"\bnotwithstanding\b",
        82,
        "An override can reveal which ordinary rule Congress chose not to apply in this situation.",
        "Overrides are common drafting tools used to resolve conflicts between statutes or make a narrow rule work as intended.",
        "The overridden rule must be identified before judging whether the override is unusual or consequential.",
    ),
    SignalRule(
        "exception",
        r"\b(?:special rule|exception|except as provided|shall not apply)\b",
        76,
        "Exceptions can change who actually receives a benefit, bears a burden, or falls outside the headline rule.",
        "Tax and regulatory systems routinely need exceptions to prevent double counting, edge-case unfairness, or unintended interactions.",
        "An exception is not evidence of favoritism; its beneficiaries, purpose, and effect still have to be reconstructed.",
    ),
    SignalRule(
        "specific_class",
        r"\b(?:certain|specified|qualified)\s+(?:children|business(?:es)?|trade|property|employees?|taxpayers?|payments?|services?|entities|individuals?)\b",
        68,
        "A narrowly defined class may matter because small wording differences decide who qualifies and who does not.",
        "Specific eligibility language is normal when Congress needs a program or tax rule to have enforceable boundaries.",
        "The class may be broad in practice; the definition and real affected population must be traced before drawing conclusions.",
    ),
    SignalRule(
        "temporary_or_transition",
        r"\b(?:temporary|transition|termination|sunset|before January 1, 2026|2018 through 2025)\b",
        74,
        "Temporary rules can make the immediate effect and the long-term effect very different.",
        "Temporary provisions may reflect budget rules, transition needs, experimentation, or a deliberate future reconsideration point.",
        "The detected date may be only one part of a larger effective-date or transition scheme.",
    ),
)

COMPILED = tuple((rule, re.compile(rule.pattern, re.I)) for rule in RULES)


def _section_map(lines: list[str]) -> list[tuple[str, str]]:
    current_sec = ""
    current_heading = ""
    out: list[tuple[str, str]] = []
    for raw in lines:
        m = SECTION_RE.match(raw.strip())
        if m:
            current_sec = "SEC. " + m.group(1)
            current_heading = m.group(2).strip().rstrip(".")
        out.append((current_sec, current_heading))
    return out


def _excerpt(lines: list[str], line_no: int, radius: int = 1) -> tuple[int, int, str]:
    start = max(1, line_no - radius)
    end = min(len(lines), line_no + radius)
    text = " ".join(x.strip() for x in lines[start - 1:end] if x.strip())
    return start, end, re.sub(r"\s+", " ", text)[:900]


def _question(rule: SignalRule, sec: str, heading: str) -> str:
    place = heading or sec or "this part of the bill"
    prompts = {
        "delegated_authority": f"Exactly what decision is delegated in {place}, what limits apply, and who is affected by that decision?",
        "override": f"What ordinary rule does {place} override, and what changes because of that override?",
        "exception": f"Who falls inside and outside the exception in {place}, and what practical difference does it make?",
        "specific_class": f"Who actually qualifies for the narrowly defined class in {place}, and why was that boundary chosen?",
        "temporary_or_transition": f"What changes when the temporary or transition rule in {place} begins or ends?",
    }
    return prompts[rule.signal]


def scan_text(source: Path, bill_id: str) -> list[InvestigationCandidate]:
    lines = source.read_text(encoding="utf-8").splitlines()
    secmap = _section_map(lines)
    candidates: list[InvestigationCandidate] = []
    seen: set[tuple[str, str, str]] = set()

    for line_no, raw in enumerate(lines, start=1):
        sec, heading = secmap[line_no - 1]
        for rule, rx in COMPILED:
            match = rx.search(raw)
            if not match:
                continue
            # De-duplicate repeated drafting language in the same section/category.
            fingerprint = (sec, rule.signal, re.sub(r"\W+", " ", match.group(0).lower()).strip())
            if fingerprint in seen:
                continue
            seen.add(fingerprint)
            start, end, evidence = _excerpt(lines, line_no)
            candidates.append(
                InvestigationCandidate(
                    candidate_id=f"{bill_id}:text:{line_no}:{rule.signal}",
                    bill_id=bill_id,
                    section=sec,
                    section_heading=heading,
                    category=rule.signal,
                    score=rule.base_score,
                    source_start_line=start,
                    source_end_line=end,
                    evidence_excerpt=evidence,
                    why_human_might_care=rule.why_human_might_care,
                    question_to_investigate=_question(rule, sec, heading),
                    ordinary_explanations=[rule.ordinary_explanation],
                    uncertainty=[rule.uncertainty],
                    source_basis="official_bill_text_signal",
                )
            )
    return candidates


def _money_number(value: str | None) -> float | None:
    if not value or not value.startswith("$"):
        return None
    try:
        return float(value[1:].replace(",", ""))
    except ValueError:
        return None


def candidates_from_atomic_events(path: Path, bill_id: str) -> list[InvestigationCandidate]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    out: list[InvestigationCandidate] = []
    for event in payload.get("events", []):
        # Significance may only build on meaning that already survived the prior gate.
        # Large unresolved numbers are not human facts and must not outrank understood ones.
        if not event.get("publishable", False):
            continue
        label0 = (event.get("semantic_label") or "").strip().lower()
        if label0 in {"", "in general"}:
            continue
        before = _money_number(event.get("before"))
        after = _money_number(event.get("after"))
        if before is None or after is None or before <= 0:
            continue
        ratio = after / before
        delta = after - before
        # This is an attention trigger, not a judgment about whether the change is good/bad.
        if ratio < 1.5 and ratio > 0.67 and abs(delta) < 100_000:
            continue
        magnitude = min(96, 68 + int(min(28, abs(ratio - 1.0) * 12)))
        section = event.get("section", "")
        label = event.get("semantic_label") or event.get("official_heading") or section
        out.append(
            InvestigationCandidate(
                candidate_id=f"{bill_id}:atomic:{event.get('event_id','unknown')}",
                bill_id=bill_id,
                section=section,
                section_heading=event.get("official_heading", ""),
                category="large_before_after_change",
                score=magnitude,
                source_start_line=int(event.get("source_start_line", 0)),
                source_end_line=int(event.get("source_end_line", 0)),
                evidence_excerpt=event.get("evidence_excerpt", ""),
                why_human_might_care=f"This verified before/after event changes {label} from {event.get('before')} to {event.get('after')}, large enough to deserve context before the final story is written.",
                question_to_investigate=f"Who is affected by the change in {label}, how often does it matter, and what is the real financial consequence?",
                ordinary_explanations=["A large numerical change can reflect inflation, consolidation of prior rules, a policy reset, or a threshold that affects relatively few people; size alone does not establish importance."],
                uncertainty=["The statutory number alone does not establish budget cost, number of beneficiaries, distributional effect, or whether another limitation offsets the apparent change."],
                source_basis="verified_atomic_meaning_event",
            )
        )
    return out


def rank_candidates(candidates: Iterable[InvestigationCandidate], limit: int = 40) -> list[InvestigationCandidate]:
    # Build a portfolio, not a leaderboard dominated by whichever drafting phrase repeats most.
    ordered = sorted(candidates, key=lambda c: (-c.score, c.source_start_line, c.candidate_id))
    buckets: dict[str, list[InvestigationCandidate]] = {}
    for c in ordered:
        buckets.setdefault(c.category, []).append(c)
    category_order = sorted(buckets, key=lambda k: (-buckets[k][0].score, k))
    selected: list[InvestigationCandidate] = []
    round_no = 0
    while len(selected) < limit:
        added = False
        for category in category_order:
            bucket = buckets[category]
            if round_no < len(bucket) and round_no < 10:
                selected.append(bucket[round_no])
                added = True
                if len(selected) >= limit:
                    break
        if not added:
            break
        round_no += 1
    return selected


def write_payload(source: Path, atomic_events: Path, bill_id: str, out: Path) -> dict:
    raw = scan_text(source, bill_id) + candidates_from_atomic_events(atomic_events, bill_id)
    ranked = rank_candidates(raw)
    categories: dict[str, int] = {}
    for c in ranked:
        categories[c.category] = categories.get(c.category, 0) + 1
    payload = {
        "schema_version": "38.0",
        "bill_id": bill_id,
        "doctrine": "investigate_before_editorialize",
        "candidate_count": len(ranked),
        "category_counts": dict(sorted(categories.items())),
        "public_claims_allowed": sum(c.public_claim_allowed for c in ranked),
        "guardrail": "These are investigation candidates, not findings of wrongdoing and not public prose.",
        "candidates": [asdict(c) for c in ranked],
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("source")
    p.add_argument("--atomic-events", required=True)
    p.add_argument("--bill-id", required=True)
    p.add_argument("--out", required=True)
    a = p.parse_args()
    payload = write_payload(Path(a.source), Path(a.atomic_events), a.bill_id, Path(a.out))
    print(
        f"PASS 38: ranked {payload['candidate_count']} investigation candidates across "
        f"{len(payload['category_counts'])} categories; {payload['public_claims_allowed']} public claims allowed"
    )


if __name__ == "__main__":
    main()
