import yfinance as yf
import pandas as pd

def fetch_option_chain(ticker, expiry):
    tk = yf.Ticker(ticker)
    chain = tk.option_chain(expiry)

    calls = chain.calls.copy()
    calls["type"] = "call"
    calls["expiry"] = expiry

    return calls


def load_all_expiries(ticker):
    tk = yf.Ticker(ticker)
    frames = []

    for exp in tk.options:
        frames.append(fetch_option_chain(ticker, exp))

    return pd.concat(frames, ignore_index=True)