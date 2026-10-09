#!/usr/bin/env python3
"""Capture or deterministically rebuild the SDBES V7 Observatory stress run."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sdbes.v7 import build_stress_report, load_json, sha256_file  # noqa: E402


SOURCE_DIR = ROOT / "docs" / "SDBES" / "data" / "v7_observatory_snapshot"
REPORT_PATH = ROOT / "docs" / "SDBES" / "data" / "V7_OBSERVATORY_STRESS_REPORT.json"
SOURCE_FILES = {
    "catalog": "research/catalog.json",
    "reviews": "research/reviews.json",
    "claims": "research/claims.json",
    "ledger": "research/ledger.json",
}


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def capture(ref: str) -> dict[str, object]:
    commit = subprocess.check_output(["git", "rev-parse", ref], cwd=ROOT, text=True).strip()
    for name, source_path in SOURCE_FILES.items():
        payload = subprocess.check_output(["git", "show", f"{ref}:{source_path}"], cwd=ROOT)
        parsed = json.loads(payload)
        write_json(SOURCE_DIR / f"{name}.json", parsed)
    return {"source_ref": ref, "source_commit": commit}


def build(snapshot_override: dict[str, object] | None = None) -> None:
    manifest_path = SOURCE_DIR / "manifest.json"
    if snapshot_override is None:
        manifest = load_json(manifest_path)
    else:
        manifest = {
            **snapshot_override,
            "captured_files": {},
            "capture_boundary": "Structured Observatory JSON only; review markdown and simulator code were not merged.",
        }
    for name in SOURCE_FILES:
        path = SOURCE_DIR / f"{name}.json"
        manifest["captured_files"][name] = {
            "path": str(path.relative_to(ROOT)),
            "sha256": sha256_file(path),
            "bytes": path.stat().st_size,
        }
    write_json(manifest_path, manifest)
    report = build_stress_report(
        load_json(SOURCE_DIR / "catalog.json"),
        load_json(SOURCE_DIR / "reviews.json"),
        load_json(SOURCE_DIR / "claims.json"),
        load_json(SOURCE_DIR / "ledger.json"),
        manifest,
    )
    write_json(REPORT_PATH, report)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--capture-ref", help="Git ref containing the Observatory structured source files")
    args = parser.parse_args()
    build(capture(args.capture_ref) if args.capture_ref else None)
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
