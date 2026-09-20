#!/usr/bin/env python3
"""Daily / lookback arXiv ingest for the DBE research lab.

Heuristic 0–100 importance / confidence / popularity scores written here are
harvest metadata. They are NOT C, T, D, or A and must not enter claims.json.
Physics confidence lives on a named claim ID (see score.py and the Version
Control Protocol). Ingest is not a version.

Usage:
  python research/fetch_arxiv.py              # last 7 days
  python research/fetch_arxiv.py --days 400   # first-run lookback
  python research/fetch_arxiv.py --max 20
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CATALOG = ROOT / "catalog.json"

HARVEST_NOTE = (
    "Heuristic importance/confidence/popularity are harvest metadata. "
    "They do not equal C/T/D/A and cannot raise C."
)

QUERIES = {
    "anyons": 'all:anyon OR all:"quantum double" OR all:"non-Abelian"',
    "tqc": 'all:"topological quantum computation" OR all:"topological quantum computing"',
    "majorana": 'all:"Majorana zero mode" OR all:"Majorana braiding"',
    "braid-knot": "all:braiding AND (all:anyon OR all:Majorana OR all:knot)",
    "topology": 'all:"topological order" OR all:"toric code"',
    "fracton": 'all:fracton OR all:"Haah code" OR all:"X-cube"',
    "time-crystal": 'all:"time crystal" OR all:Floquet',
    "plasma": "all:tokamak AND (all:control OR all:ELM OR all:RMP)",
    "holography": "all:holographic AND (all:encoding OR all:AdS OR all:plasma)",
    "fusion-quantum": "all:fusion AND (all:quantum OR all:qubit)",
}

KEYWORD_FIELDS = [
    ("anyon", "anyons"),
    ("quantum double", "anyons"),
    ("topological quantum", "tqc"),
    ("majorana", "majorana"),
    ("braid", "braid-knot"),
    ("knot", "braid-knot"),
    ("fracton", "fracton"),
    ("haah", "fracton"),
    ("time crystal", "time-crystal"),
    ("floquet", "time-crystal"),
    ("tokamak", "plasma"),
    ("plasma", "plasma"),
    ("holograph", "holography"),
    ("ads/cft", "holography"),
    ("fusion", "fusion-quantum"),
]


def atom_text(el, tag):
    child = el.find(f"{{http://www.w3.org/2005/Atom}}{tag}")
    return (child.text or "").strip() if child is not None else ""


def fetch_query(query: str, max_results: int, start: int = 0) -> list[dict]:
    params = {
        "search_query": query,
        "start": start,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "DBE-research-lab/0.3"})
    with urllib.request.urlopen(req, timeout=45) as resp:
        raw = resp.read()
    root = ET.fromstring(raw)
    out = []
    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        aid = atom_text(entry, "id")
        m = re.search(r"arxiv.org/abs/([^v]+)", aid)
        arxiv_id = m.group(1) if m else aid.rsplit("/", 1)[-1]
        title = re.sub(r"\s+", " ", atom_text(entry, "title"))
        summary = re.sub(r"\s+", " ", atom_text(entry, "summary"))
        published = atom_text(entry, "published")[:10]
        authors = [
            a.findtext("{http://www.w3.org/2005/Atom}name") or ""
            for a in entry.findall("{http://www.w3.org/2005/Atom}author")
        ]
        out.append(
            {
                "arxiv": arxiv_id,
                "title": title,
                "authors": authors[:8],
                "published": published,
                "year": int(published[:4]) if published else None,
                "url": f"https://arxiv.org/abs/{arxiv_id}",
                "summary": summary,
            }
        )
    return out


def tag_fields(title: str, summary: str) -> list[str]:
    blob = f"{title} {summary}".lower()
    fields = []
    for key, field in KEYWORD_FIELDS:
        if key in blob and field not in fields:
            fields.append(field)
    return fields or ["topology"]


def score(paper: dict, field_hint: str) -> tuple[int, int, int]:
    """Harvest 0–100 gauges. Not C/T/D/A. Cannot raise a frozen claim."""
    blob = f"{paper['title']} {paper.get('summary','')}".lower()
    importance = 50
    if any(w in blob for w in ("universal", "threshold", "fault-tolerant", "braiding")):
        importance += 18
    if any(w in blob for w in ("experiment", "processor", "hardware", "tokamak")):
        importance += 12
    if field_hint in ("anyons", "tqc", "majorana", "fusion-quantum"):
        importance += 8
    importance = min(95, importance)
    confidence = 70 if "proof" in blob or "theorem" in blob else 62
    if "simulation" in blob:
        confidence = max(confidence - 4, 50)
    popularity = min(90, 55 + importance // 5)
    return importance, confidence, popularity


def explain(paper: dict) -> tuple[str, str, str]:
    s = paper.get("summary") or ""
    first = s.split(". ")[0][:280]
    plain = first + ("." if not first.endswith(".") else "")
    why = "Touches a DBE pillar (anyons / TQC / Majorana / plasma / holography / clocks). Score against a named claim before it can move C."
    lim = "arXiv preprint — harvest gauges only. Not a C/T/D/A verdict until bound and gated."
    return plain, why, lim


def load_catalog() -> dict:
    if CATALOG.exists():
        return json.loads(CATALOG.read_text())
    return {"papers": [], "pillars": [], "fields": [], "protocol": {"note": HARVEST_NOTE}}


def merge(cat: dict, incoming: list[dict]) -> int:
    existing = {p.get("arxiv") or p.get("id") for p in cat["papers"]}
    added = 0
    for p in incoming:
        key = p.get("arxiv") or p.get("id")
        if not key or key in existing:
            continue
        cat["papers"].append(p)
        existing.add(key)
        added += 1
    return added


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--max", type=int, default=15)
    args = ap.parse_args()
    cutoff = datetime.now(timezone.utc) - timedelta(days=args.days)
    cat = load_catalog()
    harvested = []
    for field, q in QUERIES.items():
        try:
            rows = fetch_query(q, args.max)
        except Exception as exc:
            print(f"[warn] {field}: {exc}", file=sys.stderr)
            continue
        for row in rows:
            try:
                pub = datetime.fromisoformat(row["published"]).replace(tzinfo=timezone.utc)
            except Exception:
                continue
            if pub < cutoff:
                continue
            fields = tag_fields(row["title"], row["summary"])
            if field not in fields:
                fields.insert(0, field)
            imp, conf, pop = score(row, field)
            plain, why, lim = explain(row)
            harvested.append(
                {
                    "id": row["arxiv"].replace("/", "-"),
                    "arxiv": row["arxiv"],
                    "title": row["title"],
                    "authors": row["authors"],
                    "year": row["year"],
                    "date": row["published"],
                    "venue": "arXiv",
                    "url": row["url"],
                    "fields": fields,
                    "role": "week" if args.days <= 10 else "lookback",
                    "foundational": False,
                    "tags": ["daily-run", "arxiv", "harvest"],
                    "importance": imp,
                    "confidence": conf,
                    "popularity": pop,
                    "coreIdea": plain,
                    "whyItMatters": why,
                    "limitation": lim,
                    "source": "arXiv API",
                    "claimIds": [],
                    "bindAction": "HOLD",
                }
            )
        print(f"[ok] {field}: scanned {len(rows)} (harvest only; C unchanged)")
    added = merge(cat, harvested)
    cat["generatedAt"] = datetime.now(timezone.utc).isoformat()
    proto = cat.get("protocol") or {}
    proto["note"] = HARVEST_NOTE
    cat["protocol"] = proto
    CATALOG.write_text(json.dumps(cat, indent=2) + "\n")
    print(f"merged {added} new papers → {CATALOG}")
    print("NOTE harvest gauges are not C/T/D/A and cannot raise a frozen claim.")


if __name__ == "__main__":
    main()
