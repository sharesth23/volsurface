import numpy as np 

def svi_total_variance(k, a, b, rho, m, sigma):
    return a + b * (rho * (k - m) + np.sqrt((k - m)**2 + sigma**2))

def svi_implied_vol(F, K, T, params):
    if np.any(np.asarray(T) <= 0):
        raise ValueError("Time to maturity (T) must be strictly positive.")
    k = np.log(K / F)
    w = svi_total_variance(k, **params)
    return np.sqrt(w / T)
