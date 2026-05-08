import matplotlib.pyplot as plt
import numpy as np

def plot_smile_comparison(strikes, market_vols, model_vols_dict, maturity):
    """
    Plots market vols vs multiple model vols for a given maturity.
    model_vols_dict: {'ModelName': [vols]}
    """
    fig = plt.figure(figsize=(10,6))
    plt.scatter(strikes, market_vols, color='black', label='Market Data', zorder=5)

    for model_name, vols in model_vols_dict.items():
        plt.plot(strikes, vols, label=model_name)

    plt.xlabel("Strike")
    plt.ylabel("Implied Volatility")
    plt.title(f"Implied Volatility Smile Comparison (T={maturity})")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    return fig
