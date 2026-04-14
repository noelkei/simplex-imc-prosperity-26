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
