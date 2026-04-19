# Round 2 Battery 01 Post-Run Analysis

## Executive Verdict

Battery 01 produced useful evidence, but it did **not** yet produce a clean final submission decision.

- Best raw single-run PnL: `R2-CAND-10` / `C10` with `2659.906`.
- Practical champion status: **provisional only**. C10's `bid()` is `0`, C07/C10 are effectively the same active trading logic except metadata, and Round 2 testing randomizes the 80% quote subset.
- Main positive evidence: IPR is carrying all realized PnL in this battery.
- Main failure evidence: ACO was not actually tested as alpha because every ACO module ended with `0` ACO PnL and `0` ACO position.
- Main implementation lesson: hard spread gates around `4` are mismatched to observed Round 2 top spreads, especially ACO.
- Main validation lesson: do not choose a champion from one platform result. C08 had two trials: `1669.594` and `837.500` profit, a range of `832.094`.

## Sources And Provenance

- Raw platform JSONs: [`rounds/round_2/performances/noel/historical`](../../performances/noel/historical)
- Canonical bot sources repaired/copied to: [`rounds/round_2/bots/noel/canonical`](../../bots/noel/canonical)
- Run summaries: [`rounds/round_2/performances/noel/canonical`](../../performances/noel/canonical)
- Post-run memory: [`post_run_research_memory.md`](../post_run_research_memory.md)
- No separate `.log` files or persisted `R2_BOT_LOG` stdout were found. Diagnostics therefore use platform `profit`, `activitiesLog`, `graphLog`, and final `positions`.

## Ranking By Real Platform PnL

| short_id   | variant   | candidate   |   profit |   final_ipr_pnl |   final_aco_pnl |   final_ipr_position |   final_aco_position |   max_drawdown |
|:-----------|:----------|:------------|---------:|----------------:|----------------:|---------------------:|---------------------:|---------------:|
| C10        | trial_1   | R2-CAND-10  | 2659.91  |        2659.91  |               0 |                   11 |                    0 |          0     |
| C02        | trial_1   | R2-CAND-02  | 2656.62  |        2656.62  |               0 |                   34 |                    0 |          0     |
| C07        | trial_1   | R2-CAND-07  | 2359.7   |        2359.7   |               0 |                   13 |                    0 |         -1.797 |
| C08        | trial_1   | R2-CAND-08  | 1669.59  |        1669.59  |               0 |                   -6 |                    0 |        -66     |
| C09        | trial_1   | R2-CAND-09  |  862.297 |         862.297 |               0 |                   -3 |                    0 |        -72     |
| C08        | trial_2   | R2-CAND-08  |  837.5   |         837.5   |               0 |                  -15 |                    0 |       -120     |
| C01        | trial_1   | R2-CAND-01  |  559     |         559     |               0 |                  -30 |                    0 |       -332     |
| C03        | trial_1   | R2-CAND-03  |    0     |           0     |               0 |                    0 |                    0 |          0     |
| C04        | trial_1   | R2-CAND-04  |    0     |           0     |               0 |                    0 |                    0 |          0     |
| C05        | trial_1   | R2-CAND-05  |    0     |           0     |               0 |                    0 |                    0 |          0     |
| C06        | trial_1   | R2-CAND-06  |    0     |           0     |               0 |                    0 |                    0 |          0     |

Decision caveat: C10 beats C02 by only `3.281` PnL, which is not meaningful under the observed randomized-subset variance.

## Product Attribution

| short_id   | variant   |   INTARIAN_PEPPER_ROOT |   ASH_COATED_OSMIUM |
|:-----------|:----------|-----------------------:|--------------------:|
| C01        | trial_1   |                559     |                   0 |
| C02        | trial_1   |               2656.62  |                   0 |
| C03        | trial_1   |                  0     |                   0 |
| C04        | trial_1   |                  0     |                   0 |
| C05        | trial_1   |                  0     |                   0 |
| C06        | trial_1   |                  0     |                   0 |
| C07        | trial_1   |               2359.7   |                   0 |
| C08        | trial_1   |               1669.59  |                   0 |
| C08        | trial_2   |                837.5   |                   0 |
| C09        | trial_1   |                862.297 |                   0 |
| C10        | trial_1   |               2659.91  |                   0 |

Interpretation:

- IPR generated all nonzero PnL.
- ACO generated exactly `0` final PnL in all runs, including ACO-only and combined bots.
- Combined bot scores should currently be read as IPR-family scores, not two-product evidence.

## Spread-Gate Diagnostics

Average platform spread coverage across Battery 01:

| product              |   spread_min |   spread_median |   spread_mean |   spread_max |   pct_spread_le_4 |   pct_spread_le_6 |   pct_spread_le_18 |
|:---------------------|-------------:|----------------:|--------------:|-------------:|------------------:|------------------:|-------------------:|
| ASH_COATED_OSMIUM    |            5 |              16 |        16.226 |           21 |             0     |             0.024 |              0.841 |
| INTARIAN_PEPPER_ROOT |            2 |              14 |        14.626 |           21 |             0.033 |             0.037 |              0.971 |

Why this matters:

- Current non-overlay bots require `spread <= 4` before trading.
- C09 overlay allows some activity up to `spread <= 6`.
- ACO's observed top spread is almost never compatible with those gates; ACO-only C03-C06 therefore likely failed by inactivity/over-throttling.
- IPR had rare narrow-spread windows and produced PnL, but the hard gate likely increases variance and may skip useful wider-spread opportunities.

## Code Equivalence And Non-Determinism

|   signature_group | short_ids                | modes                   | profits            |
|------------------:|:-------------------------|:------------------------|:-------------------|
|                 1 | C06-trial_1              | aco_full_book           | 0.000              |
|                 2 | C08-trial_1, C08-trial_2 | ipr_drift,aco_reversal  | 1669.594, 837.500  |
|                 3 | C03-trial_1              | aco_reversal            | 0.000              |
|                 4 | C09-trial_1              | ipr_drift,aco_imbalance | 862.297            |
|                 5 | C07-trial_1, C10-trial_1 | ipr_drift,aco_imbalance | 2359.703, 2659.906 |
|                 6 | C04-trial_1              | aco_imbalance           | 0.000              |
|                 7 | C05-trial_1              | aco_microprice          | 0.000              |
|                 8 | C02-trial_1              | ipr_extreme             | 2656.625           |
|                 9 | C01-trial_1              | ipr_drift               | 559.000            |

Key read:

- C07 and C10 have the same active trading configuration except bot metadata and role; C10 is not a meaningful MAF result because `maf_bid = 0`.
- The C07/C10 PnL gap and C08 two-trial gap show that upload-to-upload randomness is decision-relevant.
- Repeated trials are mandatory for the next champion decision unless deadline pressure forces a caveated choice.

## Hypothesis Verdicts

| Hypothesis | Battery 01 Evidence | Verdict | Next Action |
| --- | --- | --- | --- |
| IPR drift/residual can make money | Multiple positive real PnL runs, all PnL attributed to IPR | supported | rerun C02 and IPR drift family; add inventory challenger |
| IPR extreme residual is better than base drift | C02 nearly tied for top raw PnL | promising, not proven | repeat C02 and compare median/worst-case |
| ACO top imbalance is usable online | C04/C07/C09/C10 show zero ACO attribution | not tested due implementation gating | ACO activation probe first |
| ACO reversal is usable online | C03 zero; C08 positive PnL came from IPR | not tested due implementation gating | retest after spread fix |
| Spread defensive overlay helps | C09 lower PnL and likely over-throttling | weakened | replace binary gate with continuous sizing |
| MAF bid policy helps | C10 bid is 0; testing ignores final bid acceptance | not tested | final scenario decision only |
| Round 2 test is deterministic | C08 trials diverge materially | contradicted | repeated trials / robust ranking |

## Per-Run Decision Index

| short_id   | variant   |   profit | decision                                            | candidate_class   | memory_action   | summary_path                                                                     |
|:-----------|:----------|---------:|:----------------------------------------------------|:------------------|:----------------|:---------------------------------------------------------------------------------|
| C01        | trial_1   |  559     | rerun before rejecting                              | experimental      | update lightly  | rounds/round_2/performances/noel/canonical/run_20260419_battery01_c01_trial_1.md |
| C02        | trial_1   | 2656.62  | promote to rerun/variant                            | primary           | update          | rounds/round_2/performances/noel/canonical/run_20260419_battery01_c02_trial_1.md |
| C03        | trial_1   |    0     | reject current implementation                       | reject            | update          | rounds/round_2/performances/noel/canonical/run_20260419_battery01_c03_trial_1.md |
| C04        | trial_1   |    0     | reject current implementation                       | reject            | update          | rounds/round_2/performances/noel/canonical/run_20260419_battery01_c04_trial_1.md |
| C05        | trial_1   |    0     | reject current implementation                       | reject            | update          | rounds/round_2/performances/noel/canonical/run_20260419_battery01_c05_trial_1.md |
| C06        | trial_1   |    0     | reject current implementation                       | reject            | update          | rounds/round_2/performances/noel/canonical/run_20260419_battery01_c06_trial_1.md |
| C07        | trial_1   | 2359.7   | promote to rerun/variant                            | primary           | update          | rounds/round_2/performances/noel/canonical/run_20260419_battery01_c07_trial_1.md |
| C08        | trial_1   | 1669.59  | backup / rerun only if reversal remains interesting | backup            | update          | rounds/round_2/performances/noel/canonical/run_20260419_battery01_c08_trial_1.md |
| C08        | trial_2   |  837.5   | backup / rerun only if reversal remains interesting | backup            | update          | rounds/round_2/performances/noel/canonical/run_20260419_battery01_c08_trial_2.md |
| C09        | trial_1   |  862.297 | revise overlay                                      | experimental      | update          | rounds/round_2/performances/noel/canonical/run_20260419_battery01_c09_trial_1.md |
| C10        | trial_1   | 2659.91  | promote to rerun/variant                            | primary           | update          | rounds/round_2/performances/noel/canonical/run_20260419_battery01_c10_trial_1.md |

## Generation 2 Candidate Queue

This queue mixes PnL candidates and diagnostic candidates deliberately. The goal is to learn fast while keeping a competitive IPR base alive.

| candidate_id                                | role                                         | scope                                    | primary_change                                                                                              | priority                      |
|:--------------------------------------------|:---------------------------------------------|:-----------------------------------------|:------------------------------------------------------------------------------------------------------------|:------------------------------|
| R2-G2-01-IPR-EXTREME-RERUN-CHAMPION         | primary / robustness                         | INTARIAN_PEPPER_ROOT                     | Rerun C02-style IPR extreme logic without ACO to estimate quote-subset variance.                            | spec/implement first          |
| R2-G2-02-IPR-DRIFT-RERUN-CODE-EQUIV         | primary / robustness                         | INTARIAN_PEPPER_ROOT                     | Rerun the C07/C10 IPR drift family with ACO disabled for clean comparability.                               | spec/implement first          |
| R2-G2-03-IPR-EXTREME-FLATTER-INVENTORY      | primary / risk challenger                    | INTARIAN_PEPPER_ROOT                     | Add late/soft inventory neutralization to C02 without changing residual entry logic.                        | wave 1 challenger             |
| R2-G2-04-IPR-SPREAD-RETUNE                  | diagnostic / execution                       | INTARIAN_PEPPER_ROOT                     | Replace hard spread gate with continuous size/price throttling at wider spreads.                            | wave 2                        |
| R2-G2-05-ACO-ACTIVATION-PROBE               | diagnostic                                   | ASH_COATED_OSMIUM                        | Create small-size ACO probe with spread gate widened to realistic ACO levels and explicit activity logging. | wave 1 diagnostic             |
| R2-G2-06-ACO-IMBALANCE-WIDE-SPREAD          | secondary / alpha challenger                 | ASH_COATED_OSMIUM                        | Retest top imbalance with realistic spread handling and conservative quote sizes.                           | wave 2 after activation probe |
| R2-G2-07-ACO-REVERSAL-WIDE-SPREAD           | secondary / process challenger               | ASH_COATED_OSMIUM                        | Retest reversal with realistic spread handling and minimum fill opportunities.                              | wave 2                        |
| R2-G2-08-COMBINED-IPR-EXTREME-ACO-PROBE     | primary combined / diagnostic                | INTARIAN_PEPPER_ROOT + ASH_COATED_OSMIUM | Use C02-style IPR as base and add small ACO activation module.                                              | wave 1 combined               |
| R2-G2-09-COMBINED-IPR-EXTREME-ACO-IMBALANCE | primary combined / alpha                     | INTARIAN_PEPPER_ROOT + ASH_COATED_OSMIUM | C02-style IPR plus corrected ACO imbalance module.                                                          | wave 2/3                      |
| R2-G2-10-SPREAD-OVERLAY-CONTINUOUS          | execution overlay                            | INTARIAN_PEPPER_ROOT + ASH_COATED_OSMIUM | Convert spread overlay from binary gate to product-specific size curve.                                     | wave 3                        |
| R2-G2-11-BRUNO-R1-KALMAN-R2-PORT            | Round 1 canonical port / controlled side bet | INTARIAN_PEPPER_ROOT + ASH_COATED_OSMIUM | Port Bruno Kalman ACO module into Round 2 wrapper with current IPR base, R2 limits, bid=0, and R2 logging.  | wave 2 side bet               |
| R2-G2-12-NOEL-R1-C26-R2-PORT                | Round 1 canonical port / controlled side bet | INTARIAN_PEPPER_ROOT + ASH_COATED_OSMIUM | Port Noel C26 ACO one-sided/exit overlay into Round 2 wrapper with current IPR base and R2 logging.         | wave 2 side bet               |
| R2-G2-13-MAF-BID-SCENARIO                   | mechanics-only                               | Market Access Fee                        | Choose a bid policy from EDA scenario table after champion PnL stabilizes.                                  | near-final decision           |

## Generation 2 Priority Plan

Spec/implement first:

1. `R2-G2-01-IPR-EXTREME-RERUN-CHAMPION`
2. `R2-G2-02-IPR-DRIFT-RERUN-CODE-EQUIV`
3. `R2-G2-05-ACO-ACTIVATION-PROBE`
4. `R2-G2-08-COMBINED-IPR-EXTREME-ACO-PROBE`

Implement next if first wave confirms:

1. `R2-G2-03-IPR-EXTREME-FLATTER-INVENTORY`
2. `R2-G2-06-ACO-IMBALANCE-WIDE-SPREAD`
3. `R2-G2-07-ACO-REVERSAL-WIDE-SPREAD`
4. `R2-G2-09-COMBINED-IPR-EXTREME-ACO-IMBALANCE`

Side bets, controlled so they do not dominate:

1. `R2-G2-11-BRUNO-R1-KALMAN-R2-PORT`
2. `R2-G2-12-NOEL-R1-C26-R2-PORT`

Near-final mechanics:

1. `R2-G2-13-MAF-BID-SCENARIO`

## What Not To Do Yet

- Do not treat C10 as a proven MAF bot.
- Do not abandon ACO EDA signals purely because current ACO implementations produced zero PnL; first fix activation.
- Do not keep the current `spread <= 4` ACO gate.
- Do not pick C10 over C02 from the `3.281` PnL difference.
- Do not stack ACO imbalance, reversal, microprice, and full-book together until at least one ACO module has nonzero platform attribution.
- Do not let Round 1 ports dominate the work; use them as two controlled challengers.

## Artifacts

- [`battery_01_run_metrics.csv`](artifacts/battery_01_run_metrics.csv)
- [`battery_01_product_attribution.csv`](artifacts/battery_01_product_attribution.csv)
- [`battery_01_spread_gate_diagnostics.csv`](artifacts/battery_01_spread_gate_diagnostics.csv)
- [`battery_01_code_equivalence.csv`](artifacts/battery_01_code_equivalence.csv)
- [`battery_01_generation2_candidates.csv`](artifacts/battery_01_generation2_candidates.csv)
- [`battery_01_profit_ranking.png`](artifacts/battery_01_profit_ranking.png)
- [`battery_01_product_attribution.png`](artifacts/battery_01_product_attribution.png)
- [`battery_01_pnl_trajectories.png`](artifacts/battery_01_pnl_trajectories.png)
- [`battery_01_spread_gate_coverage.png`](artifacts/battery_01_spread_gate_coverage.png)

## Handoff

- Phase 06 should be reviewed with caveats.
- Next useful work is not broad EDA; it is targeted Gen2 spec/implementation around IPR robustness and ACO activation.
- Strategy/spec must reopen the ACO contracts before judging ACO alpha.
- Validation must run repeated trials for any close champion candidate.
