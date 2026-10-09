"""Semantic integrity checks for SDBES V5/V6 staged and runtime data."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


ALLOWED_DISCOVERY_CLASSES = {"D", "P", "S", "X"}
ALLOWED_REVIEW_WORKFLOW = {"STAGED", "IN_REVIEW", "REVIEWED", "QUARANTINED"}
ALLOWED_CONTEXT = {"NOT_ASSESSED", "COMPATIBLE", "INCOMPATIBLE", "PARTIAL", "UNKNOWN"}
ALLOWED_RUBRIC = {"T0", "T1", "T2", "T3"}
ALLOWED_ACTIVITY_MODES = {"EXPLORATORY", "CONFIRMATORY", "REPLICATION", "ROBUSTNESS", "SOFTWARE_QA"}
ALLOWED_ATTEMPT_OUTCOMES = {"SUCCESS", "NULL", "ADVERSE", "INVALID", "ABANDONED", "FAILED_TO_RUN"}
ALLOWED_COMPARISON_STATES = {"COMPARABLE", "INSUFFICIENT_COMPARABLE_INFORMATION", "PREFERENCE_SENSITIVE"}
CONFIRMATORY_FIELDS = {
    "claim_version",
    "primary_outcome",
    "comparator",
    "scope",
    "exclusions",
    "analysis_procedure",
    "stopping_rule",
    "decision_thresholds",
    "prior_data_exposure",
    "frozen_at",
}
CONCEPT_ID = re.compile(r"^DBE-([A-F])\d{2}$")


@dataclass(frozen=True)
class IntegrityFinding:
    code: str
    path: str
    message: str


class IntegrityError(ValueError):
    def __init__(self, findings: Iterable[IntegrityFinding]):
        self.findings = tuple(findings)
        super().__init__("; ".join(f"{f.code} at {f.path}: {f.message}" for f in self.findings))


def _duplicates(values: Iterable[str]) -> set[str]:
    seen: set[str] = set()
    duplicate: set[str] = set()
    for value in values:
        (duplicate if value in seen else seen).add(value)
    return duplicate


def validate_inventory(data: dict[str, Any], root: Path | None = None) -> list[IntegrityFinding]:
    findings: list[IntegrityFinding] = []
    concepts = data.get("concepts", [])
    sources = data.get("sources", [])
    concept_ids = [item.get("id") for item in concepts]
    source_ids = [item.get("id") for item in sources]
    concept_set = set(concept_ids)
    source_set = set(source_ids)

    for duplicate in sorted(_duplicates(concept_ids)):
        findings.append(IntegrityFinding("DUPLICATE_CONCEPT_ID", "concepts", duplicate))
    for duplicate in sorted(_duplicates(source_ids)):
        findings.append(IntegrityFinding("DUPLICATE_SOURCE_ID", "sources", duplicate))

    for index, concept in enumerate(concepts):
        path = f"concepts[{index}]"
        match = CONCEPT_ID.match(str(concept.get("id", "")))
        if not match:
            findings.append(IntegrityFinding("INVALID_CONCEPT_ID", f"{path}.id", "expected DBE-A01 form"))
        elif concept.get("domain_code") != match.group(1):
            findings.append(IntegrityFinding("DOMAIN_ID_MISMATCH", f"{path}.domain_code", "must match ID prefix"))
        if concept.get("discovery_class") not in ALLOWED_DISCOVERY_CLASSES:
            findings.append(IntegrityFinding("INVALID_DISCOVERY_CLASS", f"{path}.discovery_class", "use D/P/S/X"))
        if concept.get("review_workflow") not in ALLOWED_REVIEW_WORKFLOW:
            findings.append(IntegrityFinding("INVALID_REVIEW_WORKFLOW", f"{path}.review_workflow", "unsupported state"))
        if concept.get("context_compatibility") not in ALLOWED_CONTEXT:
            findings.append(IntegrityFinding("INVALID_CONTEXT_STATE", f"{path}.context_compatibility", "unsupported state"))
        for ref in concept.get("source_refs", []):
            if ref not in source_set:
                findings.append(IntegrityFinding("UNRESOLVED_SOURCE_REF", f"{path}.source_refs", ref))
        if concept.get("display_status") == "PRIMARY_SOURCE_VERIFIED":
            receipts = concept.get("verification_receipts", [])
            if not receipts:
                findings.append(IntegrityFinding("VERIFICATION_WITHOUT_RECEIPT", path, "verified status requires receipt"))

    for index, source in enumerate(sources):
        verification = source.get("verification", {})
        if verification.get("status") == "PRIMARY_SOURCE_VERIFIED" and not verification.get("receipt"):
            findings.append(IntegrityFinding("SOURCE_VERIFICATION_WITHOUT_RECEIPT", f"sources[{index}]", source.get("id", "")))

    for index, claim in enumerate(data.get("reviewed_claims", [])):
        path = f"reviewed_claims[{index}]"
        candidate = claim.get("candidate")
        if candidate and candidate not in concept_set:
            findings.append(IntegrityFinding("BROKEN_CLAIM_CROSSWALK", f"{path}.candidate", candidate))
        rubric = claim.get("observatory_rubric")
        if rubric is not None and rubric not in ALLOWED_RUBRIC:
            findings.append(IntegrityFinding("INVALID_OBSERVATORY_RUBRIC", f"{path}.observatory_rubric", str(rubric)))

    counts = data.get("derived_counts", {})
    actual = {
        "concepts": len(concepts),
        "source_records": len(sources),
        "scientific_or_official_sources": sum(s.get("record_type") == "SCIENTIFIC_OR_OFFICIAL" for s in sources),
        "software_records": sum(s.get("record_type") == "SOFTWARE" for s in sources),
        "discovery_portals": sum(s.get("record_type") == "PORTAL" for s in sources),
        "assessed_concepts": sum(bool(c.get("scientific_assessment_refs")) for c in concepts),
        "unresolved_source_refs": len({f.message for f in findings if f.code == "UNRESOLVED_SOURCE_REF"}),
    }
    for key, value in actual.items():
        if counts.get(key) != value:
            findings.append(IntegrityFinding("DERIVED_COUNT_MISMATCH", f"derived_counts.{key}", f"expected {value}"))

    if root:
        for index, snapshot in enumerate(data.get("source_snapshots", [])):
            path = root / snapshot.get("path", "")
            if not path.is_file():
                findings.append(IntegrityFinding("SNAPSHOT_MISSING", f"source_snapshots[{index}]", str(path)))
                continue
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest != snapshot.get("sha256"):
                findings.append(IntegrityFinding("SNAPSHOT_HASH_MISMATCH", f"source_snapshots[{index}]", str(path)))
    return findings


def require_valid_inventory(data: dict[str, Any], root: Path | None = None) -> None:
    findings = validate_inventory(data, root=root)
    if findings:
        raise IntegrityError(findings)


def validate_runtime(runtime: dict[str, Any], inventory: dict[str, Any]) -> list[IntegrityFinding]:
    findings: list[IntegrityFinding] = []
    concept_ids = {item["id"] for item in inventory.get("concepts", [])}
    claim_ids = [item.get("id") for item in runtime.get("reviewed_claims", [])]
    program_ids = [item.get("id") for item in runtime.get("program_claims", [])]
    for duplicate in sorted(_duplicates(claim_ids)):
        findings.append(IntegrityFinding("DUPLICATE_REVIEWED_CLAIM_ID", "reviewed_claims", duplicate))
    for duplicate in sorted(_duplicates(program_ids)):
        findings.append(IntegrityFinding("DUPLICATE_PROGRAM_CLAIM_ID", "program_claims", duplicate))
    for index, claim in enumerate(runtime.get("reviewed_claims", [])):
        if claim.get("candidate") not in concept_ids:
            findings.append(IntegrityFinding("BROKEN_CLAIM_CROSSWALK", f"reviewed_claims[{index}].candidate", str(claim.get("candidate"))))
    relation_ids = [item.get("id") for item in runtime.get("relationships", [])]
    for duplicate in sorted(_duplicates(relation_ids)):
        findings.append(IntegrityFinding("DUPLICATE_RELATIONSHIP_ID", "relationships", duplicate))
    claim_set = set(claim_ids)
    for index, relation in enumerate(runtime.get("relationships", [])):
        if relation.get("source_id") not in claim_set or relation.get("target_id") not in concept_ids:
            findings.append(IntegrityFinding("UNRESOLVED_RELATIONSHIP_ENDPOINT", f"relationships[{index}]", relation.get("id", "")))
        if relation.get("review_status") != "REVIEWED":
            findings.append(IntegrityFinding("UNREVIEWED_RELATIONSHIP_IN_RUNTIME", f"relationships[{index}]", relation.get("id", "")))
    for index, claim in enumerate(runtime.get("program_claims", [])):
        rubric = claim.get("T")
        if rubric not in ALLOWED_RUBRIC:
            findings.append(IntegrityFinding("INVALID_OBSERVATORY_RUBRIC", f"program_claims[{index}].T", str(rubric)))
    queue_ids = [item.get("id") for item in runtime.get("research_queue", [])]
    for duplicate in sorted(_duplicates(queue_ids)):
        findings.append(IntegrityFinding("DUPLICATE_RESEARCH_TEST_ID", "research_queue", duplicate))
    for index, item in enumerate(runtime.get("research_queue", [])):
        path = f"research_queue[{index}]"
        if item.get("concept_id") not in concept_ids:
            findings.append(IntegrityFinding("BROKEN_RESEARCH_TEST_CROSSWALK", f"{path}.concept_id", str(item.get("concept_id"))))
        if item.get("activity_mode") not in ALLOWED_ACTIVITY_MODES:
            findings.append(IntegrityFinding("INVALID_ACTIVITY_MODE", f"{path}.activity_mode", str(item.get("activity_mode"))))
        if item.get("comparison_state") not in ALLOWED_COMPARISON_STATES:
            findings.append(IntegrityFinding("INVALID_COMPARISON_STATE", f"{path}.comparison_state", str(item.get("comparison_state"))))
        if item.get("activity_mode") == "CONFIRMATORY":
            plan = item.get("preregistration") or {}
            missing = sorted(CONFIRMATORY_FIELDS - set(plan))
            if missing:
                findings.append(IntegrityFinding("INCOMPLETE_CONFIRMATORY_PLAN", f"{path}.preregistration", ", ".join(missing)))
        for attempt_index, attempt in enumerate(item.get("attempts", [])):
            if attempt.get("outcome") not in ALLOWED_ATTEMPT_OUTCOMES:
                findings.append(IntegrityFinding("INVALID_ATTEMPT_OUTCOME", f"{path}.attempts[{attempt_index}]", str(attempt.get("outcome"))))
    if runtime.get("authorized_models"):
        for index, model in enumerate(runtime["authorized_models"]):
            if not model.get("authorization_receipt"):
                findings.append(IntegrityFinding("MODEL_WITHOUT_AUTHORIZATION", f"authorized_models[{index}]", str(model.get("id"))))
    return findings


def require_valid_runtime(runtime: dict[str, Any], inventory: dict[str, Any]) -> None:
    findings = validate_runtime(runtime, inventory)
    if findings:
        raise IntegrityError(findings)


def load_and_validate(path: Path, root: Path | None = None) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    require_valid_inventory(data, root=root)
    return data
