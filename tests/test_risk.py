from dbe.risk import RiskAnalyzer, assess_placeholder
from dbe.plasma import PlasmaState


class DummyCoil:
    def __init__(self, I_set: float, I_max: float) -> None:
        self.I_set = I_set
        self.I_max = I_max


class DummyPellet:
    def __init__(self, available: bool = True) -> None:
        self.available = available

    def can_fire(self, _time: float) -> bool:
        return self.available


class DummyMemory:
    def __init__(self, error_count: int) -> None:
        self.error_count = error_count


class DummyController:
    def __init__(self, coil: DummyCoil, pellet: DummyPellet, memory: DummyMemory) -> None:
        self.rmp_coil = coil
        self.pellet_injector = pellet
        self.memory = memory


def test_placeholder():
    """Ensure backwards-compatible assess_placeholder returns non-empty notes."""
    report = assess_placeholder(None)
    assert report.score == 0.0
    assert report.notes


def test_low_risk():
    """High stability, no saturation, pellet available → low risk."""
    plasma = PlasmaState()
    plasma.stability = 0.8
    controller = DummyController(
        DummyCoil(I_set=0.0, I_max=1.0),
        DummyPellet(available=True),
        DummyMemory(error_count=0),
    )
    analyzer = RiskAnalyzer()
    report = analyzer.assess(plasma, controller)
    assert report.score < 0.3
    assert report.notes == []


def test_high_risk():
    """Low stability, coil saturated, pellet unavailable, memory errors → max risk."""
    plasma = PlasmaState()
    plasma.stability = 0.2
    controller = DummyController(
        DummyCoil(I_set=1.0, I_max=1.0),
        DummyPellet(available=False),
        DummyMemory(error_count=2),
    )
    analyzer = RiskAnalyzer()
    report = analyzer.assess(plasma, controller)
    assert report.score == 1.0
    assert any("RMP coil" in note for note in report.notes)
    assert any("Pellet injector" in note for note in report.notes)
    assert any("memory error count" in note for note in report.notes)
