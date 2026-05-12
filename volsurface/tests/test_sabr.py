from volsurface.models.sabr import sabr_implied_vol


def test_sabr_positive_vol():
    vol = sabr_implied_vol(F=100, K=100, T=1, alpha=0.3, beta=0.5, rho=-0.2, nu=0.4)
    assert vol > 0
