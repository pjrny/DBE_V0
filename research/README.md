# DBE Research Lab

Interactive catalog of core papers and daily arXiv runs for the DBE fields:

Anyons, TQC, Majorana, braid/knot theory, topology, fracton memory, time crystals, plasma control, holography, fusion–quantum integration.

## View

Open `research/lab.html` in a browser (works offline; uses the embedded catalog). Tabs:

- **All / Pillars / This week / Year lookback**
- Field filter, search, sort by importance / confidence / popularity

Each card: plain-language core idea, why it matters, one limitation, DBE link, scores.

## Refresh from arXiv

```sh
python research/fetch_arxiv.py --days 400 --max 20   # first runs
python research/fetch_arxiv.py --days 7 --max 15     # daily
```

Writes into `research/catalog.json`. Re-open `lab.html` or serve the folder if you want live `catalog.json` fetch.

Feeds: quant-ph, cond-mat.str-el, cond-mat.mes-hall, hep-th, physics.plasm-ph.

Foundational tagged papers are pillars. `fetch_arxiv.py` does not auto-promote pillars; add them in `catalog.json` when a paper should lift a field.
