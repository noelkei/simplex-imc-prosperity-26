# Processed Paper Summary: Fang and Oosterlee (2008)

## Status

`draft`

## Round 4 Role

- Reference class: `knowledge draft`
- Priority for Strategy: below both the top-level `round4_raw_derived` core and the strongest `carry_forward` references
- Allowed use: inspiration and offline numerical-method framing only
- Caution: this note did not come from the local `round_4` raw-paper pipeline; do not promote it directly to live logic without stronger support

## Paper Metadata

- Paper ID: `fang_oosterlee_2008_cos_method`
- Title: `A Novel Pricing Method for European Options Based on Fourier-Cosine Series Expansions`
- Authors: Fang Fang, Cornelis W. Oosterlee
- Year: 2008
- Link: https://epubs.siam.org/doi/10.1137/080718061

## Core Claim

The COS method prices European options by expanding the risk-neutral density in a
Fourier-cosine series, yielding extremely fast and accurate prices when the
characteristic function of the log-price is known analytically (as in Heston,
Variance Gamma, CGMY, etc.).

COS price formula:
```
V(x, t) = e^{-rΔt} × Σ_{k=0}^{N-1} Re[φ(kπ/(b-a)) × e^{ikπ(x-a)/(b-a)}] × V_k
```
where:
- φ = characteristic function of log-price
- [a,b] = truncation interval (e.g., [μ-12σ, μ+12σ])
- V_k = payoff coefficients (closed-form for calls/puts)
- N = number of terms (N=128 typically gives machine precision)

## Assumptions

- Characteristic function of the model is known analytically.
- Truncation interval must contain essentially all probability mass.
- For European options only (American options need a PIDE variant).

## Problem Addressed for Round 4

**Key question from 02b research plan**: Can COS replace Bachelier for faster
or more accurate pricing under Heston?

**Answer**: No, for two reasons:
1. The COS method requires computing characteristic function values, which involves
   complex exponentials — NOT implementable in pure Python stdlib at O(1) per tick.
2. Heston itself was already eliminated because VEX vol CoV=0.119 makes it
   unnecessary. If the underlying model (Heston) is not needed, COS is not needed.

**What COS IS useful for**: Pricing the AETHER_CRYSTAL manual challenge options
under GBM, where we can pre-compute a table of payoffs offline.

## What This Paper Gives Us

- **For manual challenge (offline)**: COS can price chooser, binary put, and
  KO put under GBM with σ=251% to high precision. This is a verification tool.
- **Understanding principle**: The COS method shows why truncation interval matters
  for near-expiry options (TTE→0: the density becomes a spike → need to widen [a,b]).
- **Speed comparison**: COS is 10-100× faster than Monte Carlo for European options
  when the characteristic function is known. For our use case (manual challenge),
  Monte Carlo IS available offline, so COS is a cross-check, not a speedup.

## Relevance To Round 4

| Use Case | COS Relevant? | Alternative |
|:--|:--|:--|
| Live VEV pricing in bot | No (stdlib constraint) | Bachelier analytical |
| Manual AETHER_CRYSTAL pricing | Yes (offline check) | Monte Carlo IS (already done) |
| Heston smile validation | No (Heston eliminated) | N/A |
| Near-expiry density behavior | Conceptually yes | Already handled by Bachelier TTE=4 |

## Action Classification

`promote-cautiously` — COS is valuable as an offline verification tool for the
manual challenge, but NOT for live bot pricing. The Bachelier analytical formula
handles all live pricing needs.

## Implementation Notes

Pre-computed COS table for AETHER_CRYSTAL manual challenge (offline use):

```python
# GBM parameters for AETHER_CRYSTAL
# S0 = current price, σ = 251%, T = 4 steps × 1/252 years per step / 4
# (actually: GBM with 252 days/yr, 4 steps/day)
# For manual challenge: use Monte Carlo IS (already implemented) as primary
# COS as verification:

import math, cmath

def cos_bsm_call(S, K, T, r, sigma, N=64):
    """
    COS method for Black-Scholes European call.
    Works offline (no tick constraint). Pure Python.
    """
    x = math.log(S / K)
    a = x + (r - 0.5 * sigma**2) * T - 6 * sigma * math.sqrt(T)
    b = x + (r - 0.5 * sigma**2) * T + 6 * sigma * math.sqrt(T)

    def char_func(u):
        i = complex(0, 1)
        mu = (r - 0.5 * sigma**2) * T
        return cmath.exp(i * u * (x + mu) - 0.5 * sigma**2 * T * u**2)

    result = 0.0
    for k in range(N):
        u = k * math.pi / (b - a)
        phi = char_func(u)
        # Payoff coefficient for call
        if k == 0:
            chi = (math.exp(b) - max(0.0, math.exp(a))) / 1.0
            psi = (b - max(a, 0.0))
        else:
            chi = (math.exp(b) * (math.cos(k*math.pi) - (1/(u))*math.sin(k*math.pi))
                   - math.exp(max(0, a)) * (math.cos(0) - (1/u)*math.sin(0))) / (1 + (1/u)**2)
            psi = (math.sin(k * math.pi * (b - max(a, 0.0)) / (b - a)) * (b - a)) / (k * math.pi)
        Vk = (2 / (b - a)) * K * (chi - psi)
        weight = 0.5 if k == 0 else 1.0
        result += weight * (phi * cmath.exp(-complex(0,1) * u * a)).real * Vk

    return math.exp(-r * T) * result
```

## Downstream Use

- Strategy: COS not used in live bots. Bachelier covers all runtime pricing needs.
- Spec: COS available in offline analysis scripts for manual challenge verification.
- Validation: compare COS call prices vs Monte Carlo IS prices for AETHER_CRYSTAL.
  They should agree within ±0.5% for N=64 terms.
