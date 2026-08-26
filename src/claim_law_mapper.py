"""PASS 42 - Claim vs. Law Mapper.

Bill X-Ray separates rhetoric from statute. A public claim is decomposed into
legal promises, then compared with court-cleared or directly verified statutory
mechanisms. The mapper does not issue a simplistic TRUE/FALSE label when the
law alone cannot support one.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class LawEvidence:
    evidence_id: str
    section: str
    relationship: str
    law_says: str
    why_it_matters: str
    evidence_excerpt: str
    limits: list[str]
    source_path: str


@dataclass
class ClaimClause:
    clause_id: str
    plain_claim: str
    legal_test: str
    status: str
    explanation: str
    evidence_ids: list[str]


def _excerpt(text: str, anchor: str, span: int = 460) -> str:
    idx = text.find(anchor)
    if idx < 0:
        raise ValueError(f"Required statutory anchor not found: {anchor}")
    start = max(0, idx - 80)
    end = min(len(text), idx + span)
    return " ".join(text[start:end].split())


def build_aca_doctor_map(claim_path: Path, law_path: Path) -> dict:
    claim = json.loads(claim_path.read_text(encoding="utf-8"))
    text = law_path.read_text(encoding="utf-8")

    evidence = [
        LawEvidence(
            "aca_existing_coverage",
            "SEC. 1251",
            "QUALIFIES",
            "The Act says it must not be read to require a person to terminate health coverage they had on the date of enactment, and it creates grandfathered treatment for qualifying existing coverage.",
            "This protects continuity from a command in the Act itself, but it is a rule about coverage, not a guarantee that a particular physician stays available.",
            _excerpt(text, "Nothing in this Act"),
            [
                "It does not say an insurer, employer, or doctor can never change or end an arrangement.",
                "Keeping a health plan and keeping a particular doctor are different legal questions.",
            ],
            str(law_path),
        ),
        LawEvidence(
            "aca_participating_primary_care_choice",
            "PHS Act SEC. 2719A(a), added by ACA",
            "PARTIALLY_SUPPORTS",
            "When a plan uses a participating-primary-care-provider designation, it must let an enrollee choose any participating primary care provider who is available to accept that person.",
            "The statute protects choice inside the participating network. The words participating and available are conditions.",
            _excerpt(text, "shall permit each participant"),
            [
                "This does not require a specific doctor to participate in the plan's network.",
                "This does not require a doctor to remain available or continue accepting a patient.",
            ],
            str(law_path),
        ),
        LawEvidence(
            "aca_network_choice",
            "ACA SEC. 1311(c)(1)(B)",
            "PARTIALLY_SUPPORTS",
            "Qualified health plans must ensure a sufficient choice of providers and tell enrollees about in-network and out-of-network provider availability.",
            "The law requires meaningful provider choice, but sufficient choice is not the same as a guarantee of one named physician.",
            _excerpt(text, "ensure a sufficient choice of providers"),
            ["Network-adequacy protection does not itself promise that every existing doctor will remain in every network."],
            str(law_path),
        ),
    ]

    clauses = [
        ClaimClause(
            "keep_specific_doctor",
            "A person who likes a particular doctor will be able to keep that doctor under the reform.",
            "Does the statute create an unconditional right to continue using the same specific physician?",
            "NOT_ESTABLISHED_AS_UNCONDITIONAL_GUARANTEE",
            "The reviewed provisions protect provider choice within participating networks and preserve certain existing coverage, but they contain conditions and do not create an unconditional guarantee that one specific doctor will remain participating and available.",
            ["aca_participating_primary_care_choice", "aca_network_choice", "aca_existing_coverage"],
        ),
        ClaimClause(
            "reform_does_not_force_plan_termination",
            "The reform itself will not force a person to terminate qualifying existing coverage.",
            "Does the Act itself require people enrolled at enactment to terminate that coverage?",
            "SUPPORTED_WITH_SCOPE_LIMITS",
            "Section 1251 says the Act must not be construed to require termination of coverage held on the date of enactment, subject to the grandfathered-coverage framework.",
            ["aca_existing_coverage"],
        ),
        ClaimClause(
            "meaningful_provider_choice",
            "The law protects a person's ability to choose a doctor rather than assigning one specific doctor to them.",
            "Does the law require some provider choice?",
            "SUPPORTED_WITH_CONDITIONS",
            "The law protects choice among participating primary care providers who are available and requires qualified plans to ensure a sufficient choice of providers.",
            ["aca_participating_primary_care_choice", "aca_network_choice"],
        ),
    ]

    verdict = {
        "classification": "CLAIM_BROADER_THAN_STATUTORY_GUARANTEE",
        "short": "The law protects provider choice and some existing coverage, but the reviewed provisions do not guarantee that every person can keep one specific doctor regardless of network participation or availability.",
        "not_a_verdict_on": [
            "Whether particular people later kept or lost doctors in practice.",
            "Whether later regulations, contracts, insurer decisions, employer decisions, or market changes caused a doctor relationship to continue or end.",
            "The speaker's motive or intent.",
        ],
    }

    payload = {
        "schema_version": "42",
        "bill_id": "ACA",
        "claim": claim,
        "claim_clauses": [asdict(x) for x in clauses],
        "law_evidence": [asdict(x) for x in evidence],
        "verdict": verdict,
        "public_render": {
            "headline": "THEY SAID THIS",
            "claim": claim["claim"],
            "law_answer": verdict["short"],
            "what_the_law_does_protect": [
                "Certain existing coverage is protected from being terminated merely because the Act requires it.",
                "Where a plan uses a participating primary care provider, the enrollee may choose any participating provider who is available to accept them.",
                "Qualified plans must provide a sufficient choice of providers.",
            ],
            "what_the_law_does_not_establish": [
                "An unconditional right to one particular doctor forever.",
                "A requirement that a particular doctor remain in a particular insurer's network.",
                "A promise that market or contractual relationships outside the statutory guarantee will never change.",
            ],
            "human_conclusion": "The political sentence is simpler and broader than the statutory machinery. The law protects choice, but it protects choice through conditions such as participating networks and provider availability. Bill X-Ray should show that gap rather than stamp TRUE or FALSE on it.",
        },
        "guardrails": [
            "Political rhetoric and statutory text are separate evidence lanes.",
            "No TRUE/FALSE label when the statute supports only a qualified comparison.",
            "Absence of an unconditional guarantee in the reviewed provisions is not proof of later real-world outcomes.",
            "Do not infer motive, deception, fraud, or intent from a mismatch between rhetoric and legal mechanism.",
        ],
        "release_readiness": "CLAIM_MAP_READY_FOR_HUMAN_GATE",
    }
    return payload


def build_tcja_child_credit_map(coverage_path: Path) -> dict:
    data = json.loads(coverage_path.read_text(encoding="utf-8"))
    facts = {x["fact_id"]: x for x in data["facts"] if x.get("status") == "COURT_CLEARED_DIRECT"}
    required = ["child_credit_amount", "refundable_cap", "child_ssn"]
    missing = [x for x in required if x not in facts]
    if missing:
        raise ValueError(f"Missing cleared TCJA facts: {missing}")
    return {
        "schema_version": "42",
        "bill_id": "TCJA",
        "claim": {"claim": "The child tax credit is $2,000.", "source_type": "headline_test_claim"},
        "verdict": {
            "classification": "SUPPORTED_BUT_INCOMPLETE",
            "short": "The law raises the headline child-credit amount to $2,000 for the temporary period, but that number does not by itself describe refundability or eligibility conditions.",
        },
        "support_fact_ids": required,
        "public_render": {
            "claim": "The child tax credit is $2,000.",
            "law_answer": "Yes as a headline amount, but the law also caps the refundable portion at $1,400 under those temporary rules and requires the qualifying child's Social Security number for the credit.",
        },
    }


def build_pass42(claim_path: Path, aca_law_path: Path, tcja_coverage_path: Path, out_path: Path) -> dict:
    payload = {
        "schema_version": "42",
        "doctrine": "Do not decide whether rhetoric is true by keyword matching. Decompose the claim, reconstruct the legal promise it would require, compare that promise with verified statutory mechanisms, and preserve what the statute cannot answer.",
        "aca_keep_doctor": build_aca_doctor_map(claim_path, aca_law_path),
        "tcja_child_credit": build_tcja_child_credit_map(tcja_coverage_path),
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--claim", type=Path, required=True)
    ap.add_argument("--aca-law", type=Path, required=True)
    ap.add_argument("--tcja-coverage", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    p = build_pass42(a.claim, a.aca_law, a.tcja_coverage, a.out)
    a1 = p["aca_keep_doctor"]
    t1 = p["tcja_child_credit"]
    print("PASS 42 CLAIM VS LAW")
    print(f"ACA doctor claim: {a1['verdict']['classification']}")
    print(f"TCJA child-credit claim: {t1['verdict']['classification']}")
    print(f"readiness={a1['release_readiness']}")


if __name__ == "__main__":
    main()
