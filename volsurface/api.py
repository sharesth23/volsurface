import numpy as np 
import pandas as pd
from volsurface.arbitrage.detection import butterfly_arbitrage, calendar_arbitrage
from volsurface.calibration.svi_calibration import calibrate_svi
from volsurface.calibration.sabr_calibration import calibrate_sabr
from volsurface.core.surface import VolSurface, ParametricVolSurface
from volsurface.validation.no_arbitrage import validate_surface
from volsurface.data.fetch_yahoo import load_all_expiries
from volsurface.data.cleaning import filter_otm_options, estimate_forward_price

class VolSurfaceAPI:
    def __init__(self, option_chain, model="svi", F=None):
        """
        option_chain: pd.DataFrame with columns ['strike', 'time_to_maturity', 'implied_vol']
        model: 'svi' or 'sabr'
        F: Forward price.
        """
        self.option_chain = option_chain
        self.model = model
        self.F = F
        self.surface = None

    @classmethod
    def from_ticker(cls, ticker, model="svi", max_expiries=3):
        """
        Factory method to create an API instance from a Yahoo Finance ticker.
        """
        raw_data = load_all_expiries(ticker, max_expiries=max_expiries)
        if raw_data.empty:
            raise ValueError(f"No data found for ticker {ticker}")

        # Estimate Forward Price if possible
        F_est = estimate_forward_price(raw_data)

        # Preprocess: calculate TTM and filter OTM
        current_date = pd.Timestamp.now()
        raw_data['time_to_maturity'] = (
            pd.to_datetime(raw_data['expiry']) - current_date
        ).dt.days / 365.0

        # Ensure we have impliedVolatility (yfinance provides it)
        if 'impliedVolatility' in raw_data.columns:
            raw_data = raw_data.rename(columns={'impliedVolatility': 'implied_vol'})

        clean_data = filter_otm_options(raw_data, F_est)
        clean_data = clean_data.dropna(subset=['implied_vol'])

        return cls(clean_data, model=model, F=F_est)

    def calibrate(self):
        strikes = self.option_chain['strike'].values
        maturities = self.option_chain['time_to_maturity'].values
        vols = self.option_chain['implied_vol'].values

        if self.F is None:
            self.F = np.mean(strikes)

        if self.model == "svi":
            # For simplicity, we fit the first maturity slice
            T = maturities[0]
            mask = maturities == T
            params = calibrate_svi(self.F, strikes[mask], T, vols[mask])
            self.surface = ParametricVolSurface("svi", params, F=self.F)

        elif self.model == "sabr":
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
