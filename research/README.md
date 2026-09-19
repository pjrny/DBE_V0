# Research Observatory

Catalog, tag, score, and brief the papers that lift DBE V0 → V1 and DBE-S.

Fields: Anyons, TQC, Majorana, braid/knot theory, topology, fracton memory, time crystals, plasma control, holography, fusion–quantum integration (Q = 1000).

```sh
# first runs look back a year or more
python research/ingest.py --lookback-days 365

# daily
python research/ingest.py --lookback-days 7

# interactive CLI tab
python cli/research_observatory.py
python cli/research_observatory.py --field anyons --role week --sort importance

# viewable HTML tab (same folder as catalog.json)
cd research && python -m http.server 8000
# open http://localhost:8000/lab.html
```

Foundational papers are pillars and may be any age. Live ingest never deletes them. If a paper is load-bearing rather than a citation, the catalog suggests a new pillar.

Each paper has:

- tags and field segments
- importance / confidence / popularity (0–100)
- a plain-language core idea, why it matters for DBE, and one limitation
