# 📈 volsurface

![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![GSoC](https://img.shields.io/badge/GSoC-ready-orange.svg)
![Quant](https://img.shields.io/badge/domain-Quant%20Finance-purple.svg)

![Stars](https://img.shields.io/github/stars/sharesth23/volsurface?style=social)
![Forks](https://img.shields.io/github/forks/sharesth23/volsurface?style=social)
![Issues](https://img.shields.io/github/issues/sharesth23/volsurface)
![Pull Requests](https://img.shields.io/github/issues-pr/sharesth23/volsurface)
![Last Commit](https://img.shields.io/github/last-commit/sharesth23/volsurface)

---

**volsurface** is an open-source, research-grade Python library for constructing  
**arbitrage-aware implied volatility surfaces** from noisy real-world option data.

The project is intentionally designed as a **Google Summer of Code (GSoC)–level open-source contribution**, combining:

- academic volatility modeling  
- robust numerical calibration  
- modern Python packaging, testing, and CI practices  

---

## 🎯 Project Motivation (GSoC Context)

Implied volatility surfaces are a core object in:

- derivatives pricing  
- volatility trading strategies  
- portfolio and systemic risk analysis  

However, **raw option chain data is noisy, sparse, and frequently violates economic consistency**.  
Many student projects stop at plotting volatility smiles.

This repository instead focuses on:

> **Correctness, robustness, benchmarking, and reproducible research.**

The goal is to build a **community-usable open-source framework** that mirrors how volatility
surfaces are handled in **professional derivatives research and risk systems**.

---

## ✨ Key Features

- ✅ Black–Scholes implied volatility engine  
- ✅ **SABR volatility model** with constrained calibration  
- ✅ **SVI volatility model** (total variance parameterization)  
- ✅ **Benchmark framework** (SABR vs SVI using RMSE)  
- ✅ Diagnostic plots (smiles & model errors)  
- ✅ Modular **pip-installable** package  
- ✅ Research paper (LaTeX) included  

---
## 🗂️ Repository Structure

```
volsurface/
├── cleaning/
│   └── arbitrage.py          # Arbitrage detection and data cleaning
├── data/
│   └── fetch_yahoo.py        # Market data fetching (Yahoo Finance, etc.)
├── experiments/
│   └── earnings_event.py     # Research experiments (earnings events, etc.)
├── iv/
│   └── black_scholes.py      # Black-Scholes implied volatility calculations
├── models/
│   ├── sabr.py               # SABR volatility model
│   ├── sabr_calibration.py   # SABR model calibration
│   ├── svi.py                # SVI volatility model
│   └── svi_calibration.py    # SVI model calibration
├── paper/
│   └── iv_surface.tex        # LaTeX research paper
├── surface/
│   └── surface_builder.py    # Volatility surface construction
├── tests/
│   ├── test_arbitrage.py     # Arbitrage detection tests
│   ├── test_bs.py            # Black-Scholes tests
│   └── test_sabr.py          # SABR model tests
├── validation/
│   └── no_arbitrage.py       # No-arbitrage validation
└── visualization/
    ├── smile_plot.py         # Volatility smile plotting
    └── surface_plot.py       # Volatility surface plotting
```

---
## 📊 Benchmarking: SABR vs SVI
  The library includes a dedicated benchmark pipeline to compare model performance quantitatively.
```python code 
from volsurface.benchmark.benchmark_runner import run_benchmark
from volsurface.visualization.smile import plot_smile

F = 100
T = 1.0
strikes = [80, 90, 100, 110, 120]
market_vols = [0.35, 0.30, 0.25, 0.27, 0.32]

results = run_benchmark(F, strikes, T, market_vols)

plot_smile(
    strikes,
    market_vols,
    results["SABR_VOL"],
    results["SVI_VOL"]
)

print("SABR RMSE:", results["SABR_RMSE"])
print("SVI RMSE:", results["SVI_RMSE"])

```


---

## INSTALLATION

```bash
git clone https://github.com/sharesth23/volsurface.git
cd volsurface
pip install -e .

---




