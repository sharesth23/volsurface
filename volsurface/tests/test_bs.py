from volsurface.iv.black_scholes import bs_call_price

def test_bs_price_positive():
    price = bs_call_price(S=100, K=100, T=1, r=0.05, sigma=0.2)
    assert price > 0
