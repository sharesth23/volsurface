# Theory and Methodology

## 1. Implied Volatility Modeling

### SABR Model
The Stochastic Alpha-Beta-Rho (SABR) model is a stochastic volatility model used to describe the volatility smile in interest rate and equity markets.

**Dynamics:**
- $dF_t = \alpha_t F_t^\beta dW_t^1$
- $d\alpha_t = \nu \alpha_t dW_t^2$
- $E[dW_t^1 dW_t^2] = \rho dt$

### SVI Model
The Stochastic Volatility Inspired (SVI) model is a popular parameterization for the equity volatility smile.

**Formula:**
$w(k) = a + b (\rho(k-m) + \sqrt{(k-m)^2 + \sigma^2})$

where $k$ is the log-strike.

## 2. Static Arbitrage Detection

### Calendar Arbitrage
Calendar arbitrage occurs if the total variance $w = \sigma^2 T$ decreases with time $T$ for a fixed strike $K$.
Condition for no arbitrage: $\frac{\partial w}{\partial T} \geq 0$.

### Butterfly Arbitrage
Butterfly arbitrage occurs if the risk-neutral density is negative. This is equivalent to the call price surface not being convex in strike.
Condition for no arbitrage: $\frac{\partial^2 C}{\partial K^2} \geq 0$.

## 3. Calibration Process

We use non-linear least squares optimization (L-BFGS-B) to fit model parameters to observed market data. The objective function is the Mean Squared Error (MSE) between market and model implied volatilities.
