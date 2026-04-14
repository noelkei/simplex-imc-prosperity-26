# Debug Trader

Use this skill to investigate and narrow a failing or suspicious `Trader` behavior.

## Required sources

- Contract: `../docs/prosperity_wiki/api/01_trader_contract.md`
- Datamodel and runtime: `../docs/prosperity_wiki/api/02_datamodel_reference.md`, `../docs/prosperity_wiki/api/03_runtime_and_resources.md`
- Trading rules: `../docs/prosperity_wiki/trading/01_exchange_mechanics.md`, `../docs/prosperity_wiki/trading/02_orders_and_position_limits.md`
- Active round: the relevant file in `../docs/prosperity_wiki/rounds/`
- Workflow: `../docs/prosperity_workflows/06_workstream_debugging_and_validation.md`

## Steps

1. Reproduce or describe the failure using the smallest available log, test, run artifact, or input state.
2. Compare the behavior against wiki contract, datamodel, trading rules, runtime constraints, and round limits.
3. Check empty order books, missing products, current positions, order signs, aggregate order capacity, conversions, and `traderData`.
4. Classify the issue as rule or contract failure, implementation bug, heuristic weakness, or evidence gap.
5. Make narrow fixes when executing; avoid broad strategy rewrites unless the task asks for them.
6. Do not infer official behavior from `bots/`, `performances/`, or old run outputs.
7. Handoff with reproduction, source category, fix or recommended fix, validation, and remaining caveats.
