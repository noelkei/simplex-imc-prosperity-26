# Round 4 Workspace

Official round facts expected path: `../../docs/prosperity_wiki/rounds/round_4.md`

The official Round 4 facts file is now available at
[`../../docs/prosperity_wiki/rounds/round_4.md`](../../docs/prosperity_wiki/rounds/round_4.md).

Do NOT duplicate or modify official round facts here. This folder contains derived artifacts only.

Round 4 ingestion has started. Use the workspace artifacts below for derived
facts, caveats, and phase state.

## How To Start

1. Open [`../../docs/prosperity_wiki/rounds/round_4.md`](../../docs/prosperity_wiki/rounds/round_4.md).
2. Open [`workspace/_index.md`](workspace/_index.md).
3. Continue or review phase 00 ingestion in [`workspace/00_ingestion.md`](workspace/00_ingestion.md).
4. Use the uploaded raw CSVs in [`data/raw/`](data/raw/) to begin targeted EDA on counterparties and Round 3 carry-forward revalidation.
5. Update the relevant phase context whenever status, decisions, blockers, or next actions change.

## How To Continue

- Read [`workspace/_index.md`](workspace/_index.md) first.
- Use `Current Next Priority Action` to decide what to do next.
- Use the phase context files in `workspace/` as short resumption notes.
- Keep bots, data, and performance outputs inside this round folder.

## How To Close Work

- Update [`workspace/_index.md`](workspace/_index.md).
- Update the relevant `workspace/phase_YY_*_context.md` file.
- Link the artifact that was produced or changed.
- Set the phase to `READY_FOR_REVIEW`, `COMPLETED`, or `BLOCKED`.
- Leave one concrete next action for the next human or agent.

## Local Artifacts

- `workspace/`: phase tracking and reviewed workflow artifacts.
- `bots/<member>/canonical/`: current selected or candidate bot files owned by a team member.
- `bots/<member>/historical/`: previous attempts owned by a team member.
- `performances/<member>/canonical/`: current decision-supporting run summaries owned by a team member.
- `performances/<member>/historical/`: superseded or non-current run summaries owned by a team member.
- `data/`: round-local `raw/`, `processed/`, and `external/` data artifacts.

Supported members: `isaac`, `bruno`, `amin`, `daniela`, `noel`.

Personal scratch work belongs in [`../../non-canonical/`](../../non-canonical/), not in this formal round workspace.
