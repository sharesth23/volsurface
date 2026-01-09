import pandas as pd 

def calendar_arbitrage_check(df):
    df = df.sort_values(["strike", "time_to_maturity"])
    violations = []

    for strike, grp in df.groupby("strike"):
        iv_diff = np.diff(grp["implied_vol"].values)
        if np.any(iv_diff < -0.01):
            violations.append(strike)

    return violations