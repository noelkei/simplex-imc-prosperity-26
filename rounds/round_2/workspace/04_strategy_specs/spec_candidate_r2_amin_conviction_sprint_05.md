# Round 2 Strategy Spec - Amin Conviction Sprint 05

## Review Status

- Status: `DEFERRED_UNDER_DEADLINE`
- Owner: Amin / OpenClaw
- Reviewer: Unassigned
- Reviewed on: deadline-deferred implementation

## Candidate

- Candidate ID: `r2_amin_conviction_sprint_05`
- Shortlist priority: `high`
- Evidence strength: `experimental`
- Product scope: `ASH_COATED_OSMIUM`, `INTARIAN_PEPPER_ROOT`
- Linked candidate file: `../03_strategy_candidates.md`

## Intent

This is the explicitly aggressive Round 2 moonshot branch.

Instead of staying mostly in market-making mode, it allows ACO to shift into a conviction-driven sprint mode when directional pressure is unusually strong and persistent. The goal is not incremental cleanliness, but to capture larger bursts that more conservative candidates may under-monetize.

## Core Logic

- Keep the Kalman + regime-aware depth backbone from `_04`.
- Compute a directional conviction score from:
  - predictive shift
  - microprice displacement
  - imbalance
  - selective depth-price shift
  - spread regime
- If conviction is low: behave close to the safer quoting baseline.
- If conviction is medium: skew one-sided more aggressively.
- If conviction is very high and persistent: enter sprint mode.
- Sprint mode:
  - takes more size in the conviction direction
  - posts much more heavily on the favored side
  - suppresses opposite-side quoting except for partial unload logic
  - decays quickly if signal weakens

## Why This Could Work

- The current score is close enough to 9k that a materially different risk posture may be the only way to jump the barrier rather than grind for tiny gains.
- ACO appears to contain short directional bursts that conservative MM logic may underexploit.
- Round 2 partial visibility randomness may occasionally reward stronger directional commitment when visible pressure is unusually clear.

## Why This Could Fail

- Overtrading noise.
- Getting loaded before reversal.
- Local stub replay does not show a clean improvement over `_04`.

## Recommendation

Treat this candidate as a deliberate upside shot, not the safest default. Upload it because it may interact favorably with the platform randomness even though the lightweight local harness does not prefer it.

## Implementation Handoff

- Target bot path: `../../bots/amin/historical/candidate_r2_amin_conviction_sprint_05.py`
- Filename rule followed: incremented suffix to `_05`
- Core parameters:
  - `ACO_MEDIUM_CONVICTION = 1.75`
  - `ACO_HIGH_CONVICTION = 2.85`
  - `ACO_SPRINT_ENTRY = 3.6`
  - `ACO_SPRINT_DECAY = 1.55`
  - `ACO_SPRINT_MAX_HOLD = 10`
  - `MARKET_ACCESS_BID = 9`
