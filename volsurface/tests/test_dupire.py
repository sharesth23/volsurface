import numpy as np
from volsurface.models.dupire import dupire_local_vol


class DummySurface:
    def iv(self, K, T):
        # Flat vol surface
        return 0.2


def test_dupire_flat_vol():
    surface = DummySurface()

    # For a flat volatility surface, local vol should equal implied vol
    lv = dupire_local_vol(1.0, 100, surface, F=100)

    assert np.isclose(lv, 0.2, atol=1e-4)


def test_dupire_invalid_variance():
    class BadSurface:
        def iv(self, K, T):
            if T > 1.0:
                return 0.1  # Arbitrage! Vol drops fast causing negative variance
            return 0.5

    surface = BadSurface()

    lv = dupire_local_vol(1.0, 100, surface, F=100)

    assert np.isnan(lv)
