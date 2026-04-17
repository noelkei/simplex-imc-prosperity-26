# High-ROI Threshold Variant Immediate-Fill Replay

## Method

- This is a local sanity replay, not official Prosperity PnL.
- It models immediate fills against visible sample books only.
- Resting orders that platform bots may hit later are not modeled.
- Platform ranking must use JSON `profit` once platform artifacts exist.
- This batch includes archived controls where current canonical files have already been narrowed.
- Baseline bar: total `10007.0`, IPR `7286.0`, ACO `2721.0` from platform-style artifact analysis.

## Ranking

| Rank | Bot | Total Replay PnL | IPR Replay PnL | ACO Replay PnL | Rejections | Errors |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | `candidate_27_v1_c26_soft_flatten.py` | 249079.00 | 238054.00 | 11025.00 | 0 | 0 |
| 2 | `candidate_26_v3_a3b1_one_sided_exit_overlay.py` | 248251.00 | 238054.00 | 10197.00 | 0 | 0 |
| 3 | `candidate_28_v1_c26_strict_one_sided.py` | 248105.00 | 238054.00 | 10051.00 | 0 | 0 |
| 4 | `candidate_25_v2_a2b1_conservative_regime_gate.py` | 247946.00 | 238054.00 | 9892.00 | 0 | 0 |
| 5 | `candidate_24_v1_a1b1_size_skew_refine.py` | 247631.00 | 238054.00 | 9577.00 | 0 | 0 |
| 6 | `candidate_10_bot02_carry_tight_mm.py` | 247628.00 | 238054.00 | 9574.00 | 0 | 0 |

## Interpretation

- Use this replay only to catch contract, limit, or obvious immediate-fill issues.
- Do not use this replay PnL scale for promotion.
- Upload selected bots to Prosperity, save `.py` + `.json` + `.log`, then rerun `analyze_platform_artifacts.py`.
