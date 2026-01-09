import numpy as np

def sabr_implied_vol(F, K, T, alpha, beta, rho, nu):
    if F <= 0 or K <= 0:
        return np.nan

    if abs(F - K) < 1e-8:
        return (alpha / (F ** (1 - beta))) * (
            1 + (
                ((1 - beta)**2 / 24) * (alpha**2 / F**(2 - 2*beta)) +
                (rho * beta * nu * alpha) / (4 * F**(1 - beta)) +
                ((2 - 3*rho**2) * nu**2 / 24)
            ) * T
        )

    z = (nu / alpha) * (F * K)**((1 - beta) / 2) * np.log(F / K)
    x = np.log((np.sqrt(1 - 2*rho*z + z*z) + z - rho) / (1 - rho))

    return (alpha / ((F * K)**((1 - beta)/2))) * (z / x)
