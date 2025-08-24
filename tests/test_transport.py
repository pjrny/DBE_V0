from dbe.plasma import create_radial_grid, initialize_profiles, TransportSimulator, PlasmaParams, Profiles


def test_radial_grid():
    grid = create_radial_grid(1.0, 5)
    assert len(grid) == 5
    assert grid[0] == 0
    assert abs(grid[-1] - 1.0) < 1e-8


def test_initialize_profiles_length():
    state = initialize_profiles(PlasmaParams(), Profiles(), npoints=11)
    assert len(state.r) == 11
    assert len(state.T_keV) == 11


def test_transport_step_reduces_core_temp():
    params = PlasmaParams(minor_radius=1.0)
    profiles = Profiles(T0_keV=10.0)
    state = initialize_profiles(params, profiles, npoints=11)
    sim = TransportSimulator(state, profiles)
    core_temp_before = state.T_keV[0]
    sim.step(dt=0.01)
    core_temp_after = state.T_keV[0]
    assert core_temp_after <= core_temp_before
