import numpy as np
from scipy.interpolate import SmoothBivariateSpline

class VolSurface:
    def __init__(self, strikes, maturities, vols):
        self.model = SmoothBivariateSpline(strikes, maturities, vols)

    def iv(self, K, T):
        return float(self.model(K, T))