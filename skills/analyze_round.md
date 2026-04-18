# Analyze Round

Use this skill to summarize a released round for downstream EDA, strategy, implementation, or validation.

## Required sources

- Wiki: `../docs/prosperity_wiki/README.md`
- Trading rules: `../docs/prosperity_wiki/trading/01_exchange_mechanics.md`, `../docs/prosperity_wiki/trading/02_orders_and_position_limits.md`
- Active round: the relevant file in `../docs/prosperity_wiki/rounds/`
- Round state: `../rounds/round_X/workspace/_index.md` and `../rounds/round_X/workspace/phase_00_ingestion_context.md` when working in an active round workspace
- Workflows: `../docs/prosperity_workflows/04_workstream_strategy.md`, `../docs/prosperity_workflows/07_workstream_round_preparation.md`

## Steps

1. Read the wiki README, shared trading rules, and active round doc.
2. Identify algorithmic products, manual products, position limits, challenge names, and source caveats only from wiki sources.
3. Separate algorithmic mechanics from manual-only mechanics.
4. Label product hints as wiki facts, not strategy conclusions.
5. Use playbook guidance only as heuristic context when strategy framing is requested.
6. Do not infer missing limits or behavior from bot artifacts, performance artifacts, `non-canonical/` drafts, examples, or memory.
7. Record unknowns that may affect EDA, strategy, or implementation separately from facts, with a next action: clarify, targeted EDA, or defer with risk.
8. Record a compact Round Mechanics Delta for downstream phases: active products/limits, new or changed Trader/API mechanics, data/schema changes, manual-only mechanics, and prior-round assumptions at risk.
9. If raw data, logs, or run artifacts arrive after ingestion starts or closes, update ingestion data availability, clear or replace stale "no data" blockers, update `_index.md`, update the phase context, and keep data observations labeled as evidence rather than official facts.
10. Update or create the round `_index.md` and ingestion phase context when working in an active round workspace, including blockers or next priority action for material unknowns.
11. Handoff a concise summary with sources, caveats, downstream-impacting unknowns, phase status, and concrete next actions.
