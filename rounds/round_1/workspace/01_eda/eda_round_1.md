# EDA — Round 1

## Status

READY_FOR_REVIEW

Review outcome: not reviewed.

## Product Scope

| Product | Present In Data | Usable Evidence | Likely Trader Scope | Decision |
| --- | --- | --- | --- | --- |
| `INTARIAN_PEPPER_ROOT` | yes | yes | likely | include for algorithmic trader; drift-tracking signal is strong but review pending |
| `ASH_COATED_OSMIUM` | yes | yes | likely | include for algorithmic trader; fixed fair value signal is strong but review pending |
| `DRYLAND_FLAX` | no historical price CSV rows | wiki/manual only | no bot scope | manual auction only |
| `EMBER_MUSHROOM` | no historical price CSV rows | wiki/manual only | no bot scope | manual auction only |

Product branches: analysis is kept in one canonical EDA file because the two algorithmic products have simple, separable behavior.

## Data Sources

| File | Rows | Days |
| --- | --- | --- |
| `rounds/round_1/data/raw/prices_round_1_day_-2.csv` | 20,000 total / 10,000 per product | -2 |
| `rounds/round_1/data/raw/prices_round_1_day_-1.csv` | 20,000 total / 10,000 per product | -1 |
| `rounds/round_1/data/raw/prices_round_1_day_0.csv` | 20,000 total / 10,000 per product | 0 |
| `rounds/round_1/data/raw/trades_round_1_day_-2.csv` | 773 | -2 |
| `rounds/round_1/data/raw/trades_round_1_day_-1.csv` | 760 | -1 |
| `rounds/round_1/data/raw/trades_round_1_day_0.csv` | 743 | 0 |

Prices file columns: `day;timestamp;product;bid_price_1..3;bid_volume_1..3;ask_price_1..3;ask_volume_1..3;mid_price;profit_and_loss`
Trades file columns: `timestamp;buyer;seller;symbol;currency;price;quantity`
Delimiter: semicolon. Timestamps run 0–999,900 in steps of ~100 per day.

## Data Quality And Filters

Prices files contain 10,000 rows per product per day. Some rows have an incomplete top-of-book or `mid_price = 0.0`.

| Day | Product | Rows | Both best bid/ask present | Missing best bid | Missing best ask | `mid_price = 0.0` |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| -2 | `INTARIAN_PEPPER_ROOT` | 10,000 | 9,216 | 413 | 387 | 16 |
| -1 | `INTARIAN_PEPPER_ROOT` | 10,000 | 9,219 | 415 | 383 | 17 |
| 0 | `INTARIAN_PEPPER_ROOT` | 10,000 | 9,253 | 388 | 380 | 21 |
| -2 | `ASH_COATED_OSMIUM` | 10,000 | 9,187 | 413 | 418 | 18 |
| -1 | `ASH_COATED_OSMIUM` | 10,000 | 9,225 | 398 | 394 | 17 |
| 0 | `ASH_COATED_OSMIUM` | 10,000 | 9,232 | 393 | 389 | 14 |

Interpretation caveat: spread and mid-based dispersion claims should be read as filtered book analyses using rows with usable bid/ask or positive mid data. The original EDA did not store a reusable command/script, so human review should confirm these filters before marking the phase `COMPLETED`.

## Feature Inventory

| Feature | Source | Meaning | Classification | Strategy Use | Stability | Notes / Caveats |
| --- | --- | --- | --- | --- | --- | --- |
| `mid_price` | raw | observed mid from CSV | predictive | center fair-value estimates | regime-dependent | rows with `mid_price = 0.0` need filtering |
| best bid/ask spread | derived from raw book | top-of-book execution width | execution/risk | choose quote width inside market spread | stable in sample | requires usable bid and ask rows |
| IPR drift rate | derived | slope of `mid_price` over timestamp | predictive | set `fair_value = day_start + t * 0.001` | stable in sample, unconfirmed live | estimated from 3 historical days |
| IPR residual to drift FV | derived | noise around drift fair value | execution/risk | size quote edge vs noise | unknown live | original EDA did not store reusable script |
| ACO deviation from 10,000 | derived | distance from fixed fair value proxy | predictive | quote around 10,000 and manage inventory | stable in sample, unconfirmed live | slow reversion means position risk |
| ACO lag autocorrelation | derived | persistence of deviation | execution/risk | avoid expecting instant reversion | regime-dependent | validation needed on live sample |

## Feature Engineering Notes

| Transformation Or Feature | Purpose | Result | Keep? | Next Validation |
| --- | --- | --- | --- | --- |
| IPR linear drift fit | test whether "steady" means predictable slope | worked; residual stdev small vs spread | yes | confirm live first ticks match slope scale |
| ACO fixed-FV deviation | test hidden fixed fair value around 10,000 | worked across 3 days | yes | confirm no live-day level shift |
| Spread distribution | estimate executable quote width | worked for both products | yes | check platform run fill/rejection behavior |
| ACO autocorrelation | test reversion speed | promising but not enough alone for aggressive reversion | maybe | validate inventory holding time in runs |

## Key Findings

---

### INTARIAN_PEPPER_ROOT

**Finding 1 — Linear drift, not stable.**
The mid price increases by exactly ~0.1 per 100-tick step (+1 per 1,000 timestamp units), sustained across all three days. This is **not** a mean-reverting or stable product — it has a predictable upward trend.

| Day | Start mid | End mid | Drift | Rate |
| --- | --- | --- | --- | --- |
| -2 | 9,998.5 | 11,001.5 | +1,003 | +0.1003 per 100 ticks |
| -1 | 10,998.5 | 11,998.0 | +999.5 | +0.1000 per 100 ticks |
| 0 | 11,998.5 | 13,000.0 | +1,001.5 | +0.1002 per 100 ticks |

Each day starts approximately 1,000 above the previous day's start.

**Finding 2 — Fair value formula.**
`fair_value(t) = day_start_price + t * 0.001`

Residuals from this formula (day 0): mean = +1.49, stdev = 2.36, max = +12.1, min = -9.2.
Noise is small relative to the ~12–14 market spread — the formula is accurate enough to trade from.

**Finding 3 — Market spread is 11–16 ticks, concentrated at 12–14.**

| Spread | Frequency |
| --- | --- |
| 12 | 22.2% |
| 13 | 23.0% |
| 14 | 17.2% |
| 11 | 11.1% |
| 15–18 | ~20% |

**Finding 4 — Order book depth.**
Typical first-level volume: ~11–12 units bid/ask. Second level present ~65% of ticks, ~20 units.

**Finding 5 — Trades.**
1,011 trades across 3 days. Prices span 9,995–13,005 (tracking the trend). Avg qty per trade: ~5 units. Max: 8 units. Buyer/seller not identified in logs.

**Hypothesis:** The wiki describes IPR as "steady" — this likely refers to the spread volatility and tick-by-tick noise being small, not the level being flat. The drift is a structural feature, not noise.

**Implication:** A static fair value will be wrong almost immediately. The strategy must track the drift.

---

### ASH_COATED_OSMIUM

**Finding 1 — Mean-reverts around 10,000 with tight dispersion.**
When both bid and ask sides are present (~92% of ticks), the mid price stays within ±23 of 10,000 across all three days.

| Day | Mean mid | Stdev | Max dev from 10k | Min dev from 10k |
| --- | --- | --- | --- | --- |
| -2 | 9,998.2 | 5.22 | +19 | -21 |
| -1 | 10,000.8 | 4.45 | +19 | -18 |
| 0 | 10,001.6 | 5.68 | +23 | -23 |

No cross-day trend. Each day mean is within 2 units of 10,000.

**Finding 2 — High autocorrelation (slow mean reversion).**

| Lag | Autocorr |
| --- | --- |
| 1 | 0.789 |
| 5 | 0.780 |
| 10 | 0.770 |
| 20 | 0.760 |
| 50 | 0.717 |

The process is persistent: if the price is currently 9,992, it is likely to stay near 9,992 for several ticks before reverting. This is consistent with an AR(1)-like process with mean = 10,000.

**Finding 3 — Market spread is predominantly 16.**

| Spread | Frequency |
| --- | --- |
| 16 | 63.7% |
| 18 | 12.5% |
| 19 | 12.7% |

**Finding 4 — Trades.**
1,265 trades across 3 days. Price range 9,979–10,026 (±26 from 10,000). Avg qty: ~5 units. Max: 10 units.

**Hypothesis (hidden pattern):** The "hidden pattern" hinted at in the wiki is likely that ASH_COATED_OSMIUM has a fixed, knowable fair value of 10,000 despite appearing volatile. The slow AR(1)-like reversion is predictable enough to market-make against.

**Implication:** Fair value = 10,000. Market-make tight. The slow reversion means positions may be held for several ticks — position management matters.

---

## Summary Table

| Product | Fair Value Model | Drift | Typical Spread | Key Risk |
| --- | --- | --- | --- | --- |
| `INTARIAN_PEPPER_ROOT` | `day_start + t * 0.001` | +0.1/100 ticks | 12–14 | Stale fair value loses edge immediately |
| `ASH_COATED_OSMIUM` | Fixed = 10,000 | None | 16 | Slow reversion means position can grow before P&L is realized |

---

## Conditional Patterns / Regimes

| Condition Or Regime | Dependent Features | Observed Behavior | Strategy Relevance | Confidence | Caveats |
| --- | --- | --- | --- | --- | --- |
| IPR timestamp progression | `mid_price`, timestamp, drift rate | fair value rises about 0.001 per timestamp unit | static FV should not be used | strong | live drift rate still needs confirmation |
| ACO deviation from 10,000 | `mid_price - 10000`, autocorrelation | deviations persist before reverting | use position skew; avoid over-aggressive reversion | medium | based on 3 historical days |
| Wide enough top-of-book spread | best bid/ask spread | spreads exceed residual/noise estimates | market making has plausible edge | medium | fill behavior must be validated on platform |

## Signal Hypotheses

| Signal | Feature Dependencies | What It Means | Why It Matters | Strategy Use | Stability | Confidence | Limitations / Caveats |
| --- | --- | --- | --- | --- | --- | --- | --- |
| IPR drift fair value | timestamp, first usable mid, drift rate | fair value moves upward predictably | quoting around stale mid loses edge | drift-tracking market maker | stable in sample, unknown live | live slope/start price must be checked |
| ACO fixed fair value | mid deviation from 10,000, spread, autocorrelation | price oscillates around 10,000 | quoting around 10,000 can capture spread | fixed-FV market maker with inventory skew | stable in sample, regime-dependent live | slow reversion can create inventory pressure |

## Open Questions

- What is `day_start_price` for the live round? The bot needs to observe the first mid price at t=0. If t=0 data is unavailable, use first available mid.
- Does the drift rate (0.001/tick) hold exactly in the live round, or is it approximate? Current evidence: residuals stdev 2.36 — small but present. Treat as an estimate, not a guarantee.
- Is the ACO fair value exactly 10,000 or does it have a slow multi-day drift? All three historical days show mean within 2 units — treat as 10,000 for now.

---

## Downstream Use / Agent Notes

- **Strong enough to consider:** IPR drift fair value and ACO fixed fair value, with review caveat.
- **Exploratory only:** ACO autocorrelation as a timing signal; use it for risk/inventory reasoning before using it for aggressive directional entry.
- **Do not use yet:** static IPR fair value; aggressive ACO mean-reversion without inventory controls.
- **Additional validation needed:** confirm live IPR slope/start price, confirm ACO live level near 10,000, validate fill/rejection behavior on platform.
- **Understanding phase:** use these findings as the factual basis. Label drift rate and fair value as evidence-based estimates, not confirmed rules.
- **Strategy phase:** IPR -> drift-tracking market maker. ACO -> fixed-fair-value market maker.
- **Specification:** cite the signal hypotheses above and preserve missing-signal behavior.
- **Implementation:** IPR needs timestamp access and a first-tick initializer. ACO can use a hardcoded fair value with position skew.
