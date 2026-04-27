# Processed Paper Summary: Bergault et al. (2022)

## Status

`draft`

## Paper Metadata

- Paper ID: `bergault_2022_multi_asset_mm`
- Title: `Closed-Form Approximations in Multi-Asset Market Making`
- Authors: Philippe Bergault, David Evangelista, Olivier Gueant, Douglas Vieira
- Year: 2022
- Markdown file: `../../../round_3/research/papers_md/bergault_evangelista_gueant_vieira_2022_closed_form_approximations_in_multi_asset_market_making.md`
- Link: https://arxiv.org/abs/1810.04383

## Core Claim

In multi-asset market making, optimal quoting depends on **portfolio inventory**
rather than isolated per-symbol positions. The coupling between correlated assets
can be approximated analytically (quadratic value-function ansatz) without solving
a full high-dimensional dynamic program. The resulting quote skew formula:

```
δ_bid_i = f(q^T Γ e_i + ½ z_i e_i^T Γ e_i) + 1/k_i
δ_ask_i = f(-q^T Γ e_i + ½ z_i e_i^T Γ e_i) + 1/k_i
```

where Γ encodes inventory-covariance coupling, q is the inventory vector, e_i
is the unit vector for asset i.

## Assumptions

- Active vouchers VEV_5200–5400 share enough underlying-driven risk that a
  portfolio-style inventory term is meaningful.
- Simple moneyness/delta weights approximate the paper's full covariance matrix.
- The simplified exponential-intensity special case gives the most usable formula.

## Problem Addressed for Round 4

- We have a concentrated short position across three related strikes: VEV_5200,
  VEV_5300, VEV_5400 (all short ~300 units). These are correlated through VEX.
- Per-symbol limits (300 each) could mask family-level over-exposure.
- When all three strikes are maxed short simultaneously, the portfolio delta is
  -364, far exceeding the VEX hedge capacity of ±200.
- We need a family-coupling signal to detect when individual-symbol limits are
  simultaneously stressed and tighten the whole strategy.

## What This Paper Gives Us

- Key insight: the portfolio inventory vector q interacts with the covariance
  Γ to create cross-asset quote shifts. For our voucher family, Γ is
  approximately a scaled identity (strikes are correlated through VEX).
- Simplified formula (symmetric exponential intensity, Model B):
  ```
  δ_bid_i ≈ √γ × (q^T Γ e_i + ½ z_i e_i^T Γ e_i) + 1/k_i
  ```
- For our use case, collapse to a scalar family exposure metric:
  ```
  family_delta = Σ_i (pos_i × delta_i)  # total portfolio delta
  ```
  and use it to scale the quote shift across all active strikes.

## Relevance To Round 4

| Signal / Risk / Question | Relevance | Strength | Caveat |
|:--|:--|:--|:--|
| Short 300 × VEV_5200/5300/5400 simultaneously | family exposure = -364 delta; exceeds VEX limit | high | direct R4 risk |
| Family delta monitors un-hedged tail risk | Bergault's portfolio inventory term → our family_delta | high | use delta weights, not raw positions |
| Short-vol strategy with VEX hedge | cross-asset coupling makes VEX decisions affect all strikes | high | VEX = the "common stock" in the family |
| Upper strikes (5400/5500) have lower delta | deweight them in family exposure term | medium | confirmed by Bachelier delta table |

## Action Classification

`promote` — family delta metric is the practical implementation. Directly
addresses the un-hedged tail risk identified in the R4 delta hedge analysis.

## Implementation Notes

```python
# Bachelier deltas from calibrated sigma table
DELTA_TABLE = {
    4000: 0.9999, 4500: 0.9998, 5000: 0.9463, 5100: 0.8353,
    5200: 0.6199, 5300: 0.3720, 5400: 0.1582, 5500: 0.0648
}

# Family portfolio delta (Bergault q^T Γ e_i collapsed to scalar)
def compute_family_delta(positions, delta_table):
    """Portfolio delta = Σ pos_i × delta_i across all option strikes."""
    total = 0.0
    for strike, pos in positions.items():
        total += pos * delta_table.get(strike, 0.0)
    return total

# Usage example:
# positions = {5200: -300, 5300: -300, 5400: -300}
# family_delta = compute_family_delta(positions, DELTA_TABLE)
# → family_delta = -300×0.6199 + -300×0.3720 + -300×0.1582 = -345.03
# Required VEX hedge: -family_delta = +345 (but capped at 200)
# Residual un-hedged delta: -345 + 200 = -145

# Gate: if family_delta < -250 AND vex_pos < 150, stop adding short options
def family_risk_gate(family_delta, vex_pos, threshold=-250):
    un_hedged = family_delta + vex_pos
    return un_hedged > threshold  # True = safe to trade; False = stop

# Quote tilt proportional to family exposure (Bergault δ formula)
def family_quote_tilt(family_delta, strike, delta_table, risk_aversion=0.005):
    """Shift fair value by family delta pressure, weighted by strike delta."""
    weight = delta_table.get(strike, 0.0)
    return risk_aversion * family_delta * weight
```

## Downstream Use

- Strategy: compute family_delta at each tick. If abs(family_delta) > 200 AND
  VEX hedge is maxed, freeze new short entries across ALL active strikes.
  This prevents adding correlated risk beyond hedge capacity.
- Spec: log `family_delta` and `un_hedged_delta` to traderData each tick.
  Use family_quote_tilt() as a modifier on top of per-strike fair values.
- Validation: monitor family_delta time series. If it consistently sits near
  -300 to -400, the hedge cap is binding and risk is growing.
