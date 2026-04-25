# Post-Run Research Memory

Curated reusable evidence from platform or platform-style runs. This is not a
dump of every metric; keep only insights that change future decisions.

## Status

- Round: `round_3`
- Last updated: `2026-04-25`
- Current champion: no current active champion yet. Best historical tested artifact is `B02-resid` / `r3_b02_itm_residual.json` with `1409.371`, but it is not the current active canonical path.
- Latest platform artifact: [`rounds/round_3/performances/amin/historical/probe_l27_surface_5300_5400_relval.json`](../performances/amin/historical/probe_l27_surface_5300_5400_relval.json)
- Archival note: the three corrected challenger raw artifacts and the full 25-bot Wave 1 learner batch now live under `../performances/amin/historical/`; their older human-readable run-summary `.md` files remain under `../performances/amin/canonical/`.
- Primary synthesis artifact: [`06_testing/round_3_full_performance_synthesis.md`](06_testing/round_3_full_performance_synthesis.md)
- Memory confidence: `medium`

## Source Runs

| Run | Candidate | Artifacts | PnL Source | Decision Relevance | Notes |
| --- | --- | --- | --- | --- | --- |
| `B02-resid` | `C05 surrogate` | [`json`](../performances/amin/historical/r3_b02_itm_residual.json) | real platform PnL | research | profit `1409.371`, delta1 `1211.906`, itm `197.464`, active `0.000` |
| `D01-logger` | `diagnostic state probe` | [`json`](../performances/amin/historical/baseline_state_logger.json), [`summary`](../performances/amin/canonical/run_20260425_1530_baseline_state_logger.md) | real platform PnL | research | no-trade live logger; confirms `5400/5500` activity and `6000/6500` floor persistence |
| `C06-base-v01` | `C06 corrected centered composite` | [`json`](../performances/amin/historical/candidate_c06_v01_centered_base.json), [`summary`](../performances/amin/canonical/run_20260425_1535_candidate_c06_v01_centered_base.md) | real platform PnL | research | profit `-3008.203`, delta1 `599.500`, itm `0.000`, active `-3607.703`; `VEV_5200` dominates the loss |
| `C06-inv-v01` | `C06 inventory composite` | [`json`](../performances/amin/historical/candidate_c06_composite_inv.json), [`summary`](../performances/amin/canonical/run_20260425_1540_candidate_c06_composite_inv.md) | real platform PnL | research | profit `-5245.475`, delta1 `599.500`, itm `0.000`, active `-5844.975`; stronger inventory skew did not rescue the basket |
| `W1-batch` | `Wave 1 learner batch` | [`report`](06_testing/round_3_full_performance_synthesis.md), [`csv`](06_testing/artifacts/full_synthesis/full_wave1_probe_summary.csv) | real platform PnL | research | 25-run batch: isolated delta-1 strongly positive, pure voucher-only learners non-positive, `VEV_5100/5200` toxic, upper residual negative, passive upper zero fills |
| `B02-anchor` | `C05 surrogate` | [`json`](../performances/amin/historical/r3_b02_itm_anchor.json) | real platform PnL | research | profit `726.893`, delta1 `599.500`, itm `127.393`, active `0.000` |
| `B06-tte` | `C07 surrogate` | [`json`](../performances/amin/historical/r3_b06_tte_cautious.json) | real platform PnL | research | profit `-752.886`, delta1 `599.500`, itm `0.000`, active `-1352.386` |
| `B07-hedge` | `C03 hedge variant` | [`json`](../performances/amin/historical/r3_b07_delta_hedge.json) | real platform PnL | research | profit `-1275.997`, delta1 `-1022.434`, itm `0.000`, active `-253.563` |
| `B08-regime` | `C03 / C06 regime variant` | [`json`](../performances/amin/historical/r3_b08_regime_composite.json) | real platform PnL | research | profit `-1501.925`, delta1 `599.500`, itm `0.000`, active `-2101.425` |
| `C06-legacy` | `C06 / C03 legacy` | [`json`](../performances/amin/historical/candidate_c06_composite_base.json) | real platform PnL | research | profit `-1631.925`, delta1 `599.500`, itm `0.000`, active `-2231.425` |
| `B03-pure` | `C03 surrogate` | [`json`](../performances/amin/historical/r3_b03_voucher_pure.json) | real platform PnL | research | profit `-2261.849`, delta1 `0.000`, itm `0.000`, active `-2261.849` |
| `B04-surf` | `C03 + C05 + upper-strike probe` | [`json`](../performances/amin/historical/r3_b04_full_surface.json) | real platform PnL | research | profit `-2561.846`, delta1 `599.500`, itm `318.797`, active `-3281.120` |
| `B01-base` | `C01 + C02 surrogate` | [`json`](../performances/amin/historical/r3_b01_delta1_baseline.json) | real platform PnL | research | profit `-6414.711`, delta1 `-6414.711`, itm `0.000`, active `0.000` |
| `B01-opt` | `C01 + C02 surrogate` | [`json`](../performances/amin/historical/r3_b01_delta1_optiver.json) | real platform PnL | research | profit `-20402.156`, delta1 `-20402.156`, itm `0.000`, active `0.000` |
| `B05-adv` | `C06 surrogate` | [`json`](../performances/amin/historical/r3_b05_composite_advanced.json) | real platform PnL | research | profit `-25333.769`, delta1 `-22856.344`, itm `0.000`, active `-2477.425` |

## Run Knowledge Index

| Run | Candidate | Strategy Family | Changed Axis | Tested Feature / Signal | PnL Source | Comparable To | Knowledge Delta | Memory Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `B02-resid` | `C05 surrogate` | itm_residual_vex | execution / risk | ITM intrinsic residual + VEX anchor | real platform | historical Round 3 set | new | update |
| `D01-logger` | `diagnostic state probe` | live_market_probe | baseline | live `TTE=5d` book / spread / residual capture | real platform | historical Round 3 set | new | update |
| `C06-base-v01` | `C06 corrected centered composite` | composite_centered_residual | feature toggle | centered Bachelier residual on `VEV_5000-5300` with HYDRO/VEX sidecars | real platform | `C06-legacy` | contradicts | update |
| `C06-inv-v01` | `C06 inventory composite` | composite_centered_residual_inventory | risk | inventory skew + imbalance confirmation on the corrected centered core | real platform | `C06-base-v01` | contradicts | update |
| `W1-batch` | `Wave 1 learner batch` | wave1_learning_matrix | branch isolation | isolated delta-1, ITM, active-subset, upper, and surface probes | real platform | prior historical + corrected set | contradicts and confirms | update |
| `B02-anchor` | `C05 surrogate` | itm_anchor_composite | execution / risk | ITM voucher anchor residual + delta-1 support | real platform | historical Round 3 set | new | update |
| `B06-tte` | `C07 surrogate` | tte_cautious_composite | execution / risk | TTE-cautious active-voucher residual | real platform | historical Round 3 set | contradicts | update |
| `B07-hedge` | `C03 hedge variant` | delta_hedged_composite | execution / risk | active-voucher residual + VEX delta hedge | real platform | historical Round 3 set | contradicts | update |
| `B08-regime` | `C03 / C06 regime variant` | regime_aware_composite | execution / risk | regime-adaptive active-voucher residual | real platform | historical Round 3 set | contradicts | update |
| `C06-legacy` | `C06 / C03 legacy` | composite_active_vouchers_legacy | execution / risk | legacy raw Bachelier residual + model-surface guardrail | real platform | historical Round 3 set | contradicts | update |
| `B03-pure` | `C03 surrogate` | active_voucher_pure | execution / risk | active-voucher residual without delta-1 legs | real platform | historical Round 3 set | contradicts | update |
| `B04-surf` | `C03 + C05 + upper-strike probe` | full_surface_composite | execution / risk | 8-strike full-surface residual trader | real platform | historical Round 3 set | contradicts | update |
| `B01-base` | `C01 + C02 surrogate` | delta1_pair_baseline | execution / risk | delta-1 Kalman maker pair | real platform | historical Round 3 set | confirms | update lightly |
| `B01-opt` | `C01 + C02 surrogate` | delta1_pair_optiver | execution / risk | delta-1 optiver-style execution stack | real platform | historical Round 3 set | confirms | update lightly |
| `B05-adv` | `C06 surrogate` | advanced_composite | execution / risk | active-voucher residual + optiver delta-1 stack | real platform | historical Round 3 set | contradicts | update |

## Current Reusable Insights

| Insight ID | Products | Based On Runs | Analysis Mode | Finding | Confidence | Portability | Reuse In | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `R3-MEM-01` | all | all 11 historical JSONs | validation heuristic | The sum of the final per-product `activitiesLog.profit_and_loss` rows equals JSON `profit` exactly in every artifact. | high | likely reusable | validation / Phase 06 | only applies when `activitiesLog` exists |
| `R3-MEM-02` | all | all 11 historical JSONs | validation heuristic | Final `graphLog` is only an audit proxy; median absolute delta vs `profit` is about `124.541`, max `344.146`. | high | likely reusable | validation / Phase 06 | do not rank bots with `graphLog` alone |
| `R3-MEM-03` | delta-1 branch | W1-batch (`L01`, `L02`, `L04`, `L05`, `L06`) | edge | Clean isolated delta-1 learners are strongly positive live; `HYDRO` and `VEX` both work much better in isolation than in the old legacy/composite implementations. | high | round-specific | strategy / spec / variant | live `TTE=5d` evidence only; robustness still needs one more design wave |
| `R3-MEM-04` | VEX + ITM | B02-anchor, B02-resid, W1-batch (`L07`-`L10`) | edge decomposition | Historical ITM/VEX winners are mostly VEX-driven; pure live ITM learners are near-flat, while `VEX + ITM` stays positive. | high | round-specific | strategy / variant | ITM still looks useful as an add-on, just not as the main standalone edge |
| `R3-MEM-05` | active vouchers | historical active family + W1-batch (`L12`-`L20`, `L25`) | failure / strike selection | No pure voucher-only Wave 1 learner finished positive; `VEV_5100` and `VEV_5200` are toxic, `VEV_5000` is weak, and `VEV_5300` is the least-bad active strike but not a standalone winner. | high | round-specific | strategy / spec / variant | `VEV_5300` still helps as a relative or combo leg |
| `R3-MEM-06` | active vouchers | C06-legacy, B05, B07, B08, B04, B03, W1-batch | failure | Inventory saturation remains a real clue, but the Wave 1 batch shows that inventory control only helps once the basket is cleaned; `L20` beats `L16`, while the broad C06 inventory overlay still fails. | high | round-specific | spec / variant | inventory is a secondary cleaner, not a primary rescue |
| `R3-MEM-07` | HYDRO / upper strikes | historical JSONs + D01 + W1-batch | contradiction / validation | Platform-style evidence still says HYDRO spreads are wide and `VEV_5400/5500` are tighter than raw-day EDA implied, but live trading now shows HYDRO can still win while directional upper residuals remain negative. | medium/high | round-specific | targeted EDA / validation | spread evidence alone was not enough to rank these branches correctly |
| `R3-MEM-08` | corrected active basket | C06-base-v01, C06-inv-v01, W1-batch | failure / strike selection | The broad active basket is not homogeneous. `VEV_5200` remains the dominant do-not-trust strike, and Wave 1 now shows `VEV_5100` should join it in the reject pile unless rescued later. | high | round-specific | strategy / spec / variant | strong enough to hard-prune the next design wave |
| `R3-MEM-09` | upper + floor vouchers | D01-logger + W1-batch (`L21`-`L24`) | edge / negative evidence | `VEV_5400/5500` are live enough to test, but directional residual trading is negative and passive upper quoting currently gets zero fills; `VEV_6000/6500` still remain frozen. | high | round-specific | strategy / variant | upper branch is still research-only, not promotion-ready |
| `R3-MEM-10` | surface relative value | W1-batch (`L26`, `L27`) | failure | Current surface-pair implementations are negative; `L26` is especially bad and looks like realized adverse selection rather than terminal inventory mark. | high | round-specific | strategy / variant | pause or redesign execution before rerunning this family |
| `R3-MEM-11` | corrected active voucher composites | C06-base-v01, C06-inv-v01 | failure | The corrected centered composite did not rescue the broad `VEV_5000-5300` basket, and stronger inventory skew made the result worse. | high | round-specific | strategy / spec | this rejects the broad current composite path, not all strike-isolated residual learners |
| `R3-MEM-12` | path quality across families | all 39 current runs, especially historical active family + W1 active learners | path / reversal analysis | Many bad final runs still had strong intra-run peaks: `20/39` runs peaked above `+100` and finished negative, and `17/39` peaked above `+500` and finished negative. Active-voucher branches often show edge-then-reversal, while surface `L26` shows almost no positive path at all. | high | round-specific | strategy / spec / variant | do not treat all negative finals as equivalent; separate bad hold/unwind from no-edge families |

## Feature Feedback

| Feature Or Signal | Runs | Outcome | Evidence Method | Confidence Change | Next Action |
| --- | --- | --- | --- | --- | --- |
| HYDRO delta-1 maker logic | B01-base, B01-opt, composite families, W1-batch (`L01`, `L02`, `L06`) | legacy/composite implementations failed, isolated learners succeeded strongly | product attribution + Wave 1 live PnL | up for isolated branch / down for old stack | keep HYDRO only in cleaner delta-1 designs |
| VEX delta-1 / anchor logic | most nonzero VEX runs + W1-batch (`L04`, `L05`, `L06`, `L10`, `L25`) | helped clearly | product attribution + Wave 1 live PnL | up | keep VEX as standalone branch and default combo leg |
| ITM residual / anchor logic | B02-anchor, B02-resid, W1-batch (`L07`-`L10`) | historical family helped; pure live ITM is near-flat; VEX+ITM stays positive | product attribution + Wave 1 live PnL | mixed / addon-only | keep ITM as optional overlay, not primary alpha |
| Raw active-voucher residual family | B03, C06-legacy, B05, B06, B08 | failed in tested implementations | strike-level attribution + inventory saturation | down for raw family | test centered-residual challenger next |
| Broad active-voucher centered residual family | C06-base-v01 | failed in current corrected implementation | live product attribution + final positions | down | split by strike / subset rather than rerunning the basket |
| Inventory skew overlay on the broad active basket | C06-inv-v01 | failed | controlled comparison vs centered base | down | keep inventory only as a later subset overlay |
| Upper-strike live branch | D01-logger | reopened | live spread / movement diagnostics | up | create `5400/5500` learners now |
| TTE-cautious overlay | B06 | improved less than hoped | direct comparison vs legacy family | unchanged/down | keep as secondary branch only |
| Delta hedge overlay | B07 | reduced active-voucher loss but hurt VEX leg badly | product attribution | unclear | debug only after base centered run exists |
| Intra-run path retention | all 39 current runs | many negative finishes still show meaningful mid-run peaks | timestamp-level `activitiesLog` path analysis | up as a decision tool | classify future families into `edge then reversal` versus `no edge` before pruning |

## Multivariate Relationship Feedback

| Relationship | Runs | EDA Expectation | Run Evidence | Confidence Change | Next Action |
| --- | --- | --- | --- | --- | --- |
| VEX is the usable voucher anchor | most positive families | strong | supports | up | keep VEX as anchor and isolate it |
| HYDRO is independent and additive | composite families | additive sidecar | independence not contradicted, but contribution weak/negative | unchanged for independence / down for usefulness | hydro-only learner |
| Wide-strike spreads make 5400/5500 untradeable | raw EDA vs B04 platform-style log | exclude by default | historical platform-style spreads contradict the raw spread claim, but profitability still weak | unchanged / mixed | targeted EDA before reopening |
| Active vouchers are one homogeneous branch | corrected C06 runs | broad `5000-5300` basket should be reasonable | contradicted by `VEV_5200` vs `VEV_5300` split | down | move to strike-isolated learners |
| `VEV_6000/6500` may break the floor live | D01-logger | possible live movement | no evidence of a break | unchanged/up for exclusion | keep floor family out of active trading |

## Process Hypothesis Feedback

| Process Hypothesis | Products | Runs | Run Evidence | Confidence Change | Strategy / Spec Impact |
| --- | --- | --- | --- | --- | --- |
| ITM residual snap-back is monetizable | VEV_4000-4500 | B02-anchor, B02-resid | supports | up | move ITM learning variants forward |
| Active near-ATM residual mean reversion is monetizable with current raw implementations | VEV_5000-5300 | B03, C06-legacy, B05, B06, B08 | weakens / contradicts raw implementation family | down for current raw family | centered challenger + inventory control |
| Active near-ATM residual mean reversion is monetizable as one broad corrected centered basket | VEV_5000-5300 | C06-base-v01, C06-inv-v01 | contradicts | down | stop rerunning the broad basket; isolate strikes and subsets |
| Upper-strike residual may still be tradable live | VEV_5400-5500 | D01-logger | supports reopening, not profitability | up from deferred | create upper-strike learners |
| TTE=5d needs caution | VEV_5000-5300 | B06 | not resolved cleanly | unchanged | keep as later calibration branch |

## Redundancy Decision Feedback

| Feature Family | Prior Redundancy Decision | Runs | Evidence | Next Action |
| --- | --- | --- | --- | --- |
| Raw residual vs centered residual | raw residual was the historical default | B03, C06-legacy, B05, B06, B08 | raw family underperformed | spec revision already done | test centered residual live |
| Hydro sidecar branch | keep as separate branch | composite families | currently adds little or negative value | reopen | isolate before keeping it in composites |
| Broad active basket vs strike-isolated learners | broad active basket was still acceptable in corrected C06 | C06-base-v01, C06-inv-v01 | broad basket still fails even after correction | reopen | move to strike-isolated / subset learners |

## Statistical Confidence Notes

- Decision-relevant confidence update: `activitiesLog` final-sum is an exact PnL proxy when JSON `profit` is present; `graphLog` final is not.
- Tool or method used: platform JSON parsing, product attribution, spread coverage, and graphLog drawdown.
- Caveat or overfit risk: no stdout `.log`, no own-trade detail, and no exact artifact bundle for every historical upload.

## Log-Derived Feature Discoveries

| Feature Or Signal | Source Runs / Logs | Evidence | Online Usability | Proposed Use | Next Step |
| --- | --- | --- | --- | --- | --- |
| `activitiesLog` final product PnL split | all historical JSONs | exact reconstruction of total PnL | validation-only | diagnostics / run ranking | keep as default PnL proxy when `profit` is missing |
| HYDRO wide-top-spread warning | all historical JSONs | mean HYDRO top spread about `15.6` | usable online | execution filter / strategy pruning | hydro-only learner |
| `VEV_5000` strike penalty | active-voucher runs | negative in `7/7` tested runs | usable online | product filter / risk control | targeted variant excluding `VEV_5000` |
| Short-saturation alert for active vouchers | active-voucher composite runs | repeated `-300` terminal positions | usable online | risk control | inventory-first challenger |
| `VEV_5200` live strike penalty | C06-base-v01, C06-inv-v01 | dominant loss in both corrected runs | usable online | product filter / risk control | isolate `5200` and assume exclusion until proven otherwise |
| upper-strike live movement | D01-logger | `5400/5500` move with one- to two-tick spreads | usable online | new learner branch | create upper residual and passive learners |
| live floor persistence | D01-logger | `6000/6500` stay at `0.5` with one-tick spread | usable online | exclusion / monitoring | keep floor family out of active bot budget |

## Feature Confidence Updates

| Feature Or Signal | Previous Confidence | New Confidence | Reason | Affected Artifact |
| --- | --- | --- | --- | --- |
| ITM residual branch | medium/high | medium / addon-only | pure live ITM learners are near-flat while VEX+ITM stays positive mostly through the VEX leg | strategy / variant |
| HYDRO online implementation | medium | medium/high for isolated branch / low for old composite stack | Wave 1 hydro-only learners are positive, which overturns the earlier blanket rejection | strategy / variant |
| Raw active-voucher residual family | medium/high | lowered | repeated historical losses and short saturation | spec / variant |
| Broad corrected active-voucher basket | medium/high | low | both corrected challengers still failed materially | strategy / variant |
| `VEV_5300` active branch | medium | medium | it is the least-bad active strike, but the standalone live learner is still negative | strategy / variant |
| `VEV_5200` active branch | medium | low / likely reject | dominant live loss in both corrected runs | strategy / variant |
| upper-strike branch | low / deferred | low / experimental | logger reopened `5400/5500`, but live directional residual runs are still negative and passive upper gets no fills | strategy / variant |

## Failure Patterns

| Pattern | Runs | Conditions | Failure Class | Action |
| --- | --- | --- | --- | --- |
| Active-voucher short saturation | C06-legacy, B05, B08, B04, B03 | repeated terminal `-300` per strike | inventory / risk | test inventory-clean challenger |
| HYDRO drag in legacy/composite stacks | B01-base, B01-opt, B05 and most composites | HYDRO PnL stays negative in the older implementations | implementation / execution | do not generalize this failure to the isolated HYDRO branch |
| VEV_5100 toxicity | W1-batch (`L13`, `L17`, `L19`) | `VEV_5100` is deeply negative alone and still toxic inside subsets | signal / strike-selection | exclude `VEV_5100` by default from the next design wave |
| VEV_5000 drag | all active-voucher runs | `VEV_5000` negative in every tested run | product-selection / risk | test subset without `VEV_5000` |
| VEV_5200 concentration | C06-base-v01, C06-inv-v01 | `VEV_5200` dominates loss even after correction | signal / strike-selection | isolate or exclude `VEV_5200` before any broad active rerun |
| Edge-then-reversal collapse | historical active family, C06-legacy, C06-base-v01, W1 active (`L12`, `L13`, `L15`, `L16`, `L17`, `L19`) | good intraday peaks followed by large late giveback | hold / unwind / sizing / regime-shift | redesign exits and holding horizon before declaring the branch dead |

## Edge Decomposition Memory

| Edge | Runs | Driver | Real Edge Or Fragile? | Evidence | Reuse |
| --- | --- | --- | --- | --- | --- |
| VEX + ITM residual family | B02-anchor, B02-resid, W1-batch (`L10`) | VEX anchor plus low-damage ITM add-on | real enough to reprioritize, but mostly VEX-driven | historical wins plus positive `L10` and near-flat pure ITM | next learner / spec |
| Raw active-voucher family | B03, C06-legacy, B05, B06, B08 | mostly short inventory mark against lower strikes | fragile / failing | repeated negative strike attribution | replace with centered challenger |
| VEX + `VEV_5300` live combination | C06-base-v01, C06-inv-v01, W1-batch (`L25`) | VEX positive while `VEV_5300` is the least-bad active leg | promising but still mostly VEX-driven | `L25` is positive overall with `VEX +332.461` and `VEV_5300 -216.604` | direct learner / selective combo |
| Upper-strike live branch | D01-logger, W1-batch (`L21`-`L24`) | movement plus tight spreads, but poor realized trading | fragile / not yet monetized | directional upper losses and passive zero-fill result | lower-priority research only |
| Selective active-voucher entry signal | historical active family + W1 active (`L12`, `L15`, `L16`, `L20`) | some active bots do produce monetizable mid-run mark-to-market peaks before failing to retain them | fragile / execution-sensitive | path analysis shows edge exists in some subsets, but closing logic is broken | only re-open via shorter-horizon or stricter unwind designs |

## Counterfactual Backlog

| Idea | Source Run | Improvement Axis | Expected ROI | Status | Next Action |
| --- | --- | --- | --- | --- | --- |
| R3-NEXT-01 | W1-batch | strategy selection | very high | open | Decide whether the next champion family should be delta-1 first rather than voucher-first. |
| R3-NEXT-02 | W1-batch + historical ITM/VEX winners | selective combo | high | open | Decide whether ITM should survive only as a low-damage add-on to VEX rather than as a standalone branch. |
| R3-NEXT-03 | W1-batch (`L12`, `L15`, `L16`, `L20`, `L25`) | product selection | high | open | Decide whether `VEV_5000 + VEV_5300` is the only active subset still worth carrying into design. |
| R3-NEXT-04 | W1-batch (`L13`, `L14`, `L17`, `L18`, `L19`, `L26`) | branch pruning | very high | open | Formalize `VEV_5100` and `VEV_5200` as excluded-by-default until future evidence rescues them. |
| R3-NEXT-05 | W1-batch (`L21`-`L24`) | branch pruning / redesign | medium | open | Decide whether the upper branch should be paused, kept passive-only, or redesigned with a different execution style. |
| R3-NEXT-06 | W1-batch (`L26`, `L27`) | execution redesign | medium | open | Decide whether surface-pair logic deserves a redesign or a full pause after the current adverse-selection failure. |
| R3-NEXT-07 | full 39-run path synthesis | holding horizon / exit design | high | open | Decide whether selective active-voucher follow-ups should explicitly optimize for faster profit capture and tighter unwind, not just better fair value estimation. |

## Negative Evidence / Do Not Rediscover

| Idea | Runs | Why It Failed Or Was Weak | Reopen Only If |
| --- | --- | --- | --- |
| Treat `graphLog` final as real PnL | all | it drifts materially from JSON `profit` | only as audit sanity check |
| Assume HYDRO is dead because legacy composites lost money | B01-base, B01-opt, composites, W1-batch (`L01`, `L02`) | isolated HYDRO learners are now clearly positive | only if a later cleaner HYDRO design turns negative again |
| Treat raw active-voucher losses as proof the corrected centered challenger is dead | historical active-voucher family | current active canonical bot uses a different centered signal and different guardrail | after the corrected base has a real run |
| Assume stronger inventory skew alone fixes the current active basket | C06-inv-v01 | lower terminal inventory still produced a materially worse run | after strike selection is solved on smaller subsets |
| Keep `VEV_5200` in the default active basket | C06-base-v01, C06-inv-v01 | it dominates live losses in both corrected challengers | only if isolated or subset learners overturn the current evidence |
| Treat `VEV_5300` as a standalone active winner | W1-batch (`L15`, `L25`) | it is the least-bad active strike, but the standalone learner is still negative | only if a redesigned selective combo shows genuine standalone alpha |

## Downstream Notes

- EDA: treat HYDRO as a live-positive branch again, but keep the wide-spread caveat; keep `VEV_5100/5200` as targeted negative-evidence strikes.
- Understanding: carry forward that clean delta-1 is now the strongest live family, pure ITM is near-flat, the active voucher family needs hard pruning, and the upper/surface branches remain exploratory.
- Understanding: also carry forward that many active-voucher failures are `edge then reversal`, not pure `no edge`; the surface branch is the cleaner example of true no-edge / bad signal.
- Strategy generation: the next wave should start from the full synthesis report, not from the old “wave 1 unrun” backlog.
- Spec writing: stop assuming the active `5000-5300` basket is homogeneous; if vouchers stay in scope, they should be selective add-ons to a stronger base family.
- Variant generation: prioritize delta-1-first or VEX-led selective voucher combos over broad composite retries, and if selective active vouchers stay alive, bias toward shorter-horizon capture / unwind experiments.
