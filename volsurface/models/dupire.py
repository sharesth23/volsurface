import numpy as np

def dupire_local_vol(T, K, surface, F, dK=0.01, dT=0.01):
    """
    Computes Dupire local volatility from an implied volatility surface.

    Parameters:
    - T: Time to maturity
    - K: Strike price
    - surface: An object with an `iv(K, T)` method that returns the implied volatility.
    - dK: Step size for strike derivative
    - dT: Step size for time derivative

    Returns:
    - Local volatility at (T, K)
    """
    iv = surface.iv(K, T)

    # Implied variance
    w = iv**2 * T

    # Time derivative of implied variance
    iv_dt = surface.iv(K, T + dT)
    w_dt = iv_dt**2 * (T + dT)
    dw_dT = (w_dt - w) / dT

    # Strike derivatives of implied variance
    iv_up = surface.iv(K + dK, T)
    iv_dn = surface.iv(K - dK, T)
    w_up = iv_up**2 * T
    w_dn = iv_dn**2 * T

    dw_dK = (w_up - w_dn) / (2 * dK)
    d2w_dK2 = (w_up - 2 * w + w_dn) / (dK**2)

    # Gatheral's formula for local variance:
    # y = log(K/F), but here we assume F=100 (or drift=0 so F=S)
    # The simpler formula in terms of K:
    # sigma_L^2 = dw/dT / (1 - (K/w)*dw_dK + 0.25*(-0.25 - 1/w + K^2/w^2)*(dw_dK)^2 + 0.5 * K^2 * d2w_dK2)

    # Convert derivatives with respect to K to derivatives with respect to y = log(K/F)
    # y = log(K) - log(F), dy = dK / K
    y = np.log(K / F) # log-moneyness y = log(K/F)

    # Let's use the Gatheral formulation with y = log(K/S_0) assuming r=0, q=0
    # y = log(K/S)
    # dw/dy = K * dw/dK
    dw_dy = K * dw_dK
    # d^2w/dy^2 = K^2 * d^2w/dK^2 + K * dw/dK
    d2w_dy2 = K**2 * d2w_dK2 + K * dw_dK

    # Gatheral's formula:
    # v_L(y, T) = dw/dT / [1 - (y/w)*dw/dy + 0.25*(-0.25 - 1/w + y^2/w^2)*(dw/dy)^2 + 0.5*d^2w/dy^2]

    den = 1.0 - (y / w) * dw_dy + 0.25 * (-0.25 - 1.0 / w + (y**2) / (w**2)) * (dw_dy**2) + 0.5 * d2w_dy2

    if den <= 0 or dw_dT < 0:
        return np.nan

    return np.sqrt(dw_dT / den)
