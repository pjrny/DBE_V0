"""
dbe.plasma
----------
Phase 2: radial profiles and simple transport simulation.

This module implements a 1D radial grid and a toy transport
simulator used to evolve temperature and density profiles in time.
It extends the Phase 1 scaffolding to include basic physics:
  * creation of radial grid of npoints between 0 and minor radius
  * analytic initialization of temperature, density and q-profiles
  * Spitzer resistivity function as before
  * a simple finite-difference thermal transport equation with
    diffusion coefficient that decreases with shear (toy model)
  * functions to trigger ELM-like crashes when the edge gradient
    exceeds a threshold.

The goal is not to reproduce full MHD but to capture qualitative
features relevant for DBE control experiments.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class PlasmaParams:
    minor_radius: float = 1.0      # m
    major_radius: float = 3.0      # m
    lnLambda: float = 15.0         # Coulomb log
    B0: float = 5.0               # Tesla


@dataclass
class Profiles:
    T0_keV: float = 10.0
    n0_1e20: float = 1.0
    alpha_T: float = 3.0
    alpha_n: float = 2.0
    q0: float = 1.0
    q_edge: float = 3.0
    shear_strength: float = 3.0

    def T_keV(self, x: float) -> float:
        # x = r / a
        return self.T0_keV * (1.0 - x**self.alpha_T)

    def n_1e20(self, x: float) -> float:
        return self.n0_1e20 * (1.0 - x**self.alpha_n)

    def q_profile(self, x: float) -> float:
        # simple linear q-profile: q(r) = q0 + (q_edge - q0)*x
        return self.q0 + (self.q_edge - self.q0) * x


def spitzer_resistivity_ohm_m(Te_eV: float, lnLambda: float = 15.0, Z: int = 1) -> float:
    Te_eV = max(1.0, Te_eV)
    return 5.2e-5 * Z * lnLambda * (Te_eV ** -1.5)


@dataclass
class PlasmaState:
    r: List[float]
    T_keV: List[float]
    n_1e20: List[float]
    q: List[float]
    time: float = 0.0
    stability: float = 1.0  # 0-1 indicator for disruptions



def create_radial_grid(minor_radius: float, npoints: int) -> List[float]:
    """Create an evenly spaced radial grid from 0 to minor_radius."""
    if npoints < 2:
        raise ValueError("npoints must be >= 2")
    dr = minor_radius / (npoints - 1)
    return [i * dr for i in range(npoints)]


def initialize_profiles(params: PlasmaParams, profiles: Profiles, npoints: int = 101) -> PlasmaState:
    """Initialise PlasmaState with analytic profiles."""
    r_grid = create_radial_grid(params.minor_radius, npoints)
    T: List[float] = []
    n_arr: List[float] = []
    q_list: List[float] = []
    for r in r_grid:
        x = r / params.minor_radius
        T.append(profiles.T_keV(x))
        n_arr.append(profiles.n_1e20(x))
        q_list.append(profiles.q_profile(x))
    return PlasmaState(r=r_grid, T_keV=T, n_1e20=n_arr, q=q_list, time=0.0, stability=1.0)


class TransportSimulator:
    """
    Simple 1D thermal transport simulator.

    Uses an explicit finite-difference scheme to evolve the temperature
    profile according to a diffusion equation with variable diffusivity:
        dT/dt = 1/r d/dr( r * chi(r) dT/dr ) + S
    where chi(r) is a radial diffusion coefficient that depends on local
    magnetic shear (q-profile) via a toy model. Sources (heating) and
    sinks (losses) can be provided externally.
    """

    def __init__(self, state: PlasmaState, profiles: Profiles):
        self.state = state
        self.profiles = profiles

    def diffusivity(self, idx: int) -> float:
        """
        Compute a toy diffusivity [keV s^-1] at grid index idx.
        Diffusivity decreases with increasing shear. For a linear q-profile
        the shear ~ dq/dr ~ (q_edge - q0)/a is constant; we modulate by radius.
        """
        x = self.state.r[idx] / self.state.r[-1]  # normalised radius
        base_chi = 0.5  # baseline diffusivity coefficient
        shear = self.profiles.shear_strength * (1 - x)  # more shear near core
        return base_chi / (1.0 + shear)

    def step(self, dt: float, sources: Optional[List[float]] = None) -> None:
        """Advance the temperature profile by time dt."""
        T = self.state.T_keV
        n = len(T)
        new_T = T.copy()
        # zero-flux boundary conditions at r=0 and r=a
        for i in range(1, n - 1):
            chi_left = self.diffusivity(i - 1)
            chi_right = self.diffusivity(i)
            dr_left = self.state.r[i] - self.state.r[i - 1]
            dr_right = self.state.r[i + 1] - self.state.r[i]
            # central difference approximation of diffusion term
            flux_in = chi_left * (T[i - 1] - T[i]) / dr_left
            flux_out = chi_right * (T[i] - T[i + 1]) / dr_right
            diffusion = (flux_in - flux_out) / ((dr_left + dr_right) / 2.0)
            new_T[i] += dt * diffusion
            # add source term if provided
            if sources:
                new_T[i] += dt * sources[i]
        # update state
        self.state.T_keV = new_T
        self.state.time += dt

    def check_edge_gradient(self, threshold: float = 3.0) -> bool:
        """
        Check if the edge temperature gradient exceeds a threshold.
        If so, return True to indicate an ELM-like crash should be triggered.
        """
        T = self.state.T_keV
        r = self.state.r
        # compute gradient between last two points
        grad = abs((T[-1] - T[-2]) / (r[-1] - r[-2]))
        return grad > threshold

    def trigger_elm(self, crash_fraction: float = 0.2) -> None:
        """
        Simulate an ELM-like crash: reduce pedestal temperature by a fraction.
        """
        # reduce last quarter of points
        n = len(self.state.T_keV)
        start = int(0.75 * n)
        for i in range(start, n):
            self.state.T_keV[i] *= (1.0 - crash_fraction)
        # degrade overall stability
        self.state.stability = max(0.0, self.state.stability - 0.1)

    def run_until(self, end_time: float, dt: float = 0.01) -> None:
        """
        Evolve the plasma until end_time. At each step, check for ELM triggers
        and apply them. This is a demonstration of how the transport simulator
        can be used without coupling to DBE control.
        """
        while self.state.time < end_time and self.state.stability > 0.0:
            self.step(dt)
            if self.check_edge_gradient():
                self.trigger_elm()


# Retain default_plasma for API compatibility
def default_plasma(params: Optional[PlasmaParams] = None,
                   profiles: Optional[Profiles] = None,
                   npoints: int = 101) -> PlasmaState:
    p = params or PlasmaParams()
    prof = profiles or Profiles()
    return initialize_profiles(p, prof, npoints)
