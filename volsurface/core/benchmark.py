import numpy as np
import pandas as pd
from volsurface.calibration.sabr_calibration import calibrate_sabr
from volsurface.calibration.svi_calibration import calibrate_svi
from volsurface.models.sabr import sabr_implied_vol
from volsurface.models.svi import svi_implied_vol
from scipy.interpolate import SmoothBivariateSpline

def calculate_rmse(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred)**2))

def calculate_mae(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))

def run_benchmark(F, strikes, maturities, market_vols):
    """
    Compares SABR, SVI, and Spline models.
    """
    results = {}

    # SABR Calibration
    sabr_params = calibrate_sabr(F, strikes, maturities, market_vols)
    sabr_vols = np.array([
        sabr_implied_vol(F, K, T, sabr_params['alpha'], sabr_params['beta'], sabr_params['rho'], sabr_params['nu'])
        for K, T in zip(strikes, maturities)
    ])
    results['SABR'] = {
        'rmse': calculate_rmse(market_vols, sabr_vols),
        'mae': calculate_mae(market_vols, sabr_vols),
        'params': sabr_params
    }

    # SVI Calibration
    unique_T = np.unique(maturities)
    svi_vols = np.zeros_like(market_vols)
    svi_params_list = {}
    for T in unique_T:
        mask = maturities == T
        if np.any(mask):
            params = calibrate_svi(F, strikes[mask], T, market_vols[mask])
            svi_params_list[T] = params
            for i, (K, m_T) in enumerate(zip(strikes, maturities)):
                if m_T == T:
                    svi_vols[i] = svi_implied_vol(F, K, T, params)

    results['SVI'] = {
        'rmse': calculate_rmse(market_vols, svi_vols),
        'mae': calculate_mae(market_vols, svi_vols),
        'params': svi_params_list
    }

    # Spline
    # SmoothBivariateSpline needs at least (kx+1)*(ky+1) points, defaults to 4x4=16.
    # For small data, we'll use a simpler interpolation or skip.
    try:
        if len(strikes) >= 16:
            spline = SmoothBivariateSpline(strikes, maturities, market_vols)
            spline_vols = np.array([float(spline(K, T)) for K, T in zip(strikes, maturities)])
            results['Spline'] = {
                'rmse': calculate_rmse(market_vols, spline_vols),
                'mae': calculate_mae(market_vols, spline_vols)
            }
        else:
            results['Spline'] = {'status': 'Insufficient data for Spline (min 16 points)'}
    except Exception as e:
        results['Spline'] = {'status': f'Error: {str(e)}'}

    return results
