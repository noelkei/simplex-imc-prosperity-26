# Round 1 Workspace

Official round facts: [`../../docs/prosperity_wiki/rounds/round_1.md`](../../docs/prosperity_wiki/rounds/round_1.md)

Do NOT duplicate or modify official round facts here. This folder contains derived artifacts only.

This round workspace is active. Use [`workspace/_index.md`](workspace/_index.md) as the source of current state, blockers, product scope, active strategies, and next action.

## How To Continue

1. Open [`workspace/_index.md`](workspace/_index.md).
2. Use `Current Next Priority Action` to decide what to do next.
3. Use the phase context files in `workspace/` as short resumption notes.
4. Keep bots, data, and performance outputs inside this round folder.

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
