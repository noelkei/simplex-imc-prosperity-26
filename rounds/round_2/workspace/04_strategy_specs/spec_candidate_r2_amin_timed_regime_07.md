# Round 2 Strategy Spec - Amin Timed Regime 07

## Review Status

- Status: `DEFERRED_UNDER_DEADLINE`
- Owner: Amin / OpenClaw
- Reviewer: Unassigned
- Reviewed on: fast-turn implementation

## Candidate

- Candidate ID: `r2_amin_timed_regime_07`
- Shortlist priority: `medium-high`
- Evidence strength: `experimental`
- Product scope: `ASH_COATED_OSMIUM`, `INTARIAN_PEPPER_ROOT`

## Why this is different

This branch intentionally shifts away from the latest "same logic everywhere" style and instead changes behavior across the session:

- early phase: more willing to accumulate IPR and quote ACO actively
- middle phase: maintain balanced participation
- late phase: reduce fresh risk and monetize inventory more defensively

This is a schedule-driven execution change rather than another pure signal retune.

## Design

- Backbone inherited from `r2_amin_regime_depth_04`
- IPR:
  - earlier timestamps allow larger repost size and higher carry participation
  - later timestamps reduce fresh reposting and force more conservative inventory growth
- ACO:
  - early phase lowers taking threshold slightly
  - late phase raises taking threshold and reduces passive size

## Motivation

Round 2 books appear dynamic but not uniformly so. A time-aware execution schedule may outperform a stationary policy if the best risk-taking window is earlier while late-stage inventory is more expensive to carry.

## Validation Note

Local lightweight replay does not clearly beat `_04`, but this branch is intentionally preserved as a structurally different execution model for platform testing.

## Implementation Handoff

- Target bot path: `../../bots/amin/canonical/candidate_r2_amin_timed_regime_07.py`
- Filename rule followed: incremented suffix to `_07`
- Core idea: regime-aware logic plus timestamp-based risk schedule
