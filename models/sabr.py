import numpy as np
from scipy.optimize import minimize

def sabr_vol(F, K, T, alpha, beta, rho, nu):
    if F == K:
        return alpha / (F ** (1 - beta))

    z = (nu / alpha) * (F * K) ** ((1 - beta) / 2) * np.log(F / K)
    x = np.log((np.sqrt(1 - 2 * rho * z + z**2) + z - rho) / (1 - rho))

    return (alpha / ((F * K) ** ((1 - beta) / 2))) * (z / x)