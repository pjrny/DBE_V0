from dbe.actuators import RMPCoil, PelletInjector
from dbe.plasma import PlasmaParams, Profiles, create_radial_grid, initialize_profiles, TransportSimulator


def test_rmp_threshold_multiplier():
    coil = RMPCoil(I_max=1.0)
    # At zero current threshold multiplier should be 1
    coil.I_set = 0.0
    assert coil.elm_threshold_multiplier() == 1.0
    # At half current should be 1.25 (1 + 0.5 * 0.5)
    coil.I_set = 0.5
    assert abs(coil.elm_threshold_multiplier() - 1.25) < 1e-6
    # At full current should be 1.5
    coil.I_set = 1.0
    assert abs(coil.elm_threshold_multiplier() - 1.5) < 1e-6


def test_rmp_confinement_penalty():
    coil = RMPCoil(I_max=1.0)
    # At zero current penalty should be 1
    coil.I_set = 0.0
    assert coil.confinement_penalty() == 1.0
    # Half current penalty should be 1 - 0.05 * 0.5 = 0.975
    coil.I_set = 0.5
    assert abs(coil.confinement_penalty() - 0.975) < 1e-6
    # Full current penalty should be 0.95
    coil.I_set = 1.0
    assert abs(coil.confinement_penalty() - 0.95) < 1e-6


def test_pellet_injector_fire():
    # Create a basic plasma and transport simulator
    params = PlasmaParams()
    r = create_radial_grid(params.minor_radius, 100)
    profiles = Profiles()
    state = initialize_profiles(r, profiles)
    sim = TransportSimulator(r, state)
    injector = PelletInjector(rate_max_hz=10.0, size_max=1.0)
    t0 = 0.0
    # copy initial temperature profile
    original_T = list(sim.state.T_keV)
    # fire pellet of maximum size
    fired = injector.fire(sim, t0, size=1.0)
    assert fired is True
    # drop fraction should be 0.05 at full size
    drop_fraction = 0.05 * (1.0 / injector.size_max)
    # check that last element decreased appropriately
    assert abs(sim.state.T_keV[-1] - original_T[-1] * (1.0 - drop_fraction)) < 1e-8
    # second firing too soon should be suppressed
    fired2 = injector.fire(sim, t0 + 0.05, size=1.0)
    assert fired2 is False
