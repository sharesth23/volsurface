from volsurface.arbitrage.detection import calendar_arbitrage, butterfly_arbitrage


def validate_surface(df):
    return {
        "calendar_violations": calendar_arbitrage(df),
        "butterfly_violations": butterfly_arbitrage(df),
    }
