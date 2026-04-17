# Repository Agent Rules

## Reading order

1. `docs/prosperity_wiki/README.md`
2. `docs/prosperity_wiki/api/01_trader_contract.md`
3. `docs/prosperity_wiki/api/02_datamodel_reference.md`
4. `docs/prosperity_wiki/trading/01_exchange_mechanics.md`
5. `docs/prosperity_wiki/trading/02_orders_and_position_limits.md`
6. Current round doc under `docs/prosperity_wiki/rounds/` when the task names or implies an active round.
7. `docs/prosperity_workflows/README.md` and the task-specific workflow.
8. `docs/prosperity_workflows/10_time_aware_team_pipeline.md` when the task involves round execution, phase status, implementation readiness, validation, or deadline tradeoffs.
9. Task-specific repo skill under `skills/` when the task matches one.
10. Current round README: `rounds/round_X/README.md` when working on a round.
11. Current round control panel: `rounds/round_X/workspace/_index.md`.
12. Current phase context: `rounds/round_X/workspace/phase_YY_*_context.md` if it matches the task.
13. `non-canonical/<member>/` only when the user explicitly points to a specific draft.
14. `docs/prosperity_playbook/00_agent_playbook.md` only for heuristics, after facts are known.

## Source hierarchy

- Wiki = facts: API, datamodel, exchange rules, limits, runtime, platform flow, round facts, and caveats.
- Playbook = heuristics: strategy framing, risk habits, debugging patterns, and iteration advice.
- Workflows = how to work: process, handoffs, validation, and safe change rules.
- Round-local bot/performance folders = non-authoritative execution artifacts.
- `non-canonical/` = informal personal scratch space, outside the formal workflow.

## Hard rules

- Do not infer official rules from round-local bots or performance outputs.
- Do not use `non-canonical/` as evidence, examples, or reference implementations unless the user explicitly points to a specific file; even then, treat it as non-authoritative context.
- Do not recreate top-level `bots/` or `performances/`; active execution artifacts belong under `rounds/round_X/`.
- Put new round-local bot and performance artifacts under `rounds/round_X/{bots,performances}/<member>/canonical/`; archive superseded work under the same member's `historical/` folder. Supported members are `isaac`, `bruno`, `amin`, `daniela`, and `noel`.
- Do not invent missing facts; record a caveat and cite the missing source.
- Do not change the `Trader` interface unless round wiki docs explicitly require it.
- Do not assume products, position limits, runtime behavior, or manual mechanics outside the round docs.
- Do not turn playbook advice or sample-data observations into official rules.
- Do not implement a strategy without a reviewed strategy spec; in fast mode, create or request a one-page spec rather than skipping the gate.
- Treat EDA as targeted signal discovery: state the decision it may affect, use hypothesis-driven feature engineering, classify signals as usable, exploratory, or not ready, and stop when more analysis will not change the next decision.
- Ground strategy candidates, specs, and variants in linked EDA signals, feature evidence, regime assumptions, and understanding insights when those artifacts exist; otherwise label the missing evidence as an assumption or route it to targeted EDA.
- When `rounds/round_X/workspace/post_run_research_memory.md` exists for the active round, read it before EDA, understanding, strategy generation, spec writing, or trader variant work. Treat it as evidence input, not passive documentation; cite relevant insight IDs or descriptions when they influence decisions. Missing memory does not block work; record the absence only when it affects confidence or direction.
- Consume current phase artifacts before rethinking earlier phases. Reopen an earlier phase only when material new evidence, a blocker, implementation behavior, validation, or debugging changes the decision.
- Write phase artifacts for downstream agents. EDA and understanding should make clear what to use, what not to trust yet, and what to validate next.
- Do not treat a final submission as ready without a readable validation or performance summary.
- Keep `rounds/round_X/workspace/_index.md` and the relevant phase context current when changing phase status, active strategies, implementations, blockers, or final submission decisions.
- Use `skills/manage_phase_state.md` when starting, resuming after a time gap, closing, detecting inconsistency, or repairing drift in a phase; do not silently update only one of `_index.md`, the phase context, or the main artifact.
- Before changing or closing a phase, compare phase status across `_index.md`, the phase context, and the main artifact. Update all three or record the mismatch as a blocker.
- Do not mark a phase `COMPLETED` while human review is merely recommended or unassigned. Use `READY_FOR_REVIEW` unless review is approved or explicitly deferred under deadline pressure.
- Do not put active round work in `workstreams/round_template/`; it is only a scaffold source for round workspaces.
- If the next step is determined by repository state, proceed and update the relevant artifact. Ask the human only when the choice affects strategy direction, prioritization, review approval, deadline tradeoffs, or final submission selection.

## Repo skills

When a task matches a file in `skills/`, read that skill after the workflows and before editing. Use:

- `skills/analyze_round.md` for ingestion and round fact summaries.
- `skills/add_new_round.md` for new round setup.
- `skills/run_eda.md` for EDA.
- `skills/synthesize_understanding.md` for understanding summaries.
- `skills/generate_strategy_candidates.md` for strategy candidates, lightweight prioritization, rejection, and shortlisting.
- `skills/write_strategy_spec.md` for strategy specs, review state, and implementation readiness.
- `skills/create_trader.md` for implementation.
- `skills/validate_trader.md` for validation and run summaries.
- `skills/debug_trader.md` for debugging.
- `skills/generate_trader_variant.md` for controlled variants.
- `skills/manage_phase_state.md` for phase starts, resumes after time gaps, closures, drift detection, and state repair.
- `skills/develop_strategy.md` is deprecated; use `skills/generate_strategy_candidates.md` or `skills/write_strategy_spec.md` instead.

## Start and continue behavior

When a user asks "where are we?", "what now?", or "continue round_X", open `rounds/round_X/workspace/_index.md` first, then the matching phase context. Report the current phase status, blockers, active strategies or implementations, and next priority action before doing deeper work.

When starting a phase, confirm required inputs, set the phase `IN_PROGRESS` if work begins, and create or update the phase context. When continuing a phase, prefer updating the existing phase artifact over creating a duplicate.

When an artifact is missing, say what is missing and propose the smallest useful next action. Do not skip required gates; use fast-mode compression only when the required spec, validation, or handoff information still exists in short form.

## Trader contract summary

Implement `Trader.run(state)` and return `result, conversions, traderData`.
`result` maps product symbols to lists of `Order` objects.
Use wiki-defined datamodel fields, order signs, and position signs.
Use `traderData` as string persistence between calls.
Add round-specific methods only when round docs say they apply.

## Closing a phase

Before closing a phase, confirm the required artifact exists, required template fields or checklist items are filled or explicitly deferred, `_index.md` is current, and the relevant phase context is current.

Use review outcomes: `not reviewed`, `approved`, `approved with caveats`, `changes requested`, or `deferred under deadline`.

Mark a phase:

- `READY_FOR_REVIEW` when the owner believes exit criteria are met but review is not approved or deferred.
- `COMPLETED` only when review is approved, approved with caveats, or explicitly deferred under deadline pressure.
- `BLOCKED` when a missing artifact, stale state, source conflict, platform/run access issue, or human decision blocks useful progress.

Ask for human review when closure changes strategy direction, priority, risk, or submission readiness.

## Working philosophy

There is no single correct strategy. Make small, reviewable changes, label assumptions, validate against the wiki, and hand off evidence clearly.
