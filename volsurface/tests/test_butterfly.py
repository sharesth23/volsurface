import pandas as pd
from volsurface.arbitrage.detection import butterfly_arbitrage

def test_butterfly_arbitrage_detection():
    # Example where butterfly arbitrage exists (non-convex call prices)
    # Price = [10, 8, 7] for strikes [90, 100, 110] -> convex (OK)
    # Price = [10, 9, 7] for strikes [90, 100, 110] -> non-convex (Violation)
    # Price = C(K). We want C(100) <= 0.5 * C(90) + 0.5 * C(110) = 0.5*10 + 0.5*7 = 8.5
    # If C(100) = 9, then 9 > 8.5, violation.

    # We need to provide IVs that result in these prices.
    # For simplicity, let's just test the logic with a mock that bypasses BS if possible,
    # but the current implementation uses bs_call_price.

    # S=100, T=1, r=0
    # K=90, sigma=0.2 -> price ~ 13.3
    # K=100, sigma=0.5 -> price ~ 19.7
    # K=110, sigma=0.2 -> price ~ 4.4

    # (13.3 + 4.4) / 2 = 8.85. 19.7 > 8.85, so this should be a violation.

    df = pd.DataFrame({
        "strike": [90, 100, 110],
        "time_to_maturity": [1.0, 1.0, 1.0],
        "implied_vol": [0.2, 0.5, 0.2]
    })

    violations = butterfly_arbitrage(df, S=100.0, r=0.0)
    assert len(violations) > 0
    assert violations[0] == (1.0, 100)
