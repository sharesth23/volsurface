import numpy as np
from scipy.stats import norm 

def bs_call_price(S, K, T, r, sigma):
    S = np.asarray(S)
    K = np.asarray(K)
    T = np.asarray(T)
    r = np.asarray(r)
    sigma = np.asarray(sigma)

    is_scalar = S.ndim == 0 and K.ndim == 0 and T.ndim == 0 and r.ndim == 0 and sigma.ndim == 0

    with np.errstate(divide='ignore', invalid='ignore'):
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        call_prices = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

    intrinsic = np.maximum(S - K, 0)

    condition = (T > 0) & (sigma > 0)

    result = np.where(condition, call_prices, intrinsic)

    if is_scalar:
        return result.item()
    return result



 