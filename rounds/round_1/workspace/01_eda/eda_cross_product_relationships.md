# EDA Cross-Product Relationships

## Status

READY_FOR_REVIEW

## Question

- Question: Do `INTARIAN_PEPPER_ROOT` and `ASH_COATED_OSMIUM` have an actionable relationship that should be considered inside the same bot?
- Product scope: both Round 1 algorithmic products.
- Why this matters downstream: A single `Trader.run()` can run product-specific strategies plus shared risk logic, but cross-product signals should not be invented if the data does not support them.

## Data Sources

- Raw data: `rounds/round_1/data/raw/prices_round_1_day_{-2,-1,0}.csv`
- Processed data: `rounds/round_1/data/processed/strategy_expansion_metrics.json`
- Reproduction script: `rounds/round_1/workspace/01_eda/strategy_expansion_analysis.py`
- External context: none.

## Data Quality And Filters

- Cross-product panel rows: 30000 matched `(day, timestamp)` rows with both products present.
- Metrics use residual, mid delta, spread, imbalance, depth, and one-sided flags.
- Findings based on rows where the paired feature exists for both products.
- Caveat: the sample includes only two algorithmic products and three historical days.

## Feature Inventory

| Feature | Source | Meaning | Classification | Strategy Use | Stability | Notes / Caveats |
| --- | --- | --- | --- | --- | --- | --- |
| same-time residual correlation | derived | IPR residual vs ACO residual at same timestamp | cross-product | possible pairs/filter signal | weak | Observed near zero |
| lead-lag residual correlation | derived | IPR residual at t vs ACO residual at t+k | cross-product | possible lead-lag signal | weak | Observed near zero |
| same-time spread/depth correlation | derived | shared liquidity regime | risk / execution | possible shared risk gate | weak | Observed near zero |
| one-sided co-occurrence | derived | simultaneous book quality issue | risk / execution | common skip/fallback | weak | Observed near zero |

## Analyses Run

- Reproduction command: `python3 rounds/round_1/workspace/01_eda/strategy_expansion_analysis.py`
- Output artifacts: `rounds/round_1/data/processed/strategy_expansion_metrics.json`
- Correlation / covariance checks: same-time correlations across residual, mid delta, spread, imbalance, total depth, and one-sided flags.
- Lead-lag checks: IPR feature at t against ACO feature at t plus lags -10, -5, -2, -1, 0, 1, 2, 5, 10 observations.

## Cross-Product Results

### Same-Time Correlations

| Pair | Correlation | Interpretation |
| --- | ---: | --- |
| IPR residual vs ACO residual | -0.009 | no actionable relationship |
| IPR mid delta vs ACO mid delta | +0.016 | no actionable relationship |
| IPR spread vs ACO spread | -0.001 | no shared spread regime |
| IPR imbalance_l1 vs ACO imbalance_l1 | +0.002 | no shared book pressure |
| IPR total depth vs ACO total depth | +0.006 | no shared depth state |
| IPR one-sided vs ACO one-sided | -0.004 | no shared book outage |

### Strongest Tested Lead-Lag Relationships

| Feature | Strongest Lag Tested | Correlation | Interpretation |
| --- | --- | ---: | --- |
| residual | IPR t to ACO t-1 | -0.0168 | too small to trade |
| mid_delta | IPR t to ACO t | +0.0160 | too small to trade |
| spread | IPR t to ACO t-5 | +0.0098 | too small to trade |
| imbalance_l1 | IPR t to ACO t-1 | -0.0104 | too small to trade |

## Conditional Patterns / Regimes

| Condition Or Regime | Dependent Features | Observed Behavior | Strategy Relevance | Confidence | Caveats |
| --- | --- | --- | --- | --- | --- |
| Cross-product residual lead-lag | residual | All tested correlations within about +/-0.017 | reject directional cross-product signal | medium | Linear correlation only; nonlinear checks not exhausted |
| Shared liquidity regime | spread, depth, one-sided | Same-time correlations near zero | no shared quote-width gate required | medium | Could still monitor each product independently |
| Shared book pressure | imbalance_l1 | Same-time and lag correlations near zero | no cross-product imbalance filter | medium | Product-specific imbalance remains promising |

## Signal Hypotheses

| Signal | Feature Dependencies | What It Means | Why It Matters | Strategy Use | Stability | Confidence | Limitations / Caveats |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Product independence remains the base assumption | residual, spread, depth, imbalance | No meaningful cross-product relation appears in sample | Avoids adding false complexity | Run product strategies independently inside same bot | stable historically | medium | Nonlinear or live-only relation could exist |
| Cross-product risk overlay only | per-product anomaly flags | Shared relation is weak, but one bot can coordinate risk | Prevents accidental overcomplication | Use shared `traderData` and per-product health flags, not directional pairs trading | unknown | exploratory | Needs spec only if chosen |

## Assumptions

- Linear and lead-lag correlations are sufficient to reject simple cross-product trading for this round.
- Product-specific strategies can run concurrently in one bot without needing cross-product capital allocation beyond per-product limits.

## Open Questions

- Is there a nonlinear cross-product relation not captured by this pass?
- Should the final bot include a shared risk flag if either product breaks its FV regime, even without product correlation?

## Downstream Use / Agent Notes

- Strong enough to consider: independent per-product logic in one `Trader.run()`.
- Exploratory only: shared risk overlay using anomaly flags.
- Do not use yet: directional cross-product arbitrage, pairs trading, or lead-lag trading.
- How strategy generation should use this: include cross-product relation as a rejected/deferred idea, and include shared risk only as an overlay candidate.
- How specification should use this: if a combined bot is chosen, explicitly state products are run independently unless a risk overlay is selected.
- How implementation should use this: one bot should still coordinate `traderData`, exceptions, and shared risk flags.

## Reusable Metrics

- Matched cross-product panel rows: 30000.
- Strongest tested residual lead-lag correlation magnitude: 0.0168.
- Strongest tested mid-delta correlation magnitude: 0.0160.

## Strategy Implications

- Do not shortlist cross-product arbitrage.
- Keep a combined bot architecture because the platform submission is one `Trader`, but product strategies should remain independent by default.
- Consider a defensive regime-switch overlay as a conceptually distinct approach.

## Interpretation Limits

- Lack of linear correlation in sample data does not prove no live relationship exists.
- The current analysis does not test nonlinear interactions exhaustively.
- Cross-product findings should not override stronger product-specific FV and microstructure evidence.

## Next Action

- Update strategy candidates with cross-product arbitrage rejected/deferred and shared risk overlay marked exploratory.
