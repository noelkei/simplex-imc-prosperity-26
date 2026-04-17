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

1. Read the active round `_index.md` and EDA phase context before analyzing. If `../rounds/round_X/workspace/post_run_research_memory.md` exists, read it before choosing EDA questions; treat it as evidence input and cite relevant insights when they drive EDA choices.
2. Prioritize EDA questions from ingestion unknowns when they could affect strategy, implementation, validation, or debugging.
3. State the exact EDA question and the downstream decision it may affect before analyzing.
4. Place or cite input artifacts under `../rounds/round_X/data/raw/`, `../rounds/round_X/data/processed/`, or `../rounds/round_X/data/external/`.
5. Persist reusable outputs under existing round-local paths such as `../rounds/round_X/data/processed/`, `../rounds/round_X/workspace/01_eda/`, or a nearby `artifacts/` folder when already present; do not create new top-level artifact roots.
6. Link persisted tables, plots, notebooks, scripts, processed files, and raw logs in the EDA `Artifact Index`; do not rely on terminal output as durable evidence.
7. Cite the data, log, or run artifact path and relevant product scope, including products present, products with usable evidence, likely trader scope, and any deferred/excluded products.
8. Separate algorithmic findings usable by `Trader.run()` from manual-challenge findings when both exist.
9. Read wiki sources for field meanings, signs, products, limits, and runtime context.
10. Classify relevant columns with the dataset framework before choosing analyses; mark unclear meanings as open questions or blockers.
11. Quantify data quality before relying on results: row counts by file/product, timestamp coverage and gaps, missing bid/ask counts when order books are used, zero/blank `mid_price` counts when mid prices are used, and any filters applied.
12. Choose targeted checks from the EDA methodology: descriptive stats, distributions, volatility/regimes, spreads/microstructure, correlations, lead-lag, price-vs-trade alignment, volume behavior, or order book dynamics.
13. Treat feature engineering as part of EDA: test useful transformations such as spreads, returns/deltas, rolling mean/std, z-scores, normalized values, imbalance/liquidity proxies, trade-pressure proxies, fair-value deviations, and specific feature combinations.
14. Keep feature engineering targeted and hypothesis-driven. Do not brute-force feature combinations; document only useful, potentially useful, or meaningfully rejected transformations.
15. Include lightweight distribution hypotheses and threshold/execution observations only when they could change strategy, risk, parameterization, or validation.
16. Use a stop/deepen checkpoint before adding new analysis branches: deepen only when the next check could change strategy selection, spec parameters, risk controls, validation, or debugging; otherwise stop and write the handoff.
17. Look for conditional patterns or regimes when they could affect trading: volatility, spread, liquidity, imbalance, trade-flow bursts, product-specific behavior, or plausible cross-product relationships.
18. Produce reproducible output: command notes, script, table, plot, or optional notebook. Use a notebook when exploratory code, charts, or feature experiments would help a human inspect or extend the work; keep Markdown as the canonical handoff.
19. Write EDA summaries under `../rounds/round_X/workspace/01_eda/` using `eda_<short_question>.md` and the EDA summary template.
20. Include `Product Scope`, `Algorithmic vs Manual Scope`, `Artifact Index`, `Data Quality And Filters`, `Feature Inventory`, `Feature Engineering Notes`, `Distribution Hypotheses`, `Conditional Patterns / Regimes`, `Threshold / Execution Findings`, `Signal Hypotheses`, `Negative Evidence`, and `Downstream Use / Agent Notes`.
21. For each important feature, pattern, or signal, state what it means, why it matters, how it could be used in a strategy, limitations/caveats, and confidence level.
22. State whether each major finding uses raw rows, filtered rows, or mixed data.
23. Separate facts, conditional patterns/regimes, signal hypotheses, assumptions, open questions, and strategy interpretation.
24. State signal strength as strong, medium, weak, or contradictory, with uncertainty and limitations.
25. Prioritize the top 1-3 signal hypotheses by decision impact, and state which weak or rejected signals should not drive strategy yet.
26. Record negative evidence for meaningful failed checks, including why the idea was plausible and when it should be reopened; do not document every tiny dead end. Avoid rediscovering ideas already marked weak in post-run memory unless reopen conditions are met.
27. Mark which signals are strong enough to consider, exploratory only, or not ready to use; include what validation is needed next.
28. Do not claim a rule or valid strategy only because a pattern appears in sample data.
29. Do not use round-local bot artifacts, performance artifacts, or `non-canonical/` drafts as truth; treat them only as named artifacts if explicitly analyzed.
30. Avoid decorative EDA: every chart, table, or metric must state what it changes, what remains uncertain, and how a downstream phase should use it.
31. Prefer fewer clear, reusable signals over many unclear findings.
32. Propose follow-up EDA only when it could materially change strategy selection, parameterization, risk controls, validation, or debugging.
33. Before closing EDA, confirm another agent can use the artifact without rerunning the analysis.
34. Confirm at least one downstream stage can use the EDA directly, or record why EDA was skipped/deferred under deadline pressure.
35. Update `../rounds/round_X/workspace/_index.md` and `../rounds/round_X/workspace/phase_01_eda_context.md`, including any resolved or new downstream-impacting unknowns.
36. Handoff with method, filters, linked artifacts, findings, evidence limits, negative evidence, assumptions, what to use, what not to trust yet, validation needed, and next action.
