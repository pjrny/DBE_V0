def test_package_imports():
    import dbe  # noqa: F401
    from dbe import plasma, actuators, quantum, controller, risk  # noqa
