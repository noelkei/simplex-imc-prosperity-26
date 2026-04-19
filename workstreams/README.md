# Workstreams

This folder holds the reusable round workspace template.

Active round work belongs under `rounds/round_X/`, not here.

Personal drafts belong under `non-canonical/<member>/`, not here.

If a teammate or agent asks "where are we?", open `rounds/round_X/workspace/_index.md` first. Use `round_template/` only to create or repair a round workspace scaffold.

## Template Usage

The repository pre-creates `rounds/round_1/` through `rounds/round_5/`. If a round workspace is missing or damaged:

1. Copy `workstreams/round_template/` to `rounds/round_X/workspace/`.
2. Update `rounds/round_X/workspace/_index.md` with the round number, deadline if known, and active round wiki link.
3. Keep all phase statuses as `NOT_STARTED` until work actually begins.

Do not fill the template with real round facts. Edit only the copied round workspace.

## Phase States

Use only:

- `NOT_STARTED`
- `IN_PROGRESS`
- `BLOCKED`
- `READY_FOR_REVIEW`
- `COMPLETED`

Move a phase to `READY_FOR_REVIEW` only when its required artifact exists and the owner believes the exit criteria are met. Move it to `COMPLETED` only after review or a recorded deadline-mode review deferral.

Move a phase to `BLOCKED` when progress requires missing data, source clarification, platform/run access, or a human decision. When unblocked, return it to `IN_PROGRESS` and record the decision in the phase context.

## `_index.md`

The round `_index.md` in `rounds/round_X/workspace/` is the control panel. It should show:

- current next priority action
- status for every phase
- product scope
- active strategy candidate queue with roles and priority tiers
- active implementation queue constrained by reviewed specs and validation capacity
- latest results
- blockers and decisions needed
- final submission status

Agents should read the active round `_index.md` before continuing a round.

If `_index.md` and a phase context disagree, treat `_index.md` as the control panel and update both files as soon as the correct state is known.

## Phase Context Files

Phase context files are short resumption notes. Update the relevant context file whenever:

- new work is added
- decisions change
- phase status changes
- implementation affects understanding
- performance changes prioritization
- debugging changes the next action

Do not use context files as long reports. Link full artifacts instead.
