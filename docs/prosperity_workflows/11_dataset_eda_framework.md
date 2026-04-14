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
5. Write a structured EDA artifact that another agent can use without rerunning the analysis.

## EDA As Knowledge Transfer

The main EDA output is a readable artifact, not a plot or notebook. A good EDA summary lets another contributor:

- understand the data source and column meanings
- see what was analyzed and why
- reuse metrics or derived features
- distinguish facts, observations, hypotheses, and assumptions
- understand signal strength, uncertainty, and limitations
- decide whether to proceed to understanding, strategy, specification, validation, debugging, or more EDA

## Signal Strength

- Strong: repeated across relevant slices or directly affects implementation/validation.
- Medium: visible but limited by sample size, regime, or missing comparison.
- Weak: interesting but not enough to drive strategy without more EDA.
- Contradictory: evidence conflicts across slices or sources.

## Stop Or Deepen

Deepen EDA when:

- a finding could change shortlist, spec, validation, or debugging decisions
- a signal looks actionable but uncertain
- evidence contradicts an assumption
- debugging exposes a data or interpretation gap

Stop EDA when:

- additional analysis will not change the next implementation decision
- less than 24 hours remain and implementation/validation is the bottleneck
- the result is enough to support 1-2 implementation-ready specs
