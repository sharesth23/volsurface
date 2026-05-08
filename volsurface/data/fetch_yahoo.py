import yfinance as yf
import pandas as pd
import numpy as np

def fetch_option_chain(ticker, expiry):
    """
    Fetches both calls and puts for a given ticker and expiry.
    Calculates mid-price and filters for liquidity.
    """
    tk = yf.Ticker(ticker)
    chain = tk.option_chain(expiry)

    calls = chain.calls.copy()
    calls["type"] = "call"

    puts = chain.puts.copy()
    puts["type"] = "put"

    df = pd.concat([calls, puts], ignore_index=True)
    df["expiry"] = expiry

    # Calculate Mid Price
    df["mid"] = (df["bid"] + df["ask"]) / 2.0

    # Filter for non-zero bids to ensure some liquidity
    df = df[df["bid"] > 0]

    return df


def load_all_expiries(ticker, max_expiries=5):
    """
    Loads option chains for multiple expiries.
    """
    tk = yf.Ticker(ticker)
    frames = []

    expiries = tk.options[:max_expiries]
    for exp in expiries:
        frames.append(fetch_option_chain(ticker, exp))

    if not frames:
        return pd.DataFrame()

    return pd.concat(frames, ignore_index=True)
