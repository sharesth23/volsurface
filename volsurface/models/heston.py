import numpy as np
from scipy.integrate import quad
from scipy.optimize import root_scalar


def heston_cf(u, T, v0, kappa, theta, sigma, rho):
    """
    Characteristic function of the Heston model.
    """
    alpha = -u * u / 2 - 1j * u / 2
    beta = kappa - rho * sigma * 1j * u
    gamma = sigma * sigma / 2

    # Calculate d
    d = np.sqrt(beta * beta - 4 * alpha * gamma)

    # Calculate r_plus and r_minus
    r_plus = (beta + d) / (2 * gamma)
    r_minus = (beta - d) / (2 * gamma)

    # Calculate g
    g = r_minus / r_plus

    # Calculate C and D
    C = kappa * (
        r_minus * T - (2 / sigma**2) * np.log((1 - g * np.exp(-d * T)) / (1 - g))
    )
    D = r_minus * (1 - np.exp(-d * T)) / (1 - g * np.exp(-d * T))

    return np.exp(C * theta + D * v0)


def heston_call_price(F, K, T, v0, kappa, theta, sigma, rho):
    """
    Computes European Call option price under the Heston model.
    """
    if F <= 0 or K <= 0 or T <= 0:
        return max(F - K, 0)

    k = np.log(K / F)

    def integrand(u):
        cf = heston_cf(u - 0.5j, T, v0, kappa, theta, sigma, rho)
        num = np.exp(-1j * u * k) * cf
        den = u**2 + 0.25
        return num.real / den

    integral, _ = quad(integrand, 0, np.inf, limit=200)
    return F - np.sqrt(K * F) / np.pi * integral


def heston_implied_vol(F, K, T, v0, kappa, theta, sigma, rho):
    """
    Computes Implied Volatility for the Heston model by first calculating the
    option price and then backing out the Black-Scholes implied volatility.
    """
    price = heston_call_price(F, K, T, v0, kappa, theta, sigma, rho)

    if price <= max(F - K, 0):
        return np.nan

    from volsurface.iv.black_scholes import bs_call_price

    def objective(vol):
        return bs_call_price(F, K, T, 0.0, vol) - price

    try:
        res = root_scalar(objective, bracket=[1e-5, 5.0], method="brentq")
        return res.root
    except ValueError:
        return np.nan
