# Validate Trader

Use this skill to review a `Trader` implementation for contract, rule, and evidence issues.

## Required sources

- Wiki: `../docs/prosperity_wiki/README.md`
- Contract and datamodel: `../docs/prosperity_wiki/api/01_trader_contract.md`, `../docs/prosperity_wiki/api/02_datamodel_reference.md`
- Runtime: `../docs/prosperity_wiki/api/03_runtime_and_resources.md`
- Trading rules: `../docs/prosperity_wiki/trading/01_exchange_mechanics.md`, `../docs/prosperity_wiki/trading/02_orders_and_position_limits.md`
- Active round: the relevant file in `../docs/prosperity_wiki/rounds/`
- Workflow: `../docs/prosperity_workflows/06_workstream_debugging_and_validation.md`

## Steps

1. Read the required sources and the implementation under review.
2. Check that `Trader.run(state)` returns `result, conversions, traderData`.
3. Check product symbols, datamodel fields, order signs, position signs, and aggregate order capacity against wiki and round docs.
4. Check imports, runtime cost, logging volume, and `traderData` serialization/size assumptions.
5. Review tests, logs, sample-data output, or platform feedback if provided.
6. Classify failures as rule or contract failure, implementation bug, heuristic weakness, or evidence gap.
7. Do not treat `bots/`, `performances/`, or sample PnL as official rules.
8. Report pass/fail, sources checked, reproduction steps, caveats, and next action.
