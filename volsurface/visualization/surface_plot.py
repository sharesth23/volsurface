import numpy as np
import matplotlib.pyplot as plt

def plot_surface(surface, strike_range, maturity_range):
    K, T = np.meshgrid(strike_range, maturity_range)
    Z = np.vectorize(surface.iv)(K, T)

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(K, T, Z, cmap="viridis", edgecolor='none', alpha=0.8)

    ax.set_xlabel("Strike")
    ax.set_ylabel("Maturity")
    ax.set_zlabel("Implied Volatility")
    ax.set_title("Implied Volatility Surface")
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)

    return fig

def plot_contour(surface, strike_range, maturity_range):
    K, T = np.meshgrid(strike_range, maturity_range)
    Z = np.vectorize(surface.iv)(K, T)

    fig, ax = plt.subplots(figsize=(10, 8))
    cp = ax.contourf(K, T, Z, cmap="viridis")
    fig.colorbar(cp)

    ax.set_xlabel("Strike")
    ax.set_ylabel("Maturity")
    ax.set_title("Implied Volatility Contour")

    return fig
