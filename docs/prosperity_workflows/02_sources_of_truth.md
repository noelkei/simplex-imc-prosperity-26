# Sources of Truth

Use source categories deliberately. Mixing factual rules with heuristics makes handoffs unsafe.

## Factual source: wiki

[`../prosperity_wiki/`](../prosperity_wiki/) is the factual source for:

- `Trader.run()` contract, return shape, `traderData`, and datamodel fields.
- Order signs, position signs, matching rules, resting order behavior, and position-limit enforcement.
- Runtime constraints, supported libraries, persistence constraints, sample data, and logs.
- Platform submission flow, active-file behavior, and round schedule facts.
- Round-specific products, limits, manual mechanics, and source caveats.

When implementing or validating behavior, prefer the wiki critical path:

- [`../prosperity_wiki/api/01_trader_contract.md`](../prosperity_wiki/api/01_trader_contract.md)
- [`../prosperity_wiki/api/02_datamodel_reference.md`](../prosperity_wiki/api/02_datamodel_reference.md)
- [`../prosperity_wiki/api/03_runtime_and_resources.md`](../prosperity_wiki/api/03_runtime_and_resources.md)
- [`../prosperity_wiki/trading/01_exchange_mechanics.md`](../prosperity_wiki/trading/01_exchange_mechanics.md)
- [`../prosperity_wiki/trading/02_orders_and_position_limits.md`](../prosperity_wiki/trading/02_orders_and_position_limits.md)
- The active round file under [`../prosperity_wiki/rounds/`](../prosperity_wiki/rounds/)

## Heuristic source: playbook

[`../prosperity_playbook/`](../prosperity_playbook/) is guidance for judgment, not official fact.

Use it for:

- Strategy framing such as fair value, inventory control, execution, and iteration.
- Debugging habits such as using logs and sample data.
- Risk priorities such as avoiding position-limit violations and over-complexity.
- Research direction when the wiki gives facts but not strategy choices.

Do not turn playbook advice into official rules. If a strategy uses playbook guidance, label it as a heuristic assumption.

## Non-sources

Do not use round-local artifacts, `non-canonical/` drafts, removed top-level execution artifacts, external material, or remembered Prosperity behavior as authority for official rules. Repo-local code and run outputs can show local artifacts, but they cannot define what Prosperity requires.

## Caveat rule

If a fact is absent, inconsistent, or unclear, write down the uncertainty. The safe output is a caveat plus a next step, not an invented rule.
