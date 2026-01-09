import numpy as np
from scipy.optimize import minimize
from sabr import sabr_implied_vol

def sabr_calibration(strikes, maturities, prices, F, r):
    def objective(params):
        alpha, beta, rho, nu = params
        errors = []

        for i in range(len(strikes)):
            K = strikes[i]
            T = maturities[i]
            P = prices[i]
            error = P - sabr_implied_vol(F, K, T, alpha, beta, rho, nu)
            errors.append(error)
        return np.sum(errors**2)