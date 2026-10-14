# DBE GitHub Pages portal

## Publishing source
GitHub Pages publishes from the repository branch `feature/research-grade-physics` at the repository root. This is supported by successful `pages build and deployment` workflows on that branch, most recently before this change at commit `4cbf04020ea384527d348880ab4a34dc5d1eac74`. The root `index.html` is a static portal; no SDBES or scientific branch is merged.

Public routes:
- `https://pjrny.github.io/DBE_V0/`: repository project hub.
- `https://pjrny.github.io/DBE_V0/research/lab.html`: existing interactive Observatory (untouched).
- `https://pjrny.github.io/DBE_V0/dimensions/`: static public-facing Dimensions Beyond Energy research abstract.

## Sources and update policy
The new `dimensions/index.html` is an exact byte-for-byte mirror of `index.html` from the `dimensions-beyond-energy` branch at `41e0122fc10cf437b9e8cfa9c0b2357f850041dd`, blob `38868b59145591d978f2412d875ab604a711d884`. This is a pinned snapshot: updates to the originating branch do **not** automatically update the mirror. The CI source-hash test deliberately fails if a future edit silently changes the copy. To update it, explicitly review a new snapshot and its source hash together.

The hub's project summaries were written from the root READMEs of `SDBES`, `feature/research-grade-physics`, and `dimensions-beyond-energy` as read on 2026-10-14. They are intentionally short; follow the linked branch READMEs for full detail. The main branch's Python simulator is not a browser site.

## Observatory preservation
The existing `research/lab.html`, `research/lab.js` and the Observatory JSON files remain on the publishing branch. The new landing page links to them using relative project-site paths, so it works at `/DBE_V0/`. Changes to this portal must not rewrite the frozen research ledger or browser-side data just to make a link look functional.

## Future V8 navigator
The SDBES `navigator/index.html` is a Vite/React **source entry point**, not a standalone deployable HTML file. It must be built with the correct GitHub Pages base path before a public `/navigator/` link can be offered. The portal currently links to the repository source and labels its web deployment pending. Once a tested production bundle is published, replace the source-only launch card with the live URL.

## Checks
- `python -m pytest -q tests/test_pages_hub.py` verifies local destinations, source snapshot integrity, README links, and Observatory asset dependencies.
- Existing Python package CI also runs the page tests.
- GitHub's separate `pages build and deployment` job confirms Pages publication from the configured source. A successful source commit does not, by itself, guarantee the live site was deployed.
