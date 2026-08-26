"""PASS 42.1 - Reality Stack.

A statute is only one layer of policy reality. This module keeps political
rhetoric, enacted law, agency implementation, court interpretation, official
analysis, observed outcomes, and secondary commentary as separate evidence
lanes. It is designed to prevent a later fact, regulation, or market outcome
from being silently rewritten into the original statute.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


LANE_ORDER = [
    "RHETORIC",
    "ENACTED_LAW",
    "IMPLEMENTATION",
    "COURT_INTERPRETATION",
    "OFFICIAL_ANALYSIS",
    "OBSERVED_OUTCOME",
    "SECONDARY_INTERPRETATION",
]


@dataclass
class RealityLane:
    lane: str
    question: str
    status: str
    source_ids: list[str]
    safe_conclusion: str
    cannot_conclude: list[str]


def _index_sources(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for source in registry.get("sources", []):
        sid = source.get("source_id")
        if not sid:
            raise ValueError("Every reality-stack source must have source_id")
        if sid in out:
            raise ValueError(f"Duplicate source_id: {sid}")
        lane = source.get("lane")
        if lane not in LANE_ORDER:
            raise ValueError(f"Unknown evidence lane: {lane}")
        if not source.get("supported_meaning"):
            raise ValueError(f"Source {sid} lacks supported_meaning")
        if not source.get("publisher"):
            raise ValueError(f"Source {sid} lacks publisher")
        if not (source.get("url") or source.get("local_source")):
            raise ValueError(f"Source {sid} lacks a retrievable locator")
        out[sid] = source
    return out


def _lane_sources(source_index: dict[str, dict[str, Any]], lane: str) -> list[str]:
    return [sid for sid, src in source_index.items() if src["lane"] == lane]


def _empty_status(registry: dict[str, Any], lane: str) -> dict[str, str] | None:
    for row in registry.get("empty_lanes", []):
        if row.get("lane") == lane:
            return row
    return None


def build_aca_reality_stack(claim_map: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    source_index = _index_sources(registry)
    claim = claim_map["aca_keep_doctor"]

    lanes = [
        RealityLane(
            "RHETORIC",
            "What was the public actually told?",
            "EVIDENCE_LOADED",
            _lane_sources(source_index, "RHETORIC"),
            "The public promise was broad: people who liked their doctors and health plans were told they would be able to keep them.",
            ["Whether the promise was legally guaranteed", "Whether later implementation fulfilled it", "Speaker motive or intent"],
        ),
        RealityLane(
            "ENACTED_LAW",
            "What did Congress actually enact?",
            "EVIDENCE_LOADED",
            _lane_sources(source_index, "ENACTED_LAW"),
            claim["verdict"]["short"],
            ["Later regulatory choices", "Later market behavior", "A universal real-world outcome for every patient"],
        ),
        RealityLane(
            "IMPLEMENTATION",
            "How did agencies turn the statute into operating rules?",
            "EVIDENCE_LOADED",
            _lane_sources(source_index, "IMPLEMENTATION"),
            "CMS implementation focused on network adequacy and access standards, and those standards evolved over time. That regulates network sufficiency; it still does not convert the statute into a guarantee that one named doctor must remain in every plan network.",
            ["That agency rules preserved every preexisting doctor relationship", "That later rules describe the statute's original text"],
        ),
        RealityLane(
            "COURT_INTERPRETATION",
            "Did a court materially reinterpret this issue?",
            "NO_SOURCE_LOADED",
            [],
            "No court interpretation is being used in this Pass 42.1 example.",
            ["That no relevant case exists", "That courts agreed with any political or administrative interpretation"],
        ),
        RealityLane(
            "OFFICIAL_ANALYSIS",
            "What did official reviewers later find?",
            "EVIDENCE_LOADED",
            _lane_sources(source_index, "OFFICIAL_ANALYSIS"),
            "GAO later documented concerns about obtaining or continuing care as narrow networks became more prevalent in exchange coverage and summarized evidence that exchange networks could include fewer providers than plans outside the exchanges.",
            ["That every exchange enrollee lost provider access", "That the statute alone caused the observed network pattern"],
        ),
        RealityLane(
            "OBSERVED_OUTCOME",
            "What happened in the operating market?",
            "EVIDENCE_LOADED",
            _lane_sources(source_index, "OBSERVED_OUTCOME"),
            "GAO reported that some issuers narrowed provider networks over time, with selected issuers describing cost management and competitive pricing as reasons for doing so.",
            ["That every issuer narrowed networks", "That every narrow network was caused by the ACA", "That a particular person lost a particular doctor"],
        ),
        RealityLane(
            "SECONDARY_INTERPRETATION",
            "How did journalists, scholars, advocates, and critics interpret the record?",
            "INTENTIONALLY_HELD",
            [],
            "Secondary commentary is not used in the initial Pass 42.1 gate. The architecture supports it, but later versions must label source perspective and keep commentary subordinate to primary evidence.",
            ["That secondary sources are unnecessary", "That later commentary should be treated as equivalent to enacted law"],
        ),
    ]

    loaded = {lane.lane: lane.source_ids for lane in lanes if lane.source_ids}
    if not loaded.get("RHETORIC") or not loaded.get("ENACTED_LAW") or not loaded.get("IMPLEMENTATION"):
        raise ValueError("Reality stack requires rhetoric, enacted-law, and implementation lanes for this example")

    gap_analysis = {
        "public_claim": claim["public_render"]["claim"],
        "claim_vs_law": claim["verdict"]["classification"],
        "law_vs_implementation": "IMPLEMENTATION_ADDS_OPERATING_STANDARDS_WITHOUT_CREATING_SPECIFIC_DOCTOR_GUARANTEE",
        "implementation_vs_outcome": "NETWORK_ADEQUACY_RULES_COEXIST_WITH_REPORTED_NARROW_NETWORK_CONCERNS",
        "causation_status": "NOT_ESTABLISHED_BY_THIS_STACK",
        "why": "The sources support a broad public promise, a narrower conditional statutory mechanism, agency network-adequacy rules, and later official evidence of narrow-network concerns. They do not establish one simple causal chain from statute to every person's doctor relationship.",
    }

    public_answer = {
        "headline": "WHAT THEY SAID / WHAT THE LAW DID / WHAT HAPPENED",
        "rhetoric": lanes[0].safe_conclusion,
        "law": lanes[1].safe_conclusion,
        "implementation": lanes[2].safe_conclusion,
        "official_review": lanes[4].safe_conclusion,
        "observed_outcome": lanes[5].safe_conclusion,
        "bottom_line": (
            "The promise was broader than the statutory guarantee. The law protected provider choice through conditions such as participation and availability; regulators then policed network adequacy rather than guaranteeing one specific doctor. Later official reviews found real concerns about narrow networks and continuing access. That is enough to show a gap between slogan, legal mechanism, and operating reality - but not enough to say the ACA alone caused any particular person to lose a doctor."
        ),
    }

    guardrails = [
        "Never rewrite an implementation rule into the enacted statute.",
        "Never rewrite a later market outcome into the speaker's original intent.",
        "Never flatten source authority: statute, regulation, GAO review, journalism, and advocacy are different evidence objects.",
        "A missing lane means not loaded, not nonexistent.",
        "Observed correlation or market experience is not automatic proof of statutory causation.",
        "When sources disagree, preserve the disagreement and source provenance instead of averaging it into false certainty.",
    ]

    return {
        "schema_version": "42.1",
        "bill_id": "ACA",
        "topic": "keep-your-doctor claim",
        "source_registry": registry,
        "lanes": [asdict(x) for x in lanes],
        "gap_analysis": gap_analysis,
        "public_answer": public_answer,
        "guardrails": guardrails,
        "release_readiness": "REALITY_STACK_READY_FOR_HUMAN_GATE",
    }


def build_pass421(claim_map_path: Path, registry_path: Path, out_path: Path) -> dict[str, Any]:
    claim_map = json.loads(claim_map_path.read_text(encoding="utf-8"))
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    payload = build_aca_reality_stack(claim_map, registry)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--claim-map", type=Path, required=True)
    ap.add_argument("--registry", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    payload = build_pass421(a.claim_map, a.registry, a.out)
    print("PASS 42.1 REALITY STACK")
    for lane in payload["lanes"]:
        print(f"{lane['lane']}: {lane['status']} ({len(lane['source_ids'])} sources)")
    print(f"readiness={payload['release_readiness']}")


if __name__ == "__main__":
    main()
