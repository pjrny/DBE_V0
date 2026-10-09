"""SDBES V7 Observatory-scale integrity and consistency checks.

V7 deliberately separates corpus profiling from scientific adjudication.  A
paper can be inventoried, reviewed, and associated with a program claim
without automatically strengthening that claim.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable


ALLOWED_ACTIONS = {"HOLD", "REJECT", "INCLUDE", "NEW PILLAR"}
ALLOWED_ROUTES = {"QUEUE", "AUTO-MERGED", "REJECT"}
ALLOWED_GATE_STATES = {"pass", "fail", "partial", "unknown", None}
PROGRAM_CLAIM_ID = re.compile(r"^(?:E-[A-Z0-9]+|S-(?:Q|L\d+))$")


@dataclass(frozen=True)
class V7Finding:
    code: str
    severity: str
    path: str
    message: str


def _duplicates(values: Iterable[str]) -> list[str]:
    counts = Counter(values)
    return sorted(value for value, count in counts.items() if count > 1)


def _normal_title(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def validate_observatory(
    catalog: dict[str, Any],
    reviews: dict[str, Any],
    claims: dict[str, Any],
    ledger: dict[str, Any],
) -> list[V7Finding]:
    """Return data-quality findings without hiding known source defects."""

    findings: list[V7Finding] = []
    papers = catalog.get("papers", [])
    cards = reviews.get("cards", [])
    program_claims = claims.get("claims", [])
    paper_ids = [str(item.get("id", "")) for item in papers]
    card_ids = [str(item.get("id", "")) for item in cards]
    claim_ids = [str(item.get("id", "")) for item in program_claims]
    paper_set = set(paper_ids)
    claim_set = set(claim_ids)

    for value in _duplicates(paper_ids):
        findings.append(V7Finding("DUPLICATE_PAPER_ID", "HIGH", "catalog.papers", value))
    for value in _duplicates(card_ids):
        findings.append(V7Finding("DUPLICATE_REVIEW_ID", "HIGH", "reviews.cards", value))
    for value in _duplicates(claim_ids):
        findings.append(V7Finding("DUPLICATE_PROGRAM_CLAIM_ID", "HIGH", "claims.claims", value))

    for index, paper in enumerate(papers):
        path = f"catalog.papers[{index}]"
        if not paper.get("id") or not paper.get("title") or not paper.get("url"):
            findings.append(V7Finding("INCOMPLETE_PAPER_IDENTITY", "HIGH", path, "id, title, and url are required"))
        refs = paper.get("claimIds", [])
        for ref in refs:
            if ref not in claim_set and ref != "REJECT":
                findings.append(V7Finding("UNRESOLVED_PAPER_CLAIM_REF", "HIGH", f"{path}.claimIds", str(ref)))

    missing_source_tier = sum(not paper.get("sourceTier") for paper in papers)
    if missing_source_tier:
        findings.append(V7Finding(
            "MISSING_SOURCE_TIER",
            "MEDIUM",
            "catalog.papers[*].sourceTier",
            f"{missing_source_tier} of {len(papers)} records lack a source-tier classification",
        ))

    for index, card in enumerate(cards):
        path = f"reviews.cards[{index}]"
        if str(card.get("paperId", "")) not in paper_set:
            findings.append(V7Finding("REVIEW_WITHOUT_CATALOG_PAPER", "HIGH", f"{path}.paperId", str(card.get("paperId"))))
        if card.get("action") not in ALLOWED_ACTIONS:
            findings.append(V7Finding("INVALID_REVIEW_ACTION", "HIGH", f"{path}.action", str(card.get("action"))))
        if card.get("route") not in ALLOWED_ROUTES:
            findings.append(V7Finding("INVALID_REVIEW_ROUTE", "HIGH", f"{path}.route", str(card.get("route"))))
        for ref in card.get("bind", []):
            if ref not in claim_set and ref != "REJECT":
                findings.append(V7Finding("UNRESOLVED_REVIEW_CLAIM_REF", "HIGH", f"{path}.bind", str(ref)))
        for gate, state in card.get("gates", {}).items():
            if gate == "note":
                continue
            if state not in ALLOWED_GATE_STATES:
                findings.append(V7Finding("INVALID_GATE_STATE", "MEDIUM", f"{path}.gates.{gate}", str(state)))

    for index, claim in enumerate(program_claims):
        if not PROGRAM_CLAIM_ID.match(str(claim.get("id", ""))):
            findings.append(V7Finding("INVALID_PROGRAM_CLAIM_ID", "HIGH", f"claims.claims[{index}].id", str(claim.get("id"))))

    normalized_titles: dict[str, list[str]] = {}
    for paper in papers:
        normalized_titles.setdefault(_normal_title(str(paper.get("title", ""))), []).append(str(paper.get("id", "")))
    for title, ids in sorted(normalized_titles.items()):
        if title and len(ids) > 1:
            findings.append(V7Finding("POSSIBLE_DUPLICATE_TITLE", "MEDIUM", "catalog.papers", ", ".join(ids)))

    if not ledger.get("terms") or not ledger.get("definitions"):
        findings.append(V7Finding("INCOMPLETE_LEDGER", "HIGH", "ledger", "definitions and terms are required"))
    return findings


def _counter(records: Iterable[dict[str, Any]], key: str) -> dict[str, int]:
    values = ("UNSPECIFIED" if record.get(key) in (None, "") else str(record.get(key)) for record in records)
    return dict(sorted(Counter(values).items()))


def build_stress_report(
    catalog: dict[str, Any],
    reviews: dict[str, Any],
    claims: dict[str, Any],
    ledger: dict[str, Any],
    snapshot: dict[str, Any],
) -> dict[str, Any]:
    papers = catalog["papers"]
    cards = reviews["cards"]
    program_claims = claims["claims"]
    findings = validate_observatory(catalog, reviews, claims, ledger)
    paper_ids = {str(item["id"]) for item in papers}
    reviewed_paper_ids = {str(item["paperId"]) for item in cards if str(item.get("paperId")) in paper_ids}
    claim_ids = {str(item["id"]) for item in program_claims}
    associations = [
        {"paper_id": str(card["paperId"]), "claim_id": ref, "review_id": card["id"], "relation": "REVIEW_BINDS_TO_PROGRAM_CLAIM"}
        for card in cards
        for ref in card.get("bind", [])
        if ref in claim_ids
    ]
    association_counts = Counter(item["claim_id"] for item in associations)
    associated_review_ids = {item["review_id"] for item in associations}
    candidate_deltas = [
        {"review_id": card["id"], "paper_id": card["paperId"], "declared_delta": card.get("claimDelta")}
        for card in cards
        if card.get("claimDelta") not in (None, "none")
    ]
    source_tiers = _counter(papers, "sourceTier")
    severe = [finding for finding in findings if finding.severity in {"CRITICAL", "HIGH"}]

    return {
        "schema_name": "SDBES_V7_OBSERVATORY_SCALE_STRESS_REPORT",
        "schema_version": "7.0.0",
        "generated_from": snapshot,
        "scientific_boundary": {
            "mode": "BULK_METADATA_AND_EXISTING_REVIEW_STRESS_TEST",
            "new_scientific_assessments": 0,
            "scientific_promotions_applied": 0,
            "rule": "Inventory, review, and claim association do not by themselves strengthen a scientific claim.",
        },
        "grain": {
            "catalog_record": "one Observatory paper inventory record",
            "review_record": "one structured Observatory review card",
            "association_record": "one review-declared paper-to-program-claim binding",
        },
        "counts": {
            "catalog_papers": len(papers),
            "review_cards": len(cards),
            "reviewed_catalog_papers": len(reviewed_paper_ids),
            "catalog_papers_without_review_card": len(paper_ids - reviewed_paper_ids),
            "program_claims": len(program_claims),
            "paper_claim_associations": len(associations),
            "review_cards_without_program_claim_binding": len(cards) - len(associated_review_ids),
            "declared_claim_delta_records": len(candidate_deltas),
            "data_quality_findings": len(findings),
            "high_or_critical_findings": len(severe),
        },
        "coverage": {
            "reviewed_catalog_share": round(len(reviewed_paper_ids) / len(paper_ids), 6) if paper_ids else 0,
            "source_tiers": source_tiers,
            "actions": _counter(cards, "action"),
            "routes": _counter(cards, "route"),
        },
        "program_claim_load": [
            {"claim_id": claim_id, "associated_review_count": association_counts.get(claim_id, 0)}
            for claim_id in sorted(claim_ids)
        ],
        "claim_delta_candidates": candidate_deltas,
        "known_findings": [asdict(finding) for finding in findings],
        "release_decision": {
            "status": "PASS_WITH_QUARANTINED_SOURCE_DEFECTS" if severe else "PASS",
            "may_browse_corpus": True,
            "may_use_existing_review_bindings": True,
            "may_auto_promote_claims": False,
            "may_auto_create_causal_edges": False,
            "missing_catalog_links_are_quarantined": True,
        },
        "v4_model_eligibility": {
            "authorized_executable_models": 0,
            "reference_implementations_found": ["sdbes.v4"],
            "decision": "NO_REGISTERED_SCIENTIFIC_MODEL_PACKAGE",
            "explanation": "The V4 reference implementation tests contracts and regression behavior; it is not yet a registered domain simulator with a pinned model card, calibrated inputs, and authorization receipt.",
        },
        "external_source_probes": [
            {
                "id": "OPENAI_MATH_2026_10_09",
                "source": "https://github.com/openai/math",
                "status": "SEPARATE_EXPERIMENTAL_SOURCE_FAMILY",
                "reported_inventory": {"manuscripts": 722, "families": 372},
                "formal_verification": "MIXED; some results have Lean artifacts and some do not",
                "independent_confirmation": "NOT_ESTABLISHED_BY_REPOSITORY_MEMBERSHIP_OR_LEAN_CHECK_ALONE",
                "v7_use": "Test formal-artifact ingestion, dependency tracking, correction history, and possible bottleneck relevance; do not merge into Observatory evidence scores automatically.",
            }
        ],
    }


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
