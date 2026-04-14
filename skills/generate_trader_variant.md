# Generate Trader Variant

Use this skill to create a controlled `Trader` variant from a reviewed or deadline-deferred strategy spec.

## Required sources

- Round state: `../rounds/round_X/workspace/_index.md`
- Strategy spec: `../rounds/round_X/workspace/04_strategy_specs/`
- Parent bot, if any: `../rounds/round_X/bots/<member>/canonical/`
- Implementation workflow: `../docs/prosperity_workflows/05_workstream_bot_implementation.md`
- Trader production template: `../docs/templates/trader_production_template.md`
- Run summary template: `../docs/templates/run_summary_template.md`

## Steps

1. Confirm the parent strategy spec is `approved` or explicitly `deferred under deadline`.
2. Confirm active implementations remain at max 2 after adding the variant.
3. Choose exactly one changed axis: parameter, threshold, execution logic, risk band, or feature toggle.
4. Record parent spec, parent bot if any, changed axis, exact change, expected effect, and validation check before editing.
5. Name the variant `candidate_<id>_v01_<short_name>.py`, incrementing the variant number for the same candidate.
6. Keep the variant within the reviewed strategy hypothesis; update the spec before changing strategy direction.
7. Check Trader production readiness and contract smoke-check items before validation.
8. Do not use `non-canonical/` draft code as the parent bot unless the user explicitly points to it and the behavior is first captured in the reviewed/deferred spec.
9. Update `_index.md`, `phase_05_implementation_context.md`, and later the run summary with variant metadata and linked run.
10. Archive superseded variants under `../rounds/round_X/bots/<member>/historical/`.
