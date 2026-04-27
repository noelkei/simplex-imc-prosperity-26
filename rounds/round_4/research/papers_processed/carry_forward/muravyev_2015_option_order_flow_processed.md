# Processed Paper Summary: Muravyev (2015)

## Status

`draft`

## Round 4 Role

- Reference class: `carry-forward reference`
- Priority for Strategy: below the top-level `round4_raw_derived` processed core
- Allowed use: order-flow framing, validation cross-checks, and counterparty-context interpretation
- Caution: parts of this note were written before the full `round_4` raw-derived paper core existed, so treat it as supporting context rather than as the primary driver

## Paper Metadata

- Paper ID: `muravyev_2015_option_order_flow`
- Title: `Order Flow and Expected Option Returns`
- Authors: Dmitriy Muravyev
- Year: 2015
- Markdown file: `../../../round_3/research/papers_md/muravyev_2015_order_flow_and_expected_option_returns.md`
- Link: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1963865

## Core Claim

Option order flow contains economically meaningful information because market
makers absorb inventory shocks and reprice risk. The paper decomposes trade
price impact into information and inventory components, finding that **inventory
risk dominates asymmetric information** in option markets. Order imbalance is
the strongest predictor of future option returns among 50+ predictors tested.

Key decomposition:
- price response at the trading exchange = information impact + inventory impact
- price response at non-trading exchanges = information impact only
- Empirical finding: inventory impact ≈ 2× information impact per trade

## Assumptions

- Prosperity top-of-book imbalance is a proxy for the signed option-trade flow.
- Voucher symbols share enough underlying-driven risk that family-level inventory
  pressure is more informative than isolated per-symbol imbalance.
- In Round 4, counterparty identity (`Trade.buyer`, `Trade.seller`) gives us a
  BETTER signal than raw imbalance — directly identifying who is creating pressure.

## Problem Addressed for Round 4

- Round 4 introduces named counterparties. Mark 22 is a near-deterministic OTM
  seller; Mark 01 is their buyer counterpart in an artificial loop. This is
  precisely the kind of structured inventory flow the paper analyzes.
- We now have richer order-flow information than Round 3 ever had:
  not just "who is on which side" but "which known participant."
- The paper warns imbalance alone weakens near expiry (TTE=4 is deep near-expiry).
  The **counterparty identity signal is more robust** than raw imbalance here
  because it is structurally motivated, not return-predictive.

## What This Paper Gives Us

- Framing: imbalance is an inventory-pressure signal, not directional alpha.
  This is why counterparty veto (Mark 22 = no-buy) outperforms raw imbalance.
- Formula (order imbalance):
  ```
  OrdImb = (#BuyTrades - #SellTrades) / #Trades
  ```
- Market-wide insight: family-level imbalance across VEV_5000–5500 carries more
  information than per-symbol imbalance for correlated vouchers.
- Expiration finding: negative imbalance spikes near expiry (TTE→0). This
  supports caution on new shorts as TTE=4 decreases further in Round 5+.

## Relevance To Round 4

| Signal / Risk / Question | Relevance | Strength | Caveat |
|:--|:--|:--|:--|
| Mark 22 near-deterministic OTM seller | strongest direct application in R4 | high | now better than raw imbalance |
| Mark 01 / Mark 22 loop is artificial | avoid participating; structural not alpha | high | loop identified in EDA |
| Imbalance weakens near expiry | confirms counterparty signal > raw imbalance at TTE=4 | medium | paper studies listed equity options |
| Family-level pressure across VEV_5200–5400 | aggregate short-vol position creates family pressure | medium | single-exchange Prosperity |

## Action Classification

`promote` — counterparty-identity framing directly upgrades this paper's
inventory-pressure lens to Round 4. The Mark 22 veto is the operational form.

## Implementation Notes

```python
# Round 4 counterparty-aware imbalance gate
# Applied to state.market_trades per tick
def check_counterparty_danger(market_trades, symbol):
    """Return True if Mark 22 is selling this symbol this tick."""
    for trade in market_trades.get(symbol, []):
        if trade.seller == "Mark 22":
            return True  # hard no-buy signal
    return False

# Family-level imbalance (secondary signal)
def family_imbalance(order_depths, active_strikes):
    total_bid = sum(sum(order_depths[s].buy_orders.values())
                    for s in active_strikes if s in order_depths)
    total_ask = sum(sum(order_depths[s].sell_orders.values())
                    for s in active_strikes if s in order_depths)
    total = total_bid + total_ask
    return (total_bid - total_ask) / total if total > 0 else 0.0
```

## Downstream Use

- Strategy: Mark 22 seller-state is the operationalized form of "structured
  inventory pressure." Treat it as a hard entry veto for VEV_5200+.
- Spec: check `Trade.seller == "Mark 22"` in market_trades before any aggressive
  buy order on VEV_5200–6500. Log counterparty state to traderData.
- Validation: track how often Mark 22 is active per tick; monitor markout after
  trades on ticks where Mark 22 is NOT present.
