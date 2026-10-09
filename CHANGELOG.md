# Changelog

All notable changes to this project will be documented in this file.

## [SDBES V4 R2] - 2026-10-09

### Added
- Added the V4 R2 causal-dynamics, model-composition, simulation-credibility,
  and research-intervention specification and schema template.
- Added dependency-free executable reference semantics for local response
  families, ordered finite-horizon propagation, unit/timebase closure,
  coupling validation, V3 predicate authorization, typed resource balances,
  multi-fidelity promotion, transfer, V2 evidence return, K/X separation,
  research decisions, kill tests, and milestone bindings.
- Added a frozen 15-case V1→V4 regression suite containing only the ten
  previously assessed papers and five previously used DBE/DBE-S cases.
- Added a dedicated SDBES CI release gate for Python 3.10–3.12.

### Verification
- V3 reference checks: pass.
- V4 R2 reference checks: 13/13 pass.
- Existing-case regression: 15/15 pass; 13 expected refinements, 2 unchanged,
  0 unexpected regressions.
- The nine legacy simulator failures reproduce unchanged at the V3 baseline
  commit and are outside the V4 R2 change set.

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
