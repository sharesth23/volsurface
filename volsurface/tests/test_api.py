import pandas as pd
import numpy as np
import pytest
from volsurface.api import VolSurfaceAPI

def test_api_invalid_model_calibration():
    # Mock data
    F = 100.0
    strikes = np.array([90, 95, 100, 105, 110])
    maturities = np.array([1.0, 1.0, 1.0, 1.0, 1.0])
    vols = np.array([0.3, 0.28, 0.25, 0.26, 0.29])

    df = pd.DataFrame({
        "strike": strikes,
        "time_to_maturity": maturities,
        "implied_vol": vols
    })

    api = VolSurfaceAPI(df, model="unsupported", F=F)

    with pytest.raises(ValueError, match="Model must be 'svi' or 'sabr'"):
        api.calibrate()

def test_api_sabr_calibration():
    # Mock data
    F = 100.0
    strikes = np.array([90, 95, 100, 105, 110])
    maturities = np.array([1.0, 1.0, 1.0, 1.0, 1.0])
    vols = np.array([0.3, 0.28, 0.25, 0.26, 0.29])

    df = pd.DataFrame({
        "strike": strikes,
        "time_to_maturity": maturities,
        "implied_vol": vols
    })

    api = VolSurfaceAPI(df, model="sabr", F=F)
    api.calibrate()

    # Check if we can get IV
    iv = api.iv(100, 1.0)
    assert isinstance(iv, float)
    assert iv > 0

def test_api_svi_calibration():
    # Mock data
    F = 100.0
    strikes = np.array([90, 95, 100, 105, 110])
    maturities = np.array([1.0, 1.0, 1.0, 1.0, 1.0])
    vols = np.array([0.3, 0.28, 0.25, 0.26, 0.29])

    df = pd.DataFrame({
        "strike": strikes,
        "time_to_maturity": maturities,
        "implied_vol": vols
    })

    api = VolSurfaceAPI(df, model="svi", F=F)
    api.calibrate()

    # Check if we can get IV
    iv = api.iv(100, 1.0)
    assert isinstance(iv, float)
    assert iv > 0
