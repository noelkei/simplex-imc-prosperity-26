# Strategy Spec: Round 3 Learning Batch Wave 1

## Status

`deferred under deadline`

## Objective

Implement a learning-first batch of isolated or near-isolated learner bots so
we can map the Round 3 signal surface by product, strike family, and local
combination. This batch is **not** trying to submit the best global composite
yet. It is trying to answer:

- which product branches really have live `TTE=5d` edge,
- which strikes or subsets are helping versus hurting,
- which failures are signal failures versus execution failures,
- which branches deserve later composite reintegration.

## Source Evidence

- [`../03_strategy_candidates.md`](../03_strategy_candidates.md)
- [`../03_signal_strategy_learning_matrix.md`](../03_signal_strategy_learning_matrix.md)
- [`../02_understanding.md`](../02_understanding.md)
- [`../01_eda/eda_option_surface_and_microstructure.md`](../01_eda/eda_option_surface_and_microstructure.md)
- [`../post_run_research_memory.md`](../post_run_research_memory.md)
- [`../06_testing/round_3_historical_performance_analysis.md`](../06_testing/round_3_historical_performance_analysis.md)
- [`../06_testing/round_3_canonical_run_analysis.md`](../06_testing/round_3_canonical_run_analysis.md)
- [`../06_debugging/issue_2026-04-25_active_voucher_strike_misallocation.md`](../06_debugging/issue_2026-04-25_active_voucher_strike_misallocation.md)

## Batch Scope

- Batch size cap: `25`
- Owner: `amin`
- Intent: `learning / validation / pruning`
- Promotion target: none yet

## Strategy Families Covered

| Family | Products | Why Included |
| --- | --- | --- |
| Delta-1 reversion / imbalance learners | `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT` | live microstructure still exists but HYDRO execution is unresolved |
| ITM voucher residual learners | `VEV_4000`, `VEV_4500` | strongest live and historical residual family |
| Active voucher strike learners | `VEV_5000-5300` subsets | current composites fail mainly because the basket is too broad and `VEV_5200` dominates losses |
| Upper voucher learners | `VEV_5400`, `VEV_5500` | live logger reopened them |
| Surface pair learners | adjacent voucher pairs | current evidence suggests local relative-value may be cleaner than broad basket residuals |
| VEX plus selected voucher subset | `VELVETFRUIT_EXTRACT` + best strike subsets | historical and current evidence both say VEX is a positive leg |

## Feature Contract

### F01 Delta-1 Mid Reversion

- Source fields: top-of-book best bid / ask, mid, current position.
- Online proxy: previous mid stored in `traderData`.
- Role: primary signal for `HYDRO` and `VEX` reversion learners.
- Missing-data fallback: stay idle for that product.
- Validation check: product PnL split and live signal diagnostics.

### F02 Delta-1 Imbalance

- Source fields: top-of-book best bid / ask volume.
- Online proxy: top-level imbalance computed each iteration.
- Role: primary signal for imbalance learners, supporting lean elsewhere.
- Missing-data fallback: use zero lean.
- Validation check: product PnL split versus imbalance-led learners.

### F03 Centered Intrinsic / Extrinsic Residual

- Source fields: VEX mid, voucher mid, strike.
- Online proxy: `voucher_mid - intrinsic_value` minus slow EMA anchor in `traderData`.
- Role: primary signal for ITM, active, and upper voucher learners in this batch.
- Missing-data fallback: stay idle on that strike.
- Validation check: per-strike PnL, final position, and live residual diagnostics.

### F04 VEX Sidecar

- Source fields: VEX book only.
- Online proxy: same delta-1 learner logic as standalone VEX bots.
- Role: supporting sidecar for selected ITM / voucher combo learners.
- Missing-data fallback: run voucher branch only.
- Validation check: whether combo bot beats the isolated voucher branch or simply inherits VEX PnL.

### F05 Inventory Skew

- Source fields: current position, per-product limit.
- Online proxy: linear inventory penalty in quote fair value.
- Role: supporting risk overlay for one clean active-subset learner only.
- Missing-data fallback: zero skew.
- Validation check: compare to same subset without the skew overlay.

### F06 Passive Upper-Strike Quoting

- Source fields: upper-strike best bid / ask and current position.
- Online proxy: best-book passive one-tick quoting with bounded inventory.
- Role: primary execution style for the passive upper learner.
- Missing-data fallback: stay idle.
- Validation check: compare to the upper residual learner family.

### F07 Surface Pair Spread EMA

- Source fields: VEX mid plus voucher mids for two adjacent strikes.
- Online proxy: EMA anchor of the pairwise extrinsic spread.
- Role: primary signal for the two surface relative-value learners.
- Missing-data fallback: stay idle if either leg is missing.
- Validation check: pair-level PnL and whether the spread learner avoids the `VEV_5200` directional failure mode.

## Round-Specific Mechanics Contract

- Round products and limits: `HYDROGEL_PACK` / `VELVETFRUIT_EXTRACT` limit `200`; each voucher limit `300`.
- Live expiry regime: confirmed `TTE=5d`.
- Voucher universe kept in coverage: `VEV_4000` to `VEV_6500`.
- This batch intentionally excludes `VEV_6000/6500` from active trading logic.
- No conversions are used.
- `Trader.run(state)` returns `result, conversions, traderData`.
- Only supported stdlib imports are allowed.

## Bot Batch

The implemented bots are:

- `L01` hydro reversion
- `L02` hydro imbalance
- `L04` vex reversion
- `L05` vex imbalance
- `L06` dual delta-1 combo
- `L07` itm 4000 residual
- `L08` itm 4500 residual
- `L09` itm pair residual
- `L10` itm pair plus vex
- `L12` active 5000 residual
- `L13` active 5100 residual
- `L14` active 5200 residual
- `L15` active 5300 residual
- `L16` active 5000 + 5300 residual
- `L17` active 5100 + 5300 residual
- `L18` active 5200 + 5300 residual
- `L19` active 5000 + 5100 + 5300 residual
- `L20` active 5000 + 5300 inventory
- `L21` upper 5400 residual
- `L22` upper 5500 residual
- `L23` upper 5400 + 5500 residual
- `L24` upper 5400 + 5500 passive
- `L25` vex + 5300 combo
- `L26` surface 5200 / 5300 relative value
- `L27` surface 5300 / 5400 relative value

## Variant Rules

- Each learner changes one practical axis: product scope, strike subset, signal mode, execution mode, or inventory overlay.
- No learner is allowed to drift into a broad full-round composite.
- Broad active-voucher baskets should not be reopened in this batch unless they explicitly exclude the known failure strike `VEV_5200`.
- `VEV_6000/6500` remain off the active trading path unless a later live artifact contradicts the floor regime.

## Expected Decisions This Batch Should Unlock

- Keep or prune HYDRO as a future sidecar.
- Keep or prune `VEV_5200`.
- Decide whether the active branch should center on `VEV_5300` and upper strikes instead of `VEV_5000-5300` together.
- Decide whether ITM should replace active vouchers as the next primary wave.
- Decide whether surface-pair learners deserve a second wave.

## Validation Plan

- Rank by real platform PnL from JSON `profit`.
- Use final `activitiesLog` per-product rows for attribution.
- Compare learners primarily against:
  - other learners in the same family,
  - the live logger market metrics,
  - historical best learner `r3_b02_itm_residual`,
  - current failed challengers `candidate_c06_v01_centered_base` and `candidate_c06_composite_inv`.

## Falsification Rules

- If HYDRO isolated learners still fail, downgrade HYDRO from future composites.
- If `VEV_5200` isolated or paired learners still fail, remove it from active voucher composites.
- If `VEV_5400/5500` learners do not monetize despite live movement and tight spreads, re-close the upper branch.
- If ITM learners still outperform everything else, promote ITM from backlog to primary wave.
