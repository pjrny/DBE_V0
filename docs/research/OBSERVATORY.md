# Research Observatory

Interactive catalog of sources that lift the DBE pillars:

Anyons, TQC, Majorana, braid/knot theory, topology, fracton memory, time crystals, plasma control, holography, fusion–quantum integration.

## What a daily run does

1. Query arXiv feeds:
   - https://arxiv.org/list/quant-ph/recent
   - https://arxiv.org/list/cond-mat.str-el/recent
   - https://arxiv.org/list/cond-mat.mes-hall/recent
   - https://arxiv.org/list/hep-th/recent
   - https://arxiv.org/list/physics.plasm-ph/recent
   - https://arxiv.org/search/advanced
2. Tag every hit against the ten fields.
3. Score **importance** (how much it lifts a DBE pillar toward Q = 1000), **confidence** (peer review / experiment vs theory / known disputes), and **popularity** (venue + recency-weighted attention).
4. Write a plain-language triple: core idea, why it matters, one limitation.
5. **Foundational** papers are never aged out. First runs use `--lookback-days 365` (or more).
6. If a paper is not just a citation but a new load-bearing idea, suggest a **new pillar**.

## Commands

```sh
python research/ingest.py --lookback-days 365
python cli/research_observatory.py
python cli/research_observatory.py --field anyons --role week
```

Program manuscripts (DBE white paper, DBE-S revision) sit in the catalog as `role: internal`. They are scored with lower confidence on purpose.

## Q = 1000

DBE-S forbids naive WKB, unbounded cross-section scaling, perfect coherence, and missing Bremsstrahlung. Papers that ignore those loss channels cannot validate Q = 1000 and should not be promoted to pillars.
