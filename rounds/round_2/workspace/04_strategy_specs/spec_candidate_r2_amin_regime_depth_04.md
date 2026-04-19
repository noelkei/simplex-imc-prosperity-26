# Round 2 Strategy Spec - Amin Regime Depth 04

## Review Status

- Status: `DEFERRED_UNDER_DEADLINE`
- Owner: Amin / OpenClaw
- Reviewer: Unassigned
- Reviewed on: deadline-deferred implementation

## Candidate

- Candidate ID: `r2_amin_regime_depth_04`
- Shortlist priority: `high`
- Evidence strength: `medium`
- Product scope: `ASH_COATED_OSMIUM`, `INTARIAN_PEPPER_ROOT`
- Linked candidate file: `../03_strategy_candidates.md`

## Round 2 Focus

This branch is explicitly optimized around Round 2 constraints:

- testing only exposes a randomized 80% quote subset
- accepted bids get 25% more quotes in the final blind-auction simulation
- therefore the bot should remain robust on partial visibility while gaining upside from richer depth if market access is won

## Selection Trace

- `_03` improved platform score to 8975 by leaning harder into microprice and top-level pressure.
- Follow-up research on the raw Round 2 data showed that deeper multi-level imbalance is not a good signal here, but depth-weighted price shift is useful.
- The depth-price signal is strongest in spread regimes that are either tight or wide, and weak in the middle spread regime.
- This candidate therefore uses regime-aware depth information selectively instead of applying it uniformly.

## Core Logic

- ACO:
  - keep Kalman fair value backbone.
  - use microprice plus selective depth-price shift in the fair-value observation.
  - trust depth-price shift more when spread is tight or wide.
  - avoid overreacting in the middle spread regime.
- IPR:
  - keep the carry-style long bias.
  - make repost aggression depend on both top-level imbalance and a smaller depth-price contribution.

## Why This Fits Round 2

- With default testing at 80% quotes, the bot still works because it only relies on visible depth and clips all adjustments.
- If the Market Access Fee bid is accepted, the extra 25% quotes should improve depth-price estimation and opportunistic fills.
- This makes the candidate naturally fee-aware without depending on extra access to function.

## Validation Notes

- Local fast replay stub: `_04` recovered to competitive performance after de-risking the first version.
- In the stub it edges `_03` on two sample days and is near-tied on the third.
- Platform validation is still required because the stub is only directional.

## Implementation Handoff

- Target bot path: `../../bots/amin/canonical/candidate_r2_amin_regime_depth_04.py`
- Filename rule followed: incremented suffix to `_04`
- Core parameters:
  - `ACO_DEPTH_SHIFT_CLIP = 2.0`
  - `ACO_MICROPRICE_WEIGHT = 0.4`
  - selective depth weighting by spread regime
  - `IPR_PRESSURE_REPOST_COEF = 3.0`
  - `MARKET_ACCESS_BID = 9`
