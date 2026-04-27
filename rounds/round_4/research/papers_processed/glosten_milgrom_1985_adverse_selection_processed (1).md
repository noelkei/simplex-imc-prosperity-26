# Processed Paper Summary: Glosten and Milgrom (1985)

## Status

`draft`

## Paper Metadata

- Paper ID: `glosten_milgrom_1985_adverse_selection`
- Title: `Bid, Ask and Transaction Prices in a Specialist Market with Heterogeneously Informed Traders`
- Authors: Lawrence R. Glosten, Paul R. Milgrom
- Year: 1985
- Link: https://www.sciencedirect.com/science/article/pii/0304405X85900443

## Core Claim

The bid-ask spread in financial markets is not just a transaction cost — it is
partly compensation for adverse selection from informed traders. A market maker
who cannot distinguish informed from uninformed order flow must widen spreads to
break even against the adverse selection. The spread has three components:

1. **Adverse selection component**: compensation for trading against informed agents
2. **Inventory holding cost**: compensation for imbalanced positions
3. **Order processing cost**: fixed operational costs

Key formula (competitive MM equilibrium):
- Ask = E[V | buy] > E[V]  (you buy from someone who knows it's worth more)
- Bid = E[V | sell] < E[V]  (you sell to someone who knows it's worth less)
- Spread = Ask - Bid = f(fraction of informed traders × signal precision)

## Assumptions

- Market maker cannot observe trader type (informed vs. uninformed) ex ante.
- Informed traders have a signal about the true value V.
- Uninformed traders trade for liquidity reasons only.
- Zero-profit condition for competitive market maker.

## Problem Addressed for Round 4

Round 4 fundamentally changes the information environment:
- We now **can** observe trader identity (`Trade.buyer`, `Trade.seller`).
- Mark 22 is a known informed agent (deterministic OTM seller).
- Mark 01 is a known counterparty in an artificial loop (uninformed in the GM sense).
- This breaks the key GM assumption: **we can now discriminate informed from uninformed**.

GM tells us: if we can identify informed traders, we should:
1. Set a narrower spread against uninformed flow (Mark 01, Mark 38, Mark 14).
2. Set a wider spread (or refuse to trade) against informed flow (Mark 22).
3. Update our estimate of V based on who is trading.

## What This Paper Gives Us

- Framework: Bayesian updating of fair value based on trade identity.
  When Mark 22 sells VEV_5200, update fair value DOWN for that strike.
  When Mark 67 buys VEX, update VEX fair value UP (mildly).

- Quote skew rule (implementable):
  ```
  # After observing Mark 22 sell at strike K:
  # Bayesian update: fair_value[K] decreases (Mark 22 knows something)
  # Response: widen our bid (or remove it entirely)
  fair_value_adj = fair_value[K] - mark22_signal_weight × recent_mark22_volume
  ```

- Spread decomposition for Prosperity:
  - Adverse selection spread (from informed Mark 22): ~2-4 ticks wider ask
  - Inventory spread: from Stoikov-Saglam
  - Processing spread: ≈0 in Prosperity (no fixed costs)

- Counterparty-conditional bid-ask:
  - Mark 22 sells → our bid is dangerous (we'd be buying from informed seller)
  - Mark 67 buys VEX → our VEX ask should be tighter (uninformed momentum)

## Relevance To Round 4

| Signal / Risk | GM Interpretation | R4 Implementation |
|:--|:--|:--|
| Mark 22 selling VEV_5200+ | informed seller signal → E[V\|sell] < E[V] | hard no-buy veto |
| Mark 01 buying VEV_5400+ | synthetic loop → NOT informed signal | ignore (artificial flow) |
| Mark 67 buying VEX | uninformed momentum → update VEX fair value up | mild lean on VEX bid |
| Mark 14 balanced HYDROGEL | market-maker flow → uninformed baseline | normal spread |
| Mark 38 ITM vouchers | structural flow → uninformed | normal spread |

## Action Classification

`promote` — the ability to identify informed vs uninformed traders makes
Glosten-Milgrom directly operational in Round 4. Mark 22 = informed seller.

## Implementation Notes

```python
# Mark 22 adverse selection gate
MARK22_ADVERSE = "Mark 22"
MARK67_POSITIVE = "Mark 67"

def update_fair_from_counterparty(fair_values, market_trades, signal_weight=0.5):
    """Bayesian-style fair value update based on counterparty identity."""
    for symbol, trades in market_trades.items():
        for trade in trades:
            if trade.seller == MARK22_ADVERSE:
                # Mark 22 selling = informed downward signal
                if symbol in fair_values:
                    fair_values[symbol] -= signal_weight * trade.quantity
            elif trade.buyer == MARK67_POSITIVE and symbol == "VELVETFRUIT_EXTRACT":
                # Mark 67 buying VEX = mild upward pressure
                fair_values[symbol] += 0.2 * trade.quantity
    return fair_values

# GM spread decomposition: spread = 2 × adverse_selection_component
# At TTE=4, with Mark 22 active: adverseselection_comp ≈ 1-2 ticks
# Recommended: if Mark 22 present in last 5 ticks, add +2 to ask, +2 to bid (widen)
def adverseselection_spread_adj(mark22_recent_count):
    return min(3, mark22_recent_count)  # additional ticks of spread width
```

## Downstream Use

- Strategy: when Mark 22 is the active seller of a VEV strike, the GM-optimal
  response is to widen or remove our bid at that strike.
- Spec: maintain a `mark22_active` boolean per symbol per tick. Gate all
  aggressive buys on NOT mark22_active.
- Validation: compute realized markout conditional on Mark 22 presence vs absence.
  Theory predicts markout is significantly worse when Mark 22 is selling.
