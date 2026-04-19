# Round 2 Performances

Saved platform artifacts:

- `noel/historical/baseline_state_logger.json`
- `noel/historical/candidate_r2_cand_*.json`
- `noel/canonical/run_20260419_battery01_*.md`

The baseline logger is historical EDA evidence for quote-subset comparability,
not alpha evidence or a candidate validation result.

Battery 01 candidate JSONs are raw platform evidence. The canonical decision
evidence is the generated run summaries under `noel/canonical/` and the
aggregate report at `../workspace/06_testing/round2_battery_01_analysis.md`.

Performance results are non-authoritative evidence. Preserve durable run evidence as `.md` and/or `.json` summaries using `docs/templates/run_summary_template.md`.

## Folders

- `<member>/canonical/`: current decision-supporting run summaries owned by that team member.
- `<member>/historical/`: superseded, stale, non-comparable, or no-longer-decision-relevant run summaries owned by that team member.

Supported members: `isaac`, `bruno`, `amin`, `daniela`, `noel`.

## Naming

- Canonical run summary: `<member>/canonical/run_YYYYMMDD_HHMM_<candidate_id>.md`
- Debug-focused run summary: `<member>/canonical/run_YYYYMMDD_HHMM_<candidate_id>_<issue_id>.md`
- Historical archive: `<member>/historical/YYYYMMDD_<candidate_id>_<reason>.md`, or keep the original run name if it is already clear.
- Optional machine-readable summary: use the same stem with `.json`

## Required Contents

Every durable run summary must include:

- bot path
- linked strategy spec
- raw artifact path, if available
- run id or platform id
- metrics
- runtime issues, errors, rejections, and position-limit concerns
- interpretation limits
- decision and next action

## Raw Logs

Raw logs may be untracked or ignored. Preserve durable evidence in tracked `.md` and/or `.json` summaries.

## Promotion And Archive Rules

- Put a run summary in `<member>/canonical/` when it is currently used to compare, promote, debug, or choose a candidate.
- Move a run summary to `<member>/historical/` when it is superseded, non-comparable, stale, or no longer decision-relevant.
- Link current evidence from `../workspace/_index.md` to `<member>/canonical/` unless historical context is explicitly needed.
- Canonical performance evidence is still non-authoritative; it does not define official rules or prove a strategy is correct.

## Update Rules

After each meaningful run, update `../workspace/_index.md` and `../workspace/phase_06_testing_context.md` with the latest result, best current candidate if changed, and next action.
