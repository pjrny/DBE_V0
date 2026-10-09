#!/usr/bin/env python3
"""Executable V7 Observatory-scale release gate."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sdbes.v7 import build_stress_report, load_json, sha256_file, validate_observatory  # noqa: E402

SOURCE_DIR = ROOT / "docs" / "SDBES" / "data" / "v7_observatory_snapshot"
REPORT_PATH = ROOT / "docs" / "SDBES" / "data" / "V7_OBSERVATORY_STRESS_REPORT.json"


def expect_code(findings, code: str) -> None:
    assert any(finding.code == code for finding in findings), (code, findings)


def run() -> None:
    catalog = load_json(SOURCE_DIR / "catalog.json")
    reviews = load_json(SOURCE_DIR / "reviews.json")
    claims = load_json(SOURCE_DIR / "claims.json")
    ledger = load_json(SOURCE_DIR / "ledger.json")
    manifest = load_json(SOURCE_DIR / "manifest.json")
    expected = load_json(REPORT_PATH)

    for name, item in manifest["captured_files"].items():
        assert sha256_file(ROOT / item["path"]) == item["sha256"], name

    started = time.perf_counter()
    actual = build_stress_report(catalog, reviews, claims, ledger, manifest)
    elapsed = time.perf_counter() - started
    assert actual == expected
    assert elapsed < 5.0, f"V7 deterministic stress build took {elapsed:.3f}s"

    assert actual["counts"]["catalog_papers"] == 405
    assert actual["counts"]["review_cards"] == 291
    assert actual["counts"]["program_claims"] == 13
    assert actual["scientific_boundary"]["scientific_promotions_applied"] == 0
    assert actual["release_decision"]["status"] == "PASS_WITH_QUARANTINED_SOURCE_DEFECTS"
    missing = [finding for finding in actual["known_findings"] if finding["code"] == "REVIEW_WITHOUT_CATALOG_PAPER"]
    assert sorted(finding["message"] for finding in missing) == ["2609.20725", "2609.20985"]
    assert actual["v4_model_eligibility"]["authorized_executable_models"] == 0

    bad = copy.deepcopy(catalog)
    bad["papers"][1]["id"] = bad["papers"][0]["id"]
    expect_code(validate_observatory(bad, reviews, claims, ledger), "DUPLICATE_PAPER_ID")

    bad = copy.deepcopy(reviews)
    bad["cards"][0]["action"] = "PROMOTE"
    expect_code(validate_observatory(catalog, bad, claims, ledger), "INVALID_REVIEW_ACTION")

    bad = copy.deepcopy(reviews)
    bad["cards"][0]["bind"] = ["UNKNOWN"]
    expect_code(validate_observatory(catalog, bad, claims, ledger), "UNRESOLVED_REVIEW_CLAIM_REF")

    bad = copy.deepcopy(catalog)
    bad["papers"][0]["claimIds"] = ["UNKNOWN"]
    expect_code(validate_observatory(bad, reviews, claims, ledger), "UNRESOLVED_PAPER_CLAIM_REF")

    bad = copy.deepcopy(reviews)
    bad["cards"][0]["gates"]["G1"] = "maybe"
    expect_code(validate_observatory(catalog, bad, claims, ledger), "INVALID_GATE_STATE")

    print(f"V7_OBSERVATORY_STRESS_CHECKS_PASSED elapsed={elapsed:.3f}s")


if __name__ == "__main__":
    run()
