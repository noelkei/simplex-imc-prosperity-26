# Spec Pack C: 5300 Active Family

## Review Status

- Status: `COMPLETED`
- Owner: Codex
- Reviewer: Human
- Reviewed on: 2026-04-27

## Candidate

- Candidate ID: `pack_c_5300_active_family`
- Candidate priority tier: `spec-first`
- Evidence strength: `medium-high`
- Product scope: `VELVETFRUIT_EXTRACT`, `VEV_5300`, contextual `VEV_5100/5200`
- Linked candidate file: `../03_strategy_candidates.md`

## Pack Members

| Candidate | Product Scope | Role In Pack | Target Bot Path |
| --- | --- | --- | --- |
| `r4_s04_vex_5300_overlay` | `VEX + VEV_5300` | plain isolated `5300` branch | `rounds/round_4/bots/noel/canonical/r4_s04_vex_5300_overlay.py` |
| `r4_s09_5300_toxic_strike_gate` | `VEX + VEV_5300` plus `5100/5200` context | anti-signal gated `5300` | `rounds/round_4/bots/noel/canonical/r4_s09_5300_toxic_strike_gate.py` |
| `r4_s11_5300_horizon_hold` | `VEX + VEV_5300` | horizon-aware `5300` redesign | `rounds/round_4/bots/noel/canonical/r4_s11_5300_horizon_hold.py` |

## Review Decision

- `_index.md` spec status: `approved`
- Approved for implementation: `yes`
- Reviewer decision notes: User requested moving directly into `Phase 05` for the exploratory Wave 1 implementation set. Treat this pack as approved with caveats for exploration only, not final submission.
- Required changes before coding: none; keep the three branches close enough that the winning difference is interpretable.

## Sources

- Wiki facts: Round 4 product scope/limits and trader contract.
- EDA evidence: `5300` remains the only serious active-strike candidate, but
  with retention and cross-strike caveats.
- Understanding summary: `5300` should be treated as special, not as a generic
  basket member.
- Post-run research memory: `5300` had long-horizon support in `round_3`, but
  not enough to justify blind reuse.
- Playbook heuristics: none as primary evidence.

## Carry-Forward Context

- Validated carry-forward principles used:
  - `5300` deserves isolated treatment
  - `5100/5200` are more credible as anti-signal than as default inventory
- Untested hypotheses intentionally being tested:
  - `5300` needs toxic-neighbor gating
  - `5300` is primarily a hold/retention problem
- Anti-patterns explicitly avoided:
  - reopening the broad active strike basket
  - using `5200` as direct inventory inside the same branch

## Selection Trace

- Based on candidates: `r4_s04`, `r4_s09`, `r4_s11`
- Signals used: isolated `5300` overlay, toxic-neighbor quiet state, horizon
  and no-new-entry rules.
- Alternatives considered: plain `4000` and old-winner revalidation live in
  Pack B; counterparty-defense-first logic lives in Pack D.
- Why selected: `5300` is the main unresolved direct trading leg in `round_4`
  and deserves a clean three-way test.
- Known caveats: trade count may be sparse and make horizon conclusions noisy.
- Branch posture: `rescue via retention`

## Evidence Traceability

- Linked EDA Signals: `5300` specialness, `5200+` danger-state context,
  cross-strike role split.
- Feature Evidence: isolated `5300` remained the only active strike worthy of
  serious follow-up.
- Metric Availability: all direct features are online-observable.
- Baseline vs richer model verdict: richer logic is justified only if gated or
  horizon-aware variants outperform plain `5300`.
- Multivariate Evidence: cross-strike context matters more than symbol-local
  thinking for the active middle strikes.
- Process / Distribution Assumptions:
  - `5300` can be good, but only in narrower states
  - late entry and toxic neighbors are plausible failure modes
- Redundancy Decisions: horizon logic and neighbor gating must remain separate
  hypotheses.
- Regime Assumptions: toxic-neighbor activity in `5100/5200` is observable in
  time to matter.
- Understanding Insight: `5300` is special but unresolved.
- Research tool evidence used, if any: `doshi`, `nimalendran_son`,
  `garcia_ares`, `kaeck`.
- Evidence gaps or strategy assumptions:
  - hold timer and toxic-neighbor thresholds are strategy assumptions.

## Round-Specific Mechanics Contract

| Mechanic / Trader Function / Field | Source | Decision | Bot Behavior | Validation Check |
| --- | --- | --- | --- | --- |
| `Trader.run()` | trader contract | implement | trade `VEX`, `VEV_5300`, and contextual reads from `VEV_5100/5200` only | smoke test and tuple shape |
| `Trade.buyer` / `Trade.seller` | round 4 doc | implement selectively | used only as contextual anti-signal support, not direct trigger | inspect veto windows vs bad fills |
| `VEV_5100` / `VEV_5200` | round 4 doc | implement as context only | never hold direct inventory from these symbols in this pack | product-order audit |
| Manual challenge products | round 4 doc | exclude | no manual logic in uploadable bot | code contains no manual references |
| `bid()` | trader contract / round 4 doc | not applicable | no round-2-only behavior | class validity check |

## Linked-Product Framing Contract

- Product role: `active risk leg`
- Signal class: `regime | mixed`
- Underlying role: `anchor`
- Trading posture: `conditional`
- Natural hold horizon: `short / medium hold`
- What makes this a trading leg instead of only a signal: `5300` is the only
  non-ITM voucher with enough direct interest to merit isolated inventory.
- Rule that should prevent edge from turning into giveback: suppress `5300`
  entries in toxic neighbor states and add explicit no-new-entry / giveback
  rules where relevant.

## Feature Contract

| Feature | Source Fields | Online Availability | Lifecycle Label | Role | Parameters | Multivariate Relationship | Process Assumption | Redundancy Decision | Missing-Signal Behavior | State / `traderData` Required | Validation / Invalidation Check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `VEX` anchor plus `5300` overlay | `VEX` and `5300` best bid/ask, positions | usable online | implementation candidate | direct signal | `5300` spread cap `10`, overlay edge `2`, max `5300` clip `10`, soft `5300` band `60` | non-redundant vs `4000` overlay because different strike role | isolated `5300` can still monetize in cleaner states | keep | missing `5300` book disables overlay only | optional last anchor state | compare plain `r4_s04` vs gated variants |
| toxic-neighbor quiet state | `5100/5200` books and market-trade state | usable online | implementation candidate | execution filter | disable `5300` entries when `5100/5200` spread shock active, `Mark 22` seller state active, or `5200` concentration `high`; 2-step cooldown | cross-strike layer intentionally separate from horizon layer | bad neighbor states reveal poor `5300` conditions | keep in `r4_s09` only | if contextual products missing, revert to plain `r4_s04` | 2-step cooldown timer | compare `r4_s09` vs `r4_s04` |
| horizon hold rule | timestamp/session progress, current `5300` entry state | usable online | implementation candidate | risk control | no new `5300` entries after final `25%` of day; max hold timer `6` decision steps; giveback cutoff `50%` of peak unrealized edge | different from toxic-neighbor gating | `5300` failure may be retention, not signal | keep in `r4_s11` only | if timer state missing, flatten and reset | entry timestamp, local edge peak, hold timer | compare `r4_s11` vs `r4_s04` |
| spread-state filter | `5300` spread and top depth | usable online | implementation candidate | execution filter | reduced size when spread `8-10`, disable above `10`, passive only when spread `>= 6` but clean state | low-value supporting filter | wide active-strike books worsen fills | keep | disable overlay if invalid | none | fill-quality split by spread bucket |

## Feature Exclusions

| Feature | Why Excluded | Reopen Only If |
| --- | --- | --- |
| direct `5200` inventory | current evidence says signal-only / danger-state | Pack D and `r4_s10` contradict this clearly |
| family-pressure proxy | would blur the `5300`-specific question | Pack E shows decisive incremental lift |
| heavy pricing stack | not needed to answer the `5300` question | simple surface proxy materially changes outcomes |

## Signal / Fair Value Logic

- Signal:
  - `r4_s04`: isolated `5300` overlay against `VEX`
  - `r4_s09`: same signal but only in quiet neighbor states
  - `r4_s11`: same signal but with explicit horizon control
- Inputs: `VEX` and `5300` books, contextual `5100/5200` state, session time.
- Missing-signal behavior:
  - missing `VEX` disables the branch
  - missing `5300` disables the overlay
  - missing neighbor state removes only the extra gate
- Process assumption that would invalidate this logic: `5300` has no direct
  edge at all, regardless of gating or hold style.
- Multivariate or redundancy caveat: do not combine toxic-neighbor and horizon
  logic into one branch before isolated testing.

## Execution Logic

- Buy behavior: enter `5300` only when overlay edge is present and the branch's
  contextual conditions are satisfied.
- Sell behavior: symmetric to buy behavior.
- Passive/resting order behavior: allow modest passive participation only in
  cleaner spread states; avoid passive expansion in noisy late-session states.
- Stay-idle behavior: missing book, toxic-neighbor state, late-session block,
  no capacity, or giveback cutoff active.

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
  - `5300` soft band `60`
  - stop new same-side overlay entries above internal cap `100`
  - flatten faster than ITM packs when contextual state deteriorates

## State And Runtime

- `traderData` use: short JSON blob for cooldown timers, hold timers, and
  current entry diagnostics.
- Imports: standard library only.
- Runtime risk: low; only a few products and short timers tracked.
- Research-only dependencies excluded from uploadable bot: `yes`

## Expected Failure Cases

- Failure case: plain `5300` shows no edge and both richer variants merely
  reduce already weak activity.
- Mitigation or validation: classify as `no edge` and deprioritize direct
  `5300` inventory.
- Failure case: `5300` has edge, but horizon and gating assumptions conflict.
- Mitigation or validation: compare `r4_s09` and `r4_s11` attribution directly.

## Validation Plan

- Contract checks: only `VEX`/`5300` orders allowed; `5100/5200` must remain
  context-only.
- Order sign and limit checks: positive buys, negative sells, no breach of
  `200/300` limits.
- Performance/run checks: `5300`-attributed PnL, trade count, path quality,
  giveback after entry, late-entry behavior, neighbor-state failure rate.
- Debug signals to inspect: `5300` edge, neighbor-state gate, hold timer,
  giveback cutoff, position.
- Linked-product attribution checks, if applicable: separate anchor and `5300`
  contribution and inspect whether context changed `5300` quality.
- Giveback / retention checks, if applicable: this is a primary objective of
  the pack, especially for `r4_s11`.

## Implementation Handoff

- Target bot paths:
  - `rounds/round_4/bots/noel/canonical/r4_s04_vex_5300_overlay.py`
  - `rounds/round_4/bots/noel/canonical/r4_s09_5300_toxic_strike_gate.py`
  - `rounds/round_4/bots/noel/canonical/r4_s11_5300_horizon_hold.py`
- Parameters to implement:
  - `5300` spread cap `10`
  - `5300` edge `2`
  - `5300` clip `10`
  - toxic-neighbor cooldown `2` steps
  - no new entries in final `25%` of day
  - hold timer `6` steps
  - giveback cutoff `50%`
- Known caveats: if `5300` is completely dead, accept that the correct outcome
  of the pack is pruning, not rescuing it at any cost.
