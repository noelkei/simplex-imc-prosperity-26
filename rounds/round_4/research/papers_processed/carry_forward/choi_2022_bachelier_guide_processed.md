# Processed Paper Summary: Choi, Kwak, Tee, Wang (2022)

## Status

`draft`

## Round 4 Role

- Reference class: `carry-forward reference`
- Priority for Strategy: below the top-level `round4_raw_derived` processed core
- Allowed use: pricing/framing support, validation cross-checks, and Greek intuition
- Caution: if current-round EDA or raw-derived `round_4` papers conflict with this note, prefer current-round evidence

## Paper Metadata

- Paper ID: `choi_2022_bachelier_guide`
- Title: `A Black-Scholes User's Guide to the Bachelier Model`
- Authors: Jaehyuk Choi, Minsuk Kwak, Chyng Wen Tee, Yumeng Wang
- Year: 2022
- Markdown file: none (summary from knowledge)
- Link: https://arxiv.org/abs/2104.08686

## Core Claim

The Bachelier model (normal distribution for price returns, not log-returns) is
analytically superior to Black-Scholes when the underlying can trade near or
below zero and when the implied vol smile is nearly flat. It provides simpler
Greeks, a cleaner delta-hedge, and easier calibration for near-ATM options.
Key formula: `C = (F-K)·Φ(d) + σ√T·φ(d)` where `d = (F-K)/(σ√T)`.

## Assumptions

- Price returns are approximately normally distributed at the tick level.
- Interest rates are zero (risk-neutral drift = 0).
- Volatility σ is constant within a strike bucket (the "flat smile" assumption).

## Problem Addressed for Round 4

- We need the correct per-strike Bachelier sigma for TTE=4/365 (Round 4).
- We need Greeks (delta, gamma, vega, theta) from Bachelier for portfolio
  management and for estimating the VEX hedge requirement analytically.
- Round 3 used sigma_abs=95 (wrong); Round 4 must use the calibrated table.

## Calibrated Sigma Table (Round 4, TTE=4/365, S≈5247.6)

| Strike | Bachelier σ | BS IV | Delta (Δ) | Gamma (Γ·σ√T) | Vega | Theta/day |
|-------:|------------:|------:|----------:|---------------:|-----:|----------:|
| 4000 | 3199.8 | 69.64% | 0.9999 | ≈0 | ≈0 | ≈0.01 |
| 4500 | 1982.5 | 40.76% | 0.9998 | ≈0 | ≈0 | ≈0.01 |
| 5000 | 1469.7 | 28.69% | 0.9463 | 0.0019 | 8.45 | 1.86 |
| 5100 | 1446.0 | 27.95% | 0.8353 | 0.0032 | 13.40 | 4.68 |
| 5200 | 1491.5 | 28.55% | 0.6199 | 0.0040 | 17.27 | 7.91 |
| 5300 | 1531.8 | 29.05% | 0.3720 | 0.0039 | 17.26 | 8.06 |
| 5400 | 1452.8 | 27.29% | 0.1582 | 0.0027 | 11.35 | 4.56 |
| 5500 | 1590.4 | 29.60% | 0.0648 | 0.0013 | 6.01 | 2.38 |

Theta/day = C(TTE=4/365) - C(TTE=3/365). Positive for short positions.

## Bachelier Greeks (Implementable Formulas)

```python
# All formulas use: d = (S - K) / (sigma * sqrt(T))
# vt = sigma * sqrt(T)
delta = norm_cdf(d)                       # dC/dS
gamma = norm_pdf(d) / (sigma * sqrt(T))  # d²C/dS²
vega  = sqrt(T) * norm_pdf(d)            # dC/dσ
theta = -sigma * norm_pdf(d) / (2*sqrt(T)) / 365  # dC/dt per calendar day
```

## What This Paper Gives Us

- Formula: Bachelier call price, all Greeks in closed form.
- Simplification: delta is `N(d)`, not the complex BS `N(d1)`. Gamma is
  `φ(d)/(σ√T)` — simpler to compute and numerically stable near ATM.
- Constraint: Bachelier assumes normal returns. VEX tick distribution is
  discrete (0/±1/±2/±3) but approximately normal — adequate.
- Key insight: For near-ATM options, Bachelier and BS give nearly identical
  prices, but Bachelier is more stable when σ√T is small (short TTE).

## Relevance To Round 4

- TTE=4 is one step shorter than Round 3's TTE=5. Theta is higher.
- The vol smile is nearly flat in the active zone (Bachelier sigma ratio
  0.969–1.066 for strikes 5000–5500), confirming Bachelier adequacy.
- The hardcoded sigma table above replaces all EMA-based sigma estimation.
- Greeks enable exact VEX hedge sizing: hedge = -Σ(pos_i × delta_i).

## Action Classification

`promote` — formulas are exact, calibrated, and ready to copy into bots.

## Implementation Notes

```python
TTE_R4 = 4 / 365.0
SIGMA_TABLE = {
    4000: 3199.8, 4500: 1982.5,
    5000: 1469.7, 5100: 1446.0, 5200: 1491.5,
    5300: 1531.8, 5400: 1452.8, 5500: 1590.4,
}
```

## Downstream Use

- Strategy: calibrated sigma table feeds all option fair-value computations.
- Spec: Greeks enable exact hedge sizing. Theta enables expected inter-round PnL.
- Validation: compare bot's computed fairs against market mids at each tick.
