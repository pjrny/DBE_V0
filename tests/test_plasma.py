from dbe.plasma import spitzer_resistivity_ohm_m


def test_spitzer_basic():
    eta_hot = spitzer_resistivity_ohm_m(Te_eV=1e4)
    eta_cool = spitzer_resistivity_ohm_m(Te_eV=10)
    assert eta_hot < eta_cool
