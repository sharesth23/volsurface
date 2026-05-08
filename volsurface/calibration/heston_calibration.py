import numpy as np
from scipy.optimize import minimize
from volsurface.models.heston import heston_implied_vol

def calibrate_heston(F, strikes, maturities, market_vols):
    """
    Calibrate Heston model parameters to market implied volatilities.
    """
    def objective(params):
        v0, kappa, theta, sigma, rho = params

        # Feller condition penalty
        penalty = 0.0
        if 2 * kappa * theta < sigma**2:
            penalty = 1e6 * (sigma**2 - 2 * kappa * theta)

        model_vols = []
        for K, T in zip(strikes, maturities):
            iv = heston_implied_vol(F, K, T, v0, kappa, theta, sigma, rho)
            if np.isnan(iv):
                return 1e6
            model_vols.append(iv)

        mse = np.mean((np.array(model_vols) - market_vols)**2)
        return mse + penalty

    # Bounds: v0 > 0, kappa > 0, theta > 0, sigma > 0, rho in [-1, 1]
    bounds = [
        (1e-4, 1.0),    # v0
        (1e-4, 10.0),   # kappa
        (1e-4, 1.0),    # theta
        (1e-4, 5.0),    # sigma
        (-0.999, 0.999) # rho
    ]

    # Initial guess
    x0 = [0.04, 2.0, 0.04, 0.2, -0.5]

    res = minimize(objective, x0, bounds=bounds, method="L-BFGS-B")

    return dict(
        v0=res.x[0],
        kappa=res.x[1],
        theta=res.x[2],
        sigma=res.x[3],
        rho=res.x[4]
    )
