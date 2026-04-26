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

- Compare status, owner/reviewer, review outcome, blockers, linked artifacts, deadline risk, next action, and any phase-specific wait-state fields across `_index.md`, the phase context, and the main artifact.
- Update only the minimum state fields needed: status, owner/reviewer, review outcome, blockers, linked artifact, next priority action, deadline risk, and recently changed artifacts.
- Before closure, confirm the required artifact exists and review rules are satisfied. Exception: for Phase `02b External Paper Research`, allow operational `COMPLETED` once the prompt exists and at least one processed paper exists, or when the user explicitly skips it with reason.
- For Phase `02b External Paper Research`, also keep the paper-pipeline state synchronized enough for resumption: wait state, current raw-set coverage, and whether the phase is only operationally complete or fully processed for the local raw set.
- When a phase closure is part of round closeout, also check whether `_index.md`, the phase context, and the closeout artifact agree on whether the round is still active, paused, or retrospective-only.
- If status cannot be safely reconciled, preserve or set `BLOCKED` and record the mismatch as the blocker.

## Boundaries

- Do not perform EDA, strategy, implementation, validation, or debugging work.
- Do not duplicate workflow exit criteria; link or refer to the relevant workflow.
- Do not decide strategy direction, final submission, review approval, or deadline tradeoffs.
- Do not silently update only one phase surface when the state change affects multiple artifacts.
- Do not reinterpret paper contents or batch priority while doing state repair; only synchronize the paper-pipeline state that the phase already records.

## Handoff

Leave the phase resumable with current status, review outcome if applicable, blocker, artifact link, and next action.
