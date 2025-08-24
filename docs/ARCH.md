# Architecture

This document explains the structure of the DBE research-grade code base and how data flows through the various components.

## Module tree

- **`dbe/`** – core simulation library
  - **`plasma.py`** – defines the radial grid, analytic profiles, transport solver and ELM triggers.
  - **`actuators.py`** – contains the resonant magnetic perturbation (RMP) coil and pellet injector models.
  - **`quantum.py`** – implements the Majorana qubit register, fracton memory, Floquet time crystal clock and holographic encoder.
  - **`controller.py`** – houses the `DBEController` class which orchestrates quantum subsystems and actuators based on the plasma state and stability metrics.
  - **`risk.py`** – defines the `RiskReport` dataclass and a `RiskAnalyzer` that computes risk scores and explanatory notes.

- **`cli/`** – command‑line utilities
  - **`run_batch.py`** – generates datasets by running multiple simulations under random conditions and writing the results to CSV.
  - **`compare_baseline.py`** – (future work) will compare DBE‑controlled and baseline runs.

- **`docs/`** – project documentation (including this file).

- **`tests/`** – automated unit tests covering each module.

## Data flow

1. **Initialisation:** A `PlasmaState` is created with radial temperature, density and safety‑factor profiles. A `TransportSimulator` is initialised to evolve these profiles via a finite‑difference heat transport equation with ELM triggers.

2. **Quantum subsystem setup:** A `MajoranaQubitRegister` is initialised with a configurable number of logical qubits. A `FractonMemory` instance stores past state snapshots or controller parameters. The `TimeCrystalClock` provides a global tick for synchronisation, and the `HolographicEncoder` compresses high‑dimensional arrays for efficient storage and processing.

3. **Control loop:** At each simulation step or instability event:
   - The `TransportSimulator` advances the plasma state and checks for edge gradients that might exceed the ELM threshold, triggering crashes when necessary.
   - The `DBEController` compresses the current temperature profile via the holographic encoder and stores it in fracton memory. It then computes response time and stability score from the quantum subsystems.
   - Using a heuristic policy (or future machine learning model), the controller sets the RMP coil current and decides whether to fire a pellet. These actuators modify the plasma by raising the ELM threshold or inducing benign crashes.
   - After actuators act, a `RiskAnalyzer` evaluates the new state, producing a risk score and notes. High risk may prompt the controller to allocate more qubits to anomaly detection or engage the time crystal and compression subsystems.

4. **Outputs:** Metrics such as stability, risk, coil current, pellet firing and energy gain are logged. The batch runner writes these to CSV for further analysis or machine learning.

## Extending the architecture

The code is modular by design:

- New physics models (e.g., multi‑fluid or kinetic plasma descriptions, improved transport coefficients) can be added to `plasma.py` without changing the rest of the system.
- Additional actuators (neutral beams, electron cyclotron heating, divertor coils) can be introduced in `actuators.py` and hooked into the controller.
- The decision logic in `controller.py` can be replaced by model predictive control, reinforcement learning or other optimisation techniques.
- The `RiskAnalyzer` in `risk.py` can be expanded to include more sophisticated disruption prediction algorithms.

This flexibility allows the DBE simulator to grow from a toy model into a platform for exploring advanced fusion control strategies.
