#!/usr/bin/env python3
"""Daily arXiv ingest for the DBE Research Observatory.

Queries the program feeds and writes a dated JSON run under research/runs/.
Foundational pillars are never dropped: they live in catalog.json for any date.
The first few runs should use --lookback-days 365 (or more).

Example:
    python research/ingest.py --lookback-days 365
    python research/ingest.py --lookback-days 7
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FEEDS = [
    "https://arxiv.org/list/quant-ph/recent",
    "https://arxiv.org/list/cond-mat.str-el/recent",
    "https://arxiv.org/list/cond-mat.mes-hall/recent",
    "https://arxiv.org/list/hep-th/recent",
    "https://arxiv.org/list/physics.plasm-ph/recent",
    "https://arxiv.org/search/advanced",
]

QUERIES = [
    "all:anyon AND (cat:quant-ph OR cat:cond-mat.str-el)",
    "ti:Majorana AND (cat:quant-ph OR cat:cond-mat.mes-hall)",
    "all:fracton AND (cat:quant-ph OR cat:cond-mat.str-el)",
    'all:"time crystal" OR (ti:Floquet AND cat:quant-ph)',
    "all:holographic AND (cat:hep-th OR cat:quant-ph)",
    "all:tokamak AND cat:physics.plasm-ph",
    "all:braid AND all:anyon AND cat:quant-ph",
]

FIELD_PATTERNS = {
    "anyons": re.compile(r"\banyon", re.I),
    "tqc": re.compile(r"topological quantum|quantum double|surface code|fault[- ]tolerant", re.I),
    "majorana": re.compile(r"majorana|kitaev chain|zero mode", re.I),
    "braid-knot": re.compile(r"\bbraid|\bknot theory|fusion space", re.I),
    "topology": re.compile(r"topological order|toric code|tqft", re.I),
    "fracton": re.compile(r"fracton|haah|x-cube|subsystem symmetr", re.I),
    "time-crystal": re.compile(r"time crystal|floquet", re.I),
    "plasma": re.compile(r"tokamak|plasma|elm|stellarator", re.I),
    "holography": re.compile(r"holograph|ads/cft|tensor network code", re.I),
    "fusion-quantum": re.compile(r"fusion|q\s*=|lawson|aneutronic", re.I),
}

NS = {"a": "http://www.w3.org/2005/Atom"}


def tag(text: str) -> list[str]:
    hits = [name for name, pat in FIELD_PATTERNS.items() if pat.search(text)]
    return hits or ["tqc"]


def fetch_query(q: str, n: int = 12) -> list[dict]:
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {
            "search_query": q,
            "start": 0,
            "max_results": n,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
    )
    req = urllib.request.Request(url, headers={"User-Agent": "DBE-Observatory/1.0"})
    with urllib.request.urlopen(req, timeout=40) as resp:
        xml = resp.read()
    root = ET.fromstring(xml)
    out = []
    for entry in root.findall("a:entry", NS):
        aid = (entry.findtext("a:id", default="", namespaces=NS) or "").split("/abs/")[-1]
        title = " ".join((entry.findtext("a:title", default="", namespaces=NS) or "").split())
        summary = " ".join((entry.findtext("a:summary", default="", namespaces=NS) or "").split())
        authors = [
            au.findtext("a:name", default="", namespaces=NS) or ""
            for au in entry.findall("a:author", NS)
        ]
        published = (entry.findtext("a:published", default="", namespaces=NS) or "")[:10]
        fields = tag(title + " " + summary)
        first = summary.split(". ")[0].strip()
        out.append(
            {
                "id": aid,
                "title": title,
                "authors": authors[:8],
                "date": published,
                "url": f"https://arxiv.org/abs/{aid}",
                "fields": fields,
                "coreIdea": first + ".",
                "whyItMatters": "Live ingest; score against DBE pillars before promotion.",
                "limitation": "Preprint. Heuristic tags and scores; not a peer-review verdict.",
                "source": "arXiv API",
                "importance": 52,
                "confidence": 58,
                "popularity": 70,
                "role": "week",
                "foundational": False,
                "tags": ["live", *fields],
            }
        )
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lookback-days", type=int, default=7)
    parser.add_argument("--out-dir", type=Path, default=ROOT / "runs")
    args = parser.parse_args()
    cutoff = datetime.now(timezone.utc) - timedelta(days=args.lookback_days)

    seen: set[str] = set()
    papers: list[dict] = []
    for q in QUERIES:
        try:
            batch = fetch_query(q)
        except Exception as exc:  # noqa: BLE001
            print(f"query failed: {q}: {exc}", file=sys.stderr)
            continue
        for paper in batch:
            if paper["id"] in seen:
                continue
            seen.add(paper["id"])
            try:
                dt = datetime.fromisoformat(paper["date"]).replace(tzinfo=timezone.utc)
            except ValueError:
                continue
            if dt >= cutoff:
                papers.append(paper)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    payload = {
        "startedAt": datetime.now(timezone.utc).isoformat(),
        "lookbackDays": args.lookback_days,
        "feeds": FEEDS,
        "count": len(papers),
        "papers": papers,
        "notes": (
            "Foundational pillars stay in catalog.json (any date). "
            "This run only captures the sliding lookback window."
        ),
    }
    dest = args.out_dir / f"{stamp}.json"
    dest.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"wrote {dest} ({len(papers)} papers, lookback={args.lookback_days}d)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
