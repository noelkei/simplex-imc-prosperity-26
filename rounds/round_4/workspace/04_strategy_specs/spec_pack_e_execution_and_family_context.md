# Spec Pack E: Execution And Family Context

## Review Status

- Status: `COMPLETED`
- Owner: Codex
- Reviewer: Human
- Reviewed on: 2026-04-27

## Candidate

- Candidate ID: `pack_e_execution_and_family_context`
- Candidate priority tier: `implement-first`
- Evidence strength: `medium`
- Product scope: `VEX` anchor plus selective voucher-family context
- Linked candidate file: `../03_strategy_candidates.md`

## Pack Members

| Candidate | Product Scope | Role In Pack | Target Bot Path |
| --- | --- | --- | --- |
| `r4_s07_trade_to_book_execution_overlay` | `VEX` plus selective vouchers | book-state execution overlay | `rounds/round_4/bots/noel/canonical/r4_s07_trade_to_book_execution_overlay.py` |
| `r4_s08_family_pressure_overlay` | voucher family plus `VEX` | family-state context overlay | `rounds/round_4/bots/noel/canonical/r4_s08_family_pressure_overlay.py` |

## Review Decision

- `_index.md` spec status: `approved`
- Approved for implementation: `yes`
- Reviewer decision notes: User requested moving directly into `Phase 05` for the exploratory Wave 1 implementation set. Treat this pack as approved with caveats for exploration only, not final submission.
- Required changes before coding: none; keep the family proxy simple and online-usable.

## Sources

- Wiki facts: Round 4 product scope/limits and trader contract.
- EDA evidence: trade-location bucket, book-state overlays, family-level
  context, cross-strike linkage.
- Understanding summary: linked-book framing matters, but not every family idea
  is implementation-worthy yet.
- Post-run research memory: family imbalance was unresolved but promising.
- Playbook heuristics: none as primary evidence.

## Carry-Forward Context

- Validated carry-forward principles used:
  - linked-product thinking matters more than isolated-symbol thinking
  - execution quality can matter as much as direct signal logic
- Untested hypotheses intentionally being tested:
  - trade-to-book context improves execution quality
  - family-pressure context adds value beyond symbol-local state
- Anti-patterns explicitly avoided:
  - complex latent-state or heavy offline regime models
  - converting paper framing directly into large runtime machinery

## Selection Trace

- Based on candidates: `r4_s07`, `r4_s08`
- Signals used: trade-location/book-state context, family pressure / imbalance
  proxy.
- Alternatives considered: danger-state and old-winner tests were prioritized
  into earlier packs because they are cleaner and higher ROI.
- Why selected: this pack covers two broad but still important context ideas
  that could either improve many later bots or prove not worth the complexity.
- Known caveats: family pressure is only partially available online and must be
  kept simple.
- Branch posture: `coverage gap`

## Evidence Traceability

- Linked EDA Signals: `trade_location_context`, linked-book family structure,
  cross-strike agreement/disagreement framing.
- Feature Evidence: execution overlays were one of the strongest practical
  paper-aligned themes; family pressure remained promising but unresolved.
- Metric Availability: trade-location is implemented; family pressure is
  partially available via simple proxy only.
- Baseline vs richer model verdict:
  - trade-to-book overlay: `richer adds value`
  - family pressure overlay: `not checked`
- Multivariate Evidence: family-level features risk redundancy if they simply
  mirror spread or counterparty state.
- Process / Distribution Assumptions:
  - bad trade-to-book states damage fills
  - linked-book pressure matters enough to justify a simple proxy
- Redundancy Decisions: family-pressure proxy must not duplicate counterparty
  concentration logic already isolated in Pack D.
- Regime Assumptions: family-state changes slowly enough to be used as a gating
  context rather than tick-level trigger.
- Understanding Insight: execution overlays should be tested before more complex
  pricing ideas.
- Research tool evidence used, if any: `cartea`, `doshi`, `kaeck`,
  `garleanu`, `bergault`.
- Evidence gaps or strategy assumptions:
  - family-pressure proxy must be intentionally simple and may fail cleanly.

## Round-Specific Mechanics Contract

| Mechanic / Trader Function / Field | Source | Decision | Bot Behavior | Validation Check |
| --- | --- | --- | --- | --- |
| `Trader.run()` | trader contract | implement | trade `VEX` and selective overlays only | smoke test and tuple shape |
| `Trade.buyer` / `Trade.seller` | round 4 doc | implement sparingly | can assist context, but not as primary signal in this pack | verify family proxy does not depend on raw-name alpha |
| Voucher-family linkage | round 4 doc + EDA | implement | use neighboring strikes only as context, not indiscriminate inventory | product-order audit |
| Manual challenge products | round 4 doc | exclude | no manual logic in uploadable bot | code contains no manual references |
| `bid()` | trader contract / round 4 doc | not applicable | no round-2-only behavior | class validity check |

## Linked-Product Framing Contract

- Product role: `execution overlay` and `family context`
- Signal class: `microstructure | regime`
- Underlying role: `anchor`
- Trading posture: `conditional`
- Natural hold horizon: `short hold | session state`
- What makes this a trading leg instead of only a signal: both branches are
  intended to change whether and how the bot takes anchor-plus-overlay risk.
- Rule that should prevent edge from turning into giveback: do less in bad
  trade-to-book states and under adverse family-state pressure.

## Feature Contract

| Feature | Source Fields | Online Availability | Lifecycle Label | Role | Parameters | Multivariate Relationship | Process Assumption | Redundancy Decision | Missing-Signal Behavior | State / `traderData` Required | Validation / Invalidation Check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trade-location bucket | last market-trade price vs local best bid/ask, current spread | usable online | implementation candidate | execution filter | classify as favorable / neutral / adverse; disable aggressive expansion for `1` step after adverse bucket | mostly orthogonal to anchor edge | where a trade prints in the book says something about local fill quality | keep in `r4_s07` | if last trade unavailable, revert to spread-only gating | one-step recent bucket | compare fill quality vs plain anchor |
| book-state gate | spread, top depth, imbalance | usable online | implementation candidate | execution filter | normal mode spread `<= 4`, reduced mode `5-6`, disable `> 6`; require non-empty depth | overlaps with Pack A spread gate but richer here | execution quality varies materially with immediate book state | keep in `r4_s07` | if one component missing, use available sub-gates conservatively | none | compare to Pack A and Pack B bots |
| family-pressure proxy | signed flow / active-trade share across voucher family, simple cross-strike concentration | usable online | implementation candidate | regime feature | low / medium / high family pressure state from rolling last `5` relevant trade events; only gate, never direct trigger | may overlap with Pack D concentration logic | linked-book stress can be approximated with a compact proxy | keep in `r4_s08` only if simple | if proxy unavailable, disable family gate and log | rolling per-family counters | compare `r4_s08` against control families |
| `VEX` anchor dependency | `VEX` edge plus overlay candidate state | usable online | implementation candidate | direct signal | no overlay action unless `VEX` anchor itself is neutral-to-positive | non-redundant core anchor dependency | context overlays should sit on top of a valid base | keep in both pack members | if anchor invalid, stay idle | optional anchor state | attribution split: anchor vs contextual lift |

## Feature Exclusions

| Feature | Why Excluded | Reopen Only If |
| --- | --- | --- |
| full family exposure model | too complex for first pack | simple family proxy clearly helps |
| raw-name participant features | tested more cleanly in Pack D | Pack D fails but context still looks promising |
| pricing-surface filters | belong in Pack F | Pack F shows strong lift with tiny proxy |

## Signal / Fair Value Logic

- Signal:
  - `r4_s07`: use trade-to-book and book state to control how the anchor/overlay
    takes risk
  - `r4_s08`: use family-pressure state as a simple regime gate
- Inputs: current book, recent market-trade print location, rolling family
  activity counters, anchor edge.
- Missing-signal behavior: if contextual features are absent, revert to simpler
  anchor behavior rather than invent state.
- Process assumption that would invalidate this logic: these context features
  are merely descriptive and do not improve decisions.
- Multivariate or redundancy caveat: Pack E must stay distinct from Pack D and
  not become "all context at once."

## Execution Logic

- Buy behavior: buy only when anchor edge is valid and contextual state is
  neutral/favorable.
- Sell behavior: symmetric to buy behavior.
- Passive/resting order behavior: most of the value in `r4_s07` should come
  from changing execution quality, not inventing new signals.
- Stay-idle behavior: adverse trade-location bucket, bad book state, high
  family-pressure state, or no anchor edge.

## Position And Risk Handling

- Position limits: `VEX` `200`; selective voucher overlays `300`.
- Aggregate buy capacity: exchange limit minus current position.
- Aggregate sell capacity: exchange limit plus current position.
- Inventory skew or reduction: Pack E should reduce risk earlier than the pure
  controls because its edge is contextual rather than core.

## State And Runtime

- `traderData` use: small recent-state blob for last trade-location bucket and
  rolling family counters.
- Imports: standard library only.
- Runtime risk: low to moderate; still simple enough for uploadable bot.
- Research-only dependencies excluded from uploadable bot: `yes`

## Expected Failure Cases

- Failure case: contextual layers do not improve anything beyond the plain base.
- Mitigation or validation: downgrade quickly and keep as validation-only ideas.
- Failure case: family-pressure proxy is too weak or too redundant.
- Mitigation or validation: inspect whether it adds anything beyond spread and
  counterparty concentration.

## Validation Plan

- Contract checks: no unsupported products or manual mechanics.
- Order sign and limit checks: positive buys, negative sells, no product-limit
  breaches.
- Performance/run checks: compare fill quality, hit rate, and path quality
  against Pack A/B baselines; inspect contextual regime segmentation.
- Debug signals to inspect: trade-location bucket, book-state regime,
  family-pressure state, anchor edge, positions.
- Linked-product attribution checks, if applicable: confirm family-state gates
  improve overlay selection rather than just shutting down trading.
- Giveback / retention checks, if applicable: secondary only; primary objective
  is execution quality.

## Implementation Handoff

- Target bot paths:
  - `rounds/round_4/bots/noel/canonical/r4_s07_trade_to_book_execution_overlay.py`
  - `rounds/round_4/bots/noel/canonical/r4_s08_family_pressure_overlay.py`
- Parameters to implement:
  - adverse trade-location cooldown `1`
  - book-state disable spread `> 6`
  - family-pressure rolling window `5`
  - family-pressure states `low / medium / high`
- Known caveats: do not let Pack E absorb Pack D's counterparty thesis or Pack
  F's pricing-support thesis.
