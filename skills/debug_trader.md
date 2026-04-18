# Debug Trader

Use this skill to investigate and narrow a failing or suspicious `Trader` behavior.

## Required sources

- Contract: `../docs/prosperity_wiki/api/01_trader_contract.md`
- Datamodel and runtime: `../docs/prosperity_wiki/api/02_datamodel_reference.md`, `../docs/prosperity_wiki/api/03_runtime_and_resources.md`
- Trading rules: `../docs/prosperity_wiki/trading/01_exchange_mechanics.md`, `../docs/prosperity_wiki/trading/02_orders_and_position_limits.md`
- Active round: the relevant file in `../docs/prosperity_wiki/rounds/`
- Round state: `../rounds/round_X/workspace/_index.md` and `../rounds/round_X/workspace/phase_07_debugging_context.md`
- Current run evidence: `../rounds/round_X/performances/<member>/canonical/`
- Debug notes: `../rounds/round_X/workspace/06_debugging/`
- Template: `../docs/templates/debug_issue_template.md`
- Workflow: `../docs/prosperity_workflows/06_workstream_debugging_and_validation.md`

## Steps

1. Reproduce or describe the failure using the smallest available log, test, run artifact, or input state.
2. Determine the owning member from the linked run, bot path, round index, task request, or current phase owner. Use one of `isaac`, `bruno`, `amin`, `daniela`, or `noel`; ask only if ownership is unclear and matters for handoff.
3. Link the strategy spec and canonical performance/validation run that exposed the issue, or record the missing link as a blocker.
4. State expected behavior and observed behavior before proposing a fix.
5. Compare the behavior against wiki contract, datamodel, trading rules, runtime constraints, round limits, and the spec Round-Specific Mechanics Contract.
6. Check empty order books, missing products, current positions, order signs, aggregate order capacity, conversions, `traderData`, and stale prior-round constants or mechanics.
7. Classify the issue as rule or contract failure, implementation bug, data/EDA gap, heuristic weakness, execution tuning issue, or evidence gap.
8. Make narrow fixes when executing; avoid broad strategy rewrites unless the task asks for them.
9. Do not infer official behavior from round-local bot artifacts, performance artifacts, `non-canonical/` drafts, or old run outputs.
10. Write debugging notes under `../rounds/round_X/workspace/06_debugging/` using `issue_<candidate_id>_<short_issue>.md`.
11. Each issue must include linked spec, linked run summary, bot path, reproduction steps, expected vs observed behavior, classification, fix or recommendation, validation, and next action.
12. Reroute by classification: rule/contract failures go to implementation or ingestion, implementation bugs get narrow fixes, data gaps go to EDA, heuristic weaknesses go to strategy/spec, tuning issues get low-risk parameter changes, and evidence gaps need clearer reproduction.
13. Update `../rounds/round_X/workspace/_index.md` and `../rounds/round_X/workspace/phase_07_debugging_context.md`.
14. Handoff with reproduction, expected vs observed behavior, linked spec/run, source category, fix or recommended fix, validation, and remaining caveats.
