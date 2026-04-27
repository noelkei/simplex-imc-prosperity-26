# Spec Pack F: Low-Priority Probes

## Review Status

- Status: `COMPLETED`
- Owner: Codex
- Reviewer: Human
- Reviewed on: 2026-04-27

## Candidate

- Candidate ID: `pack_f_low_priority_probes`
- Candidate priority tier: `validate-next`
- Evidence strength: `weak-medium`
- Product scope: upper vouchers and tiny pricing-support filters
- Linked candidate file: `../03_strategy_candidates.md`

## Pack Members

| Candidate | Product Scope | Role In Pack | Target Bot Path |
| --- | --- | --- | --- |
| `r4_s12_upper_passive_probe` | `VEV_5400/5500` | passive-only upper-loop closure test | `rounds/round_4/bots/noel/canonical/r4_s12_upper_passive_probe.py` |
| `r4_s14_surface_sanity_filter` | selective voucher overlays | tiny surface-sanity support test | `rounds/round_4/bots/noel/canonical/r4_s14_surface_sanity_filter.py` |

## Review Decision

- `_index.md` spec status: `approved`
- Approved for implementation: `yes`
- Reviewer decision notes: User requested moving directly into `Phase 05` for the exploratory Wave 1 implementation set. Treat this pack as approved with caveats for exploration only, not final submission.
- Required changes before coding: none; keep both branches tiny and easy to kill.

## Sources

- Wiki facts: Round 4 product scope/limits and trader contract.
- EDA evidence: upper/floor strikes are poor default inventory; pricing surface
  matters for framing but not yet for heavy live logic.
- Understanding summary: upper branch is low confidence, surface support is
  useful only if extremely compact.
- Post-run research memory: upper loop and broad baskets were anti-pattern-rich;
  surface ideas should stay support-only.
- Playbook heuristics: none as primary evidence.

## Carry-Forward Context

- Validated carry-forward principles used:
  - upper/floor strikes should not be default aggressive inventory
  - surface awareness is framing support, not primary alpha
- Untested hypotheses intentionally being tested:
  - there might be a tiny passive niche in the upper loop
  - a minimal surface sanity proxy might improve selectivity cheaply
- Anti-patterns explicitly avoided:
  - active upper aggression
  - full Heston/COS live machinery
  - treating surface residuals as direct alpha without guards

## Selection Trace

- Based on candidates: `r4_s12`, `r4_s14`
- Signals used: passive-only upper posture, local surface sanity proxy.
- Alternatives considered: more ambitious upper or pricing branches were
  rejected as too complex or too weak.
- Why selected: these are cheap closure probes that can either kill or rescue
  edge cases without much implementation burden.
- Known caveats: both candidates may legitimately do very little.
- Branch posture: `prune/reopen with new thesis`

## Evidence Traceability

- Linked EDA Signals: `upper_floor_exclusion`, `surface_awareness_not_flat_vol`.
- Feature Evidence: both ideas are weaker than the main packs and should be
  treated as probes.
- Metric Availability:
  - upper passive posture: fully online
  - surface sanity proxy: partially available online as a simple local check
- Baseline vs richer model verdict:
  - upper passive posture: `baseline only`
  - surface sanity proxy: `richer low ROI unless simple`
- Multivariate Evidence: surface proxy risks redundancy with spread and simple
  anchor context.
- Process / Distribution Assumptions:
  - some upper-loop prints may be monetizable only passively
  - noisy local kinks can be filtered without a heavy model
- Redundancy Decisions: `r4_s14` must remain a support filter, never a primary
  signal.
- Regime Assumptions: both branches should act only in narrow, observable
  states.
- Understanding Insight: neither branch deserves center-stage resources.
- Research tool evidence used, if any: `roos`, `bollen_whaley`, `fengler`.
- Evidence gaps or strategy assumptions:
  - both branches are allowed to fail cleanly and be retired.

## Round-Specific Mechanics Contract

| Mechanic / Trader Function / Field | Source | Decision | Bot Behavior | Validation Check |
| --- | --- | --- | --- | --- |
| `Trader.run()` | trader contract | implement | trade upper-loop or overlay-support logic only | smoke test and tuple shape |
| `Trade.buyer` / `Trade.seller` | round 4 doc | exclude | not needed for this pack | code audit |
| Upper vouchers `5400/5500` | round 4 doc | implement selectively | passive-only quoting if at all | product-order audit |
| Manual challenge products | round 4 doc | exclude | no manual logic in uploadable bot | code contains no manual references |
| `bid()` | trader contract / round 4 doc | not applicable | no round-2-only behavior | class validity check |

## Linked-Product Framing Contract

- Product role: `upper passive leg` and `support layer`
- Signal class: `microstructure | surface`
- Underlying role: `anchor`
- Trading posture: `passive | conditional`
- Natural hold horizon: `short hold | session state`
- What makes this a trading leg instead of only a signal: `r4_s12` tests
  whether upper quotes can earn anything passively; `r4_s14` changes whether
  other overlay entries are allowed.
- Rule that should prevent edge from turning into giveback: keep size tiny and
  disable immediately in bad spread or noisy surface states.

## Feature Contract

| Feature | Source Fields | Online Availability | Lifecycle Label | Role | Parameters | Multivariate Relationship | Process Assumption | Redundancy Decision | Missing-Signal Behavior | State / `traderData` Required | Validation / Invalidation Check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| passive upper quote posture | `5400/5500` best bid/ask, spread, top depth | usable online | implementation candidate | direct signal | quote only when spread `>= 6` and `<= 12`, clip `4`, soft band `20`, no crossing allowed | intentionally separate from active middle-strike logic | any upper-loop value should come from passive fills only | keep in `r4_s12` only | if book too thin or missing, stay idle | none | likely zero-fill outcome is acceptable |
| dominance avoidance | recent visible trade pressure and spread shock in upper loop | usable online | implementation candidate | execution filter | disable passive upper quoting for `2` steps after adverse trade/pressure event | small supporting layer | upper passive edge disappears in clearly toxic state | keep | if no recent trades, rely on spread/depth only | short timer only | compare quoted vs filled outcomes by regime |
| local surface sanity proxy | neighboring voucher mids or best quotes around target strike plus `VEX` anchor | usable online | implementation candidate | diagnostic / risk control | reject overlay entry when local neighboring quotes imply inconsistent kink larger than `3` ticks; never direct trigger | may overlap with spread or role filters | some residual-like entries are just local quote distortion | keep only in `r4_s14` | if neighbor quotes missing, do not apply the filter | none or tiny last-neighbor cache | compare filtered vs unfiltered overlay quality |

## Feature Exclusions

| Feature | Why Excluded | Reopen Only If |
| --- | --- | --- |
| active upper aggression | contradicted by current understanding | passive probe unexpectedly works well |
| full stochastic-volatility runtime | too heavy and unsupported | tiny local filter proves insufficient and review allows more complexity |
| direct residual alpha from pricing model | too easy to overread | validation shows simple sanity filter has real lift |

## Signal / Fair Value Logic

- Signal:
  - `r4_s12`: passive-only upper quote experiment
  - `r4_s14`: support-only surface sanity filter applied to other overlay logic
- Inputs: upper-loop books, neighboring quotes, `VEX` anchor, simple spread and
  depth state.
- Missing-signal behavior:
  - `r4_s12`: stay idle if book conditions are not clearly acceptable
  - `r4_s14`: if neighbors unavailable, do not apply the filter
- Process assumption that would invalidate this logic: any apparent upper-loop
  or surface benefit is too sparse or too noisy to survive validation.
- Multivariate or redundancy caveat: `r4_s14` must not duplicate Pack E or Pack
  D context filters.

## Execution Logic

- Buy behavior: `r4_s12` may only rest small passive buys; `r4_s14` does not
  create direct buys on its own.
- Sell behavior: same as above on the sell side.
- Passive/resting order behavior: central to `r4_s12`; tiny and cancellable.
- Stay-idle behavior: default for both branches unless narrow enabling
  conditions are met.

## Position And Risk Handling

- Position limits: any voucher used directly remains under exchange limit `300`.
- Aggregate buy capacity: `300 - current_position`.
- Aggregate sell capacity: `300 + current_position`.
- Inventory skew or reduction: internal cap `20` for upper passive probe; do
  not average into upper-loop positions.

## State And Runtime

- `traderData` use: optional small timers only.
- Imports: standard library only.
- Runtime risk: extremely low.
- Research-only dependencies excluded from uploadable bot: `yes`

## Expected Failure Cases

- Failure case: `r4_s12` gets no fills or only toxic fills.
- Mitigation or validation: treat that as useful closure evidence and prune.
- Failure case: `r4_s14` filters almost nothing or filters good trades too.
- Mitigation or validation: inspect entry reduction and net path improvement.

## Validation Plan

- Contract checks: no unsupported products or manual mechanics; no active upper
  crossing in `r4_s12`.
- Order sign and limit checks: small passive clip only, no product-limit
  breaches.
- Performance/run checks: fill count, markout, path quality, and whether the
  branch deserves to survive at all.
- Debug signals to inspect: upper spread, depth, passive quote presence,
  dominance timer, surface-kink filter state.
- Linked-product attribution checks, if applicable: for `r4_s14`, inspect
  whether the filter improved the parent overlay rather than merely reducing
  trades.
- Giveback / retention checks, if applicable: minor only.

## Implementation Handoff

- Target bot paths:
  - `rounds/round_4/bots/noel/canonical/r4_s12_upper_passive_probe.py`
  - `rounds/round_4/bots/noel/canonical/r4_s14_surface_sanity_filter.py`
- Parameters to implement:
  - upper spread window `6-12`
  - passive clip `4`
  - internal upper cap `20`
  - upper adverse-state timer `2`
  - local kink reject threshold `3`
- Known caveats: these branches are allowed to prove that they should not
  survive; do not embellish them if their first signal is weak.
