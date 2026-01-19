from iv.black_scholes import bs_call_price, implied_volatility

def test_bs_price_positive():
    price = bs_call_price(S=100, K=100, T=1, r=0.05, sigma=0.2)
    assert price > 0

def test_implied_vol_recovery():
    true_vol = 0.25
    price = bs_call_price(100, 100, 1, 0.01, true_vol)
    iv = implied_volatility(price, 100, 100, 1, 0.01)
    assert abs(iv - true_vol) < 1e-3
