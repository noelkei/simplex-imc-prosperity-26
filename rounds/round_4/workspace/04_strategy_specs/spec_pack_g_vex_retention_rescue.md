# Spec Pack G: VEX Retention Rescue

## Review Status

- Status: `COMPLETED`
- Owner: Codex
- Reviewer: Human
- Reviewed on: 2026-04-27

## Candidate

- Candidate ID: `pack_g_vex_retention_rescue`
- Candidate priority tier: `spec-first`
- Evidence strength: `strong`
- Product scope: `VELVETFRUIT_EXTRACT`, contextual `VEV_5200`
- Linked candidate file: `../03_strategy_candidates.md`

## Pack Members

| Candidate | Product Scope | Role In Pack | Target Bot Path |
| --- | --- | --- | --- |
| `r4_w2_01_vex_late_no_new_entry` | `VEX` | pure late-entry rescue | `rounds/round_4/bots/noel/canonical/r4_w2_01_vex_late_no_new_entry.py` |
| `r4_w2_02_vex_peak_giveback_stop` | `VEX` | peak-to-close rescue | `rounds/round_4/bots/noel/canonical/r4_w2_02_vex_peak_giveback_stop.py` |
| `r4_w2_03_vex_toxic_window_cooldown` | `VEX` plus contextual `VEV_5200` | narrow veto timing rescue | `rounds/round_4/bots/noel/canonical/r4_w2_03_vex_toxic_window_cooldown.py` |
| `r4_w2_04_vex_smaller_second_clip` | `VEX` | sizing diagnosis | `rounds/round_4/bots/noel/canonical/r4_w2_04_vex_smaller_second_clip.py` |

## Review Decision

- `_index.md` spec status: `approved`
- Approved for implementation: `yes`
- Reviewer decision notes: User explicitly requested implementing all `15`
  Wave 2 bots and entering `Phase 05`. Treat that instruction as operational
  approval for exploratory implementation with validation caveats.
- Required changes before coding: none

## Sources

- Wiki facts: Round 4 product scope, position limits, and trader contract.
- EDA evidence:
  - `VEX` remains the strongest base and anchor.
  - `VEV_5200` contextual state is useful as veto, not default inventory.
- Understanding summary:
  - `VEX` is the default base.
  - counterparty information is context first.
- Post-run research memory:
  - `r4_w1_i01_vex_over_hydro`
  - `r4_w1_i03_5200_signal_only`
  - `r4_w1_i04_late_session_retention`
- Playbook heuristics: none as primary evidence.

## Carry-Forward Context

- Validated carry-forward principles used:
  - keep `VEX` as the primary delta-1 base
  - make retention a first-class design axis
  - use counterparty context as veto, not as a whole-bot thesis
- Untested hypotheses intentionally being tested:
  - a late-session no-new-entry rule rescues the live `VEX` base
  - a peak giveback stop rescues path quality without killing the branch
  - narrow `5200` warning windows outperform broad contextual gating
- Anti-patterns explicitly avoided:
  - standalone `HYDRO` reopens
  - hard whole-bot vetoes
  - adding new alpha layers while the base retention question is unresolved

## Selection Trace

- Based on candidates: `r4_w2_01`, `r4_w2_02`, `r4_w2_03`, `r4_w2_04`
- Signals used:
  - Wave 1 A/B/D late giveback pattern
  - `VEX` as only live base
  - `VEV_5200` danger-state context around bad late extensions
- Alternatives considered:
  - broad `VEX` logic rewrite
  - immediate move to richer execution overlays
  - direct `HYDRO` re-tests
- Why selected: Pack `G` is the cheapest and cleanest way to learn whether the
  best live base is failing because of edge quality or because of retention.
- Known caveats:
  - all four branches depend on the parent `VEX` base still engaging
  - late giveback evidence is still based on a small number of open-short paths
- Branch posture: `rescue via retention`

## Evidence Traceability

- Linked EDA Signals:
  - `VEX_anchor_same_time`
  - `mark22_seller_danger_state`
  - `engineered_context_over_raw_names`
- Feature Evidence:
  - `r4_s01` showed life but poor retention
  - `r4_s10` showed that a narrow contextual veto can remove a harmful late
    extension
- Metric Availability:
  - all implemented features are online-usable from book, position, timestamp,
    and `market_trades`
- Baseline vs richer model verdict:
  - retention-first rescue is higher ROI than adding richer alpha to a weakly
    retained base
- Multivariate Evidence:
  - `5200` context should stay a narrow warning filter because broader
    contextual gating was over-suppressive in Wave 1
- Process / Distribution Assumptions:
  - late-session `VEX` entries are lower quality than earlier `VEX` entries
  - the worst late extensions are observable through either clock time or
    immediate contextual warning
- Redundancy Decisions:
  - no-new-entry, giveback stop, cooldown, and smaller repeat clip must remain
    separate axes
- Regime Assumptions:
  - the `98000+` or final-session region remains the main giveback zone until
    contradicted by new runs
- Understanding Insight:
  - `VEX` is infrastructure plus possible alpha; it should be fixed before
    being wrapped by more complex overlays
- Research tool evidence used, if any:
  - run-informed diagnosis from `06_testing/round_4_wave1_pack_abd_partial_synthesis.md`
- Evidence gaps or strategy assumptions:
  - exact retention thresholds are strategy assumptions and must be logged in
    validation

## Round-Specific Mechanics Contract

| Mechanic / Trader Function / Field | Source | Decision | Bot Behavior | Validation Check |
| --- | --- | --- | --- | --- |
| `Trader.run()` | trader contract | implement | trade `VEX` only; `VEV_5200` may be read as context in `r4_w2_03` | smoke test and tuple shape |
| `Trade.buyer` / `Trade.seller` | round 4 doc | implement selectively | only `r4_w2_03` may read `Mark 22` or equivalent seller warning state | inspect cooldown windows against skipped late trades |
| `VEV_5200` | round 4 doc | implement as context only | no direct `VEV_5200` inventory in this pack | product-order audit |
| Manual challenge products | round 4 doc | exclude | no manual logic | code search shows no manual references |
| `bid()` | trader contract / round 4 doc | not applicable | no round-2-only mechanics | class validity check |

## Linked-Product Framing Contract

- Product role: `delta-1 base with contextual warning`
- Signal class: `microstructure | regime`
- Underlying role: `alpha`
- Trading posture: `conditional`
- Natural hold horizon: `short hold`
- What makes this a trading leg instead of only a signal: `VEX` itself is the
  tradable base; contextual inputs only decide whether to continue entering.
- Rule that should prevent edge from turning into giveback: explicit late
  no-new-entry, giveback stop, cooldown, or repeat-clip size reduction.

## Feature Contract

| Feature | Source Fields | Online Availability | Lifecycle Label | Role | Parameters | Multivariate Relationship | Process Assumption | Redundancy Decision | Missing-Signal Behavior | State / `traderData` Required | Validation / Invalidation Check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| inherited `VEX` base edge | `VEX` best bid/ask, local spread, local depth, current position | usable online | implementation candidate | direct signal | carry forward the Wave 1 `VEX` base entry logic unchanged; spread cap `1`, max clip `16`, soft band `60` | non-redundant parent edge | the parent `VEX` branch is still the best live base | keep unchanged across all four variants | missing `VEX` book disables trading | optional last-side memory | compare all variants to the Wave 1 `r4_s01` baseline |
| late no-new-entry rule | `timestamp`, current `VEX` position, current side | usable online | implementation candidate | risk control | no new same-side entries after `98000` or final `18%` of session; exits still allowed | separate from giveback stop | late entries are lower quality than earlier entries | keep only in `r4_w2_01` | if time state invalid, disable this feature only | no extra state | improved close without killing early fills |
| peak giveback stop | mark-to-market path on open `VEX` inventory | usable online | implementation candidate | risk control | local peak-tracking window on current open position; flatten or disable re-entry if giveback exceeds `40%` of local unrealized peak or `22` ticks equivalent | separate from no-new-entry because it can trigger earlier | giveback reflects retention failure rather than bad initial entry | keep only in `r4_w2_02` | if peak state absent, fall back to parent branch | local peak value, current entry side | peak-to-close drawdown compresses materially |
| toxic-window cooldown | recent `VEV_5200` market trades, `Trade.seller`, `timestamp` | usable online | implementation candidate | execution filter | 2-step cooldown after recent `VEV_5200` trade with `Mark 22` on seller side or equivalent cached danger-state flag | intentionally merged with contextual warning; do not add other context features here | the best use of `5200` is narrow timing veto | keep only in `r4_w2_03` | missing `VEV_5200` state removes only cooldown | 2-step cooldown timer | skips late bad extension while still matching early path |
| smaller second clip | current `VEX` position, last entry side, count of same-side extensions | usable online | implementation candidate | risk control | first clip `16`, second same-side clip `8`, third disabled until flatten or side reversal | separate sizing-only diagnosis | damage may come from repeating a valid idea with too much size | keep only in `r4_w2_04` | if extension count missing, default to parent sizing | same-side extension counter | second clip damage shrinks without flattening total opportunity |

## Feature Exclusions

| Feature | Why Excluded | Reopen Only If |
| --- | --- | --- |
| direct `HYDRO` branch | negative Wave 1 evidence and wrong question for this pack | a linked-product role appears later |
| direct `4000` or `5300` inventory | would contaminate the retention diagnosis | Pack `H` or `J` gives decisive evidence first |
| hard contextual veto | Wave 1 already showed over-suppression | lighter veto still fails cleanly |
| family-pressure overlay | lower-priority incremental context | Pack `I` shows distinct lift |

## Signal / Fair Value Logic

- Signal: inherit the existing Wave 1 `VEX` base signal unchanged and test only
  retention modifiers.
- Inputs: `VEX` top of book, position, timestamp, and optional `VEV_5200`
  recent market-trade state for `r4_w2_03`.
- Missing-signal behavior:
  - missing `VEX` book disables the bot for the step
  - missing `VEV_5200` state disables only the cooldown feature
- Process assumption that would invalidate this logic: the base `VEX` edge was
  never real, and the apparent giveback is only noise.
- Multivariate or redundancy caveat: do not combine no-new-entry and giveback
  stop into the same first-pass branch.

## Execution Logic

- Buy behavior: use the inherited `VEX` base edge logic, then apply only the
  variant's retention gate.
- Sell behavior: symmetric to buy behavior.
- Passive/resting order behavior: unchanged from the parent `VEX` base.
- Stay-idle behavior:
  - invalid `VEX` book
  - no capacity
  - variant-specific no-new-entry or cooldown condition active
- No-trade / disable conditions:
  - no new same-side trades when the retention rule is triggered

## Position And Risk Handling

- Position limits: `VEX` exchange limit `200`
- Aggregate buy capacity: `200 - current_position`
- Aggregate sell capacity: `200 + current_position`
- Inventory skew or reduction:
  - soft band `60`
  - parent branch maximum clip `16`
  - branch-specific smaller repeat clip in `r4_w2_04`

## State And Runtime

- `traderData` use:
  - optional cooldown timer
  - local unrealized peak tracker
  - same-side extension count
- Imports: standard library only
- Runtime risk: low
- Research-only dependencies excluded from uploadable bot: `yes`

## Expected Failure Cases

- Failure case: the base `VEX` edge is fake, so retention rules only reduce an
  already weak branch.
- Mitigation or validation: compare path quality and trade count to `r4_s01`;
  if no branch retains positive structure, classify as `no edge`.
- Failure case: the chosen late cutoff is too early and suppresses legitimate
  early-middle opportunities.
- Mitigation or validation: inspect first missed trade timestamps and compare
  to peak PnL timing.
- Failure case: cooldown and no-new-entry windows overlap too heavily.
- Mitigation or validation: keep them in separate bots and log disable reasons.

## Validation Plan

- Contract checks: only `VEX` traded; `VEV_5200` remains context-only.
- Order sign and limit checks: positive buys, negative sells, no breach of
  `VEX` limit `200`.
- Performance/run checks:
  - close-vs-peak drawdown
  - late-entry count
  - end-of-session inventory
  - PnL path relative to `r4_s01`
- Debug signals to inspect:
  - disable reason
  - late cutoff triggered
  - giveback percentage
  - cooldown timer
  - repeat clip count
- Linked-product attribution checks, if applicable: not applicable beyond
  verifying `VEV_5200` never generates direct orders.
- Giveback / retention checks, if applicable: this is the primary objective of
  the pack.

## Implementation Handoff

- Target bot paths:
  - `rounds/round_4/bots/noel/canonical/r4_w2_01_vex_late_no_new_entry.py`
  - `rounds/round_4/bots/noel/canonical/r4_w2_02_vex_peak_giveback_stop.py`
  - `rounds/round_4/bots/noel/canonical/r4_w2_03_vex_toxic_window_cooldown.py`
  - `rounds/round_4/bots/noel/canonical/r4_w2_04_vex_smaller_second_clip.py`
- Parameters to implement:
  - `VEX` max clip `16`
  - no-new-entry cutoff `98000` or final `18%`
  - giveback stop `40%` or `22` ticks equivalent
  - cooldown `2` steps
  - second clip size `8`
- Known caveats:
  - this pack deliberately assumes the parent `VEX` signal is worth rescuing
  - if all four branches fail cleanly, the right output is pruning, not more
    retention complexity
