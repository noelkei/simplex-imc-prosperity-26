# Spec: candidate_03_combined

## Reopen Notice

- Historical note: this spec was written for the previous shortlist before Phase 03 strategy expansion was reopened on 2026-04-16.
- Current pipeline note: Phase 04 is now `BLOCKED` until the expanded strategy shortlist is reviewed.
- Use this spec as the baseline reference for `candidate_03_combined`, not as approval to implement or validate newly shortlisted `candidate_05_microstructure_edge_scalper` or `candidate_06_aco_markov_regime_mm`.

Implementation must not start until this spec is reviewed.

## Review Status

- Status: READY_FOR_REVIEW
- Owner: Claude
- Reviewer: Unassigned
- Reviewed on: —

## Candidate

- Candidate ID: `candidate_03_combined`
- Shortlist priority: high — **recommended production bot**
- Evidence strength: strong (inherits from both sub-strategies)
- Product scope: `INTARIAN_PEPPER_ROOT` + `ASH_COATED_OSMIUM`
- Linked candidate file: `../03_strategy_candidates.md`
- Sub-strategy specs (reference): `spec_candidate_01_ipr_drift_mm.md`, `spec_candidate_02_aco_fixed_fv_mm.md`

## Review Decision

- `_index.md` spec status: not reviewed
- Approved for implementation: yes
- Reviewer decision notes: approved by human 2026-04-16
- Required changes before coding: none anticipated

---

## Sources

- Wiki facts: `workspace/00_ingestion.md` — position limits ±80 each product, order signs, `run()` contract
- EDA evidence: `workspace/01_eda/eda_round_1.md` — IPR drift R²=0.9999; ACO FV~10000 94.4% ±10; spread IPR~13 ACO~16; zero/one-sided rows
- Understanding: `workspace/02_understanding.md` — products are independent; no cross-product signal
- Playbook: none

## Evidence Traceability

- Linked EDA Signals: IPR `FV(t)=day_start+0.001×t` R²=0.9999; ACO `FV=10000` confirmed by book + trades
- Feature Evidence: `mid_price`, `timestamp`, `ask_price_1`, `bid_price_1` per product
- Regime Assumptions: IPR slope stable; ACO FV stable; **products are independent** — no cross-product dependency
- Understanding Insight: combining both into one `Trader` is safe because logic is fully independent per product; a single submission covers both
- Evidence gaps: IPR slope and ACO FV are historical assumptions; live round may differ

---

## Architecture

Single `Trader` class. `run()` processes each product independently and populates a shared `result` dict. Sub-strategies share `traderData` using **namespaced keys** to avoid collisions.

```
Trader.run(state):
    result = {}
    conversions = 0
    # Sub-strategy 1 — IPR
    result["INTARIAN_PEPPER_ROOT"], ipr_state = _run_ipr(state, parsed_traderData)
    # Sub-strategy 2 — ACO
    result["ASH_COATED_OSMIUM"], aco_state   = _run_aco(state, parsed_traderData)
    traderData = _serialize(ipr_state, aco_state)
    return result, conversions, traderData
```

**Failure isolation**: if one sub-strategy raises an exception or produces no orders, the other must still execute and return its orders. Use try/except per sub-strategy; on exception, log and return empty list for that product.

---

## Parameters (all visible — not invented at code time)

### IPR Sub-strategy

| Parameter | Value | Rationale |
| --- | --- | --- |
| `IPR_DRIFT_SLOPE` | 0.001 | EDA-confirmed per-tick drift rate |
| `IPR_SPREAD_BUFFER` | 4 | Edge above residual std≈2; half-spread ~6.5 |
| `IPR_ORDER_SIZE` | 20 | 4 round trips within ±80 |
| `IPR_MAX_POSITION` | 75 | 5-unit buffer below hard limit |

### ACO Sub-strategy

| Parameter | Value | Rationale |
| --- | --- | --- |
| `ACO_FV` | 10000 | EDA-confirmed fixed fair value |
| `ACO_SPREAD_BUFFER` | 8 | Edge above price std≈5.35; half mean-spread ~8 |
| `ACO_ORDER_SIZE` | 20 | Conservative |
| `ACO_MAX_POSITION` | 75 | 5-unit buffer below hard limit |
| `ACO_SKEW_FACTOR` | 0.1 | Inventory skew toward flat |
| `ACO_FV_ALERT_THRESHOLD` | 30 | Deviation from FV triggering warning log |
| `ACO_FV_ALERT_TICKS` | 50 | Consecutive ticks to trigger warning |

---

## Signal / Fair Value Logic

### IPR
- `FV_IPR(t) = ipr_day_start + IPR_DRIFT_SLOPE × timestamp`
- `ipr_day_start` = first valid (non-zero) `mid_price` observed for IPR, persisted via `traderData` key `"IPR_DS"`.
- If `mid_price = 0`: skip quoting IPR this tick; do not update `ipr_day_start`; use last known FV.
- If `ipr_day_start` not yet set: defer quoting until first valid tick.

### ACO
- `FV_ACO = ACO_FV` (constant 10000)
- `skew_offset = -ACO_SKEW_FACTOR × aco_position` — shifts both thresholds to encourage rebalancing.
- If `mid_price = 0`: skip quoting ACO this tick; increment `aco_alert_count` only if mid_price was non-zero before.
- If `|mid_price - ACO_FV| > ACO_FV_ALERT_THRESHOLD` for `ACO_FV_ALERT_TICKS` consecutive ticks: log warning, continue quoting — do not auto-change FV.

### Cross-product note
- IPR and ACO mid_price zeroes are independent events. A zero in one product does not affect the other sub-strategy.

---

## Execution Logic

### IPR
- **Buy**: if `best_ask < FV_IPR(t) - IPR_SPREAD_BUFFER` → buy at `best_ask`, qty = `min(IPR_ORDER_SIZE, IPR_MAX_POSITION - ipr_pos)`. Skip if capacity ≤ 0.
- **Sell**: if `best_bid > FV_IPR(t) + IPR_SPREAD_BUFFER` → sell at `best_bid`, qty = `max(-IPR_ORDER_SIZE, -(IPR_MAX_POSITION + ipr_pos))`. Skip if capacity ≤ 0.
- **Idle**: no side satisfies threshold, or capacity = 0.

### ACO
- **Buy**: if `best_ask < ACO_FV - ACO_SPREAD_BUFFER + skew_offset` → buy at `best_ask`, qty = `min(ACO_ORDER_SIZE, ACO_MAX_POSITION - aco_pos)`. Skip if capacity ≤ 0.
- **Sell**: if `best_bid > ACO_FV + ACO_SPREAD_BUFFER + skew_offset` → sell at `best_bid`, qty = `max(-ACO_ORDER_SIZE, -(ACO_MAX_POSITION + aco_pos))`. Skip if capacity ≤ 0.
- **Idle**: no side satisfies threshold after skew adjustment, or capacity = 0.

### Shared execution rules
- One order per side per product per tick.
- Aggregated orders per product must not exceed remaining capacity (wiki enforcement: all orders cancelled if limit would be breached).
- Both sub-strategies run every tick regardless of the other's outcome.

---

## Position And Risk Handling

| Product | Limit | Max position used | Buy capacity | Sell capacity |
| --- | --- | --- | --- | --- |
| `INTARIAN_PEPPER_ROOT` | ±80 | ±75 | `75 - ipr_pos` | `75 + ipr_pos` |
| `ASH_COATED_OSMIUM` | ±80 | ±75 | `75 - aco_pos` | `75 + aco_pos` |

- Positions are **independent** — IPR position does not affect ACO capacity or vice versa.
- Both products use separate capacity calculations from `state.position.get(SYMBOL, 0)`.

---

## State And Runtime

### `traderData` schema
Serialized as a semicolon-delimited key:value string. All keys namespaced to avoid collisions.

| Key | Type | Default | Description |
| --- | --- | --- | --- |
| `IPR_DS` | float | `None` (absent) | Day-start price for IPR drift intercept |
| `ACO_AC` | int | `0` | Consecutive ACO alert ticks counter |

Example: `"IPR_DS:10998.5;ACO_AC:0"`

Parsing: split on `;`, then on `:`. If malformed or absent, use defaults. If a key is missing, treat as default. Do not crash on malformed `traderData`.

### Imports
- `from datamodel import TradingState, Order` (platform-provided)
- No external libraries (no numpy, pandas, etc.)
- Simple arithmetic only — no floating point precision issues expected at this scale.

### Runtime risks
- `traderData` string must not exceed platform string limits — current schema is ~25 chars; well within safe bounds.
- Both sub-strategies must complete within the platform's per-tick time budget — both are O(1).
- Do not mutate `state` object.

---

## Expected Failure Cases

| Failure Case | Sub-strategy | Mitigation |
| --- | --- | --- |
| IPR `ipr_day_start` never set (tick-0 is zero) | IPR | Defer quoting; set on next valid tick |
| ACO FV sustained deviation (hidden pattern) | ACO | Log alert; continue quoting FV=10000; observe in validation |
| IPR drift slope wrong in live round | IPR | FV diverges; log and observe; no auto-adapt in spec v1 |
| One sub-strategy raises exception | Both | try/except per sub-strategy; return empty orders for failing product, preserve other |
| Position at ±75 | Both | Capacity clipping — order size reduces to 0 naturally |
| Exchange rejects all orders (limit breach) | Both | Capacity calculation prevents if correct; validate in backtest |
| `traderData` malformed | Both | Parse defensively; fall back to defaults |

---

## Validation Plan

### Contract checks
- `run()` returns a 3-tuple `(result, conversions, traderData)`.
- `result` is a dict; may contain keys `"INTARIAN_PEPPER_ROOT"` and/or `"ASH_COATED_OSMIUM"`.
- Each value is a list of `Order` objects with correct `symbol`, `price`, `quantity` sign.
- `conversions` is an integer (0 for this round).
- `traderData` is a non-None string parseable by the same parser.

### Order sign and limit checks
- Buy orders: `quantity > 0`; sell orders: `quantity < 0`.
- Per tick per product: `sum(buy quantities) ≤ 80 - current_position`; `|sum(sell quantities)| ≤ 80 + current_position`.
- `|position|` never exceeds 80 in backtest replay.

### Performance checks (backtest on days −2, −1, 0)
- IPR P&L > 0 across 3 days.
- ACO P&L > 0 across 3 days.
- Combined P&L > 0.
- No position-limit rejection events.
- IPR position does not rail at ±75 for extended runs (>200 ticks).
- ACO inventory skew demonstrably reduces max absolute position vs no-skew baseline.

### Debug signals to inspect
- Per tick: `IPR FV(t)`, `ipr_pos`, IPR buy/sell threshold, orders placed for IPR.
- Per tick: `ACO skew_offset`, `aco_pos`, `aco_alert_count`, ACO buy/sell threshold, orders placed for ACO.
- `traderData` string at each tick.
- Any exception traces from either sub-strategy.

---

## Spec Quality Checklist

- [x] Candidate ID, priority, evidence basis linked from shortlist.
- [x] Linked EDA signals, feature evidence, regime assumptions, understanding insight recorded.
- [x] Signal / fair value logic defined for both products.
- [x] Execution behavior (buy, sell, idle) defined for both products.
- [x] Missing-data behavior defined (zero mid_price, one-sided book, malformed traderData).
- [x] Position limits and aggregate capacity defined per product.
- [x] Parameters visible and not hidden.
- [x] `traderData` schema defined with namespaced keys — no collision risk.
- [x] Failure isolation between sub-strategies defined.
- [x] Runtime constraints noted (O(1), no external libs, string size safe).
- [x] Expected failure cases named with mitigations.
- [x] Validation checks specific enough for testing.
- [x] Assumptions labeled (slope, FV, independence).
- [x] Reviewer and status filled.

---

## Implementation Handoff

- Target bot path: `rounds/round_1/bots/<member>/canonical/candidate_03_combined.py`
- Implement as a single `Trader` class with two private helper methods (one per product).
- Parameters: all listed in the Parameters section above — implement as module-level constants.
- `traderData` schema: `"IPR_DS:<float>;ACO_AC:<int>"` — parse defensively.
- Known caveats:
  - IPR slope 0.001 hardcoded — flag for observation in first live run.
  - ACO FV=10000 hardcoded — monitor for hidden pattern; alert counter logged.
  - Exception isolation per sub-strategy is **required** — do not let one product crash the other.
