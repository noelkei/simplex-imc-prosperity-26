# Create Trader

Use this skill when implementing a `Trader` from a documented strategy or explicit request.

## Required sources

- Wiki: `../docs/prosperity_wiki/README.md`
- Contract: `../docs/prosperity_wiki/api/01_trader_contract.md`
- Datamodel: `../docs/prosperity_wiki/api/02_datamodel_reference.md`
- Runtime: `../docs/prosperity_wiki/api/03_runtime_and_resources.md`
- Trading rules: `../docs/prosperity_wiki/trading/01_exchange_mechanics.md`, `../docs/prosperity_wiki/trading/02_orders_and_position_limits.md`
- Active round: the relevant file in `../docs/prosperity_wiki/rounds/`
- Round state: `../rounds/round_X/workspace/_index.md` and `../rounds/round_X/workspace/phase_05_implementation_context.md`
- Strategy specs: `../rounds/round_X/workspace/04_strategy_specs/`
- Round bots: `../rounds/round_X/bots/<member>/`
- Trader production template: `../docs/templates/trader_production_template.md`
- Workflow: `../docs/prosperity_workflows/05_workstream_bot_implementation.md`

## Steps

1. Read the required sources before editing.
2. Identify the target products and limits only from the active round wiki doc.
3. Confirm `_index.md` records the candidate spec status as `approved` or explicitly `deferred under deadline`; if not, create or request a one-page spec review before implementation instead of skipping the gate.
4. Confirm a reviewed or deadline-deferred strategy spec exists. If it does not, create or request a one-page spec before implementation.
5. Check the spec defines signal/fair value, linked EDA signals, feature evidence, regime assumptions, understanding insight, Feature Contract, execution, missing-signal behavior, risk/position handling, state/runtime, expected failures, and validation checks.
6. Confirm implemented features match the spec Feature Contract: source fields, online availability, role, parameters, missing-signal fallback, `traderData` state, and validation check.
7. Confirm the implementation matches the spec Round-Specific Mechanics Contract: implemented mechanics are present, excluded mechanics are absent, and not-applicable mechanics are not hardcoded.
8. Confirm no CSV-only or EDA-only feature is hardcoded into trading behavior unless the spec defines an online proxy or explicitly deadline-defers the risk.
9. Confirm no stale prior-round product symbols, limits, fair values, constants, or mechanics are used unless the spec cites current-round evidence or labels the assumption.
10. If implementation reveals a missing assumption or ambiguous behavior, return to the spec instead of inventing behavior in code.
11. Determine the owning member from the round index, task request, or current phase owner. Use one of `isaac`, `bruno`, `amin`, `daniela`, or `noel`; ask only if ownership is unclear and matters for handoff.
12. Implement candidate bots under `../rounds/round_X/bots/<member>/canonical/` using `candidate_<candidate_id>_<short_name>.py`; use `baseline_<short_name>.py` only for baseline/reference bots.
13. Implement only against `Trader.run(state)` and the wiki datamodel.
14. Return `result, conversions, traderData` without changing the Trader interface.
15. Check order signs, position signs, aggregate order capacity, runtime, imports, `traderData` size risk, missing products, empty books, missing signals, and round-specific mechanics/functions named in the spec.
16. Use `../docs/templates/trader_production_template.md` for the submission readiness checklist and contract smoke-check guidance.
17. Do not use removed legacy top-level artifacts, round-local outputs, or `non-canonical/` drafts as truth; inspect `non-canonical/` only when the user explicitly points to a draft.
18. Link the implementation to the reviewed strategy spec and update `../rounds/round_X/workspace/_index.md` and `../rounds/round_X/workspace/phase_05_implementation_context.md`.
19. Handoff with sources used, owner/member, bot path, linked strategy spec, implemented insight, implemented features and roles, contract readiness status, strategy assumptions, validation performed, and remaining caveats.
