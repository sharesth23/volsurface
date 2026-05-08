import numpy as np
import pytest
from volsurface.models.dupire import dupire_local_vol

class DummySurface:
    def __init__(self, vol=0.20):
        self.vol = vol

    def iv(self, K, T):
        return self.vol

def test_dupire_flat_surface():
    surface = DummySurface(vol=0.20)

    # For a flat implied volatility surface, local volatility should equal implied volatility
    loc_vol = dupire_local_vol(T=1.0, K=100.0, surface=surface, F=100.0)

    assert not np.isnan(loc_vol)
    assert np.isclose(loc_vol, 0.20, atol=1e-4)

def test_dupire_arbitrage_surface():
    # A dummy surface that creates arbitrage (negative variance derivative)
    class ArbitrageSurface:
        def iv(self, K, T):
            if T > 1.0:
                return 0.10 # Variance drops drastically
            return 0.50

    surface = ArbitrageSurface()
    loc_vol = dupire_local_vol(T=1.0, K=100.0, surface=surface, F=100.0)

    # Negative variance derivative should result in NaN
    assert np.isnan(loc_vol)
