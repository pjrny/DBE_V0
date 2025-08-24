# Theory

This document outlines the theoretical foundations implemented in the research-grade DBE fusion simulator. It summarises the physical and computational models that underlie the code base. For a more general introduction, see the top-level README.

## Plasma physics model

The plasma is modelled as a one-dimensional toroidal column with minor radius `a`. We discretise the radial coordinate into `N` grid points with spacing `\u0394r`. At each radius `r`, we track profiles of:

- Electron temperature `T(r,t)` in keV,
- Density `n(r,t)` in 10^20 m⁻³,
- Safety factor `q(r)` describing the twist of magnetic field lines.

The baseline profiles are analytic functions; for example the temperature profile is `T(r) = T0 * (1 − (r/a)^\u03b1_T)`, where `T0` and `\u03b1_T` are parameters. Similar forms define `n(r)` and `q(r)`.

### Energy transport

Energy transport is captured by a radial diffusion equation for the temperature:
```
∂T/∂t = 1/(r) ∂/∂r (r χ ∂T/∂r) + P_ext + P_α − S_loss.
```
Here `\u03c7(r,t)` is the heat diffusivity, which can depend on local shear and turbulence level. The terms `P_ext` and `P_α` represent external heating (e.g. neutral beams or electron cyclotron waves) and self-heating by fusion alpha particles. `S_loss` represents losses due to radiation or conduction. In the toy code we implement a simplified finite-difference solver with constant `\u03c7` modulated by shear flow.

### Resistivity and currents

Electrical resistivity `\u03b7` is given by the Spitzer formula for a fully ionised plasma:
```
η ≈ 5.2 × 10⁻⁵ Z ln Λ T_e^{-3/2}  Ω·m,
```
with `Z` the ion charge (typically 1 for D–T), `ln Λ` the Coulomb logarithm (~15), and electron temperature `T_e` in eV. This resistivity determines current diffusion and influences tearing mode growth.

### Instability thresholds

Several macroscopic stability limits are monitored:

- **Beta limit:** The ratio of plasma pressure to magnetic pressure is `\u03b2 = (2 \u03bc_0 p) / B^2`. If \u03b2 exceeds a critical value, ideal MHD instabilities can develop. The code computes a normalised \u03b2 and flags when it approaches the limit.

- **Safety factor q and magnetic shear:** Sawtooth and tearing instabilities are related to `q` dropping below unity or the presence of rational surfaces. When the core `q` goes below ~1, the simulator triggers sawtooth crashes.

- **Edge-localised modes (ELMs):** A steep pressure gradient at the edge can drive peeling–ballooning modes. We model an ELM threshold based on the pressure gradient; when exceeded, the code triggers a crash that instantaneously flattens the edge temperature profile and deposits energy onto the divertor. Resonant magnetic perturbation coils and pellet pacing can raise this threshold or release pressure in a controlled way.

These thresholds, while simplified, mirror the physical mechanisms encountered in experiments.

## Quantum subsystems

The Dimensional Braid Engine consists of several advanced quantum hardware components that contribute to control:

- **Majorana qubit register:** A topological quantum processor built from Majorana zero modes. Its braid operations are inherently fault-tolerant and provide fast quantum simulation of plasma states. The code abstracts this as a register with a specified number of logical qubits and a braid latency. Response time scales inversely with the number of qubits allocated.

- **Fracton memory:** An exotic error-correcting memory where logical information is stored nonlocally. Local errors cannot propagate freely, making the memory self-correcting over long timescales. The simulator models this by storing arbitrary data keyed by string identifiers. A small probability of correlated errors can be introduced to simulate memory faults.

- **Floquet time crystal:** A periodically driven quantum system that spontaneously breaks time-translation symmetry, yielding a stable clock signal. In the simulator, this provides a global tick used to synchronise all control actions, ensuring deterministic ordering of operations.

- **Holographic encoder:** Inspired by the AdS/CFT correspondence, this module compresses a high-dimensional plasma state into a lower-dimensional boundary representation while preserving information. In the toy model, it performs block-averaging of arrays with a configurable block size and can reconstruct approximate states by repeating the averaged values.

These subsystems are combined in the DBE controller to produce fast, robust decisions for plasma control.

## Actuators and control

Two main actuators are represented:

- **Resonant magnetic perturbation (RMP) coils:** Apply nonaxisymmetric magnetic fields to modify the edge magnetic topology. In the code, coil current `I` (between 0 and a maximum) raises the ELM threshold via a factor `(1 + I/I_max)`. It also introduces a modest confinement penalty because RMP fields can degrade core confinement.

- **Pellet injector:** Fires frozen deuterium–tritium pellets into the plasma edge. A pellet locally increases density and reduces temperature, triggering a small ELM that relieves pressure. The pellet injector is limited by a maximum firing rate and pellet size; if fired too frequently, it becomes unavailable until it cools down.

The `DBEController` reads the plasma state, compresses profiles using the holographic encoder, writes them to fracton memory, and decides control actions (coil current and pellet firing) based on simple heuristics. These heuristics can be replaced by more sophisticated optimisation algorithms in future work.

## Risk analysis

A `RiskAnalyzer` monitors system state and assigns a risk score between 0 and 1. The baseline risk is higher when plasma stability is low. Additional penalties are added for saturated RMP coils (little headroom for further perturbation), unavailable pellet injectors, and fracton memory errors. The risk report includes explanatory notes and is used to decide when to apply more aggressive control.

## Future work

The current models are deliberately simplified. Future extensions could include:

- Multi-fluid or kinetic effects beyond single-fluid MHD,
- More accurate models for turbulence suppression, transport barriers, and rotation,
- Advanced control policies derived from reinforcement learning or model predictive control,
- Coupling to real experimental data for validation.

The goal is to provide an extensible framework where new physics and control modules can be plugged in while retaining a clear separation between the plasma simulation, quantum subsystems, actuators, controller logic, and risk analysis.
