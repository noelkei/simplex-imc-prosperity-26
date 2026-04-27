# Spec Pack B: Round 3 Revalidation

## Review Status

- Status: `COMPLETED`
- Owner: Codex
- Reviewer: Human
- Reviewed on: 2026-04-27

## Candidate

- Candidate ID: `pack_b_round3_revalidation`
- Candidate priority tier: `spec-first`
- Evidence strength: `strong`
- Product scope: `VELVETFRUIT_EXTRACT`, `VEV_4000`
- Linked candidate file: `../03_strategy_candidates.md`

## Pack Members

| Candidate | Product Scope | Role In Pack | Target Bot Path |
| --- | --- | --- | --- |
| `r4_s03_vex_4000_overlay` | `VEX + VEV_4000` | plain ITM overlay baseline | `rounds/round_4/bots/noel/canonical/r4_s03_vex_4000_overlay.py` |
| `r4_s13_4000_benign_flow_overlay` | `VEX + VEV_4000` | ITM overlay with benign-flow conditioning | `rounds/round_4/bots/noel/canonical/r4_s13_4000_benign_flow_overlay.py` |
| `r4_s15_round3_winner_revalidation` | `VEX + VEV_4000` | old winner family with round-4 danger filters | `rounds/round_4/bots/noel/canonical/r4_s15_round3_winner_revalidation.py` |

## Review Decision

- `_index.md` spec status: `approved`
- Approved for implementation: `yes`
- Reviewer decision notes: User requested moving directly into `Phase 05` for the exploratory Wave 1 implementation set. Treat this pack as approved with caveats for exploration only, not final submission.
- Required changes before coding: none; keep the differences between the three bots narrow and attributable.

## Sources

- Wiki facts: Round 4 product scope/limits and shared trader contract.
- EDA evidence: `VEX` anchor dominance, `4000` as the most plausible ITM
  structural overlay, and counterparty-conditioned execution context.
- Understanding summary: old winner ingredients still matter, but must be
  rechecked under the new tape.
- Post-run research memory: `round_3` winner family was delta-1 plus ITM;
  broad baskets and raw imbalance were anti-patterns.
- Playbook heuristics: none as primary evidence.

## Carry-Forward Context

- Validated carry-forward principles used:
  - `delta-1 first`
  - `VEX` as anchor
  - `4000` as the strongest ITM overlay candidate
- Untested hypotheses intentionally being tested:
  - benign-flow conditioning improves the old ITM add-on
  - the old winner survives if danger-state filters are added
- Anti-patterns explicitly avoided:
  - broad `5000/5100/5200/5300` baskets
  - direct raw-name alpha
  - reopening upper/floor strikes inside the winner-family test

## Selection Trace

- Based on candidates: `r4_s03`, `r4_s13`, `r4_s15`
- Signals used: `VEX` anchor, `4000` structural overlay, benign-flow filter,
  `Mark 22` veto, trade-to-book execution gate.
- Alternatives considered: direct `5300` tests live in Pack C; family-pressure
  and surface support live elsewhere.
- Why selected: this pack asks the most valuable carry-forward question in
  `round_4`: whether the best `round_3` family survives, improves, or dies.
- Known caveats: `r4_s15` is the richest branch in the pack and may blur
  attribution if not compared carefully to the simpler controls.
- Branch posture: `protect winner`

## Evidence Traceability

- Linked EDA Signals: `VEX_anchor_same_time`, `option_book_role_split`,
  engineered context over raw names, benign-flow idea from markout studies.
- Feature Evidence: `4000` remained the cleanest ITM add-on candidate in the
  current interpretation set.
- Metric Availability: all live features are online-observable; no offline-only
  pricing stack required.
- Baseline vs richer model verdict: `richer adds value` only if the added
  filters improve path quality over the plain `4000` overlay.
- Multivariate Evidence: raw names are weak alone; engineered context is more
  defensible.
- Process / Distribution Assumptions:
  - the ITM overlay is structurally safer than active middle strikes
  - bad counterparty/book states should degrade overlay quality
- Redundancy Decisions: `r4_s13` and `r4_s15` must differ in clear ways from
  `r4_s03`, not just add correlated filters for sport.
- Regime Assumptions: benign flow and normal book state are distinct enough to
  define cleaner overlay windows.
- Understanding Insight: old winners must be revalidated, not trusted.
- Research tool evidence used, if any: processed paper support from
  `vasios`, `doshi`, `choi`, `muravyev`, and `stoikov_saglam`.
- Evidence gaps or strategy assumptions:
  - the exact threshold for "benign flow" is a strategy assumption to be tested.

## Round-Specific Mechanics Contract

| Mechanic / Trader Function / Field | Source | Decision | Bot Behavior | Validation Check |
| --- | --- | --- | --- | --- |
| `Trader.run()` | trader contract | implement | trade `VEX` and `VEV_4000` only | smoke test and tuple shape |
| `Trade.buyer` / `Trade.seller` | round 4 doc | implement selectively | used only in `r4_s13` and `r4_s15` as contextual filters, never naked alpha | log veto state against realized fills |
| Voucher products | round 4 doc | implement selectively | `VEV_4000` only; no other vouchers in this pack | product-order audit |
| Manual challenge products | round 4 doc | exclude | no manual logic in uploadable bot | code contains no manual references |
| `bid()` | trader contract / round 4 doc | not applicable | no round-2-only behavior | class validity check |

## Linked-Product Framing Contract

- Product role: `ITM structural overlay`
- Signal class: `mixed`
- Underlying role: `anchor`
- Trading posture: `conditional`
- Natural hold horizon: `short / medium hold`
- What makes this a trading leg instead of only a signal: `VEV_4000` is the
  only carry-forward overlay with enough structural support to merit direct
  inventory in Wave 1.
- Rule that should prevent edge from turning into giveback: disable or reduce
  the overlay under adverse counterparty/book context instead of forcing trades.

## Feature Contract

| Feature | Source Fields | Online Availability | Lifecycle Label | Role | Parameters | Multivariate Relationship | Process Assumption | Redundancy Decision | Missing-Signal Behavior | State / `traderData` Required | Validation / Invalidation Check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `VEX` anchor edge | `VEX` best bid/ask and position | usable online | implementation candidate | direct signal | anchor quote width `1`, cross edge `2`, max `VEX` clip `10`, soft `VEX` band `70` | core non-redundant anchor | `VEX` still carries the cleanest same-time information | keep | if `VEX` book invalid, disable overlay trading | optional last anchor state only | compare to Pack A `r4_s01` |
| `VEV_4000` structural overlay | `VEV_4000` best bid/ask, `VEX` anchor state | usable online | implementation candidate | direct signal | overlay activate only if `4000` spread `<= 8`, overlay edge `>= 2`, max `4000` clip `15`, soft `4000` band `90` | low redundancy with base, but must stay separate from `5300` logic | `4000` behaves as benign ITM support more often than active risk leg | keep | if voucher book invalid, trade anchor only | none beyond optional anchor state | compare `r4_s03` vs `r4_s01` |
| benign-flow filter | `market_trades` buyer/seller names, concentration metrics, trade location bucket | usable online | implementation candidate | execution filter | disable add-on if `5200+` `Mark 22` seller state active, if concentration state is `high`, or if last trade bucket is worst-book | overlaps with broader danger-state logic but narrower in scope | bad flow state hurts add-on quality before it hurts the whole anchor | keep only in `r4_s13` / `r4_s15` | if trade data sparse, revert to plain `r4_s03` behavior | short rolling state for counts/buckets | compare `r4_s13` against `r4_s03` |
| trade-to-book gate | same-step book state and trade-location bucket | usable online | implementation candidate | execution filter | allow overlay only in neutral/favorable book state; one-step cooldown after worst-book print | partially related to benign-flow filter | execution quality matters for the winner family | keep only in `r4_s15` | if unavailable, disable gate not whole bot | 1-step recent-state memory | compare `r4_s15` vs `r4_s13` |
| hard danger veto | `5200+` seller-side `Mark 22` activity | usable online | implementation candidate | risk control | hard veto duration `3` decision steps after strong signal, immediate disable of new overlay entries | correlated with broader danger-state, but intentionally explicit here | the old winner should be protected from the clearest adverse state | keep only in `r4_s15` | if no trade tape, do not invent the veto | 3-step timer in `traderData` | markout/fill quality during veto windows |

## Feature Exclusions

| Feature | Why Excluded | Reopen Only If |
| --- | --- | --- |
| `5300` active overlays | different thesis and risk shape | Pack C fails and `4000` pack is inconclusive |
| family pressure proxy | too broad for old-winner revalidation | Pack E shows clear distinct value |
| heavy surface or Heston logic | too complex and not needed for this pack | tiny online pricing proxy proves essential |

## Signal / Fair Value Logic

- Signal:
  - `r4_s03`: plain `VEX` anchor plus `4000` structural overlay
  - `r4_s13`: same overlay only under benign flow
  - `r4_s15`: old winner family plus hard defensive context
- Inputs: `VEX` and `VEV_4000` books, positions, recent market-trade
  participant state, recent trade-location bucket.
- Missing-signal behavior:
  - missing `VEX` disables the whole strategy
  - missing `4000` book reverts to anchor-only behavior where appropriate
  - missing trade tape removes only the contextual filters
- Process assumption that would invalidate this logic: `4000` is no longer the
  most benign direct overlay in `round_4`.
- Multivariate or redundancy caveat: benign-flow and trade-to-book gates must
  not become a feature dump.

## Execution Logic

- Buy behavior: buy `VEX` or `VEV_4000` only when the relevant edge threshold
  is met and the contextual filters allow it.
- Sell behavior: symmetric to buy behavior with the same contextual filters.
- Passive/resting order behavior: anchor may quote passively in neutral books;
  the `4000` overlay should be more conservative and may prefer crossing only
  when clear edge exists.
- Stay-idle behavior: hard danger veto active, voucher spread too wide,
  contextual state bad, or no capacity.

## Position And Risk Handling

- Position limits:
  - `VEX`: exchange limit `200`
  - `VEV_4000`: exchange limit `300`
- Aggregate buy capacity:
  - `VEX`: `200 - current_position`
  - `VEV_4000`: `300 - current_position`
- Aggregate sell capacity:
  - `VEX`: `200 + current_position`
  - `VEV_4000`: `300 + current_position`
- Inventory skew or reduction:
  - `VEX` soft band `70`
  - `VEV_4000` soft band `90`
  - cut overlay size first when either leg grows too large

## State And Runtime

- `traderData` use: small JSON blob for short-horizon danger-veto timers,
  concentration counts, and last trade-location bucket.
- Imports: standard library only.
- Runtime risk: O(number of tracked trades/products) with small constant.
- Research-only dependencies excluded from uploadable bot: `yes`

## Expected Failure Cases

- Failure case: the plain `4000` overlay still works, but context filters only
  reduce activity without improving path quality.
- Mitigation or validation: compare `r4_s03`, `r4_s13`, and `r4_s15` directly.
- Failure case: `r4_s15` looks worse because it is over-filtered rather than
  because the old winner is gone.
- Mitigation or validation: inspect missed-good-trade counts and veto windows.

## Validation Plan

- Contract checks: only `VEX` and `VEV_4000` traded; trade-tape use defensive
  only.
- Order sign and limit checks: positive buys, negative sells, no breach of
  `200/300` exchange limits.
- Performance/run checks: compare the three bots on total PnL, path quality,
  overlay attribution, veto-window behavior, and giveback after entry.
- Debug signals to inspect: anchor edge, overlay edge, benign-flow state,
  trade-location bucket, veto timer, positions.
- Linked-product attribution checks, if applicable: split `VEX` and `4000`
  contributions and inspect whether the overlay or the anchor drove results.
- Giveback / retention checks, if applicable: inspect whether contextual
  filters reduce post-entry reversals.

## Implementation Handoff

- Target bot paths:
  - `rounds/round_4/bots/noel/canonical/r4_s03_vex_4000_overlay.py`
  - `rounds/round_4/bots/noel/canonical/r4_s13_4000_benign_flow_overlay.py`
  - `rounds/round_4/bots/noel/canonical/r4_s15_round3_winner_revalidation.py`
- Parameters to implement:
  - `VEX` cross edge `2`, clip `10`, soft band `70`
  - `4000` overlay edge `2`, spread cap `8`, clip `15`, soft band `90`
  - hard danger veto timer `3` steps
  - contextual fallback to plain overlay when trade tape is sparse
- Known caveats: preserve attribution by keeping `r4_s03`, `r4_s13`, and
  `r4_s15` as a narrow ladder, not three unrelated rewrites.
