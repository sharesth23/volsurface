import pandas as pd
import numpy as np
from typing import Optional
from volsurface.data.fetch_yahoo import load_all_expiries
from volsurface.iv.black_scholes import bs_call_price


def calendar_arbitrage(df: Optional[pd.DataFrame] = None, ticker: Optional[str] = None):
    if df is None:
        if ticker is not None:
            option_data = load_all_expiries(ticker)
            current_date = pd.Timestamp.now()
            option_data["time_to_maturity"] = (
                pd.to_datetime(option_data["expiry"]) - current_date
            ).dt.days / 365.0

            df = pd.DataFrame(
                {
                    "strike": option_data["strike"].values,
                    "time_to_maturity": option_data["time_to_maturity"].values,
                    "implied_vol": option_data["impliedVolatility"].values,
                }
            )
            df = df.dropna(subset=["implied_vol"])

    if df is None or df.empty:
        return []

    df = df.copy()
    df = df.sort_values(["strike", "time_to_maturity"])
    violations = []

    for strike, grp in df.groupby("strike"):
        T = grp["time_to_maturity"].values
        iv = grp["implied_vol"].values

        if len(T) > 1:
            sort_idx = np.argsort(T)
            T_sorted = T[sort_idx]
            iv_sorted = iv[sort_idx]

            for i in range(len(T_sorted) - 1):
                if iv_sorted[i + 1] < iv_sorted[i]:
                    violations.append(strike)
                    break

    return violations


def butterfly_arbitrage(df: pd.DataFrame, S: float = 100.0, r: float = 0.0):
    """
    Detects butterfly arbitrage violations.
    A violation occurs if the call price is not convex with respect to the strike.
    """
    if df is None or df.empty:
        return []

    violations = []

    # Check for each maturity
    for T, grp in df.groupby("time_to_maturity"):
        grp = grp.sort_values("strike")
        if len(grp) < 3:
            continue

        strikes = grp["strike"].values
        vols = grp["implied_vol"].values

        prices = bs_call_price(S, strikes, T, r, vols)

        for i in range(1, len(strikes) - 1):
            K1, K2, K3 = strikes[i - 1], strikes[i], strikes[i + 1]
            C1, C2, C3 = prices[i - 1], prices[i], prices[i + 1]

            # Convexity condition: (C1 - C2)/(K2 - K1) >= (C2 - C3)/(K3 - K2)
            # Since C is decreasing, slopes are negative.
            # This is equivalent to C2 <= C1 * (K3-K2)/(K3-K1) + C3 * (K2-K1)/(K3-K1)

            weight = (K3 - K2) / (K3 - K1)
            if (
                C2 > weight * C1 + (1 - weight) * C3 + 1e-7
            ):  # small epsilon for numerical stability
                violations.append((T, K2))

    return violations
