# DBE Fusion Stability Simulator (Research Grade)

This project implements a research‑grade simulation of a fusion plasma discharge controlled by a **Dimensional Braid Engine (DBE)**. It combines a simplified magnetohydrodynamic (MHD) transport model with models of advanced quantum subsystems and realistic actuators to explore how a DBE might stabilise tokamak plasmas by predicting and mitigating instabilities.

## Highlights

- **Physics core:** A 1‑D radial grid with analytic temperature, density and safety‑factor profiles evolves under a finite‑difference transport equation. A shear‑dependent diffusivity suppresses turbulence, and built‑in triggers simulate edge localised modes (ELMs) and other instabilities.
- **Actuators:** Models of resonant magnetic perturbation (RMP) coils and pellet injection change the edge stability and temperature profile. Actuator limits (current, pellet size and rate) are respected.
- **Quantum subsystems:** Topological quantum compute with Majorana braids, fracton memory for robust state storage, a Floquet time crystal for synchronised timing, and a holographic encoder for compressing high‑dimensional plasma states.
- **DBE controller:** The `DBEController` coordinates quantum subsystems and actuators based on plasma stability. It stores compressed profiles in fracton memory, decides coil currents and pellet injections, and synchronises actions on the time crystal tick.
- **Risk analysis:** A `RiskAnalyzer` monitors stability, actuator saturation and memory errors, producing a risk score and explanatory notes for each event.
- **Batch runs:** The script in `cli/run_batch.py` runs many randomised scenarios, collects risk scores and outputs a CSV dataset for analysis.
- **Integration API:** The `simulate_event()` function in `dbe_simulation.py` allows embedding the simulation into other frameworks (e.g. web applications).

## Getting started

Clone this repository and install Python 3. No external packages are required. To run an interactive simulation:
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

This repository is inspired by the DBE white paper and related literature. The plasma model uses simplified MHD and transport equations and is not intended for operational predictions. The quantum subsystem models demonstrate timing and error‑resilience rather than performing real quantum computation. See `docs/THEORY.md` for details and references to original research.

## Contributing

Contributions are welcome. See the open issues for planned work and feel free to open new issues or pull requests.
