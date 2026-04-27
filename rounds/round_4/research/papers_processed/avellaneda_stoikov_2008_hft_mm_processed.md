# Processed Paper Summary: Avellaneda and Stoikov (2008)

## Status

`draft`

## Paper Metadata

- Paper ID: `avellaneda_stoikov_2008_hft_mm`
- Title: `High-Frequency Trading in a Limit Order Book`
- Authors: Marco Avellaneda, Sasha Stoikov
- Year: 2008
- Link: https://math.nyu.edu/~avellane/HighFrequencyTrading.pdf

## Core Claim

The optimal market-making strategy involves quoting around a **reservation price**
that is skewed from the mid-price by inventory. The spread is set to capture a
target profit rate given the arrival intensities of buyers and sellers.

Key formulas:
```
reservation_price = s - q × γ × σ² × (T - t)    # inventory-adjusted mid
spread = γ × σ² × (T - t) + (2/γ) × ln(1 + γ/k)  # optimal half-spread
```
where:
- s = current mid-price
- q = current inventory (+ = long, - = short)
- γ = risk aversion parameter
- σ = price volatility
- T - t = time horizon remaining
- k = order arrival intensity decay parameter

## Assumptions

- Poisson arrivals for buy and sell orders with exponential intensity decay.
- Continuous-time control, approximated here to per-tick decisions.
- Single asset; we extend to multi-strike by applying per-strike with family overlay.
- At TTE=4/365 the "time horizon" T-t maps to our remaining rounds.

## Problem Addressed for Round 4

- We need a principled rule for quote placement that accounts for:
  (a) current inventory in each option strike
  (b) time remaining (TTE=4, getting shorter each round)
  (c) risk aversion to large gamma exposure
- Avellaneda-Stoikov gives a clean formula for the reservation price and spread.
- Extension: replace σ (stock vol) with option-specific risk measure = Γ × σ_VEX²
  to account for the fact that we carry option, not stock.

## What This Paper Gives Us

- **Reservation price formula** — the most directly useful output:
  ```
  r = fair_value - pos × γ × option_risk × TTE
  ```
  where option_risk = Γ × σ_VEX² for the strike.

- **Spread formula** — gives the minimum spread to earn positive expected value:
  ```
  spread = γ × option_risk × TTE + (2/γ) × ln(1 + γ/k)
  ```
  In practice, we use spread = max(1, inventory_penalty) ticks.

- **Inventory skew direction**:
  - Short options (pos < 0): reservation_price shifts UP (we prefer to buy back)
  - Long options (pos > 0): reservation_price shifts DOWN (we prefer to sell off)
  - At TTE=4, the γ × option_risk × TTE term is significant for ATM strikes.

- **Time sensitivity**: as TTE decreases (R5, R6, R7), the inventory penalty grows.
  A fixed inventory position becomes more dangerous each round. This supports
  actively flattening positions as TTE approaches 1.

## Relevance To Round 4

| Concept | R4 Application | Strike Specifics |
|:--|:--|:--|
| Reservation price | skew fair_value by pos × risk | 5200: risk = 0.0040 × 1491² |
| Inventory-aware spread | widen when large short position | 5200/5300 are primary risk |
| Time horizon shrinks per round | TTE=4 → 3 → 2 → 1; scale risk up | urgency increases each round |
| Poisson arrival approximation | passive quoting at reservation ± half-spread | applies per strike |

## Action Classification

`promote` — reservation price formula is directly implementable. Replaces
ad-hoc inventory management with principled Avellaneda-Stoikov framework.

## Implementation Notes

```python
import math

# Calibrated option risk parameters for TTE=4
TTE_R4 = 4 / 365.0
GAMMA_TABLE = {5200: 0.0040, 5300: 0.0039, 5400: 0.0027, 5500: 0.0013}
SIGMA_VEX = 1491.5  # use VEX realized vol (from EDA: 571 annualized → daily)
RISK_AVERSION = 0.001  # γ, tunable

def reservation_price(fair_value, pos, strike, tte=TTE_R4, gamma=RISK_AVERSION):
    """Avellaneda-Stoikov reservation price adjusted for option inventory risk."""
    option_risk = GAMMA_TABLE.get(strike, 0.002) * SIGMA_VEX ** 2
    return fair_value - pos * gamma * option_risk * tte

def optimal_spread(strike, tte=TTE_R4, gamma=RISK_AVERSION, k=1.5):
    """Avellaneda-Stoikov optimal half-spread (in price units)."""
    option_risk = GAMMA_TABLE.get(strike, 0.002) * SIGMA_VEX ** 2
    half_spread = gamma * option_risk * tte + (2 / gamma) * math.log(1 + gamma / k)
    return max(1.0, half_spread)  # minimum 1-tick spread

# Usage:
# pos = -280 (short 280 VEV_5200)
# fair = 59.2 (Bachelier fair value)
# r = reservation_price(fair, pos, 5200)  # shifts UP since pos < 0
# bid = r - optimal_spread(5200)
# ask = r + optimal_spread(5200)
```

## Downstream Use

- Strategy: use reservation_price() as the basis for all passive quote placement
  in active option strikes. This replaces the simple "fair ± V_OFFSET" approach.
- Spec: compute r and spread per strike at each tick. Log r, spread, and the
  inventory penalty term to traderData for validation.
- Validation: check whether realized fills cluster around r (good calibration)
  or systematically outside the spread (V_OFFSET miscalibration).
