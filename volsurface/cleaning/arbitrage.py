import pandas as pd 
import numpy as np 

def calendar_arbitrage_check(df: pd.Dataframe):
    df = df.copy()
    df = df.sort_values(["strikes", "times_to_maturity"])
    violations = []

    for strike , grp in df.groupby ("strike")
      T = grp["time_to_maturity"].values 
      iv = grp["implied_vol"].values 
      