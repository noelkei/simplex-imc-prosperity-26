# Validate Trader

Use this skill to review a `Trader` implementation for contract, rule, and evidence issues.

## Required sources

- Wiki: `../docs/prosperity_wiki/README.md`
- Contract and datamodel: `../docs/prosperity_wiki/api/01_trader_contract.md`, `../docs/prosperity_wiki/api/02_datamodel_reference.md`
- Runtime: `../docs/prosperity_wiki/api/03_runtime_and_resources.md`
- Trading rules: `../docs/prosperity_wiki/trading/01_exchange_mechanics.md`, `../docs/prosperity_wiki/trading/02_orders_and_position_limits.md`
- Active round: the relevant file in `../docs/prosperity_wiki/rounds/`
- Round state: `../rounds/round_X/workspace/_index.md` and `../rounds/round_X/workspace/phase_06_testing_context.md`
- Linked strategy spec, including its EDA and understanding references when evaluating behavior evidence.
- Round performances: `../rounds/round_X/performances/<member>/canonical/` and `../rounds/round_X/performances/<member>/historical/`
- Template: `../docs/templates/run_summary_template.md`
- Trader production template: `../docs/templates/trader_production_template.md`
- Workflow: `../docs/prosperity_workflows/06_workstream_debugging_and_validation.md`

## Steps

1. Read the required sources and the implementation under review.
2. Check that `Trader.run(state)` returns `result, conversions, traderData`.
3. Check product symbols, datamodel fields, order signs, position signs, and aggregate order capacity against wiki and round docs.
4. Check imports, runtime cost, logging volume, `traderData` serialization/size assumptions, missing products, empty books, missing signals, and round-specific methods such as `bid()`.
5. Confirm the implementation links to a reviewed strategy spec or record this as a workflow blocker.
6. Apply the contract smoke-check guidance from `../docs/templates/trader_production_template.md`.
7. Review tests, logs, sample-data output, performance summaries, or platform feedback if provided.
8. Classify failures as rule or contract failure, implementation bug, data/EDA gap, heuristic weakness, execution tuning issue, evidence gap, or deadline tradeoff.
9. Do not treat round-local artifacts, `non-canonical/` drafts, or sample PnL as official rules.
10. Determine the owning member from the bot path, round index, task request, or current phase owner. Use one of `isaac`, `bruno`, `amin`, `daniela`, or `noel`; ask only if ownership is unclear and matters for handoff.
11. Write current decision-supporting run summaries under `../rounds/round_X/performances/<member>/canonical/` using `run_YYYYMMDD_HHMM_<candidate_id>.md` or `run_YYYYMMDD_HHMM_<candidate_id>_<issue_id>.md`.
12. Include bot path, linked spec, insight being tested when applicable, linked signal/regime assumption, raw artifact path if available, run id, metrics, errors/rejections/limit concerns, comparability, contract readiness status, interpretation limits, signal/regime evidence verdict, decision, and next action.
13. Record whether the run is comparable to the baseline or prior run as `yes`, `no`, or `unclear`; non-comparable runs can support debugging but should not drive promotion without an explicit caveat.
14. State whether validation supports, weakens, contradicts, or does not test the linked signal/regime assumption, with a brief basis.
15. Promote a candidate only when the evidence summary includes linked spec, bot path, contract/rule checks, one meaningful run or validation summary, concerns/caveats, and an explicit continue/promote/debug/discard/revise/rerun/stop decision.
16. Move or mark superseded, non-comparable, stale, or no-longer-decision-relevant summaries under `../rounds/round_X/performances/<member>/historical/`.
17. If valid behavior performs poorly, suggest returning to strategy/spec rather than treating the result as an implementation bug by default.
18. If validation contradicts the linked signal/regime assumption, route to strategy/spec or EDA before changing code unless there is also a rule or implementation failure.
19. Update `../rounds/round_X/workspace/_index.md` and `../rounds/round_X/workspace/phase_06_testing_context.md`, including latest validation run reference, comparability, contract readiness status, decision, and one-line note.
20. Report pass/fail, sources checked, linked spec/run if available, reproduction steps, caveats, and next action.
