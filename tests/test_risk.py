from dbe.risk import assess_placeholder


def test_placeholder():
    r = assess_placeholder(None)
    assert r.score == 0.0
    assert r.notes
