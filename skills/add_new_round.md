# Add New Round

Use this skill when documenting a newly released Prosperity round in the repo wiki.

## Required sources

- Wiki structure: `../docs/prosperity_wiki/README.md`
- Future-round guidance: `../docs/prosperity_wiki/rounds_future/README.md`
- Shared facts: `../docs/prosperity_wiki/api/`, `../docs/prosperity_wiki/trading/`, `../docs/prosperity_wiki/platform/`
- Workflow: `../docs/prosperity_workflows/07_workstream_round_preparation.md`
- Time-aware pipeline: `../docs/prosperity_workflows/10_time_aware_team_pipeline.md`
- Safe changes: `../docs/prosperity_workflows/09_safe_change_rules.md`
- Round workspace: `../rounds/round_X/`
- Workstream template: `../workstreams/round_template/`

## Steps

1. Confirm the new round material is in the accepted factual source set for this repo.
2. Create the curated round wiki page under `../docs/prosperity_wiki/rounds/` from factual sources only.
3. Use the pre-created `../rounds/round_X/` folder for the released round. If its `workspace/` folder is missing or damaged, copy `../workstreams/round_template/` to `../rounds/round_X/workspace/`.
4. Initialize `../rounds/round_X/workspace/_index.md` with the round name, deadline if known, active round wiki link, and all phase statuses set to `NOT_STARTED`.
5. Initialize all phase context files with `NOT_STARTED`, unassigned owner/reviewer, links to the new round index, and the first next action.
6. Confirm member-first bot and performance folders exist for `isaac`, `bruno`, `amin`, `daniela`, and `noel`: `../rounds/round_X/bots/<member>/canonical/`, `../rounds/round_X/bots/<member>/historical/`, `../rounds/round_X/performances/<member>/canonical/`, and `../rounds/round_X/performances/<member>/historical/`.
7. Extract products, limits, challenge names, algorithmic facts, manual facts, and source caveats into the new round ingestion artifact.
8. Record a compact Round Mechanics Delta for downstream phases: active products/limits, new or changed Trader/API mechanics, data/schema changes, manual-only mechanics, and prior-round assumptions at risk.
9. Record unknowns that may affect EDA, strategy, or implementation separately from facts, with a next action: clarify, targeted EDA, or defer with risk.
10. Keep manual-only mechanics separate from bot implementation requirements.
11. If the source appears to change the API contract, quote or paraphrase the exact source and mark the caveat before implementation depends on it.
12. Update `_index.md` blockers or next priority action when a downstream-impacting unknown remains.
13. Do not use round-local bot artifacts, performance artifacts, `non-canonical/` drafts, sample outputs, or memory as authority.
14. Handoff with reviewed sources, new or updated round doc path, initialized round workspace path, Round Mechanics Delta, unresolved facts, downstream-impacting unknowns, and downstream actions.
