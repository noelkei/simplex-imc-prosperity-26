# Spec Pack J: 4000 Activation And Execution

## Review Status

- Status: `COMPLETED`
- Owner: Codex
- Reviewer: Human
- Reviewed on: 2026-04-27

## Candidate

- Candidate ID: `pack_j_4000_activation_and_execution`
- Candidate priority tier: `spec-first`
- Evidence strength: `medium-high`
- Product scope: `VELVETFRUIT_EXTRACT`, `VEV_4000`, light contextual tape checks
- Linked candidate file: `../03_strategy_candidates.md`

## Pack Members

| Candidate | Product Scope | Role In Pack | Target Bot Path |
| --- | --- | --- | --- |
| `r4_w2_13_4000_forced_activation` | `VEX + VEV_4000` | honest activation baseline | `rounds/round_4/bots/noel/canonical/r4_w2_13_4000_forced_activation.py` |
| `r4_w2_14_4000_benign_tape_only` | `VEX + VEV_4000` | one-filter contextual follow-up | `rounds/round_4/bots/noel/canonical/r4_w2_14_4000_benign_tape_only.py` |
| `r4_w2_15_4000_quote_ladder_probe` | `VEX + VEV_4000` | winner-style adapted execution probe | `rounds/round_4/bots/noel/canonical/r4_w2_15_4000_quote_ladder_probe.py` |

## Review Decision

- `_index.md` spec status: `approved`
- Approved for implementation: `yes`
- Reviewer decision notes: User explicitly requested implementing all `15`
  Wave 2 bots and entering `Phase 05`. Treat that instruction as operational
  approval for exploratory implementation with validation caveats, including
  the deliberately permissive `4000` activation baseline.
- Required changes before coding: none

## Sources

- Wiki facts: Round 4 product scope, limits, and trade fields.
- EDA evidence:
  - `4000` remains a plausible structural overlay
  - `VEX` is the proper anchor
  - surface-aware framing supports simple valuation, not heavy complexity
- Understanding summary:
  - `4000` belongs in low-complexity overlay space
- Post-run research memory:
  - `r4_w1_i02_4000_untested`
  - anti-pattern against claiming overlay success when no overlay inventory
    traded
- Uploaded winner references:
  - `../research/big_volcano_man_fixed.py`
  - `../research/algo run for round 4.py`
- Processed paper references:
  - `../research/papers_processed/carry_forward/choi_2022_bachelier_guide_processed.md`
  - `../research/papers_processed/vasios_2015_mimicking_non_anonymous_processed.md`

## Carry-Forward Context

- Validated carry-forward principles used:
  - `VEX` is the anchor
  - `4000` is unresolved, not disproven
- Untested hypotheses intentionally being tested:
  - `4000` can still add value if direct activation is forced
  - `4000` may be execution-limited rather than no-edge
  - a single benign-tape filter may help only after activation is proven
- Anti-patterns explicitly avoided:
  - another composite old-winner retest
  - whole-bot contextual veto
  - pretending to test `4000` while only trading `VEX`

## Selection Trace

- Based on candidates: `r4_w2_13`, `r4_w2_14`, `r4_w2_15`
- Signals used:
  - Wave 1 Pack `B` attribution failure
  - `4000` structural overlay framing from understanding
  - winner-style strike-specific quote ladder adaptation
- Alternatives considered:
  - abandoning `4000`
  - reusing the old composite winner stack
  - adding multiple context filters before first proving activation
- Why selected: this pack is required before any honest judgment on `4000`.
- Known caveats:
  - permissive activation may expose low-quality `4000` flow
  - winner-style quote ladder may teach execution quality but not edge quality
- Branch posture: `coverage gap`

## Evidence Traceability

- Linked EDA Signals:
  - `VEX_anchor_same_time`
  - `option_book_role_split`
  - `surface_awareness_not_flat_vol`
- Feature Evidence:
  - Pack `B` never generated direct `4000` inventory
  - `4000` still fits the ITM structural overlay story
- Metric Availability:
  - all direct features are online-usable
  - rolling IV and fair value are online-computable
- Baseline vs richer model verdict:
  - a simple fair-value ladder is justified
  - full old winner composite is not
- Multivariate Evidence:
  - `4000` activation must be separated from contextual filters
- Process / Distribution Assumptions:
  - the main question is activation and execution, not yet optimized retention
- Redundancy Decisions:
  - forced activation, benign tape, and quote ladder must remain separate axes
- Regime Assumptions:
  - a direct `4000` trade opportunity should appear if thresholds are simple
    enough
- Understanding Insight:
  - `4000` should remain a low-complexity overlay, not a full family
- Research tool evidence used, if any:
  - `choi_2022` for simple pricing backbone
  - uploaded winner code for strike-level quote ladder structure
- Evidence gaps or strategy assumptions:
  - activation threshold and quote-ladder width are strategy assumptions

## Round-Specific Mechanics Contract

| Mechanic / Trader Function / Field | Source | Decision | Bot Behavior | Validation Check |
| --- | --- | --- | --- | --- |
| `Trader.run()` | trader contract | implement | trade `VEX` and `VEV_4000` only | smoke test and tuple shape |
| `Trade.buyer` / `Trade.seller` | round 4 doc | implement selectively | `r4_w2_14` may use a light benign-tape filter only | inspect direct `4000` activation still survives |
| rolling IV / delta calculation | current round books | implement | use small online fair-value calculator where needed | log valid-window count |
| explicit underlying delta hedge | uploaded winner code | exclude | keep `4000` attribution clean | confirm no hedge-only orders |
| Manual challenge products | round 4 doc | exclude | no manual logic | code contains no manual references |

## Linked-Product Framing Contract

- Product role: `ITM structural overlay`
- Signal class: `valuation | microstructure`
- Underlying role: `anchor`
- Trading posture: `conditional`
- Natural hold horizon: `short / medium hold`
- What makes this a trading leg instead of only a signal: `4000` should carry
  direct inventory when the overlay is truly active.
- Rule that should prevent edge from turning into giveback: keep the first pass
  simple and visible; only the benign-tape branch adds one filter.

## Feature Contract

| Feature | Source Fields | Online Availability | Lifecycle Label | Role | Parameters | Multivariate Relationship | Process Assumption | Redundancy Decision | Missing-Signal Behavior | State / `traderData` Required | Validation / Invalidation Check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| forced `4000` activation core | `VEX` mid, `4000` best bid/ask, current positions | usable online | implementation candidate | direct signal | allow `4000` branch whenever spread `<= 10`, fair edge `>= 1`, and parent `VEX` anchor valid; max clip `15`, soft band `90` | intentionally simpler than Pack `B` | a valid `4000` opportunity exists if thresholds are not over-filtered | keep in all three bots as the shared baseline | missing `4000` book disables overlay; `VEX` may still trade if parent branch is allowed | optional last valid fair estimate | direct `VEV_4000` inventory or quote intent must appear in validation |
| simple `4000` fair-value ladder | `VEX` mid, `4000` best bid/ask, timestamp | usable online | implementation candidate | direct signal | compute current `4000` implied vol and keep rolling IV window `10`, min valid obs `5`; quote one level around rolling-IV fair value with intrinsic floor | shared valuation layer | `4000` benefits from strike-specific fair value even if full old winner logic does not transfer | keep, but keep small | if rolling IV invalid, use recent-mid approximation or stay idle | rolling IV window, last valid fair value | fair-value estimates remain stable enough to place quotes |
| winner-style quote ladder and queue takeover | `4000` best bid/ask, fair band, top depth | usable online | implementation candidate | execution filter | if fair bid beats best ask by `>= 1`, buy then repost; symmetric on sell side; ladder width `1`; do not exceed clip `12` on takeover | separate from simple activation | `4000` may be execution-limited and benefit from the winner trade style | keep only in `r4_w2_15` | missing fair value disables this feature only | last quote side, last band | direct `4000` engagement improves vs `r4_w2_13` |
| benign-tape-only filter | recent `4000` and `VEX` trade-location, `VEX` spread, optional recent adverse seller warning | usable online | implementation candidate | execution filter | require clean `VEX` spread `<= 1` and no immediate adverse tape marker before new `4000` entries; exits still allowed | kept separate from activation baseline | a single clean-state filter may help without repeating Pack `B` over-filtering | keep only in `r4_w2_14` | missing tape state removes only the filter | short recent-tape cache | direct `4000` activation still survives after filtering |
| option delta diagnostic | rolling IV estimate, `VEX` mid, strike `4000`, timestamp | usable online | log-only diagnostic | diagnostic | compute delta for logging and optional size sanity only; no direct hedge | diagnostic only | delta size may explain when `4000` behaves like structure vs direct alpha | downgraded | if invalid, ignore | last valid delta | helps distinguish inventory-limited from no-edge |

## Feature Exclusions

| Feature | Why Excluded | Reopen Only If |
| --- | --- | --- |
| composite old winner stack | Wave 1 showed it answered nothing | direct `4000` activation is proven first |
| hard counterparty veto | Wave 1 over-suppressed similar structures | a lighter one-filter overlay still fails |
| full hedge engine from old winner bot | wrong question for attribution-first `4000` pack | direct `4000` edge is proven and attribution needs extension |
| multi-strike family logic | would contaminate the clean `4000` test | `4000` alone shows real life |

## Signal / Fair Value Logic

- Signal:
  - `r4_w2_13`: shared direct `4000` activation baseline
  - `r4_w2_14`: same baseline plus one benign-tape filter
  - `r4_w2_15`: same baseline plus winner-style quote ladder
- Inputs: `VEX` and `4000` books, timestamp, optional recent `4000` or `VEX`
  tape state.
- Missing-signal behavior:
  - missing `VEX` or `4000` book disables the overlay
  - invalid fair-value window triggers fallback to recent-mid approximation or
    no trade
  - missing benign-tape context disables only the filter
- Process assumption that would invalidate this logic: `4000` still fails to
  activate or still produces zero attributable value even under permissive
  thresholds.
- Multivariate or redundancy caveat: do not compare `r4_w2_14` before first
  proving that `r4_w2_13` actually trades `4000`.

## Execution Logic

- Buy behavior: allow direct `4000` orders when the activation core is live;
  `r4_w2_15` may cross obvious mispricing first.
- Sell behavior: symmetric to buy behavior.
- Passive/resting order behavior: rest around fair value when not crossing.
- Stay-idle behavior:
  - invalid `4000` book
  - invalid fair-value state
  - branch-specific benign-tape filter active
  - no capacity
- No-trade / disable conditions:
  - `4000` spread above `10`
  - missing anchor

## Position And Risk Handling

- Position limits:
  - `VEX`: `200`
  - `VEV_4000`: `300`
- Aggregate buy capacity:
  - `VEX`: `200 - current_position`
  - `VEV_4000`: `300 - current_position`
- Aggregate sell capacity:
  - `VEX`: `200 + current_position`
  - `VEV_4000`: `300 + current_position`
- Inventory skew or reduction:
  - `4000` soft band `90`
  - direct `4000` max clip `15`
  - queue-takeover branch uses `12` as maximum aggressive take clip

## State And Runtime

- `traderData` use:
  - rolling IV window
  - last valid fair estimate
  - optional benign-tape cache
  - optional delta diagnostic
- Imports: standard library plus `math`
- Runtime risk: medium
- Research-only dependencies excluded from uploadable bot: `yes`

## Expected Failure Cases

- Failure case: even the permissive activation branch still trades no `4000`.
- Mitigation or validation: treat that as high-signal failure and route back to
  EDA or product-priority pruning.
- Failure case: quote ladder creates fills but no meaningful edge.
- Mitigation or validation: classify as `execution teaches mechanics, not edge`
  and avoid over-promoting.
- Failure case: the benign-tape filter repeats Pack `B` over-suppression.
- Mitigation or validation: log whether direct `4000` activation survives.

## Validation Plan

- Contract checks: only `VEX` and `4000` may trade.
- Order sign and limit checks: positive buys, negative sells, no limit breach.
- Performance/run checks:
  - direct `4000` trade count
  - direct `4000` PnL attribution
  - quote-intent visibility when no fills occur
  - comparison between activation baseline and quote ladder
- Debug signals to inspect:
  - activation gate
  - fair value
  - rolling IV count
  - queue-takeover trigger
  - benign-tape filter reason
- Linked-product attribution checks, if applicable:
  - separate `VEX` path changes from direct `4000` contribution
- Giveback / retention checks, if applicable:
  - secondary only; first objective is honest activation

## Implementation Handoff

- Target bot paths:
  - `rounds/round_4/bots/noel/canonical/r4_w2_13_4000_forced_activation.py`
  - `rounds/round_4/bots/noel/canonical/r4_w2_14_4000_benign_tape_only.py`
  - `rounds/round_4/bots/noel/canonical/r4_w2_15_4000_quote_ladder_probe.py`
- Parameters to implement:
  - `4000` spread cap `10`
  - activation edge `1`
  - IV window `10`
  - min valid IV obs `5`
  - soft band `90`
  - clip `15`
  - queue-takeover clip `12`
  - ladder width `1`
- Known caveats:
  - this pack is intentionally permissive because honesty of attribution comes
    before refinement
  - if `4000` still does not engage, that itself is a valuable decision
