import numpy as np
from scipy.optimize import minimize
from volsurface.models.sabr import sabr_implied_vol


def calibrate_sabr(F, strikes, maturities, market_vols, beta=0.5):
    def objective(params):
        alpha, rho, nu = params
        model_vols = [
            sabr_implied_vol(F, K, T, alpha, beta, rho, nu)
            for K, T in zip(strikes, maturities)
        ]
        return np.mean((np.array(model_vols) - market_vols)**2)

    bounds = [(1e-4, 5.0), (-0.999, 0.999), (1e-4, 5.0)]
    x0 = [0.2, 0.0, 0.5]

    res = minimize(objective, x0, bounds=bounds, method="L-BFGS-B")
    return dict(alpha=res.x[0], beta=beta, rho=res.x[1], nu=res.x[2])
