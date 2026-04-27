# Spec Pack A: Delta-1 Controls

## Review Status

- Status: `COMPLETED`
- Owner: Codex
- Reviewer: Human
- Reviewed on: 2026-04-27

## Candidate

- Candidate ID: `pack_a_delta1_controls`
- Candidate priority tier: `spec-first`
- Evidence strength: `strong`
- Product scope: `VELVETFRUIT_EXTRACT`, `HYDROGEL_PACK`
- Linked candidate file: `../03_strategy_candidates.md`

## Pack Members

| Candidate | Product | Role In Pack | Target Bot Path |
| --- | --- | --- | --- |
| `r4_s01_vex_base_control` | `VELVETFRUIT_EXTRACT` | anchor control | `rounds/round_4/bots/noel/historical/r4_s01_vex_base_control.py` |
| `r4_s02_hydro_base_control` | `HYDROGEL_PACK` | independent delta-1 control | `rounds/round_4/bots/noel/historical/r4_s02_hydro_base_control.py` |

## Review Decision

- `_index.md` spec status: `approved`
- Approved for implementation: `yes`
- Reviewer decision notes: User requested moving directly into `Phase 05` for the exploratory Wave 1 implementation set. Treat this pack as approved with caveats for exploration only, not final submission.
- Required changes before coding: none; preserve control purity and validate against later overlay packs.

## Sources

- Wiki facts: Round 4 product scope/limits and shared `Trader.run()` contract.
- EDA evidence: `round_4` anchor/base framing in `01_eda/` and
  `02_understanding.md`.
- Understanding summary: `delta-1 first`, `VEX` as anchor, `HYDRO` as
  independent control.
- Post-run research memory: `round_3` memory says the cleanest winner family
  started from delta-1 and ITM, so plain controls remain required.
- Playbook heuristics: none as primary evidence.

## Carry-Forward Context

- Validated carry-forward principles used:
  - `delta-1 first`
  - controls must remain feature-light
- Untested hypotheses intentionally being tested:
  - whether `VEX` clearly dominates `HYDRO` as a base in `round_4`
- Anti-patterns explicitly avoided:
  - adding counterparty or voucher context to the controls
  - turning controls into composites

## Selection Trace

- Based on candidates: `r4_s01_vex_base_control`, `r4_s02_hydro_base_control`
- Signals used: local top-of-book edge, spread state, simple imbalance state
- Alternatives considered: direct voucher overlays and counterparty-conditioned
  branches are deferred to other packs so these controls stay clean.
- Why selected: every later pack needs clean baselines to tell whether a new
  overlay genuinely adds value.
- Known caveats: these controls may not be final winners, but they are required
  to interpret the rest of Wave 1.
- Branch posture: `clean isolation test`

## Evidence Traceability

- Linked EDA Signals: `VEX_anchor_same_time`, clean `HYDRO` delta-1 branch,
  low-complexity anchor logic.
- Feature Evidence: strong carry-forward support for delta-1-first.
- Metric Availability: fully online from current order books and positions.
- Baseline vs richer model verdict: `baseline only` for this pack by design.
- Multivariate Evidence: no extra multivariate layer required for controls.
- Process / Distribution Assumptions: liquid delta-1 names are the least
  contaminated place to start.
- Redundancy Decisions: no counterparty, no family pressure, no pricing support
  layer in this pack.
- Regime Assumptions: normal spread state and visible best-book liquidity are
  sufficient for the first control pass.
- Understanding Insight: the round's novelty should be layered over clean bases
  rather than replacing them.
- Research tool evidence used, if any: none required.
- Evidence gaps or strategy assumptions:
  - initial quote widths and clip sizes are strategy assumptions for Wave 1
    validation, not wiki facts.

## Round-Specific Mechanics Contract

| Mechanic / Trader Function / Field | Source | Decision | Bot Behavior | Validation Check |
| --- | --- | --- | --- | --- |
| `Trader.run()` | trader contract | implement | return orders, `0` conversions, string `traderData` | import/smoke test and tuple shape |
| `Trade.buyer` / `Trade.seller` | round 4 doc | exclude | control bots do not consume counterparty identity | confirm code ignores market-trade names |
| Voucher products | round 4 doc | exclude | no voucher orders in this pack | product-order audit |
| Manual challenge products | round 4 doc | exclude | no manual mechanics in uploadable bot | code contains no manual references |
| `bid()` | trader contract / round 4 doc | not applicable | do not implement round-2-only behavior | class still valid without round-2 logic |

## Linked-Product Framing Contract

- Product role: `delta-1`
- Signal class: `microstructure`
- Underlying role: `alpha` for `HYDRO`, `alpha and anchor` for `VEX`
- Trading posture: `passive | conditional`
- Natural hold horizon: `scalp / short hold`
- What makes this a trading leg instead of only a signal: direct top-of-book
  tradability and clean order-flow exposure.
- Rule that should prevent edge from turning into giveback: stay out in wide or
  thin books and bias back toward flat inventory quickly.

## Feature Contract

| Feature | Source Fields | Online Availability | Lifecycle Label | Role | Parameters | Multivariate Relationship | Process Assumption | Redundancy Decision | Missing-Signal Behavior | State / `traderData` Required | Validation / Invalidation Check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| delta-1 local edge | best bid/ask in `order_depths` | usable online | implementation candidate | direct signal | passive quote width `1`, cross edge `2`, max clip `12`, soft inventory band `80`, hard internal cap `120` | none needed | local best-book mispricing exists often enough to monetize | keep | stay idle if either side missing | none required; optional empty JSON string | compare PnL/path vs later overlay packs |
| spread gate | best ask minus best bid | usable online | implementation candidate | execution filter | normal mode when spread `<= 4`, reduced mode when spread `5-6`, disable above `6` | none needed | wide books worsen fills | keep | disable quoting on invalid spread | none | fill quality by spread bucket |
| top-book imbalance | top-level bid and ask sizes | usable online | implementation candidate | risk control | require imbalance magnitude `< 0.65` for normal quoting; otherwise reduce same-side clip by 50% | low-value support only | extreme top imbalance raises adverse-fill risk | keep | if depth missing, revert to spread-only mode | none | markout split by imbalance bucket |

## Feature Exclusions

| Feature | Why Excluded | Reopen Only If |
| --- | --- | --- |
| counterparty context | needed later, but would contaminate controls | control pack underperforms so badly it becomes uninformative |
| voucher overlays | controls must stay product-pure | later review decides controls can be dropped |
| family pressure / surface filters | no decision impact for the control objective | later runs show controls need support just to be interpretable |

## Signal / Fair Value Logic

- Signal: top-of-book local edge around the current midpoint.
- Inputs: best bid, best ask, top-level size, current position.
- Missing-signal behavior: stay idle if either side of the book is absent.
- Process assumption that would invalidate this logic: control products become
  too one-sided or too wide to represent clean baselines.
- Multivariate or redundancy caveat: do not add counterparty or option-book
  context here.

## Execution Logic

- Buy behavior: cross only when ask is at least `2` ticks below local fair
  anchor and buy capacity exists.
- Sell behavior: cross only when bid is at least `2` ticks above local fair
  anchor and sell capacity exists.
- Passive/resting order behavior: when spread is normal, place one-sided or
  two-sided passive quotes `1` tick from the local fair anchor with reduced
  size near soft inventory limits.
- Stay-idle behavior: missing book side, spread above `6`, no capacity, or
  extreme imbalance.

## Position And Risk Handling

- Position limits: exchange limit `200` per product.
- Aggregate buy capacity: `200 - current_position`.
- Aggregate sell capacity: `200 + current_position`.
- Inventory skew or reduction: cut same-side size after `|position| >= 80`,
  stop aggressive expansion after `|position| >= 120`, bias passive quotes
  toward flattening when beyond `40`.

## State And Runtime

- `traderData` use: optional empty JSON string; no persistent model needed.
- Imports: standard library only.
- Runtime risk: O(1) per product per iteration.
- Research-only dependencies excluded from uploadable bot: `yes`

## Expected Failure Cases

- Failure case: controls earn little because the true edge now lives entirely
  in overlays or veto logic.
- Mitigation or validation: judge them as controls, not only as standalone
  winners.
- Failure case: wide or unbalanced books create noisy passive fills.
- Mitigation or validation: inspect fill quality by spread and imbalance regime.

## Validation Plan

- Contract checks: correct tuple return, no unsupported methods, no manual
  logic, no voucher orders.
- Order sign and limit checks: positive buys, negative sells, per-product
  aggregate capacity under `200`.
- Performance/run checks: product-isolated PnL, path quality, inventory shape,
  fill count, and markout by spread bucket.
- Debug signals to inspect: mid, spread, imbalance, quote mode, position.
- Linked-product attribution checks, if applicable: not applicable.
- Giveback / retention checks, if applicable: confirm controls are not hiding
  late giveback via oversized passive inventory.

## Implementation Handoff

- Target bot paths:
  - `rounds/round_4/bots/noel/historical/r4_s01_vex_base_control.py`
  - `rounds/round_4/bots/noel/historical/r4_s02_hydro_base_control.py`
- Parameters to implement:
  - passive quote width `1`
  - cross edge `2`
  - spread disable `> 6`
  - max clip `12`
  - soft inventory band `80`
  - hard internal cap `120`
- Known caveats: do not add any counterparty or voucher context in this pack.
