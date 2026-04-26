# Round 3 Canonical Run Analysis

## Executive Verdict

The first two corrected challengers did **not** beat the historical reference.

- `candidate_c06_v01_centered_base.json` finished at `-3008.203`.
- `candidate_c06_composite_inv.json` finished at `-5245.475`.
- Historical frozen C06 legacy reference remains better at `-1631.925`.
- Historical best overall learner still remains `r3_b02_itm_residual.json` at `1409.371`.

The main failure mode is now much clearer than before:

- both corrected challengers lose almost entirely through the active voucher bucket,
- `VEV_5200` is the dominant losing strike in both runs,
- `VEV_5300` stays positive,
- `VEX` stays positive,
- inventory skew did **not** rescue the active-voucher branch on this live run.

## Current Canonical Run Ranking

| short_id | file | profit | delta1_total | itm_total | active_total | max_drawdown |
| --- | --- | --- | --- | --- | --- | --- |
| D01-logger | baseline_state_logger.json | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| C06-base-v01 | candidate_c06_v01_centered_base.json | -3008.203 | 599.500 | 0.000 | -3607.703 | -4154.039 |
| C06-inv-v01 | candidate_c06_composite_inv.json | -5245.475 | 599.500 | 0.000 | -5844.975 | -5393.154 |

## Product Attribution

### Centered Base

| product | profit_and_loss | final_position |
| --- | --- | --- |
| VEV_5200 | -4040.363 | 270 |
| VEV_5100 | -110.790 | -10 |
| HYDROGEL_PACK | -0.809 | 4 |
| VEV_4000 | 0.000 | 0 |
| VEV_4500 | 0.000 | 0 |
| VEV_5400 | 0.000 | 0 |
| VEV_5500 | 0.000 | 0 |
| VEV_6000 | 0.000 | 0 |
| VEV_6500 | 0.000 | 0 |
| VEV_5000 | 45.628 | 8 |
| VEV_5300 | 497.822 | -224 |
| VELVETFRUIT_EXTRACT | 600.309 | 4 |

### Inventory Variant

| product | profit_and_loss | final_position |
| --- | --- | --- |
| VEV_5200 | -6058.820 | 114 |
| VEV_5100 | -218.538 | -22 |
| HYDROGEL_PACK | -0.809 | 4 |
| VEV_4000 | 0.000 | 0 |
| VEV_4500 | 0.000 | 0 |
| VEV_5400 | 0.000 | 0 |
| VEV_5500 | 0.000 | 0 |
| VEV_6000 | 0.000 | 0 |
| VEV_6500 | 0.000 | 0 |
| VEV_5000 | 48.814 | 4 |
| VEV_5300 | 383.569 | -70 |
| VELVETFRUIT_EXTRACT | 600.309 | 4 |

## Immediate Run Findings

- The centered base ended with `VEV_5200 = +270` and `VEV_5300 = -224`; the loss profile suggests the signal is over-allocating into `VEV_5200`.
- The inventory variant reduced the terminal `VEV_5200` position to `+114`, but still lost more money than the base, so the current C04 overlay looks like an execution/risk penalty rather than a rescue.
- Neither corrected run generated meaningful PnL in ITM or upper strikes because those products were not part of the active logic.
- The logger run confirms the market data itself is usable and reconstructs a full live-day book path with zero trading interference.

## Live-Day Market Metrics From The State Logger

The logger is useful because it gives us a clean live Round 3 book sample under confirmed `TTE=5d`.

| product | spread_mean | spread_median | mid_std | unique_mids | pct_spread_le_2 | pct_spread_le_4 | pct_spread_le_8 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HYDROGEL_PACK | 15.645 | 16.000 | 29.697 | 158 | 0.000 | 0.000 | 0.033 |
| VELVETFRUIT_EXTRACT | 4.983 | 5.000 | 7.520 | 66 | 0.045 | 0.083 | 1.000 |
| VEV_4000 | 20.973 | 21.000 | 7.555 | 66 | 0.000 | 0.000 | 0.000 |
| VEV_4500 | 16.081 | 16.000 | 7.543 | 66 | 0.000 | 0.000 | 0.014 |
| VEV_5000 | 6.231 | 6.000 | 7.182 | 63 | 0.004 | 0.021 | 1.000 |
| VEV_5100 | 4.444 | 4.000 | 6.362 | 59 | 0.013 | 0.519 | 1.000 |
| VEV_5200 | 2.984 | 3.000 | 4.916 | 45 | 0.056 | 1.000 | 1.000 |
| VEV_5300 | 2.171 | 2.000 | 3.355 | 30 | 0.818 | 1.000 | 1.000 |
| VEV_5400 | 1.419 | 1.000 | 1.567 | 15 | 1.000 | 1.000 | 1.000 |
| VEV_5500 | 1.169 | 1.000 | 0.667 | 7 | 1.000 | 1.000 | 1.000 |
| VEV_6000 | 1.000 | 1.000 | 0.000 | 1 | 1.000 | 1.000 | 1.000 |
| VEV_6500 | 1.000 | 1.000 | 0.000 | 1 | 1.000 | 1.000 | 1.000 |

What changes from this live view:

- `VEV_6000` and `VEV_6500` are still completely frozen at `0.5`.
- `VEV_5400` and especially `VEV_5500` are active enough to justify learning bots.
- `HYDROGEL_PACK` still has wide spreads, so any HYDRO bot must be execution-sensitive.
- `VELVETFRUIT_EXTRACT` remains the cleanest live delta-1 product.

## Live-Day Microstructure Signal Check

| product | imbalance_corr_fut_delta | mid_reversion_corr | mid_delta_acf1 |
| --- | --- | --- | --- |
| HYDROGEL_PACK | 0.374 | -0.143 | -0.143 |
| VELVETFRUIT_EXTRACT | 0.313 | -0.172 | -0.172 |
| VEV_4000 | 0.468 | -0.286 | -0.286 |
| VEV_4500 | 0.381 | -0.197 | -0.197 |
| VEV_5000 | 0.164 | -0.055 | -0.055 |
| VEV_5100 | 0.146 | -0.047 | -0.047 |
| VEV_5200 | 0.320 | -0.114 | -0.114 |
| VEV_5300 | 0.377 | -0.140 | -0.140 |
| VEV_5400 | 0.219 | -0.180 | -0.180 |
| VEV_5500 | 0.298 | -0.215 | -0.215 |
| VEV_6000 |  |  |  |
| VEV_6500 |  |  |  |

Interpretation:

- HYDRO and VEX both still show live reversion plus useful top-of-book imbalance.
- ITM vouchers (`VEV_4000`, `VEV_4500`) have stronger live reversion than the active strikes.
- `VEV_5300`, `VEV_5400`, and `VEV_5500` look more promising than `VEV_5100`/`VEV_5200`.

## Live-Day Voucher Residual Check

Using a simple intrinsic anchor against live `VELVETFRUIT_EXTRACT` mids:

| product | strike | extrinsic_mean | extrinsic_std | resid_reversion_corr | unique_mid |
| --- | --- | --- | --- | --- | --- |
| VEV_4000 | 4000 | 0.012 | 0.898 | -0.445 | 66 |
| VEV_4500 | 4500 | 0.011 | 0.817 | -0.361 | 66 |
| VEV_5000 | 5000 | 3.216 | 0.650 | -0.068 | 63 |
| VEV_5100 | 5100 | 12.403 | 1.260 | 0.020 | 59 |
| VEV_5200 | 5200 | 38.908 | 2.658 | 0.019 | 45 |
| VEV_5300 | 5300 | 50.056 | 3.355 | -0.078 | 30 |
| VEV_5400 | 5400 | 16.020 | 1.567 | -0.090 | 15 |
| VEV_5500 | 5500 | 6.340 | 0.667 | -0.135 | 7 |
| VEV_6000 | 6000 | 0.500 | 0.000 |  | 1 |
| VEV_6500 | 6500 | 0.500 | 0.000 |  | 1 |

Interpretation:

- The strongest live residual reversion remains in `VEV_4000` / `VEV_4500`.
- `VEV_5000` is weak but still directionally mean-reverting.
- `VEV_5100` and `VEV_5200` are weak to non-reverting on this live day.
- `VEV_5300` is still tradable but less clean than the ITM branch.
- `VEV_5400` / `VEV_5500` are now real candidates for targeted probes, not just monitoring.

## Decision-Relevant Takeaways

1. The active-voucher batch should stop treating `VEV_5000-5300` as one homogeneous family.
2. `VEV_5200` is now the main do-not-trust strike until an isolated learner proves otherwise.
3. `VEV_4000` / `VEV_4500` should move up sharply in the learner queue.
4. `VEV_5400` / `VEV_5500` deserve their own live probes because the logger confirms movement plus tight spreads.
5. `HYDRO` still needs an isolated learner; the live signal exists, but the historical execution has been poor.

## Recommended Bot Families After These Runs

- Isolated HYDRO learners: signal exists, execution still unproven.
- Isolated VEX learners: positive leg, clean microstructure, strong anchor role.
- ITM residual learners: strongest live and historical signal family.
- Active-voucher subset learners: especially `5000`, `5300`, and pair/subset variants that exclude `5200`.
- Upper-strike learners: `5400`, `5500`, and `5400/5500` passive or residual variants.
- Surface relative-value learners: especially `5200/5300` and `5300/5400`.

## Artifacts

- [`artifacts/canonical_runs/canonical_run_metrics.csv`](artifacts/canonical_runs/canonical_run_metrics.csv)
- [`artifacts/canonical_runs/canonical_product_attribution.csv`](artifacts/canonical_runs/canonical_product_attribution.csv)
- [`artifacts/canonical_runs/live_market_metrics.csv`](artifacts/canonical_runs/live_market_metrics.csv)
- [`artifacts/canonical_runs/live_signal_metrics.csv`](artifacts/canonical_runs/live_signal_metrics.csv)
- [`artifacts/canonical_runs/live_option_residual_metrics.csv`](artifacts/canonical_runs/live_option_residual_metrics.csv)
