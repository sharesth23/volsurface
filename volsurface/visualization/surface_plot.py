import numpy as np
import matplotlib.pyplot as plt


def plot_surface(surface, strike_range, maturity_range):
    K, T = np.meshgrid(strike_range, maturity_range)
    Z = np.vectorize(surface.iv)(K, T)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(K, T, Z, cmap="viridis")

    ax.set_xlabel("Strike")
    ax.set_ylabel("Maturity")
    ax.set_zlabel("Implied Volatility")
    plt.show()
