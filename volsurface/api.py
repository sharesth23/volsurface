import numpy as np 
from volsurface.arbitrage.detection import butterfly_arbitrage, calendar_arbitrage
from volsurface.calibration.svi_calibration import calibrate_svi
from volsurface.calibration.sabr_calibration import calibrate_sabr
from volsurface.core.surface import VolSurface, ParametricVolSurface
from volsurface.validation.no_arbitrage import validate_surface

class VolSurfaceAPI:
    def __init__(self, option_chain, model="svi", F=None):
        """
        option_chain: pd.DataFrame with columns ['strike', 'time_to_maturity', 'implied_vol']
        model: 'svi' or 'sabr'
        F: Forward price. If None, it might be estimated or required.
        """
        self.option_chain = option_chain
        self.model = model
        self.F = F
        self.surface = None

    def calibrate(self):
        strikes = self.option_chain['strike'].values
        maturities = self.option_chain['time_to_maturity'].values
        vols = self.option_chain['implied_vol'].values

        if self.F is None:
            # Simple heuristic if F is not provided: use ATM strike if possible or mean
            self.F = np.mean(strikes)

        if self.model == "svi":
            # calibrate_svi(F, strikes, T, vols)
            # SVI is usually calibrated per slice, but here we might be doing a simplistic fit
            # For a real library, we'd handle multiple expiries.
            # Assuming a single expiry for now as per the current calibrate_svi signature
            T = maturities[0]
            params = calibrate_svi(self.F, strikes, T, vols)
            self.surface = ParametricVolSurface("svi", params, F=self.F)

        elif self.model == "sabr":
            # calibrate_sabr(F, strikes, maturities, market_vols, beta=0.5)
            params = calibrate_sabr(self.F, strikes, maturities, vols)
            self.surface = ParametricVolSurface("sabr", params, F=self.F)
        else:
            raise ValueError("Model must be 'svi' or 'sabr'")

    def iv(self, strike, maturity):
        if self.surface is None:
            raise ValueError("Surface not calibrated. Call calibrate() first.")
        return self.surface.iv(strike, maturity)

    def diagnostics(self):
        return validate_surface(self.option_chain)
