import pandas as pd
import numpy as np

def filter_otm_options(df, F):
    """
    Filters for Out-of-the-Money (OTM) options.
    OTM calls have strike > F.
    OTM puts have strike < F.
    OTM options are typically more liquid and have cleaner IVs.
    """
    if df is None or df.empty:
        return df

    otm_calls = df[(df["type"] == "call") & (df["strike"] >= F)]
    otm_puts = df[(df["type"] == "put") & (df["strike"] < F)]

    return pd.concat([otm_calls, otm_puts], ignore_index=True)

def estimate_forward_price(df):
    """
    Estimates forward price using Put-Call parity for At-the-Money options.
    C - P = (F - K) * exp(-rT)
    Assuming r=0 for simplicity, F = C - P + K
    """
    if df is None or df.empty:
        return None

    # Find closest strikes for calls and puts
    # This is a simplistic estimation
    unique_expiries = df["expiry"].unique()
    forward_prices = {}

    for exp in unique_expiries:
        grp = df[df["expiry"] == exp]
        # Find ATM options (where call and put prices are closest or strike is near spot)
        # For simplicity, just use the first strike that has both call and put
        common_strikes = set(grp[grp["type"] == "call"]["strike"]) & set(grp[grp["type"] == "put"]["strike"])
        if not common_strikes:
            continue

        # Pick one strike (e.g. median)
        K = sorted(list(common_strikes))[len(common_strikes)//2]
        C = grp[(grp["type"] == "call") & (grp["strike"] == K)]["mid"].values[0]
        P = grp[(grp["type"] == "put") & (grp["strike"] == K)]["mid"].values[0]

        F_est = C - P + K
        forward_prices[exp] = F_est

    if not forward_prices:
        return None

    return np.mean(list(forward_prices.values()))
