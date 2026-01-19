import numpy as np 
from cleaning.arbitrage import butterfly_arbitrage
from volsurface.models.svi_calibration import calibrate_svi
from volsurface.models.sabr_calibration import calibrate_sabr
from volsurface.surface.surface_builder import VolSurface
from volsurface.validation.no_arbitrage import validate_surface


class VolSurface:
    def __init__(self, option_chain, model="svi"):
        self.option_chain = option_chain
        self.model = model
        self.surface = None

    def calibrate(self):
        if self.model == "svi":
            params = calibrate_svi_surface(self.option_chain)
        elif self.model == "sabr":
            params = calibrate_sabr_surface(self.option_chain)
        else:
            raise ValueError("Model must be 'svi' or 'sabr'")

        self.surface = VolSurfaceGrid(params, self.model)

    def iv(self, strike, maturity):
        return self.surface.iv(strike, maturity)

    def diagnostics(self):
        return surface_diagnostics(self.surface)


