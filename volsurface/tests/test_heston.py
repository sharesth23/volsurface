import numpy as np
import pytest
from volsurface.models.heston import heston_call_price, heston_implied_vol
from volsurface.calibration.heston_calibration import calibrate_heston

def test_heston_call_price():
    F = 100.0
    K = 100.0
    T = 1.0
    v0, kappa, theta, sigma, rho = 0.04, 2.0, 0.04, 0.2, -0.5
    price = heston_call_price(F, K, T, v0, kappa, theta, sigma, rho)

    assert not np.isnan(price)
    assert price > 0
    # Expected approximate price for these standard parameters
    assert np.isclose(price, 7.81, atol=0.1)

def test_heston_implied_vol():
    F = 100.0
    K = 100.0
    T = 1.0
    v0, kappa, theta, sigma, rho = 0.04, 2.0, 0.04, 0.2, -0.5
    iv = heston_implied_vol(F, K, T, v0, kappa, theta, sigma, rho)

    assert not np.isnan(iv)
    assert iv > 0
    # Expected approximate IV
    assert np.isclose(iv, 0.196, atol=0.01)

def test_calibrate_heston():
    F = 100.0
    strikes = np.array([90, 100, 110])
    maturities = np.array([1.0, 1.0, 1.0])
    market_vols = np.array([0.22, 0.20, 0.19])

    res = calibrate_heston(F, strikes, maturities, market_vols)

    assert "v0" in res
    assert "kappa" in res
    assert "theta" in res
    assert "sigma" in res
    assert "rho" in res

    assert res["v0"] > 0
    assert res["kappa"] > 0
    assert res["theta"] > 0
    assert res["sigma"] > 0
    assert -1 <= res["rho"] <= 1
