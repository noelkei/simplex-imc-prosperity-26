# Understanding Summary

## Status

READY_FOR_REVIEW

## Sources

- Wiki facts: `docs/prosperity_wiki/rounds/round_1.md`, `docs/prosperity_wiki/trading/01_exchange_mechanics.md`, `docs/prosperity_wiki/trading/02_orders_and_position_limits.md`
- EDA evidence: `rounds/round_1/workspace/01_eda/eda_round_1.md`
- Ingestion: `rounds/round_1/workspace/00_ingestion.md`
- Playbook heuristics: not used as evidence

## Current Understanding

**INTARIAN_PEPPER_ROOT**

- Fact: position limit 80, algorithmic product.
- Fact: wiki describes it as "quite steady" and "hardy, slow-growing root."
- Evidence: mid price drifts linearly upward at +0.001 per timestamp unit (+1 per 1,000 units, +~1,000 per day) across all 3 historical days. Day-start prices: ~10,000 / ~11,000 / ~12,000. Consistent across days.
- Evidence: fair value formula `fv(t) = day_start_price + t * 0.001` fits with residual stdev 2.36 against a market spread of 12–14. The formula is accurate enough to trade from.
- Evidence: market bots quote a spread of 12–14 ticks at first level, ~11–12 units per side.
- Hypothesis: "quite steady" in the wiki refers to the drift *rate* being stable and predictable, not to the price level being flat. The product trends upward at a constant rate.
- Hypothesis: the drift rate will hold in the live round at approximately 0.001/tick. It is an evidence-based estimate, not a guaranteed constant.

**ASH_COATED_OSMIUM**

- Fact: position limit 80, algorithmic product. Wiki hints it "may follow a hidden pattern."
- Evidence: mid price mean-reverts around 10,000 across all 3 days. Stdev 4–5 when both order book sides present. Max deviation ±23 from 10,000 over 3 days.
- Evidence: autocorrelation at lag 1 = 0.79 — the process is locally persistent (slow reversion), consistent with AR(1) mean = 10,000.
- Evidence: market bots quote a spread of 16 ticks (64% of ticks) at first level, ~14 units per side.
- Hypothesis: the "hidden pattern" is that ASH_COATED_OSMIUM has a knowable fair value of 10,000 despite short-term volatility. The name and wiki description are misleading — this is actually the more stable product by price level.
- Hypothesis: fair value 10,000 holds across live days. No cross-day drift observed in 3 days of history.

**Manual Products**

- Fact: DRYLAND_FLAX guaranteed buyback 30/unit, no fee. EMBER_MUSHROOM guaranteed buyback 20/unit, fee 0.10/unit (net 19.90).
- Fact: Exchange Auction format — single limit order per product, clearing price maximizes volume, ties broken by higher price, player submits last.
- Hypothesis: buying below the guaranteed buyback price is risk-free profit if filled. The buyback floor sets the minimum profitable price.

## Evidence Synthesis

| Claim Or Observation | Source | Evidence Strength | Decision Impact | What Would Change This |
| --- | --- | --- | --- | --- |
| IPR drifts +0.001/tick linearly | EDA (3 days, consistent) | strong | high — determines entire strategy class | Drift absent or different rate in live round |
| IPR fair value = `day_start + t*0.001` with residual stdev 2.36 | EDA | strong | high — sets quoting center | Large residuals in live round |
| ACO fair value = 10,000, stdev 4–5 | EDA (3 days, consistent) | strong | high — sets quoting center | Cross-day drift appearing in live round |
| ACO autocorr 0.79 (slow reversion) | EDA | medium | medium — affects position holding time | Fast reversion observed in live data |
| ACO market spread = 16 dominant | EDA | strong | medium — sets target quoting spread | Spread widens significantly in live round |
| IPR market spread = 12–14 dominant | EDA | strong | medium — sets target quoting spread | Spread widens significantly in live round |
| DRYLAND_FLAX buyback 30, no fee | Wiki fact | strong | medium — sets manual floor | None — this is a stated fact |
| EMBER_MUSHROOM buyback 20, fee 0.10 | Wiki fact | strong | medium — sets manual floor | None — this is a stated fact |

## Confidence And Impact

- Overall confidence: `high` for fair value models; `medium` for exact spread/parameter choices.
- Highest-impact implication: IPR requires a drift-tracking fair value. A static mid-price will be wrong within seconds and the bot will lose edge continuously.
- Main caveat: all parameter estimates come from 3 days of historical data. Live round behavior may differ. Implementation must allow parameter adjustment without structural changes.

## Assumptions

- Drift rate of +0.001/tick is stable in the live round (supported by 3 consistent days; treat as tunable).
- ASH_COATED_OSMIUM fair value = 10,000 in the live round (supported by 3 days with mean within 2 of 10,000).
- Market bots quote similar spreads in the live round as in historical data.
- Position limits (80 each) apply as stated.
- The `state.timestamp` field is accessible in `run()` and represents the same time scale as the CSV data.

## Open Questions

- What is `day_start_price` for IPR at the start of the live round? (Observe first available mid price.)
- Does the drift rate reset or continue across multiple live round days?
- Manual: how are other participants likely to bid? (Unknown. Use guaranteed buyback floor as anchor.)

## Prioritized Unknowns

| Unknown | Affects | Priority | Next Action |
| --- | --- | --- | --- |
| Live round IPR drift rate | Strategy performance | medium | Observe first ~100 ticks; verify drift is active |
| Live round ACO fair value | Strategy performance | low | Observe first ~100 ticks; confirm mean-reversion around 10,000 |
| Manual auction other participants' bids | Manual P&L | medium | Bid near (but below) buyback floor; accept uncertainty |

## Strategy Implications

- **IPR:** Market maker tracking `fv(t) = day_start_price + t * 0.001`. Quote inside the 12–14 bot spread. Position limit 80. Must initialize `day_start_price` on first tick.
- **ACO:** Market maker around fixed FV = 10,000. Quote inside the 16-tick bot spread. Position limit 80. Slow reversion means position can accumulate — need position skew logic.
- **Manual:** DRYLAND_FLAX bid ≤ 29. EMBER_MUSHROOM bid ≤ 19.80 (net profit ≥ 0.10/unit after fee). Human platform action, not bot code.
- **Combined submission:** Both algorithmic strategies run in the same `Trader.run()`. No interaction between products.

## Next Action

- Write strategy candidates for IPR drift market maker and ACO fixed-FV market maker.
- Human decision needed: review shortlist before spec is written.

