# Spec Pack D: Counterparty Defensive

## Review Status

- Status: `COMPLETED`
- Owner: Codex
- Reviewer: Human
- Reviewed on: 2026-04-27

## Candidate

- Candidate ID: `pack_d_counterparty_defensive`
- Candidate priority tier: `spec-first`
- Evidence strength: `medium-high`
- Product scope: `VEX` anchor, contextual voucher family with focus on `5200+`
- Linked candidate file: `../03_strategy_candidates.md`

## Pack Members

| Candidate | Product Scope | Role In Pack | Target Bot Path |
| --- | --- | --- | --- |
| `r4_s05_mark22_veto_gate` | `VEX` plus `5200+` context | explicit `Mark 22` danger veto | `rounds/round_4/bots/noel/historical/r4_s05_mark22_veto_gate.py` |
| `r4_s06_counterparty_concentration_gate` | selective voucher family context | concentration-state filter | `rounds/round_4/bots/noel/historical/r4_s06_counterparty_concentration_gate.py` |
| `r4_s10_5200_signal_only_veto` | family context only | `5200` as signal-only monitor | `rounds/round_4/bots/noel/historical/r4_s10_5200_signal_only_veto.py` |

## Review Decision

- `_index.md` spec status: `approved`
- Approved for implementation: `yes`
- Reviewer decision notes: User requested moving directly into `Phase 05` for the exploratory Wave 1 implementation set. Treat this pack as approved with caveats for exploration only, not final submission.
- Required changes before coding: none; preserve context-first logic and avoid slipping into raw-name alpha.

## Sources

- Wiki facts: Round 4 counterparty identities are exposed in trade data.
- EDA evidence: `Mark 22` seller-side danger-state in `5200+`, concentration
  and trade-location context, engineered context beating raw names.
- Understanding summary: counterparties matter as context, not as direct alpha.
- Post-run research memory: `5200` looked more like anti-signal than inventory
  already in `round_3`.
- Playbook heuristics: none as primary evidence.

## Carry-Forward Context

- Validated carry-forward principles used:
  - counterparties are context first
  - `5100/5200` are better starting points for veto ideas than inventory ideas
- Untested hypotheses intentionally being tested:
  - `Mark 22` seller flow is a genuine danger-state veto
  - concentration state is more robust than raw identities
  - `5200` is useful as signal-only monitor
- Anti-patterns explicitly avoided:
  - raw-name alpha bots
  - direct `5200` inventory
  - pair-recurrence triggers

## Selection Trace

- Based on candidates: `r4_s05`, `r4_s06`, `r4_s10`
- Signals used: `Mark 22` seller state, concentration/dominance state, `5200`
  signal-only monitor, spread/depth deterioration.
- Alternatives considered: execution overlay lives in Pack E; old-winner
  revalidation lives in Pack B.
- Why selected: this pack isolates the highest-ROI direct novelty in `round_4`
  without forcing it to masquerade as stand-alone alpha.
- Known caveats: counterparty effects may partly reflect product-selection
  effects rather than unique participant information.
- Branch posture: `coverage gap`

## Evidence Traceability

- Linked EDA Signals: `mark22_seller_danger_state`,
  `counterparty_concentration_context`, `engineered_context_over_raw_names`,
  `5200` signal-only framing.
- Feature Evidence: model ladder favored engineered context over raw names.
- Metric Availability: all chosen inputs are online-observable from
  `market_trades`, order books, and positions.
- Baseline vs richer model verdict: `richer adds value` only if defensive gates
  improve path quality over simple anchor baselines.
- Multivariate Evidence: identity-only features are weak; grouped context is
  more defensible.
- Process / Distribution Assumptions:
  - visible participant state is locally persistent enough to gate decisions
  - `5200+` adverse states are observable before they fully contaminate fills
- Redundancy Decisions: `Mark 22` veto, concentration gate, and `5200`
  monitor must remain distinct hypotheses.
- Regime Assumptions: participant-conditioned states cluster over short local
  windows, not just single trades.
- Understanding Insight: treat counterparty information as state, not thesis.
- Research tool evidence used, if any: `doshi`, `vasios`,
  `goncalves_pinto_sala`, `nimalendran_son`.
- Evidence gaps or strategy assumptions:
  - the exact short-window threshold for "danger-state" remains a strategy
    assumption for Wave 1.

## Round-Specific Mechanics Contract

| Mechanic / Trader Function / Field | Source | Decision | Bot Behavior | Validation Check |
| --- | --- | --- | --- | --- |
| `Trader.run()` | trader contract | implement | trade `VEX` plus contextual reads from voucher family | smoke test and tuple shape |
| `Trade.buyer` / `Trade.seller` | round 4 doc | implement | use only in rolling contextual filters | validate names influence gates, not direct prices |
| `VEV_5200` | round 4 doc | implement as context only | never open direct `5200` inventory in this pack | product-order audit |
| Manual challenge products | round 4 doc | exclude | no manual logic in uploadable bot | code contains no manual references |
| `bid()` | trader contract / round 4 doc | not applicable | no round-2-only behavior | class validity check |

## Linked-Product Framing Contract

- Product role: `monitor / veto`
- Signal class: `regime | microstructure`
- Underlying role: `anchor`
- Trading posture: `no-trade | conditional`
- Natural hold horizon: `session state`
- What makes this a trading leg instead of only a signal: `r4_s05` and
  `r4_s06` still trade the anchor or selective overlays, but only when the
  contextual state permits it.
- Rule that should prevent edge from turning into giveback: hard-disable new
  risk when the short-horizon participant state becomes adverse.

## Feature Contract

| Feature | Source Fields | Online Availability | Lifecycle Label | Role | Parameters | Multivariate Relationship | Process Assumption | Redundancy Decision | Missing-Signal Behavior | State / `traderData` Required | Validation / Invalidation Check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `Mark 22` seller state | `market_trades` buyer/seller, symbol, quantity | usable online | implementation candidate | risk control | activate on seller-dominant `Mark 22` flow in `5200+` over rolling `3` trade events or `2` decision steps; veto lasts `3` steps | raw identity is weak alone, so this feature always stays contextual | `Mark 22` state is locally persistent enough to matter | keep only in `r4_s05` | if trade tape missing, feature disables cleanly | rolling counts and veto timer | compare anchor path quality during active vs inactive state |
| concentration / dominance state | recent trade counts by counterparty and symbol | usable online | implementation candidate | execution filter | concentration `high` if top participant share `>= 50%` in short window; reduce size 50% or disable overlay entries | partially overlaps with `Mark 22` state but more general | concentration is more stable than single-name logic | keep only in `r4_s06` | if no recent trades, fall back to no concentration gate | rolling per-symbol counts | compare to `r4_s05` and base controls |
| `5200` signal-only monitor | `VEV_5200` trade presence, spread, contextual flow state | usable online | implementation candidate | diagnostic / risk control | if `5200` is active in bad state, disable family expansion for `2` steps; never trade `5200` directly | complements broader danger-state logic | `5200` mostly carries warning information | keep only in `r4_s10` | if `5200` absent, feature is neutral | 2-step timer | measure whether the veto improves other-leg path quality |
| spread/depth deterioration | top-of-book spread and depth in relevant products | usable online | implementation candidate | execution filter | reduce size in spread `> 6`, disable in spread `> 10`, require non-empty top depth | orthogonal support layer | adverse participant states and bad books often co-occur | keep | if book invalid, stay idle | none | fill-quality split by combined danger-state regime |

## Feature Exclusions

| Feature | Why Excluded | Reopen Only If |
| --- | --- | --- |
| raw-name directional alpha | contradicted by current evidence | later runs show strong incremental edge beyond contextual use |
| pair-recurrence triggers | too sample-sensitive | run evidence shows repeatable gain beyond simpler states |
| direct `5200` trading | current best thesis is monitor-only | `r4_s10` fails while direct `5200` evidence appears elsewhere |

## Signal / Fair Value Logic

- Signal:
  - `r4_s05`: hard danger veto from `Mark 22` seller state
  - `r4_s06`: softer concentration/dominance state filter
  - `r4_s10`: `5200`-driven signal-only veto
- Inputs: market-trade participant fields, relevant voucher symbols, order-book
  spread/depth, anchor product state.
- Missing-signal behavior: if trade tape is silent or sparse, these features
  revert to neutral rather than hallucinating state.
- Process assumption that would invalidate this logic: counterparty state is too
  unstable or fully explained by product choice alone.
- Multivariate or redundancy caveat: do not combine all three gates into one bot
  before isolated validation.

## Execution Logic

- Buy behavior: buy the anchor or paired leg only when the pack's contextual
  state is neutral.
- Sell behavior: symmetric to buy behavior.
- Passive/resting order behavior: passive quoting allowed only when the
  contextual state is neutral and book quality is acceptable.
- Stay-idle behavior: hard danger veto active, concentration too high, `5200`
  warning active, or books too poor.

## Position And Risk Handling

- Position limits:
  - `VEX`: `200`
  - any direct voucher used outside `5200`: `300`
- Aggregate buy capacity: exchange limit minus current position.
- Aggregate sell capacity: exchange limit plus current position.
- Inventory skew or reduction: these bots should be more conservative than the
  plain controls; cut new risk fast when danger-state activates.

## State And Runtime

- `traderData` use: rolling counterparty counts, short timers, and last known
  danger-state labels.
- Imports: standard library only.
- Runtime risk: modest but still lightweight; small rolling dictionaries only.
- Research-only dependencies excluded from uploadable bot: `yes`

## Expected Failure Cases

- Failure case: the contextual gates simply reduce trading without improving
  path quality.
- Mitigation or validation: compare against plain controls and overlay packs.
- Failure case: one participant appears predictive only because they dominate a
  structurally bad strike.
- Mitigation or validation: inspect by-symbol attribution and not just top-line
  PnL.

## Validation Plan

- Contract checks: no direct `5200` orders; trade-tape use must be defensive.
- Order sign and limit checks: positive buys, negative sells, no product limit
  breach.
- Performance/run checks: path quality under active danger-state, missed-trade
  cost, PnL by contextual regime, and by-product attribution.
- Debug signals to inspect: `Mark 22` counts, concentration state, `5200`
  monitor flag, spread/depth regime, veto timers.
- Linked-product attribution checks, if applicable: confirm contextual gates are
  improving anchor or overlay quality rather than merely shutting the bot off.
- Giveback / retention checks, if applicable: confirm veto logic reduces bad
  entries or giveback windows.

## Implementation Handoff

- Target bot paths:
  - `rounds/round_4/bots/noel/historical/r4_s05_mark22_veto_gate.py`
  - `rounds/round_4/bots/noel/historical/r4_s06_counterparty_concentration_gate.py`
  - `rounds/round_4/bots/noel/historical/r4_s10_5200_signal_only_veto.py`
- Parameters to implement:
  - danger-state timer `3`
  - concentration high threshold `50%`
  - `5200` veto timer `2`
  - spread reduce `> 6`
  - spread disable `> 10`
- Known caveats: if these gates only reduce activity but not bad-path exposure,
  they should be downgraded quickly rather than embellished.
