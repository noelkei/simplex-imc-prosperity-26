# Round 3 Historical Performance Analysis

## Executive Verdict

Historical Round 3 platform artifacts already teach us a lot before we run the two corrected canonical challengers.

- Best tested historical artifact: `r3_b02_itm_residual.json` with real platform PnL `1409.371`.
- Best tested branch so far: **VEX + ITM voucher residual** (`r3_b02_itm_residual`, then `r3_b02_itm_anchor`).
- Weakest current branch: **HYDRO online implementations**. HYDRO is negative in every nonzero tested run.
- Main active-voucher problem in historical bots: losses cluster in `VEV_5000-5200`, while `VEV_5300` stays positive and several bots finish max short across all active strikes.
- Validation heuristic now calibrated: the final per-product `activitiesLog` rows reconstruct total PnL exactly; `graphLog` is only an audit proxy.

## Artifact Audit And PnL Proxy Calibration

Real platform PnL source for these historical artifacts is JSON `profit`. For future cases where `profit` is missing but `activitiesLog` exists, the best proxy is:

1. Sum of the final per-product `profit_and_loss` values from `activitiesLog`.
2. Use `graphLog` only as a weak audit proxy.

Calibration on the 11 historical Round 3 JSONs:

- `activitiesLog` final-sum delta vs JSON `profit`: exact `0.0` in every artifact.
- `graphLog` final value median absolute delta vs JSON `profit`: `129.728` mean absolute delta, `124.541` median absolute delta, max `344.146`.

## Ranking By Real Platform PnL

| short_id | file | profit | delta1_total | itm_total | active_total | max_drawdown |
| --- | --- | --- | --- | --- | --- | --- |
| B02-resid | r3_b02_itm_residual.json | 1409.371 | 1211.906 | 197.464 | 0.000 | -5305.212 |
| B02-anchor | r3_b02_itm_anchor.json | 726.893 | 599.500 | 127.393 | 0.000 | -446.278 |
| B06-tte | r3_b06_tte_cautious.json | -752.886 | 599.500 | 0.000 | -1352.386 | -18404.141 |
| B07-hedge | r3_b07_delta_hedge.json | -1275.997 | -1022.434 | 0.000 | -253.563 | -15035.053 |
| B08-regime | r3_b08_regime_composite.json | -1501.925 | 599.500 | 0.000 | -2101.425 | -27684.946 |
| C06-legacy | candidate_c06_composite_base.json | -1631.925 | 599.500 | 0.000 | -2231.425 | -27684.946 |
| B03-pure | r3_b03_voucher_pure.json | -2261.849 | 0.000 | 0.000 | -2261.849 | -21413.080 |
| B04-surf | r3_b04_full_surface.json | -2561.846 | 599.500 | 318.797 | -3281.120 | -27072.923 |
| B01-base | r3_b01_delta1_baseline.json | -6414.711 | -6414.711 | 0.000 | 0.000 | -16460.062 |
| B01-opt | r3_b01_delta1_optiver.json | -20402.156 | -20402.156 | 0.000 | 0.000 | -22469.750 |
| B05-adv | r3_b05_composite_advanced.json | -25333.769 | -22856.344 | 0.000 | -2477.425 | -32426.994 |

## Bucket Attribution

`delta1_total = HYDROGEL + VEX`, `itm_total = VEV_4000 + VEV_4500`, `active_total = VEV_5000-5300`, `upper_total = VEV_5400 + VEV_5500`.

| short_id | profit | delta1_total | itm_total | active_total | upper_total | max_drawdown | active_short_saturation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B02-resid | 1409.371 | 1211.906 | 197.464 | 0.000 | 0.000 | -5305.212 | 0 |
| B02-anchor | 726.893 | 599.500 | 127.393 | 0.000 | 0.000 | -446.278 | 0 |
| B06-tte | -752.886 | 599.500 | 0.000 | -1352.386 | 0.000 | -18404.141 | 3 |
| B07-hedge | -1275.997 | -1022.434 | 0.000 | -253.563 | 0.000 | -15035.053 | 3 |
| B08-regime | -1501.925 | 599.500 | 0.000 | -2101.425 | 0.000 | -27684.946 | 4 |
| C06-legacy | -1631.925 | 599.500 | 0.000 | -2231.425 | 0.000 | -27684.946 | 4 |
| B03-pure | -2261.849 | 0.000 | 0.000 | -2261.849 | 0.000 | -21413.080 | 0 |
| B04-surf | -2561.846 | 599.500 | 318.797 | -3281.120 | -199.023 | -27072.923 | 3 |
| B01-base | -6414.711 | -6414.711 | 0.000 | 0.000 | 0.000 | -16460.062 | 0 |
| B01-opt | -20402.156 | -20402.156 | 0.000 | 0.000 | 0.000 | -22469.750 | 0 |
| B05-adv | -25333.769 | -22856.344 | 0.000 | -2477.425 | 0.000 | -32426.994 | 4 |

Interpretation:

- The two positive bots are ITM/VEX families.
- Delta-1-only families are negative, especially the Optiver-style stack.
- Historical active-voucher families mostly lose through the lower active strikes and end heavily short.
- The corrected centered-residual challenger is still worth running because these historical bots mostly tested raw or differently tuned residual families, not the new centered implementation.

## Active Voucher Strike Attribution

| short_id | VEV_5000 | VEV_5100 | VEV_5200 | VEV_5300 |
| --- | --- | --- | --- | --- |
| B01-base | 0.000 | 0.000 | 0.000 | 0.000 |
| B01-opt | 0.000 | 0.000 | 0.000 | 0.000 |
| B02-anchor | 0.000 | 0.000 | 0.000 | 0.000 |
| B02-resid | 0.000 | 0.000 | 0.000 | 0.000 |
| B03-pure | -1304.062 | -525.648 | -519.322 | 87.185 |
| B04-surf | -1935.734 | -724.707 | -701.262 | 80.583 |
| B05-adv | -1132.039 | -724.707 | -701.262 | 80.583 |
| B06-tte | -7.000 | -724.707 | -701.262 | 80.583 |
| B07-hedge | -839.178 | 121.293 | 383.738 | 80.583 |
| B08-regime | -756.039 | -724.707 | -701.262 | 80.583 |
| C06-legacy | -886.039 | -724.707 | -701.262 | 80.583 |

Key pattern:

- `VEV_5000` is negative in `7/7` tested active-voucher runs.
- `VEV_5100` is negative in `6/7`.
- `VEV_5200` is negative in `6/7`.
- `VEV_5300` is positive in `7/7`.

This is the clearest reason to test a subset variant that excludes `VEV_5000` before we assume the entire active-voucher branch is bad.

## Spread Diagnostics From Platform-Style Logs

| product | spread_mean | spread_median | pct_spread_le_4 | pct_spread_le_8 | pct_spread_le_12 | pct_spread_le_20 |
| --- | --- | --- | --- | --- | --- | --- |
| HYDROGEL_PACK | 15.645 | 16.000 | 0.000 | 0.033 | 0.040 | 1.000 |
| VELVETFRUIT_EXTRACT | 4.983 | 5.000 | 0.083 | 1.000 | 1.000 | 1.000 |
| VEV_4000 | 20.973 | 21.000 | 0.000 | 0.000 | 0.021 | 0.024 |
| VEV_4500 | 16.081 | 16.000 | 0.000 | 0.014 | 0.021 | 1.000 |
| VEV_5000 | 6.231 | 6.000 | 0.021 | 1.000 | 1.000 | 1.000 |
| VEV_5100 | 4.444 | 4.000 | 0.519 | 1.000 | 1.000 | 1.000 |
| VEV_5200 | 2.984 | 3.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| VEV_5300 | 2.171 | 2.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| VEV_5400 | 1.419 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| VEV_5500 | 1.169 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| VEV_6000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| VEV_6500 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

What this changes:

- HYDRO top-of-book spreads are much wider than VEX in platform-style logs, which weakens trust in the current HYDRO online implementation.
- VEX still looks tradable.
- `VEV_5000-5300` are not obviously failing just because spreads are too wide.
- `VEV_5400/5500` look much tighter here than the raw-day EDA suggested; that contradiction should trigger targeted validation, not blind promotion.

## Signal And Bot Coverage Matrix

| candidate_id | strategy | products | isolated_bot_exists | tested_json_exists | current_active_bot | gap_or_next_probe |
| --- | --- | --- | --- | --- | --- | --- |
| C01 | HYDROGEL microstructure MM | HYDROGEL_PACK | no | partial only (never hydro-only) | none isolated | missing hydro-only learner; current evidence says hydro is weak/negative in the tested combined implementations |
| C02 | VEX delta-1 MM + voucher anchor | VELVETFRUIT_EXTRACT | no | partial only (never vex-only) | none isolated | missing vex-only learner despite VEX being the strongest tested delta-1 leg |
| C03 | Active-voucher centered residual reversion | VEV_5000-5300 | yes | yes for legacy/raw family; no for current centered challenger | candidate_c06_v01_centered_base.py | run the centered challenger; historical raw family lost money and saturated shorts, especially in VEV_5000-5200 |
| C04 | Active-voucher residual + inventory skew + imbalance | VEV_5000-5300 | no | no clean C04 run yet | candidate_c06_composite_inv.py | run the clean inventory challenger; current historical evidence says short saturation is a real issue |
| C05 | ITM structural-anchor residual | VEV_4000-4500 | partial | yes | none | historical best tested family; worth a fresh learning variant or spec promotion |
| C06 | Full composite trader | HYDROGEL + VEX + VEV_5000-5300 | not applicable | yes for legacy/alternate composite families | candidate_c06_v01_centered_base.py | current centered base still needs its first run; hydro and VEV_5000 behavior remain the biggest composite risks |
| C07 | TTE-cautious active-voucher residual | VEV_5000-5300 | no | yes | none | historical cautious bot still lost; keep as calibration branch, not as current default |
| D01 | No-trade diagnostic state logger | all round_3 products | yes | no | baseline_state_logger.py | run only for state/log collection; use for diagnostics, never for alpha |

Counts from the current repo state:

- Formal strategy candidates in the Round 3 strategy artifact: `7` (`C01` to `C07`).
- Underlying non-composite signal families: `6` (`C01`-`C05` + `C07`; `C06` is the composite wrapper).
- Implemented Round 3 bot files now relevant to learning: `14` total.
  - `11` historical tested bots with paired JSONs.
  - `2` current canonical challengers.
  - `1` diagnostic no-trade state logger.

## What We Have Not Tested Cleanly Yet

- No **HYDRO-only** learner bot.
- No **VEX-only** learner bot.
- No clean **C04 inventory** run yet.
- No fresh run yet for the corrected **centered-residual base**.
- No **upper-strike-only (`VEV_5400/5500`)** learner bot.
- No **pure ITM-only** bot without any VEX/delta-1 support.

## Recommended Next Iterations

These next runs are for **learning signal behavior**, not for picking the final global champion immediately.

| idea_id | type | idea | why | priority |
| --- | --- | --- | --- | --- |
| R3-NEXT-01 | diagnostic | Run baseline_state_logger first if we need richer per-iteration state/trade logs. | Historical JSONs give book/PnL, but not enough detail about trade events, own fills, or exact state transitions. | high |
| R3-NEXT-02 | validation | Run candidate_c06_v01_centered_base against the historical legacy base. | Historical active-voucher runs weaken raw residual implementations but strengthen the case for the corrected centered-residual challenger. | high |
| R3-NEXT-03 | validation | Run candidate_c06_composite_inv after the centered base. | Historical active-voucher runs repeatedly hit short saturation; the clean inventory variant directly tests that risk control. | high |
| R3-NEXT-04 | learning variant | Create a hydro-only learner and a vex-only learner. | We still do not have isolated online evidence for C01 or C02; current data only tests them in pairs or composites. | high |
| R3-NEXT-05 | learning variant | Reopen ITM residual as a near-term learner/follow-up. | The only positive tested family is ITM/VEX, led by r3_b02_itm_residual (+1409.371) and r3_b02_itm_anchor (+726.893). | high |
| R3-NEXT-06 | learning variant | Test an active-voucher subset without VEV_5000 (for example VEV_5100-5300 or VEV_5200-5300). | VEV_5000 was negative in 7/7 tested runs; VEV_5300 was positive in 7/7. | medium/high |
| R3-NEXT-07 | targeted EDA + variant | Recheck VEV_5400/5500 with platform-style evidence before discarding them. | Historical activitiesLog spreads look tight there, which contradicts the raw-day EDA; however the one full-surface run still lost money. | medium |

## Bottom Line

Before new uploads, the historical JSONs already tell us:

1. The best exact PnL proxy from platform-style artifacts is the final `activitiesLog` product sum, not `graphLog`.
2. ITM/VEX residual logic is the strongest tested family so far.
3. HYDRO is the weakest current online branch and should not be trusted without an isolated learner.
4. Raw active-voucher families underperform mainly through `VEV_5000-5200` and short saturation, which is exactly why the new centered and inventory-clean challengers are still worth testing.

## Artifacts

- [`artifacts/historical_run_metrics.csv`](artifacts/historical_run_metrics.csv)
- [`artifacts/historical_product_attribution.csv`](artifacts/historical_product_attribution.csv)
- [`artifacts/historical_spread_diagnostics.csv`](artifacts/historical_spread_diagnostics.csv)
- [`artifacts/historical_signal_coverage.csv`](artifacts/historical_signal_coverage.csv)
- [`artifacts/historical_next_backlog.csv`](artifacts/historical_next_backlog.csv)
- [`artifacts/historical_profit_ranking.png`](artifacts/historical_profit_ranking.png)
- [`artifacts/historical_bucket_attribution.png`](artifacts/historical_bucket_attribution.png)
- [`artifacts/historical_active_voucher_pnl.png`](artifacts/historical_active_voucher_pnl.png)
- [`artifacts/historical_graph_trajectories.png`](artifacts/historical_graph_trajectories.png)

## Handoff

- This report is decision-supporting evidence, not official Prosperity truth.
- Next useful work is:
  1. optional diagnostic logger run for richer state logs,
  2. first run of `candidate_c06_v01_centered_base.py`,
  3. first run of `candidate_c06_composite_inv.py`,
  4. then isolated learning variants for HYDRO, VEX, and ITM / strike selection.
