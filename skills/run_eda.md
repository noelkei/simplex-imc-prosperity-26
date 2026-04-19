# Run EDA

Use this skill to turn data, logs, or run artifacts into evidence another agent can consume for understanding, strategy, specification, implementation, variants, validation, or debugging.

## Required sources

- Wiki: `../docs/prosperity_wiki/README.md`
- Datamodel and runtime: `../docs/prosperity_wiki/api/02_datamodel_reference.md`, `../docs/prosperity_wiki/api/03_runtime_and_resources.md`
- Trading signs and limits: `../docs/prosperity_wiki/trading/02_orders_and_position_limits.md`
- Active round: the relevant file in `../docs/prosperity_wiki/rounds/`
- Round state: `../rounds/round_X/workspace/_index.md` and `../rounds/round_X/workspace/phase_01_eda_context.md`
- Post-run research memory, when present: `../rounds/round_X/workspace/post_run_research_memory.md`
- Workflow: `../docs/prosperity_workflows/03_workstream_eda.md`
- Dataset framework: `../docs/prosperity_workflows/11_dataset_eda_framework.md`
- Template: `../docs/templates/eda_summary_template.md`

## Steps

1. Read the active round `_index.md` and EDA phase context before analyzing. If `../rounds/round_X/workspace/post_run_research_memory.md` exists, read it before choosing EDA questions; treat it as evidence input and cite relevant insights when they drive EDA choices. Post-run discoveries become targeted EDA questions only when they pass the decision gate: they could change strategy selection, parameters, risk controls, validation, debugging, or backlog status.
2. Fill the EDA Round Adaptation Check before deep analysis. Use it to seed EDA questions from current-round mechanics, schema changes, product behavior, and prior-round assumptions at risk.
3. Prioritize EDA questions from ingestion unknowns when they could affect strategy, implementation, validation, or debugging.
4. State the exact EDA question and the downstream decision it may affect before analyzing.
5. Place or cite input artifacts under `../rounds/round_X/data/raw/`, `../rounds/round_X/data/processed/`, or `../rounds/round_X/data/external/`.
6. Persist reusable outputs under existing round-local paths such as `../rounds/round_X/data/processed/`, `../rounds/round_X/workspace/01_eda/`, or a nearby `artifacts/` folder when already present; do not create new top-level artifact roots.
7. Link persisted tables, plots, notebooks, scripts, processed files, and raw logs in the EDA `Artifact Index`; do not rely on terminal output as durable evidence.
8. Cite the data, log, or run artifact path and relevant product scope, including products present, products with usable evidence, likely trader scope, and any deferred/excluded products.
9. Separate algorithmic findings usable by `Trader.run()` from manual-challenge findings when both exist.
10. Read wiki sources for field meanings, signs, products, limits, and runtime context.
11. Classify relevant columns with the dataset framework before choosing analyses; mark unclear meanings as open questions or blockers.
12. Quantify data quality before relying on results: row counts by file/product, timestamp coverage and gaps, missing bid/ask counts when order books are used, zero/blank `mid_price` counts when mid prices are used, and any filters applied.
13. Choose targeted checks from the EDA methodology: descriptive stats, distributions, volatility/regimes, spreads/microstructure, correlations, lead-lag, price-vs-trade alignment, volume behavior, or order book dynamics. Use the research environment when it improves the check: `pandas`/`numpy` for core tables, `polars` for large logs, `scipy`/`statsmodels`/`pingouin` for confidence, correlations, regressions, and tests, `arch`/`ruptures` for decision-relevant regimes, `sklearn` for PCA/loadings, mutual information, lightweight grouping, or baselines, and `numba` for repeated loops.
14. Treat feature engineering as part of EDA: test useful transformations such as spreads, returns/deltas, rolling mean/std, z-scores, normalized values, imbalance/liquidity proxies, trade-pressure proxies, fair-value deviations, and specific feature combinations. Do not force research libraries into simple checks, and record tools used or skipped when that affects reproducibility or confidence.
    After feature engineering, run the default multivariate and process sequence unless the artifact explicitly records why a check is irrelevant or low ROI:
    1. Build the serious feature set and target variables, such as future mid delta, return sign, fill/markout proxy, or PnL proxy.
    2. Run correlation, covariance when magnitude matters, and redundancy checks on serious features.
    3. Run simple explanatory regressions or controlled comparisons when a target exists; keep them explanatory, not predictive pipelines.
    4. Run cross-product correlation, covariance, and lead-lag checks when multiple products have aligned timestamps or plausible interaction.
    5. Use PCA/loadings, mutual information, clustering, change-points, or latent/regime tooling only when the ROI gate says it could change promotion, strategy, spec, validation, or debugging.
    6. Produce process/distribution hypotheses for serious products or signal families: trending, mean-reverting, random-walk-like, jumpy, multimodal, volatility-clustered, regime-switching, flow-driven, or unclear.
    7. Classify multivariate and process findings through the same feature lifecycle and downstream action labels as other signals.
15. Classify each serious feature by origin (`csv`, `online`, `log/post-run`, `combined`, `manual-only`), online usability (`usable online`, `EDA-only`, `log-only`, `unknown`), and role (`direct signal`, `execution filter`, `risk control`, `diagnostic`, `manual`, `avoid`).
16. Evaluate each serious feature against the signal gate, stability gate, and actionability gate:
    - signal gate: predicts, explains, or classifies something useful
    - stability gate: persists across days, timestamps, products, or regimes
    - actionability gate: changes strategy, parameters, risk, validation, or debugging
17. Keep feature engineering targeted and hypothesis-driven. Do not brute-force feature combinations; document only useful, potentially useful, or meaningfully rejected transformations.
18. Apply feature explosion controls: default to 5-8 serious feature candidates and 1-3 promoted signal hypotheses per EDA artifact unless the user explicitly requests breadth and the deadline allows it.
19. Record a feature promotion decision for every serious feature: promote to understanding, keep exploratory, negative evidence, EDA-only calibration, needs logs, or reject.
20. Preserve meaningful negative evidence for high-plausibility rejected features so later agents do not rediscover weak ideas.
21. Include lightweight process/distribution hypotheses, multivariate relationships, redundancy decisions, and threshold/execution observations only when they could change strategy, risk, parameterization, or validation.
22. Use a stop/deepen checkpoint before adding new analysis branches: deepen only when the next check could change strategy selection, spec parameters, risk controls, validation, or debugging; otherwise stop and write the handoff.
23. Look for conditional patterns or regimes when they could affect trading: volatility, spread, liquidity, imbalance, trade-flow bursts, product-specific behavior, or plausible cross-product relationships.
24. Produce reproducible output: command notes, script, table, plot, or optional notebook. Use a notebook when exploratory code, charts, or feature experiments would help a human inspect or extend the work; keep Markdown as the canonical handoff.
25. Write EDA summaries under `../rounds/round_X/workspace/01_eda/` using `eda_<short_question>.md` and the EDA summary template.
26. Include `Product Scope`, `Algorithmic vs Manual Scope`, `Round Adaptation Check`, `Artifact Index`, `Data Quality And Filters`, `Feature Inventory`, `Feature Engineering Notes`, `Feature Promotion Decisions`, `Multivariate Feature Map`, `Redundancy / Dimensionality Check`, `Cross-Product Relationships`, `Process / Distribution Hypotheses`, `Multivariate Model Notes`, `Conditional Patterns / Regimes`, `Threshold / Execution Findings`, `Signal Hypotheses`, `Downstream Feature Contract Implications`, `Negative Evidence`, and `Downstream Use / Agent Notes`.
27. For each important feature, pattern, or signal, state what it means, why it matters, how it could be used in a strategy, limitations/caveats, and confidence level.
28. State whether each major finding uses raw rows, filtered rows, or mixed data.
29. Separate facts, conditional patterns/regimes, signal hypotheses, assumptions, open questions, and strategy interpretation.
30. State signal strength as strong, medium, weak, or contradictory, with uncertainty and limitations.
31. Prioritize the top 1-3 signal hypotheses by decision impact, and state which weak or rejected signals should not drive strategy yet.
32. Mark which signals are strong enough to consider, exploratory only, or not ready to use; include what validation is needed next.
33. Do not claim a rule or valid strategy only because a pattern appears in sample data.
34. Do not use round-local bot artifacts, performance artifacts, or `non-canonical/` drafts as truth; treat them only as named artifacts if explicitly analyzed.
35. Avoid decorative EDA: every chart, table, or metric must state what it changes, what remains uncertain, and how a downstream phase should use it.
36. Prefer fewer clear, reusable signals over many unclear findings.
37. Propose follow-up EDA only when it could materially change strategy selection, parameterization, risk controls, validation, or debugging.
38. Before closing EDA, confirm another agent can use the artifact without rerunning the analysis.
39. Confirm at least one downstream stage can use the EDA directly, or record why EDA was skipped/deferred under deadline pressure.
40. Update `../rounds/round_X/workspace/_index.md` and `../rounds/round_X/workspace/phase_01_eda_context.md`, including any resolved or new downstream-impacting unknowns.
41. Handoff with method, filters, linked artifacts, findings, feature origin/usability/role/status, evidence limits, negative evidence, assumptions, what to use, what not to trust yet, validation needed, and next action.
