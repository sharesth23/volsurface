import matplotlib.pyplot as plt


def plot_smile(strikes, vols, maturity):
    fig = plt.figure(figsize=(10,6))
    plt.plot(strikes, vols, label=f"Maturity: {maturity}")
    plt.xlabel("Strike")
    plt.ylabel("Implied Volatility")
    plt.title(f"Implied Volatility Smile for Maturity: {maturity}")
    plt.legend()
    plt.grid(True)
    
    return fig


