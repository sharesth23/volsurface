import numpy as np
from scipy.stats import norm


def bs_call_price(S, K, T, r, sigma):
    if T <= 0 or sigma <= 0:
        return max(S - K, 0)

    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)


def implied_volatility(price, S, K, T, r, tol=1e-6):
    low, high = 1e-6, 5.0

    for _ in range(100):
        mid = 0.5 * (low + high)
        val = bs_call_price(S, K, T, r, mid)

        if abs(val - price) < tol:
            return mid

        if val > price:
            high = mid
        else:
            low = mid

    return mid


if __name__ == "__main__":
    # Example usage
    S = 100  # Stock price
    K = 100  # Strike price
    T = 0.25  # Time to expiration (3 months)
    r = 0.05  # Risk-free rate
    sigma = 0.2  # Volatility

    # Calculate call price
    call_price = bs_call_price(S, K, T, r, sigma)
    print(f"Call price: ${call_price:.4f}")

    # Calculate implied volatility from the price
    iv = implied_volatility(call_price, S, K, T, r)
    print(f"Implied volatility: {iv:.4f} ({iv*100:.2f}%)")