# Round 1 Noel Submission Manifest

## Purpose

Deployable Round 1 bot files and final selection notes for Noel's current Prosperity platform tests. Each `.py` file is self-contained and implements `Trader.run(state)`.

## Common Baseline

- IPR: target `+80` carry layer.
- ACO: one strategy family per bot.
- Limits: `+/-80` per product.
- Current high-ROI linked spec: `../../../workspace/04_strategy_specs/spec_high_roi_3_variant_batch.md`
- Threshold refinement spec: `../../../workspace/04_strategy_specs/spec_candidate_27_28_threshold_refinements.md`
- Current high-ROI local replay summary: `../../../performances/noel/canonical/run_20260417_high_roi_variant_replay_summary.md`
- Promotion score: platform JSON `profit`; local replay is only a sanity check.

## Current Upload Decision

Upload `candidate_26_v3_a3b1_one_sided_exit_overlay.py` as the final recommended file. `candidate_28` is the closest backup, but it did not beat the incumbent on platform PnL. `candidate_27` is rejected for final upload.

| Candidate | File | Strategy Role | Platform Test Priority |
| --- | --- | --- | --- |
| `candidate_26` | `candidate_26_v3_a3b1_one_sided_exit_overlay.py` | Current platform leader: A3+B1 one-sided exit and book-state overlay | final upload |
| `candidate_28` | `../historical/candidate_28_v1_c26_strict_one_sided.py` | C26 threshold refinement: stricter one-sided overlay | backup only |
| `candidate_27` | `../historical/candidate_27_v1_c26_soft_flatten.py` | C26 threshold refinement: earlier soft ACO flatten | rejected |

## Historical Controls Included In Replay

These controls are stored under `../historical/` in the pulled tree and are not the current canonical upload set.

| Candidate | Historical File | Strategy Role |
| --- | --- | --- |
| `candidate_10` | `../historical/candidate_10_bot02_carry_tight_mm.py` | A1+B1 control / prior >10k baseline |
| `candidate_24` | `../historical/candidate_24_v1_a1b1_size_skew_refine.py` | A1+B1 ACO size/skew refinement |
| `candidate_25` | `../historical/candidate_25_v2_a2b1_conservative_regime_gate.py` | A2+B1 conservative residual-regime gate |

## Platform Ranking

This ranking uses platform JSON `profit` and final `activitiesLog` product PnL.

| Rank | Candidate | Total PnL | IPR PnL | ACO PnL | Final ACO | Decision |
| ---: | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `candidate_26` | 10090.46875 | 7286.0 | 2804.46875 | 9 | promote |
| 2 | `candidate_28` | 10076.3125 | 7286.0 | 2790.3125 | 6 | backup |
| 3 | `candidate_10` | 10007.0 | 7286.0 | 2721.0 | 0 | robust fallback |
| 7 | `candidate_27` | 9920.1875 | 7286.0 | 2634.1875 | 10 | reject |

## High-ROI Local Replay Ranking

This ranking is immediate-fill sanity evidence only, not official Prosperity PnL.

| Rank | Bot | Total Replay PnL | IPR Replay PnL | ACO Replay PnL | Rejections | Errors |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | `candidate_27_v1_c26_soft_flatten.py` | 249079.00 | 238054.00 | 11025.00 | 0 | 0 |
| 2 | `candidate_26_v3_a3b1_one_sided_exit_overlay.py` | 248251.00 | 238054.00 | 10197.00 | 0 | 0 |
| 3 | `candidate_28_v1_c26_strict_one_sided.py` | 248105.00 | 238054.00 | 10051.00 | 0 | 0 |
| 4 | `candidate_25_v2_a2b1_conservative_regime_gate.py` | 247946.00 | 238054.00 | 9892.00 | 0 | 0 |
| 5 | `candidate_24_v1_a1b1_size_skew_refine.py` | 247631.00 | 238054.00 | 9577.00 | 0 | 0 |
| 6 | `candidate_10_bot02_carry_tight_mm.py` | 247628.00 | 238054.00 | 9574.00 | 0 | 0 |

## Previous Next-Wave Bot Files

The broader `candidate_14` through `candidate_23` next-wave files are now historical comparison artifacts in the pulled tree. The current upload set above is the tighter high-ROI batch.

## Platform Ranking Procedure

After platform runs exist, rank by JSON `profit`, then use final `activitiesLog` product rows for IPR/ACO split. Rerun:

```bash
python3 rounds/round_1/performances/noel/canonical/analyze_platform_artifacts.py
```
