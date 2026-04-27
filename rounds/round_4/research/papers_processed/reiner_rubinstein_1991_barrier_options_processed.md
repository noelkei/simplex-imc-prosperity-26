# Processed Paper Summary: Reiner and Rubinstein (1991) — Barrier Options

## Status

`draft`

## Paper Metadata

- Paper ID: `reiner_rubinstein_1991_barrier_options`
- Title: `Breaking Down the Barriers`
- Authors: Eric Reiner, Mark Rubinstein
- Year: 1991
- Link: https://www.risk.net/derivatives/1520283/breaking-down-barriers

## Core Claim

Barrier options (knock-in, knock-out, up-and-out, down-and-out, etc.) have
closed-form prices under GBM. The formulas are extensions of Black-Scholes that
account for the barrier crossing probability.

**Down-and-Out Put** (most relevant to manual challenge — knock-out put):
```
P_DOput = P_BSM(S, K, T, σ) - (H/S)^(2λ-2) × P_BSM(H²/S, K, T, σ)
where λ = (r + σ²/2) / σ²
```

More precisely, the analytical closed-form for a down-and-out put with:
- Barrier H < S (option knocked out if S falls to H)
- Strike K (typically K ≥ H)
- At r=0:
```
P_DOput = P_BSM(S, K, T, σ) - (H/S)^{2λ} × P_BSM(H²/S, K, T, σ)
where λ = 1 - r/σ² ≈ 1 at r=0
```

At r=0, the reflection principle gives:
```
P_KOpput = P_BSM(S, K, T, σ) - (H/S)^0 × P_BSM(H²/S, K, T, σ)
         = P_BSM(S, K, T, σ) - P_BSM(H²/S, K, T, σ)
```

## Assumptions

- GBM for AETHER_CRYSTAL (continuous path, not discrete).
- Barrier is monitored continuously (in practice, Prosperity uses discrete steps:
  4 steps/day × 252 days/year → path sampling may differ slightly).
- r = 0 (Prosperity convention).
- H < K < S (down-and-out put: H is floor barrier below current price and strike).

## Problem Addressed for Round 4

The manual challenge AETHER_CRYSTAL includes a **knock-out put** option.
The put is knocked out (becomes worthless) if AETHER_CRYSTAL falls to the barrier H.

**Key distinction from plain put**:
- Plain put: profits if S < K at expiry
- KO put: profits if S < K at expiry AND S never touched H during the life
- KO put price < Plain put price (additional risk of barrier knockout)

**Discrete barrier correction** (Broadie-Glasserman, 1997):
When the barrier is monitored at discrete times (as in Prosperity), the effective
barrier is shifted by:
```
H_effective = H × exp(±0.5826 × σ × √(dt))
```
For a down-and-out put: H_effective is slightly LOWER than H
(discrete monitoring gives less chance of hitting barrier → higher KO put value).

## What This Paper Gives Us

- **Closed-form KO put**: implementable in Python stdlib using bsm_put().
- **Barrier correction**: adjust H downward for discrete monitoring.
- **Pricing hierarchy**: KO put < plain put (quick sanity check).
- **At H → 0**: KO put → plain put (another boundary condition).

## Action Classification

`promote` — closed-form barrier option price is directly implementable.
The discrete barrier correction is a small but important accuracy improvement.

## Implementation Notes

```python
import math
from statistics import NormalDist

_nd = NormalDist()

def bsm_put(S, K, T, sigma, r=0.0):
    """Standard BSM put price."""
    if T <= 0:
        return max(K - S, 0.0)
    vt = sigma * math.sqrt(T)
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / vt
    d2 = d1 - vt
    return K * math.exp(-r * T) * _nd.cdf(-d2) - S * _nd.cdf(-d1)

def down_and_out_put(S, K, H, T, sigma, r=0.0, discrete_steps=None):
    """
    Reiner-Rubinstein (1991) down-and-out put price.
    H = barrier level (H < S and H ≤ K typically)
    discrete_steps: if not None, apply Broadie-Glasserman discrete barrier correction.
    """
    if H >= S:
        return 0.0  # already knocked out

    # Discrete barrier correction (Broadie-Glasserman 1997)
    if discrete_steps is not None:
        dt = T / discrete_steps
        H_adj = H * math.exp(-0.5826 * sigma * math.sqrt(dt))
    else:
        H_adj = H

    # Reiner-Rubinstein formula at r=0 (λ = 1)
    lam = 1.0 - r / (sigma**2) if sigma > 0 else 1.0
    mu = r / (sigma**2) - 0.5  # drift parameter

    # Image stock price reflected at barrier
    S_image = H_adj**2 / S

    plain_put = bsm_put(S, K, T, sigma, r)
    image_put = bsm_put(S_image, K, T, sigma, r)

    # Reflection factor
    reflection = (H_adj / S) ** (2 * lam - 2)

    return plain_put - reflection * image_put

# Example for AETHER_CRYSTAL manual challenge:
# S = 100, K = 90, H = 70 (barrier), sigma = 2.51
# T = 4/252, discrete_steps = 4*4 = 16 (4 steps/day × 4 days)
# price = down_and_out_put(S, K, H, T, sigma, discrete_steps=16)
#
# Sanity checks:
# price < bsm_put(S, K, T, sigma)   → KO put cheaper than plain put
# As H → 0: price → plain put
# As H → S: price → 0 (immediately knocked out)
```

## Downstream Use

- Strategy: compute down_and_out_put() for the manual challenge KO put instrument.
  Apply discrete barrier correction (4 steps/day in Prosperity).
- Spec: use both closed-form AND Monte Carlo IS as cross-checks. If they agree
  within 2%, use closed-form as the final answer.
- Validation:
  - KO put < plain put (always true)
  - KO put(H=0) = plain put
  - KO put(H=S) = 0
  All three boundary conditions must hold numerically.
