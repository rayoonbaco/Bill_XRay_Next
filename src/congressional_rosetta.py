"""Congressional Rosetta Grammar for Bill X-Ray Next.

PASS 37 recognizes recurring legislative grammar and records what each construct
*does* before any writer is allowed to turn it into public prose. Grammar is not
meaning by itself: every hit carries the context still required to make a safe
human claim.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class GrammarRule:
    rule_id: str
    name: str
    pattern: str
    legal_function: str
    human_operation: str
    context_requirements: tuple[str, ...]
    public_claim_from_grammar_alone: bool = False
    priority: int = 50


@dataclass
class GrammarHit:
    bill_id: str
    hit_id: str
    rule_id: str
    rule_name: str
    source_line: int
    section: str
    matched_text: str
    legal_function: str
    human_operation: str
    context_required: list[str]
    public_claim_allowed: bool
    confidence: float


RULES: tuple[GrammarRule, ...] = (
    GrammarRule(
        "delegated_rulemaking",
        "delegated rulemaking",
        r"\b(?:Secretary|Administrator|Commission|Board|agency)\s+shall\s+(?:prescribe|promulgate)\b",
        "Congress requires an executive actor to write implementing rules.",
        "An agency or official must write the detailed rules that make this part work.",
        ("Identify the official or agency.", "Identify what the future rules are allowed or required to decide."),
        priority=100,
    ),
    GrammarRule(
        "delegated_determination",
        "delegated determination",
        r"\b(?:Secretary|Administrator|Commission|Board|agency)\s+shall\s+determine\b",
        "Congress assigns a decision to an executive actor.",
        "An agency or official gets the job of deciding a specified question.",
        ("Identify the decision being delegated.", "Identify any standards or limits Congress placed on that decision."),
        priority=95,
    ),
    GrammarRule(
        "strike_insert",
        "strike and insert amendment",
        r"\bstrik(?:e|ing)\b.{0,180}?\binsert(?:ing)?\b",
        "The bill edits existing law by removing old text and replacing or adding new text.",
        "Congress changes an existing rule rather than stating the whole new rule from scratch.",
        ("Retrieve the pre-amendment text.", "Resolve what the edited words or numbers mean in their statutory context."),
        priority=90,
    ),
    GrammarRule(
        "notwithstanding",
        "override clause",
        r"\bnotwithstanding\b",
        "This clause operates despite another rule that would otherwise apply.",
        "This rule overrides another rule for the situation described here.",
        ("Identify the rule being overridden.", "Determine the scope and duration of the override."),
        priority=85,
    ),
    GrammarRule(
        "subject_to",
        "subject-to condition",
        r"\bsubject\s+to\b",
        "This rule is subordinate to, limited by, or conditioned on another rule.",
        "This only works within the limits of another rule.",
        ("Identify the controlling rule or condition.", "Determine what happens if the condition is not met."),
        priority=80,
    ),
    GrammarRule(
        "except_as_provided",
        "exception cross-reference",
        r"\bexcept\s+as\s+provided\b",
        "The apparent rule has an exception defined elsewhere.",
        "There is an exception, and the reader must follow it before treating this as the whole rule.",
        ("Locate the referenced exception.", "Determine who or what the exception removes from the general rule."),
        priority=80,
    ),
    GrammarRule(
        "treated_as",
        "legal classification",
        r"\bshall\s+(?:not\s+)?be\s+treated\s+as\b|\bis\s+(?:not\s+)?treated\s+as\b",
        "The statute assigns a legal classification that may differ from ordinary-language identity.",
        "For this law, Congress tells us to count something as—or not as—something else.",
        ("Identify the thing being classified.", "Identify the legal category and the consequences of that classification."),
        priority=78,
    ),
    GrammarRule(
        "deemed",
        "deeming rule",
        r"\b(?:shall\s+be|is)\s+deemed\b",
        "The statute creates a legal assumption or status for a defined purpose.",
        "The law tells us to treat a fact or status as legally true for this purpose.",
        ("Identify what is being deemed true.", "Identify the purpose and downstream legal consequence."),
        priority=77,
    ),
    GrammarRule(
        "for_purposes_of",
        "local scope definition",
        r"\bfor\s+purposes\s+of\b",
        "The statement defines or modifies meaning only within a specified statutory scope.",
        "This definition or rule applies only in the part of the law named here.",
        ("Identify the exact scope.", "Do not generalize the definition outside that scope."),
        priority=70,
    ),
    GrammarRule(
        "effective_date",
        "effective date",
        r"\beffective\s+date\b|\bshall\s+apply\s+to\b|\bafter\s+December\s+31,\s*\d{4}\b",
        "The statute specifies when a change begins to govern conduct, transactions, or tax years.",
        "This tells us when the change starts applying.",
        ("Resolve the affected transactions, conduct, or tax years.", "Check for separate transition or expiration rules."),
        priority=65,
    ),
    GrammarRule(
        "redesignate",
        "redesignation",
        r"\bredesignat(?:e|ed|ing)\b",
        "The statute renumbers or relabels existing provisions.",
        "Congress is moving a label or number; that may be bookkeeping rather than a policy change by itself.",
        ("Trace the moved provision so later cross-references still point to the right text.",),
        priority=60,
    ),
    GrammarRule(
        "authorization",
        "authorization",
        r"\bauthoriz(?:e|es|ed|ation)\b.{0,100}?\b(?:appropriat|amount|sum|fund|program)\b",
        "Congress permits or establishes spending authority, which is not necessarily the same as cash already appropriated.",
        "Congress is allowing money to be provided or a program to be funded; that does not automatically mean the cash has been handed over.",
        ("Distinguish authorization from appropriation.", "Identify amount, period, recipient, and conditions."),
        priority=72,
    ),
    GrammarRule(
        "appropriation",
        "appropriation",
        r"\b(?:appropriat(?:e|ed|ion)|amounts?\s+appropriated)\b",
        "Congress provides or refers to budget authority for spending.",
        "This is about money Congress makes available to spend, subject to the exact wording and conditions.",
        ("Identify whether the text actually provides budget authority or merely references an appropriation.", "Identify amount, availability period, recipient, and purpose."),
        priority=73,
    ),
)

COMPILED = tuple((rule, re.compile(rule.pattern, re.I | re.S)) for rule in RULES)
SECTION_RE = re.compile(r"^SEC\.\s+([0-9A-Z.-]+)\.")


def _section_by_line(lines: list[str]) -> list[str]:
    current = ""
    result: list[str] = []
    for line in lines:
        m = SECTION_RE.match(line.strip())
        if m:
            current = "SEC. " + m.group(1)
        result.append(current)
    return result


def scan_lines(lines: list[str], bill_id: str) -> list[GrammarHit]:
    sections = _section_by_line(lines)
    text = "\n".join(lines)
    hits: list[GrammarHit] = []
    candidates: list[tuple[int, int, GrammarRule, re.Match[str]]] = []
    for rule, rx in COMPILED:
        for match in rx.finditer(text):
            candidates.append((match.start(), -rule.priority, rule, match))
    for _, _, rule, match in sorted(candidates):
        line_no = text.count("\n", 0, match.start()) + 1
        matched = re.sub(r"\s+", " ", match.group(0)).strip()
        hits.append(
            GrammarHit(
                bill_id=bill_id,
                hit_id=f"{bill_id}:{match.start()}:{rule.rule_id}",
                rule_id=rule.rule_id,
                rule_name=rule.name,
                source_line=line_no,
                section=sections[line_no - 1] if sections else "",
                matched_text=matched,
                legal_function=rule.legal_function,
                human_operation=rule.human_operation,
                context_required=list(rule.context_requirements),
                public_claim_allowed=rule.public_claim_from_grammar_alone,
                confidence=0.96,
            )
        )
    return hits


def scan_file(path: Path, bill_id: str) -> list[GrammarHit]:
    return scan_lines(path.read_text(encoding="utf-8").splitlines(), bill_id)


def grammar_catalog() -> list[dict]:
    return [asdict(rule) for rule in RULES]


def write_payload(source: Path, bill_id: str, out: Path) -> dict:
    hits = scan_file(source, bill_id)
    counts: dict[str, int] = {}
    for hit in hits:
        counts[hit.rule_id] = counts.get(hit.rule_id, 0) + 1
    payload = {
        "schema_version": "37.0",
        "bill_id": bill_id,
        "doctrine": "grammar_before_claim",
        "rule_count": len(RULES),
        "hit_count": len(hits),
        "public_claims_allowed_from_grammar_alone": sum(h.public_claim_allowed for h in hits),
        "rule_counts": dict(sorted(counts.items())),
        "rules": grammar_catalog(),
        "hits": [asdict(hit) for hit in hits],
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def explain_text(text: str) -> list[GrammarHit]:
    return scan_lines([text], "sample")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("--bill-id", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    payload = write_payload(Path(args.source), args.bill_id, Path(args.out))
    print(
        f"PASS 37: recognized {payload['hit_count']} grammar uses across "
        f"{len(payload['rule_counts'])} construct types; "
        f"{payload['public_claims_allowed_from_grammar_alone']} public claims allowed from grammar alone"
    )


if __name__ == "__main__":
    main()
