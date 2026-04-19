# Round 2 Bots

This folder contains round-local bot artifacts only. Bots are non-authoritative and must not be used as the source of truth for Prosperity rules.

## Folders

- `<member>/canonical/`: active candidate bots, baselines, and the selected submission file owned by that team member.
- `<member>/historical/`: superseded attempts, archived candidates, and old experiments owned by that team member.

Supported members: `isaac`, `bruno`, `amin`, `daniela`, `noel`.

## Naming

- Candidate bot: `<member>/canonical/candidate_<candidate_id>_<short_name>.py`
- Baseline bot: `<member>/canonical/baseline_<short_name>.py`
- Optional active submission file: `<member>/canonical/submission_active.py`
- Historical archive: `<member>/historical/YYYYMMDD_<candidate_id>_<reason>.py`

## Promotion Rules

- A candidate must link to a reviewed strategy spec before implementation work starts.
- A promoted candidate must have a validation or performance summary in `../performances/<member>/canonical/`.
- Update `../workspace/_index.md` and `../workspace/phase_05_implementation_context.md` when active implementations change.
- Historical bots are implementation artifacts only; do not infer official rules or strategy correctness from them.

## Baselines

Baselines are reference behavior for comparison only. They are non-authoritative and do not define what the final strategy should be.

## Current Round 2 Notes

- Noel Battery 01 bots and results are preserved for post-run evidence.
- Bruno Generation 2 canonical bots are under `bruno/canonical/` and are the
  current 13-bot upload queue for the next Prosperity test batch.
- `bruno/canonical/candidate_r2_g2_13_maf_bid_scenario.py` intentionally
  returns a nonzero `bid()` scenario. Testing ignores bid acceptance, but do not
  use it as a final submission without a final MAF decision.
