"""
dbe.actuators
-------------
Phase 1 stubs: typed interfaces for actuators.
"""

from dataclasses import dataclass

@dataclass
class RMPCoil:
    I_max: float = 1.0
    I_set: float = 0.0

@dataclass
class PelletInjector:
    rate_max_hz: float = 50.0
    size_max: float = 1.0
    last_fire_s: float = 0.0
