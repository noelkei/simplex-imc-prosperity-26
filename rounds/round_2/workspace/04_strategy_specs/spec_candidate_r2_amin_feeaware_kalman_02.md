# Round 2 Strategy Spec - Amin Fee-Aware Kalman Market Making

## Review Status

- Status: `DEFERRED_UNDER_DEADLINE`
- Owner: Amin / OpenClaw
- Reviewer: Unassigned
- Reviewed on: deadline-deferred implementation

## Candidate

- Candidate ID: `r2_amin_feeaware_kalman_02`
- Shortlist priority: `high`
- Evidence strength: `medium`
- Product scope: `ASH_COATED_OSMIUM`, `INTARIAN_PEPPER_ROOT`
- Linked candidate file: `../03_strategy_candidates.md`

## Review Decision

- `_index.md` spec status: `deadline deferred`
- Approved for implementation: `yes, under hackathon pressure`
- Reviewer decision notes: User explicitly requested a new Round 2 bot and PR direction. This spec is created in one-page fast mode to preserve the gate.
- Required changes before coding: human review later if this becomes the chosen final submission.

## Sources

- Wiki facts: `../../../docs/prosperity_wiki/rounds/round_2.md`, `../../../docs/prosperity_wiki/api/01_trader_contract.md`, `../../../docs/prosperity_wiki/api/03_runtime_and_resources.md`, `../../../docs/prosperity_wiki/trading/01_exchange_mechanics.md`, `../../../docs/prosperity_wiki/trading/02_orders_and_position_limits.md`
- EDA evidence: `../01_eda/eda_report.md`
- Understanding summary: `../02_understanding.md` (not yet populated, assumption carried forward)
- Post-run research memory: none
- Additional repo evidence: existing Amin candidate and user guidance that Bruno's Kalman direction was strongest so far

## Selection Trace

- Based on candidate: keep Kalman-style adaptive fair value for ACO, but make the full bot explicitly Round-2 fee-aware by preferring strategies that monetize deeper books if extra access is granted while remaining robust when testing still exposes only 80% of quotes.
- Signals used: ACO short-horizon mean reversion around a stable level near 10000, ACO order-book imbalance as a small quote shift, IPR persistent positive drift with increasing day-level price baseline.
- Alternatives considered: fixed-fair-value hybrid, pure carry IPR plus static ACO MM, full regime-switching model.
- Why selected: user specifically called out Bruno's Kalman approach as strongest. EDA supports adaptive ACO fair value estimation. Round 2 fee mechanics reward strategies that can exploit additional quote visibility without depending on it.
- Known caveats: no final simulator access for bid EV, no authoritative performance comparison yet in this run, no reviewed understanding artifact.

## Evidence Traceability

- Linked EDA Signals: `../01_eda/eda_report.md`
  - ACO AR(1) phi around `0.66` to `0.79` with short half-life `1.7` to `2.9` ticks.
  - ACO Kalman grid search favored `Q=0.1`, `R=8.0` across days.
  - IPR drift fit is about `+999.9` per day with very stable slope.
  - Both products show short-horizon imbalance IC roughly `0.36` to `0.40`.
- Feature Evidence:
  - Adaptive ACO fair value should improve over fixed 10000 when visible book is thinned or temporarily skewed.
  - Extra visible quotes from accepted bid should help ACO liquidity-taking and fair-value estimation more than a purely static bot.
  - IPR still benefits from aggressive long accumulation, but quote placement should avoid paying unnecessary edge away when fees reduce net PnL.
- Regime Assumptions:
  - ACO remains short-horizon mean reverting in Round 2.
  - IPR upward drift remains the dominant edge.
- Evidence gaps or strategy assumptions:
  - Bid value for market access is not directly estimable from official testing because `bid()` is ignored.
  - Exact top-50% clearing threshold is unknown.

## Round-Specific Mechanics Contract

| Mechanic / Trader Function / Field | Source | Decision | Bot Behavior | Validation Check |
| --- | --- | --- | --- | --- |
| `Trader.bid()` for Round 2 Market Access Fee | `round_2.md`, `01_trader_contract.md` | implement | Return conservative positive integer bid, chosen to preserve upside from extra access while limiting profit haircut risk. | Bot defines `bid()` and returns integer. |
| Extra 25% quote access only if accepted | `round_2.md` | implement awareness | Strategy uses visible depth adaptively and should improve when more levels appear, but never require extra levels to function. | Bot logic works with baseline 80% quote subset. |
| Bid ignored during Round 2 testing | `round_2.md` | implement awareness | Core trading logic is independent of bid outcome. | Identical run logic regardless of accepted or rejected fee. |
| Manual Research/Scale/Speed allocation | `round_2.md` | not applicable | No manual challenge logic in bot. | No manual-allocation code present. |

## Feature Contract

| Feature | Source Fields | Online Availability | Role | Parameters | Missing-Signal Behavior | State / `traderData` Required | Validation Check |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ACO Kalman fair value | best bid, best ask, previous fair state | usable online | direct signal | `Q=0.1`, `R=8.0`, init from visible mid or 10000 | If book is one-sided, infer proxy mid from visible side; if empty, keep prior fair. | fair value and variance in JSON | `traderData` remains tiny, fair updates every tick. |
| ACO fee-aware market making | ACO fair value, top levels, position, imbalance | usable online | execution + edge capture | target half-spread 4 to 6 ticks, imbalance shift clipped to 2 ticks, inventory skew up to 4 ticks | If one side missing, place one-sided risk-reducing quote only. | optional diagnostics only | No crossed quotes, capacity-safe orders. |
| ACO opportunistic multi-level taking | visible asks below fair or bids above fair | usable online | direct monetization | take only if edge exceeds threshold and inventory allows | If only top level visible, still function on that level. | none | Trades only when expected edge exceeds fees/selection risk proxy. |
| IPR drift anchor | timestamp, visible book, optional previous anchor | usable online | direct signal | anchor = `12000 + 0.1 * day_offset?` not used directly; practical rule = aggressive long bias with passive reposting and mild trimming only far above local anchor | If no ask side, repost near bid without crossing. | optional last mid for diagnostics | Never exceeds long limit. |
| IPR imbalance-aware reposting | best bid, best ask, top volumes | usable online | execution filter | repost offset 0 to 2 ticks depending on imbalance and spread | If top volumes missing, default to `best_bid + 1` capped below best ask. | none | Passive repost remains legal and non-crossing. |

## Feature Exclusions

| Feature | Why Excluded | Reopen Only If |
| --- | --- | --- |
| Full HMM regime engine | too much complexity for current PR cycle | replay shows clustered failures that simple inventory control cannot fix |
| Nonlinear bid optimization | no official acceptance threshold data | manual scenario work supports clearer EV range |
| IPR active shorting | evidence still strongly favors long-only bias | new validation shows strong reversal episodes |

## Signal / Fair Value Logic

- ACO:
  - maintain a Kalman fair value from visible book.
  - sweep prices materially better than fair.
  - quote around fair with inventory and imbalance skew.
- IPR:
  - treat product as persistent upward-drift carry trade.
  - accumulate long inventory quickly, then maintain queue priority with passive reposting.
  - optionally trim only at clearly rich prices relative to local visible mid and only when very long.

## Execution Logic

- Buy behavior:
  - IPR sweeps visible asks while capacity remains and edge is consistent with long-bias carry.
  - ACO buys asks below fair by threshold and posts passive bid near fair.
- Sell behavior:
  - IPR rarely sells, mainly defensive trims when near max long and book is unusually rich.
  - ACO sells bids above fair by threshold and posts passive ask near fair.
- Passive/resting order behavior:
  - Both products repost residual intent without crossing visible quotes.
- Stay-idle behavior:
  - If book is empty or quote would be unsafe, do nothing.

## Position And Risk Handling

- Position limits:
  - `ASH_COATED_OSMIUM`: 80
  - `INTARIAN_PEPPER_ROOT`: 80
- Aggregate capacity tracked per product before each appended order.
- ACO inventory skew widens and shifts quotes away from building the same-side position.
- IPR reduces passive aggressiveness when already very long.

## State And Runtime

- `traderData` use:
  - ACO Kalman fair value and variance.
  - optional tiny diagnostics for IPR last visible mid.
- Imports:
  - standard library only.
- Runtime risk:
  - low; loops over visible levels only.
- Research-only dependencies excluded from uploadable bot: `yes`

## Expected Failure Cases

- Failure case: Kalman fair drifts off due to one-sided noisy book.
- Mitigation or validation: clamp one-sided proxy updates and retain prior fair when book quality is poor.

- Failure case: IPR overpays while already full long.
- Mitigation or validation: reduce repost aggressiveness and allow defensive trim in rich books.

- Failure case: non-zero bid destroys net edge if accepted too high.
- Mitigation or validation: keep bid conservative and document it as a parameter for later tuning.

## Validation Plan

- Contract checks: `run()` return shape, `bid()` integer, JSON `traderData`.
- Position-limit checks: aggregate order safety on both products.
- Local checks: syntax compile and simple smoke replay on sample data if tooling exists.
- Performance checks: compare candidate to existing Amin Round 2 hybrid and inspect whether ACO inventory path and fill quality improve.

## Implementation Handoff

- Target bot path: `../../bots/amin/canonical/candidate_r2_amin_feeaware_kalman_02.py`
- Parameters to implement:
  - `ACO_KALMAN_Q = 0.1`
  - `ACO_KALMAN_R = 8.0`
  - `ACO_BASE_HALF_SPREAD = 5`
  - `ACO_TAKE_EDGE = 2`
  - `IPR_TRIM_EDGE = 8`
  - `MARKET_ACCESS_BID = 12`
- Known caveats:
  - bid is a conservative placeholder, not an EV-optimized final answer
  - spec created in fast mode under user instruction
