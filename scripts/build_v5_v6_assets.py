#!/usr/bin/env python3
"""Build the V5/V6 staging inventory from pinned Phase-1 source snapshots.

This is a deterministic migration helper, not a scientific assessor.  It
preserves the atlas wording and derives counts from records.  It never turns a
Phase-1 discovery tag into a V1/V2 scientific assessment.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE1 = ROOT / "docs" / "research" / "phase1"
OUT = ROOT / "docs" / "SDBES" / "data"
PAPER_CASES = ROOT / "docs" / "SDBES" / "tests" / "V1_V2_10_PAPER_ASSESSMENTS.json"
REGRESSION_CASES = ROOT / "docs" / "SDBES" / "tests" / "V1_V4_R2_EXISTING_CASES.json"
PROGRAM_CLAIMS = ROOT / "research" / "claims.json"

ATLAS = PHASE1 / "DBE_RESEARCH_ATLAS.md"
LIBRARY = PHASE1 / "SOURCE_LIBRARY.md"
GAPS = PHASE1 / "SEARCH_AND_GAPS.md"

DOMAIN_NAMES = {
    "A": "Nuclear energy and fusion architectures",
    "B": "Planetary heat, solar and other renewable gradients",
    "C": "Magnetism, materials, conversion and storage",
    "D": "Intelligence and discovery multipliers",
    "E": "Unconventional reservoirs and fundamental physics",
    "F": "Demand reduction, computation and digital civilization",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_sources(text: str) -> list[dict]:
    blocks = re.split(r"(?m)^### (?=[A-Z][A-Z0-9]+ - )", text)
    sources: list[dict] = []
    for block in blocks[1:]:
        first, *rest = block.splitlines()
        match = re.match(r"([A-Z][A-Z0-9]+) - (.+)", first.strip())
        if not match:
            continue
        source_id, title = match.groups()
        body = "\n".join(rest)
        link = re.search(r"\[Primary page or official record\]\(([^)]+)\)", body)
        doi = re.search(r"DOI: \[[^]]+\]\(([^)]+)\)", body)
        title_link = re.fullmatch(r"\[([^]]+)\]\(([^)]+)\)", title.strip())
        record_type = "SOFTWARE" if source_id.startswith("T") else "PORTAL" if source_id.startswith("P") else "SCIENTIFIC_OR_OFFICIAL"
        sources.append(
            {
                "id": source_id,
                "title": title_link.group(1) if title_link else title.strip(),
                "record_type": record_type,
                "url": link.group(1) if link else title_link.group(2) if title_link else None,
                "doi_url": doi.group(1) if doi else None,
                "verification": {
                    "status": "SOURCE_RECORD_PRESENT",
                    "receipt": None,
                    "note": "Inventory record only; primary-result verification is not implied.",
                },
            }
        )
    return sources


def field(body: str, label: str) -> str | None:
    match = re.search(
        rf"\*\*{re.escape(label)}:\*\*\s*(.*?)(?=\s+\*\*[^*\n]+:\*\*|\n|\Z)",
        body,
    )
    return match.group(1).strip() if match else None


def parse_source_refs(body: str) -> list[str]:
    anchors = field(body, "Source anchors") or ""
    return list(dict.fromkeys(re.findall(r"\[([A-Z][A-Z0-9]+):", anchors)))


def parse_concepts(text: str) -> list[dict]:
    pattern = re.compile(
        r"(?ms)^### (DBE-([A-F])\d{2}) - (.+?)\n(.*?)(?=^### DBE-[A-F]\d{2} - |\Z)"
    )
    concepts: list[dict] = []
    for match in pattern.finditer(text):
        concept_id, domain_code, title, body = match.groups()
        class_match = re.search(r"\*\*Class:\*\*\s*([DPSX])\s*-\s*([^.]*)", body)
        role_match = re.search(r"\*\*Role:\*\*\s*([^.]*)", body)
        tags = field(body, "Tags") or ""
        concepts.append(
            {
                "id": concept_id,
                "title": title.strip(),
                "domain_code": domain_code,
                "domain": DOMAIN_NAMES[domain_code],
                "discovery_class": class_match.group(1) if class_match else None,
                "discovery_class_label": class_match.group(2).strip() if class_match else None,
                "role": role_match.group(1).strip() if role_match else None,
                "bounded_question": field(body, "Bounded question"),
                "mechanism_status": field(body, "Mechanism status"),
                "resource_ledger": field(body, "Energy/resource ledger"),
                "main_gap": field(body, "Main gap"),
                "next_investigation": field(body, "Next discriminating investigation"),
                "coverage": field(body, "Coverage"),
                "formal_confidence": field(body, "Formal confidence"),
                "source_refs": parse_source_refs(body),
                "tags": [item.strip().rstrip(".") for item in tags.split(",") if item.strip()],
                "review_workflow": "STAGED",
                "work_disposition": "DISCOVERY_INVENTORY",
                "record_roles": ["CONCEPT_CANDIDATE"],
                "scientific_assessment_refs": [],
                "context_compatibility": "NOT_ASSESSED",
                "display_status": "Discovery-only — not assessed",
            }
        )
    return concepts


def main() -> None:
    concepts = parse_concepts(ATLAS.read_text(encoding="utf-8"))
    sources = parse_sources(LIBRARY.read_text(encoding="utf-8"))
    source_ids = {source["id"] for source in sources}
    unresolved = sorted(
        {ref for concept in concepts for ref in concept["source_refs"] if ref not in source_ids}
    )
    gap_text = GAPS.read_text(encoding="utf-8")
    gap_invalid = "requested file reference is not currently visible" in gap_text.lower()

    payload = {
        "schema_name": "SDBES_V6_STAGING_INVENTORY_R2",
        "snapshot_date": "2026-10-09",
        "scientific_status": "STAGING_ONLY",
        "warning": (
            "Discovery records are not scientific assessments. Phase-1 D/P/S/X tags are preserved "
            "as legacy discovery metadata only."
        ),
        "source_snapshots": [
            {
                "path": str(ATLAS.relative_to(ROOT)),
                "sha256": sha256(ATLAS),
                "role": "concept inventory source",
            },
            {
                "path": str(LIBRARY.relative_to(ROOT)),
                "sha256": sha256(LIBRARY),
                "role": "source-record inventory",
            },
            {
                "path": str(GAPS.relative_to(ROOT)),
                "sha256": sha256(GAPS),
                "role": "quarantined source-gap artifact",
                "content_status": "INVALID_SOURCE_CONTENT" if gap_invalid else "UNREVIEWED",
            },
        ],
        "source_incidents": [
            {
                "id": "INC-SEARCH-AND-GAPS-001",
                "path": str(GAPS.relative_to(ROOT)),
                "status": "INVALID_SOURCE_CONTENT" if gap_invalid else "UNREVIEWED",
                "effect": "The reported 19 background-only/adjacent-source identities remain unreconciled.",
                "do_not_infer": "Do not infer that the remaining 71 concepts have direct support.",
                "reactivation_condition": "Recover or reconstruct the mapping with documented review provenance.",
            }
        ],
        "derived_counts": {
            "concepts": len(concepts),
            "source_records": len(sources),
            "scientific_or_official_sources": sum(s["record_type"] == "SCIENTIFIC_OR_OFFICIAL" for s in sources),
            "software_records": sum(s["record_type"] == "SOFTWARE" for s in sources),
            "discovery_portals": sum(s["record_type"] == "PORTAL" for s in sources),
            "assessed_concepts": sum(bool(c["scientific_assessment_refs"]) for c in concepts),
            "unresolved_source_refs": len(unresolved),
        },
        "unresolved_source_refs": unresolved,
        "concepts": concepts,
        "sources": sources,
    }

    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / "V6_CONCEPT_INVENTORY.json"
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    paper_cases = json.loads(PAPER_CASES.read_text(encoding="utf-8"))["papers"]
    regressions = json.loads(REGRESSION_CASES.read_text(encoding="utf-8"))["cases"]
    regression_by_id = {case["id"]: case for case in regressions}
    reviewed_claims = []
    relationships = []
    for paper in paper_cases:
        regression = regression_by_id[paper["id"]]
        reviewed_claims.append(
            {
                **paper,
                "record_type": "REVIEWED_CLAIM_CASE",
                "review_workflow": "REVIEWED",
                "assessment_result": regression["r2_conclusion"],
                "assessment_scope": "Frozen V1-V4 regression case; not an independent reproduction.",
                "v4_contract": regression["v4_contract"],
                "source_locator": {
                    "path": "docs/SDBES/tests/V1_V2_10_PAPER_ASSESSMENTS.json",
                    "record_id": paper["id"],
                    "exact_primary_result_location": None,
                    "status": "INVENTORY_LOCATOR_ONLY",
                },
            }
        )
        relationships.append(
            {
                "id": f"REL-{paper['id']}-{paper['candidate']}",
                "source_id": paper["id"],
                "target_id": paper["candidate"],
                "relation_type": paper["application_relation"],
                "review_status": "REVIEWED",
                "gate": None,
                "source_locator": "docs/SDBES/tests/V1_V2_10_PAPER_ASSESSMENTS.json",
            }
        )
    program_source = json.loads(PROGRAM_CLAIMS.read_text(encoding="utf-8"))
    program_claims = [
        {
            **claim,
            "record_type": "LEGACY_PROGRAM_CLAIM",
            "review_workflow": "IMPORTED_SNAPSHOT",
            "assessment_scope": "Program-use decision in the pinned research snapshot; not universal scientific status.",
            "source_locator": {"path": "research/claims.json", "record_id": claim["id"]},
        }
        for claim in program_source["claims"]
    ]
    runtime = {
        "schema_name": "SDBES_V5_READ_ONLY_RUNTIME_R2",
        "snapshot_date": "2026-10-09",
        "mode": "READ_ONLY",
        "source_snapshots": [
            {
                "path": str(PROGRAM_CLAIMS.relative_to(ROOT)),
                "sha256": sha256(PROGRAM_CLAIMS),
                "role": "13 legacy Observatory program claims",
            }
        ],
        "reviewed_claims": reviewed_claims,
        "program_claims": program_claims,
        "program_claim_rubric": {
            "freeze": program_source["freeze"],
            "rule": program_source["rule"],
            "axes": program_source["axes"],
            "warning": "Legacy Observatory harvest metadata; never substitute these axes for canonical SDBES assessments.",
        },
        "relationships": relationships,
        "research_queue": [
            {
                "id": f"RQ-{concept['id']}",
                "concept_id": concept["id"],
                "title": concept["next_investigation"],
                "activity_mode": "EXPLORATORY",
                "origin": "PHASE1_PROPOSED_INVESTIGATION",
                "comparison_state": "INSUFFICIENT_COMPARABLE_INFORMATION",
                "attempts": [],
                "preregistration": None,
                "decision_rule": None,
                "work_status": "PROPOSED",
            }
            for concept in concepts
            if concept["next_investigation"]
        ],
        "authorized_models": [],
        "scenario_message": "No authorized model available",
    }
    runtime_target = OUT / "V5_RUNTIME_VIEW.json"
    runtime_target.write_text(json.dumps(runtime, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {target.relative_to(ROOT)}: {len(concepts)} concepts, {len(sources)} sources")
    print(
        f"wrote {runtime_target.relative_to(ROOT)}: {len(reviewed_claims)} reviewed claim cases, "
        f"{len(program_claims)} program cases, {len(relationships)} reviewed relationships"
    )


if __name__ == "__main__":
    main()
