# Round 1 Workspace

Official round facts: [`../../docs/prosperity_wiki/rounds/round_1.md`](../../docs/prosperity_wiki/rounds/round_1.md)

Do NOT duplicate or modify official round facts here. This folder contains derived artifacts only.

This round workspace is pre-created; no round work has begun yet.

## How To Start

1. Open [`workspace/_index.md`](workspace/_index.md).
2. Confirm all phases are `NOT_STARTED`.
3. Start phase 00 ingestion in [`workspace/00_ingestion.md`](workspace/00_ingestion.md).
4. Update the relevant phase context whenever status, decisions, blockers, or next actions change.

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
