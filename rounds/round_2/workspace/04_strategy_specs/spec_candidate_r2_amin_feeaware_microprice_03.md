# Round 2 Strategy Spec - Amin Fee-Aware Microprice 03

## Review Status

- Status: `DEFERRED_UNDER_DEADLINE`
- Owner: Amin / OpenClaw
- Reviewer: Unassigned
- Reviewed on: deadline-deferred implementation

## Candidate

- Candidate ID: `r2_amin_feeaware_microprice_03`
- Shortlist priority: `high`
- Evidence strength: `medium`
- Product scope: `ASH_COATED_OSMIUM`, `INTARIAN_PEPPER_ROOT`
- Linked candidate file: `../03_strategy_candidates.md`

## Review Decision

- `_index.md` spec status: `deadline deferred`
- Approved for implementation: `yes, under hackathon pressure`
- Reviewer decision notes: Built as a next numbered branch after `feeaware_kalman_02`, keeping the same Round 2 fee-aware structure but rotating toward stronger microprice and order-book pressure exploitation.
- Required changes before coding: human review later if this becomes the chosen final submission.

## Sources

- EDA evidence: `../01_eda/eda_report.md`
- Additional repo evidence: `../01_eda/compare_candidates.py`, `../../performances/amin/canonical/candidate_comparison_2026-04-19.json`
- Fast local research used for this branch: top-of-book imbalance and microprice follow-through checks on Round 2 raw price data.

## Selection Trace

- Prior branch already used latent fair value plus mild imbalance skew.
- New evidence shows top-of-book imbalance has stronger next-tick directional effect than the current implementation is pricing in, especially for ACO.
- Therefore this branch keeps the Kalman fair value, but shifts the observation and quoting logic toward microprice and pressure-following execution.

## Signal / Fair Value Logic

- ACO:
  - keep Kalman fair value backbone.
  - replace plain midpoint observation with microprice-adjusted observation.
  - shift quotes using both imbalance and microprice displacement.
  - reduce taking threshold when pressure agrees with the quote direction.
- IPR:
  - keep strong long-bias carry structure.
  - repost more aggressively when book pressure is positive instead of only using a binary repost rule.

## Expected Edge

- ACO should respond faster to one-sided books without fully abandoning the stabilizing Kalman fair value.
- IPR should improve queue priority and continuation capture during strong buy-pressure stretches.
- Candidate is intentionally a structural sibling of `_02`, not a tiny retune, to give the platform another distinct path toward breaking the next milestone.

## Implementation Handoff

- Target bot path: `../../bots/amin/historical/candidate_r2_amin_feeaware_microprice_03.py`
- Filename rule followed: incremented suffix to `_03`
- Core parameters:
  - `ACO_MICROPRICE_WEIGHT = 0.75`
  - `ACO_MICROPRICE_CLIP = 3.0`
  - `ACO_PRESSURE_TAKE_EDGE = 0.5`
  - `IPR_PRESSURE_REPOST_COEF = 5.0`
  - `MARKET_ACCESS_BID = 9`
