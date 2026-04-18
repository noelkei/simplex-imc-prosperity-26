# Round 2 - "Growing Your Outpost"

Source: https://imc-prosperity.notion.site/Round-2-Growing-Your-Outpost-345e8453a09380b29132fdf4de9174d4

---

## Overview

Same two products as Round 1: `ASH_COATED_OSMIUM` and `INTARIAN_PEPPER_ROOT`.
Same position limits: 80 each.

Two new mechanics:
1. **Market Access Fee (MAF)**: bid for extra 25% market volume via `bid()` function in Trader.
2. **Manual: Invest & Expand**: allocate 50,000 XIRECs budget across Research / Scale / Speed.

Round 2 is the last qualifier before Phase 2. Target: net PnL ≥ 200,000 XIRECs cumulative.

---

## Algorithmic Trading: "Limited Market Access"

### Products & Limits
- `ASH_COATED_OSMIUM`: position limit 80 (same as R1)
- `INTARIAN_PEPPER_ROOT`: position limit 80 (same as R1)

### Market Access Fee (MAF)

Implement a `bid()` method inside `class Trader` returning an integer:
```python
class Trader:
    def bid(self):
        return 15   # your MAF bid in XIRECs

    def run(self, state: TradingState):
        ...
```

- **Extra access**: top 50% of bids across all participants get 25% more quotes in the order book.
- **Fee**: one-time, deducted from Round 2 profits if bid accepted.
- **Blind auction**: bids are compared only at final simulation, NOT during testing.
- **During testing**: all participants interact with 80% of generated quotes (no extra access regardless of bid).
- The MAF does not affect any round other than Round 2. `bid()` in other rounds is ignored.
- Accepted bids satisfy: `bid > median(all_bids)` (top 50%, not top 50% by count of accepted).

Example: bids [10, 20, 15, 19, 21, 34] → median = 19.5 → accepted = [20, 21, 34].

Extra market access example:
```
Without extra access:     With extra access:
ask 10 @ $9               ask 10 @ $9
ask 10 @ $7               ask  5 @ $8   ← extra quote (fits distribution)
bid 10 @ $5               ask 10 @ $7
bid  5 @ $4               bid 10 @ $5
                          bid  5 @ $4
```

PnL formula:
- With access (bid accepted):  `profit = R2_profit - bid`
- Without access (bid rejected): `profit = R2_profit`

### Game Theory for MAF
- Need top 50%, not highest. Extremely high bid wastes XIRECs.
- Estimated value of extra access ≈ 25% × test_PnL ≈ 2,500 XIRECs (if test PnL ≈ 10,000).
- Rational max bid ≈ value of extra access. Safe bid to be top 50%: bid slightly above expected median.
- Random testing variability: 80% of quotes are slightly randomized per submission. Submitting the same file multiple times has "very limited payoff."

---

## Manual Trading: "Invest & Expand"

Budget: **50,000 XIRECs**

### Three Pillars
Assign percentages (0–100% each, total ≤ 100%) to:
- **Research** (x%): edge strength. Formula: `research(x) = 200_000 * log(1+x) / log(1+100)` where log = natural log.
  - research(0) = 0, research(100) = 200,000.
- **Scale** (y%): market breadth. Linear: `scale(y) = 7 * y / 100`.
  - scale(0) = 0, scale(100) = 7.
- **Speed** (z%): win rate. **Rank-based** across all players.
  - Highest z investment → 0.9 multiplier. Lowest → 0.1.
  - Equal investments share the same rank.
  - Linear interpolation between ranks.
  - Example: investments [70,70,70,50,40,40,30] → ranks [1,1,1,4,5,5,7]
    - rank 1 → 0.9, rank 7 → 0.1, rank 4 → 0.5

### PnL Formula
```
PnL = Research(x) * Scale(y) * Speed(z_rank) - Budget_Used
Budget_Used = 50,000 * (x + y + z) / 100
```

### Key Numbers
- Research is **logarithmic**: 50% budget → 85% of max value. Diminishing returns beyond ~20-25%.
- Scale is **linear**: always worth investing proportionally.
- Speed is **zero-sum competition**: your rank relative to others determines multiplier.
- If everyone invests z=0: all tied at rank 1 → all get speed=0.9 (best case).
- If 50% invest z>0: z=0 players fall to speed≈0.5.
- The speed arms race makes a moderate investment (z=10-20%) a cheap insurance policy.

### Optimization Analysis (EDA)
Unconstrained optimum for fixed speed: maximize R(x)*S(y) with x+y=budget:
Condition: y = (1+x)*ln(1+x). For x=23, y=77 satisfies this approximately.

Best allocations by speed assumption (total=100%):
| Speed | Research | Scale | Speed_inv | P&L |
|-------|----------|-------|-----------|-----|
| 0.5 | 23% | 77% | 0% | 321,165 |
| 0.5 | 23% | 67% | 10% | 272,962 |
| 0.7 | 23% | 77% | 0% | 469,631 |
| 0.7 | 23% | 67% | 10% | 402,146 |

**Recommendation**: Research=23%, Scale=67%, Speed=10% as a balanced hedge.
- Costs only 5,000 XIRECs for speed insurance
- Expected P&L: 273k–402k depending on speed rank
- If Nash equilibrium = everyone at z=0 → you're still at rank 1 for being above 0%
