import pandas as pd
from cleaning.arbitrage import calendar_arbitrage

def test_calendar_arbitrage_detection():
    df = pd.DataFrame({
        "strike": [100, 100],
        "time_to_maturity": [0.5, 1.0],
        "implied_vol": [0.3, 0.25]
    })
    violations = calendar_arbitrage(df)
    assert 100 in violations
