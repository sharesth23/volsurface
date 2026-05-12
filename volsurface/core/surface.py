from scipy.interpolate import SmoothBivariateSpline
from volsurface.models.svi import  svi_implied_vol
from volsurface.models.sabr import sabr_implied_vol
from volsurface.models.heston import heston_implied_vol

class VolSurface:
    def __init__(self, strikes, maturities, vols):
        self.spline = SmoothBivariateSpline(strikes, maturities, vols)

    def iv(self, K, T):
        return float(self.spline(K, T))

class ParametricVolSurface:
    def __init__(self, model_type, params, F=None):
        self.model_type = model_type
        self.params = params
        self.F = F

    def iv(self, K, T):
        if self.model_type == "svi":
            # For SVI, we assume params is a dict of parameters
            return svi_implied_vol(self.F, K, T, self.params)
        elif self.model_type == "sabr":
            # SABR params: alpha, beta, rho, nu
            return sabr_implied_vol(
                self.F, K, T,
                self.params['alpha'],
                self.params['beta'],
                self.params['rho'],
                self.params['nu']
            )
        elif self.model_type == "heston":
            # Heston params: v0, kappa, theta, sigma, rho
            return heston_implied_vol(
                self.F, K, T,
                self.params['v0'],
                self.params['kappa'],
                self.params['theta'],
                self.params['sigma'],
                self.params['rho']
            )
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
