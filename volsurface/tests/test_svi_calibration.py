import numpy as np
from volsurface.calibration.svi_calibration import calibrate_svi


def test_calibrate_svi_returns_correct_structure():
    F = 100
    strikes = np.array([90, 95, 100, 105, 110])
    T = 1.0
    vols = np.array([0.25, 0.22, 0.20, 0.22, 0.25])

    res = calibrate_svi(F, strikes, T, vols)

    assert isinstance(res, dict)
    expected_keys = {"a", "b", "rho", "m", "sigma"}
    assert set(res.keys()) == expected_keys

    for key in expected_keys:
        assert isinstance(res[key], (float, np.floating))


def test_calibrate_svi_bounds_and_validity():
    F = 100
    strikes = np.array([90, 95, 100, 105, 110])
    T = 1.0
    vols = np.array([0.25, 0.22, 0.20, 0.22, 0.25])

    res = calibrate_svi(F, strikes, T, vols)

    # Check theoretical/optimization bounds used in the scipy minimize call
    # bounds=[(0, None), (0, None), (-1, 1), (0, None), (0, None)]
    # (a, b, rho, m, sigma)
    assert res["a"] >= 0
    assert res["b"] >= 0
    assert -1 <= res["rho"] <= 1
    assert res["m"] >= 0
    assert res["sigma"] >= 0
