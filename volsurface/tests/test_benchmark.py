import numpy as np
from volsurface.core.benchmark import run_benchmark

def test_benchmark_runner():
    F = 100.0
    strikes = np.array([90, 100, 110])
    maturities = np.array([1.0, 1.0, 1.0])
    market_vols = np.array([0.3, 0.25, 0.28])

    results = run_benchmark(F, strikes, maturities, market_vols)

    assert 'SABR' in results
    assert 'SVI' in results
    assert 'Spline' in results
    assert results['SABR']['rmse'] >= 0
    assert results['SVI']['rmse'] >= 0
