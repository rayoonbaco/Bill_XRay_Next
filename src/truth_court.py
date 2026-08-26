"""PASS 39 - Adversarial Truth Court for Bill X-Ray Next.

The court takes Pass 38 investigation candidates and narrows them into one of
three states:

* SUPPORTED_NARROWLY - a limited factual statement is directly supported by an
  already-verified atomic meaning event.
* QUESTION_ONLY - the text supports asking a question, but not yet making the
  implied substantive claim.
* HOLD - evidence is missing, malformed, or too weak even for the proposed
  investigation framing.

No satire, motive attribution, corruption claim, winner/loser claim, or causal
claim can be introduced here. The court exists to reduce claims, not embellish
them.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass
class CourtOpinion:
    candidate_id: str
    bill_id: str
    section: str
    section_heading: str
    category: str
    source_start_line: int
    source_end_line: int
    evidence_excerpt: str
    prosecutor: str
    defense: str
    progressive_reading: str
    conservative_reading: str
    text_referee: str
    citation_referee: str
    verdict: str
    allowed_public_statement: str | None
    allowed_public_question: str | None
    forbidden_inferences: list[str]
    unresolved_context: list[str]
    confidence: float


def _money_statement(c: dict[str, Any]) -> str | None:
    why = c.get("why_human_might_care", "")
    marker = "This verified before/after event changes "
    if not why.startswith(marker):
        return None
    # Pass 38 already generated this from a publishable atomic meaning event.
    body = why[len(marker):]
    if ", large enough" in body:
        body = body.split(", large enough", 1)[0]
    if " from " not in body or " to " not in body:
        return None
    return f"The bill changes {body}."


def _views(category: str) -> tuple[str, str]:
    if category == "large_before_after_change":
        return (
            "A progressive reader may ask who receives the benefit, who is left out, and how the change is distributed across households or income groups.",
            "A conservative reader may ask whether the change reduces tax burdens, changes incentives, or simplifies an existing rule, and what it costs or saves.",
        )
    if category == "delegated_authority":
        return (
            "A progressive reader may ask whether agency discretion is needed to administer a complex rule fairly and consistently.",
            "A conservative reader may ask whether Congress delegated too much policy choice to unelected officials.",
        )
    if category == "override":
        return (
            "A progressive reader may ask whether the override prevents an older rule from frustrating the new policy goal.",
            "A conservative reader may ask why an ordinary rule was displaced and whether the exception expands government power or complexity.",
        )
    if category == "exception":
        return (
            "A progressive reader may ask whether the exception prevents unfair treatment of an edge case or vulnerable group.",
            "A conservative reader may ask whether the exception creates unequal treatment, complexity, or a special carve-out.",
        )
    if category == "temporary_or_transition":
        return (
            "A progressive reader may ask whether the temporary period protects people during a transition or reflects budget constraints.",
            "A conservative reader may ask whether a temporary rule hides the long-run policy choice or creates uncertainty.",
        )
    return (
        "A progressive reader may ask who is protected, excluded, or burdened by the boundary Congress drew.",
        "A conservative reader may ask whether the boundary is administrable, neutral, and justified rather than arbitrary or preferential.",
    )


def adjudicate(c: dict[str, Any]) -> CourtOpinion:
    category = c.get("category", "")
    evidence = (c.get("evidence_excerpt") or "").strip()
    start = int(c.get("source_start_line") or 0)
    end = int(c.get("source_end_line") or 0)
    question = (c.get("question_to_investigate") or "").strip() or None
    ordinary = " ".join(c.get("ordinary_explanations") or [])
    uncertainties = list(c.get("uncertainty") or [])
    progressive, conservative = _views(category)

    forbidden = [
        "motive or intent not stated in evidence",
        "corruption, favoritism, waste, or deception without independent proof",
        "budget cost, beneficiary count, or distributional effect not established here",
        "causal claims about real-world outcomes not established by the statutory excerpt",
    ]

    if not evidence or start <= 0 or end < start:
        return CourtOpinion(
            candidate_id=c.get("candidate_id", ""), bill_id=c.get("bill_id", ""),
            section=c.get("section", ""), section_heading=c.get("section_heading", ""),
            category=category, source_start_line=start, source_end_line=end,
            evidence_excerpt=evidence,
            prosecutor="The candidate cannot be tested responsibly because its source evidence is incomplete or malformed.",
            defense=ordinary or "No defense can be evaluated without a valid source excerpt.",
            progressive_reading=progressive, conservative_reading=conservative,
            text_referee="The text record is insufficient for adjudication.",
            citation_referee="HOLD: no valid line-bounded evidence packet.",
            verdict="HOLD", allowed_public_statement=None, allowed_public_question=None,
            forbidden_inferences=forbidden, unresolved_context=uncertainties + ["Repair the evidence packet before further use."], confidence=0.25,
        )

    if c.get("source_basis") == "verified_atomic_meaning_event" and category == "large_before_after_change":
        statement = _money_statement(c)
        if statement:
            return CourtOpinion(
                candidate_id=c["candidate_id"], bill_id=c.get("bill_id", ""), section=c.get("section", ""),
                section_heading=c.get("section_heading", ""), category=category,
                source_start_line=start, source_end_line=end, evidence_excerpt=evidence,
                prosecutor=f"The verified before/after change is large enough to deserve explanation: {statement}",
                defense=ordinary or "Size alone does not establish importance, fairness, cost, or motive.",
                progressive_reading=progressive, conservative_reading=conservative,
                text_referee="The narrow numerical change is supported because it came from a publishable atomic meaning event. Broader consequence claims are not supported here.",
                citation_referee=f"SUPPORTED for the narrow before/after statement at source lines {start}-{end}; broader claims require additional evidence.",
                verdict="SUPPORTED_NARROWLY", allowed_public_statement=statement,
                allowed_public_question=question, forbidden_inferences=forbidden,
                unresolved_context=uncertainties, confidence=0.93,
            )

    # Text-signal categories identify grammar or wording worth tracing, but do not
    # prove the real-world consequence until referenced rules/context are resolved.
    return CourtOpinion(
        candidate_id=c["candidate_id"], bill_id=c.get("bill_id", ""), section=c.get("section", ""),
        section_heading=c.get("section_heading", ""), category=category,
        source_start_line=start, source_end_line=end, evidence_excerpt=evidence,
        prosecutor=c.get("why_human_might_care", "This wording may deserve closer investigation."),
        defense=ordinary or "There may be an ordinary drafting or administrative explanation that has not yet been reconstructed.",
        progressive_reading=progressive, conservative_reading=conservative,
        text_referee="The excerpt supports noticing the drafting construct and asking the investigation question. It does not yet prove the substantive consequence implied by that question.",
        citation_referee=f"QUESTION ONLY: source lines {start}-{end} support the observed wording, not a broader public claim.",
        verdict="QUESTION_ONLY", allowed_public_statement=None,
        allowed_public_question=question, forbidden_inferences=forbidden,
        unresolved_context=uncertainties + ["Resolve referenced law, definitions, scope, and practical effect before promoting this to a factual claim."],
        confidence=0.88,
    )


def run_court(queue_path: Path, out_path: Path, limit: int = 40) -> dict[str, Any]:
    queue = json.loads(queue_path.read_text(encoding="utf-8"))
    candidates = queue.get("candidates", [])[:limit]
    opinions = [adjudicate(c) for c in candidates]
    counts: dict[str, int] = {}
    for o in opinions:
        counts[o.verdict] = counts.get(o.verdict, 0) + 1
    payload = {
        "schema_version": "39.0",
        "bill_id": queue.get("bill_id", ""),
        "doctrine": "adversarial_narrowing_before_story",
        "opinion_count": len(opinions),
        "verdict_counts": dict(sorted(counts.items())),
        "public_statements_allowed": sum(bool(o.allowed_public_statement) for o in opinions),
        "question_only_count": sum(o.verdict == "QUESTION_ONLY" for o in opinions),
        "guardrail": "The Truth Court may narrow or block claims. It may not invent facts, motives, consequences, or jokes.",
        "opinions": [asdict(o) for o in opinions],
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--queue", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--limit", type=int, default=40)
    args = ap.parse_args()
    payload = run_court(args.queue, args.out, args.limit)
    print(
        f"PASS 39: adjudicated {payload['opinion_count']} candidates; "
        f"{payload['public_statements_allowed']} narrow statements allowed; "
        f"{payload['question_only_count']} remain question-only"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
