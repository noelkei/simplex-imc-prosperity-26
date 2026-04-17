# Spec: Experimental Five-Bot Matrix

Implementation may proceed from this lightweight spec because the user approved a five-bot performance batch on 2026-04-16. These are exploratory bots, not final submission approval.

## Review Status

- Status: COMPLETED
- Owner: Codex
- Reviewer: User
- Reviewed on: 2026-04-16

## Candidate

- Candidate IDs: `candidate_09_baseline_fv_combo`, `candidate_10_carry_tight_mm`, `candidate_11_microstructure_scalper`, `candidate_12_aco_markov_overlay`, `candidate_13_hybrid_adaptive_model`
- Shortlist priority: high for batch implementation, promote only after validation
- Evidence strength: strong for FV baselines; medium for microstructure/model variants
- Product scope: `INTARIAN_PEPPER_ROOT` and `ASH_COATED_OSMIUM`
- Linked candidate file: `../03_strategy_candidates.md`

## Review Decision

- `_index.md` spec status: approved with caveats
- Approved for implementation: yes
- Reviewer decision notes: user requested five different bots for performance testing and accepted complexity/code size.
- Required changes before coding: none; keep each bot self-contained and validation-ready.

## Sources

- Wiki facts: `../00_ingestion.md`; position limits +/-80 each product; order signs positive buy / negative sell.
- EDA evidence: `../01_eda/eda_round_1.md`; `../01_eda/eda_strategy_expansion_feature_lab.md`; `../01_eda/eda_strategy_expansion_models.md`; `../01_eda/eda_cross_product_relationships.md`.
- Understanding summary: `../02_understanding.md`.
- Playbook heuristics: none used as evidence.

## Evidence Traceability

- IPR signal: drift FV with slope 0.001/timestamp, R2 about 0.9999, residual std about 2.20.
- ACO signal: fixed FV around 10000, residual std about 5.35, trade median 10000.
- Microstructure signal: sparse positive best-quote edge and imbalance correlation around 0.64 with next residual delta.
- Markov signal: ACO under bucket mean next delta +4.67; over bucket -4.06; deep buckets sparse and must not be over-weighted.
- Cross-product insight: no actionable cross-product relationship found; one bot still runs both product strategies concurrently.
- Evidence gaps: fill model and PnL must be validated by replay/backtest; model signals may capture bid-ask bounce.

## Bot Matrix

| Bot ID | Target Path | IPR Logic | ACO Logic | Purpose |
| --- | --- | --- | --- | --- |
| `bot_01` | `rounds/round_1/bots/noel/canonical/candidate_09_bot01_baseline_fv_combo.py` | drift FV MM | fixed FV MM | robust baseline |
| `bot_02` | `rounds/round_1/bots/noel/canonical/candidate_10_bot02_carry_tight_mm.py` | max-long carry | tight aggressive MM | high-upside aggressive |
| `bot_03` | `rounds/round_1/bots/noel/canonical/candidate_11_bot03_micro_scalper.py` | microstructure scalper | microstructure scalper | margin extraction |
| `bot_04` | `rounds/round_1/bots/noel/canonical/candidate_12_bot04_aco_markov.py` | drift FV MM | Markov-regime MM | ACO hidden-pattern test |
| `bot_05` | `rounds/round_1/bots/noel/canonical/candidate_13_bot05_hybrid_adaptive.py` | defensive hybrid + score | adaptive FV + score | complex adaptive ensemble |

## Shared Position And Risk Handling

- Product limits: +/-80 for both products.
- Aggregate buy capacity: `limit - current_position - already_ordered_buy_qty`.
- Aggregate sell capacity: `limit + current_position - already_ordered_sell_abs_qty`.
- Every bot must clip orders before adding them.
- If a product book is missing or empty, return no orders for that product.
- If a fair value cannot be initialized, skip that product until a valid quote/mid exists.
- `conversions = 0` for all bots.

## Shared State And Runtime

- `traderData` stores compact JSON with fields such as IPR day-start, ACO EMA, last mid, counters, or alert counts.
- Imports allowed: `json`, `math` if needed, `datamodel.Order`, `datamodel.TradingState`.
- Runtime target: O(number of visible book levels), well under platform limits.
- No external libraries and no in-bot training.

## Bot-Specific Execution Logic

### `bot_01` Baseline FV Combo

- IPR: estimate `ipr_day_start = first_valid_mid - 0.001*timestamp`; trade around `FV = ipr_day_start + 0.001*timestamp`.
- ACO: use `FV = 10000`.
- Buy: sweep asks below `FV - buffer`; rest bid near FV adjusted for inventory if spread allows.
- Sell: sweep bids above `FV + buffer`; rest ask near FV adjusted for inventory if spread allows.
- Risk: moderate order sizes and max effective position below hard limit.

### `bot_02` Carry Tight MM

- IPR: target +80 long; sweep all asks up to capacity and post remaining bid at `best_bid + 1`.
- ACO: tight FV market maker with stronger inventory skew; sweep favorable levels and post full-capacity quotes.
- Risk: intentionally high IPR directional exposure; relies on historical positive drift.

### `bot_03` Microstructure Scalper

- IPR and ACO: compute FV, best-quote edge, spread, L1/L3 imbalance.
- Buy when ask edge is positive enough or imbalance strongly favors upward residual correction.
- Sell when bid edge is positive enough or imbalance strongly favors downward residual correction.
- Passive quotes only when both sides exist and price remains favorable against FV.
- Risk: smaller order sizes, stricter edge thresholds, skip low-quality books.

### `bot_04` ACO Markov Overlay

- IPR: baseline drift FV MM.
- ACO: bucket residual around 10000 and use hardcoded expected next residual delta.
- Buy when state expected delta is positive and ask is sufficiently cheap to FV plus expected delta.
- Sell when state expected delta is negative and bid is sufficiently rich to FV plus expected delta.
- Risk: ignore deep sparse buckets except as capped directional hints.

### `bot_05` Hybrid Adaptive Model

- IPR: blend drift FV with microstructure score; reduce exposure when residual or spread is abnormal.
- ACO: maintain EMA around 10000; switch from fixed FV toward EMA only after sustained deviation; add light residual/imbalance score.
- Execution: more complex scoring and quote placement; may combine sweep and passive orders.
- Risk: defensive caps, anomaly counters, no automatic full trust in adaptive FV until sustained evidence.

## Expected Failure Cases

- IPR slope or intercept breaks: baseline/carry variants may lose; hybrid should reduce exposure.
- ACO fixed FV shifts: fixed variants may lose; Markov/adaptive variants should perform better.
- Microstructure features overfit bid-ask bounce: scalper/linear variants may overtrade.
- One-sided books: bots must quote only the side they can reason about or skip safely.
- Position-limit rejection: prevented by aggregate capacity clipping.

## Validation Plan

- Contract checks: `Trader.run(state)` returns `(result, conversions, traderData)`; `result` maps symbols to order lists.
- Static checks: Python compile, no unsupported imports, no interface changes.
- Order checks: positive buy quantities, negative sell quantities, aggregate capacity within +/-80.
- Performance checks: compare all five bots on the same historical days; record total PnL, PnL by product, max absolute position, order count, and limit breaches if runner supports it.
- Promotion rule: after validation, promote best 1-2 bots to active implementations; archive or keep the rest as experimental references.

## Implementation Handoff

- Owner/member: `noel`.
- Target folder: `rounds/round_1/bots/noel/canonical/`.
- Implement five self-contained files listed in the bot matrix.
- Known caveats: this spec is optimized for fast performance exploration; validation decides what survives.
