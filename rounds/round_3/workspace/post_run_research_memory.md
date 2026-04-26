# Post-Run Research Memory

Curated reusable evidence from platform or platform-style runs. This is not a
dump of every metric; keep only insights that change future decisions.

## Status

- Round: `round_3`
- Last updated: `2026-04-26`
- Current champion framing: the best full-stack live architecture remains the `delta-1 + ITM` Kalman winner family, now re-confirmed by `W5-01 = W4-03 = 1606.305`, with `W4-04 = 1604.305` essentially tied. The best pure fallback benchmark is now `W5-04 = 1672.000`, which improves the old clean delta-1 control without changing the preferred full architecture. The old absolute reference `B02-resid` (`1409.371`) now matters mainly as historical comparison.
- Latest platform artifact batch: the archived partial Wave 5 closeout set (`7/12` observed JSONs) under `../performances/amin/historical/`, summarized in [`06_testing/round_3_full_performance_synthesis.md`](06_testing/round_3_full_performance_synthesis.md)
- Archival note: the three corrected challenger raw artifacts, the Wave 5 observed artifacts, and the older human-readable run-summary `.md` files now all live under `../performances/amin/historical/`.
- Primary synthesis artifact: [`06_testing/round_3_full_performance_synthesis.md`](06_testing/round_3_full_performance_synthesis.md)
- Closeout framing artifact: [`06_testing/round_3_closeout_retrospective.md`](06_testing/round_3_closeout_retrospective.md)
- Memory confidence: `medium/high`

## Source Runs

| Run | Candidate | Artifacts | PnL Source | Decision Relevance | Notes |
| --- | --- | --- | --- | --- | --- |
| `B02-resid` | `C05 surrogate` | [`json`](../performances/amin/historical/r3_b02_itm_residual.json) | real platform PnL | research | profit `1409.371`, delta1 `1211.906`, itm `197.464`, active `0.000` |
| `D01-logger` | `diagnostic state probe` | [`json`](../performances/amin/historical/baseline_state_logger.json), [`summary`](../performances/amin/historical/run_20260425_1530_baseline_state_logger.md) | real platform PnL | research | no-trade live logger; confirms `5400/5500` activity and `6000/6500` floor persistence |
| `C06-base-v01` | `C06 corrected centered composite` | [`json`](../performances/amin/historical/candidate_c06_v01_centered_base.json), [`summary`](../performances/amin/historical/run_20260425_1535_candidate_c06_v01_centered_base.md) | real platform PnL | research | profit `-3008.203`, delta1 `599.500`, itm `0.000`, active `-3607.703`; `VEV_5200` dominates the loss |
| `C06-inv-v01` | `C06 inventory composite` | [`json`](../performances/amin/historical/candidate_c06_composite_inv.json), [`summary`](../performances/amin/historical/run_20260425_1540_candidate_c06_composite_inv.md) | real platform PnL | research | profit `-5245.475`, delta1 `599.500`, itm `0.000`, active `-5844.975`; stronger inventory skew did not rescue the basket |
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
| `W2-batch` | `Wave 2 learning batch` | [`report`](06_testing/round_3_full_performance_synthesis.md), [`csv`](06_testing/artifacts/full_synthesis/full_wave2_probe_summary.csv) | real platform PnL | research | 19-run batch: delta-1 control revalidated, passive standalone ITM inactive, `5300` still horizon-shaped not fast, `5000` still drags, fast-unwind rescue mostly failed from the start |
| `W3-batch` | `Wave 3 winner-shaping batch` | [`report`](06_testing/round_3_full_performance_synthesis.md), [`csv`](06_testing/artifacts/full_synthesis/full_wave3_probe_summary.csv) | real platform PnL | research | 24-run batch: `W3-15` becomes the new clean champion, `W3-23` proves active ITM synergy, `W3-17` becomes the first credible standalone selective `5300` winner, and inverse diagnostics remain unresolved |
| `W4-batch` | `Wave 4 finalist batch` | [`report`](06_testing/round_3_full_performance_synthesis.md), [`csv`](06_testing/artifacts/full_synthesis/full_wave4_probe_summary.csv) | real platform PnL | research | 12-run batch: `W4-03` becomes the new overall clean winner, `W4-04` confirms the same family, pure champion controls remain stable, tiny `5300` overlays stay subtractive, and direct inverse closure still does not trade cleanly |
| `W5-batch-partial` | `Wave 5 closeout batch` | [`report`](06_testing/round_3_full_performance_synthesis.md), [`csv`](06_testing/artifacts/full_synthesis/full_wave5_probe_summary.csv), [`closeout`](06_testing/round_3_closeout_retrospective.md) | real platform PnL | closeout | observed `7/12` runs: `W5-04` improves the pure fallback benchmark, `W5-01` only reconfirms the winner family, toxic-strike veto becomes informationally useful, and upside-distillation descendants stay research-only |

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
| `W2-batch` | `Wave 2 learning batch` | wave2_architecture_and_rescue | branch isolation / rescue redesign | delta-1 control, passive ITM, selective active retests, rescue exits, toxic micro-rescue, upper/floor coverage | real platform | Wave 1 + corrected + historical Round 3 set | contradicts and confirms | update |
| `W3-batch` | `Wave 3 winner-shaping batch` | wave3_winner_shaping | branch promotion / selective rescue | delta-1 Kalman control, active ITM overlay, selective `5300` rescue, inverse diagnostics, and final-stack tests | real platform | Wave 2 + full historical Round 3 set | contradicts and confirms | update |
| `W4-batch` | `Wave 4 finalist batch` | wave4_finalist_narrowing | finalist comparison / final additive overlays | champion control, champion plus active ITM, tiny `5300` overlays, distilled `5300` salvage, and forced inverse closure | real platform | Wave 3 + full historical Round 3 set | contradicts and confirms | update |
| `W5-batch-partial` | `Wave 5 closeout batch` | wave5_closeout | winner protection / fallback benchmark / upside distillation / toxic-signal test | protected winner family, cleaner fallback, partial upside descendants, and toxic-strike veto framing | real platform | Wave 4 + full historical Round 3 set | confirms and narrows | update |

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
| `R3-MEM-13` | Wave 2 base architecture | W2-batch (`W2-01`, `W2-04`) | champion control | Wave 2 revalidated delta-1 as the clean base architecture. `W2-01` and `W2-04` finished identically at `872.653`, and the ITM overlay was inactive under current thresholds. | high | round-specific | strategy / spec / variant | ITM can still matter, but not as this passive overlay form |
| `R3-MEM-14` | `VEV_5300` horizon shape | `L15`, `W2-05`, `W2-09` plus markout analysis | execution / horizon | `VEV_5300` is not a fast scalp. Entry and `1k` markouts are still negative, `5k` is around flat, and `10k` turns positive. Late-flatten helps a bit; fast-unwind is directionally wrong. | high | round-specific | strategy / spec / variant | this supports horizon-aware rescue and no-new-entry gates, not immediate take-profit bots |
| `R3-MEM-15` | selective active subset | `L16`, `W2-06`, `W2-10`, `W2-13` | strike / subset selection | `VEV_5000` remains negative at every tested horizon and drags the `5000 + 5300` subset from the start. `5300` still carries the only positive long-horizon markout in the active family. | high | round-specific | strategy / spec / variant | if `5000` stays alive, it now needs an explicit new thesis |
| `R3-MEM-16` | toxic strikes under tiny-risk control | `W2-15`, `W2-16` plus Wave 1 `L13/L14/L17/L18` | rescue / diagnostic | Tiny anchored rescues reduced `5100/5200` unit toxicity a lot, but both are still negative at every horizon; `5200` remains the worse final-PnL strike. | medium/high | round-specific | strategy / variant | `5100` can maybe survive only as a tiny diagnostic side branch; `5200` is still near hard-reject territory |
| `R3-MEM-17` | upper and floor coverage | `W2-14`, `W2-18`, `W2-19` | coverage / pruning | Upper passive/anchored ideas are low-damage and nearly flat, but current positive upper-combo PnL is really VEX-driven. Floor micro probe again showed zero usable edge. | high | round-specific | strategy / pruning | upper remains optional research-only; floor can be closed unless new live evidence appears |
| `R3-MEM-18` | global `>5k` peak study | all 58 runs, `7` with peak `>5k` | regime / giveback | The big mid-run peaks are a real signal source, but they were overwhelmingly driven and later destroyed by active vouchers, especially `5100/5200/5000`. `5300` is still the least-bad active peak driver. | high | round-specific | strategy / pruning | do not reopen the old broad basket just because it once reached `+18k` |
| `R3-MEM-19` | no-trade gate evidence | `L16`, `W2-05`, `W2-06`, `W2-09`, `W2-10` | regime / shutdown | Several selective active runs peak very early (`~20-24%` of session) and then place `60-70%` of their trades after the peak. That is the strongest current evidence for a regime or no-new-entry gate. | high | round-specific | strategy / spec / variant | simple observable regime filters now have higher ROI than hidden-state complexity |
| `R3-MEM-20` | Wave 3 champion base | `W3-15`, `W3-01`, `W3-02` | champion control | Wave 3 finally improved the clean delta-1 base materially: `W3-15 = 1527.305` now beats the old clean controls and the old absolute reference, which strongly supports a winner-focused final architecture around delta-1 first. | high | round-specific | strategy / spec / final selection | this is the strongest current promotion signal in the round |
| `R3-MEM-21` | Wave 3 ITM synergy | `W3-23`, `W3-01`, `W3-03` | additive overlay | Active ITM can add real value again when attached to the clean delta-1 base: `W3-23` outperforms `W3-01` by `+79`, while standalone refreshed `W3-03` is positive but much smaller. | high | round-specific | strategy / spec / final selection | ITM now looks like a genuine additive overlay, not just historical baggage |
| `R3-MEM-22` | `5300` rescue vs stack dilution | `W3-17`, `W3-11`, `W3-24`, `W3-08` | selective rescue / architecture pruning | Selective `5300` still has edge when filtered well enough, but it is not automatically additive to the best clean stacks. `W3-17` is the first credible standalone selective `5300` winner, yet `W3-24` still trails `W3-23`, and `W3-08` underperforms the pure delta-1 base. | high | round-specific | strategy / spec / final selection | keep `5300` alive only as a tiny rescue backlog or micro-overlay candidate |
| `R3-MEM-23` | `>10k` salvage counterfactuals | all `5` runs with peak `>10k` | giveback / retention | The old giant peaks were not fake upside: simple giveback-stop proxies would have salvaged roughly `+10k` to `+16k` in several cases. The problem was retention, strike mix, and continuation logic, not the total absence of signal. | medium/high | round-specific | strategy / spec / selective rescue | this supports using simple online retention logic before reopening any heavy complexity |
| `R3-MEM-24` | Wave 4 winner axis | `W4-03`, `W4-04`, `W4-01`, `W4-02`, `W4-11` | finalist comparison | Wave 4 resolved the clean winner axis: `delta-1 + ITM` on top of the Kalman base is now the best live family, with `W4-03 = 1606.305` and `W4-04 = 1604.305`, while pure-champion controls remain stable but lower at `1527.305`. | high | round-specific | strategy / spec / final selection | the next wave should protect this family, not rediscover it |
| `R3-MEM-25` | Wave 4 `5300` endgame verdict | `W4-05`, `W4-06`, `W4-07`, `W4-08`, `W4-09`, `W4-12` | overlay pruning | Tiny `5300` overlays can coexist with the winner base, but they remain subtractive; standalone and trend-led `5300` finalists are negative or flat. `5300` is now rescue-only and should not consume normal finalist slots. | high | round-specific | strategy / spec / pruning | if `5300` stays, it should stay only inside an upside-distillation or micro-overlay context |
| `R3-MEM-26` | Direct inverse closure verdict | `W4-10` plus prior inverse diagnostics | closure / negative evidence | Direct inverse trading on toxic strikes remains lower ROI than hoped: the forced `5100` inverse closure bot still did not trade the target leg cleanly. Toxic strikes are currently more valuable as veto / anti-signal inputs than as standard direct inventory legs. | medium/high | round-specific | strategy / spec / pruning | do not spend another normal slot on direct inverse unless the user explicitly wants it |
| `R3-MEM-27` | Ceiling problem after Wave 4 | full `94`-run synthesis | architecture / upside | The round now has a clean winner around `1.6k`, but the only evidence of much larger ceilings still lives inside the old `>10k` legacy peaks. Therefore the next wave should be an upside-distillation wave, not another broad exploration wave and not only more winner housekeeping. | high | round-specific | strategy / spec / final planning | the key question is no longer “who wins cleanly?” only, but “can a pruned descendant of the old peaks beat the clean winner without collapsing?” |
| `R3-MEM-28` | Wave 5 fallback benchmark | `W5-04` | closeout / benchmark | The pure `delta-1` fallback benchmark improved again to `1672.000`, which means `delta-1` is not only stable context but also the cleanest standalone architecture observed at round end. This strengthens the case for treating `delta-1` as both base and control in future rounds. | high | round-specific | round_4 framing / strategy / validation | this improves the fallback benchmark, but does not by itself invalidate the `delta-1 + ITM` winner family as the preferred full stack |
| `R3-MEM-29` | Wave 5 winner protection verdict | `W5-01`, `W5-02`, `W5-03` versus `W4-03`, `W4-04` | closeout / retention | Protecting the winner family did not create a new full-stack ceiling. `W5-01` simply re-confirmed the existing winner family, while stricter early-stop / retention-lock variants gave up too much realized edge. | high | round-specific | round_4 framing / strategy | winner protection matters more as discipline than as a new source of alpha |
| `R3-MEM-30` | Wave 5 toxic-strike veto signal | `W5-11` plus prior `5100/5200` evidence | signal-role redesign | `5100/5200` survive the round better as informational veto inputs than as default inventory legs. The first direct toxic-veto implementation stayed positive without reopening the old toxic basket. | medium/high | round-specific | round_4 framing / EDA / strategy | still not enough evidence to hard-code the exact veto form without fresh round data |
| `R3-MEM-31` | Round 3 closeout verdict | full `101`-run synthesis plus partial Wave 5 | closeout / governance | `round_3` no longer has an active implementation queue worth running. The round should now be consumed as four things only: validated findings, carry-forward principles, untested hypotheses, and anti-patterns. | high | round-specific | round_4 handoff / workspace hygiene | do not reopen `round_3` execution unless the user explicitly overrides the closeout decision |

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
| Wave 2 delta-1 control | W2-01, W2-04 | revalidated strongly | real platform PnL + path + markouts | up | treat delta-1 as the default base family |
| Passive standalone ITM | W2-03 | inactive / too timid | real platform PnL + zero-trade result | down for standalone passive form | if ITM survives, test it as selective overlay or more active support, not as a zero-trade passenger |
| `VEV_5300` selective branch | L15, W2-05, W2-09 | still alive, but horizon-sensitive | product PnL + markout horizon analysis | up for slower-horizon rescue / down for fast-unwind | design around no-trade gates and hold horizon |
| `VEV_5000` inside selective active | L16, W2-06, W2-10, W2-13 | still drags from entry onward | product PnL + per-product markout | down | justify explicitly before keeping it in the next wave |
| Fast-unwind rescue as a default pattern | W2-07, W2-08, W2-11, W2-12 | failed badly | real platform PnL + zero-positive-path diagnosis | down | stop assuming faster is automatically better for active vouchers |

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
| Rescue logic that realizes bad trades immediately | `W2-07`, `W2-08`, `W2-11`, `W2-12`, `W2-17` | no positive path at all despite hundreds of trades | execution / signal-selection | do not treat these as simple “needs later flatten” cases; the entry regime itself likely changed for the worse |

## Edge Decomposition Memory

| Edge | Runs | Driver | Real Edge Or Fragile? | Evidence | Reuse |
| --- | --- | --- | --- | --- | --- |
| VEX + ITM residual family | B02-anchor, B02-resid, W1-batch (`L10`) | VEX anchor plus low-damage ITM add-on | real enough to reprioritize, but mostly VEX-driven | historical wins plus positive `L10` and near-flat pure ITM | next learner / spec |
| Raw active-voucher family | B03, C06-legacy, B05, B06, B08 | mostly short inventory mark against lower strikes | fragile / failing | repeated negative strike attribution | replace with centered challenger |
| VEX + `VEV_5300` live combination | C06-base-v01, C06-inv-v01, W1-batch (`L25`) | VEX positive while `VEV_5300` is the least-bad active leg | promising but still mostly VEX-driven | `L25` is positive overall with `VEX +332.461` and `VEV_5300 -216.604` | direct learner / selective combo |
| Upper-strike live branch | D01-logger, W1-batch (`L21`-`L24`) | movement plus tight spreads, but poor realized trading | fragile / not yet monetized | directional upper losses and passive zero-fill result | lower-priority research only |
| Selective active-voucher entry signal | historical active family + W1 active (`L12`, `L15`, `L16`, `L20`) | some active bots do produce monetizable mid-run mark-to-market peaks before failing to retain them | fragile / execution-sensitive | path analysis shows edge exists in some subsets, but closing logic is broken | only re-open via shorter-horizon or stricter unwind designs |
| Delta-1 champion control | `L06`, `W2-01`, `W2-04` | clean delta-1 reversion / imbalance | real enough to anchor the next architecture | positive close, strong path retention, positive short/long markouts | default base family |
| `VEV_5300` slower-horizon residual | `L15`, `W2-05`, `W2-09` | weak short-horizon fills, better `10k` markout | fragile but still real enough for one more try | live markout shape is consistently improving with horizon | only re-open via horizon-aware / no-trade designs |

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
| R3-NEXT-08 | W2-batch | architecture choice | very high | open | Decide whether the next serious challenger set starts from pure delta-1 exploitation first, with vouchers demoted to one tiny selective overlay slot at most. |
| R3-NEXT-09 | W2-batch + markout analysis | regime / no-trade | very high | open | Build the next planning pass around explicit no-new-entry / regime-gate hypotheses for selective active vouchers. |
| R3-NEXT-10 | W2-batch + markout analysis | strike pruning | high | open | Decide whether `VEV_5000` should now be demoted below `VEV_5300` rather than kept in the default selective subset. |
| R3-NEXT-11 | W2-batch | branch pruning | high | open | Decide whether `VEV_5200` is now a hard reject and whether `VEV_5100` survives only as a tiny diagnostic branch. |
| R3-NEXT-12 | W3-batch | final architecture | very high | open | Decide whether the winner-focused next spec starts from `W3-15`, from `W3-23`, or from a tightly edited hybrid of the two. |
| R3-NEXT-13 | W3-batch + `>10k` study | selective rescue | high | open | Decide whether `5300` survives only as a micro-overlay rescue branch, informed by `W3-17`, `W3-11`, and the giveback counterfactual study. |
| R3-NEXT-14 | W3 inverse diagnostics | branch closure | high | open | Decide whether `5000/5100/5200` are now closed for final-bot purposes unless a clean inverse rerun is explicitly requested. |
| R3-NEXT-15 | W4-batch | final winner vs upside ceiling | very high | open | Decide whether to simply promote `W4-03/W4-04` or to spend one final wave trying to convert the old `>10k` upside into a retainable architecture. |
| R3-NEXT-16 | W4-batch + `>10k` product giveback study | toxic-strike role redesign | high | open | Decide whether `5100/5200` should now survive only as veto / anti-signal inputs instead of as direct normal tradable legs. |

## Negative Evidence / Do Not Rediscover

| Idea | Runs | Why It Failed Or Was Weak | Reopen Only If |
| --- | --- | --- | --- |
| Treat `graphLog` final as real PnL | all | it drifts materially from JSON `profit` | only as audit sanity check |
| Assume HYDRO is dead because legacy composites lost money | B01-base, B01-opt, composites, W1-batch (`L01`, `L02`) | isolated HYDRO learners are now clearly positive | only if a later cleaner HYDRO design turns negative again |
| Treat raw active-voucher losses as proof every later active-salvage attempt is dead | historical active-voucher family | later pruned descendants may still exploit some of the old upside under radically better retention and strike selection | only if a distilled Wave 5 descendant still collapses or never builds edge |
| Assume stronger inventory skew alone fixes the current active basket | C06-inv-v01 | lower terminal inventory still produced a materially worse run | after strike selection is solved on smaller subsets |
| Keep `VEV_5200` in the default active basket | C06-base-v01, C06-inv-v01 | it dominates live losses in both corrected challengers | only if isolated or subset learners overturn the current evidence |
| Treat `VEV_5300` as a standalone active winner | W1-batch (`L15`, `L25`) | it is the least-bad active strike, but the standalone learner is still negative | only if a redesigned selective combo shows genuine standalone alpha |
| Assume fast-unwind is the default rescue for active vouchers | W2-07, W2-08, W2-11, W2-12 | the fast-unwind variants often never built positive path at all | only if a new entry-regime definition fixes the negative short-horizon markouts |
| Read `W2-18` as proof that upper strikes are now profitable | W2-18 | almost all realized PnL came from the VEX leg | only if an upper-first or upper-only branch turns positive on its own |
| Spend more budget on floor bots by default | logger + W2-19 | floor again showed zero useful microstructure | only if live logs show a real floor break |

## Downstream Notes

- EDA: treat HYDRO as a live-positive branch again, but keep the wide-spread caveat; keep `VEV_5100/5200` as targeted negative-evidence strikes.
- Understanding: carry forward that clean delta-1 is now the strongest live family, pure ITM is near-flat, the active voucher family needs hard pruning, and the upper/surface branches remain exploratory.
- Understanding: also carry forward that many active-voucher failures are `edge then reversal`, not pure `no edge`; the surface branch is the cleaner example of true no-edge / bad signal.
- Strategy generation for `round_4`: start from the full `101`-run closeout, the Wave 5 decision board, the `>10k` salvage study, and the closeout artifact, not from any pre-Wave-4 planning state.
- Strategy generation for `round_4`: simple observable regime gates still have higher ROI than jumping straight to hidden-state/HMM complexity.
- Strategy generation for `round_4`: the best carry-forward framing is now `delta-1 first`, `ITM` as the best additive overlay, `5300` as a special-case rescue candidate, and `5100/5200` mainly as danger-state information.
- Spec writing: stop assuming the active `5000-5300` basket is homogeneous; if vouchers stay in scope, `5300` and `5000` now need separate rationale and separate hold-horizon logic.
- Variant generation for future rounds: prioritize delta-1-first or one tiny selective voucher overlay over broad retries; if selective active vouchers stay alive, favor no-new-entry / horizon-aware designs over naive fast-unwind rescues.
