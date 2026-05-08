import pandas as pd
import numpy as np
from volsurface.data.cleaning import filter_otm_options, estimate_forward_price

def test_otm_filtering():
    F = 100.0
    df = pd.DataFrame({
        "strike": [90, 110, 90, 110],
        "type": ["call", "call", "put", "put"],
        "mid": [12, 2, 2, 12]
    })

    # OTM: call strike >= 100, put strike < 100
    otm_df = filter_otm_options(df, F)

    assert len(otm_df) == 2
    assert "call" in otm_df[otm_df["strike"] == 110]["type"].values
    assert "put" in otm_df[otm_df["strike"] == 90]["type"].values

def test_forward_price_estimation():
    # C - P = F - K  => F = C - P + K
    # K=100, C=5, P=4 => F = 5 - 4 + 100 = 101
    df = pd.DataFrame({
        "strike": [100, 100],
        "type": ["call", "put"],
        "mid": [5, 4],
        "expiry": ["2025-12-31", "2025-12-31"]
    })

    F_est = estimate_forward_price(df)
    assert abs(F_est - 101.0) < 1e-7
