# Create Trader

Use this skill when implementing a `Trader` from a documented strategy or explicit request.

## Required sources

- Wiki: `../docs/prosperity_wiki/README.md`
- Contract: `../docs/prosperity_wiki/api/01_trader_contract.md`
- Datamodel: `../docs/prosperity_wiki/api/02_datamodel_reference.md`
- Runtime: `../docs/prosperity_wiki/api/03_runtime_and_resources.md`
- Trading rules: `../docs/prosperity_wiki/trading/01_exchange_mechanics.md`, `../docs/prosperity_wiki/trading/02_orders_and_position_limits.md`
- Active round: the relevant file in `../docs/prosperity_wiki/rounds/`
- Workflow: `../docs/prosperity_workflows/05_workstream_bot_implementation.md`

## Steps

1. Read the required sources before editing.
2. Identify the target products and limits only from the active round wiki doc.
3. Confirm the strategy is documented; if not, write the assumption explicitly before implementation.
4. Implement only against `Trader.run(state)` and the wiki datamodel.
5. Return `result, conversions, traderData` without changing the Trader interface.
6. Check order signs, position signs, aggregate order capacity, runtime, imports, and `traderData` size risk.
7. Do not use `bots/` or `performances/` as truth; inspect them only as non-authoritative local context when explicitly useful.
8. Handoff with sources used, strategy assumptions, validation performed, and remaining caveats.
