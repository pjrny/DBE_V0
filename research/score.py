#!/usr/bin/env python3
"""Protocol scorer for daily papers.

Heuristic 0–100 numbers from fetch_arxiv.py are harvest metadata.
They are not C, T, D, or A and must not enter the frozen claim table.

The venue is normalised (case and whitespace) before any gate is read, so
"arXiv", "ARXIV", " arxiv " and "arxiv" are the same bare preprint. A bare
arXiv / preprint venue never passes A5 and never raises C.

Usage:
  python research/score.py --bind E-S3 --action INCLUDE --paper lo-2026 --venue nature
"""
from __future__ import annotations

import argparse
import json
import re
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

# Venues that are a bare preprint. Anything that starts with one of these
# words (e.g. "arXiv:2610.00464", "arXiv preprint", "preprint (submitted)")
# is also a bare preprint. An empty venue is unknown and treated the same way.
PREPRINT_VENUES = {"", "arxiv", "arxiv preprint", "preprint"}
_PREPRINT_PREFIX = re.compile(r"^(arxiv|preprint)\b")


def normalize_venue(venue: str | None) -> str:
    """Lowercase and collapse whitespace: '  arXiv  Preprint ' -> 'arxiv preprint'."""
    return " ".join((venue or "").split()).lower()


def is_bare_preprint(venue: str | None) -> bool:
    v = normalize_venue(venue)
    return v in PREPRINT_VENUES or bool(_PREPRINT_PREFIX.match(v))


def route(action: str, status: str, venue: str | None) -> dict:
    """Decide the route for one scored paper.

    Returns a dict with the normalised venue, whether A5 passes, whether the
    venue may raise C at all, and the ROUTE string printed by the CLI.
    """
    v = normalize_venue(venue)
    preprint = is_bare_preprint(v)
    a5 = not preprint
    auto = False
    if action == "INCLUDE" and a5 and status in {"KEEP", "HOLD"}:
        auto = True
    if action in {"WEAKEN", "DISCONFIRM"}:
        auto = True
    if auto and action == "INCLUDE":
        label = "AUTO-MERGED PATCH"
    elif auto:
        label = "APPLIED-WEAKEN"
    else:
        label = "QUEUE"
    return {
        "venue": v,
        "preprint": preprint,
        "a5": a5,
        # Only a journal / replicated-hardware venue may ever raise C, and even
        # then only through STRENGTHEN with all of A1–A8 (not decided here).
        "canRaiseC": a5 and action == "STRENGTHEN",
        "auto": auto,
        "route": label,
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--bind", required=True)
    p.add_argument("--action", required=True, choices=["STRENGTHEN", "WEAKEN", "DISCONFIRM", "INCLUDE", "HOLD", "NEW PILLAR", "REJECT"])
    p.add_argument("--paper", required=True)
    p.add_argument("--venue", default="arxiv")
    args = p.parse_args(argv)
    claims = json.loads(CLAIMS.read_text())["claims"]
    claim = next((c for c in claims if c["id"] == args.bind), None)
    if claim is None:
        print(f"unknown claim {args.bind}")
        return 2
    r = route(args.action, claim["status"], args.venue)
    shown = " ".join((args.venue or "").split()) or "(none)"
    print(f"BIND {args.bind} ({claim['status']} {claim['C']}/{claim['T']}/{claim['D']}/{claim['A']})")
    print(f"ACTION {args.action}  PAPER {args.paper}  VENUE {shown}")
    if r["preprint"]:
        print("A5 FAIL bare arXiv/preprint venue: cannot pass A5 or raise C")
    else:
        print("A5 venue is not a bare preprint (still confirm journal or replicated hardware)")
    print("ROUTE", r["route"])
    print("NOTE heuristic gauges must not move C. Auto-Gate:\n", AUTO_GATE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
