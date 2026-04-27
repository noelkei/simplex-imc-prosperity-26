# Processed Paper Summary: Stoikov and Saglam (2009)

## Status

`draft`

## Round 4 Role

- Reference class: `carry-forward reference`
- Priority for Strategy: below the top-level `round4_raw_derived` processed core
- Allowed use: inventory-risk framing, validation cross-checks, and quote-tilt intuition
- Caution: if current-round EDA or raw-derived `round_4` papers conflict with this note, prefer current-round evidence

## Paper Metadata

- Paper ID: `stoikov_saglam_2009_option_mm_inventory`
- Title: `Option Market Making under Inventory Risk`
- Authors: Sasha Stoikov, Mehmet Saglam
- Year: 2009
- Markdown file: `../../../round_3/research/papers_md/stoikov_saglam_2009_option_market_making_under_inventory_risk.md`
- Link: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1393818

## Core Claim

Option market-makers should tilt quotes as inventory risk builds, not just apply
hard position caps. The relevant exposure is a **mix of net delta plus residual
gamma/vega risk** when hedging is incomplete. Near expiry, the gamma term
dominates — which is precisely the TTE=4 regime we are in.

Key insight from the paper's maturity split:
- Long-maturity options: vega (stochastic vol) risk dominates residual PnL
- **Short-maturity options: gamma risk dominates residual PnL** (TTE ≤ 5)

At TTE=4, residual PnL increments are dominated by:
```
ΔI ≈ q_option × ½ × Γ × σ² × S² × (u² - 1) × Δt
```
This is the core risk we must manage when short 300 × VEV_5200/5300.

## Assumptions

- Delta hedging via VEX is available but capped at ±200 units.
- No continuous hedging; discrete per-tick hedge adjustments only.
- Inventory exposure is the joint option + VEX position, not option alone.
- Simple quote-skew heuristics are more deployable than the full dynamic program.

## Problem Addressed for Round 4

- We are short ~900 units of options (300 × VEV_5200/5300/5400) with positive
  delta requiring +364 VEX to fully hedge, capped at +200.
- Residual un-hedged delta ≈ -164 with elevated gamma at TTE=4.
- We need a principled way to: (a) skew quotes to stop adding more short gamma,
  (b) use VEX quote behavior to simultaneously manage stock-level exposure.
- The paper's incomplete-market case (Theorem 4/5) applies directly.

## What This Paper Gives Us

- Core formula — inventory-aware quote premium (incomplete market):
  ```
  ask_premium = max(0, min(C/D, C/(2D) - γ·k·(q_option - ½)))
  bid_premium = max(0, min(C/D, C/(2D) + γ·k·(q_option + ½)))
  ```
  where k encodes residual gamma/vega risk:
  ```
  k = (½σ²(T-t) + α²(T_mat-t)²) × Γ² × S⁴ × σ²(T-t)
  ```
- Simplified implementation for Round 4:
  widen ask (make selling harder to fill) and narrow bid as short gamma
  position grows. At TTE=4, scale k by Bachelier Γ from the sigma table.
- Multi-period: quote tilt steepens as expiry approaches. This is the
  "flattening near horizon" behavior we need to implement.

## Relevance To Round 4

| Signal / Risk / Question | Relevance | Strength | Caveat |
|:--|:--|:--|:--|
| Short 300 VEV_5200: large gamma at TTE=4 | paper gives exact framework for gamma-risk quote tilt | high | we simplify to heuristic skew |
| VEX cap at ±200 → un-hedged delta -164 | incomplete market case applies directly | high | single-asset hedge, not joint stock+option |
| Quote skew should increase near TTE=0 | confirms more aggressive position flattening in R5, R6, R7 | high | future rounds, not immediate |
| Short VEV_5400/5500 has lower gamma | lighter skew justified for OTM positions | medium | confirmed by Bachelier Γ table |

## Action Classification

`promote` — incomplete-market gamma-risk quote tilt is directly applicable.
Simplified heuristic is implementable in O(1) per tick.

## Implementation Notes

```python
# Bachelier gamma values at TTE=4 (from calibrated sigma table)
GAMMA_TABLE = {
    5000: 0.0019, 5100: 0.0032, 5200: 0.0040,
    5300: 0.0039, 5400: 0.0027, 5500: 0.0013
}

# Inventory-aware quote skew for short-vol positions
# pos_option: current position (negative = short)
# Positive skew_shift = raise ask (don't want more shorts)
# Negative skew_shift = lower bid (don't want to be bought back)
def inventory_skew(pos_option, strike, gamma_table, risk_aversion=0.01):
    gamma = gamma_table.get(strike, 0.002)
    # k ≈ gamma² × S⁴ × σ² × T (simplified from paper)
    # For practicality, use linear approximation: k_proxy = gamma × 100
    k_proxy = gamma * 100
    skew = risk_aversion * k_proxy * pos_option
    return skew  # add to reservation price

# Usage: fair_value_skewed = fair_value + inventory_skew(pos, strike, GAMMA_TABLE)
# Short position (pos < 0) → skew is negative → lower bid, raise ask
```

## Downstream Use

- Strategy: short-vol positions (especially VEV_5200/5300) must apply quote
  tilt as position approaches -300. Do not passively accept more shorts when
  at the limit.
- Spec: add `inventory_skew()` modifier to option fair-value computation.
  Gate: if abs(pos_option) > 250, widen ask by +1 tick to discourage fills.
- Validation: track realized skew vs theoretical; monitor whether tilt reduces
  unwanted inventory accumulation in VEV_5200/5300.
