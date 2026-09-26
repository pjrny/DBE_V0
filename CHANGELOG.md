# Changelog

## [0.4.6] - 2026-09-26
### Added
- Daily observatory run (lookback 7 days). No paper version bump. Ultra-high-rate quantum codes, chromatic dynamical decoupling, WEST ICRF edge singularities, and a gyrokinetic saturation-rule solver are queued. C unchanged. DBE-0.2.2 / DBES-0.2.0 stand.

### Changed
- Command-strip date stamp moved to 2026-09-26 so this-week counts the new harvest.

All notable changes to this project will be documented in this file.

## [0.4.5] - 2026-09-25
### Added
- Daily observatory run (lookback 7 days). No paper version bump. Non-Abelian sheaf qLDPC, ITER quasi-symmetric error-field correction, and a pair-density-wave Majorana lattice are queued. C unchanged. DBE-0.2.2 / DBES-0.2.0 stand.

### Changed
- Command-strip date stamp moved to 2026-09-25 so this-week counts the new harvest.

## [0.4.4] - 2026-09-24
### Added
- Daily observatory run (lookback 7 days). No paper version bump. ITB–RMP confinement trade-off, a SOLPS-ITER surrogate, JET pedestal Alfvén modes, KSTAR electron-cyclotron startup, a Dijkgraaf–Witten rank bound, and a quantum-dot Majorana coherence simulation are queued. C unchanged. DBE-0.2.2 / DBES-0.2.0 stand.

### Changed
- Command-strip date stamp moved to 2026-09-24 so this-week counts the new harvest.

## [0.4.3] - 2026-09-23
### Added
- Daily observatory run (lookback 7 days). No paper version bump. Gay–Jeronimo qLTCs, the plasma-staircase criterion, Haagerup–Izumi categories, and dynamically assisted Schwinger pair production are queued. C unchanged. DBE-0.2.2 / DBES-0.2.0 stand.

### Changed
- Command-strip date stamp moved to 2026-09-23 so this-week counts the new harvest.

## [0.4.2] - 2026-09-22
### Changed
- Observatory collapsed to five tabs (Mission, Papers, Daily, Engine, Q ledger). Week/month/year are chips, not tabs.
- Command strip above tabs: freeze, publish readiness, min KEEP C, this-week count, auto-add queue, blockers.
- Mission tab draws pillar strength, week delta, dependencies, blockers, and bridge papers that couple two or more claims.
- Daily cards speak KEEP / HOLD / CUT / ADD against the same catalog. No rebuild.

## [0.4.1] - 2026-09-20
### Added
- Follow-on harvest: DIII-D error-field ramp-up, kobra Vlasov, NIF Q_sci=4.13, ASPT on processors, MAST-U PCS integration notes.
- DBE-0.1.2 / DBES-0.1.2 PATCH bibliography. No C moves. E-HOL denylist held.

## [0.4.0] - 2026-09-20
### Added
- Confidence-framework freeze: `research/claims.json` (C/T/D/A), `research/versions.json`, `research/reviews.json`, `research/ledger.json`.
- Daily review cards under `research/reviews/2026-09-20/` with G1–G6, disputer, and protocol route.
- `research/score.py` — protocol scorer that refuses to treat harvest 0–100 gauges as C.
- Observatory HTML tab now has Claims, Versions, Reviews, and Ledger layers. Heuristic gauges are labeled as harvest metadata.

### Changed
- Catalog expanded with this week's arXiv, year lookback, PRC 109/110 Layer-2 bounds, Seo 2024 tearing RL, and S3-adjacent reconstruction papers.
- Pillars recut to engine status: KEEP / WATCH / HOLD / CUT / QUEUE. Holography and the five-head monolith stay CUT. Q = 1000 is a ledger test, not an output.
- DBE-0.1.1 / DBES-0.1.1 PATCH INCLUDE for 2026-09-20. Spacetime-fractons queued as a new pillar (no auto-bump).

## [0.3.1] - 2026-09-19
### Changed
- Research Observatory HTML tab (`research/lab.html`) now matches the catalog schema: core idea / why it matters / limitation, importance–confidence–popularity gauges, field chips, this week / month / year lookback / pillars / catalog / daily runs / suggested pillars.
- Catalog expanded to 50+ papers including Kitaev 1997/2001/honeycomb, Nayak 2008, S₃ Nature 2026, Lyons–Brown, DBE V1 and DBE-S (lower confidence), plus this week’s arXiv (Tamiya, Polley, Jennings, …).
- Suggested pillars now include cyclic fusion universality, Floquet–Majorana codes, fracton holography, non-Abelian qLDPC, and topological hardware for dynamics.

## [0.3.0] - 2026-09-19
### Added
- Research Lab (`research/lab.html` + `research/catalog.json`) with tabs for All / Pillars / This week / Year lookback / Recent.
- Per-paper tags, field segments, importance / confidence / popularity scores, plain-language core idea, why it matters, one limitation, and DBE link.
- Seed catalog: Kitaev 1997, Nayak 2008, S3 Nature 2026 hardware gates, Lyons–Brown fault-tolerance, week’s coherent-error threshold and modular DQC stack, Majorana braid sims, semi-holographic time crystals, DBE-S Q=1000 and V0 architecture.
- Suggested new pillars: Haah/X-cube fracton memory; Floquet time crystals.
- `research/fetch_arxiv.py` daily/year lookback ingest from quant-ph, cond-mat.str-el, cond-mat.mes-hall, hep-th, physics.plasm-ph.

## [0.2.0] - 2025-08-20
### Added
- Created a modular package structure for the DBE research simulator with subpackages for plasma physics, actuators, quantum subsystems, controller logic and risk analysis.
- Implemented a radial grid and 1D energy transport model with Spitzer resistivity, shear-dependent diffusivity and ELM triggers.
- Added models for resonant magnetic perturbation coils and pellet injectors to adjust edge stability and pacing ELMs.
- Added quantum subsystem stubs representing Majorana qubit registers, fracton memory, a time-crystal clock and a holographic encoder.
- Added a DBE controller that uses the quantum subsystems to decide actuator inputs based on plasma stability.
- Added a risk analyzer that computes a risk score based on stability, actuator saturation, pellet availability and memory errors.
- Added a batch runner CLI script to generate synthetic runs and output risk analysis datasets.
- Added extensive documentation in `docs/` covering the physics model, system architecture and example scenarios.
- Added continuous integration with GitHub Actions to run the test suite on each push.
- Added test suites covering plasma physics functions, actuators, quantum subsystems, controller logic and risk analysis.

### Changed
- Updated the top-level README to describe the research-grade simulator and how to run batch jobs.
- Refactored the code base into separate modules under the `dbe` package.
- Added CLI tools for running batch simulations and baseline comparisons.

### Fixed
- Various minor improvements and bug fixes to ensure deterministic simulation outputs and correct pellet scheduling.

### Known Limitations
- The transport model remains a simplified single-fluid treatment; no 2D MHD or kinetic effects are included.
- Quantum subsystem implementations are illustrative and do not perform actual quantum computation.
- Risk model thresholds and penalties are heuristic and should be calibrated with real data in the future.
- Research-lab harvest scores are editorial heuristics, not C/T/D/A and not citation metrics.
