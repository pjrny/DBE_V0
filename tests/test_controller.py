from dbe.controller import DBEController
from dbe.plasma import PlasmaState


def test_controller_high_stability():
    controller = DBEController()
    ps = PlasmaState(stability=0.8)
    decision = controller.decide(ps)
    assert decision["rmp_current"] == 0.0
    assert decision["pellet_fire"] is False
    assert controller.last_decision == decision


def test_controller_mid_stability():
    controller = DBEController()
    ps = PlasmaState(stability=0.5)
    decision = controller.decide(ps)
    assert decision["rmp_current"] == 0.5 * controller.rmp_coil.I_max
    assert decision["pellet_fire"] is False


def test_controller_low_stability():
    controller = DBEController()
    ps = PlasmaState(stability=0.2)
    decision = controller.decide(ps)
    assert decision["rmp_current"] == controller.rmp_coil.I_max
    assert decision["pellet_fire"] is True
