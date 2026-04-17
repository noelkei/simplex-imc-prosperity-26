# EDA Strategy Expansion Models

## Status

READY_FOR_REVIEW

## Question

- Question: Do offline Markov states, light linear models, or PCA-style state compression reveal strategy ideas that are not just variants of the existing FV market maker?
- Product scope: `INTARIAN_PEPPER_ROOT` and `ASH_COATED_OSMIUM`.
- Why this matters downstream: The bot can hardcode offline-learned matrices or coefficients, but only if the signal is simple, stable, and not just bid-ask bounce.

## Data Sources

- Raw data: `rounds/round_1/data/raw/prices_round_1_day_{-2,-1,0}.csv`
- Processed data: `rounds/round_1/data/processed/strategy_expansion_metrics.json`
- Reproduction script: `rounds/round_1/workspace/01_eda/strategy_expansion_analysis.py`
- External context: none.

## Data Quality And Filters

- Same row and missingness profile as `eda_strategy_expansion_feature_lab.md`.
- Markov and model rows require nonzero `mid_price` and valid future residual targets inside the same product/day sequence.
- Linear models train on days -2 and -1 and validate on day 0.
- Findings based on filtered rows with derived residual, spread, imbalance, depth, and one-sided flags.

## Feature Inventory

| Feature | Source | Meaning | Classification | Strategy Use | Stability | Notes / Caveats |
| --- | --- | --- | --- | --- | --- | --- |
| residual bucket | derived | discretized FV deviation | predictive / regime | Markov transition state | medium | Bucket choice is a modeling assumption |
| future residual delta | derived | residual change over 1/5/10 observations | target | model validation | unknown | Includes microstructure bounce |
| standardized residual/spread/imbalance/depth | derived | light model input | predictive / descriptive | hardcoded coefficient candidate | medium | Coefficients are offline artifacts |
| PCA components | derived | orthogonal feature combinations | descriptive / regime | compact state / risk flag | exploratory | Not a direct trading rule |

## Feature Engineering Notes

| Transformation Or Feature | Purpose | Result | Keep? | Next Validation |
| --- | --- | --- | --- | --- |
| Markov residual buckets | Look for state persistence/mean reversion | ACO residual buckets mean-revert; IPR buckets collapse toward slight-over state | maybe | Backtest Markov-gated quoting |
| Light linear regression | Test embeddable multifeature score | Day-0 R2 around 0.40-0.50, sign accuracy 0.66-0.82 | maybe | Remove collinear log feature and test as execution layer |
| PCA on residual/spread/imbalance/depth | Find compact state axes | PC1 = residual/imbalance axis; PC2 = spread/depth axis | exploratory | Use for regime labels, not direct orders |
| Log residual in model | Test transform | Collinear with raw residual; coefficients unstable | no | Drop from implementation spec unless needed for scale |

## Analyses Run

- Reproduction command: `python3 rounds/round_1/workspace/01_eda/strategy_expansion_analysis.py`
- Output artifacts: `rounds/round_1/data/processed/strategy_expansion_metrics.json`
- Markov: residual-bucket transition matrices by product.
- Regression: simple ridge-stabilized OLS with standardized features, train days -2/-1, validate day 0.
- PCA: covariance/eigen decomposition over standardized residual, spread, imbalance, and depth features.

## Markov Findings

### `ASH_COATED_OSMIUM`

| Current Bucket | Count | Mean Current Residual | Mean Next Residual | Mean Next Delta | Mode Next Bucket | Interpretation |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| under | 770 | -12.60 | -7.92 | +4.67 | slight_under | clear mean reversion |
| slight_under | 6414 | -6.10 | -4.98 | +1.12 | slight_under | mild mean reversion |
| neutral | 13216 | -0.18 | -0.08 | +0.10 | neutral | mostly persistent |
| slight_over | 8316 | +5.17 | +4.30 | -0.87 | slight_over | mild mean reversion |
| over | 1170 | +12.02 | +7.96 | -4.06 | over | clear mean reversion |

- Deep buckets have too few observations (`deep_under` count 4, `deep_over` count 9) to drive a strategy.
- ACO Markov is plausible as a regime gate around fixed-FV market making.

### `INTARIAN_PEPPER_ROOT`

| Current Bucket | Count | Mean Current Residual | Mean Next Residual | Mean Next Delta | Mode Next Bucket | Interpretation |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| under | 1317 | -4.47 | +1.46 | +5.93 | slight_over | strong snapback |
| neutral | 3879 | +0.02 | +1.44 | +1.42 | slight_over | drift/grid artifact likely |
| slight_over | 20844 | +1.61 | +1.52 | -0.10 | slight_over | dominant state |
| over | 2089 | +3.33 | +1.51 | -1.82 | slight_over | mean reversion to common state |
| deep_over | 1463 | +7.84 | +1.43 | -6.41 | slight_over | snapback |

- IPR Markov mostly restates the deterministic FV residual and discrete book mechanics.
- Use IPR Markov only as execution/risk context, not as a primary strategy edge.

## Light Linear Model Findings

Target: future residual delta over 1, 5, or 10 product observations. Train days -2/-1, validate day 0.

| Product | Horizon | Day-0 R2 | Day-0 Sign Accuracy | MAE | Interpretation |
| --- | ---: | ---: | ---: | ---: | --- |
| `INTARIAN_PEPPER_ROOT` | 1 | 0.498 | 0.686 | 1.219 | mostly residual/bounce correction |
| `INTARIAN_PEPPER_ROOT` | 5 | 0.497 | 0.817 | 1.214 | promising as execution score, not FV replacement |
| `INTARIAN_PEPPER_ROOT` | 10 | 0.492 | 0.771 | 1.214 | similar to horizon 5 |
| `ASH_COATED_OSMIUM` | 1 | 0.415 | 0.719 | 1.700 | useful short-horizon mean-reversion signal |
| `ASH_COATED_OSMIUM` | 5 | 0.415 | 0.685 | 1.814 | promising but modest |
| `ASH_COATED_OSMIUM` | 10 | 0.398 | 0.665 | 1.956 | weaker with horizon |

- Coefficients on raw and log residual are unstable because the two features are nearly identical.
- The useful implementation candidate should drop log residual and keep a small fixed coefficient vector if validation confirms edge.

## PCA Findings

| Product | PC1 Explained | PC1 Main Weights | PC2 Explained | PC2 Main Weights | Strategy Use |
| --- | ---: | --- | ---: | --- | --- |
| `INTARIAN_PEPPER_ROOT` | 47.6% | residual -0.61, imbalance_l1 +0.62, imbalance_l3 +0.49 | 23.1% | spread +0.63, total_depth -0.78 | compact state axes |
| `ASH_COATED_OSMIUM` | 37.3% | residual -0.53, imbalance_l1 +0.63, imbalance_l3 +0.57 | 22.7% | spread +0.61, total_depth -0.79 | compact state axes |

- PC1 says residual and book imbalance move together in the sample.
- PC2 says spread and visible depth define a separate liquidity axis.
- PCA should not be implemented as a black-box trading rule, but it supports a two-axis regime design: price-pressure state plus liquidity state.

## Conditional Patterns / Regimes

| Condition Or Regime | Dependent Features | Observed Behavior | Strategy Relevance | Confidence | Caveats |
| --- | --- | --- | --- | --- | --- |
| ACO residual far from FV | Markov residual bucket | Mean next delta points back toward FV | Markov-gated ACO mean reversion | medium | Deep buckets are sparse |
| IPR residual far from drift FV | residual bucket | Snaps toward slight-over bucket | Execution filter around drift FV | medium | May be book-grid mechanics |
| Price-pressure axis | PCA PC1 | residual and imbalance are linked | Lightweight state score | exploratory | Needs bot-level validation |
| Liquidity axis | PCA PC2 | spread and depth separate from residual | Quote width / skip state | exploratory | Not directional |

## Signal Hypotheses

| Signal | Feature Dependencies | What It Means | Why It Matters | Strategy Use | Stability | Confidence | Limitations / Caveats |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ACO Markov residual regime | residual buckets, transition matrix | ACO tends to move back toward FV from under/over states | Could improve entry timing and inventory skew | Hardcode transition probabilities or expected deltas | regime-dependent | medium | Must avoid overfitting bucket thresholds |
| Light linear state score | residual, imbalance, spread, depth, one-sided | Small feature vector predicts residual correction on day 0 | Embeddable coefficients can gate quotes | Use as additive score or quote skew | unknown | medium | Needs simplified coefficients and replay validation |
| PCA regime map | residual/imbalance and spread/depth axes | State separates pressure from liquidity | Helps design non-duplicative strategies | Use to define regimes manually | unknown | exploratory | Not directly tradable |

## Assumptions

- Historical day -2/-1 to day 0 validation is representative enough to propose candidates.
- The bot may hardcode small matrices or coefficient vectors but cannot train online.
- Markov buckets are modeling choices, not official product rules.

## Open Questions

- Does the ACO Markov candidate beat fixed-FV skew after realistic position and fill simulation?
- Does a simplified linear model still work after removing log residual collinearity?
- Should PCA become a spec feature, or only an analysis lens for human strategy design?

## Downstream Use / Agent Notes

- Strong enough to consider: ACO Markov as an experimental candidate; linear state score as execution layer.
- Exploratory only: PCA components.
- Do not use yet: log residual as a standalone feature; in-bot model training.
- How strategy generation should use this: add Markov/regime and light-linear candidates, but keep them separate from FV baseline.
- How specification should use this: hardcode matrices/coefficients only after choosing a candidate; document state buckets and fallback.
- How implementation should use this: keep all model inference O(1) and pure Python.

## Reusable Metrics

- ACO Markov `under` bucket mean next delta: +4.67.
- ACO Markov `over` bucket mean next delta: -4.06.
- IPR light model horizon-5 day-0 sign accuracy: 0.817.
- ACO light model horizon-1 day-0 sign accuracy: 0.719.
- PCA PC1 explained variance: IPR 47.6%, ACO 37.3%.

## Strategy Implications

- Add an ACO Markov/regime candidate.
- Add a light linear state-score candidate or execution overlay.
- Treat PCA as design evidence for regime axes rather than a production signal.

## Interpretation Limits

- Model metrics predict residual deltas, not final PnL.
- Residual-delta prediction can be inflated by microstructure bounce.
- All models require backtest validation before implementation readiness.

## Next Action

- Use these findings to update strategy candidates and mark model-based approaches as experimental until validated.
