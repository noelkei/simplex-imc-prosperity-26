# Run EDA

Use this skill to turn data, logs, or run artifacts into evidence for strategy or debugging.

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
3. State the exact EDA question before analyzing.
4. Place or cite input artifacts under `../rounds/round_X/data/raw/`, `../rounds/round_X/data/processed/`, or `../rounds/round_X/data/external/`.
5. Cite the data, log, or run artifact path and relevant product scope.
6. Read wiki sources for field meanings, signs, products, limits, and runtime context.
7. Classify relevant columns with the dataset framework before choosing analyses; mark unclear meanings as open questions or blockers.
8. Choose targeted checks from the EDA methodology: descriptive stats, distributions, volatility/regimes, spreads/microstructure, correlations, lead-lag, price-vs-trade alignment, volume behavior, or order book dynamics.
9. Add derived features only when useful for downstream decisions, such as OHLC, returns, rolling mean/std, SMA/EMA, RSI, z-scores, spread features, normalized prices, or custom hypothesis signals.
10. Produce reproducible output: command notes, script, notebook, table, or plot.
11. Write EDA summaries under `../rounds/round_X/workspace/01_eda/` using `eda_<short_question>.md` and the EDA summary template.
12. Separate facts, observations, hypotheses, assumptions, open questions, and strategy interpretation.
13. State signal strength as strong, medium, weak, or contradictory, with uncertainty and limitations.
14. Do not claim a rule or valid strategy only because a pattern appears in sample data.
15. Do not use round-local bot artifacts, performance artifacts, or `non-canonical/` drafts as truth; treat them only as named artifacts if explicitly analyzed.
16. Avoid decorative EDA: every chart, table, or metric must state what it changes, what remains uncertain, and how a downstream phase should use it.
17. Propose follow-up EDA only when it could materially change strategy selection, parameterization, risk controls, validation, or debugging.
18. Before closing EDA, confirm another agent can use the artifact without rerunning the analysis.
19. Confirm at least one downstream stage can use the EDA directly, or record why EDA was skipped/deferred under deadline pressure.
20. Update `../rounds/round_X/workspace/_index.md` and `../rounds/round_X/workspace/phase_01_eda_context.md`, including any resolved or new downstream-impacting unknowns.
21. Handoff with method, findings, evidence limits, assumptions, linked artifacts, and next action.
