import numpy as np
import pytest
from volsurface.models.svi import svi_total_variance, svi_implied_vol

def test_svi_total_variance_scalar():
    k = 0.0
    a = 0.04
    b = 0.1
    rho = -0.5
    m = 0.1
    sigma = 0.1

    expected = a + b * (rho * (k - m) + np.sqrt((k - m)**2 + sigma**2))
    result = svi_total_variance(k, a, b, rho, m, sigma)

    assert np.isclose(result, expected)

def test_svi_total_variance_array():
    k = np.array([-0.1, 0.0, 0.1])
    a = 0.04
    b = 0.1
    rho = -0.5
    m = 0.1
    sigma = 0.1

    expected = a + b * (rho * (k - m) + np.sqrt((k - m)**2 + sigma**2))
    result = svi_total_variance(k, a, b, rho, m, sigma)

    np.testing.assert_allclose(result, expected)

def test_svi_implied_vol_scalar():
    F = 100.0
    K = 105.0
    T = 1.0
    params = {'a': 0.04, 'b': 0.1, 'rho': -0.5, 'm': 0.1, 'sigma': 0.1}

    k = np.log(K / F)
    expected_w = svi_total_variance(k, **params)
    expected_iv = np.sqrt(expected_w / T)

    result = svi_implied_vol(F, K, T, params)

    assert np.isclose(result, expected_iv)

def test_svi_implied_vol_array():
    F = 100.0
    K = np.array([90.0, 100.0, 110.0])
    T = 1.0
    params = {'a': 0.04, 'b': 0.1, 'rho': -0.5, 'm': 0.1, 'sigma': 0.1}

    k = np.log(K / F)
    expected_w = svi_total_variance(k, **params)
    expected_iv = np.sqrt(expected_w / T)

    result = svi_implied_vol(F, K, T, params)

    np.testing.assert_allclose(result, expected_iv)

def test_svi_implied_vol_negative_t():
    F = 100.0
    K = 100.0
    T = 0.0
    params = {'a': 0.04, 'b': 0.1, 'rho': -0.5, 'm': 0.1, 'sigma': 0.1}

    with pytest.raises(ValueError, match="Time to maturity \\(T\\) must be strictly positive."):
        svi_implied_vol(F, K, T, params)

def test_svi_implied_vol_negative_t_array():
    F = 100.0
    K = 100.0
    T = np.array([1.0, 0.0, 2.0])
    params = {'a': 0.04, 'b': 0.1, 'rho': -0.5, 'm': 0.1, 'sigma': 0.1}

    with pytest.raises(ValueError, match="Time to maturity \\(T\\) must be strictly positive."):
        svi_implied_vol(F, K, T, params)
