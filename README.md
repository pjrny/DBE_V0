# DBE Fusion Stability Simulator (Research Grade)

This project implements a research-grade simulation of a fusion plasma discharge controlled by a **Dimensional Braid Engine (DBE)**. It combines a simplified magnetohydrodynamic (MHD) transport model with models of advanced quantum subsystems and realistic actuators to explore how a DBE might stabilise tokamak plasmas by predicting and mitigating instabilities.

## Research Observatory

The `research/` tree is a catalog of core papers across Anyons, TQC, Majorana, braid/knot theory, topology, fracton memory, time crystals, plasma control, holography, and fusion–quantum integration.

- `research/catalog.json` — tagged sources with importance, confidence, popularity, plus plain-language core idea / why it matters / limitation.
- `research/ingest.py` — daily arXiv ingest. First runs: `python research/ingest.py --lookback-days 365`.
- `cli/research_observatory.py` — interactive tab to browse the catalog.
- `docs/research/OBSERVATORY.md` — scoring rules, feeds, and the Q = 1000 honesty bar.

Foundational pillars are never aged out. New papers can propose new pillars (cyclic fusion universality, Floquet–Majorana codes, fracton holography, 2D non-Abelian qLDPC, topological dynamics hardware).

```sh
python cli/research_observatory.py
python research/ingest.py --lookback-days 7
python -m unittest tests/test_research.py
```

## Highlights

- **Physics core:** A 1-D radial grid with analytic temperature, density and safety-factor profiles evolves under a finite-difference transport equation. A shear-dependent diffusivity suppresses turbulence, and built-in triggers simulate edge localised modes (ELMs) and other instabilities.
- **Actuators:** Models of resonant magnetic perturbation (RMP) coils and pellet injection change the edge stability and temperature profile. Actuator limits (current, pellet size and rate) are respected.
- **Quantum subsystems:** Topological quantum compute with Majorana braids, fracton memory for robust state storage, a Floquet time crystal for synchronised timing, and a holographic encoder for compressing high-dimensional plasma states.
- **DBE controller:** The `DBEController` coordinates quantum subsystems and actuators based on plasma stability.
- **Risk analysis:** A `RiskAnalyzer` monitors stability, actuator saturation and memory errors.
- **Batch runs:** `cli/run_batch.py` runs randomised scenarios to CSV.
- **Integration API:** `simulate_event()` in `dbe_simulation.py` embeds the simulation in other frameworks.

## Getting started

Clone this repository and install Python 3. No external packages are required. To run an interactive simulation:
```sh
python dbe_simulation.py
```

To run a batch of random scenarios:
```sh
python cli/run_batch.py
```

## Scientific notes

This repository is inspired by the DBE white paper and related literature. The plasma model uses simplified MHD and transport equations and is not intended for operational predictions. The quantum subsystem models demonstrate timing and error-resilience rather than performing real quantum computation. See `docs/THEORY.md` and `docs/research/OBSERVATORY.md`.
