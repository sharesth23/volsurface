import pandas as pd
import numpy as np
from typing import Optional
from volsurface.data.fetch_yahoo import load_all_expiries


def calendar_arbitrage(
    df: Optional[pd.DataFrame] = None,
    ticker: Optional[str] = None,
    expiry: Optional[str] = None
):
    if df is None:
        if ticker is not None:
            option_data = load_all_expiries(ticker)
            current_date = pd.Timestamp.now()
            option_data['time_to_maturity'] = (
                pd.to_datetime(option_data['expiry']) - current_date
            ).dt.days / 365.0

            df = pd.DataFrame({
                'strike': option_data['strike'].values,
                'time_to_maturity': option_data['time_to_maturity'].values,
                'implied_vol': option_data['impliedVolatility'].values
            })
            df = df.dropna(subset=['implied_vol'])

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
