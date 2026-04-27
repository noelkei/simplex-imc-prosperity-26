# Processed Paper Summary: Binary/Digital Put Option (BSM)

## Status

`draft`

## Paper Metadata

- Paper ID: `binary_put_bsm_digital`
- Title: `Digital Options under Black-Scholes`
- Authors: Standard BSM result (Black, Scholes 1973; Reiner, Rubinstein 1991)
- Year: 1973 / 1991
- Link: https://doi.org/10.1086/260062

## Core Claim

A **binary put** (also called cash-or-nothing put or digital put) pays a fixed
amount Q if S_T < K at expiry, and zero otherwise. Under GBM (BSM framework),
the price is simply the discounted risk-neutral probability of ending below K:

```
Binary_Put(S, K, T, σ, r) = Q × e^{-rT} × Φ(-d₂)
where d₂ = [ln(S/K) + (r - σ²/2)T] / (σ√T)
```

At r=0:
```
Binary_Put = Q × Φ(-d₂)
where d₂ = [ln(S/K) - σ²T/2] / (σ√T)
```

This is also related to the vanilla put by:
```
∂P_BSM/∂K = e^{-rT} × Φ(-d₂) = Binary_Put / Q (per unit of payout)
```

The binary put is the "digital" version of the vanilla put — the payoff is
a step function instead of a ramp.

## Assumptions

- GBM for AETHER_CRYSTAL price process.
- σ = 251% annualized, 252 days/year, 4 steps/day.
- r = 0 (Prosperity convention).
- Payout Q is fixed (from problem statement).
- European exercise only (payment at expiry, not upon crossing K).

## Problem Addressed for Round 4

The manual challenge AETHER_CRYSTAL includes a **binary put** option.
The binary put pays Q if AETHER_CRYSTAL ends below strike K at the relevant date.

**Key differences from vanilla put**:
- Vanilla put: payoff = max(K - S_T, 0) → increasing in (K - S_T)
- Binary put: payoff = Q × 1{S_T < K} → fixed payout, discontinuous

**Pricing consideration**: the binary put payoff discontinuity makes it
sensitive to smile assumptions. Under flat vol (Bachelier/BS adequate for
our strikes), the BSM formula is exact.

**Vega note**: binary put has negative vega near the money (unlike vanilla put).
This is because higher vol WIDENS the distribution and makes the probability of
ending at exactly S_T < K less certain for ATM/NTM options.

## What This Paper Gives Us

- **Closed-form formula**: one line of Python, no numerical integration.
- **Relationship to vanilla put**: binary put = ∂P_vanilla/∂K / Q.
  This is a consistency check: if binary_put = Q × Φ(-d₂), then
  vanilla put = ∫_K^∞ binary_put(K') dK' (call-spread approximation).
- **Numerical sensitivity**: binary put value is sensitive to σ near-the-money.
  At σ=251% (high vol), the distribution is wide → Φ(-d₂) is closer to 0.5
  → binary puts on ATM options are worth approximately 0.5 × Q.

## Action Classification

`promote` — single-line closed-form formula. Directly implementable for the
manual challenge. No approximation needed.

## Implementation Notes

```python
import math
from statistics import NormalDist

_nd = NormalDist()

def binary_put(S, K, T, sigma, Q=1.0, r=0.0):
    """
    Cash-or-nothing binary put option price (BSM).
    Pays Q if S_T < K at expiry.
    """
    if T <= 0:
        return Q if S < K else 0.0
    vt = sigma * math.sqrt(T)
    d2 = (math.log(S / K) + (r - 0.5 * sigma**2) * T) / vt
    return Q * math.exp(-r * T) * _nd.cdf(-d2)

def binary_call(S, K, T, sigma, Q=1.0, r=0.0):
    """
    Cash-or-nothing binary call option price (BSM).
    Pays Q if S_T > K at expiry.
    """
    if T <= 0:
        return Q if S > K else 0.0
    vt = sigma * math.sqrt(T)
    d2 = (math.log(S / K) + (r - 0.5 * sigma**2) * T) / vt
    return Q * math.exp(-r * T) * _nd.cdf(d2)

# Example for AETHER_CRYSTAL manual challenge:
# S = current AETHER_CRYSTAL price
# K = strike from problem statement
# sigma = 2.51 (251% annualized)
# T = time to expiry in years
# Q = payout amount from problem statement
# price = binary_put(S, K, T, sigma, Q)
#
# Sanity checks:
# binary_put + binary_call = Q × e^{-rT}  (they're complementary)
# At S >> K: binary_put → 0 (very unlikely to finish below K)
# At S << K: binary_put → Q (almost certain to finish below K)
# At S = K (ATM), T→0: binary_put → Q/2 (50/50)

# Additional check via put-call relationship:
# binary_put(K) = -dP_vanilla/dK × Q  (digital ≈ slope of vanilla)
def binary_put_from_vanilla_slope(S, K, T, sigma, Q=1.0, r=0.0, eps=0.01):
    """Finite-difference verification of binary_put via vanilla put slope."""
    from math import exp
    def vanilla_put(k):
        vt = sigma * math.sqrt(T)
        d1 = (math.log(S/k) + (r + 0.5*sigma**2)*T) / vt
        d2 = d1 - vt
        return k * exp(-r*T) * _nd.cdf(-d2) - S * _nd.cdf(-d1)
    slope = (vanilla_put(K + eps) - vanilla_put(K - eps)) / (2 * eps)
    return Q * exp(-r*T) * (-slope)  # should match binary_put()
```

## Downstream Use

- Strategy: compute binary_put() for the manual challenge binary put instrument.
  Cross-check: binary_put + binary_call = Q (at r=0).
- Spec: use sigma=2.51 and r=0 as primary parameters. Match T to the specific
  expiry date given in the problem statement.
- Validation:
  - binary_put + binary_call = Q × e^{-rT} (complementary payoffs)
  - At S=K: binary_put ≈ 0.5 × Q (50/50 probability at-the-money)
  - Monte Carlo IS should agree within 1% for N=50,000 paths
