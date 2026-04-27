# Processed Paper Summary: Rubinstein (1991) — Chooser Options

## Status

`draft`

## Paper Metadata

- Paper ID: `rubinstein_1991_chooser_options`
- Title: `Pay Now, Choose Later`
- Authors: Mark Rubinstein
- Year: 1991
- Link: https://www.risk.net/derivatives/1520301/pay-now-choose-later

## Core Claim

A **chooser option** (also called "as-you-like-it option") gives the holder the
right to choose at time t_c whether the option becomes a call or a put, with
common strike K and maturity T > t_c. Under GBM, it has a closed-form price.

**Key identity**: a chooser is equivalent to a call plus a put with a shorter maturity:
```
Chooser(S, K, t_c, T) = Call(S, K, T) + Put(S, K × e^{-r(T-t_c)}, t_c)
```

This decomposition makes the chooser tractable because it reduces to two vanilla options.

**BSM Chooser Price** (with r = 0 for simplicity):
```
C_chooser = S × Φ(d₁) - K × Φ(d₂) + K × Φ(-d₂') - S × Φ(-d₁')
where:
d₁  = [ln(S/K) + ½σ²T] / (σ√T)
d₂  = d₁ - σ√T
d₁' = [ln(S/K) + ½σ²t_c] / (σ√t_c)
d₂' = d₁' - σ√t_c
```

## Assumptions

- GBM (geometric Brownian motion) for AETHER_CRYSTAL price process.
- σ = 251% annualized, 252 days/year, 4 steps per day.
- Risk-free rate r ≈ 0 (Prosperity has no discounting).
- The chooser choice date t_c must be specified (problem statement dependent).

## Problem Addressed for Round 4

The manual challenge AETHER_CRYSTAL includes exotic option pricing.
One of the instruments is a **chooser option** on AETHER_CRYSTAL.

**From EDA analysis:**
- AETHER_CRYSTAL GBM parameters: μ=0, σ=251%, T=total game duration, dt=1/1008
  (4 steps/day × 252 days/year)
- The chooser at choice date t_c gives us an option on whether to hold a call or put.
- Wrong pricing = wrong manual P&L.

## What This Paper Gives Us

- **Closed-form formula**: implementable in pure Python, no scipy needed.
- **Decomposition**: Chooser = Call(K, T) + Put(K × e^{-r(T-t_c)}, t_c)
  This is THE key result — reduces to two BSM options.
- **Put-Call symmetry**: at r=0 and T=t_c (symmetric chooser):
  `Chooser = Call + Put = straddle`
  This is a quick sanity check: chooser ≥ straddle when t_c < T.

## AETHER_CRYSTAL Pricing Parameters

From the Round 4 manual challenge specification:
```
S₀ = AETHER_CRYSTAL initial price (from market data)
K  = strike (from problem statement)
σ  = 251% annualized = 251/100 = 2.51
T  = total time to expiry (in years)
t_c = chooser decision date (in years, given in problem)
r  = 0 (Prosperity convention)
dt = 1 / (252 × 4) = 1/1008 per step
```

## Action Classification

`promote` — closed-form chooser price is directly implementable in Python
stdlib. This should be computed precisely for the manual challenge.

## Implementation Notes

```python
import math
from statistics import NormalDist

_nd = NormalDist()

def bsm_call(S, K, T, sigma, r=0.0):
    """Black-Scholes call price (r=0 default for Prosperity)."""
    if T <= 0:
        return max(S - K, 0.0)
    vt = sigma * math.sqrt(T)
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / vt
    d2 = d1 - vt
    return S * _nd.cdf(d1) - K * math.exp(-r * T) * _nd.cdf(d2)

def bsm_put(S, K, T, sigma, r=0.0):
    """Black-Scholes put price (r=0 default for Prosperity)."""
    if T <= 0:
        return max(K - S, 0.0)
    vt = sigma * math.sqrt(T)
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / vt
    d2 = d1 - vt
    return K * math.exp(-r * T) * _nd.cdf(-d2) - S * _nd.cdf(-d1)

def chooser_option(S, K, tc, T, sigma, r=0.0):
    """
    Rubinstein (1991) chooser option price.
    Chooser = Call(K, T) + Put(K × exp(-r(T-tc)), tc)
    At r=0: Chooser = Call(K, T) + Put(K, tc)
    """
    call_part = bsm_call(S, K, T, sigma, r)
    k_star = K * math.exp(-r * (T - tc))  # adjusted strike for put part
    put_part = bsm_put(S, k_star, tc, sigma, r)
    return call_part + put_part

# Example usage for AETHER_CRYSTAL:
# S = 100 (hypothetical initial price)
# K = 100 (ATM strike)
# sigma = 2.51 (251% annualized)
# T = 4/252 (4 days to expiry at 252 days/yr — adjust per problem)
# tc = 2/252 (chooser date = 2 days from now)
# price = chooser_option(S, K, tc, T, sigma)
#
# Sanity check: at tc = T → chooser = straddle = call + put
# At tc → 0: chooser → call (choice is meaningless immediately)
```

## Downstream Use

- Strategy: compute chooser_option() once per manual challenge configuration.
  Cross-check against Monte Carlo IS results from the EDA analysis script.
- Spec: the closed-form value is the PRIMARY answer for the manual challenge.
  If Monte Carlo and closed-form disagree by >1%, check parameter inputs.
- Validation: at tc=T (simultaneous choice and expiry): price = straddle price.
  At tc=0: price ≈ call price. These are the boundary conditions to verify.
