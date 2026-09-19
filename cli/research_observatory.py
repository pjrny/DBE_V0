#!/usr/bin/env python3
"""Interactive Research Observatory tab for DBE_V0.

Browse the catalog: this week, lookback, pillars, suggested pillars, and
plain-language briefs (core idea / why it matters / limitation).

    python cli/research_observatory.py
    python cli/research_observatory.py --field anyons --sort importance
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "research" / "catalog.json"


def load() -> dict:
    if not CATALOG.exists():
        sys.exit(f"missing {CATALOG}")
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def show_paper(paper: dict) -> None:
    print()
    print("=" * 72)
    flags = []
    if paper.get("foundational"):
        flags.append("FOUNDATIONAL")
    if paper.get("role"):
        flags.append(str(paper["role"]).upper())
    print("  ".join(flags) or "PAPER")
    print(paper["title"])
    print(", ".join(paper.get("authors", [])[:6]))
    print(f"{paper.get('date')} · {paper.get('venue')}")
    print(
        "importance {importance}  confidence {confidence}  popularity {popularity}".format(
            **{k: paper.get(k, 0) for k in ("importance", "confidence", "popularity")}
        )
    )
    print("fields:", ", ".join(paper.get("fields", [])))
    print()
    print("Core idea")
    print(paper.get("coreIdea", ""))
    print()
    print("Why it matters")
    print(paper.get("whyItMatters", ""))
    print()
    print("Limitation")
    print(paper.get("limitation", ""))
    if paper.get("url"):
        print()
        print(paper["url"])
    print("=" * 72)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field", default="all")
    parser.add_argument("--sort", default="importance", choices=["importance", "confidence", "popularity", "date"])
    parser.add_argument("--role", default="all", help="week|month|lookback|pillar|internal|all")
    parser.add_argument("--list", action="store_true", help="print titles and exit")
    args = parser.parse_args()
    data = load()
    papers = list(data.get("papers", []))
    if args.field != "all":
        papers = [p for p in papers if args.field in p.get("fields", [])]
    if args.role != "all":
        papers = [p for p in papers if p.get("role") == args.role]
    reverse = args.sort != "date"
    papers.sort(key=lambda p: p.get(args.sort, 0), reverse=reverse if args.sort != "date" else True)
    if args.sort == "date":
        papers.sort(key=lambda p: p.get("date", ""), reverse=True)

    print(f"DBE Research Observatory  ·  {len(papers)} papers")
    print("Pillars:", ", ".join(p["name"] for p in data.get("pillars", []) if p.get("status") == "established"))
    print(
        "Suggested:",
        ", ".join(p["name"] for p in data.get("pillars", []) if p.get("status") == "suggested") or "(none)",
    )
    print()
    for i, paper in enumerate(papers, 1):
        print(f"{i:3d}  [{paper.get('importance', 0):3d}]  {paper.get('date')}  {paper['title'][:70]}")
    if args.list or not sys.stdin.isatty():
        return 0

    while True:
        raw = input("\nOpen # (or q): ").strip()
        if raw.lower() in {"q", "quit", "exit"}:
            return 0
        if not raw.isdigit():
            continue
        idx = int(raw) - 1
        if 0 <= idx < len(papers):
            show_paper(papers[idx])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
