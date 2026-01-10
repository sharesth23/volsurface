# VolSurface

![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![CI](https://github.com/sharesth23/arbitragelab-volsurface/actions/workflows/ci.yml/badge.svg)
![GSoC](https://img.shields.io/badge/GSoC-ready-orange.svg)
![Quant](https://img.shields.io/badge/domain-Quant%20Finance-purple.svg)

**VolSurface** is an open-source, research-grade Python library for constructing  
**arbitrage-aware implied volatility surfaces** from noisy real-world option data.

The project is intentionally designed as a **Google Summer of Code (GSoC)–level contribution**, combining
**academic volatility modeling**, **robust numerical methods**, and **open-source engineering best practices**.

---

## 🎯 GSoC Motivation & Problem Statement

Implied volatility surfaces are a central object in:

- derivatives pricing
- volatility trading
- portfolio risk management

Yet real option chain data is **noisy, sparse, and often violates economic consistency**.
Most student projects stop at plotting volatility smiles — this project focuses on:

> **Correctness, robustness, and research reproducibility.**

### Project Goal
Build an **extensible open-source framework** that:
- calibrates industry-standard volatility models,
- benchmarks competing parameterizations,
- produces diagnostics used by professional derivatives desks,
- and supports reproducible academic analysis.

---

## ✨ Key Features

- ✅ Black–Scholes implied volatility engine  
- ✅ **SABR model** with constrained calibration  
- ✅ **SVI model** (total variance parameterization)  
- ✅ **Benchmark framework** (SABR vs SVI using RMSE)  
- ✅ Diagnostic plots (smiles & model errors)  
- ✅ Modular **pip-installable** package structure  
- ✅ Research paper (LaTeX) included  

---

## 📦 Installation

```bash
git clone https://github.com/sharesth23/arbitragelab-volsurface.git
cd volsurface
pip install -e .
