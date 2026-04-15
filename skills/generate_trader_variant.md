# Generate Trader Variant

Use this skill to create a controlled `Trader` variant from a reviewed or deadline-deferred strategy spec.

## Required sources

- Round state: `../rounds/round_X/workspace/_index.md`
- Strategy spec: `../rounds/round_X/workspace/04_strategy_specs/`
- Understanding: `../rounds/round_X/workspace/02_understanding.md`
- EDA summaries: `../rounds/round_X/workspace/01_eda/`
- Parent bot, if any: `../rounds/round_X/bots/<member>/canonical/`
- Implementation workflow: `../docs/prosperity_workflows/05_workstream_bot_implementation.md`
- Trader production template: `../docs/templates/trader_production_template.md`
- Run summary template: `../docs/templates/run_summary_template.md`

## Steps

1. Confirm the parent strategy spec is `approved` or explicitly `deferred under deadline`.
2. Confirm active implementations remain at max 2 after adding the variant.
3. Choose exactly one changed axis: parameter, threshold, execution logic, risk band, or feature toggle.
4. Record parent spec, parent bot if any, variant hypothesis, linked signal or regime assumption, insight being tested, changed axis, exact change, expected effect based on EDA/understanding, falsification metric, and validation check before editing.
5. Name the variant `candidate_<id>_v01_<short_name>.py`, incrementing the variant number for the same candidate.
6. Keep the variant within the reviewed strategy hypothesis; update the spec before changing strategy direction or testing a new signal, feature relationship, or regime assumption.
7. Do not create performance-only parameter fishing variants. If the variant cannot name a falsification metric, route back to spec, strategy, or EDA.
8. Check Trader production readiness and contract smoke-check items before validation.
9. Do not use `non-canonical/` draft code as the parent bot unless the user explicitly points to it and the behavior is first captured in the reviewed/deferred spec.
10. Update `_index.md`, `phase_05_implementation_context.md`, and later the run summary with variant metadata and linked run.
11. Archive superseded variants under `../rounds/round_X/bots/<member>/historical/`.
