# Round 2 Strategy Spec - Amin Hybrid IPR Drift + ACO Market Making

## Review Status

- Status: `READY_FOR_REVIEW`
- Owner: Amin / OpenClaw
- Reviewer: Unassigned
- Reviewed on: not reviewed

## Candidate

- Candidate ID: `r2_amin_hybrid_01`
- Shortlist priority: `high`
- Evidence strength: `medium`
- Product scope: `INTARIAN_PEPPER_ROOT`, `ASH_COATED_OSMIUM`
- Linked candidate file: `../03_strategy_candidates.md`

## Review Decision

- `_index.md` spec status: `not reviewed`
- Approved for implementation: `no`
- Reviewer decision notes: pending
- Required changes before coding: human review or explicit deadline deferral

## Sources

- Wiki facts: `../../../docs/prosperity_wiki/rounds/round_2.md`, `../../../docs/prosperity_wiki/api/01_trader_contract.md`, `../../../docs/prosperity_wiki/trading/02_orders_and_position_limits.md`
- EDA evidence: `../01_eda/eda_report.md`
- Understanding summary: `../02_understanding.md`
- Post-run research memory: none
- Playbook heuristics: not used directly

## Selection Trace

- Based on candidate: hybrid carry-plus-market-making structure reused from strongest Round 1 bot shapes.
- Signals used: IPR day-level drift persistence, ACO mean-reverting fair-value behavior near 10000, order-book imbalance signal as optional execution skew.
- Alternatives considered: pure Round 1 carry baseline, pure imbalance-driven microstructure bot, regime-aware ACO model.
- Why selected: fastest robust path with current evidence. It matches the strongest product-level structure already visible in Round 2 EDA and reuses low-complexity implementation patterns from Round 1.
- Known caveats: no final-round extra-access data, no reviewed understanding doc yet, no direct evidence that a more complex regime model beats simple quoting on Round 2.

## Evidence Traceability

- Linked EDA Signals: `../01_eda/eda_report.md`
  - IPR linear drift fit of about `+999.9` per day on each sample day.
  - ACO mid mean near `10000` with low variance and short half-life.
  - Both products show positive order-book imbalance IC around `0.36` to `0.40` at short horizons.
- Feature Evidence:
  - IPR: drift/carry behavior is strong enough to justify aggressive long accumulation until position limit.
  - ACO: stable fair value near `10000` supports sweep-plus-passive market making.
  - Imbalance: evidence is good enough for a light quote shift, not a standalone directional engine yet.
- Regime Assumptions:
  - ACO is still primarily mean-reverting in Round 2.
  - IPR still rewards directional long carry.
- Understanding Insight:
  - Round 2 changed market access mechanics, not core product identities.
- Research tool evidence used, if any:
  - none beyond repo EDA artifacts.
- Evidence gaps or strategy assumptions:
  - final value of extra market access is unknown.
  - testing ignores `bid()`, so bid calibration remains a scenario decision outside core bot validation.

## Round-Specific Mechanics Contract

| Mechanic / Trader Function / Field | Source | Decision | Bot Behavior | Validation Check |
| --- | --- | --- | --- | --- |
| `Trader.bid()` for Round 2 Market Access Fee | `round_2.md`, `01_trader_contract.md` | implement | Return a conservative placeholder bid of `0` until manual decision and EV analysis are complete. | Bot defines `bid()` and returns an integer. |
| Extra 25% quote access only for accepted top-50% bids | `round_2.md` | exclude from trading logic | No assumption of extra quotes during testing logic; core strategy must work under default 80% quote visibility. | No code path depends on unseen extra quotes. |
| Bid ignored during Round 2 testing | `round_2.md` | implement awareness | Do not tune core trading behavior around bid outcomes. | Testing behavior identical regardless of bid. |
| Manual Research/Scale/Speed allocation | `round_2.md` | not applicable | Keep fully separate from `Trader.run()`. | No manual logic appears in bot code. |

## Feature Contract

| Feature | Source Fields | Online Availability | Role | Parameters | Missing-Signal Behavior | State / `traderData` Required | Validation Check |
| --- | --- | --- | --- | --- | --- | --- | --- |
| IPR long carry accumulation | IPR order book best asks, best bid, current position | usable online | direct signal | limit=80, buy-through-all-asks, repost at best bid + 1 | If no ask side, only rest passive bid if legal. If no book, do nothing. | none | Never exceed long capacity; uses positive quantities only for buys. |
| ACO fixed fair value market making | ACO order book, current position | usable online | direct signal | fair value=10000, half spread=5, inventory skew=3 | If only one side of book exists, place defensive one-sided quotes and optionally reduce inventory. | optional JSON state for diagnostics only | Sweep only when price is strictly better than fair value; passive quotes remain inside capacity. |
| ACO inventory skew | position, position limit | usable online | risk control | skew proportional to position / limit | If position missing, assume 0. | none | Quotes shift away from adding more inventory in current direction. |
| ACO imbalance quote shift | best level bid/ask volumes | usable online | execution filter | micro shift clipped to [-2, 2] ticks | If either top side missing, no imbalance shift. | none | Quote shift changes prices only modestly and never breaks crossed-book safety checks. |
| ACO fair value deviation counter | top-of-book mid | log-only diagnostic | diagnostic | alert threshold 30, alert ticks 50 | Reset counter if two-sided mid unavailable or deviation normalizes. | JSON dict with alert counter | `traderData` stays tiny and valid JSON. |

## Feature Exclusions

| Feature | Why Excluded | Reopen Only If |
| --- | --- | --- |
| Full Kalman fair-value model for ACO | helpful but not necessary for first candidate; fixed FV already fits current evidence | Simple fixed-FV bot underperforms or logs show persistent ACO level drift |
| HMM/regime-aware ACO switching | too complex for first candidate and prior evidence does not clearly justify it | Validation shows large losses clustered in identifiable regimes |
| Aggressive IPR shorting logic | evidence favors upward drift, not symmetric mean reversion | New evidence shows strong reversal windows or changed final-day behavior |
| Non-zero Market Access Fee bid | incremental value still unknown and testing does not validate it | Scenario work produces a defendable EV-positive bid range |

## Signal / Fair Value Logic

- Signal:
  - IPR: persistent upward drift, so default posture is accumulate long inventory aggressively.
  - ACO: trade around a stable fair value of `10000` and capture spread / mispricings.
- Inputs:
  - visible order book levels, current positions, optional top-level imbalance.
- Missing-signal behavior:
  - if order book side is missing, degrade to conservative passive quoting or no-op.

## Execution Logic

- Buy behavior:
  - IPR: buy visible asks while long capacity remains; then place one passive bid slightly above current best bid when possible.
  - ACO: sweep asks priced below fair value; add passive buy quote below fair value adjusted by inventory and imbalance.
- Sell behavior:
  - IPR: no active short-selling in first candidate.
  - ACO: sweep bids priced above fair value; add passive sell quote above fair value adjusted by inventory and imbalance.
- Passive/resting order behavior:
  - IPR reposts residual long demand.
  - ACO posts both sides when book is two-sided and capacity permits, otherwise posts one-sided risk-aware fallback quotes.
- Stay-idle behavior:
  - If no safe legal quote can be formed or no book is visible, place no order for that product.

## Position And Risk Handling

- Position limits:
  - 80 for `INTARIAN_PEPPER_ROOT`
  - 80 for `ASH_COATED_OSMIUM`
- Aggregate buy capacity:
  - computed from current start-of-tick position and all buy orders already added.
- Aggregate sell capacity:
  - computed from current start-of-tick position and all sell orders already added.
- Inventory skew or reduction:
  - ACO quotes skew away from adding more exposure in the current inventory direction.
  - One-sided ACO fallback attempts mild inventory reduction when exposed.

## State And Runtime

- `traderData` use:
  - optional tiny JSON dict for ACO diagnostic counter only.
- Imports:
  - `json`, Prosperity datamodel classes.
- Runtime risk:
  - low, logic is simple loops over visible levels only.
- Research-only dependencies excluded from uploadable bot: `yes`

## Expected Failure Cases

- Failure case: one-sided book leads to invalid crossed quote.
- Mitigation or validation: clamp quote relative to visible best price and skip if unsafe.

- Failure case: aggregate orders exceed position limits.
- Mitigation or validation: track start position plus used buy/sell capacity before appending each order.

- Failure case: stale assumption that ACO fixed FV=10000 remains valid in final run.
- Mitigation or validation: inspect logs and validation runs, and upgrade to adaptive FV only if needed.

## Validation Plan

- Contract checks:
  - bot returns `result, conversions, traderData`
  - bot defines `bid()`
- Order sign and limit checks:
  - buy quantities positive, sell quantities negative, aggregate exposure stays within limits
- Performance/run checks:
  - compare candidate behavior against Round 1 baseline ideas on Round 2 sample days
  - inspect whether IPR reliably reaches long inventory and whether ACO avoids repeated inventory traps
- Debug signals to inspect:
  - ACO inventory path
  - IPR fill aggressiveness
  - ACO alert counter if fair value appears off-market

## Implementation Handoff

- Target bot path, normally `rounds/round_X/bots/<member>/canonical/...`: `../../bots/amin/canonical/candidate_r2_amin_hybrid_01.py`
- Parameters to implement:
  - `ACO_FAIR_VALUE = 10000`
  - `ACO_HALF_SPREAD = 5`
  - `ACO_SKEW_FACTOR = 3`
  - `ACO_IMBALANCE_SHIFT_CLIP = 2`
  - `MARKET_ACCESS_BID = 0`
- Known caveats:
  - spec is not reviewed yet
  - bid decision intentionally deferred
  - understanding and shortlist artifacts should be synchronized after implementation starts under hackathon pressure
