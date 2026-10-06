# Changelog

## [Unreleased]
### Fixed
- `research/score.py` venue gate. The venue is now normalised for case and whitespace before routing, so `--venue arXiv`, `ARXIV` and `arxiv` are all a bare preprint. Before, the case-sensitive check treated `arXiv` as a journal and printed "AUTO-MERGED PATCH" for an arXiv INCLUDE. A bare arXiv or preprint venue now never passes A5 and never raises C. Unit tests in `tests/test_research.py` cover the three spellings. Tooling only: no paper version bump, C unchanged, DBE-0.2.2 / DBES-0.2.0 stand.
- Research catalog metadata. Rothstein 2026 has the correct Nuclear Fusion DOI and title. The Nat. Commun. placeholder is now Minev et al. 2025 (Fibonacci anyon braiding). PRC 109 and PRC 110 carry their real titles and authors. The Floquet-tunnelling entry is Phys. Rev. Research 6, 023056 (2024). Levaillant's venue is PRA 92, 012301. Jennings has its DOI and is no longer bound to E-RL. Bravyi–Haah and Almheiri carry their publication years. Crossref DOIs were added to the pillar papers, and Ashwin is corrected to Ashvin Vishwanath.
- Duplicate catalog rows merged with aliases, so old ids still resolve (Han, Shutty, Gattu–Jain, Floquet-fracton/Soule). The Seo duplicate review card is marked. No claim or pillar evidence id dangles.

### Added
- `research/OBSERVATORY_PROMPT.md`, the canonical daily Observatory prompt (v2). The automation reads it at the start of every run, and it is edited only by PR. `research/OBSERVATORY_STARTER.md` holds a copy of the short starter text for the automation prompt box, which points the agent at this file. Tooling only: no paper version bump.
- 15 catalog rows: 5 restored rows that claim evidence cited but the 84383ff rebuild had dropped (including perez-fadon-2026), 8 triaged ADD papers queued as HOLD, and 2 reading-list papers. Inferred gauges and bindings are listed in each row's `inferred` field.

### Changed
- Catalog status now matches the claim freeze. The floquet-clock and fracton-memory pillars are CUT. The spacetime-fractons, spacetime-fracton-codes and fracton-holography pillars are CUT. All six E-HOL papers (including Maldacena 1997) and floquet-fracton-2026 are REJECT (reading list). Jennings is REJECT because it supports no claim. The DBE white paper is CUT on the E-5 denylist and kept as the audit source. The floquet-majorana-codes pillar (rejected 2026-09-21) and the expired cyclic-fusion-family, nonabelian-qldpc and topo-dynamics pillars are CUT. `tamiya-coherent-2026` resolves as an alias of tamiya-2026. No paper version bump. C unchanged. DBE-0.2.2 / DBES-0.2.0 stand.
- README and docs/research/OBSERVATORY.md freeze text now read E-TC and E-FR as CUT (DBE-0.2.0).


## [0.4.16] - 2026-10-06
### Added
- Daily observatory run (lookback 7 days). No paper version bump. Yesterday's unscored pile is scored first. Ten error-layer notes are queued under E-QEC only, including a Floquet-code circuit that is not used as a clock. A DIII-D world model is queued with no coil command. A Vlasov-Maxwell symmetry note is queued with no plant Q. A Majorana shutter is queued as not an X+Z logical. Sixteenfold-way decoherence is queued under the braid claim only. Exact recovery for non-Abelian surface codes is queued as a bridge, so the coupling stays at C1. Two holographic tensor-network papers are rejected on the denylist. The 5 Oct listing is in and left mostly unscored. C unchanged. DBE-0.2.2 / DBES-0.2.0 stand.

### Changed
- Command-strip date stamp moved to 2026-10-06 so this-week counts the new harvest.

## [0.4.15] - 2026-10-05
### Added
- Daily observatory run (lookback 7 days). No paper version bump. The 2 Oct listing is in; yesterday's unscored pile is scored first. Continuous QEC thermodynamics and a deformed toric-code norm are queued under the error layer only. Seven holographic papers are rejected on the denylist. A fusion-category dimension bound, a transmon exchange pulse, a phase-only symmetry, a lattice-Boltzmann syndrome, a graphene Floquet gap, and a quasisymmetric-field construction are rejected as not the bound claim. C unchanged. DBE-0.2.2 / DBES-0.2.0 stand.

### Changed
- Command-strip date stamp moved to 2026-10-05 so this-week counts the new harvest.
## [0.4.14] - 2026-10-04
### Added
- Weekly observatory run (lookback 7 days, Sunday sources on). No paper version bump. No 2-4 Oct arXiv listing yet. The 3 Oct unscored pile is scored: qLDPC and surface-code papers are queued under the error layer only, loss-cone learning and a vacuum response are queued with no coil command, Chern-band composite fermions and a 1D anyon chain are queued without replacing fusion, and a zonal-flow formula is queued with no plant Q. A driven holographic superfluid is rejected. C unchanged. DBE-0.2.2 / DBES-0.2.0 stand.

### Changed
- Command-strip date stamp moved to 2026-10-04 so this-week counts the new harvest.

## [0.4.13] - 2026-10-03
### Added
- Daily observatory run (lookback 7 days). No paper version bump. No Friday or Saturday arXiv listing. Phys. Rev. X mixed-state axioms are queued under the error layer only. Twisted quantum-double stabilizers, constant-depth atom-array surgery, and a toric-code electric-magnetic Clifford no-go are queued under the same layer. DIII-D island-chain transport is queued with no coil command. A polarized parafermion trench is queued as not an X+Z logical. A fractonic fluid and an axionic holographic superconductor are rejected. C unchanged. DBE-0.2.2 / DBES-0.2.0 stand.

### Changed
- Command-strip date stamp moved to 2026-10-03 so this-week counts the new harvest.

## [0.4.12] - 2026-10-02
### Added
- Daily observatory run (lookback 7 days). No paper version bump. The 1 Oct listing is scored: DIII-D control-model latency is queued, a one-shot qLDPC lift and photonic lattice surgery are queued under the error layer only, a Majorana-edge capacitance is queued as not an X+Z logical, anyon proliferation is queued without replacing fusion, and an equivalent-tokamak ITG map is queued with no plant Q. Booklet holography, a chemistry Majorana ansatz, and Floquet simulation-as-clock are rejected. C unchanged. DBE-0.2.2 / DBES-0.2.0 stand.

### Changed
- Command-strip date stamp moved to 2026-10-02 so this-week counts the new harvest.

## [0.4.11] - 2026-10-01
### Added
- Daily observatory run (lookback 7 days). No paper version bump. The 30 Sep listing is scored: a fault-tolerant-phase no-go for solvable anyon orders is queued as a bridge, qLDPC list decoding and syndrome schedules are queued, a Rydberg gap is queued without replacing fusion, and a runaway-electron wall screen is queued. Haah-code thermalization, a classical time crystal, and holographic QCD are rejected. C unchanged. DBE-0.2.2 / DBES-0.2.0 stand.

### Changed
- Command-strip date stamp moved to 2026-10-01 so this-week counts the new harvest.

## [0.4.10] - 2026-09-30
### Added
- Daily observatory run (lookback 7 days). No paper version bump. The 29 Sep listing is scored: qLDPC decoder routing with an H2 check, a KSTAR dropout reconstruction, a Kunwu CBET/SBS shot, qLDPC distance amplifiers, and one-dimensional anyons are queued. Holographic turbulence and a dissipative Floquet spectrum are rejected. C unchanged. DBE-0.2.2 / DBES-0.2.0 stand.

### Changed
- Command-strip date stamp moved to 2026-09-30 so this-week counts the new harvest.

All notable changes to this project will be documented in this file.

## [0.4.9] - 2026-09-29
### Added
- Daily observatory run (lookback 7 days). No paper version bump. The 26–28 Sep listing is scored: EXL-50U isoflux MPC, a diagnostic packet twin, Vlasov and ITG solvers, GKP-qLDPC circuits, and a toric-code no-go are queued. A laser p-11B alpha source is queued as not Floquet tunneling. Time crystals, holography, a qubit battery, and a Rep(D8) entangler are rejected. C unchanged. DBE-0.2.2 / DBES-0.2.0 stand.

### Changed
- Command-strip date stamp moved to 2026-09-29 so this-week counts the new harvest.

All notable changes to this project will be documented in this file.

## [0.4.8] - 2026-09-28
### Added
- Daily observatory run (lookback 7 days). No paper version bump. D4 twisted-sheaf qLDPC, KSTAR single-shot H-mode error-field identification, TCV edge-Er drift, decohered GKP correction, and measurement-based uncomputation are queued. Holography, a Floquet skin effect, and photonic graph-state fusion are rejected. C unchanged. DBE-0.2.2 / DBES-0.2.0 stand.

### Changed
- Command-strip date stamp moved to 2026-09-28 so this-week counts the new harvest.

All notable changes to this project will be documented in this file.

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
