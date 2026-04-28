# Post-Run Research Memory

## Status

- Round: `round_4`
- Last updated: `2026-04-28`
- Current champion: `r4_final_05_full_otm_basket`
- Latest synthesis artifact:
  [`06_testing/round_4_full_performance_synthesis.md`](06_testing/round_4_full_performance_synthesis.md)
- Memory confidence: `medium/high`

## Source Runs

| Run Group | Scope | PnL Source | Decision Relevance | Notes |
| --- | --- | --- | --- | --- |
| Bruno OTM family | `r4_final_01` to `r4_final_05`, plus `gemini`, `nuevo`, `prueba` | real platform PnL | primary | defines the winning `round_4` family and the best current champion |
| Noel Wave 1 / historical family | `r4_s01` to `r4_s15` | real platform PnL | research | establishes `VEX` as secondary, `5300` as real, `4000` as unresolved, and `5200` as veto context |
| Noel observed Wave 2 reruns | `r4_w2_05`, `r4_w2_06`, `r4_w2_07`, `r4_w2_12` | real platform PnL | secondary | reconfirms the `5300` floor but shows no clear lift over simpler winner-family bots |
| Round 3 carry-forward | `101` analyzed runs | real platform PnL | transfer framing | only retention and toxic-veto logic carry forward into the final `round_4` wave |

## Run Knowledge Index

| Evidence Bucket | Main Knowledge Delta | Memory Action |
| --- | --- | --- |
| Bruno OTM family | `5300 -> 5300+5400 -> 5300+5400+5500` is the best retained upside family in `round_4` | update |
| Noel `5300` family | `5300` is a genuine positive floor, but not the top family | update |
| Noel `5200` context work | `5200` and `Mark 22` should survive as timing veto, not as direct inventory | update |
| Round 3 peak study | old `>10k` / `~18k` baskets are inspiration-only for retention and veto design | update |

## Current Reusable Insights

| Insight ID | Products | Finding | Confidence | Reuse In | Caveat |
| --- | --- | --- | --- | --- | --- |
| `r4_i01_otm_basket_is_live` | `VEV_5300`, `VEV_5400`, `VEV_5500` | the focused OTM basket is the best monetized family in the round | high | final batch | still has giveback, but retained edge is strong |
| `r4_i02_5300_floor_is_real` | `VEV_5300` | `5300` alone repeatedly lands around `5.2k-5.4k` | high | fallback bots | lower ceiling than the basket |
| `r4_i03_5200_is_veto_not_inventory` | `VEV_5200`, `VEX`, OTM family | `5200` and `Mark 22` are more useful as danger-state inputs than as normal tradable legs | medium | one-axis derivative | still needs live confirmation on the champion family |
| `r4_i04_round3_peak_transfer_is_retention_only` | broad voucher family | do not port the raw old basket; port only retention and veto logic | high | final variants | raw basket itself remains closed |

## Carry-Forward Principles

| Principle | Why It Is Validated | Reuse In |
| --- | --- | --- |
| Start final `round_4` uploads from the best observed OTM family, not from delta-1 | direct `round_4` platform PnL dominance | final batch |
| Keep `5300` as the main option floor and `5400/5500` as additive upside legs | top `round_4` ranking | final batch |
| Use `5200` / `Mark 22` as veto information first | Wave 1 and cross-round evidence | final derivatives |
| Treat no-new-entry and giveback logic as the only worthwhile late-stage experimental axes | round3 peak study plus round4 late erosion | final derivatives |

## Untested Hypotheses Worth One Final Check

| Hypothesis | Why It Is Still Worth Testing | Status |
| --- | --- | --- |
| late-session freeze improves the OTM champion without crushing core edge | direct transfer from repeated late giveback | open in `r4_finalbatch_08` |
| `Mark 22 / 5200` toxicity should veto fresh OTM short extension | best reusable round4 context idea | open in `r4_finalbatch_09` |
| basket-level giveback stop preserves more upside than the simpler single-strike stop | highest-ROI retention derivative still missing | open in `r4_finalbatch_10` |

## Default Anti-Patterns

| Anti-Pattern | Why It Should Stay Closed |
| --- | --- |
| reopening the broad toxic active basket from `round_3` | huge peaks existed, but retention repeatedly failed |
| spending final-wave slots on flat or unrun Wave 2 probes | user direction for this pass treats them as non-ROI |
| treating `4000` as a final-wave priority | current `round_4` evidence is still too weak |
| assuming `VEX` or `HYDRO` should reclaim the main architecture slot | they are not competitive versus the live OTM family in `round_4` |

## Downstream Notes

- Strategy: use only the final 10-bot distilled queue.
- Spec: keep the new work limited to one-axis derivatives.
- Implementation: all old live `canonical/` bots are now archived; final bots
  live under `../bots/noel/canonical/`.
- Validation: rank against `r4_finalbatch_01_full_otm_basket_champion.py`
  first and only promote a derivative if it preserves or improves retained PnL.
