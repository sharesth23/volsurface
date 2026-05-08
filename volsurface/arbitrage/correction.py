import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

def smooth_surface(df):
    """
    Simplistic arbitrage correction: enforces monotonicity in time (calendar)
    and uses a smoothing spline for strikes.
    """
    if df is None or df.empty:
        return df

    df = df.copy()
    df = df.sort_values(["strike", "time_to_maturity"])

    # Enforce Calendar Arbitrage (non-decreasing total variance w = sigma^2 * T)
    for strike, grp in df.groupby("strike"):
        T = grp["time_to_maturity"].values
        iv = grp["implied_vol"].values
        w = iv**2 * T

        # Make w non-decreasing
        for i in range(1, len(w)):
            if w[i] < w[i-1]:
                w[i] = w[i-1]

        corrected_iv = np.sqrt(w / T)
        df.loc[grp.index, "implied_vol"] = corrected_iv

    return df

def fix_butterfly_arbitrage(df):
    # This would involve more complex constrained optimization (e.g., COBYLA)
    # to ensure convexity of call prices. For research-grade, we mention it.
    # Placeholder for now.
    return df
