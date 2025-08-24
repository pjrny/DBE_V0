import time
from dbe.quantum import MajoranaQubitRegister, FractonMemory, TimeCrystalClock, HolographicEncoder


def test_majorana_compute_response_time():
    # Each operation takes braid_latency_ns nanoseconds, converted to seconds
    q = MajoranaQubitRegister(logical_qubits=8, braid_latency_ns=100.0)
    t = q.compute_response_time(num_operations=5)
    assert abs(t - (5 * 100.0 / 1e9)) < 1e-12


def test_fracton_memory_write_read_scrub():
    # Error rate zero ensures deterministic reads
    memory = FractonMemory(capacity_mb=1.0, error_rate_per_hour=0.0)
    data = [1, 2, 3]
    memory.write("foo", data)
    read_data = memory.read("foo")
    assert read_data == data
    # No errors injected
    assert memory.error_count == 0
    memory.scrub()
    assert memory.error_count == 0


def test_time_crystal_sync_delay():
    # A small tick duration (1 ms)
    clock = TimeCrystalClock(tick_ns=1_000_000)  # 1 ms in ns
    delay = clock.sync_delay()
    # Delay should be non-negative and less than one tick (converted to seconds)
    tick_s = clock.tick_ns / 1e9
    assert 0.0 <= delay < tick_s


def test_holographic_encoder_roundtrip():
    encoder = HolographicEncoder(block_size=2)
    arr = [1.0, 2.0, 3.0, 4.0]
    encoded = encoder.encode(arr)
    # Each block averaged
    assert encoded == [(1.0 + 2.0) / 2, (3.0 + 4.0) / 2]
    decoded = encoder.decode(encoded, original_length=len(arr))
    # Decoded length matches original
    assert len(decoded) == len(arr)
    # Each pair of entries matches the block average
    assert decoded == [1.5, 1.5, 3.5, 3.5]
