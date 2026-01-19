import pandas as pd
import numpy as np


def calendar_arbitrage(df: pd.DataFrame):
    """
    Check for calendar arbitrage violations in option data.

    Calendar arbitrage occurs when a longer-dated option has lower implied
    volatility than a shorter-dated option at the same strike, which violates
    the no-arbitrage condition.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with columns: 'strike', 'time_to_maturity', 'implied_vol'

    Returns:
    --------
    list
        List of strikes that have calendar arbitrage violations
    """
    df = df.copy()
    df = df.sort_values(["strike", "time_to_maturity"])
    violations = []

    for strike, grp in df.groupby("strike"):
        T = grp["time_to_maturity"].values
        iv = grp["implied_vol"].values

        # Check if IV decreases as time to maturity increases
        # This would indicate a calendar arbitrage violation
        if len(T) > 1:
            # Sort by time to maturity to ensure proper comparison
            sort_idx = np.argsort(T)
            T_sorted = T[sort_idx]
            iv_sorted = iv[sort_idx]

            # Check if any longer-dated option has lower IV than
            # a shorter-dated one
            for i in range(len(T_sorted) - 1):
                if iv_sorted[i + 1] < iv_sorted[i]:
                    violations.append(strike)
                    break

    return violations
