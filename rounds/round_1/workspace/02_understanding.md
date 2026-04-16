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
- Evidence: mid price drifts linearly upward at +0.001 per timestamp unit (+1 per 1,000 units, +~1,003 per day) across all 3 historical days. Day-start prices: ~9,999 / ~10,999 / ~11,999. Each day starts exactly +1,000 above the previous day's start. Consistent across days.
- Evidence: fair value formula `fv(t) = day_start_price + t * 0.001` fits with residual stdev 2.36 against a market spread of 12–14. Signal-to-noise ratio ≈ 5–6x. The formula is accurate enough to trade from.
- Evidence: market bots quote a spread of 12–14 ticks at first level, ~11–12 units per side. Second level present ~65% of ticks at ~20 units.
- Evidence: 1,011 trades across 3 days, avg qty ~5 units, max 8 units.
- Hypothesis: "quite steady" in the wiki refers to the drift *rate* being stable and predictable, not to the price level being flat. The product trends upward at a constant rate.
- Hypothesis: the drift rate will hold in the live round at approximately 0.001/tick. It is an evidence-based estimate, not a guaranteed constant.

**Critical strategic implication — why directional dominates market-making:**

The EDA recommends a "drift-tracking market maker" for IPR. This recommendation does not compare P&L magnitudes. The comparison below shows directional is 4–8x better:

| Strategy | Average position | Drift gain (per run) | Spread income (per run) | Total (approx) |
| --- | --- | --- | --- | --- |
| Directional max-long (buy 80, hold) | +80 all day | 80 × ~90 ticks ≈ 7,200 | ~0 (no selling) | ~7,200+ |
| Drift-tracking market maker | ~0 (buys and sells evenly) | ~0 (position averages out) | ~1,000–2,000 | ~1,000–2,000 |

A drift-tracking market maker sells at ask quotes as price rises. Each sell order offsets a unit of long inventory, surrendering future drift gain in exchange for the bid-ask spread. With drift this large relative to spread (5–6x signal-to-noise), every sell is a losing trade in expectation. The correct IPR strategy is: buy 80 units ASAP and hold.

**Inter-day carry insight:** Historical data shows each new live day starts +1,000 above the previous day's close. If the live round spans multiple days and positions carry over, a max-long position accumulates an additional +1,000 per carried unit per day on top of intraday drift.

---

**ASH_COATED_OSMIUM**

- Fact: position limit 80, algorithmic product. Wiki hints it "may follow a hidden pattern."
- Evidence: mid price mean-reverts around 10,000 across all 3 days. Stdev 4–5 when both order book sides present. Max deviation ±23 from 10,000 over 3 days. Each day's mean is within 2 units of 10,000.
- Evidence: autocorrelation at lag 1 = 0.789, lag 5 = 0.780, lag 10 = 0.770, lag 20 = 0.760, lag 50 = 0.717.
- Evidence: market spread predominantly 16 ticks (63.7% of ticks), half-spread 8.
- Hypothesis: the "hidden pattern" hinted at in the wiki is that ASH_COATED_OSMIUM has a fixed, knowable fair value of 10,000. The slow AR-like reversion is predictable enough to market-make against.
- Hypothesis: fair value 10,000 holds across live days. No cross-day drift observed in 3 days of history.

**ACO autocorrelation analysis — persistence is far stronger than AR(1):**

A pure AR(1) with coefficient φ = 0.789 predicts:
- Autocorr at lag 50 = 0.789^50 ≈ 0.000001 (effectively zero)
- Half-life of deviation = -ln(2) / ln(0.789) ≈ 2.9 ticks

The EDA observes autocorr 0.717 at lag 50. This is dramatically higher than the AR(1) prediction. The ACO price process is not a simple AR(1) — it is far more persistent. Practical consequences:

1. Deviations from 10,000 can persist for tens to hundreds of ticks, not 3.
2. A position accumulated during a prolonged dip (price stuck near 9,980 for 50+ ticks) will not unwind quickly via natural reversion.
3. Inventory management is the critical risk for this product.

**Inventory risk quantification:**
- Scenario: price stuck at 9,980 (−20 from FV). Our bid at 9,995. Every incoming market sell fills us.
- At ~5 units avg per fill: 8 consecutive fills → +40 units, 50% of position limit.
- If this lasts 100 ticks (plausible given lag-50 autocorr = 0.717), we are at or near limit before price reverts.
- Mitigation: one-sided quoting — when position > 40, suppress the bid (stop buying). When position < −40, suppress the ask (stop selling). This caps inventory accumulation while still capturing spread on the other side.

---

**Manual Products**

- Fact: DRYLAND_FLAX guaranteed buyback 30/unit, no fee. EMBER_MUSHROOM guaranteed buyback 20/unit, fee 0.10/unit (net 19.90).
- Fact: Exchange Auction format — single limit order per product, clearing price maximizes volume, ties broken by higher price, player submits last.
- Hypothesis: buying below the guaranteed buyback price is risk-free profit if filled. The buyback floor sets the minimum profitable price.

## Evidence Synthesis

| Claim Or Observation | Source | Evidence Strength | Decision Impact | What Would Change This |
| --- | --- | --- | --- | --- |
| IPR drifts +0.001/tick linearly | EDA (3 days, consistent) | strong | high — determines entire strategy class | Drift absent or different rate in live round |
| IPR directional strategy dominates drift-tracking MM | EDA magnitude analysis (80 × ~90 ≈ 7,200 >> ~1,000–2,000) | strong | high — buy max long, never sell | Drift stops or spread income dramatically increases |
| IPR inter-day carry: each day starts +1,000 above previous | EDA (3 days, consistent) | strong | medium — reinforces holding across days | Day-start prices diverge from +1,000 pattern in live round |
| IPR fair value = `day_start + t*0.001` with residual stdev 2.36 | EDA | strong | low for directional (no quoting needed) | Useful only as secondary reference |
| ACO fair value = 10,000, stdev 4–5 | EDA (3 days, consistent) | strong | high — sets quoting center | Cross-day drift appearing in live round |
| ACO persistence is far stronger than AR(1) φ=0.789 predicts | EDA autocorr lag-50 = 0.717 vs predicted ≈ 0 | strong | high — positions can accumulate for 100+ ticks | Faster reversion observed in live data |
| ACO market spread = 16 dominant | EDA | strong | medium — sets target quoting spread | Spread widens significantly in live round |
| DRYLAND_FLAX buyback 30, no fee | Wiki fact | strong | medium — sets manual floor | None — this is a stated fact |
| EMBER_MUSHROOM buyback 20, fee 0.10 | Wiki fact | strong | medium — sets manual floor | None — this is a stated fact |

## Strategy-Relevant Insights

| Insight | Linked EDA Signals | Feature Evidence | Regime Assumptions | Confidence | Strategy Impact |
| --- | --- | --- | --- | --- | --- |
| IPR directional max-long dominates all market-making approaches | EDA drift magnitude (+1,003/day) + magnitude comparison | drift rate and position limit | drift rate remains close to historical sample | high | buy 80 units ASAP, hold all day, never sell |
| ACO should trade from fixed FV 10,000 with inventory skew | EDA ACO fixed fair value + persistent deviations | mid deviation from 10,000, spread, lag autocorrelation | live level remains around 10,000 | high for FV, medium for timing | fixed-FV market maker; one-sided quoting when position > 40 |
| ACO positions can persist for 100+ ticks due to process memory | EDA lag-50 autocorr = 0.717 vs AR(1) prediction ≈ 0 | lag autocorrelation function profile | price persistence continues in live round | medium | must cap inventory via one-sided quoting |
| Manual products are outside bot implementation | round wiki manual auction facts | guaranteed buyback and fee rules | manual auction format unchanged | high | human bid decision only |

## What Should Be Tried

| Candidate Direction | Supporting Insight | Product Scope | Why Try It | Validation Needed |
| --- | --- | --- | --- | --- |
| Directional max-long | IPR drift magnitude makes this 4–8x better than market-making | `INTARIAN_PEPPER_ROOT` | 80 × ~90 ≈ 7,200 >> spread income from MM; no selling means full drift capture | verify position reaches +80 within first few ticks; monitor P&L against drift prediction |
| Fixed-FV market maker with position skew and one-sided quoting | ACO fixed FV 10,000 + persistent deviations | `ASH_COATED_OSMIUM` | stable center and wide spread create market-making edge; one-sided quoting prevents runaway inventory | live level check; inventory/position validation in platform run |
| Combined independent trader | both product signals | IPR + ACO | products are independent and both have low implementation cost | validate individually before combining |

## What Should Not Be Trusted

| Signal Or Claim | Why Not Trusted | Risk If Used | Next Validation |
| --- | --- | --- | --- |
| Drift-tracking market maker for IPR | EDA magnitude: drift gain ≈ 0 for MM (position averages ~0); directional earns 4–8x more | leaves most drift gain on table | discard permanently unless drift rate drops dramatically |
| Static IPR fair value | contradicted by EDA drift | quotes become stale immediately | do not use |
| Aggressive ACO directional reversion (mean-reversion entry) | high lag-50 autocorr shows price can stay deviated 100+ ticks | position accumulates and does not unwind quickly | validate with inventory-aware run before using |
| Historical spread as guaranteed fill behavior | spread observed in samples, not platform guarantee | quote placement may not fill or may reject | platform validation |

## Confidence And Impact

- Overall confidence: `high` for fair value models and IPR directional strategy; `medium` for exact ACO spread/parameter choices.
- Highest-impact implication: IPR requires a *directional* strategy, not a market maker. The EDA's own "drift-tracking MM" recommendation does not account for the 4–8x P&L advantage of staying long.
- Second-highest-impact implication: ACO deviations persist far longer than a simple AR(1) suggests. One-sided quoting is required to prevent limit accumulation.
- Main caveat: all parameter estimates come from 3 days of historical data. Live round behavior may differ. Implementation must allow parameter adjustment without structural changes.

## Assumptions

- Drift rate of +0.001/tick is stable in the live round (supported by 3 consistent days; treat as tunable).
- ASH_COATED_OSMIUM fair value = 10,000 in the live round (supported by 3 days with mean within 2 of 10,000).
- Market bots quote similar spreads in the live round as in historical data.
- Position limits (80 each) apply as stated.
- The `state.timestamp` field is accessible in `run()` and represents the same time scale as the CSV data.

## Open Questions

- What is `day_start_price` for IPR at the start of the live round? Needed only if drift-tracking is used as a secondary reference. For directional strategy, only need to know when bot reaches position limit.
- Does the drift rate reset or continue across multiple live round days? Historical evidence: each day starts +1,000 above prior → appears to reset per day (same rate, new start).
- Manual: how are other participants likely to bid? (Unknown. Use guaranteed buyback floor as anchor.)
- What exactly makes ACO autocorrelations so flat (0.789 at lag 1, 0.717 at lag 50)? Inconsistent with simple AR(1). Investigate in live data.

## Open Risks And Unknowns

| Risk Or Unknown | Affects | Severity | Mitigation Or Next Action |
| --- | --- | --- | --- |
| Live IPR drift differs from historical estimate | strategy performance | medium | observe first live ticks; verify drift direction and magnitude |
| ACO live fair value shifts away from 10,000 | strategy/validation | medium | inspect early live mids; pause if mean deviation > 10 |
| ACO position accumulation before reversion | implementation/P&L | high | implement one-sided quoting when \|position\| > 40 |
| Platform validation rejects orders or hits limits | implementation/validation | high | run canonical bot validation before submission |
| Ingestion/EDA/understanding/strategy review debt remains | final submission readiness | medium | human review before final ready state |

## Prioritized Unknowns

| Unknown | Affects | Priority | Next Action |
| --- | --- | --- | --- |
| Live round IPR drift rate | Strategy performance | medium | Observe first ~100 ticks; verify drift is active |
| Live round ACO fair value | Strategy performance | low | Observe first ~100 ticks; confirm mean-reversion around 10,000 |
| ACO position persistence in live round | Inventory risk | medium | Monitor position every 100 ticks in platform run |
| Manual auction other participants' bids | Manual P&L | medium | Bid near (but below) buyback floor; accept uncertainty |

## Strategy Implications

- **IPR:** Directional max-long. Buy 80 units as fast as possible by sweeping all ask levels. Place a resting bid above best bid to attract remaining sellers. Never sell. Hold until end of day. Expected P&L: 80 × ~90 price ticks (per sim run) ≈ 7,200+. No fair-value tracking needed.
- **ACO:** Market maker around fixed FV = 10,000. Quote inside the 16-tick bot spread (half-spread = 5 recommended). Proportional position skew on both bid and ask: `skew = round((position / pos_limit) * SKEW_FACTOR)`. One-sided quoting when |position| > 40: suppress bid when long > 40, suppress ask when short < −40. Position limit 80.
- **Manual:** DRYLAND_FLAX bid ≤ 29. EMBER_MUSHROOM bid ≤ 19.80 (net profit ≥ 0.10/unit after fee). Human platform action, not bot code.
- **Combined submission:** Both algorithmic strategies run in the same `Trader.run()`. No interaction between products.

## Next Action

- Human review needed: approve, approve with caveats, or request corrections.
- If review changes material assumptions, update downstream strategy/spec artifacts before final submission readiness.
