from volsurface.api import VolSurfaceAPI
import matplotlib.pyplot as plt
import numpy as np

def run_real_data_example(ticker="SPY"):
    print(f"--- Fetching and Calibrating real data for {ticker} ---")

    try:
        # 1. Initialize API from Ticker
        api = VolSurfaceAPI.from_ticker(ticker, model="sabr", max_expiries=1)

        print(f"Estimated Forward Price: {api.F:.2f}")
        print(f"Data points fetched: {len(api.option_chain)}")

        # 2. Calibrate
        print("Calibrating SABR model...")
        api.calibrate()

        # 3. Predict and Visualize
        strikes = api.option_chain['strike'].values
        market_vols = api.option_chain['implied_vol'].values
        T = api.option_chain['time_to_maturity'].iloc[0]

        model_vols = [api.iv(K, T) for K in strikes]

        plt.figure(figsize=(10, 6))
        plt.scatter(strikes, market_vols, label="Market (OTM)", color='black', alpha=0.5)
        plt.plot(strikes, model_vols, label="SABR Fit", color='red', linewidth=2)
        plt.title(f"SABR Calibration for {ticker} (T={T:.4f})")
        plt.xlabel("Strike")
        plt.ylabel("Implied Volatility")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()

        print("Calibration successful.")

    except Exception as e:
        print(f"Error during real data calibration: {e}")
        print("Note: This might fail if the sandbox has restricted internet access or Yahoo Finance is unreachable.")

if __name__ == "__main__":
    run_real_data_example("SPY")
