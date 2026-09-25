# Research Observatory

Three layers, never mixed into one score bar:

1. **Library** — `catalog.json` papers with tags, fields, 0–100 harvest gauges, and a plain-language triple (core idea / why it matters / one limitation).
2. **Claims** — `claims.json` frozen C/T/D/A table (E-S3, E-QEC, E-RL, …). Heuristic gauges are not C.
3. **Version log** — `versions.json` + `CHANGELOG.md`. DBE and DBE-S version separately.

Current freeze: **DBE-0.2.2** / **DBES-0.2.0** (reviewed 25 Sep 2026; no version bump).

The viewable tab (`lab.html` + `lab.js`) hosts five layers:

- **Mission** — pillar strength (▲/▼ this week), dependencies, blockers, bridge papers, Q=1000 milestone path.
- **Papers** — same catalog. Range chips: week / month / year / all / foundational.
- **Daily** — KEEP / HOLD / CUT / ADD. Auto-Gate A1–A8. INCLUDE can PATCH. STRENGTHEN cannot raise C unless the gate passes. NEW PILLAR / CUT reversal never auto-bumps.
- **Engine** — current DBE / DBE-S freeze + claims + version log.
- **Q ledger** — terms, feeds, ingest runs.

Command strip above the tabs: freeze versions, publish readiness (min KEEP C), this-week count, waiting auto-add, open blockers. Harvest gauges are ingest metadata. They do not move C.

```sh
python research/ingest.py --lookback-days 365
python research/ingest.py --lookback-days 7
python research/fetch_arxiv.py --days 7
python research/score.py --bind E-S3 --action INCLUDE --paper lo-2026 --venue nature
python cli/research_observatory.py
cd research && python -m http.server 8000
```

Fields: Anyons, TQC, Majorana, braid/knot theory, topology, fracton memory, time crystals, plasma control, holography, fusion–quantum integration (Q = 1000 is a ledger stress test, not an output).

Foundational papers are pillars of any age. Live ingest never deletes them. New load-bearing ideas are queued as pillars — they need an interface contract before a MAJOR bump.

High harvest rank (importance ≥ 85 and confidence ≥ 80) on a KEEP/HOLD claim prompts an INCLUDE. Low-C / CUT sections are taken out of the engine view. Coupling is a new claim and starts at C1.
