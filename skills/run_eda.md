# Run EDA

Use this skill to turn data, logs, or run artifacts into evidence for strategy or debugging.

## Required sources

- Wiki: `../docs/prosperity_wiki/README.md`
- Datamodel and runtime: `../docs/prosperity_wiki/api/02_datamodel_reference.md`, `../docs/prosperity_wiki/api/03_runtime_and_resources.md`
- Trading signs and limits: `../docs/prosperity_wiki/trading/02_orders_and_position_limits.md`
- Active round: the relevant file in `../docs/prosperity_wiki/rounds/`
- Workflow: `../docs/prosperity_workflows/03_workstream_eda.md`

## Steps

1. State the exact EDA question before analyzing.
2. Cite the data, log, or run artifact path and relevant product scope.
3. Read wiki sources for field meanings, signs, products, limits, and runtime context.
4. Produce reproducible output: command notes, script, notebook, table, or plot.
5. Separate observed evidence from strategy interpretation.
6. Do not claim a rule or valid strategy only because a pattern appears in sample data.
7. Do not use `bots/` or `performances/` as truth; treat them only as named artifacts if analyzed.
8. Handoff with method, findings, evidence limits, assumptions, and next action.
