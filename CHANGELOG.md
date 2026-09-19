# Changelog

All notable changes to this project will be documented in this file.

## [0.3.0] - 2026-09-19
### Added
- Research Observatory: tagged catalog of core papers across Anyons, TQC, Majorana, braid/knot theory, topology, fracton memory, time crystals, plasma control, holography, and fusion–quantum integration.
- Each paper carries importance / confidence / popularity scores and a plain-language triple (core idea, why it matters, one limitation).
- Foundational pillars are date-unrestricted; first ingest runs look back 1 year or more.
- Suggested new pillars when a result is load-bearing (cyclic fusion universality, Floquet–Majorana codes, fracton holography, 2D non-Abelian qLDPC, topological dynamics hardware).
- `research/ingest.py` daily arXiv ingest against the program feeds.
- `cli/research_observatory.py` interactive catalog tab.
- `docs/research/OBSERVATORY.md` scoring rules and the Q = 1000 honesty bar.
- Unit tests for catalog completeness (`tests/test_research.py`).

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
