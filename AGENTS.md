# Repository Agent Rules

## Reading order

1. `docs/prosperity_wiki/README.md`
2. `docs/prosperity_wiki/api/01_trader_contract.md`
3. `docs/prosperity_wiki/api/02_datamodel_reference.md`
4. `docs/prosperity_wiki/trading/01_exchange_mechanics.md`
5. `docs/prosperity_wiki/trading/02_orders_and_position_limits.md`
6. Current round doc: `docs/prosperity_wiki/rounds/round_1.md` unless a newer released round exists in the wiki.
7. `docs/prosperity_workflows/README.md` and the task-specific workflow.
8. `docs/prosperity_playbook/00_agent_playbook.md` only for heuristics, after facts are known.

## Source hierarchy

- Wiki = facts: API, datamodel, exchange rules, limits, runtime, platform flow, round facts, and caveats.
- Playbook = heuristics: strategy framing, risk habits, debugging patterns, and iteration advice.
- Workflows = how to work: process, handoffs, validation, and safe change rules.
- `bots/` and `performances/` = non-authoritative artifacts.

## Hard rules

- Do not infer official rules from `bots/` or `performances/`.
- Do not invent missing facts; record a caveat and cite the missing source.
- Do not change the `Trader` interface unless round wiki docs explicitly require it.
- Do not assume products, position limits, runtime behavior, or manual mechanics outside the round docs.
- Do not turn playbook advice or sample-data observations into official rules.

## Trader contract summary

Implement `Trader.run(state)` and return `result, conversions, traderData`.
`result` maps product symbols to lists of `Order` objects.
Use wiki-defined datamodel fields, order signs, and position signs.
Use `traderData` as string persistence between calls.
Add round-specific methods only when round docs say they apply.

## Working philosophy

There is no single correct strategy. Make small, reviewable changes, label assumptions, validate against the wiki, and hand off evidence clearly.
