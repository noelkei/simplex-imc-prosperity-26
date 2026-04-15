# Manage Phase State

Use this skill to keep phase state synchronized without duplicating phase workflow logic.

## Use this skill when

- Starting a phase.
- Resuming a phase after a time gap.
- Closing a phase.
- Detecting inconsistency between `_index.md`, the phase context, and the main phase artifact.
- Repairing drift in status, blockers, review outcome, linked artifacts, or next action.

## Required sources

- Round state: `../rounds/round_X/workspace/_index.md`
- Relevant phase context: `../rounds/round_X/workspace/phase_YY_*_context.md`
- Main phase artifact for the phase being updated
- Workflow: `../docs/prosperity_workflows/10_time_aware_team_pipeline.md`
- Task-specific workflow when the state change depends on phase exit criteria

## Responsibilities

- Compare status, owner/reviewer, review outcome, blockers, linked artifacts, deadline risk, and next action across `_index.md`, the phase context, and the main artifact.
- Update only the minimum state fields needed: status, owner/reviewer, review outcome, blockers, linked artifact, next priority action, deadline risk, and recently changed artifacts.
- Before closure, confirm the required artifact exists and review rules are satisfied.
- If status cannot be safely reconciled, preserve or set `BLOCKED` and record the mismatch as the blocker.

## Boundaries

- Do not perform EDA, strategy, implementation, validation, or debugging work.
- Do not duplicate workflow exit criteria; link or refer to the relevant workflow.
- Do not decide strategy direction, final submission, review approval, or deadline tradeoffs.
- Do not silently update only one phase surface when the state change affects multiple artifacts.

## Handoff

Leave the phase resumable with current status, review outcome if applicable, blocker, artifact link, and next action.
