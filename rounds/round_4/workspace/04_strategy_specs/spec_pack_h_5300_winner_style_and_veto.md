# Spec Pack H: 5300 Winner-Style And Veto

## Review Status

- Status: `COMPLETED`
- Owner: Codex
- Reviewer: Human
- Reviewed on: 2026-04-27

## Candidate

- Candidate ID: `pack_h_5300_winner_style_and_veto`
- Candidate priority tier: `spec-first`
- Evidence strength: `medium-high`
- Product scope: `VELVETFRUIT_EXTRACT`, `VEV_5300`, contextual `VEV_5200`
- Linked candidate file: `../03_strategy_candidates.md`

## Pack Members

| Candidate | Product Scope | Role In Pack | Target Bot Path |
| --- | --- | --- | --- |
| `r4_w2_05_5300_clean_value_retest` | `VEX + VEV_5300` | clean current-round `5300` baseline | `rounds/round_4/bots/noel/canonical/r4_w2_05_5300_clean_value_retest.py` |
| `r4_w2_06_5300_horizon_hold_v2` | `VEX + VEV_5300` | horizon-aware rescue | `rounds/round_4/bots/noel/canonical/r4_w2_06_5300_horizon_hold_v2.py` |
| `r4_w2_07_5300_queue_takeover_probe` | `VEX + VEV_5300` | winner-style adapted execution probe | `rounds/round_4/bots/noel/canonical/r4_w2_07_5300_queue_takeover_probe.py` |
| `r4_w2_08_5300_with_5200_veto` | `VEX + VEV_5300` plus contextual `VEV_5200` | strongest active-family plus veto combination | `rounds/round_4/bots/noel/canonical/r4_w2_08_5300_with_5200_veto.py` |

## Review Decision

- `_index.md` spec status: `approved`
- Approved for implementation: `yes`
- Reviewer decision notes: User explicitly requested implementing all `15`
  Wave 2 bots and entering `Phase 05`. Treat that instruction as operational
  approval for exploratory implementation with validation caveats, including
  the winner-style adapted probes.
- Required changes before coding: none

## Sources

- Wiki facts: Round 4 product scope, limits, and trade-field availability.
- EDA evidence:
  - `5300` remains special and unresolved
  - `5200` is a danger-state candidate
  - surface awareness is useful as framing, not as heavy machinery
- Understanding summary:
  - `5300` should be isolated from the broad active family
  - `VEX` remains the anchor
- Post-run research memory:
  - `r4_w1_i03_5200_signal_only`
  - Pack `C` remains strategically open
- Uploaded winner references:
  - `../research/big_volcano_man_fixed.py`
  - `../research/big_volcano_man_IV_window.py`
  - `../research/algo run for round 4.py`
- Processed paper references:
  - `../research/papers_processed/carry_forward/choi_2022_bachelier_guide_processed.md`
  - `../research/papers_processed/carry_forward/stoikov_saglam_2009_option_mm_inventory_processed.md`
  - `../research/papers_processed/carry_forward/garcia_ares_2023_expiration_days_processed.md`
  - `../research/papers_processed/doshi_2025_risky_intraday_order_flow_processed.md`

## Carry-Forward Context

- Validated carry-forward principles used:
  - `5300` deserves separate treatment
  - `5200` should be context first
  - `VEX` should remain the anchor
- Untested hypotheses intentionally being tested:
  - `5300` may be alive but execution-limited
  - `5300` may be an edge-then-reversal branch rather than pure no-edge
  - the uploaded winner trade style may improve `5300` learnability
- Anti-patterns explicitly avoided:
  - broad active voucher basket
  - direct `5200` inventory
  - full old-round calibration port
  - heavy IV-surface runtime stack

## Selection Trace

- Based on candidates: `r4_w2_05`, `r4_w2_06`, `r4_w2_07`, `r4_w2_08`
- Signals used:
  - `5300` specialness from understanding
  - `5200` signal-only veto from Wave 1
  - winner-style queue takeover and fair-value quoting architecture
- Alternatives considered:
  - pure carry-forward `5300` retest without adaptation
  - hard whole-bot contextual veto
  - full old IV-window / hedge port
- Why selected: this pack is the best place to test whether the old winner
  architecture has real current-round value once adapted honestly.
- Known caveats:
  - canonical Pack `C` summaries are still missing
  - the fair-value proxy may help execution quality without proving `5300`
    directional edge
- Branch posture: `clean isolation test`

## Evidence Traceability

- Linked EDA Signals:
  - `option_book_role_split`
  - `mark22_seller_danger_state`
  - `surface_awareness_not_flat_vol`
- Feature Evidence:
  - `5300` remains the only serious active direct leg
  - winner bots show that strike-specific fair-value quoting plus queue
    takeover is a credible execution style
- Metric Availability:
  - current `VEX` and `5300` books plus recent `VEV_5200` trades are online
  - rolling IV and delta are online-computable using current and recent books
- Baseline vs richer model verdict:
  - a small rolling-IV fair-value layer is justified
  - full surface or hedge machinery is not
- Multivariate Evidence:
  - `5200` context must remain a separate veto axis rather than getting folded
    into the fair-value engine
- Process / Distribution Assumptions:
  - `5300` may need better execution style, not necessarily a new signal
  - late entries and toxic neighbor states are the most plausible failure modes
- Redundancy Decisions:
  - fair-value baseline, horizon hold, winner-style queue takeover, and `5200`
    veto must remain distinct axes
- Regime Assumptions:
  - `Mark 22` seller-state warnings appear early enough to block bad late
    `5300` entries
- Understanding Insight:
  - `5300` is special but unresolved, so it deserves an honest isolated test
- Research tool evidence used, if any:
  - `choi_2022` for simple pricing backbone
  - `stoikov_saglam_2009` for inventory-aware quoting posture
  - `garcia_ares_2023` for horizon caution
  - uploaded winner code for trade-style adaptation
- Evidence gaps or strategy assumptions:
  - IV window size, cross threshold, and hold timer are strategy assumptions

## Round-Specific Mechanics Contract

| Mechanic / Trader Function / Field | Source | Decision | Bot Behavior | Validation Check |
| --- | --- | --- | --- | --- |
| `Trader.run()` | trader contract | implement | trade `VEX` and `VEV_5300`; `VEV_5200` may be context-only in `r4_w2_08` | smoke test and tuple shape |
| `Trade.buyer` / `Trade.seller` | round 4 doc | implement selectively | `r4_w2_08` may read `Mark 22` seller-state as veto | inspect skipped late `5300` entries |
| `VEV_5200` | round 4 doc | implement as context only | no direct `VEV_5200` inventory in this pack | product-order audit |
| rolling IV / delta calculation | current round books | implement | use online-computable strike-level rolling IV mean and delta estimate | log valid-window count and fair-value output |
| explicit delta hedge using `VEX` | uploaded winner code | exclude | keep attribution clean; use delta as sizing/diagnostic only | confirm no hedge-only orders appear |
| Manual challenge products | round 4 doc | exclude | no manual logic | code contains no manual references |

## Linked-Product Framing Contract

- Product role: `active risk leg`
- Signal class: `valuation | regime | mixed`
- Underlying role: `anchor`
- Trading posture: `conditional`
- Natural hold horizon: `short / medium hold`
- What makes this a trading leg instead of only a signal: `5300` has enough
  current-round structural interest to merit direct inventory if execution is
  controlled.
- Rule that should prevent edge from turning into giveback: late no-new-entry
  or `5200` veto, depending on branch.

## Feature Contract

| Feature | Source Fields | Online Availability | Lifecycle Label | Role | Parameters | Multivariate Relationship | Process Assumption | Redundancy Decision | Missing-Signal Behavior | State / `traderData` Required | Validation / Invalidation Check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| simple `5300` fair-value core | `VEX` mid, `5300` best bid/ask, timestamp | usable online | implementation candidate | direct signal | compute `5300` implied vol from current mid when both sides exist; keep rolling IV window `12`, min valid obs `6`, quote around BS fair value from rolling IV mean; edge threshold `2`, passive band `1`, max clip `12`, spread cap `10` | different from context features; this is the pricing baseline | current `5300` mispricing can be estimated well enough with a small rolling IV proxy | keep as shared core across all four bots | if IV window invalid, fall back to static fair-value approximation from recent mids or stay idle if both are missing | rolling IV window, last valid fair value, optional delta estimate | direct `5300` inventory appears and can be attributed cleanly |
| winner-style queue takeover | `5300` best bid/ask, computed fair bid/fair ask, top depth | usable online | implementation candidate | execution filter | if fair bid exceeds best ask by `>= 1`, lift up to capacity then rest one tick above best bid; symmetric on sell side; do not cross if spread already invalid | separate from raw fair value; this is execution style | the winner architecture helps by taking obvious mispricing then joining the queue | keep only in `r4_w2_07` | missing valid fair value disables this feature only | last sent quote side, last fair band | better markout and fill pattern than plain `r4_w2_05` |
| `5200` signal-only veto | recent `VEV_5200` market trades, `Trade.seller`, timestamp | usable online | implementation candidate | risk control | block new `5300` entries for `2` steps after recent `VEV_5200` seller-warning event; exits still allowed | must stay separate from fair-value core | the best use of `5200` is timing veto on a stronger parent | keep only in `r4_w2_08` | missing `VEV_5200` context removes only the veto | veto cooldown timer | fewer toxic late entries than `r4_w2_05` |
| `5300` horizon hold | timestamp, open `5300` inventory, local unrealized edge peak | usable online | implementation candidate | risk control | no new `5300` entries after final `22%` of session; hold timer `6` decision steps; giveback cutoff `45%` of local unrealized peak | separate from `5200` veto and queue takeover | `5300` may be good but not as a late-session scalp | keep only in `r4_w2_06` | if state missing, disable hold feature and use base core | hold timer, entry side, local peak | later hold preserves path better than plain baseline |
| intrinsic-value floor | `VEX` mid, strike `5300` | usable online | implementation candidate | risk control | never quote below intrinsic floor; never buy above fair ask band | low-complexity adaptation from winner architecture | prevents obviously bad quote placement | merged into all `5300` fair-value branches | missing `VEX` disables branch | none | no obviously dominated quote levels |
| option delta diagnostic | rolling IV estimate, `VEX` mid, strike `5300`, timestamp | usable online | log-only diagnostic | diagnostic | compute option delta with the same rolling IV mean; use only for logging or optional size sanity cap, not hedge | diagnostic only | delta magnitude may explain when execution becomes inventory-heavy | downgraded from direct hedge trigger | if invalid, ignore diagnostic | last valid delta | helps distinguish execution-limited from inventory-limited |

## Feature Exclusions

| Feature | Why Excluded | Reopen Only If |
| --- | --- | --- |
| full underlying delta hedge | would contaminate attribution and import too much old-round structure | fair-value core clearly works and attribution needs a hedge layer later |
| old winner symbol set and parameters | incompatible with current round | current-round evidence justifies new calibration |
| full IV-surface / Heston stack | too complex for current evidence | tiny proxy shows clear incremental value |
| direct `5200` inventory | current evidence says veto first | clean positive direct `5200` run appears |

## Signal / Fair Value Logic

- Signal:
  - `r4_w2_05`: plain fair-value `5300` baseline
  - `r4_w2_06`: same signal with horizon rescue
  - `r4_w2_07`: same signal with winner-style queue takeover
  - `r4_w2_08`: same signal with `5200` veto overlay
- Inputs: `VEX` and `5300` books, timestamp, optional `VEV_5200` market-trade
  context.
- Missing-signal behavior:
  - missing `VEX` or missing `5300` book disables the step
  - invalid rolling IV window disables the branch unless recent-mid fallback is
    available
  - missing `VEV_5200` state disables only the veto
- Process assumption that would invalidate this logic: `5300` has no direct
  edge even under improved execution.
- Multivariate or redundancy caveat: do not combine queue takeover, horizon,
  and veto logic into a single first-pass bot.

## Execution Logic

- Buy behavior:
  - quote or cross `5300` only when fair-value edge survives spread and cap
    checks
  - `r4_w2_07` may take market first when obvious mispricing exists
- Sell behavior: symmetric to buy behavior.
- Passive/resting order behavior:
  - rest near fair value when no obvious cross exists
  - do not chase in late or vetoed windows
- Stay-idle behavior:
  - invalid books
  - invalid fair-value window
  - veto active
  - late no-new-entry active
- No-trade / disable conditions:
  - `5300` spread above `10`
  - missing `VEX` anchor
  - no capacity

## Position And Risk Handling

- Position limits:
  - `VEX`: `200`
  - `VEV_5300`: `300`
- Aggregate buy capacity:
  - `VEX`: `200 - current_position`
  - `VEV_5300`: `300 - current_position`
- Aggregate sell capacity:
  - `VEX`: `200 + current_position`
  - `VEV_5300`: `300 + current_position`
- Inventory skew or reduction:
  - `5300` soft band `72`
  - same-side new entries above internal cap `120` blocked
  - queue-takeover branch uses smaller passive repost size after taking

## State And Runtime

- `traderData` use:
  - rolling IV window
  - last valid fair value
  - optional delta diagnostic
  - hold timers and veto cooldowns
- Imports: standard library plus `math`; no non-runtime research libraries
- Runtime risk: medium because rolling IV and queue state add logic, but still
  bounded to one direct strike plus one contextual strike
- Research-only dependencies excluded from uploadable bot: `yes`

## Expected Failure Cases

- Failure case: rolling IV fair value is too noisy to improve execution.
- Mitigation or validation: compare queue-takeover branch to plain baseline and
  inspect fill locations and markout.
- Failure case: `5200` veto simply suppresses the branch.
- Mitigation or validation: compare entry count and late-trade quality to plain
  baseline.
- Failure case: `5300` is dead regardless of better execution style.
- Mitigation or validation: classify the entire family as `no edge` and prune.

## Validation Plan

- Contract checks: only `VEX` and `5300` can trade; `5200` must remain
  context-only.
- Order sign and limit checks: positive buys, negative sells, no breach of
  `200/300` limits.
- Performance/run checks:
  - `5300`-attributed PnL and trade count
  - markout after queue-takeover fills
  - late-entry behavior
  - effect of `5200` veto on final path
- Debug signals to inspect:
  - fair value
  - rolling IV count
  - cross-vs-rest decision
  - veto timer
  - hold timer
  - delta diagnostic
- Linked-product attribution checks, if applicable:
  - separate `VEX` anchor effect from direct `5300` inventory contribution
- Giveback / retention checks, if applicable:
  - especially for `r4_w2_06` and `r4_w2_08`

## Implementation Handoff

- Target bot paths:
  - `rounds/round_4/bots/noel/canonical/r4_w2_05_5300_clean_value_retest.py`
  - `rounds/round_4/bots/noel/canonical/r4_w2_06_5300_horizon_hold_v2.py`
  - `rounds/round_4/bots/noel/canonical/r4_w2_07_5300_queue_takeover_probe.py`
  - `rounds/round_4/bots/noel/canonical/r4_w2_08_5300_with_5200_veto.py`
- Parameters to implement:
  - IV window `12`
  - min valid IV obs `6`
  - `5300` edge `2`
  - spread cap `10`
  - queue-takeover cross threshold `1`
  - max clip `12`
  - veto cooldown `2`
  - hold timer `6`
  - late no-new-entry final `22%`
  - giveback cutoff `45%`
- Known caveats:
  - this is the most explicit Wave 2 adaptation of the old winner style
  - the point is to test whether the style improves learnability, not to assume
    it is already the final winning architecture
