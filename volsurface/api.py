import numpy as np
import pandas as pd
from typing import Union
from volsurface.core.surface import ParametricVolSurface
from volsurface.models.dupire import dupire_local_vol
from volsurface.calibration.svi_calibration import calibrate_svi
from volsurface.calibration.sabr_calibration import calibrate_sabr


class VolSurfaceAPI:
    """
    Main entry point for the library to build, calibrate, and query surfaces.
    """

    def __init__(self, data: pd.DataFrame, model: str = "svi", F: float = 100.0):
        self.data = data
        self.model = model
        self.F = F
        self.params = None
        self.surface_obj = None

    def calibrate(self):
        if self.model not in ["svi", "sabr"]:
            raise ValueError("Model must be 'svi' or 'sabr'")

        strikes = self.data["strike"].values
        maturities = self.data["time_to_maturity"].values
        vols = self.data["implied_vol"].values

        if self.model == "svi":
            self.params = calibrate_svi(self.F, strikes, maturities, vols)
        elif self.model == "sabr":
            self.params = calibrate_sabr(self.F, strikes, maturities, vols)

        self.surface_obj = ParametricVolSurface(self.model, self.params, self.F)

    def iv(self, K: Union[float, np.ndarray], T: Union[float, np.ndarray]):
        if self.surface_obj is None:
            raise ValueError("Model not fitted yet. Call calibrate() first.")
        return self.surface_obj.iv(K, T)

    def local_vol(self, K: float, T: float):
        if self.surface_obj is None:
            raise ValueError("Model not fitted yet. Call calibrate() first.")
        return dupire_local_vol(T, K, self.surface_obj, self.F)
