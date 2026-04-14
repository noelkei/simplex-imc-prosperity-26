# Workstream: Exploratory Data Analysis

EDA turns sample data and run outputs into evidence. It does not need to produce bot code.

Use [`11_dataset_eda_framework.md`](11_dataset_eda_framework.md) to classify columns and choose analyses that fit the data actually available in the current round.

## Inputs

- A concrete question, such as price stability, spread behavior, volume distribution, fill behavior, or PnL breakdown.
- Data files, logs, or run artifacts available in the repo or from the platform.
- Wiki facts for interpreting fields, signs, products, and runtime context.
- Playbook heuristics only as research prompts, not as proof.

## Good outputs

- A short summary of the question, method, and result.
- Reproducible artifacts: notebook, script, table, plot, or command notes.
- Clear source references for the data used.
- A distinction between observed evidence and strategy interpretation.
- A recommendation for the next workstream: more EDA, strategy research, implementation, or validation.
- A knowledge-transfer artifact another agent can use without rerunning EDA.

For active round workspaces, close EDA with the sections required by the round template:

- Facts
- Patterns observed
- Hypotheses
- Open questions
- Reusable metrics
- Downstream use

## How to do EDA well

Use a checklist, but keep it targeted. Start with the decision the analysis may affect: strategy choice, parameterization, risk handling, validation, or debugging. Skip checklist items that cannot change a decision under the current deadline.

Before analyzing, state:

- product scope
- data source
- exact question
- decision the result may affect
- time budget

Useful analysis dimensions include:

- Descriptive stats: count, missingness, min/max, mean/median, quantiles, and outliers.
- Distributions: mid-price, returns, spreads, volumes, trade sizes, and order book depth when available.
- Volatility and regimes: rolling volatility, abrupt shifts, stable periods, and unstable periods.
- Spreads and microstructure: bid/ask spread, mid-price, depth imbalance, price impact proxies, and liquidity gaps.
- Correlations and covariances: within-product features and cross-product relationships when products plausibly relate.
- Lead-lag relationships: lagged correlations, response timing, and predictive delays when relevant.
- Price vs trade alignment: trade price relative to mid, best bid/ask, and recent movement.
- Volume behavior: trade count, size distribution, concentration, bursts, and quiet periods.
- Order book dynamics: imbalance, depth changes, best-level persistence, and spread widening or narrowing.

Useful derived features include:

- OHLC by meaningful time bucket.
- Returns or log returns.
- Rolling means and rolling standard deviations.
- SMA or EMA features.
- Z-scores for price, spread, volume, imbalance, or residual-like signals.
- RSI only when momentum or mean-reversion framing makes it useful.
- Spread features: absolute spread, relative spread, rolling spread, and spread z-score.
- Normalized price features: price vs rolling mean, price percentile, or deviation from reference.
- Custom signals from observed data, clearly labeled as hypotheses.

EDA is shallow if it only lists stats or plots without explaining what changed, what remains uncertain, and how a downstream phase should use it.

## Knowledge transfer requirements

Every durable EDA summary should include:

- column classification summary
- facts, observations, hypotheses, and assumptions separated
- signal strength: strong, medium, weak, or contradictory
- uncertainty and interpretation limits
- reusable metrics or derived features
- downstream impact for understanding, strategy, specification, validation, and debugging
- prioritized follow-up EDA only when it could change a decision

## Safe practice

- Keep product names, symbols, and signs aligned with the wiki.
- Do not claim that a strategy is valid just because a pattern appears in sample data.
- Do not overfit conclusions to one sample day without saying so.
- Preserve surprising or contradictory findings as evidence, not as rules.
- Reuse existing processed data and summaries before creating new artifacts.
- Propose follow-up EDA only when it could materially change strategy selection, parameterization, risk controls, validation, or debugging.

## Exit criteria

EDA is done only when:

- the data/log source is named
- relevant columns are classified or explicitly marked unclear
- reproduction steps or artifact paths are recorded
- facts, observed patterns, hypotheses, assumptions, and open questions are separated
- signal strength and uncertainty are stated for important findings
- reusable metrics or derived features are listed when created
- downstream use is explicit, or the result is marked not actionable
- at least one downstream stage can use the result directly, or EDA is explicitly skipped/deferred with a reason
- the round `_index.md` and phase context are updated
- human review is requested, completed, or explicitly deferred under deadline pressure

## Handoff checklist

- Data source and date or run identifier.
- Exact question answered.
- Main findings in a few bullets.
- Files or commands needed to reproduce.
- Assumptions and unresolved questions.
- Suggested next action.
