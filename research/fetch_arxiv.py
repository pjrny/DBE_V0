#!/usr/bin/env python3
"""Daily / lookback arXiv ingest for the DBE research lab.

Pulls recent (or year-lookback) records from the DBE field feeds,
tags them, scores importance/confidence/popularity heuristics,
and merges into research/catalog.json.

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

QUERIES = {
    "Anyons": 'all:anyon OR all:"quantum double" OR all:"non-Abelian"',
    "TQC": 'all:"topological quantum computation" OR all:"topological quantum computing"',
    "Majorana": 'all:"Majorana zero mode" OR all:"Majorana braiding"',
    "Braid & Knot Theory": "all:braiding AND (all:anyon OR all:Majorana OR all:knot)",
    "Topology": 'all:"topological order" OR all:"toric code"',
    "Fracton Memory": 'all:fracton OR all:"Haah code" OR all:"X-cube"',
    "Time Crystals": 'all:"time crystal" OR all:Floquet',
    "Plasma Control": "all:tokamak AND (all:control OR all:ELM OR all:RMP)",
    "Holography": "all:holographic AND (all:encoding OR all:AdS OR all:plasma)",
    "Fusion–Quantum Integration": "all:fusion AND (all:quantum OR all:qubit)",
}

KEYWORD_FIELDS = [
    ("anyon", "Anyons"),
    ("quantum double", "Anyons"),
    ("topological quantum", "TQC"),
    ("majorana", "Majorana"),
    ("braid", "Braid & Knot Theory"),
    ("knot", "Braid & Knot Theory"),
    ("fracton", "Fracton Memory"),
    ("haah", "Fracton Memory"),
    ("time crystal", "Time Crystals"),
    ("floquet", "Time Crystals"),
    ("tokamak", "Plasma Control"),
    ("plasma", "Plasma Control"),
    ("holograph", "Holography"),
    ("ads/cft", "Holography"),
    ("fusion", "Fusion–Quantum Integration"),
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
                "authors": ", ".join(authors[:8]),
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
    return fields or ["Topology"]


def score(paper: dict, field_hint: str) -> tuple[int, int, int]:
    blob = f"{paper['title']} {paper.get('summary','')}".lower()
    importance = 50
    if any(w in blob for w in ("universal", "threshold", "fault-tolerant", "braiding")):
        importance += 18
    if any(w in blob for w in ("experiment", "processor", "hardware", "tokamak")):
        importance += 12
    if field_hint in ("Anyons", "TQC", "Majorana", "Fusion–Quantum Integration"):
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
    why = "Touches a DBE pillar (anyons / TQC / Majorana / plasma / holography / clocks)."
    lim = "arXiv preprint — treat claims as unverified until journal or independent replication."
    return plain, why, lim


def load_catalog() -> dict:
    if CATALOG.exists():
        return json.loads(CATALOG.read_text())
    return {"papers": [], "pillars": [], "fields": list(QUERIES)}


def merge(cat: dict, incoming: list[dict]) -> int:
    existing = {p.get("arxiv") or p.get("id") for p in cat["papers"]}
    added = 0
    for p in incoming:
        key = p.get("arxiv")
        if not key or key in existing:
            continue
        cat["papers"].append(p)
        existing.add(key)
        added += 1
    return added


def main():
    ap = argparse.ArgumentParser()
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
                    "venue": "arXiv",
                    "url": row["url"],
                    "fields": fields,
                    "tags": ["daily-run", "arxiv"],
                    "segment": "week" if args.days <= 10 else "year",
                    "importance": imp,
                    "confidence": conf,
                    "popularity": pop,
                    "dbe_link": f"Auto-tagged under {field}.",
                    "plain": plain,
                    "why_matters": why,
                    "limitation": lim,
                    "published": row["published"],
                }
            )
        print(f"[ok] {field}: scanned {len(rows)}")
    added = merge(cat, harvested)
    cat["generated_at"] = datetime.now(timezone.utc).isoformat()
    CATALOG.write_text(json.dumps(cat, indent=2))
    print(f"merged {added} new papers → {CATALOG}")


if __name__ == "__main__":
    main()
