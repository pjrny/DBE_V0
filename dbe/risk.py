"""
dbe.risk
--------

Phase 6: risk analysis module.

This module defines classes and functions to evaluate the risk of plasma disruption
based on the current plasma state, actuator usage, and DBE subsystem health. The
risk score is a value in [0, 1], with higher values indicating greater risk. The
analysis includes checks on plasma stability, actuator saturation, and memory
errors, returning both a risk score and human-readable notes.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Any


@dataclass
class RiskReport:
    score: float
    notes: List[str] = field(default_factory=list)


class RiskAnalyzer:
    """Evaluate risk based on plasma state and subsystem status."""

    def __init__(
        self,
        stability_thresholds: Optional[Tuple[float, float]] = None,
        coil_saturation_penalty: float = 0.3,
        pellet_saturation_penalty: float = 0.2,
        memory_error_penalty: float = 0.1,
    ) -> None:
        # stability_thresholds: (high, medium) thresholds for risk weighting
        self.stability_thresholds = stability_thresholds or (0.2, 0.5)
        self.coil_penalty = coil_saturation_penalty
        self.pellet_penalty = pellet_saturation_penalty
        self.memory_penalty = memory_error_penalty

    def assess(self, plasma_state: Any, controller: Any) -> RiskReport:
        """
        Assess risk given the plasma state and controller (includes actuators and memory).

        Parameters
        ----------
        plasma_state : Any
            The current plasma state. Must have attribute ``stability`` in [0, 1].
        controller : Any
            The controller object. Must have ``rmp_coil``, ``pellet_injector`` and ``memory``
            attributes with expected fields.

        Returns
        -------
        RiskReport
            A report containing the risk score and explanatory notes.
        """
        notes: List[str] = []
        # Baseline risk inversely related to stability: high risk when stability is low.
        stability: float = getattr(plasma_state, "stability", 1.0)
        risk_base: float = 1.0 - stability

        high_thresh, med_thresh = self.stability_thresholds

        # Descriptive notes on stability
        if stability <= high_thresh:
            notes.append(
                f"Stability {stability:.2f} below high-risk threshold {high_thresh:.2f}."
            )
        elif stability <= med_thresh:
            notes.append(
                f"Stability {stability:.2f} below medium-risk threshold {med_thresh:.2f}."
            )
        else:
            notes.append(f"Stability {stability:.2f} nominal.")

        risk: float = risk_base

        # Actuator saturation: RMP coil
        coil = getattr(controller, "rmp_coil", None)
        if coil is not None:
            I_set = getattr(coil, "I_set", None)
            I_max = getattr(coil, "I_max", None)
            if I_set is not None and I_max is not None:
                if abs(I_set - I_max) < 1e-6 and stability <= med_thresh:
                    risk += self.coil_penalty
                    notes.append("RMP coil at maximum current; limited headroom.")

        # Pellet injector saturation
        pellet = getattr(controller, "pellet_injector", None)
        if pellet is not None:
            can_fire = getattr(pellet, "can_fire", None)
            if callable(can_fire):
                try:
                    import time
                    now = time.time()
                    if stability <= high_thresh and not can_fire(now):
                        risk += self.pellet_penalty
                        notes.append("Pellet injector unavailable when needed.")
                except Exception:
                    pass

        # Memory error penalty
        memory = getattr(controller, "memory", None)
        if memory is not None:
            error_count = getattr(memory, "error_count", 0)
            if error_count and error_count > 0:
                risk += self.memory_penalty
                notes.append(f"Memory error count {error_count} > 0.")

        # Clamp risk score to [0, 1]
        score: float = max(0.0, min(1.0, risk))
        return RiskReport(score=score, notes=notes)


# Backwards compatibility stub

def assess_placeholder(_: Any) -> RiskReport:
    """Deprecated placeholder; provided for compatibility."""
    return RiskReport(score=0.0, notes=["Phase 1 placeholder"])
