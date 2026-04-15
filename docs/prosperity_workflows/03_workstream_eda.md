# Workstream: Exploratory Data Analysis

EDA turns sample data and run outputs into evidence another agent can consume without prior context. It does not need to produce bot code, but it should make strategy-relevant signals, limits, caveats, and next actions easy to use.

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
- Data quality and filter notes: row counts, missingness, incomplete books, zero/blank mid prices, timestamp coverage, and which rows were used for each major result.
- A distinction between observed evidence and strategy interpretation.
- A recommendation for the next workstream: more EDA, strategy research, implementation, or validation.
- A knowledge-transfer artifact another agent can use without rerunning EDA.

Every important feature, pattern, or signal should state:

- what it means
- why it matters
- how it could be used in a strategy
- limitations or caveats
- confidence level

Fewer clear, reusable signals are better than many unclear findings.

For active round workspaces, close EDA with the sections required by the round template:

- Product scope
- Data quality and filters
- Feature inventory
- Feature engineering notes
- Facts
- Conditional patterns / regimes
- Signal hypotheses
- Open questions
- Reusable metrics
- Downstream use / agent notes

## How to do EDA well

Use a checklist, but keep it targeted. Start with the decision the analysis may affect: strategy choice, parameterization, risk handling, validation, or debugging. Skip checklist items that cannot change a decision under the current deadline.

Before analyzing, state:

- product scope
- data source
- exact question
- decision the result may affect
- time budget

Track product scope explicitly:

- products present in the data
- products with enough usable evidence
- products likely needed in the trader
- products deferred or excluded, with rationale

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

## Feature engineering

Feature engineering is a core EDA responsibility. Raw columns are rarely enough for edge, so create simple derived features when they can expose a tradable pattern or make a hypothesis testable.

Prefer simple, hypothesis-driven transformations before complex ones:

- OHLC by meaningful time bucket.
- Returns or log returns.
- Rolling means and rolling standard deviations.
- SMA or EMA features.
- Z-scores for price, spread, volume, imbalance, or residual-like signals.
- RSI only when momentum or mean-reversion framing makes it useful.
- Spread features: absolute spread, relative spread, rolling spread, and spread z-score.
- Normalized price features: price vs rolling mean, price percentile, or deviation from reference.
- Imbalance, liquidity, or trade-pressure proxies when order book or trade data supports them.
- Fair-value deviations when a reference value can be justified.
- Feature combinations when a specific interaction is plausible, such as imbalance plus spread or price deviation plus liquidity regime.
- Custom signals from observed data, clearly labeled as hypotheses.

Do not brute-force feature combinations or produce feature catalogs that no downstream phase can use. Document only features that are useful, potentially useful, or meaningfully rejected because the result changes a decision.

## Conditional patterns and regimes

EDA should look for conditions where behavior changes, without turning into unbounded exploration. Useful checks include:

- high vs low volatility periods
- wide vs tight spread regimes
- high vs low liquidity or book imbalance
- quiet vs bursty trade flow
- product-specific differences
- cross-product relationships when products plausibly interact

If no meaningful conditional pattern is found, record the checks attempted and mark the signal as weak or unconfirmed.

## Product branching

Use one combined EDA summary by default. Split into product-specific notes only when product behavior is materially different or the combined file becomes hard to consume. Product-specific notes are supporting artifacts; merge the decision-useful findings back into the canonical EDA handoff before closing the phase.

## Optional notebooks

Markdown is the canonical handoff for downstream agents. Notebooks are optional secondary artifacts for human inspection, charts, exploratory code, feature experiments, and reproducibility.

Create a notebook when the EDA uses nontrivial plots, transformations, or exploratory code that a human may want to inspect or extend. Do not require a notebook for small checks where commands or tables are enough.

EDA is shallow if it only lists stats or plots without explaining what changed, what remains uncertain, and how a downstream phase should use it.

## Knowledge transfer requirements

Every durable EDA summary should include:

- column classification summary
- feature inventory with raw and derived features that matter
- feature engineering notes: attempted transformations, useful results, rejected results, and promising validation targets
- facts, conditional patterns/regimes, signal hypotheses, and assumptions separated
- signal strength: strong, medium, weak, or contradictory
- signal dependencies: raw/derived features used and whether they appear stable, regime-dependent, or unknown
- uncertainty and interpretation limits
- reusable metrics or derived features
- downstream use / agent notes for understanding, strategy, specification, validation, and debugging
- prioritized follow-up EDA only when it could change a decision

The downstream notes should say which signals are strong enough to consider, which are exploratory only, which should not be used yet, and what additional validation is needed.

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
- data quality and filters are documented, including row counts, timestamp coverage, missing bid/ask counts when order books are used, zero/blank `mid_price` counts when mid prices are used, and whether findings use raw or filtered rows
- relevant columns are classified or explicitly marked unclear
- reproduction steps or artifact paths are recorded
- facts, conditional patterns/regimes, signal hypotheses, assumptions, and open questions are separated
- signal strength and uncertainty are stated for important findings
- reusable metrics or derived features are listed when created
- downstream use / agent notes are explicit, or the result is marked not actionable
- at least one downstream stage can use the result directly, or EDA is explicitly skipped/deferred with a reason
- the round `_index.md` and phase context are updated
- human review is requested, completed, or explicitly deferred under deadline pressure

## Handoff checklist

- Data source and date or run identifier.
- Exact question answered.
- Data quality caveats and filters used.
- Main findings in a few bullets.
- Signals/features another agent should consider, avoid, or validate next.
- Files or commands needed to reproduce.
- Assumptions and unresolved questions.
- Suggested next action.
