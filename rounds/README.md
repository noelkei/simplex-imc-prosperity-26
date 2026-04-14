# Rounds

This folder contains round-local execution workspaces and artifacts.

Global factual sources stay in `docs/`:

- `docs/prosperity_wiki/`: operational factual source
- `docs/prosperity_wiki_raw/`: underlying factual base
- `docs/prosperity_playbook/`: heuristics
- `docs/prosperity_workflows/`: process guidance

Do not duplicate official round facts into this folder. Each `round_X/` folder contains derived work only: workspace notes, local bot candidates, data artifacts, and performance summaries.

Current decision-supporting bot and performance evidence belongs in member-owned folders such as `round_X/bots/<member>/canonical/` and `round_X/performances/<member>/canonical/`. Superseded or non-current artifacts belong in the corresponding `<member>/historical/` folder.

Supported members are `isaac`, `bruno`, `amin`, `daniela`, and `noel`.

## How To Use A Round Folder

To start or continue a round, open:

```text
rounds/round_X/workspace/_index.md
```

Use `_index.md` as the control panel for phase status, blockers, active strategies, active implementations, latest results, and final submission state. Use `workspace/phase_YY_*_context.md` files as short resumption notes.

Folder roles:

- `workspace/`: formal phase artifacts, phase contexts, and decision state.
- `data/`: round-local raw, processed, and external data artifacts.
- `bots/`: member-owned implementation candidates and archived attempts.
- `performances/`: member-owned validation and run summaries.

If official facts are not available yet for a future round, keep the round `NOT_STARTED` and do not create derived facts in `rounds/`.

Personal drafts belong in `../non-canonical/<member>/`, not in `rounds/`. Move or summarize draft work into the relevant round artifact before using it as part of the formal workflow.

Before closing work in a round, update `_index.md`, update the relevant phase context, link the produced artifact, and leave a concrete next action.
