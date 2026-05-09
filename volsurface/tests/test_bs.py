from volsurface.iv.black_scholes import bs_call_price

def test_bs_price_positive():
    price = bs_call_price(S=100, K=100, T=1, r=0.05, sigma=0.2)
    assert price > 0

def test_bs_price_edge_cases_t_zero():
    # T = 0, ITM
    assert bs_call_price(S=110, K=100, T=0, r=0.05, sigma=0.2) == 10
    # T = 0, OTM
    assert bs_call_price(S=90, K=100, T=0, r=0.05, sigma=0.2) == 0

def test_bs_price_edge_cases_t_negative():
    # T < 0, ITM
    assert bs_call_price(S=110, K=100, T=-1, r=0.05, sigma=0.2) == 10
    # T < 0, OTM
    assert bs_call_price(S=90, K=100, T=-1, r=0.05, sigma=0.2) == 0

def test_bs_price_edge_cases_sigma_zero():
    # sigma = 0, ITM
    assert bs_call_price(S=110, K=100, T=1, r=0.05, sigma=0) == 10
    # sigma = 0, OTM
    assert bs_call_price(S=90, K=100, T=1, r=0.05, sigma=0) == 0

def test_bs_price_edge_cases_sigma_negative():
    # sigma < 0, ITM
    assert bs_call_price(S=110, K=100, T=1, r=0.05, sigma=-0.1) == 10
    # sigma < 0, OTM
    assert bs_call_price(S=90, K=100, T=1, r=0.05, sigma=-0.1) == 0
