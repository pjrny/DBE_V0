# DBE Fusion Stability Forecaster

This repository contains a toy simulation of a fusion plasma discharge under the control of a **Dimensional Braid Engine (DBE)**.  The simulation is designed to illustrate, in a playful and educational way, how the DBE described in the accompanying white paper might actively stabilise a tokamak plasma by predicting and mitigating magnetohydrodynamic instabilities.

## Overview

The DBE is treated as a black‑box controller with five subsystems:

1. **Topological Quantum Core** – allocates Majorana qubits to simulate the plasma and detect anomalies.  More qubits devoted to anomaly detection yield faster response times.
2. **Fracton Memory** – divides its capacity between storing long‑term stability logs and high‑fidelity real‑time state information.  A larger real‑time allocation improves the DBE’s predictive stability score.
3. **Floquet Time Crystal** – when engaged, synchronises the entire system to reduce noise and enhance coherence, effectively boosting the effectiveness of the other subsystems.
4. **Holographic Encoder** – compresses the sensor data stream to free up qubits and memory for more useful work.
5. **Fusion Plasma Interface** – executes mitigation actions based on the DBE’s predictions.  The likelihood of a successful mitigation depends on the performance of the other subsystems.

At each simulated event, a random instability (for example an edge localised mode or a tearing mode) is triggered.  The operator must reallocate qubits and memory, decide whether to engage the time crystal and holographic encoder, and finally decide whether to execute mitigation.  The outcome of each event influences the plasma stability and the cumulative energy gain compared to a baseline reactor without the DBE.  The key performance indicators are:

* **Energy confinement time (tau_E)** – this is increased relative to a baseline value when the DBE’s stability score is high.  In this model

  `tau_E_DBE = tau_E_standard * (1 + alpha * stability_score)`

  where `alpha` is a tunable constant and the `stability_score` is derived from the fracton memory allocation and learning.

* **Instability growth rate (gamma)** – this is reduced by the DBE’s ability to act quickly.  In the simulation

  `gamma_effective = gamma_physical - beta * response_time`

  where `beta` is a tunable constant and `response_time` is determined by the number of qubits allocated to anomaly detection.

These simple formulas mirror the high‑level ideas in the white paper without attempting to model the full complexity of magnetohydrodynamic instabilities.

## Running the simulation

1. Ensure you have a recent Python 3 interpreter installed (no additional packages are required).
2. Run the simulation from a terminal:

   ```sh
   python dbe_simulation.py
   ```

3. Follow the on‑screen prompts to allocate resources, engage subsystems, and decide when to execute mitigation.  The simulation runs through a fixed number of events (five by default).  At the end you will see your cumulative energy gain compared with a baseline reactor.

You can adjust the number of events or the constants `alpha` and `beta` by editing the parameters passed to the `Simulation` class in `dbe_simulation.py`.

## Programmatic integration

The core logic of the simulation can be used as a lightweight library.  The
function `simulate_event` in `dbe_simulation.py` takes explicit parameters
for the DBE state, plasma state, physical growth rate and resource
allocations, and returns the updated objects along with the outcome of
mitigation.  This makes it straightforward to embed the model into
other systems (for example, a web application in Odoo) without relying
on the interactive command‑line interface.

Here's an example of how to call it:

```python
from dbe_simulation import DBEState, PlasmaState, simulate_event

alpha = 0.3
beta = 0.2
dbe = DBEState()
plasma = PlasmaState()
gamma_physical = 1.0  # some instability strength

# allocate 60 qubits, 40 memory units, engage time crystal and compress, and attempt mitigation
success, p_mit, new_stab, dbe, plasma = simulate_event(
    dbe_state=dbe,
    plasma_state=plasma,
    gamma_physical=gamma_physical,
    alpha=alpha,
    beta=beta,
    qubits_alloc=60,
    memory_alloc=40,
    engage_time_crystal=True,
    engage_compression=True,
    execute_mitigation=True,
)
print(f"Mitigation success: {success}, probability was {p_mit:.2f}, new stability: {new_stab:.1f}%")
```

## Notes

This project is intended as an educational demonstration.  While inspired by concepts in topological quantum computing and fusion physics, the model is deliberately simplified and should not be interpreted as a realistic predictor of plasma behaviour.  Nevertheless, it highlights the interplay between predictive control, resource allocation and system performance—ideas central to the Dimensional Braid Engine vision.