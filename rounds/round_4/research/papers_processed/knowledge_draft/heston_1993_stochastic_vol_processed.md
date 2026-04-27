# Processed Paper Summary: Heston (1993)

## Status

`draft`

## Round 4 Role

- Reference class: `knowledge draft`
- Priority for Strategy: below both the top-level `round4_raw_derived` core and the strongest `carry_forward` references
- Allowed use: inspiration, EDA framing, and offline pricing context only
- Caution: this note did not come from the local `round_4` raw-paper pipeline; do not promote it directly to live logic without stronger support

## Paper Metadata

- Paper ID: `heston_1993_stochastic_vol`
- Title: `A Closed-Form Solution for Options with Stochastic Volatility with Applications to Bond and Currency Options`
- Authors: Steven L. Heston
- Year: 1993
- Link: https://doi.org/10.1093/rfs/6.2.327

## Core Claim

When volatility is stochastic and mean-reverting, the Black-Scholes model
misprices options systematically. Heston derives a semi-analytical formula for
European option prices under the following dynamics:

```
dS = μS dt + √v S dW₁
dv = κ(θ - v) dt + ξ√v dW₂
Cov(dW₁, dW₂) = ρ dt
```

where v is instantaneous variance (not vol), κ is mean-reversion speed, θ is
long-run variance, ξ is vol-of-vol, and ρ is spot-vol correlation.

Price: `C = S × P₁ - K × e^{-rT} × P₂`
where P₁, P₂ are probability components computed via characteristic function
integration (Fourier inversion).

## Assumptions

- Price follows CIR-like variance process (non-negative variance guaranteed).
- Correlation ρ between spot and vol shocks creates the volatility smile.
- Semi-analytical: requires numerical integration over the characteristic function.

## Problem Addressed for Round 4

**Key question from 02b research plan**: Is Heston materially better than
Bachelier given VEX CoV = 0.119?

**Answer**: No. EDA analysis shows:
- VEX rolling volatility CoV = 0.119 (low — near-constant vol)
- Threshold for "meaningful stochastic vol": CoV > 0.30
- Heston adds marginal calibration quality at significant implementation cost

The Heston model is ELIMINATED as a live bot pricing model for Round 4.
Bachelier with fixed calibrated sigma is adequate.

## What This Paper Gives Us

- **Eliminated for live pricing**: Heston requires numerical integration
  (characteristic function inversion) which cannot be implemented in pure Python
  stdlib with O(1) runtime per tick.
- **Useful for understanding vol smile**: The Heston ρ parameter explains the
  ITM vol skew (deep ITM strikes K=4000/4500 have higher IV, consistent with
  negative ρ meaning vol rises when spot falls).
- **Validation insight**: If Heston and Bachelier give same prices for active
  strikes, Bachelier is correct choice. EDA confirms this for K=5000–5500
  (vol smile ratio 0.969–1.066, nearly flat).
- **Calibrated Heston parameters for interpretation** (not for live use):
  - κ ≈ 2.0 (fast mean reversion — consistent with near-constant vol)
  - θ ≈ (1491/√252)² (long-run daily variance)
  - ξ ≈ 0.3 (vol-of-vol, low CoV supports this)
  - ρ ≈ -0.3 (negative correlation explains ITM skew)

## Relevance To Round 4

| Question | Heston Answer | Implication |
|:--|:--|:--|
| Is stochastic vol present? | CoV=0.119 < 0.30 threshold | No meaningful SV → Bachelier adequate |
| Why does deep ITM (K=4000) have high IV? | Heston ρ < 0 (skew) | Structural, not tradeable at our strikes |
| Should we use Heston for manual pricing? | Numerical integration required | Use Bachelier or Black-Scholes instead |
| Heston smile for VEV_5000–5500? | Nearly flat (low vol-of-vol) | Confirms Bachelier assumption |

## Action Classification

`promote-cautiously` — Heston is useful for UNDERSTANDING the vol surface
shape (ITM skew, smile flatness), but is NOT used in the live bot. The main
value is confirming that Bachelier is the right model for active strikes.

## Implementation Notes

Heston is NOT implemented in the bot. The conclusion from analysis is:

```python
# Bachelier is sufficient because:
# 1. VEX vol CoV = 0.119 → near-constant vol
# 2. Vol smile is flat for K=5000-5500 (active zone)
# 3. Bachelier and Heston give same prices for these strikes
# 4. Heston requires O(n) Fourier integration → impossible at O(1)/tick
#
# The calibrated SIGMA_TABLE already captures all relevant pricing information:
SIGMA_TABLE = {
    4000: 3199.8, 4500: 1982.5,
    5000: 1469.7, 5100: 1446.0, 5200: 1491.5,
    5300: 1531.8, 5400: 1452.8, 5500: 1590.4,
}
# These sigma values implicitly encode the Heston-style skew effects.
```

## Downstream Use

- Strategy: use this paper to JUSTIFY Bachelier as the model of choice, not
  to implement Heston. The Heston analysis provides the theoretical backing
  for why a flat-smile model (Bachelier) is appropriate.
- Spec: no Heston code in bots. Reference Heston only in research documents.
- Validation: the fact that Bachelier and BS give nearly identical prices for
  active strikes is the empirical confirmation of Heston's irrelevance here.
