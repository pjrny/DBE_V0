# Simulation scenarios

The scenarios below illustrate typical use‑cases for the DBE simulation.

## Scenario 1: Baseline operation with ELM control

In this scenario, a plasma discharge is started with moderate parameters and the DBE is used to suppress edge localised modes (ELMs).

1. **Initial conditions:** The simulation is initialised with a radial grid, temperature, density and safety‑factor profiles typical of an H‑mode discharge. The energy confinement time is near the ITER‑98y2 baseline and the stability metric is high (e.g. 0.8).
2. **Event:** A random ELM precursor appears when the edge pressure gradient crosses the critical threshold. Without intervention, the `TransportSimulator` triggers an ELM crash, dumping energy and reducing τ_E.
3. **DBE control:** The `DBEController` reads the current stability and uses the `MajoranaQubitRegister` to compute a mitigation. It sets the RMP coil to 50 % of its maximum current and fires a small pacing pellet using the `PelletInjector`. The fracton memory logs the event and the time crystal ensures the actions occur exactly on the next tick.
4. **Outcome:** The risk analysis reports a low risk score (~0.2), the ELM amplitude is reduced and the core temperature recovers quickly. The cumulative energy gain Q remains close to the baseline.

## Scenario 2: High‑performance push and risk escalation

Here we push the plasma to high performance by increasing pressure and reducing shear, bringing the system close to MHD stability limits.

1. **Initial conditions:** The radial profiles are adjusted to yield a high β_N and low magnetic shear. The stability metric starts around 0.5.
2. **Event:** A neoclassical tearing mode (NTM) precursor emerges when the safety factor crosses q=2. The DBE attempts mitigation by calculating an RMP current and scheduling multiple pellets.
3. **Complication:** Due to the high heat load, the fracton memory experiences an error cluster. The risk analysis notes a memory error and pellet injector saturation. Despite a high mitigation probability, the control fails to fully stabilise the NTM.
4. **Outcome:** The risk score spikes to 1.0, a disruption occurs and the plasma terminates. The scenario demonstrates the importance of robust memory and actuator margins at high performance.

These scenarios are meant as starting points. Users are encouraged to run the batch script to generate many random runs and to investigate how different allocations and subsystems affect stability, risk and energy gain.
