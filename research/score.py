#!/usr/bin/env python3
"""Protocol scorer for daily papers.

Heuristic 0–100 numbers from fetch_arxiv.py are harvest metadata.
They are not C, T, D, or A and must not enter the frozen claim table.

Usage:
  python research/score.py --bind E-S3 --action INCLUDE --paper lo-2026
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CLAIMS = ROOT / "claims.json"

AUTO_GATE = """
A1 one KEEP/HOLD claim ID
A2 G1–G6 pass
A3 STRENGTHEN or INCLUDE
A4 new C ≥ 4, or C unchanged and a published bound tightens
A5 journal or replicated hardware (bare arXiv cannot raise C)
A6 no new mechanism/bus/fuel/coupling
A7 does not increase HOLD count
A8 ledger moves only in the conservative direction
"""


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--bind", required=True)
    p.add_argument("--action", required=True, choices=["STRENGTHEN", "WEAKEN", "DISCONFIRM", "INCLUDE", "HOLD", "NEW PILLAR", "REJECT"])
    p.add_argument("--paper", required=True)
    p.add_argument("--venue", default="arxiv")
    args = p.parse_args()
    claims = json.loads(CLAIMS.read_text())["claims"]
    claim = next((c for c in claims if c["id"] == args.bind), None)
    if claim is None:
        print(f"unknown claim {args.bind}")
        return 2
    auto = False
    if args.action == "INCLUDE" and args.venue != "arxiv" and claim["status"] in {"KEEP", "HOLD"}:
        auto = True
    if args.action in {"WEAKEN", "DISCONFIRM"}:
        auto = True
    print(f"BIND {args.bind} ({claim['status']} {claim['C']}/{claim['T']}/{claim['D']}/{claim['A']})")
    print(f"ACTION {args.action}  PAPER {args.paper}  VENUE {args.venue}")
    print("ROUTE", "AUTO-MERGED PATCH" if auto and args.action == "INCLUDE" else ("APPLIED-WEAKEN" if auto else "QUEUE"))
    print("NOTE heuristic gauges must not move C. Auto-Gate:\n", AUTO_GATE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
