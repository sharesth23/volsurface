import pandas as pd
import numpy as np
from volsurface.arbitrage.correction import smooth_surface

def test_calendar_arbitrage_correction():
    # IV decreases while T increases -> total variance might decrease
    # T=0.5, IV=0.4 -> w = 0.4^2 * 0.5 = 0.08
    # T=1.0, IV=0.2 -> w = 0.2^2 * 1.0 = 0.04 (Violation!)

    df = pd.DataFrame({
        "strike": [100, 100],
        "time_to_maturity": [0.5, 1.0],
        "implied_vol": [0.4, 0.2]
    })

    corrected_df = smooth_surface(df)

    # After correction, w[1.0] should be >= w[0.5]
    # w[0.5] = 0.08
    # w[1.0] becomes 0.08, so corrected_IV = sqrt(0.08 / 1.0) = 0.2828

    new_vols = corrected_df["implied_vol"].values
    assert new_vols[1] > 0.2
    assert abs(new_vols[1]**2 * 1.0 - 0.4**2 * 0.5) < 1e-7
