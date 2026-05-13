import os
import sys
# Add parent directory to path to allow running as a script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import numpy as np
import pandas as pd
from datetime import datetime
import yfinance as yf
from volsurface.data.fetch_yahoo import load_all_expiries
from volsurface.api import VolSurfaceAPI

def main():
    ticker = "SPY"
    print(f"Fetching real-world option data for {ticker} using yfinance...")

    # 1. Fetch Option Data
    try:
        # Load up to 3 expiries to save time
        tk = yf.Ticker(ticker)
        expiries = tk.options[:3]
        if not expiries:
            print("No options data found.")
            return

        print(f"Found expiries: {expiries}")

        frames = []
        for exp in expiries:
            chain = tk.option_chain(exp)
            calls = chain.calls.copy()
            calls["expiry"] = exp
            frames.append(calls)

        df = pd.concat(frames, ignore_index=True)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    # Clean the data
    df = df.dropna(subset=['impliedVolatility'])
    df = df[df['impliedVolatility'] > 0.0]

    # Calculate time to maturity in years
    today = datetime.now()
    df['expiry_date'] = pd.to_datetime(df['expiry'])
    df['time_to_maturity'] = (df['expiry_date'] - today).dt.days / 365.25
    df = df[df['time_to_maturity'] > 0] # strictly positive

    print(f"Loaded {len(df)} options contracts.")

    # Format the dataframe for the API
    df = df.rename(columns={'strike': 'strike', 'impliedVolatility': 'implied_vol'})

    # 2. Fetch Spot Price (Forward price proxy for demo)
    try:
        hist = tk.history(period="1d")
        spot = hist['Close'].iloc[-1]
    except:
        spot = 500.0 # fallback

    print(f"Current {ticker} Spot Price: {spot}")

    # 3. Fit a Volatility Surface
    print("\n--- Calibrating SVI Volatility Surface ---")
    api = VolSurfaceAPI(df, model="svi", F=spot)
    try:
        api.calibrate()
        print(f"Calibration successful! SVI Params: {api.params}")

        # 4. Query the Surface
        sample_strike = spot * 1.05 # 5% OTM
        sample_ttm = 0.5 # 6 months

        iv = api.iv(sample_strike, sample_ttm)
        print(f"Calculated SVI Implied Vol for Strike {sample_strike:.2f}, TTM {sample_ttm:.2f}: {iv:.4f}")

    except Exception as e:
        print(f"Error during calibration: {e}")

if __name__ == "__main__":
    main()
