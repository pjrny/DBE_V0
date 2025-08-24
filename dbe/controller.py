"""
dbe.controller
--------------
Phase 5: DBEController orchestrates DBE quantum subsystems and actuators.

This module defines a controller that senses the plasma state, stores
compressed state information in a fracton memory, and decides on actuator
commands based on simple heuristics. It uses a time crystal to synchronise
actions and a holographic encoder to compress the high-dimensional plasma
state before storing it. It also manages an RMP coil and a pellet injector.

These implementations are simplified and are intended to demonstrate the
integration of Phase‑2/3/4 modules. They do not represent an optimal
control algorithm.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict
import time

from .plasma import PlasmaState
from .quantum import (
    MajoranaQubitRegister,
    FractonMemory,
    TimeCrystalClock,
    HolographicEncoder,
)
from .actuators import RMPCoil, PelletInjector


@dataclass
class DBEController:
    """Coordinate DBE subsystems and actuators based on plasma state."""

    qubit_register: MajoranaQubitRegister = field(default_factory=MajoranaQubitRegister)
    memory: FractonMemory = field(
        default_factory=lambda: FractonMemory(capacity_mb=64.0, error_rate_per_hour=0.001)
    )
    clock: TimeCrystalClock = field(default_factory=lambda: TimeCrystalClock(tick_ns=1_000_000))
    encoder: HolographicEncoder = field(default_factory=lambda: HolographicEncoder(block_size=10))
    rmp_coil: RMPCoil = field(default_factory=RMPCoil)
    pellet_injector: PelletInjector = field(default_factory=PelletInjector)
    last_decision: Dict[str, Any] = field(default_factory=dict)

    def decide(self, plasma_state: PlasmaState) -> Dict[str, Any]:
        """
        Decide on actuator commands based on the current plasma state.

        Parameters
        ----------
        plasma_state : PlasmaState
            The current state of the plasma.

        Returns
        -------
        dict
            A dictionary with keys:
                - 'rmp_current': float, the commanded RMP coil current [A].
                - 'pellet_fire': bool, whether to fire a pellet.
        """
        # Compress and store the temperature profile if available
        if hasattr(plasma_state, "temperature") and plasma_state.temperature is not None:
            try:
                encoded = self.encoder.encode(plasma_state.temperature.tolist())
                self.memory.write("temp_profile", encoded)
            except Exception:
                self.memory.write("temp_profile", [plasma_state.stability])
        else:
            self.memory.write("temp_profile", [plasma_state.stability])

        stability = getattr(plasma_state, "stability", 1.0)
        decision: Dict[str, Any] = {"rmp_current": 0.0, "pellet_fire": False}

        # Simple heuristic: more aggressive control when stability is low
        if stability < 0.3:
            # Full RMP current
            decision["rmp_current"] = self.rmp_coil.I_max
            # Fire pellet if permitted
            now = time.time()
            if self.pellet_injector.can_fire(current_time=now):
                decision["pellet_fire"] = True
                # Use half-size pellet and fire at edge radius (1.0)
                self.pellet_injector.fire(
                    current_time=now,
                    radial_position=1.0,
                    size=self.pellet_injector.size_max / 2,
                )
        elif stability < 0.6:
            # Half RMP current
            decision["rmp_current"] = 0.5 * self.rmp_coil.I_max
        else:
            # No RMP current
            decision["rmp_current"] = 0.0

        # Apply the RMP current command
        self.rmp_coil.set_current(decision["rmp_current"])

        # Save decision
        self.last_decision = decision
        return decision

    def get_last_decision(self) -> Dict[str, Any]:
        """Return the last actuator decision made by the controller."""
        return self.last_decision
