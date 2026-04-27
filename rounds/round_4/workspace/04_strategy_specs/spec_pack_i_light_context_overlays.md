# Spec Pack I: Light Context Overlays

## Review Status

- Status: `COMPLETED`
- Owner: Codex
- Reviewer: Human
- Reviewed on: 2026-04-27

## Candidate

- Candidate ID: `pack_i_light_context_overlays`
- Candidate priority tier: `implement-first`
- Evidence strength: `medium`
- Product scope: `VELVETFRUIT_EXTRACT`, optional `VEV_5300`, contextual voucher family
- Linked candidate file: `../03_strategy_candidates.md`

## Pack Members

| Candidate | Product Scope | Role In Pack | Target Bot Path |
| --- | --- | --- | --- |
| `r4_w2_09_vex_plus_5200_veto` | `VEX` plus contextual `VEV_5200` | simplest portability test of the best contextual signal | `rounds/round_4/bots/noel/canonical/r4_w2_09_vex_plus_5200_veto.py` |
| `r4_w2_10_vex_trade_to_book_light` | `VEX` | lightweight execution overlay | `rounds/round_4/bots/noel/canonical/r4_w2_10_vex_trade_to_book_light.py` |
| `r4_w2_11_vex_family_pressure_light` | `VEX` plus voucher family context | compact family-state incremental test | `rounds/round_4/bots/noel/canonical/r4_w2_11_vex_family_pressure_light.py` |
| `r4_w2_12_5300_spread_conditioned_parent_gate` | `VEX + VEV_5300` | parent-book quality gate inspired by winner architecture | `rounds/round_4/bots/noel/canonical/r4_w2_12_5300_spread_conditioned_parent_gate.py` |

## Review Decision

- `_index.md` spec status: `approved`
- Approved for implementation: `yes`
- Reviewer decision notes: User explicitly requested implementing all `15`
  Wave 2 bots and entering `Phase 05`. Treat that instruction as operational
  approval for exploratory implementation with validation caveats, even though
  this pack remains lower priority than `G/H/J` in the testing queue.
- Required changes before coding: none

## Sources

- Wiki facts: Round 4 fields and limits.
- EDA evidence:
  - `5200` danger-state context
  - trade-location context
  - engineered context over raw names
  - family framing remains unresolved but plausible
- Understanding summary: counterparties are context first.
- Post-run research memory:
  - `r4_w1_i03_5200_signal_only`
  - negative evidence against hard whole-bot vetoes
- Processed paper references:
  - `../research/papers_processed/cartea_2018_order_book_signals_processed.md`
  - `../research/papers_processed/kaeck_2019_informed_index_options_processed.md`

## Carry-Forward Context

- Validated carry-forward principles used:
  - keep context compact
  - use stronger parents only
- Untested hypotheses intentionally being tested:
  - the `5200` veto travels cleanly to the simplest live base
  - trade-to-book still matters when stripped to one axis
  - family-state may add something distinct from `5200`
- Anti-patterns explicitly avoided:
  - raw-name alpha
  - broad correlated context stacks
  - direct context inventory

## Selection Trace

- Based on candidates: `r4_w2_09`, `r4_w2_10`, `r4_w2_11`, `r4_w2_12`
- Signals used: `5200` veto portability, trade-location state, family-pressure
  hypothesis, and winner-style parent-book quality discipline.
- Alternatives considered: reopen Pack `D` whole-bot context or add more
  parent legs before proving the compact overlays.
- Why selected: this pack keeps the context layer alive without repeating the
  Wave 1 mistake of letting context become the whole strategy.
- Known caveats: `r4_w2_11` and `r4_w2_12` may prove dominated by simpler
  overlays.
- Branch posture: `coverage gap`

## Evidence Traceability

- Linked EDA Signals:
  - `mark22_seller_danger_state`
  - `trade_location_context`
  - `engineered_context_over_raw_names`
- Feature Evidence:
  - `r4_s10` is the strongest reusable contextual result so far
  - trade-to-book was promising in strategy but not yet canonically validated
- Metric Availability:
  - all selected context signals are online-usable
- Baseline vs richer model verdict:
  - compact one-axis overlays are preferred to family composites
- Multivariate Evidence:
  - family-pressure must remain separate from `5200` veto because they could be
    redundant
- Process / Distribution Assumptions:
  - the parent branch should already be live
  - context helps by blocking or softening bad entries
- Redundancy Decisions:
  - do not merge trade-to-book and family-pressure in the same bot
- Regime Assumptions:
  - contextual warning states occur early enough to affect execution
- Understanding Insight:
  - context is more credible as filter than as direct alpha
- Research tool evidence used, if any:
  - `cartea_2018` for execution posture
  - `kaeck_2019` for family-state framing
- Evidence gaps or strategy assumptions:
  - family-pressure proxy thresholds are assumptions

## Round-Specific Mechanics Contract

| Mechanic / Trader Function / Field | Source | Decision | Bot Behavior | Validation Check |
| --- | --- | --- | --- | --- |
| `Trader.run()` | trader contract | implement | trade `VEX`; `r4_w2_12` may also trade `5300`; other vouchers are context only | smoke test and tuple shape |
| `Trade.buyer` / `Trade.seller` | round 4 doc | implement selectively | use only for narrow warning or trade-location context | inspect disable reasons |
| voucher family context | round 4 doc | implement as context only except `5300` in `r4_w2_12` | no direct inventory outside the named parent | product-order audit |
| Manual challenge products | round 4 doc | exclude | no manual logic | code search |

## Linked-Product Framing Contract

- Product role: `parent branch plus compact context`
- Signal class: `microstructure | regime`
- Underlying role: `alpha` for `VEX`, `anchor` for `5300`
- Trading posture: `conditional`
- Natural hold horizon: `short hold`
- What makes this a trading leg instead of only a signal: these bots still
  trade the parent branch; context only changes entry quality.
- Rule that should prevent edge from turning into giveback: compact filter or
  book-quality gate blocks the known bad windows.

## Feature Contract

| Feature | Source Fields | Online Availability | Lifecycle Label | Role | Parameters | Multivariate Relationship | Process Assumption | Redundancy Decision | Missing-Signal Behavior | State / `traderData` Required | Validation / Invalidation Check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `5200` veto on `VEX` base | recent `VEV_5200` market trades, `Trade.seller`, timestamp | usable online | implementation candidate | risk control | block new `VEX` same-side entries for `2` steps after seller-warning event | shared family-state proxy | the best `5200` signal should travel to the simplest parent | keep only in `r4_w2_09` | missing `VEV_5200` removes the overlay only | cooldown timer | better close vs plain `VEX` base |
| light trade-to-book gate | trade price relative to current best bid/ask on `VEX` | usable online | implementation candidate | execution filter | do not extend inventory when last relevant trade is at adverse side and current spread not tight; 1-step disable | distinct from `5200` because book-state may trigger without counterparty cue | bad local fills can be filtered cheaply | keep only in `r4_w2_10` | if recent trade location missing, disable the filter only | last trade-location bucket | fill quality improves without killing branch |
| family-pressure light proxy | summed sign of recent family trades across `5000/5100/5200/5300` with simple dominance cap | usable online | implementation candidate | execution filter | trigger only when family pressure exceeds compact threshold and `5200` veto is not already active | potentially redundant with `5200`; must be tested alone | broader family stress might add timing value | keep only in `r4_w2_11` | missing family state disables only the overlay | short family-state cache | decisions differ from `r4_w2_09` in meaningful windows |
| parent-book quality gate | `VEX` spread, top depth, recent `VEX` trade-location, optional `5300` book | usable online | implementation candidate | execution filter | allow `5300` overlay only when parent `VEX` spread `<= 1`, top depth above floor, and last trade-location not adverse; max `5300` clip `10` | winner-style discipline adapted at parent level | active-leg failures may come from weak parent book states | keep only in `r4_w2_12` | missing parent quality disables the overlay | short parent-state cache | `5300` trades occur in cleaner parent states only |

## Feature Exclusions

| Feature | Why Excluded | Reopen Only If |
| --- | --- | --- |
| raw-name direct alpha | weak evidence and too easy to overfit | later isolated runs prove incremental value |
| broad context stack | attribution contamination | a compact overlay shows strong lift first |
| direct `5200` inventory | current evidence says no | clean positive direct run appears |
| full winner-style fair-value engine in this pack | reserved for Pack `H` and `J` | Packs `H/J` validate it clearly |

## Signal / Fair Value Logic

- Signal: inherit the parent branch signal and let context only veto or soften
  entries.
- Inputs: parent product book, recent market trades, trade-location bucket,
  family-state proxy where applicable.
- Missing-signal behavior: if the context feature is missing, fall back to the
  parent branch rather than fabricating context.
- Process assumption that would invalidate this logic: context features are
  only descriptive and do not improve actual decisions.
- Multivariate or redundancy caveat: `r4_w2_09` and `r4_w2_11` should not be
  implemented first in the same mini-batch unless a simpler priority decision
  is impossible.

## Execution Logic

- Buy behavior: trade the parent branch only when the branch signal is live and
  the overlay does not block it.
- Sell behavior: symmetric to buy behavior.
- Passive/resting order behavior: unchanged from the parent branch.
- Stay-idle behavior:
  - parent branch invalid
  - overlay blocks the trade
  - no capacity
- No-trade / disable conditions:
  - only the contextual feature's own disable rule should fire; these are not
    whole-bot vetoes

## Position And Risk Handling

- Position limits:
  - `VEX`: `200`
  - `VEV_5300` if used directly: `300`
- Aggregate buy capacity:
  - `VEX`: `200 - current_position`
  - `VEV_5300`: `300 - current_position`
- Aggregate sell capacity:
  - `VEX`: `200 + current_position`
  - `VEV_5300`: `300 + current_position`
- Inventory skew or reduction: inherited from parent branch

## State And Runtime

- `traderData` use: short caches for cooldowns, last trade-location bucket, and
  family-pressure proxy
- Imports: standard library only
- Runtime risk: low to medium
- Research-only dependencies excluded from uploadable bot: `yes`

## Expected Failure Cases

- Failure case: context overlays are redundant and do not change decisions
  meaningfully.
- Mitigation or validation: compare disable windows and trade overlap with the
  parent branch.
- Failure case: trade-to-book filter removes too much activity.
- Mitigation or validation: log filter trigger count and missed fills.

## Validation Plan

- Contract checks: only parent products may trade; all other symbols remain
  context-only.
- Order sign and limit checks: positive buys, negative sells, no limit breach.
- Performance/run checks:
  - close-vs-parent branch
  - disable count
  - trade overlap
  - final inventory
- Debug signals to inspect:
  - context trigger type
  - trade-location bucket
  - family-pressure score
  - parent-book quality gate
- Linked-product attribution checks, if applicable:
  - verify `r4_w2_12` changes `5300` quality rather than merely suppressing it
- Giveback / retention checks, if applicable:
  - secondary only; main question is decision quality

## Implementation Handoff

- Target bot paths:
  - `rounds/round_4/bots/noel/canonical/r4_w2_09_vex_plus_5200_veto.py`
  - `rounds/round_4/bots/noel/canonical/r4_w2_10_vex_trade_to_book_light.py`
  - `rounds/round_4/bots/noel/canonical/r4_w2_11_vex_family_pressure_light.py`
  - `rounds/round_4/bots/noel/canonical/r4_w2_12_5300_spread_conditioned_parent_gate.py`
- Parameters to implement:
  - veto cooldown `2`
  - trade-to-book adverse bucket disable `1` step
  - compact family-pressure threshold from short recent window
  - parent spread gate `<= 1`
  - `5300` clip `10`
- Known caveats:
  - this pack is useful only if it stays compact
  - if Packs `G/H/J` already answer the round clearly, some of these bots may
    never need implementation
