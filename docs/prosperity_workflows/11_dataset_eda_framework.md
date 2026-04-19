# Dataset And EDA Framework

This framework helps contributors and agents understand new round data without assuming every round has the same columns or useful analyses.

Use it as a guided checklist, not a rigid schema. Classify the columns you actually have, then choose EDA that can change strategy, specification, validation, or debugging decisions.

## Column Classification

| Column category | Purpose | Common examples | Useful EDA | Derived features | Common mistakes | Downstream use |
| --- | --- | --- | --- | --- | --- | --- |
| Identifiers / indexing | Identify rows, records, runs, products, or files | row id, run id, day, scenario | uniqueness, duplicates, grouping keys | stable composite keys | treating ids as signals | reproducibility, joins |
| Time columns | Order and bucket observations | timestamp, iteration, time | gaps, sampling rate, session boundaries, regimes | buckets, elapsed time, lag features | assuming equal spacing without checking | rolling features, lead-lag |
| Product / symbol | Scope observations by tradable item | product, symbol | product coverage, missing products | product-specific panels | mixing products unintentionally | per-product strategy/spec |
| Price columns | Measure valuation and movement | bid, ask, mid, trade price, fair-like fields | distributions, returns, volatility, alignment | returns, log returns, z-score, normalized price, OHLC | treating all prices as equivalent | fair value, signals |
| Volume columns | Measure size/liquidity | quantity, volume, trade size | distributions, bursts, concentration | rolling volume, volume z-score | ignoring sign conventions | sizing, risk, liquidity |
| Order-book columns | Describe visible liquidity | bid/ask levels, depth, spread | spread, depth, imbalance, persistence | imbalance, relative spread, depth ratios | assuming book depth implies fills | execution and quoting |
| Trade columns | Describe realized transactions | buyer/seller, trade price, quantity | trade-vs-mid, impact, clustering | aggressor proxy, trade imbalance | confusing own trades and market trades | validation, signal evidence |
| State / position / PnL | Describe bot state or outcomes | position, PnL, cash, inventory | exposure, drawdown, limit pressure | inventory bands, PnL attribution | treating PnL as rule validity | validation/debugging |
| Round-specific special columns | Capture one-off mechanics | custom observations, conversion fields, manual fields | source-specific interpretation | only if wiki-supported | inventing mechanics from column names | ingestion/spec caveats |
| Derived / engineered | Reusable analysis features | rolling mean, EMA, RSI, z-score | stability, predictive usefulness | feature families | presenting derived values as facts | strategy/spec inputs |

## Fact Discipline

- Column names and meanings are facts only if defined by wiki docs, source metadata, or a named data source.
- Patterns in data are observations, not rules.
- Derived features are analysis tools, not official mechanics.
- Strategy implications are hypotheses until tested.
- If column meaning is unclear, record it as an open question or blocker before strategy depends on it.

## Adaptive EDA Flow

1. Name the data source and product scope.
2. Classify relevant columns using the table above.
3. Choose analyses that match those categories and can affect a downstream decision.
4. Create reusable metrics or derived features only when they support understanding, strategy, specification, validation, or debugging.
5. Build a serious engineered feature set for decision-relevant checks.
6. Run the default multivariate and process-hypothesis layers when applicable.
7. Write a structured EDA artifact that another agent can use without rerunning the analysis.

## Default Multivariate Layer

Run this on meaningful engineered features, not on every raw column. If the
feature set is tiny or the check cannot change a downstream decision, record
the deferral and why.

| Check | Default | Use For | Stop / Deepen Rule |
| --- | --- | --- | --- |
| Correlation matrix | mandatory by default | redundancy, sign, stability, feature budget | stop when feature families are clear; deepen if promoted signals overlap |
| Covariance matrix | expected unless irrelevant | magnitude-sensitive prices, returns, depths, spreads, product relationships | skip when standardized correlations already answer the decision |
| Redundancy analysis | mandatory for promoted or near-promoted signals | keep, merge, downgrade, or reject similar features | deepen with VIF/PCA only if pairwise checks are unclear |
| Multivariate regression | expected when a target exists | test whether a signal survives controls | keep explanatory and simple; stop before model tuning |
| Cross-product correlation / lead-lag | expected for multiple aligned products | decide whether products interact, diversify, or should be modeled separately | stop if unstable or not online-actionable |
| PCA / loadings | optional / conditional | simplify 5+ correlated feature candidates | do not use components directly in bots without an online proxy |
| Mutual information / non-linear dependence | optional / conditional | test threshold or non-linear relationships missed by correlation | use only when it may change a feature or regime decision |
| Clustering | optional / conditional | identify online-observable regimes or groups | reject clusters that do not map to an action |

The output should be a compact `Multivariate Feature Map` that says which
features overlap, which survive controls, whether cross-product signals matter,
and what downstream phases should do.

## Process / Distribution Hypothesis Layer

For serious products or signal families, summarize the approximate process
only as far as it changes decisions. Examples include trending,
mean-reverting, random-walk-like, jumpy, multimodal, volatility-clustered,
regime-switching, or flow-driven behavior.

Recommended lightweight evidence:

- distribution summaries: quantiles, tails, skew, outliers, multimodality hints
- time-series summaries: returns, rolling volatility, autocorrelation, persistence, reversal
- trend / mean-reversion checks: drift fit, AR-style persistence, residual stability
- regime checks: spread, depth, volatility, trade-flow, or imbalance bins
- heteroskedasticity checks only when risk, sizing, or validation may change
- formal mixture, latent-state, clustering, or change-point tooling only after the ROI gate passes

Process hypotheses should include product/scope, hypothesized process,
evidence, confidence, online observables, downstream implication, suggested
next test, caveat, and lifecycle status.

## EDA As Knowledge Transfer

The main EDA output is a readable artifact, not a plot or notebook. A good EDA summary lets another contributor:

- understand the data source and column meanings
- see what was analyzed and why
- reuse feature inventory entries, engineered features, and metrics
- distinguish facts, conditional patterns/regimes, signal hypotheses, and assumptions
- understand signal strength, uncertainty, and limitations
- see what downstream agents should use, avoid, or validate next
- decide whether to proceed to understanding, strategy, specification, validation, debugging, or more EDA

## Signal Strength

- Strong: repeated across relevant slices or directly affects implementation/validation.
- Medium: visible but limited by sample size, regime, or missing comparison.
- Weak: interesting but not enough to drive strategy without more EDA.
- Contradictory: evidence conflicts across slices or sources.

## Stop Or Deepen

Deepen EDA when:

- a finding could change candidate queue, spec, validation, or debugging decisions
- a signal looks actionable but uncertain
- evidence contradicts an assumption
- debugging exposes a data or interpretation gap
- redundancy checks could prevent a feature-dump strategy
- a process hypothesis could change strategy family, risk, sizing, or validation
- cross-product behavior could change product scope or execution logic

Stop EDA when:

- additional analysis will not change the next implementation decision
- less than 24 hours remain and implementation/validation is the bottleneck
- the result is enough to prioritize the next implementation-ready specs
- PCA, clustering, mutual information, latent-state, or change-point work would only produce a decorative stats report
