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
3. Confirm `_index.md` records the candidate spec status as `approved` or explicitly `deferred`; if not, create or request a one-page spec review before implementation instead of skipping the gate.
4. Confirm a reviewed or deadline-deferred strategy spec exists. If it does not, create or request a one-page spec before implementation.
5. Check the spec defines signal/fair value, execution, missing-signal behavior, risk/position handling, state/runtime, expected failures, and validation checks.
6. If implementation reveals a missing assumption or ambiguous behavior, return to the spec instead of inventing behavior in code.
7. Determine the owning member from the round index, task request, or current phase owner. Use one of `isaac`, `bruno`, `amin`, `daniela`, or `noel`; ask only if ownership is unclear and matters for handoff.
8. Implement candidate bots under `../rounds/round_X/bots/<member>/canonical/` using `candidate_<candidate_id>_<short_name>.py`; use `baseline_<short_name>.py` only for baseline/reference bots.
9. Implement only against `Trader.run(state)` and the wiki datamodel.
10. Return `result, conversions, traderData` without changing the Trader interface.
11. Check order signs, position signs, aggregate order capacity, runtime, imports, `traderData` size risk, missing products, empty books, missing signals, and round-specific methods such as `bid()`.
12. Use `../docs/templates/trader_production_template.md` for the submission readiness checklist and contract smoke-check guidance.
13. Do not use removed legacy top-level artifacts, round-local outputs, or `non-canonical/` drafts as truth; inspect `non-canonical/` only when the user explicitly points to a draft.
14. Link the implementation to the reviewed strategy spec and update `../rounds/round_X/workspace/_index.md` and `../rounds/round_X/workspace/phase_05_implementation_context.md`.
15. Handoff with sources used, owner/member, bot path, linked strategy spec, contract readiness status, strategy assumptions, validation performed, and remaining caveats.
