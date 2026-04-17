# Generate Trader Variant

Use this skill to create a controlled `Trader` variant from a reviewed or deadline-deferred strategy spec.

## Required sources

- Round state: `../rounds/round_X/workspace/_index.md`
- Strategy spec: `../rounds/round_X/workspace/04_strategy_specs/`
- Understanding: `../rounds/round_X/workspace/02_understanding.md`
- EDA summaries: `../rounds/round_X/workspace/01_eda/`
- Post-run research memory, when present: `../rounds/round_X/workspace/post_run_research_memory.md`
- Parent bot, if any: `../rounds/round_X/bots/<member>/canonical/`
- Implementation workflow: `../docs/prosperity_workflows/05_workstream_bot_implementation.md`
- Trader production template: `../docs/templates/trader_production_template.md`
- Run summary template: `../docs/templates/run_summary_template.md`

## Steps

1. Confirm the parent strategy spec is `approved` or explicitly `deferred under deadline`.
2. If `../rounds/round_X/workspace/post_run_research_memory.md` exists, read it before proposing variants; prefer counterfactual backlog and failure patterns for one-axis variant selection, and cite relevant insights when they justify the changed axis.
3. Confirm active implementations remain at max 2 after adding the variant.
4. Identify the current champion or parent bot. If a platform-validated strong champion exists, default to 1-3 variants in the batch and do not create broad parameter sweeps unless explicitly requested.
5. Run variant ROI triage before coding:
   - What weakness of the champion does this target?
   - What exactly changes?
   - Why should this have practical ROI?
   - Why is it not redundant with recent variants?
   - What result would make us discard it?
   - What is the max number of variants in this batch?
6. Choose exactly one changed axis: parameter, threshold, execution logic, risk band, or feature toggle.
7. Record parent spec, parent bot if any, variant hypothesis, linked signal or regime assumption, post-run memory insight if used, insight being tested, changed axis, exact change, expected effect based on EDA/understanding, falsification metric, and validation check before editing.
8. Name the variant `candidate_<id>_v01_<short_name>.py`, incrementing the variant number for the same candidate.
9. Keep the variant within the reviewed strategy hypothesis; update the spec before changing strategy direction or testing a new signal, feature relationship, or regime assumption.
10. Do not create performance-only parameter fishing variants. If the variant cannot name a falsification metric or practical ROI, route back to spec, strategy, or EDA.
11. Check Trader production readiness and contract smoke-check items before validation.
12. Do not use `non-canonical/` draft code as the parent bot unless the user explicitly points to it and the behavior is first captured in the reviewed/deferred spec.
13. Update `_index.md`, `phase_05_implementation_context.md`, and later the run summary with variant metadata and linked run.
14. Archive superseded variants under `../rounds/round_X/bots/<member>/historical/`.
