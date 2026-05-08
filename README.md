# 📈 volsurface

![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Build Status](https://github.com/sharesth23/volsurface/actions/workflows/python-tests.yml/badge.svg)
![Quant](https://img.shields.io/badge/domain-Quant%20Finance-purple.svg)

**volsurface** is a research-grade Python library for constructing arbitrage-aware implied volatility surfaces. It provides professional tools for parametric model calibration (SVI, SABR), static arbitrage detection, and smoothing.

---

## ✨ Key Features
- 📊 **Parametric Models**: Full implementation of SABR (Hagan et al.) and SVI (Gatheral) models.
- 🧮 **Arbitrage Analytics**: Detect and correct calendar and butterfly arbitrage violations.
- 📉 **Benchmarking**: Built-in pipeline to compare model performance (RMSE, MAE).
- 🔍 **Numerical Robustness**: Stable calibration using L-BFGS-B and constrained optimization.
- 📈 **Visualizations**: 3D surface plots, contour maps, and smile comparisons.

---

## 🚀 Quick Start

```python
import pandas as pd
from volsurface.api import VolSurfaceAPI

# Prepare your data
df = pd.DataFrame({
    "strike": [90, 100, 110],
    "time_to_maturity": [1.0, 1.0, 1.0],
    "implied_vol": [0.3, 0.25, 0.28]
})

# Initialize and calibrate
api = VolSurfaceAPI(df, model="svi", F=100.0)
api.calibrate()

# Get implied volatility for any strike/maturity
vol = api.iv(strike=105, maturity=1.0)
print(f"Implied Vol: {vol:.4f}")
```

---

## 🗂️ Project Structure

```
volsurface/
├── volsurface/
│   ├── core/           # Main API and Benchmarking
│   ├── models/         # SVI, SABR, Black-Scholes
│   ├── calibration/    # Optimization logic
│   ├── arbitrage/      # Detection and Correction
│   ├── visualization/  # Plotting tools
│   └── data/           # Data loaders (Yahoo Finance)
├── examples/           # Research demos
├── docs/               # Theoretical background
├── tests/              # Comprehensive test suite
└── paper/              # LaTeX research paper
```

---

## 📚 Documentation & Research
For a deep dive into the underlying mathematics, check out:
- [Theory and Methodology](docs/theory.md)
- [Research Paper (LaTeX)](volsurface/paper/iv_surface.tex)

---

## 🛠️ Installation
```bash
git clone https://github.com/sharesth23/volsurface.git
cd volsurface
pip install -e .
```

---

## 🤝 Contributing
Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License
This project is licensed under the MIT License.
