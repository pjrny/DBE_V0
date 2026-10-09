#!/usr/bin/env python3
"""Executable V5/V6 R2 integrity release gate."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sdbes.v5_v6 import validate_inventory, validate_runtime  # noqa: E402


INVENTORY_PATH = ROOT / "docs" / "SDBES" / "data" / "V6_CONCEPT_INVENTORY.json"
RUNTIME_PATH = ROOT / "docs" / "SDBES" / "data" / "V5_RUNTIME_VIEW.json"


def expect_code(findings, code: str) -> None:
    assert any(finding.code == code for finding in findings), (code, findings)


def run() -> None:
    inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
    runtime = json.loads(RUNTIME_PATH.read_text(encoding="utf-8"))
    assert not validate_inventory(inventory, root=ROOT)
    assert not validate_runtime(runtime, inventory)
    assert inventory["derived_counts"]["concepts"] == 90
    assert inventory["derived_counts"]["scientific_or_official_sources"] == 81
    assert inventory["derived_counts"]["software_records"] == 19
    assert inventory["derived_counts"]["discovery_portals"] == 11
    assert inventory["derived_counts"]["assessed_concepts"] == 0
    assert len(runtime["reviewed_claims"]) == 10
    assert len(runtime["program_claims"]) == 13
    assert len(runtime["relationships"]) == 10
    assert runtime["authorized_models"] == []

    bad = copy.deepcopy(inventory)
    bad["concepts"][0]["source_refs"].append("MISSING")
    expect_code(validate_inventory(bad), "UNRESOLVED_SOURCE_REF")

    bad = copy.deepcopy(inventory)
    bad["concepts"][1]["id"] = bad["concepts"][0]["id"]
    expect_code(validate_inventory(bad), "DUPLICATE_CONCEPT_ID")

    bad = copy.deepcopy(inventory)
    bad["sources"][1]["id"] = bad["sources"][0]["id"]
    expect_code(validate_inventory(bad), "DUPLICATE_SOURCE_ID")

    bad = copy.deepcopy(inventory)
    bad["concepts"][0]["domain_code"] = "F"
    expect_code(validate_inventory(bad), "DOMAIN_ID_MISMATCH")

    bad = copy.deepcopy(inventory)
    bad["concepts"][0]["display_status"] = "PRIMARY_SOURCE_VERIFIED"
    expect_code(validate_inventory(bad), "VERIFICATION_WITHOUT_RECEIPT")

    bad = copy.deepcopy(inventory)
    bad["derived_counts"]["concepts"] = 91
    expect_code(validate_inventory(bad), "DERIVED_COUNT_MISMATCH")

    bad_runtime = copy.deepcopy(runtime)
    bad_runtime["program_claims"][0]["T"] = "T5"
    expect_code(validate_runtime(bad_runtime, inventory), "INVALID_OBSERVATORY_RUBRIC")

    bad_runtime = copy.deepcopy(runtime)
    bad_runtime["reviewed_claims"][0]["candidate"] = "DBE-Z99"
    expect_code(validate_runtime(bad_runtime, inventory), "BROKEN_CLAIM_CROSSWALK")

    bad_runtime = copy.deepcopy(runtime)
    bad_runtime["relationships"][0]["source_id"] = "UNKNOWN"
    expect_code(validate_runtime(bad_runtime, inventory), "UNRESOLVED_RELATIONSHIP_ENDPOINT")

    bad_runtime = copy.deepcopy(runtime)
    bad_runtime["authorized_models"] = [{"id": "MODEL-1"}]
    expect_code(validate_runtime(bad_runtime, inventory), "MODEL_WITHOUT_AUTHORIZATION")

    bad_runtime = copy.deepcopy(runtime)
    bad_runtime["research_queue"][0]["activity_mode"] = "CONFIRMATORY"
    expect_code(validate_runtime(bad_runtime, inventory), "INCOMPLETE_CONFIRMATORY_PLAN")

    incident = inventory["source_incidents"][0]
    assert incident["status"] == "INVALID_SOURCE_CONTENT"
    print("V5_V6_INTEGRITY_CHECKS_PASSED")


if __name__ == "__main__":
    run()
