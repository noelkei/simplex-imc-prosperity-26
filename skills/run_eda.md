# Run EDA

Use this skill to turn data, logs, or run artifacts into evidence another agent can consume for understanding, strategy, specification, implementation, variants, validation, or debugging.

## Required sources

- Wiki: `../docs/prosperity_wiki/README.md`
- Datamodel and runtime: `../docs/prosperity_wiki/api/02_datamodel_reference.md`, `../docs/prosperity_wiki/api/03_runtime_and_resources.md`
- Trading signs and limits: `../docs/prosperity_wiki/trading/02_orders_and_position_limits.md`
- Active round: the relevant file in `../docs/prosperity_wiki/rounds/`
- Round state: `../rounds/round_X/workspace/_index.md` and `../rounds/round_X/workspace/phase_01_eda_context.md`
- Workflow: `../docs/prosperity_workflows/03_workstream_eda.md`
- Dataset framework: `../docs/prosperity_workflows/11_dataset_eda_framework.md`
- Template: `../docs/templates/eda_summary_template.md`

## Steps

1. Read the active round `_index.md` and EDA phase context before analyzing.
2. Prioritize EDA questions from ingestion unknowns when they could affect strategy, implementation, validation, or debugging.
3. State the exact EDA question and the downstream decision it may affect before analyzing.
4. Place or cite input artifacts under `../rounds/round_X/data/raw/`, `../rounds/round_X/data/processed/`, or `../rounds/round_X/data/external/`.
5. Cite the data, log, or run artifact path and relevant product scope, including products present, products with usable evidence, likely trader scope, and any deferred/excluded products.
6. Read wiki sources for field meanings, signs, products, limits, and runtime context.
7. Classify relevant columns with the dataset framework before choosing analyses; mark unclear meanings as open questions or blockers.
8. Quantify data quality before relying on results: row counts by file/product, timestamp coverage and gaps, missing bid/ask counts when order books are used, zero/blank `mid_price` counts when mid prices are used, and any filters applied.
9. Choose targeted checks from the EDA methodology: descriptive stats, distributions, volatility/regimes, spreads/microstructure, correlations, lead-lag, price-vs-trade alignment, volume behavior, or order book dynamics.
10. Treat feature engineering as part of EDA: test useful transformations such as spreads, returns/deltas, rolling mean/std, z-scores, normalized values, imbalance/liquidity proxies, trade-pressure proxies, fair-value deviations, and specific feature combinations.
11. Keep feature engineering targeted and hypothesis-driven. Do not brute-force feature combinations; document only useful, potentially useful, or meaningfully rejected transformations.
12. Use a stop/deepen checkpoint before adding new analysis branches: deepen only when the next check could change strategy selection, spec parameters, risk controls, validation, or debugging; otherwise stop and write the handoff.
13. Look for conditional patterns or regimes when they could affect trading: volatility, spread, liquidity, imbalance, trade-flow bursts, product-specific behavior, or plausible cross-product relationships.
14. Produce reproducible output: command notes, script, table, plot, or optional notebook. Use a notebook when exploratory code, charts, or feature experiments would help a human inspect or extend the work; keep Markdown as the canonical handoff.
15. Write EDA summaries under `../rounds/round_X/workspace/01_eda/` using `eda_<short_question>.md` and the EDA summary template.
16. Include `Product Scope`, `Data Quality And Filters`, `Feature Inventory`, `Feature Engineering Notes`, `Conditional Patterns / Regimes`, `Signal Hypotheses`, and `Downstream Use / Agent Notes`.
17. For each important feature, pattern, or signal, state what it means, why it matters, how it could be used in a strategy, limitations/caveats, and confidence level.
18. State whether each major finding uses raw rows, filtered rows, or mixed data.
19. Separate facts, conditional patterns/regimes, signal hypotheses, assumptions, open questions, and strategy interpretation.
20. State signal strength as strong, medium, weak, or contradictory, with uncertainty and limitations.
21. Prioritize the top 1-3 signal hypotheses by decision impact, and state which weak or rejected signals should not drive strategy yet.
22. Mark which signals are strong enough to consider, exploratory only, or not ready to use; include what validation is needed next.
23. Do not claim a rule or valid strategy only because a pattern appears in sample data.
24. Do not use round-local bot artifacts, performance artifacts, or `non-canonical/` drafts as truth; treat them only as named artifacts if explicitly analyzed.
25. Avoid decorative EDA: every chart, table, or metric must state what it changes, what remains uncertain, and how a downstream phase should use it.
26. Prefer fewer clear, reusable signals over many unclear findings.
27. Propose follow-up EDA only when it could materially change strategy selection, parameterization, risk controls, validation, or debugging.
28. Before closing EDA, confirm another agent can use the artifact without rerunning the analysis.
29. Confirm at least one downstream stage can use the EDA directly, or record why EDA was skipped/deferred under deadline pressure.
30. Update `../rounds/round_X/workspace/_index.md` and `../rounds/round_X/workspace/phase_01_eda_context.md`, including any resolved or new downstream-impacting unknowns.
31. Handoff with method, filters, findings, evidence limits, assumptions, linked artifacts, what to use, what not to trust yet, validation needed, and next action.
