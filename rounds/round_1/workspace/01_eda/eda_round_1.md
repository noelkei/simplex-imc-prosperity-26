# EDA — Round 1

## Status

COMPLETED

## Data Sources

| File | Rows | Days |
| --- | --- | --- |
| `rounds/round_1/data/raw/prices_round_1_day_-2.csv` | 10,000 | -2 |
| `rounds/round_1/data/raw/prices_round_1_day_-1.csv` | 10,000 | -1 |
| `rounds/round_1/data/raw/prices_round_1_day_0.csv` | 10,000 | 0 |
| `rounds/round_1/data/raw/trades_round_1_day_-2.csv` | — | -2 |
| `rounds/round_1/data/raw/trades_round_1_day_-1.csv` | — | -1 |
| `rounds/round_1/data/raw/trades_round_1_day_0.csv` | — | 0 |

Prices file columns: `day;timestamp;product;bid_price_1..3;bid_volume_1..3;ask_price_1..3;ask_volume_1..3;mid_price;profit_and_loss`
Trades file columns: `timestamp;buyer;seller;symbol;currency;price;quantity`
Delimiter: semicolon. Timestamps run 0–999,900 in steps of ~100 per day.

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

## Open Questions

- What is `day_start_price` for the live round? The bot needs to observe the first mid price at t=0. If t=0 data is unavailable, use first available mid.
- Does the drift rate (0.001/tick) hold exactly in the live round, or is it approximate? Current evidence: residuals stdev 2.36 — small but present. Treat as an estimate, not a guarantee.
- Is the ACO fair value exactly 10,000 or does it have a slow multi-day drift? All three historical days show mean within 2 units — treat as 10,000 for now.

---

## Downstream Use

- **Understanding phase:** Use these findings as the factual basis. Label drift rate and fair value as evidence-based estimates, not confirmed rules.
- **Strategy phase:** IPR → drift-tracking market maker. ACO → fixed-fair-value market maker.
- **Implementation:** IPR needs timestamp access and a first-tick initializer. ACO can use a hardcoded fair value with position skew.
