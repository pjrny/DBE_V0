"""

dbe.plasma
----------
Phase 1 scaffold: radial profiles, parameters, and placeholders.
No dynamics yet; just types and simple factories so imports pass.
"""

from dataclasses import dataclass
from typing import Callable, Optional
import math

@dataclass
class PlasmaParams:
    minor_radius: float = 1.0      # [m]
    major_radius: float = 3.0      # [m]
    lnLambda: float = 15.0         # Coulomb log (dimensionless)
    B0: float = 5.0                # Toroidal field [T]

@dataclass
class Profiles:
    # simple analytic radial profiles r in [0, a]
    T0_keV: float = 10.0
    n0_1e20: float = 1.0
    alpha_T: float = 3.0
    alpha_n: float = 2.0

    def T_keV(self, r: float, a: float) -> float:
        x = max(0.0, min(1.0, r / a))
        return self.T0_keV * (1.0 - x ** self.alpha_T)

    def n_1e20(self, r: float, a: float) -> float:
        x = max(0.0, min(1.0, r / a))
        return self.n0_1e20 * (1.0 - x ** self.alpha_n)

def spitzer_resistivity_ohm_m(Te_eV: float, lnLambda: float = 15.0, Z: int = 1) -> float:
    """Classic Spitzer η ≈ 5.2e-5 * Z * lnΛ * Te^{-3/2}  [Ω·m]; Te in eV.
    Placeholder constants; refined in Phase 2.
    """
    Te_eV = max(1.0, Te_eV)
    return 5.2e-5 * Z * lnLambda * (Te_eV ** -1.5)

@dataclass
class PlasmaState:
    """Minimal placeholder used by CLI; extended in Phase 2."""
    stability: float = 1.0   # 0..1
    tau_E_s: float = 1.0
    beta_N: float = 0.5

def default_plasma(params: Optional[PlasmaParams] = None) -> PlasmaState:
    _ = params or PlasmaParams()
    return PlasmaState()
