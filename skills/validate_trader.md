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
- Post-run memory template: `../docs/templates/post_run_research_memory_template.md`
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
8. Determine the PnL source: `real platform PnL`, `calibrated proxy`, or `weak proxy`. Real platform JSON `profit` ranks first whenever available; final `activitiesLog` product rows provide product attribution.
9. If using a proxy, state confidence `high`, `medium`, or `low`, the evidence basis, the decision use, and the caveat. Proxy PnL may prioritize uploads, filter weak candidates, or guide debugging, but it is not real PnL.
10. Compare against the current champion when one exists. State the challenger, decision versus champion (`promote`, `backup`, `fallback`, `reject`, or `rerun`), and final candidate class (`primary`, `backup`, `fallback`, `reject`, or `experimental`).
11. For serious promotion decisions, extract practical run diagnostics when artifacts allow: product PnL split, final positions, own trades, buy/sell qty, matched qty, average buy/sell, gross spread capture, max drawdown, max abs position, and inventory/mark caveats. Mark unavailable fields as missing rather than blocking validation.
12. When platform `.json` or `.log` artifacts exist, fill the run summary `Post-Run Research` section with failure-driven analysis, edge decomposition, lightweight counterfactuals, and `Memory update: added | updated | no change`.
13. Update or create `../rounds/round_X/workspace/post_run_research_memory.md` only when the run adds reusable insight such as champion change, failure pattern, edge explanation, counterfactual backlog item, or negative evidence. Link each aggregate insight back to the per-run summary or raw artifacts.
14. Record a provenance caveat if the exact `.py`, platform `.json`, and platform `.log` are not saved together. Missing one artifact does not block analysis, but the caveat must be visible.
15. For final upload candidates, run the pre-upload overfit / cheat audit from `../docs/templates/trader_production_template.md` and report `passed`, `failed`, or `caveat`.
16. Classify failures as rule or contract failure, implementation bug, data/EDA gap, heuristic weakness, execution tuning issue, evidence gap, or deadline tradeoff.
17. Do not treat round-local artifacts, `non-canonical/` drafts, sample PnL, uncalibrated replay, or post-run memory as official rules.
18. Determine the owning member from the bot path, round index, task request, or current phase owner. Use one of `isaac`, `bruno`, `amin`, `daniela`, or `noel`; ask only if ownership is unclear and matters for handoff.
19. Write current decision-supporting run summaries under `../rounds/round_X/performances/<member>/canonical/` using `run_YYYYMMDD_HHMM_<candidate_id>.md` or `run_YYYYMMDD_HHMM_<candidate_id>_<issue_id>.md`.
20. Include bot path, linked spec, insight being tested when applicable, linked signal/regime assumption, raw artifact path if available, run id, PnL source, diagnostics, errors/rejections/limit concerns, comparability, contract readiness status, overfit/cheat audit outcome when applicable, post-run research memory update, interpretation limits, signal/regime evidence verdict, decision, and next action.
21. Record whether the run is comparable to the baseline or prior run as `yes`, `no`, or `unclear`; non-comparable runs can support debugging but should not drive promotion without an explicit caveat.
22. State whether validation supports, weakens, contradicts, or does not test the linked signal/regime assumption, with a brief basis.
23. Promote a candidate only when the evidence summary includes linked spec, bot path, contract/rule checks, one meaningful run or validation summary, concerns/caveats, PnL source, champion/challenger decision, and an explicit continue/promote/debug/discard/revise/rerun/stop decision.
24. Move or mark superseded, non-comparable, stale, or no-longer-decision-relevant summaries under `../rounds/round_X/performances/<member>/historical/`.
25. If valid behavior performs poorly, suggest returning to strategy/spec rather than treating the result as an implementation bug by default.
26. If validation contradicts the linked signal/regime assumption, route to strategy/spec or EDA before changing code unless there is also a rule or implementation failure.
27. Update `../rounds/round_X/workspace/_index.md` and `../rounds/round_X/workspace/phase_06_testing_context.md`, including latest validation run reference, PnL source, comparability, contract readiness status, memory update when decision-relevant, decision, and one-line note.
28. Report pass/fail, sources checked, linked spec/run if available, reproduction steps, caveats, PnL source, candidate class, memory update, and next action.
