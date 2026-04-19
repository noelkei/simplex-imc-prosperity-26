# Round 2 Strategy Spec - Amin Regime Depth Tuned 08

## Review Status

- Status: `DEFERRED_UNDER_DEADLINE`
- Owner: Amin / OpenClaw
- Reviewer: Unassigned
- Reviewed on: fast-turn implementation

## Candidate

- Candidate ID: `r2_amin_regime_depth_tuned_08`
- Shortlist priority: `high`
- Evidence strength: `medium`
- Product scope: `ASH_COATED_OSMIUM`, `INTARIAN_PEPPER_ROOT`

## Why this branch exists

This is a direct fine-tuned successor to `_04`, based on a fresh re-read of the Round 2 data and external microprice literature.

The key research conclusion was not to add more complexity, but to tune the validated regime-aware backbone more sharply:

- ACO tight spreads are materially stronger than ACO mid spreads
- ACO mid-spread periods should be gated even harder
- IPR remains strong enough to justify slightly more assertive reposting and earlier trimming

## Tuning changes vs `_04`

- ACO:
  - tighter regime gets more weight on microprice, depth shift, and imbalance
  - wide regime stays active but less aggressive than tight regime
  - middle regime is penalized more heavily via larger take threshold and much smaller passive sizes
- IPR:
  - reposting reacts a bit more strongly to positive pressure
  - low-conviction repost size is capped to avoid overcommitting in weak states
  - trimming starts slightly earlier and with slightly larger size

## Validation note

This branch is theoretically better aligned with the latest EDA, but the local lightweight replay still does not beat `_04`.

Therefore `_08` should be viewed as a research-backed alternative rather than a locally validated replacement.

## Implementation Handoff

- Target bot path: `../../bots/amin/canonical/candidate_r2_amin_regime_depth_tuned_08.py`
- Filename rule followed: incremented suffix to `_08`
- Core idea: harder ACO regime gating plus modest IPR execution tuning
