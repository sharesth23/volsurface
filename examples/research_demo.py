import numpy as np
import pandas as pd
from volsurface.api import VolSurfaceAPI
from volsurface.core.benchmark import run_benchmark
from volsurface.visualization.smile_plot import plot_smile_comparison
import matplotlib.pyplot as plt

# 1. Generate Mock Data (Research Grade)
F = 100.0
strikes = np.array([80, 85, 90, 95, 100, 105, 110, 115, 120])
T = 1.0
maturities = np.full_like(strikes, T)
# Typical equity smile
market_vols = np.array([0.35, 0.32, 0.29, 0.27, 0.25, 0.26, 0.28, 0.31, 0.34])

df = pd.DataFrame({
    "strike": strikes,
    "time_to_maturity": maturities,
    "implied_vol": market_vols
})

print("--- VolSurface Calibration Example ---")
# 2. Calibrate SVI
api_svi = VolSurfaceAPI(df, model="svi", F=F)
api_svi.calibrate()
svi_vols = [api_svi.iv(K, T) for K in strikes]

# 3. Calibrate SABR
api_sabr = VolSurfaceAPI(df, model="sabr", F=F)
api_sabr.calibrate()
sabr_vols = [api_sabr.iv(K, T) for K in strikes]

# 4. Run Benchmark
print("\nRunning Model Benchmark...")
bench_results = run_benchmark(F, strikes, maturities, market_vols)
print(f"SVI RMSE: {bench_results['SVI']['rmse']:.6f}")
print(f"SABR RMSE: {bench_results['SABR']['rmse']:.6f}")

# 5. Visualization
print("\nGenerating Comparison Plot...")
model_comparison = {
    'SVI Model': svi_vols,
    'SABR Model': sabr_vols
}
fig = plot_smile_comparison(strikes, market_vols, model_comparison, T)
plt.show()

print("\nExample completed successfully.")
