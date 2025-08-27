"""
DBE: Research-grade simulator package (Phase 1 scaffolding).

This package provides namespaces for plasma physics, actuators,
quantum subsystems, controller logic, and risk analysis.

Phase 1 goal: imports pass; CLI remains backward-compatible.
"""
from . import plasma, actuators, quantum, controller, risk  # noqa: F401

__all__ = ["plasma", "actuators", "quantum", "controller", "risk"]
