"""
dbe.quantum
-----------
Phase 4: quantum and time-resilient modules.

This module defines classes representing the DBE's quantum subsystems,
including a Majorana-based qubit register, fracton-based memory, a time
crystal clock providing stable ticks, and a holographic encoder that
compresses and decompresses high-dimensional data.

These models are simplistic and meant to capture the qualitative behaviour
described in the white paper. They are not real quantum simulations.
"""

from dataclasses import dataclass, field
from typing import List
import random


@dataclass
class MajoranaQubitRegister:
    """
    Model a topological quantum processor using Majorana zero modes.

    The register tracks the number of logical qubits and the latency
    associated with each braiding operation. A simple compute method
    estimates the response time for a given number of operations,
    assuming each braiding operation has fixed latency.
    """
    logical_qubits: int = 64
    braid_latency_ns: float = 50.0  # latency per braid in ns
    operations_executed: int = 0

    def compute_response_time(self, num_operations: int) -> float:
        """
        Return the time in seconds required to perform a number of braiding operations.
        """
        if num_operations <= 0:
            return 0.0
        self.operations_executed += num_operations
        return (num_operations * self.braid_latency_ns) * 1e-9

    def reset(self) -> None:
        """Reset internal counters."""
        self.operations_executed = 0


@dataclass
class FractonMemory:
    """
    Model a fracton-based quantum memory with self-correcting properties.

    The memory stores an arbitrary list of floats (could represent model
    parameters or plasma state). It simulates extremely low error rates,
    with rare events flipping random bits. A scrub method can be invoked
    to correct any detected errors.
    """
    capacity_mb: float = 64.0
    error_rate_per_hour: float = 1e-9
    stored_data: List[float] = field(default_factory=list)
    total_errors: int = 0

    def write(self, data: List[float]) -> None:
        """Store data in memory. Overwrites existing content."""
        self.stored_data = data.copy()

    def read(self) -> List[float]:
        """
        Read the stored data, potentially with random bit flips based on the error rate.
        """
        if self.stored_data and random.random() < self.error_rate_per_hour * 1e-5:
            idx = random.randint(0, len(self.stored_data) - 1)
            self.stored_data[idx] *= (1.0 + random.uniform(-1e-6, 1e-6))
            self.total_errors += 1
        return self.stored_data.copy()

    def scrub(self) -> None:
        """Perform error correction by resetting any bit flips (assumes perfect ECC)."""
        self.total_errors = 0


@dataclass
class TimeCrystalClock:
    """
    Model a Floquet time crystal clock for synchronizing DBE subsystems.

    The clock emits ticks at a fixed period (tick_ns). The current tick can be
    obtained based on a simulated time in seconds.
    """
    tick_ns: float = 100.0
    start_time_s: float = 0.0

    def current_tick(self, current_time_s: float) -> int:
        """Return the tick index corresponding to the given simulation time."""
        elapsed_ns = (current_time_s - self.start_time_s) * 1e9
        if self.tick_ns <= 0:
            return 0
        return int(elapsed_ns // self.tick_ns)

    def sync_delay(self, current_time_s: float) -> float:
        """Return the time in seconds until the next tick."""
        if self.tick_ns <= 0:
            return 0.0
        elapsed_ns = (current_time_s - self.start_time_s) * 1e9
        remainder = elapsed_ns % self.tick_ns
        return (self.tick_ns - remainder) * 1e-9


@dataclass
class HolographicEncoder:
    """
    Model a holographic encoder that compresses and decompresses data.

    The encoder performs a simple down-sampling by averaging neighbouring
    values to reduce dimensionality. The decode method repeats each value
    to approximate the original length.
    """
    compression_factor: int = 2

    def encode(self, data: List[float]) -> List[float]:
        """Compress the data by averaging blocks of length compression_factor."""
        if self.compression_factor <= 0:
            return data.copy()
        comp_data: List[float] = []
        for i in range(0, len(data), self.compression_factor):
            block = data[i : i + self.compression_factor]
            if block:
                comp_data.append(sum(block) / len(block))
        return comp_data

    def decode(self, compressed: List[float], original_length: int) -> List[float]:
        """
        Decompress data by repeating each compressed value to reconstruct the original length.
        """
        if not compressed or original_length <= 0:
            return []
        repeat = max(1, original_length // len(compressed))
        decoded: List[float] = []
        for val in compressed:
            decoded.extend([val] * repeat)
        if len(decoded) > original_length:
            return decoded[:original_length]
        while len(decoded) < original_length:
            decoded.append(compressed[-1])
        return decoded
