# Strategy Spec: C06 — Full-Scope Composite Trader (Base)

## Review Status

- Status: `deferred under deadline`
- Owner: amin
- Reviewer: Unassigned
- Reviewed on: 2026-04-24 (deadline deferral)
- Deadline deferral reason: no time for formal review cycle; spec captures all required signal, execution, risk, state, and validation checks

## Candidate

- Candidate ID: `C06`
- Candidate priority tier: `spec-first`
- Evidence strength: `strong`
- Product scope: `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, `VEV_5000`, `VEV_5100`, `VEV_5200`, `VEV_5300`
- Linked candidate file: [`03_strategy_candidates.md`](../03_strategy_candidates.md)

## Review Decision

- `_index.md` spec status: `deferred under deadline`
- Approved for implementation: `deferred under deadline`
- Reviewer decision notes: fast-mode spec with full signal, execution, and risk definition
- Required changes before coding: none

## Sources

- Wiki facts: `round_3.md` — products, limits (200 for delta-1, 300 for vouchers), TTE=5d, integer prices
- EDA evidence: `01_eda/eda_option_surface_and_microstructure.md`, processed tables
- Understanding summary: `02_understanding.md`
- Post-run research memory: absent
- Playbook heuristics: feature-light quoting, inventory-aware skew, validate execution first

## Selection Trace

- Based on candidate: C06 (composite of C01 + C02 + C03)
- Signals used: mid-price reversion (delta-1), centered Bachelier residual reversion (vouchers), imbalance, spread, observed-surface guardrail
- Alternatives considered: single-product bots (too narrow for submission), full BS/IV stack (overkill), delayed-follow (rejected by EDA)
- Why selected: one Trader file is the submission unit; compositing independently-validated product branches maximizes aggregate PnL
- Known caveats: TTE=5d out-of-sample; vol proxy quality untested; online residual-anchor quality untested; integration complexity

## Evidence Traceability

- Linked EDA Signals: hydrogel imbalance-plus-reversion, velvetfruit anchor imbalance-plus-reversion, extrinsic residual reversion, surface sanity frame, spread-aware execution filter
- Feature Evidence: `derived_round_3_product_signal_metrics.csv`, `derived_round_3_option_reversion_metrics.csv`, `derived_round_3_option_extrinsic_by_tte.csv`, `derived_round_3_option_surface_summary.csv`, `derived_round_3_option_mutual_information.csv`
- Multivariate Evidence: HYDROGEL-VEX corr=0.006 (independent), VEX-voucher same-time coupling 0.75+, PCA PC1=72% price-anchor redundancy
- Process / Distribution Assumptions: delta-1 noisy mean reversion; active voucher regime with tradable residual dynamics
- Redundancy Decisions: merged price-anchor family into single Bachelier fair (PCA justification); imbalance kept as separate component (PC2=16.7%)
- Regime Assumptions: TTE=5d directionally similar to 6d-8d; surface shape holds; VEX remains stable anchor
- Understanding Insight: separate hydrogel branch + VEX-anchored voucher family; residual mispricing over delayed-follow
- Evidence gaps or strategy assumptions: exact vol proxy is a strategy assumption; the residual-anchor EMA is an online proxy for a day baseline, not the true offline baseline; TTE=5d decay rate is assumed similar

## Round-Specific Mechanics Contract

| Mechanic / Trader Function / Field | Source | Decision | Bot Behavior | Validation Check |
| --- | --- | --- | --- | --- |
| `Trader.run(state)` | API contract | implement | main entry point | returns (result, conversions, traderData) |
| `Trader.bid()` | Round 2 only | exclude | not defined (Round 3 does not require it) | absent from code |
| Integer prices | API contract | implement | all Order prices are int via `round()` | no float prices in result |
| Per-symbol position limits | round doc | implement | capacity check before order submission | aggregate buy/sell never exceeds limit headroom |
| VEV_6000/VEV_6500 floor instruments | EDA evidence | exclude | no orders for these symbols | absent from result |
| VEV_5400/VEV_5500 wide-spread | EDA evidence | exclude (wave 1) | no orders for these symbols | absent from result |
| VEV_4000/VEV_4500 ITM | EDA evidence | exclude (wave 1) | no orders for these symbols | absent from result |
| Manual Bio-Pod | round doc | not applicable | not in Trader.run() | absent from code |

## Feature Contract

### F1: Mid-Price Reversion (HYDROGEL_PACK)

| Field | Value |
| --- | --- |
| Feature | mid-price lag-1 reversion |
| Source Fields | `order_depths[symbol].buy_orders`, `order_depths[symbol].sell_orders` |
| Online Availability | usable online |
| Role | direct signal |
| Parameters | `fair = mid_price` (average of best bid and best ask) |
| Multivariate Relationship | independent from VEX (corr 0.006) |
| Process Assumption | noisy delta-1 mean reversion |
| Redundancy Decision | not applicable (single product) |
| Missing-Signal Behavior | skip product; no orders |
| State / traderData Required | none |
| Validation / Invalidation Check | track PnL per product; disable if consistently negative |

### F2: Imbalance Filter (HYDROGEL_PACK, VELVETFRUIT_EXTRACT)

| Field | Value |
| --- | --- |
| Feature | `imbalance_1` — top-of-book volume imbalance |
| Source Fields | best bid volume, best ask volume from `order_depths` |
| Online Availability | usable online |
| Role | execution filter / directional lean |
| Parameters | `imbalance = (bid_vol - ask_vol) / (bid_vol + ask_vol)` |
| Multivariate Relationship | PCA PC2 (16.7%), orthogonal to anchor |
| Process Assumption | imbalance correlates modestly with future short-horizon delta |
| Redundancy Decision | keep (non-redundant with reversion signal) |
| Missing-Signal Behavior | default to 0 (no lean) |
| State / traderData Required | none |
| Validation / Invalidation Check | compare with vs without imbalance lean |

### F3: Spread Gate (all products)

| Field | Value |
| --- | --- |
| Feature | relative spread threshold |
| Source Fields | best bid, best ask from `order_depths` |
| Online Availability | usable online |
| Role | risk control |
| Parameters | `spread = best_ask - best_bid`; skip or widen when spread > threshold |
| Multivariate Relationship | loads with price-anchor in PCA |
| Process Assumption | wide spreads indicate thin books and poor execution |
| Redundancy Decision | keep for execution gating (different role from signal) |
| Missing-Signal Behavior | skip product |
| State / traderData Required | none |
| Validation / Invalidation Check | verify active-trading timestamps have acceptable spreads |

### F4: Bachelier Fair Value (vouchers)

| Field | Value |
| --- | --- |
| Feature | Bachelier (normal-model) call price as fair value |
| Source Fields | `VELVETFRUIT_EXTRACT` mid as S, strike K from symbol name, TTE=5 (days), sigma_abs estimated |
| Online Availability | usable online (hand-coded norm_cdf) |
| Role | direct signal (fair-value backbone) |
| Parameters | `C_N = (S-K)*N(d) + sigma_abs*sqrt(T)*phi(d)` where `d = (S-K)/(sigma_abs*sqrt(T))` |
| Multivariate Relationship | VEX-voucher same-time coupling 0.75+ |
| Process Assumption | active option regime with meaningful extrinsic |
| Redundancy Decision | merged intrinsic + mid_price + moneyness into single Bachelier fair (PCA justification) |
| Missing-Signal Behavior | fall back to intrinsic value = max(S-K, 0) |
| State / traderData Required | sigma_abs estimate (can use rolling VEX move scale or fixed calibration) |
| Validation / Invalidation Check | compare Bachelier residuals vs intrinsic-only residuals; validate cross-strike ranking |

### F5: Centered Residual Reversion (online proxy for `extrinsic_dev_day`)

| Field | Value |
| --- | --- |
| Feature | centered residual around a slow residual anchor |
| Source Fields | voucher mid from `order_depths`, Bachelier fair from F4, per-symbol residual anchor from `traderData` |
| Online Availability | usable online |
| Role | direct signal |
| Parameters | `raw_residual = observed_mid - bachelier_fair`; `centered_residual = raw_residual - residual_anchor`; update `residual_anchor_next = (1 - alpha) * residual_anchor + alpha * raw_residual` with a slow `alpha` |
| Multivariate Relationship | MI 0.3358 (strongest option feature) |
| Process Assumption | residual mean-reverts around zero |
| Redundancy Decision | keep (primary signal) |
| Missing-Signal Behavior | skip voucher; no orders |
| State / traderData Required | required: per-symbol slow residual anchor in `traderData` |
| Validation / Invalidation Check | compare centered-residual behavior versus raw residual; verify the anchor stays slow enough to preserve signal and stable enough to prevent drift |

### F6: Surface Monotonicity/Convexity Guardrail (vouchers)

| Field | Value |
| --- | --- |
| Feature | observed cross-strike shape check |
| Source Fields | observed voucher mids across active strikes from `order_depths` |
| Online Availability | usable online |
| Role | risk control |
| Parameters | check observed `mid_K1 >= mid_K2` for `K1 < K2` with small tick tolerance; when at least 3 strikes are visible, also require approximate convexity on observed mids |
| Multivariate Relationship | surface checks across the voucher family |
| Process Assumption | surface should be monotone and convex in call-price space |
| Redundancy Decision | keep (structural guardrail, not signal) |
| Missing-Signal Behavior | skip monotonicity if fewer than 2 active strikes have valid books; skip convexity if fewer than 3 are visible |
| State / traderData Required | none |
| Validation / Invalidation Check | log observed-surface guardrail triggers; verify they reduce bad fills and are not trivially always true |

## Feature Exclusions

| Feature | Why Excluded | Reopen Only If |
| --- | --- | --- |
| Delayed underlying-follow | EDA rejects lag-1+ correlations | live logs show stale option books |
| VEV_6000/VEV_6500 floor alpha | constant 0.5 mids, zero variance | live data breaks floor |
| Trade-flow features | sparse prints; not reliable | richer live tape available |
| PCA components / cluster labels | research-only; no online proxy | online proxy defined in spec |
| Full BS/IV stack | overkill for short-dated single-expiry | Bachelier proves systematically biased |
| Family-level exposure matrix (Bergault) | too complex for wave 1 | simple per-symbol skew is insufficient |

## Signal / Fair Value Logic

### Delta-1 Products (HYDROGEL_PACK, VELVETFRUIT_EXTRACT)

- Signal: mid-price is the fair value; trade against book levels that deviate
- Inputs: best bid, best ask, volumes
- Fair value: `fair = (best_bid + best_ask) / 2`
- Quote logic: place buy orders below fair and sell orders above fair; lean quotes using imbalance
- Missing-signal behavior: skip product

### Voucher Products (VEV_5000 to VEV_5300)

- Signal: centered residual around a slowly updated residual anchor; trade when observed mid deviates from `bachelier_fair + residual_anchor`
- Inputs: VEX mid as S, strike K from symbol suffix, TTE=5/365 (annualized), sigma_abs parameter
- Fair value: `bachelier_call(S, K, T, sigma_abs)` with hand-coded `norm_cdf` and `norm_pdf`
- Residual pieces: `raw_residual = observed_voucher_mid - bachelier_fair`; `centered_residual = raw_residual - residual_anchor`
- Trade logic: buy when `centered_residual < -threshold`, sell when `centered_residual > +threshold`
- Missing-signal behavior: skip voucher if VEX or voucher book is empty

## Execution Logic

- **Buy behavior**: place buy orders when signal suggests underpricing. For delta-1: buy at levels below fair when ask is attractive. For vouchers: buy when the centered residual is sufficiently negative.
- **Sell behavior**: symmetric. For delta-1: sell at levels above fair when bid is attractive. For vouchers: sell when the centered residual is sufficiently positive.
- **Passive/resting order behavior**: place limit orders around `bachelier_fair + residual_anchor`, then apply any inventory skew.
- **Stay-idle behavior**: skip product when spread is too wide, book is empty, or signal is missing. For vouchers: skip aggressive and passive quoting when the observed-surface guardrail is violated.

## Position And Risk Handling

- Position limits: HYDROGEL_PACK 200, VELVETFRUIT_EXTRACT 200, each VEV_* 300
- Aggregate buy capacity: `limit - current_position` (cannot exceed long limit)
- Aggregate sell capacity: `limit + current_position` (cannot exceed short limit)
- Inventory skew: quote skew proportional to current position divided by limit; lean quotes to flatten inventory

## State And Runtime

- `traderData` use: JSON string storing `sigma_abs`, `prev_vex`, and per-symbol slow residual anchors; kept small
- Imports: `datamodel` (Order, TradingState), `json`, `math` only
- Runtime risk: low; all computations are O(1) per product per iteration
- Research-only dependencies excluded from uploadable bot: `yes`

## Expected Failure Cases

| Failure Case | Mitigation |
| --- | --- |
| VEX book is empty (voucher fair values undefined) | skip all vouchers for that iteration |
| Spread too wide to trade profitably | spread gate skips product |
| Bachelier fair is negative or unreasonable | fall back to intrinsic value |
| Residual anchor drifts too quickly and absorbs the edge | keep anchor EMA slow; compare centered vs raw residual diagnostics |
| Position near limit | reduce order size; lean quotes to flatten |
| TTE=5d behavior diverges from historical | explicit risk; C07 variant tests cautious calibration |

## Validation Plan

- Contract checks: Trader class exists, run() returns 3-tuple, result has correct products, conversions=0, traderData is string
- Order sign and limit checks: all buy quantities positive, all sell quantities negative, aggregate capacity respected
- Performance/run checks: per-product PnL attribution, fill rate, position utilization, spread capture, centered-residual trigger rate, observed-surface guardrail trigger rate
- Debug signals: log raw residuals, residual anchors, centered residuals, fair values, imbalance, spread, position per iteration

## Implementation Handoff

- Historical implemented bot path: `rounds/round_3/bots/amin/historical/candidate_c06_v01_centered_base.py`
- Frozen legacy reference: `rounds/round_3/bots/amin/historical/candidate_c06_composite_base.py` remains untouched because it already has a paired performance JSON and is archived
- Parameters to implement: `sigma_abs` (initial estimate ~80-120 for VEX daily moves), `entry_threshold` (centered-residual entry, ~2-5 ticks), `spread_limit` (max acceptable spread), `mm_offset` (quote offset from fair for delta-1), `inventory_skew_factor`, `residual_anchor_alpha`
- Known caveats: sigma_abs needs calibration; centered-residual anchor speed may need tuning; entry_threshold may need tuning; TTE=5d is out-of-sample
