"""
dbe.actuators
------------

Phase 3: simple actuator models.

This module defines basic models for actuators used to control a tokamak plasma,
including resonant magnetic perturbation (RMP) coils and pellet injectors.

The actuators modify the plasma state by adjusting stability thresholds or
injecting matter/energy into the plasma in simplified ways.

These models are deliberately lightweight and intended to illustrate how the
DBE might interact with physical actuators. They are not realistic but capture
qualitative behaviour (e.g. RMPs raising ELM thresholds and pellets pacing ELMs).
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING

# Forward declaration for type hints
if TYPE_CHECKING:
    from .plasma import TransportSimulator


@dataclass
class RMPCoil:
    """Model a resonant magnetic perturbation (RMP) coil.

    Parameters
    ----------
    I_max : float
        Maximum coil current (arbitrary units).
    I_set : float
        The present coil current in the range [0, I_max].

    The coil modifies the ELM pressure gradient threshold by raising it
    proportionally to the current setting, and incurs a small confinement
    penalty due to magnetic perturbations.
    """
    I_max: float = 1.0
    I_set: float = 0.0

    def set_current(self, current: float) -> None:
        """Set the coil current, clamped between 0 and I_max."""
        self.I_set = max(0.0, min(self.I_max, current))

    def elm_threshold_multiplier(self) -> float:
        """Compute the factor by which to multiply the ELM threshold.

        At zero current the factor is 1.0.  At full current the factor is 1.5.
        """
        if self.I_max <= 0:
            return 1.0
        return 1.0 + 0.5 * (self.I_set / self.I_max)

    def confinement_penalty(self) -> float:
        """Return a factor (<1) representing the confinement penalty.

        The penalty scales from 1.0 at zero current to 0.95 at full current.
        """
        if self.I_max <= 0:
            return 1.0
        return 1.0 - 0.05 * (self.I_set / self.I_max)


@dataclass
class PelletInjector:
    """Model a pellet injector for pacing ELMs and adding particles.

    Parameters
    ----------
    rate_max_hz : float
        Maximum pellet firing rate in Hz.
    size_max : float
        Maximum pellet size (arbitrary units).  Pellet sizes above this value
        are clamped.
    last_fire_s : float
        Timestamp (in seconds) of the last pellet injection.
    """
    rate_max_hz: float = 50.0
    size_max: float = 1.0
    last_fire_s: float = 0.0

    def can_fire(self, current_time: float) -> bool:
        """Return True if a pellet can be fired at the given time."""
        if self.rate_max_hz <= 0.0:
            return True
        minimum_interval = 1.0 / self.rate_max_hz
        return (current_time - self.last_fire_s) >= minimum_interval

    def fire(self, sim: "TransportSimulator", current_time: float, size: float) -> bool:
        """Fire a pellet into the plasma via the transport simulator.

        Parameters
        ----------
        sim : TransportSimulator
            The transport simulator whose temperature profile will be modified.
        current_time : float
            Simulation time in seconds.
        size : float
            Pellet size (0 to size_max).  Larger size produces larger temperature
            drop near the plasma edge.

        Returns
        -------
        bool
            True if the pellet was injected, False if suppressed by rate limit.
        """
        if not self.can_fire(current_time):
            return False
        # Clamp size
        size = max(0.0, min(self.size_max, size))
        # Fractional temperature drop (up to 5%)
        drop_fraction = 0.05 * (size / self.size_max) if self.size_max > 0 else 0.0
        if drop_fraction > 0.0:
            n = len(sim.state.T_keV)
            start_idx = int(n * 0.8)
            for i in range(start_idx, n):
                sim.state.T_keV[i] *= (1.0 - drop_fraction)
        self.last_fire_s = current_time
        return True
