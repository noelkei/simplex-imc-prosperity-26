# EDA Strategy Expansion Feature Lab

## Status

READY_FOR_REVIEW

## Question

- Question: Which engineered features and transformations are useful enough to expand Round 1 strategy candidates beyond the existing fair-value baseline?
- Product scope: `INTARIAN_PEPPER_ROOT` and `ASH_COATED_OSMIUM`.
- Why this matters downstream: Strategy generation needs conceptually different approaches, not only parameter variants of the same fair-value market maker.

## Product Scope

| Product | Present In Data | Usable Evidence | Likely Trader Scope | Decision |
| --- | --- | --- | --- | --- |
| `INTARIAN_PEPPER_ROOT` | yes | yes | likely | include |
| `ASH_COATED_OSMIUM` | yes | yes | likely | include |

- Product-scope rationale: both products are Round 1 algorithmic products with position limit +/-80.
- Product branches: IPR has a strong linear drift FV; ACO has a stable fixed FV. Feature work should preserve this split.

## Data Sources

- Raw data: `rounds/round_1/data/raw/prices_round_1_day_{-2,-1,0}.csv`, `rounds/round_1/data/raw/trades_round_1_day_{-2,-1,0}.csv`
- Processed data: `rounds/round_1/data/processed/strategy_expansion_metrics.json`
- Reproduction script: `rounds/round_1/workspace/01_eda/strategy_expansion_analysis.py`
- External context: none.
- Run or log artifact: none.

## Data Quality And Filters

| Product | Price Rows | Valid Mid Rows | Zero Mid Rows | Both-Sided Rows | One-Sided Rows | Trade Rows |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `INTARIAN_PEPPER_ROOT` | 30000 | 29946 | 54 | 27688 | 2258 | 1011 |
| `ASH_COATED_OSMIUM` | 30000 | 29951 | 49 | 27644 | 2307 | 1265 |

- Timestamp coverage and gaps: three historical days, aligned by product and timestamp in the price files.
- Missing bid/ask: IPR has 1216 missing `bid_price_1` rows and 1150 missing `ask_price_1` rows; ACO has 1204 missing bid rows and 1201 missing ask rows.
- Filters applied: transformation and microstructure metrics use rows with nonzero `mid_price`; spread metrics require both best bid and best ask.
- Findings based on: mixed filtered rows, depending on feature availability.
- Data quality caveat: one-sided books are common enough to be an execution feature, not only a null-handling detail.

## Feature Inventory

| Feature | Source | Meaning | Classification | Strategy Use | Stability | Notes / Caveats |
| --- | --- | --- | --- | --- | --- | --- |
| `residual` | derived | `mid_price - FV` where FV is IPR drift or ACO fixed 10000 | predictive / execution | entry, skew, state buckets | stable historically | Depends on correct FV assumption |
| `log_residual_price_scaled` | derived | `log(mid/FV) * mid` | descriptive | normalize price moves if needed | stable historically | Numerically equivalent to raw residual here |
| `spread` | raw/derived | `ask_price_1 - bid_price_1` | execution/risk | quote width and skip logic | stable historically | Missing on one-sided rows |
| `relative_spread` | derived | spread divided by mid | descriptive | cross-product normalization | stable historically | Adds little because products trade near 10000-13000 |
| `imbalance_l1` | derived | L1 bid depth minus ask depth over total L1 depth | predictive / microstructure | execution scoring, quote skew | promising | May encode book construction and bounce |
| `imbalance_l3` | derived | L1-L3 bid depth minus ask depth over total depth | predictive / microstructure | smoother execution scoring | promising | Similar caveat as L1 imbalance |
| `buy_edge_best_ask` | derived | FV minus best ask | execution | immediate buy opportunity filter | sparse | Must respect capacity |
| `sell_edge_best_bid` | derived | best bid minus FV | execution | immediate sell opportunity filter | sparse | Must respect capacity |
| `one_sided` | raw/derived | one of best bid or ask missing | execution/risk | avoid crashes, special quoting state | stable historically | Not a directional signal alone |

## Feature Engineering Notes

| Transformation Or Feature | Purpose | Result | Keep? | Next Validation |
| --- | --- | --- | --- | --- |
| Raw residual vs log residual | Test whether log transform adds signal | Correlation is 1.000 for both products after price scaling | no as separate signal | Use raw residual in specs; keep log only for model experiments |
| IPR residual to drift FV | Recenter IPR around deterministic trend | residual std 2.20, median 1.50 | yes | Validate intercept logic in bot/backtest |
| ACO residual to 10000 | Recenter ACO around fixed FV | residual std 5.35, median 0.50 | yes | Monitor live/regime deviation |
| Best quote edge vs FV | Identify immediate edge opportunities | Sparse but directly executable | yes | Backtest fill/PnL impact with capacity clipping |
| L1/L3 imbalance | Test microstructure execution feature | Correlation with next residual delta about 0.64 for both products | maybe | Validate against fill model; beware bid-ask bounce |
| One-sided book flag | Treat missing side as state | Around 7.5%-7.7% of rows per product | yes | Define quote behavior per side |

## Analyses Run

- Reproduction command: `python3 rounds/round_1/workspace/01_eda/strategy_expansion_analysis.py`
- Output artifacts: `rounds/round_1/data/processed/strategy_expansion_metrics.json`
- Optional notebook: none.
- Descriptive stats: residual, spread, best-quote edge, data quality.
- Spread / microstructure checks: best ask/bid edge to FV by threshold; imbalance correlation with next residual delta.
- Correlation checks: raw-vs-log residual equivalence.

## Conditional Patterns / Regimes

| Condition Or Regime | Dependent Features | Observed Behavior | Strategy Relevance | Confidence | Caveats |
| --- | --- | --- | --- | --- | --- |
| Positive best-ask/best-bid edge | `buy_edge_best_ask`, `sell_edge_best_bid` | ACO has positive buy edge in 4.79% of valid rows and positive sell edge in 4.48%; IPR has 1.63% and 1.55% | Supports a microstructure scalper layer | medium | Positive edge to FV is not guaranteed fill-adjusted PnL |
| Strong edge > 5 | same | ACO buy/sell rows: 0.51%/0.59%; IPR buy/sell rows: 0.00%/0.08% | Use as high-confidence sweep trigger | medium | Sparse; not enough as only strategy |
| One-sided book | best bid/ask availability | About 7.5%-7.7% rows | Execution state and defensive handling | strong | Not directional by itself |
| High imbalance | `imbalance_l1`, `imbalance_l3` | Correlates with next residual delta around 0.64 | Candidate feature for scoring quotes | medium | Likely includes book mechanics and bid-ask bounce |

## Signal Hypotheses

| Signal | Feature Dependencies | What It Means | Why It Matters | Strategy Use | Stability | Confidence | Limitations / Caveats |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Raw residual is enough; log adds no separate edge | `residual`, `log_residual_price_scaled` | Log transform is near-identical at these price/deviation scales | Avoids unnecessary bot complexity | Use raw residual for fair value and Markov buckets | stable historically | If future products have multiplicative dynamics, revisit |
| Sparse immediate-edge scalping | `buy_edge_best_ask`, `sell_edge_best_bid`, `spread` | Some ticks offer best quotes meaningfully away from FV | Can exploit small margins without changing FV model | Sweep only when edge exceeds threshold and capacity remains | regime-dependent | Needs backtest with position and fill assumptions |
| Imbalance as execution score | `imbalance_l1`, `imbalance_l3`, residual delta | Book pressure may forecast short-horizon residual movement | Could improve quote placement and skew | Add to microstructure or linear-score candidate | unknown | Must not be mistaken for official rule |

## Assumptions

- IPR FV uses first valid day intercept plus 0.001 per timestamp.
- ACO FV remains 10000 for residual and edge calculations.
- Historical order book rows are representative enough for candidate generation, not final proof.

## Open Questions

- Does imbalance still help after simulating our own order placement and position?
- Should sparse immediate-edge logic be standalone or only an execution layer inside FV strategies?
- Does one-sided-book behavior create a safe resting quote opportunity, or only a skip condition?

## Downstream Use / Agent Notes

- Strong enough to consider: raw residual, fixed/drift FV residuals, one-sided handling, sparse edge sweeps.
- Exploratory only: imbalance-driven scoring until validated in a bot backtest.
- Do not use yet: log transform as a separate strategy signal.
- How strategy generation should use this: create a microstructure candidate distinct from fair-value market making and directional carry.
- How specification should use this: define thresholds, capacity clipping, and skip behavior explicitly.
- How implementation should use this: keep feature computation O(1), no external libraries, no in-bot model training.

## Reusable Metrics

- IPR residual std: 2.20; ACO residual std: 5.35.
- ACO positive best-quote edge share: buy 4.79%, sell 4.48%.
- IPR positive best-quote edge share: buy 1.63%, sell 1.55%.
- L1 imbalance vs next residual delta correlation: IPR 0.646 at horizon 1, ACO 0.646 at horizon 1.

## Strategy Implications

- Add a microstructure scalper / execution-layer candidate.
- Keep log transforms documented but do not shortlist a log-only strategy.
- Treat one-sided book handling as a spec requirement for all active candidates.

## Interpretation Limits

- These are sample-data observations, not official rules.
- Best-quote edge to FV does not prove realized PnL without replay/backtest.
- Imbalance signal may be partly mechanical bid-ask bounce.

## Next Action

- Use this EDA with the model and cross-product EDA to update `03_strategy_candidates.md`.
