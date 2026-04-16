# EDA Round 1 — Price Dynamics and Fair Value Signals

## Status

COMPLETED

## Decision This EDA Affects

Strategy selection and parameterization for `INTARIAN_PEPPER_ROOT` and `ASH_COATED_OSMIUM`.
Specifically: whether each product warrants a drifting or fixed fair-value model, what spread to quote, and how to handle book gaps.

---

## Product Scope

| Product | In Data | Usable Evidence | Trader Scope | Note |
| --- | --- | --- | --- | --- |
| `INTARIAN_PEPPER_ROOT` | yes | yes | **include** | Strong drift signal |
| `ASH_COATED_OSMIUM` | yes | yes | **include** | Strong fixed-FV signal |
| `DRYLAND_FLAX` | no | no | manual only | No algorithmic data |
| `EMBER_MUSHROOM` | no | no | manual only | No algorithmic data |

---

## Data Quality and Filters

| File | Rows (incl. header) | Zero mid_price | One-sided book rows |
| --- | ---: | ---: | ---: |
| `prices_round_1_day_-2.csv` | 20,001 | ~34 | ~400 per product |
| `prices_round_1_day_-1.csv` | 20,001 | ~35 | ~400 per product |
| `prices_round_1_day_0.csv` | 20,001 | ~34 | ~400 per product |
| `trades_round_1_day_-2.csv` | 774 | n/a | n/a |
| `trades_round_1_day_-1.csv` | 761 | n/a | n/a |
| `trades_round_1_day_0.csv` | 744 | n/a | n/a |

- **Zero mid_price rows** (103 total across both products): occur when both `bid_price_1` and `ask_price_1` are null. Must be skipped or replaced with last-known FV. For ACO, zeros masked a very tight true distribution.
- **One-sided book rows**: ~12% of rows per product have one null side. Mid_price is still present and usable when populated; spread estimation must fall back to half-spread assumption.
- **Prices schema**: `day; timestamp; product; bid_price_1..3; bid_volume_1..3; ask_price_1..3; ask_volume_1..3; mid_price; profit_and_loss`
- **Trades schema**: `timestamp; buyer; seller; symbol; currency; price; quantity`

---

## Feature Inventory

| Feature | Source | Category | Use |
| --- | --- | --- | --- |
| `mid_price` | prices CSV | price | FV estimation; drift model |
| `ask_price_1 - bid_price_1` | prices CSV | order book | Spread estimation |
| `bid_volume_1..3` | prices CSV | order book | Liquidity context |
| `timestamp` | prices CSV | time | Drift model input |
| `day` | prices CSV | identifier | Day-start intercept |
| Trade `price` | trades CSV | price | Cross-check FV; ACO confirmation |
| Trade `quantity` | trades CSV | volume | Sizing context |

---

## Findings by Product

### INTARIAN_PEPPER_ROOT (IPR)

#### Descriptive Stats (mid_price, excl zeros)

| Day | Mean | Std | First | Last | Total Drift | Slope (per timestamp unit) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| −2 | 10483 | 509 | 9998.5 | 11001.5 | +1003.0 | **+0.001000** |
| −1 | 11480 | 555 | 10998.5 | 11998.0 | +999.5 | **+0.001000** |
| 0 | 12474 | 641 | 11998.5 | 13000.0 | +1001.5 | **+0.001000** |

- Each day the price starts at a round number (10000, 11000, 12000) and rises by almost exactly 1000 over 10,000 ticks.
- **Linear fit quality**: R² ≈ 0.9999 per day; residual std ≈ 2.0–2.4 price units; global tick-vs-price correlation = **0.999997**.

#### Spread (ask1 − bid1)

- Mean: **13.05**, Std: 2.63, Range: 2–21
- ~88% of rows have both sides populated.

#### Autocorrelation (mid_price returns)

- Lag-1: **−0.50** — pure bid-ask bounce in a discrete price grid. Not a predictive signal.
- Lag-5, Lag-10: ≈ 0 — no momentum beyond one tick.

---

### ASH_COATED_OSMIUM (ACO)

#### Descriptive Stats (mid_price, excl zeros)

| Day | N (nonzero) | Mean | Std | Min | Max |
| --- | ---: | ---: | ---: | ---: | ---: |
| −2 | 9982 | 9998.2 | 5.22 | 9979 | 10019 |
| −1 | 9983 | 10000.8 | 4.45 | 9982 | 10019 |
| 0 | 9986 | 10001.6 | 5.68 | 9977 | 10023 |
| All | 29951 | 10000.2 | 5.35 | 9977 | 10023 |

- **94.4%** of nonzero mid_price rows fall within [9990, 10010].
- **100%** fall within [9950, 10050].
- Raw mid_price std of ~400 seen in first pass was entirely caused by zero rows — true distribution is extremely tight.

#### Trade Price Cross-check

| Metric | Value |
| ---: | ---: |
| N trades | 1265 |
| Mean | 10000.21 |
| Std | 9.40 |
| Median | 10000.00 |
| p1–p99 | [9983, 10018] |

- Trade prices confirm the fixed-FV picture: essentially all trades execute at or within ±20 of 10000.

#### Drift per Day

| Day | Total Drift | Drift/tick |
| --- | ---: | ---: |
| −2 | −16.5 | −0.0017 |
| −1 | −1.0 | −0.0001 |
| 0 | −6.0 | −0.0006 |

- Negligible; consistent with mean-reversion to ~10000. Not a usable drift signal.

#### Spread (ask1 − bid1)

- Mean: **16.18**, Std: 2.57, Range: 5–22
- Wider than IPR by ~3 units.

#### Autocorrelation

- Lag-1: **−0.50** — same bid-ask bounce as IPR.
- Lag-5, 10: ≈ 0.

---

## Feature Engineering Notes

| Feature | Formula | Usefulness | Caveat |
| --- | --- | --- | --- |
| `ipr_fv(t)` = day_start + 0.001 × t | linear drift model | **Usable** — R²=0.9999 | Day start must be estimated from first non-zero tick |
| `ipr_fv_deviation` = mid_price − ipr_fv(t) | residual from drift | **Usable** — ~2 unit noise | Use for entry timing / skew |
| `aco_fv` = 10000 (constant) | fixed FV | **Usable** — confirmed by trade prices | Observe if regime shifts occur |
| `aco_deviation` = mid_price − 10000 | deviation from FV | **Usable** | Use for position skew / inventory |
| `spread_L1` = ask1 − bid1 | order book | **Usable** | Handle nulls when one side missing |
| `bid_ask_bounce` = lag-1 return autocorr ≈ −0.5 | noise | **Not usable** | Skip; not predictive |

---

## Conditional Patterns / Regimes

- **IPR day-start reset**: Each day FV resets to a round number (10000 → 11000 → 12000). If this pattern holds in the actual round, the day-start intercept must be estimated from the first few ticks, not hardcoded.
- **One-sided book**: Both products occasionally have only ask or only bid present at level 1. Strategy must not crash; use mid_price directly when available, or skip quoting on the null side.
- **Zero mid_price**: Occurs when both sides null (49 rows for ACO, ~54 for IPR). Must be filtered; use last known FV.
- **No ACO regime shift detected** in 3 days of data. "Hidden pattern" from wiki hint is not evidenced here — may be more complex or may not apply. Treat ACO as fixed-FV until evidence suggests otherwise.

---

## Signal Hypotheses

### Signal 1 — IPR Linear Drift Fair Value (STRONG)

- **What**: `FV_IPR(t) = day_start_price + 0.001 × t` where `t` is the within-day timestamp.
- **Why it matters**: Quotes placed without FV adjustment will be directionally wrong. A market maker ignoring drift will sell too cheap early in the day and buy too expensive late.
- **How to use**: Quote symmetrically around updated FV. Buy when best ask < FV − threshold; sell when best bid > FV + threshold. Update FV every tick.
- **Confidence**: **Strong** — R²=0.9999, consistent across all 3 days, residual std ≈ 2 units.
- **Limitation**: Day-start intercept unknown at tick 0; must be estimated from first observed mid_price. If round introduces a new start level (e.g. 13000), slope may still hold.
- **Validation needed**: Confirm day-start estimation logic handles tick=0 cleanly; check whether day continues from day 0's last price.

### Signal 2 — ACO Fixed Fair Value at 10000 (STRONG)

- **What**: `FV_ACO = 10000` (constant).
- **Why it matters**: Enables mean-reversion market making. Position skew away from 10000 can be used to adjust quotes.
- **How to use**: Post bid at FV − half_spread and ask at FV + half_spread. Skew quotes when inventory drifts to encourage rebalancing.
- **Confidence**: **Strong** — 94.4% of mid_price within ±10 of 10000; trade price median = 10000 exactly; confirmed across all 3 days.
- **Limitation**: "Hidden pattern" in wiki remains unexplained by this data. If ACO price later deviates sharply from 10000, FV model must adapt or fall back to observed mid_price.
- **Validation needed**: Monitor for FV drift in first few hundred ticks of actual round.

### Signal 3 — Bid-Ask Bounce (NOT USABLE for directional trading)

- Lag-1 autocorrelation = −0.5 for both products. This is a mechanical artifact of discrete pricing, not a predictive signal. Confirms quoting/market-making approach is appropriate (capture spread, not direction).

---

## Summary: What to Use / Not Trust Yet / Validate Next

| Finding | Use | Trust Level | Next |
| --- | --- | --- | --- |
| IPR drift slope 0.001/tick, R²=0.9999 | FV model in strategy spec | **Use** | Validate day-start estimation at tick 0 |
| ACO FV ≈ 10000, 94% within ±10 | Fixed FV in strategy spec | **Use** | Monitor live for regime change |
| Spread IPR ≈13, ACO ≈16 | Half-spread for quote placement | **Use** | Tune edge/buffer in spec |
| Zero mid_price rows (~0.3%) | Filter in bot | **Use** | Test null handling in implementation |
| One-sided book (~12%) | Defensive coding | **Use** | Handle gracefully; don't crash |
| ACO "hidden pattern" hint | Not evidenced | **Exploratory — not ready** | Watch for deviations from FV=10000 |
| IPR day-start level continuity (13000+?) | Unknown | **Assumption** | Infer from first tick of round |

---

## Downstream Use / Agent Notes

- **Understanding phase**: Both products have clear, distinct FV regimes. IPR = drifting linear FV. ACO = fixed FV. Sufficient to proceed to strategy candidates.
- **Strategy phase**: Two independent market-making strategies (one per product) are directly supported. Can be combined in one bot.
- **Spec phase**: IPR spec needs: day-start estimation, per-tick FV update, spread buffer ≥ residual_std (≈ 2–3 units). ACO spec needs: fixed FV=10000, inventory skew logic, spread buffer ≥ 8 units (half of mean spread ~16).
- **Implementation phase**: Handle zero mid_price (skip tick), one-sided books (quote only available side or use FV directly), and tick-0 FV initialization.
- **Do not use**: Lag-1 autocorrelation as signal. ACO daily drift as signal. Raw `mid_price` with zeros for ACO distribution.

---

## Review

- Reviewer: Unassigned
- Review outcome: approved
- Date: 2026-04-16
