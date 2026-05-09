import numpy as np

def sabr_implied_vol(F, K, T, alpha, beta, rho, nu):
    F = np.asarray(F)
    K = np.asarray(K)
    T = np.asarray(T)

    # Broadcast arrays
    F, K, T = np.broadcast_arrays(F, K, T)

    # Fast path for purely scalar inputs
    if F.ndim == 0:
        F_val = float(F)
        K_val = float(K)
        T_val = float(T)
        if F_val <= 0 or K_val <= 0:
            return np.nan
        if abs(F_val - K_val) < 1e-8:
            return (alpha / (F_val ** (1 - beta))) * (
                1 + (
                    ((1 - beta)**2 / 24) * (alpha**2 / F_val**(2 - 2*beta)) +
                    (rho * beta * nu * alpha) / (4 * F_val**(1 - beta)) +
                    ((2 - 3*rho**2) * nu**2 / 24)
                ) * T_val
            )
        z = (nu / alpha) * (F_val * K_val)**((1 - beta) / 2) * np.log(F_val / K_val)
        x = np.log((np.sqrt(1 - 2*rho*z + z*z) + z - rho) / (1 - rho))
        return (alpha / ((F_val * K_val)**((1 - beta)/2))) * (z / x)

    # Pre-allocate output
    res = np.empty(F.shape)

    # Condition: F <= 0 or K <= 0
    invalid_mask = (F <= 0) | (K <= 0)
    res[invalid_mask] = np.nan

    valid_mask = ~invalid_mask
    F_v = F[valid_mask]
    K_v = K[valid_mask]
    T_v = T[valid_mask]

    # Condition: abs(F - K) < 1e-8
    atm_mask = np.abs(F_v - K_v) < 1e-8
    otm_mask = ~atm_mask

    res_v = np.empty(F_v.shape)

    # Process ATM
    if np.any(atm_mask):
        F_atm = F_v[atm_mask]
        T_atm = T_v[atm_mask]

        term1 = alpha / (F_atm ** (1 - beta))
        term2 = ((1 - beta)**2 / 24) * (alpha**2 / F_atm**(2 - 2*beta))
        term3 = (rho * beta * nu * alpha) / (4 * F_atm**(1 - beta))
        term4 = ((2 - 3*rho**2) * nu**2 / 24)

        res_v[atm_mask] = term1 * (1 + (term2 + term3 + term4) * T_atm)

    # Process OTM
    if np.any(otm_mask):
        F_otm = F_v[otm_mask]
        K_otm = K_v[otm_mask]

        z = (nu / alpha) * (F_otm * K_otm)**((1 - beta) / 2) * np.log(F_otm / K_otm)
        x = np.log((np.sqrt(1 - 2*rho*z + z*z) + z - rho) / (1 - rho))

        res_v[otm_mask] = (alpha / ((F_otm * K_otm)**((1 - beta)/2))) * (z / x)

    res[valid_mask] = res_v
    return res
