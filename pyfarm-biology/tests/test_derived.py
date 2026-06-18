from pyfarm.biology.derived import ph_drift_rate, fermentation_efficiency, doubling_time_hours


def test_fermentation_efficiency():
    eff = fermentation_efficiency(1.060, 1.010)
    assert abs(eff - 83.33) < 1.0


def test_ph_drift_rate():
    readings = [(0.0, 6.0), (3600.0, 5.5), (7200.0, 5.0)]
    rate = ph_drift_rate(readings)
    assert abs(rate - (-0.5)) < 0.01


def test_doubling_time():
    readings_s = [(t * 3600, od) for t, od in [(0.0, 0.1), (1.0, 0.2), (2.0, 0.4), (3.0, 0.8)]]
    dt = doubling_time_hours(readings_s)
    assert dt is not None
    assert 0.9 < dt < 1.1
