# DBE Fusion Stability Simulator (Research Grade)

This project implements a research-grade simulation of a fusion plasma discharge controlled by a **Dimensional Braid Engine (DBE)**. It combines a simplified magnetohydrodynamic (MHD) transport model with models of advanced quantum subsystems and realistic actuators to explore how a DBE might stabilise tokamak plasmas by predicting and mitigating instabilities.

## Research Observatory (papers tab)

Three-layer source ledger for Anyons, TQC, Majorana, braid/knot theory, topology, fracton memory, time crystals, plasma control, holography, and fusion–quantum integration (DBE V1 / DBE-S). **Library papers, C/T/D/A claims, and the version log are separate.** Harvest importance / confidence / popularity (0–100) are catalog metadata. They are not C, T, D, or A and cannot bump a paper version.

```sh
cd research && python -m http.server 8000
# open http://localhost:8000/lab.html

python research/ingest.py --lookback-days 365   # first-run year lookback
python research/ingest.py --lookback-days 7     # daily harvest (library only)
python research/score.py --bind E-S3 --action INCLUDE --paper lo-2026 --venue nature
python cli/research_observatory.py              # library
python cli/research_observatory.py --tab claims
python cli/research_observatory.py --tab versions
```

Tabs: This week / This month / Year lookback / Catalog / Claims / Versions / Reviews / Ledger / Pillars / Daily runs. Each paper is tagged, segmented, and carries a plain-language core idea, why it matters, and one limitation. Foundational papers are pillars of any age; new load-bearing ideas are queued as pillars (NEW PILLAR never auto-bumps). Reviews can APPLY INCLUDE (PATCH) or queue STRENGTHEN / NEW PILLAR against a local working freeze.

**2026-09-19 freeze (claim table of record):** KEEP S3 braid+fusion, surface-code QEC, RL plant control. WATCH Majorana. HOLD fracton-as-hardware and time-crystal-as-clock. CUT holography and the five-head engine. Q = 1000 is a ledger stress test, not an output.

Feeds: [quant-ph](https://arxiv.org/list/quant-ph/recent), [cond-mat.str-el](https://arxiv.org/list/cond-mat.str-el/recent), [cond-mat.mes-hall](https://arxiv.org/list/cond-mat.mes-hall/recent), [hep-th](https://arxiv.org/list/hep-th/recent), [physics.plasm-ph](https://arxiv.org/list/physics.plasm-ph/recent), [advanced search](https://arxiv.org/search/advanced).

See `docs/research/OBSERVATORY.md` and `research/CHANGELOG.md`.

## Highlights

- **Physics core:** A 1-D radial grid with analytic temperature, density and safety-factor profiles evolves under a finite-difference transport equation. A shear-dependent diffusivity suppresses turbulence, and built-in triggers simulate edge localised modes (ELMs) and other instabilities.
- **Actuators:** Models of resonant magnetic perturbation (RMP) coils and pellet injection change the edge stability and temperature profile. Actuator limits (current, pellet size and rate) are respected.
- **Quantum subsystems (simulator stubs):** The Python package still contains illustrative Majorana, fracton, time-crystal, and holographic modules. The observatory freeze above is the claim table of record — those stubs are not KEEP hardware.
- **DBE controller:** The `DBEController` coordinates subsystems and actuators based on plasma stability. Bus A (plant attach) is the only KEEP attach surface today.
- **Risk analysis:** A `RiskAnalyzer` monitors stability, actuator saturation and memory errors, producing a risk score and explanatory notes for each event.
- **Batch runs:** The script in `cli/run_batch.py` runs many randomised scenarios, collects risk scores and outputs a CSV dataset for analysis.
- **Integration API:** The `simulate_event()` function in `dbe_simulation.py` allows embedding the simulation into other frameworks (e.g. web applications).

## Getting started

Clone this repository and install Python 3. No external packages are required. To run an interactive simulation:
```sh
python dbe_simulation.py
```
Follow the prompts to allocate qubits and memory, engage subsystems and execute mitigations. The game will report your cumulative energy gain and risk at the end.

To run a batch of random scenarios and save the results:
```sh
python cli/run_batch.py
```
This will produce `outputs/batch_runs.csv` with one row per run and columns `run_id, stability, coil_fraction, pellet_available, memory_errors, risk_score, notes`. You can adjust the number of runs and parameter ranges in the script.

## Scientific notes

This repository is inspired by the DBE white paper and related literature. The plasma model uses simplified MHD and transport equations and is not intended for operational predictions. The quantum subsystem models demonstrate timing and error-resilience rather than performing real quantum computation. See `docs/THEORY.md` for the simulator, and `docs/research/OBSERVATORY.md` for the paper ledger and freeze.

## Contributing

Contributions are welcome. See the open issues for planned work and feel free to open new issues or pull requests.
