"""
Dimensional Braid Engine (DBE) Fusion Stability Forecaster
==========================================================

This module implements a simplified, text‑based simulation of a fusion plasma
discharge under the control of a hypothetical **Dimensional Braid Engine** (DBE).

The DBE is described in an accompanying white paper and summarised as a
collection of five interlocking subsystems that collectively provide
predictive control and active stabilisation of a fusion plasma.  The
simulation exposes the operator (the user) to these subsystems and their
configuration parameters while a simple zero‑dimensional plasma model
evolves in time.

The simulation focuses on two key performance indicators (KPIs):

* **Energy confinement time** (τ_E): the characteristic time over which
  energy remains in the plasma before being lost.  A longer τ_E
  directly improves the fusion gain Q (the ratio of fusion power to
  external heating power).  In this model a baseline τ_E, drawn from
  empirical scaling laws (e.g. ITER‑98y2), is modified by the DBE
  according to

    τ_E,DBE = τ_E,standard × (1 + α × DBE_Stability_Score),

  where α is a tunable constant and the **DBE stability score** is
  computed from the allocation of fracton memory resources.

* **Instability growth rate** (γ): fast growing magnetohydrodynamic
  instabilities, such as tearing modes and edge localised modes
  (ELMs), can disrupt the discharge if their growth parameter exceeds
  unity over the characteristic time of the instability.  Without
  intervention γ is determined by simple linear MHD theory, but the
  DBE may suppress it by acting quickly.  A simple model captures
  this by

    γ_effective = γ_physical − β × DBE_Response_Time,

  where β is another constant and **DBE response time** depends on the
  number of topological qubits allocated to anomaly detection.

These expressions are directly inspired by the formulas appearing in the
white paper and in the task description.  This code does not attempt to
replicate realistic plasma behaviour; rather, it illustrates how the
quantitative outputs of the DBE subsystems feed into macroscopic plasma
metrics.  The event system is deliberately simplified: random events
trigger instabilities that must be mitigated by the operator.  The
operator reallocates DBE resources and decides when to fire the fusion
interface.  Outcomes affect the plasma stability and the cumulative
energy gain.

Usage:

Run this script directly from a command line.  The simulation will
prompt you to reallocate DBE resources and respond to instabilities.  The
game ends when the plasma completely disrupts (stability reaches zero)
or after a preconfigured number of discharges.  At the end the
simulation prints your final energy gain Q compared with a baseline run
without the DBE.

This module is intentionally self‑contained and does not depend on any
external libraries beyond the Python standard library.
"""

from __future__ import annotations

import math
import random
import sys
from dataclasses import dataclass, field
from typing import Optional, Tuple


def logistic(x: float, k: float = 5.0, x0: float = 0.5) -> float:
    """Logistic function used to map a raw score to [0, 1].

    Parameters
    ----------
    x : float
        The input value.
    k : float, optional
        The steepness of the logistic curve.  A larger value makes the
        transition from 0 to 1 sharper.
    x0 : float, optional
        The midpoint of the logistic curve.

    Returns
    -------
    float
        A value between 0 and 1.
    """
    return 1.0 / (1.0 + math.exp(-k * (x - x0)))


@dataclass
class DBEState:
    """Represents the state of the DBE subsystems and their resource allocations.

    The DBE comprises five subsystems.  For the purposes of this simple
    model we track only the degrees of freedom relevant to the formulas
    described in the accompanying white paper:

    * The **topological quantum core** manages quantum simulations and
      anomaly detection.  We assume a fixed budget of qubits, of which
      some fraction is allocated to anomaly detection.  A larger
      allocation reduces the response time when instabilities occur.

    * The **fracton memory** stores past plasma states and stability logs.
      The fraction of memory devoted to real‑time state data determines
      the DBE's predictive capacity and therefore the stability score.

    * The **Floquet time crystal** may be engaged or disengaged.  When
      engaged it increases the coherence of other subsystems and
      effectively amplifies their contributions.

    * The **holographic encoder** compresses the incoming sensor stream.
      When engaged it frees up qubits and memory for other tasks.

    * The **fusion plasma interface** executes mitigation actions.  It
      doesn't have an internal state here but its success probability
      depends on the other metrics.
    """

    # Resource pools
    qubits_total: int = 100
    memory_total: int = 100

    # Allocations
    qubits_for_detection: int = 50
    memory_for_state: int = 50

    # Binary subsystems
    time_crystal_engaged: bool = False
    compression_engaged: bool = False

    # Learning: track cumulative stability score improvements per event type
    stability_gain: float = 0.0

    def reallocate_resources(self, qubits: int, memory: int) -> None:
        """Reallocate qubits and memory to anomaly detection and state storage.

        Parameters
        ----------
        qubits : int
            Number of qubits to allocate to anomaly detection.  Must lie
            between 0 and ``qubits_total``.
        memory : int
            Number of memory units to allocate to real‑time state storage.
            Must lie between 0 and ``memory_total``.
        """
        if not (0 <= qubits <= self.qubits_total):
            raise ValueError(
                f"qubits allocation {qubits} outside [0, {self.qubits_total}]"
            )
        if not (0 <= memory <= self.memory_total):
            raise ValueError(
                f"memory allocation {memory} outside [0, {self.memory_total}]"
            )
        self.qubits_for_detection = qubits
        self.memory_for_state = memory

    def toggle_time_crystal(self, engaged: bool) -> None:
        """Engage or disengage the Floquet time crystal."""
        self.time_crystal_engaged = engaged

    def toggle_compression(self, engaged: bool) -> None:
        """Engage or disengage the holographic encoder."""
        self.compression_engaged = engaged

    def compute_metrics(self) -> Tuple[float, float, float, float, float]:
        """Compute DBE performance metrics based on current allocations.

        Returns
        -------
        response_time : float
            The time (arbitrary units) taken by the DBE to respond to
            detected anomalies.  Inversely proportional to the number
            of qubits allocated to detection.
        stability_score : float
            A normalised measure of the DBE's predictive capacity.  It
            increases with the logarithm of the real‑time memory
            allocation, scaled to [0, 1].  Additional learning from
            successful mitigation is also included.
        coherence_factor : float
            A multiplier (≥1) reflecting whether the Floquet time
            crystal is engaged.  When engaged the outputs of other
            subsystems are more reliable.
        efficiency_factor : float
            A multiplier (≥1) reflecting whether the holographic
            encoder is compressing sensor data.  When engaged it
            frees resources for other tasks.
        mitigation_success_prob : float
            The predicted success probability of the next mitigation
            action.  This uses a logistic function to map a combined
            metric to [0, 1].
        """
        # Response time decreases with more qubits.  We add a small
        # offset to avoid division by zero.
        base_response = 1.0  # nominal response time with one qubit
        response_time = base_response / max(1.0, self.qubits_for_detection / 10.0)

        # Stability score increases logarithmically with memory.
        max_score = math.log(self.memory_total + 1.0)
        stability_score = math.log(self.memory_for_state + 1.0) / max_score
        stability_score = min(1.0, stability_score + self.stability_gain)

        # Coherence and efficiency factors
        coherence_factor = 1.3 if self.time_crystal_engaged else 1.0
        efficiency_factor = 1.3 if self.compression_engaged else 1.0

        # Combined score for mitigation success probability.  We
        # construct a raw score as a weighted average of normalised
        # stability score and inverse response time.  Coherence and
        # efficiency act as multipliers.  The logistic function maps
        # the result to [0, 1].
        response_score = 1.0 / (1.0 + response_time)  # shorter times → higher score
        raw = (stability_score + response_score) / 2.0
        raw *= coherence_factor * efficiency_factor
        mitigation_success_prob = logistic(raw, k=5.0, x0=0.6)

        return (
            response_time,
            stability_score,
            coherence_factor,
            efficiency_factor,
            mitigation_success_prob,
        )

    def learn_from_event(self, increment: float = 0.02) -> None:
        """Increment the internal stability gain to reflect learning.

        This simulates the fracton memory subsystem improving its
        predictive capacity after a successful mitigation.  The
        increment parameter is deliberately small to produce gradual
        improvement over multiple events.
        """
        self.stability_gain = min(0.5, self.stability_gain + increment)


@dataclass
class PlasmaState:
    """Represents the simplified plasma state tracked in the simulation."""

    stability: float = 100.0  # percentage of nominal stability (0–100)
    tau_e_standard: float = 1.0  # baseline energy confinement time
    tau_e_current: float = 1.0  # current energy confinement time (updated)
    n: float = 1.0  # normalised density constant
    T: float = 1.0  # normalised temperature constant
    heating_power: float = 1.0  # normalised external heating power

    # Cumulative energy gain compared to baseline
    cumulative_Q: float = 0.0
    cumulative_Q_baseline: float = 0.0

    def update_tau_e(self, stability_score: float, alpha: float) -> None:
        """Update the energy confinement time based on the DBE stability score."""
        self.tau_e_current = self.tau_e_standard * (1.0 + alpha * stability_score)

    def compute_Q(self) -> Tuple[float, float]:
        """Compute the current and baseline fusion gain Q.

        Q ∝ (n T τ_E) / HeatingPower.  Since n, T and HeatingPower are
        normalised to 1 in this toy model, Q reduces to τ_E.  The
        baseline Q uses the standard τ_E.
        """
        Q_current = self.n * self.T * self.tau_e_current / self.heating_power
        Q_baseline = self.n * self.T * self.tau_e_standard / self.heating_power
        return Q_current, Q_baseline


class Simulation:
    """Main class orchestrating the fusion discharge simulation."""

    def __init__(
        self,
        num_events: int = 5,
        alpha: float = 0.3,
        beta: float = 0.2,
    ) -> None:
        """
        Parameters
        ----------
        num_events : int, optional
            Number of instability events to simulate during the discharge.
        alpha : float, optional
            Coefficient linking the DBE stability score to energy confinement time.
        beta : float, optional
            Coefficient linking the DBE response time to the effective
            instability growth rate.
        """
        self.num_events = num_events
        self.alpha = alpha
        self.beta = beta
        self.dbe = DBEState()
        self.plasma = PlasmaState()

    def run(self) -> None:
        """Run the interactive simulation loop."""
        print(
            "Welcome to the DBE Fusion Stability Forecaster!\n"
            "You are the operator of a fusion reactor equipped with a Dimensional Braid Engine.\n"
            "Your goal is to mitigate instabilities and maximise the energy gain Q.\n"
        )

        for event_number in range(1, self.num_events + 1):
            print(f"\n--- Event {event_number}/{self.num_events} ---")
            # Generate a random physical instability growth rate between 0.5 and 1.5
            gamma_physical = random.uniform(0.5, 1.5)
            # Display event description
            event_type = random.choice([
                "Edge Localised Mode (ELM)",
                "Tearing Mode", 
                "Fishbone", 
                "Alfvénic Instability",
                "Locked Mode",
            ])
            print(
                f"Warning: {event_type} detected!\n"
                f"Physical growth rate γ_physical ≈ {gamma_physical:.2f}."
            )

            # Compute current DBE metrics
            (
                response_time,
                stability_score,
                coherence_factor,
                efficiency_factor,
                mitigation_prob,
            ) = self.dbe.compute_metrics()
            # Update tau_E based on the current stability score
            self.plasma.update_tau_e(stability_score, self.alpha)
            # Compute predicted Q
            Q_current, Q_baseline = self.plasma.compute_Q()

            print(
                f"Current DBE metrics:\n"
                f"  Response time: {response_time:.2f}\n"
                f"  Stability score: {stability_score:.2f}\n"
                f"  Time crystal engaged: {self.dbe.time_crystal_engaged}\n"
                f"  Holographic compression engaged: {self.dbe.compression_engaged}\n"
                f"  Predicted mitigation success: {mitigation_prob * 100:.1f}%\n"
                f"  Current energy gain Q: {Q_current:.2f} (baseline {Q_baseline:.2f})"
            )

            # Ask the operator to reallocate resources
            self._prompt_resource_allocation()

            # Recompute metrics after reallocation
            (
                response_time,
                stability_score,
                coherence_factor,
                efficiency_factor,
                mitigation_prob,
            ) = self.dbe.compute_metrics()
            self.plasma.update_tau_e(stability_score, self.alpha)
            Q_current, Q_baseline = self.plasma.compute_Q()
            print(
                f"\nAfter reallocation:\n"
                f"  Response time: {response_time:.2f}\n"
                f"  Stability score: {stability_score:.2f}\n"
                f"  Predicted mitigation success: {mitigation_prob * 100:.1f}%\n"
                f"  Updated energy gain Q: {Q_current:.2f} (baseline {Q_baseline:.2f})"
            )

            # Decision to engage time crystal
            if not self.dbe.time_crystal_engaged:
                engage = self._yes_no_prompt(
                    "Engage the Floquet time crystal for additional coherence? (y/n): "
                )
                if engage:
                    self.dbe.toggle_time_crystal(True)
                    print("Time crystal engaged. Coherence factor increased.")
                    # Recompute metrics with time crystal engaged
                    (
                        response_time,
                        stability_score,
                        coherence_factor,
                        efficiency_factor,
                        mitigation_prob,
                    ) = self.dbe.compute_metrics()
                    self.plasma.update_tau_e(stability_score, self.alpha)
                    Q_current, Q_baseline = self.plasma.compute_Q()
                    print(
                        f"New predicted mitigation success: {mitigation_prob * 100:.1f}%\n"
                        f"New energy gain Q: {Q_current:.2f}"
                    )

            # Decision to engage holographic encoder
            if not self.dbe.compression_engaged:
                engage = self._yes_no_prompt(
                    "Engage holographic compression to free resources? (y/n): "
                )
                if engage:
                    self.dbe.toggle_compression(True)
                    print("Holographic encoder engaged. Efficiency factor increased.")
                    (
                        response_time,
                        stability_score,
                        coherence_factor,
                        efficiency_factor,
                        mitigation_prob,
                    ) = self.dbe.compute_metrics()
                    self.plasma.update_tau_e(stability_score, self.alpha)
                    Q_current, Q_baseline = self.plasma.compute_Q()
                    print(
                        f"New predicted mitigation success: {mitigation_prob * 100:.1f}%\n"
                        f"New energy gain Q: {Q_current:.2f}"
                    )

            # Final decision: execute mitigation or ride it out
            execute = self._yes_no_prompt(
                "Execute mitigation now? (y/n): "
            )
            if execute:
                success = random.random() < mitigation_prob
                if success:
                    print("Mitigation succeeded! The instability was suppressed.")
                    # Improve DBE learning
                    self.dbe.learn_from_event()
                    # Stability dip is small
                    self.plasma.stability = max(0.0, self.plasma.stability - 5.0)
                else:
                    print(
                        "Mitigation failed. The instability grows and damages the plasma." 
                        "Consider allocating more resources next time."
                    )
                    # Compute effective growth rate and stability loss
                    gamma_effective = gamma_physical - self.beta * response_time
                    # Clamp gamma_effective to non‑negative
                    gamma_effective = max(0.0, gamma_effective)
                    loss = gamma_effective * 20.0  # scale to percentage points
                    self.plasma.stability = max(0.0, self.plasma.stability - loss)
                # Update cumulative Q after this event
                Q_current, Q_baseline = self.plasma.compute_Q()
                self.plasma.cumulative_Q += Q_current
                self.plasma.cumulative_Q_baseline += Q_baseline
            else:
                print("You chose not to mitigate. The instability evolves unchecked.")
                gamma_effective = gamma_physical  # no mitigation
                loss = gamma_effective * 20.0
                self.plasma.stability = max(0.0, self.plasma.stability - loss)
                Q_current, Q_baseline = self.plasma.compute_Q()
                self.plasma.cumulative_Q += Q_current
                self.plasma.cumulative_Q_baseline += Q_baseline

            print(f"Plasma stability now at {self.plasma.stability:.1f}%\n")
            if self.plasma.stability <= 0.0:
                print(
                    "\nThe plasma has disrupted! Game over."
                )
                break

        # End of simulation summary
        if self.plasma.cumulative_Q_baseline == 0:
            # Avoid division by zero
            improvement = 0.0
        else:
            improvement = (
                self.plasma.cumulative_Q / self.plasma.cumulative_Q_baseline - 1.0
            ) * 100.0
        print(
            "\n=== Simulation Summary ===\n"
            f"Cumulative energy gain with DBE: {self.plasma.cumulative_Q:.2f}\n"
            f"Cumulative baseline energy gain: {self.plasma.cumulative_Q_baseline:.2f}\n"
            f"Relative improvement: {improvement:.1f}%\n"
        )

    # Helper methods for user interaction
    def _prompt_resource_allocation(self) -> None:
        """Prompt the operator to allocate qubits and memory."""
        while True:
            try:
                qubits_str = input(
                    f"Allocate qubits to anomaly detection (0–{self.dbe.qubits_total}): "
                )
                memory_str = input(
                    f"Allocate memory to real‑time state data (0–{self.dbe.memory_total}): "
                )
                qubits = int(qubits_str)
                memory = int(memory_str)
                self.dbe.reallocate_resources(qubits, memory)
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")

    def _yes_no_prompt(self, prompt: str) -> bool:
        """Prompt the user with a yes/no question and return True/False."""
        while True:
            answer = input(prompt).strip().lower()
            if answer in {"y", "yes"}:
                return True
            if answer in {"n", "no"}:
                return False
            print("Please answer with 'y' or 'n'.")


def main(argv: Optional[list[str]] = None) -> None:
    """Entry point for running the simulation from the command line."""
    sim = Simulation(num_events=5, alpha=0.3, beta=0.2)
    sim.run()


if __name__ == "__main__":
    main(sys.argv[1:])


# -----------------------------------------------------------------------------
#  Lightweight integration API
#
#  In addition to the interactive CLI, this module exposes a function
#  `simulate_event` that can be called programmatically to advance the
#  plasma and DBE states by one instability event.  This allows
#  embedding the core logic into other frameworks (for example a web
#  service written in Odoo or another language that can interface with
#  Python).  The function takes explicit parameters for resource
#  allocation and subsystem engagement and returns the outcome and
#  updated state objects.  The caller is responsible for persisting
#  these objects between calls.

def simulate_event(
    dbe_state: DBEState,
    plasma_state: PlasmaState,
    gamma_physical: float,
    alpha: float,
    beta: float,
    qubits_alloc: int,
    memory_alloc: int,
    engage_time_crystal: bool = False,
    engage_compression: bool = False,
    execute_mitigation: bool = True,
) -> Tuple[bool, float, float, DBEState, PlasmaState]:
    """Simulate a single instability event non‑interactively.

    Parameters
    ----------
    dbe_state : DBEState
        Current DBE state.  This object will be mutated and returned.
    plasma_state : PlasmaState
        Current plasma state.  This object will be mutated and returned.
    gamma_physical : float
        Physical growth rate of the instability (0.0–∞).
    alpha : float
        Coupling constant linking the DBE stability score to τ_E.
    beta : float
        Coupling constant linking the DBE response time to the
        effective growth rate.
    qubits_alloc : int
        Number of qubits to allocate to anomaly detection for this event.
    memory_alloc : int
        Number of memory units to allocate to real‑time state data.
    engage_time_crystal : bool, optional
        Whether to engage the Floquet time crystal during this event.
    engage_compression : bool, optional
        Whether to engage the holographic encoder during this event.
    execute_mitigation : bool, optional
        Whether to attempt mitigation.  If false, the event
        progresses unchecked.

    Returns
    -------
    success : bool
        True if mitigation succeeded (only meaningful when
        ``execute_mitigation`` is True).  False if mitigation was
        executed and failed or if no mitigation was attempted.
    mitigation_probability : float
        The computed probability of success based on the DBE state.
    new_stability : float
        The updated plasma stability percentage.
    dbe_state : DBEState
        The updated DBEState object (identical object, mutated in place).
    plasma_state : PlasmaState
        The updated PlasmaState object (identical object, mutated in place).

    Notes
    -----
    This function performs no input validation on the ``gamma_physical``
    parameter.  It is the caller's responsibility to provide
    physically sensible values.  Resource allocations outside
    permitted ranges will raise ``ValueError`` via ``DBEState``.
    """
    # Apply resource allocations and subsystem engagement
    dbe_state.reallocate_resources(qubits_alloc, memory_alloc)
    dbe_state.toggle_time_crystal(engage_time_crystal)
    dbe_state.toggle_compression(engage_compression)

    # Compute DBE metrics and update τ_E
    response_time, stability_score, _, _, mitigation_prob = dbe_state.compute_metrics()
    plasma_state.update_tau_e(stability_score, alpha)

    # Determine whether mitigation is attempted and its outcome
    success = False
    if execute_mitigation:
        success = random.random() < mitigation_prob
        if success:
            # Successful mitigation: small stability dip and learning
            dbe_state.learn_from_event()
            plasma_state.stability = max(0.0, plasma_state.stability - 5.0)
        else:
            # Failed mitigation: compute effective growth rate and stability loss
            gamma_effective = max(0.0, gamma_physical - beta * response_time)
            loss = gamma_effective * 20.0
            plasma_state.stability = max(0.0, plasma_state.stability - loss)
    else:
        # No mitigation attempted: instability progresses unchecked
        loss = gamma_physical * 20.0
        plasma_state.stability = max(0.0, plasma_state.stability - loss)

    # Update cumulative energy gain (always accumulate)
    Q_current, Q_baseline = plasma_state.compute_Q()
    plasma_state.cumulative_Q += Q_current
    plasma_state.cumulative_Q_baseline += Q_baseline

    return success, mitigation_prob, plasma_state.stability, dbe_state, plasma_state