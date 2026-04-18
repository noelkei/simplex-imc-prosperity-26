# Prosperity Agent Wiki

This wiki is the operational factual source for coding agents implementing Prosperity trading algorithms in this repository.

It reorganizes the raw Prosperity wiki into small, task-oriented files:

- API contracts and data structures
- exchange mechanics and position-limit rules
- platform submission flow
- per-round product and challenge facts
- general reference material

## Source of truth

Use `docs/prosperity_wiki/` as the operational source for facts during normal work.

Use `docs/prosperity_wiki_raw/` as the underlying factual base when curating, checking, or updating wiki pages.

Do not add official facts to the curated wiki unless they are supported by `docs/prosperity_wiki_raw/` or by another accepted factual source explicitly added to the repo workflow.

Do not use:

- round-local `rounds/round_X/bots/`
- round-local `rounds/round_X/performances/`
- `non-canonical/`
- `docs/prosperity_playbook/`
- external sources

## Agent rules

- Do not hallucinate missing facts.
- Do not infer unstated values or behavior.
- Do not add trading strategies or heuristics.
- Preserve API names, product symbols, field names, numbers, dates, and currency names exactly.
- If the source is inconsistent, document it as a source caveat.

## How to use this wiki (for coding agents)

- Start with the critical path: `api/01_trader_contract.md`, `api/02_datamodel_reference.md`, `trading/01_exchange_mechanics.md`, `trading/02_orders_and_position_limits.md`, and the active round file under `rounds/`.
- Treat `api/03_runtime_and_resources.md` as critical when implementing persistence, conversions, imports, logging, or performance-sensitive code.
- Treat `platform/`, `reference/`, `rounds_future/`, and `appendix/` as optional unless the task involves submission workflow, schedule, glossary terms, future round documentation, or competition context.
- Combine files by role: use `api/` for callable interfaces and datamodel fields, `trading/` for exchange and risk rules, and `rounds/` for product symbols, position limits, and round-specific manual mechanics.
- Do not infer product behavior, limits, API fields, conversion behavior, or runtime constraints from examples, repo-local bot implementations, performance outputs, or external knowledge.
- If a needed fact is absent or inconsistent, preserve the uncertainty and mark it as a source caveat instead of filling the gap.

## Recommended reading order

1. [api/01_trader_contract.md](api/01_trader_contract.md)
2. [api/02_datamodel_reference.md](api/02_datamodel_reference.md)
3. [trading/01_exchange_mechanics.md](trading/01_exchange_mechanics.md)
4. [trading/02_orders_and_position_limits.md](trading/02_orders_and_position_limits.md)
5. [platform/01_submission_flow.md](platform/01_submission_flow.md)
6. [rounds/tutorial.md](rounds/tutorial.md)
7. [rounds/round_1.md](rounds/round_1.md)
8. [rounds/round_2.md](rounds/round_2.md)

## Directory map

- `api/`: trader interface, datamodel, runtime constraints, and resources.
- `trading/`: exchange behavior, order mechanics, and position-limit enforcement.
- `platform/`: submission workflow and platform UI features.
- `reference/`: round schedule and trading glossary.
- `rounds/`: released round-specific facts.
- `rounds_future/`: instructions for documenting future rounds.
- `appendix/`: brief non-critical competition context.
