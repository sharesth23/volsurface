import pandas as pd 

def calendar_arbitrage_check(df):
    df = df.sort_values(["strike", "time_to_maturity"])
    violations = []

    for strike, grp in df.groupby("strike"):
        iv_diff = np.diff(grp["implied_vol"].values)
        if np.any(iv_diff < -0.01):
            violations.append(strike)

    return violations

def butterfly_arbitrage(df):
    violations = []

    for T, grp in df.groupby("time_to_maturity"):
        grp = grp.sort_values("strike")
        strikes = grp["strike"].values
        vols = grp["implied_vol"].values

        second_derivative = np.diff(vols, 2)
        if np.any(second_derivative < -0.01):
            violations.append(T)

    return violations