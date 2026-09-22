# Research Observatory

Three layers, never mixed into one score bar:

1. Library papers (`research/catalog.json`) — tags, fields, 0–100 harvest gauges, plain-language triple (core idea / why it matters / one limitation).
2. Frozen claims with C/T/D/A (`research/claims.json`) — the 2026-09-19 Confidence Framework freeze.
3. Version log (`research/versions.json`, `research/CHANGELOG.md`, `CHANGELOG.md`).

Do not mix harvest 0–100 gauges into C. `research/score.py` refuses to treat them as C/T/D/A.

Fields: Anyons, TQC, Majorana, braid/knot theory, topology, fracton memory, time crystals, plasma control, holography, fusion–quantum integration.

## What a daily run does

1. Harvest arXiv feeds (library only — ingest is not a version):
   - https://arxiv.org/list/quant-ph/recent
   - https://arxiv.org/list/cond-mat.str-el/recent
   - https://arxiv.org/list/cond-mat.mes-hall/recent
   - https://arxiv.org/list/hep-th/recent
   - https://arxiv.org/list/physics.plasm-ph/recent
   - https://arxiv.org/search/advanced
2. Bind each paper to 0–2 claim IDs. Zero → REJECT or NEW-PILLAR queue. More than two → split or treat as coupling (C1).
3. Run G1–G6. Fail any one and the paper cannot RAISE a score. It may still LOWER one.
4. Write a review card under `research/reviews/YYYY-MM-DD/` (core idea / why / limitation / disputer / ledger numbers). A card without DISPUTER and GATES is void.
5. INCLUDE → PATCH bibliography. WEAKEN/DISCONFIRM apply immediately. STRENGTHEN only auto-merges at C≥4 on a journal/hardware venue. NEW PILLAR never auto-bumps.

First runs use `--lookback-days 365`. Foundational pillars are never aged out. Program manuscripts (DBE white paper, DBE-S revision) sit in the catalog as `role: internal` with lower harvest confidence on purpose.

## Freeze (2026-09-19 / 2026-09-20 PATCH)

KEEP: E-S3 (S₃ braid+fusion), E-QEC (surface-code / qLDPC), E-RL (plant-attach control), S-L3 (Vlasov / hole-burning methods).

WATCH: E-MZM (Majorana — not load-bearing).

HOLD: E-TC (time crystal as physics, cut as metronome), E-FR (fracton as theory, cut as hardware), S-L1, S-L2, S-L4.

CUT: E-HOL (holography as reactor/processor part), E-5 (five-head monolith), S-Q as an output. Consciousness benchmarks stay off the engine.

Q_sci, Q_fuel, and Q_eng are different numbers. DBE-S forbids naive WKB, unbounded cross-section scaling, perfect coherence, and missing Bremsstrahlung. Q = 1000 is a ledger stress test, not an output of the current stack.

## Commands

```sh
python research/ingest.py --lookback-days 365
python research/ingest.py --lookback-days 7
python research/score.py --bind E-S3 --action INCLUDE --paper lo-2026 --venue nature
python cli/research_observatory.py
python cli/research_observatory.py --tab claims
python cli/research_observatory.py --tab versions
cd research && python -m http.server 8000   # lab.html tab
```

`lab.html` loads catalog + claims + versions + reviews + ledger. Five tabs only:

- **Mission** — pillar strength / week delta, blockers, bridge papers, Q=1000 milestone bar.
- **Papers** — week / month / year / all / foundational as chips, not tabs.
- **Daily** — KEEP/HOLD/CUT/ADD cards. Auto-Gate A1–A8.
- **Engine** — current DBE / DBE-S freeze, claims, version log.
- **Q ledger** — terms, feeds, ingest runs.

Metrics above the tabs: working freeze, publish readiness (min KEEP C), this-week count, waiting auto-add, open blockers.

APPLY on a review card writes a **local working freeze** (localStorage). INCLUDE patches; NEW PILLAR queues. Reset freeze restores published DBE-0.2.2 / DBES-0.2.0.

Pillar bars mix engine status + bound-claim C + this week's INCLUDE vs WEAKEN. They are not C. A paper that binds two claims is a bridge; coupling starts at C1.
