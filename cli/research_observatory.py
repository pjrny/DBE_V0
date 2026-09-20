#!/usr/bin/env python3
"""Interactive Research Observatory tab for DBE_V0.

Three layers, never mixed into one score bar:

  library   catalog.json  (0–100 harvest gauges are not C)
  claims    claims.json   (C/T/D/A freeze)
  versions  versions.json (DBE and DBE-S version separately)

    python cli/research_observatory.py
    python cli/research_observatory.py --field anyons --sort importance
    python cli/research_observatory.py --tab claims
    python cli/research_observatory.py --tab versions
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "research" / "catalog.json"
CLAIMS = ROOT / "research" / "claims.json"
VERSIONS = ROOT / "research" / "versions.json"


def load_json(path: Path) -> dict:
    if not path.exists():
        sys.exit(f"missing {path}")
    return json.loads(path.read_text(encoding="utf-8"))


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
    if paper.get("claimIds"):
        print("claims:", ", ".join(paper["claimIds"]), paper.get("bindAction", ""))
    print()
    print("Core idea")
    print(paper.get("coreIdea", ""))
    print()
    print("Why it matters")
    print(paper.get("whyItMatters", ""))
    print()
    print("Limitation")
    print(paper.get("limitation", ""))
    print()
    print("NOTE harvest gauges are not C/T/D/A and cannot raise C.")
    if paper.get("url"):
        print()
        print(paper["url"])
    print("=" * 72)


def show_claims(claims: dict) -> int:
    print("DBE / DBE-S claim freeze  ·  heuristic gauges are not C")
    print(claims.get("rule", ""))
    print()
    for c in claims.get("claims", []):
        print(f"{c['id']:6}  {c['status']:6}  {c['C']} {c['T']} {c['D']} {c['A']}  {c['name']}")
        print(f"        {c['claim']}")
        print(f"        {c['verdict']}")
        print(f"        Disputer: {c['disputer']}")
        print()
    return 0


def show_versions(versions: dict) -> int:
    cur = versions.get("current", {})
    print(f"Working freeze  {cur.get('DBE')}  /  {cur.get('DBES')}")
    print(versions.get("scheme", ""))
    print()
    for line in versions.get("lines", []):
        print(f"{line['id']:4}  {line['current']}  {line['freeze']}")
    print()
    print("Buses")
    for b in versions.get("buses", []):
        print(f"  {b['id']} {b['name']:16} {b['C']} {b['D']}  {b['target']}")
    print()
    print("Version log")
    for v in versions.get("history", []):
        print(f"  {v['date']}  {v['version']:12}  {v['kind']:6}  {v['action']:10}  {v['title']}")
        print(f"             {v['summary']}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field", default="all")
    parser.add_argument("--sort", default="importance", choices=["importance", "confidence", "popularity", "date"])
    parser.add_argument("--role", default="all", help="week|month|lookback|pillar|internal|all")
    parser.add_argument("--tab", default="library", choices=["library", "claims", "versions"])
    parser.add_argument("--list", action="store_true", help="print titles and exit")
    args = parser.parse_args()

    if args.tab == "claims":
        return show_claims(load_json(CLAIMS))
    if args.tab == "versions":
        return show_versions(load_json(VERSIONS))

    data = load_json(CATALOG)
    papers = list(data.get("papers", []))
    if args.field != "all":
        papers = [p for p in papers if args.field in p.get("fields", [])]
    if args.role != "all":
        papers = [p for p in papers if p.get("role") == args.role]
    papers.sort(key=lambda p: p.get(args.sort, 0), reverse=args.sort != "date")
    if args.sort == "date":
        papers.sort(key=lambda p: p.get("date", ""), reverse=True)

    proto = data.get("protocol") or {}
    print(f"DBE Research Observatory  ·  {len(papers)} papers")
    print(f"Freeze {proto.get('dbe')} / {proto.get('dbes')}")
    print("KEEP:", ", ".join(p["name"] for p in data.get("pillars", []) if p.get("engineStatus") == "KEEP") or "(none)")
    print("QUEUE:", ", ".join(p["name"] for p in data.get("pillars", []) if p.get("engineStatus") == "QUEUE") or "(none)")
    print("NOTE:", proto.get("note", "harvest gauges are not C"))
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
