# Processed Paper Summary: Easley and O'Hara (1987)

## Status

`draft`

## Paper Metadata

- Paper ID: `easley_ohara_1987_price_trade_size`
- Title: `Price, Trade Size, and Information in Securities Markets`
- Authors: David Easley, Maureen O'Hara
- Year: 1987
- Link: https://www.sciencedirect.com/science/article/pii/0304405X87900250

## Core Claim

Trade SIZE is an additional signal for adverse selection beyond trade direction.
Large trades are more likely to be informed than small trades. Market makers
should set **size-dependent spreads**: wider for larger orders.

Key implications:
- Informed traders place larger orders to maximize informational advantage.
- Uninformed (liquidity) traders have no reason to concentrate in large sizes.
- Quote should be: `bid(large) < bid(small)` and `ask(large) > ask(small)`.

## Assumptions

- Informed traders optimize trade size based on their signal strength.
- Order flow can be decomposed into informed and uninformed components.
- In Round 4: trade size information IS available in market_trades.

## Problem Addressed for Round 4

- We observe named counterparties AND trade quantities in `state.market_trades`.
- Mark 22 consistently trades in batches of 10–20 units of VEV_5200–6500.
- Mark 67 trades VEX in larger blocks.
- Easley-O'Hara tells us: the COMBINATION of identity + size is more informative
  than identity alone for updating our beliefs about fair value.
- Also applies to anonymous public trades in the order book: large market orders
  are more likely to be informed.

## What This Paper Gives Us

- Size-conditional adverse selection adjustment:
  ```
  adverse_adj(size) = base_adverse_adj × size_multiplier(size)
  where size_multiplier(10) ≈ 1.0, size_multiplier(30) ≈ 1.5
  ```
  
- Priority ordering for information content:
  1. Named informed counterparty (Mark 22) + large size → maximum caution
  2. Named informed counterparty + small size → moderate caution
  3. Anonymous + large size → elevated caution
  4. Named uninformed counterparty + any size → normal spread
  5. Anonymous + small size → baseline spread

- Quote response protocol for R4:
  ```
  if mark22_selling AND trade.quantity >= 15:
      → immediate bid withdrawal + widen ask by 2 ticks
  elif mark22_selling AND trade.quantity < 15:
      → widen ask by 1 tick, keep bid but widen by 1
  elif anonymous AND trade.quantity >= 20:
      → widen by 0.5 tick (suspicious, unknown agent)
  ```

## Relevance To Round 4

| Signal | Easley-O'Hara Interpretation | R4 Action |
|:--|:--|:--|
| Mark 22 sells 10× VEV_5300 | informed+large → high adverse selection | remove bid, widen ask |
| Mark 01 buys 10× VEV_5400 | artificial loop → NOT informed, treat as noise | ignore |
| Anonymous 25-unit market sell | possibly informed → moderate caution | widen bid |
| Mark 67 buys 30 VEX | uninformed momentum → no adverse selection | tighten VEX ask |
| Mark 22 sells 5 VEV_5200 | informed+small → probe or limit order | moderate caution |

## Action Classification

`promote` — size-conditional adverse selection layered on top of counterparty
identity gives a richer signal hierarchy. Implementable in O(1) per tick.

## Implementation Notes

```python
# Trade size thresholds calibrated from EDA (Mark 22 typical lot = 10-15)
SMALL_TRADE = 10
LARGE_TRADE = 20

# Combined Easley-O'Hara + Glosten-Milgrom risk score
def trade_adverse_score(seller, quantity, symbol):
    """
    Returns a [0, 1] adverse selection score for a sell-side trade.
    0 = no adverse selection, 1 = maximum caution.
    """
    score = 0.0
    # Identity component (GM)
    if seller == "Mark 22":
        score += 0.6
    elif seller is None:  # anonymous
        score += 0.2
    else:
        score += 0.0  # known uninformed

    # Size component (EO)
    if quantity >= LARGE_TRADE:
        score += 0.3
    elif quantity >= SMALL_TRADE:
        score += 0.1

    # Symbol component (upper strikes more dangerous with Mark 22)
    if symbol in ("VEV_5300", "VEV_5400", "VEV_5500"):
        score = min(1.0, score + 0.1)

    return min(1.0, score)

def quote_adjustment_from_adverse_score(score):
    """
    Returns (bid_adj, ask_adj) in ticks based on adverse selection score.
    Positive adjustment = move quote away from mid (widen).
    """
    if score >= 0.8:
        return (-2, +2)   # remove bid, widen ask
    elif score >= 0.5:
        return (-1, +1)   # widen both
    elif score >= 0.2:
        return (0, +1)    # widen ask only
    else:
        return (0, 0)     # no adjustment
```

## Downstream Use

- Strategy: combine identity (GM) and size (EO) into one adverse_score per
  trade. Apply quote_adjustment_from_adverse_score() to all active strikes.
- Spec: compute adverse_score for all market_trades at each tick. Maintain a
  rolling 3-tick window of max adverse_score per symbol.
- Validation: track adverse_score distribution; verify that high-score ticks
  correlate with negative markout on that strike.
