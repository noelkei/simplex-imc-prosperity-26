# Round 4 Full Performance Synthesis

## Executive Verdict

This synthesis closes the current `round_4` evidence base before the final
upload wave.

- Round 4 real platform JSON artifacts analyzed: `27`
- Members with usable performance artifacts: `bruno`, `noel`
- Archived current-round canonical bots with no useful run evidence:
  - `11` Noel Wave 2 bots with no saved positive evidence in this pass
  - `1` Isaac bot with no saved performance artifact
- Strongest real platform run:
  `r4_final_05_full_otm_basket = 8729.104`
- Highest retained upside family:
  `5300 + 5400 + 5500`
- Best non-Bruno positive fallback family:
  `5300`-centered Noel controls in the `5.2k-5.3k` range

## Cross-Round Decision

The last `round_4` wave should not chase the raw `round_3` `>10k` or
`~18k` peaks directly.

- In `round_3`, the broad active voucher baskets proved that upside existed,
  but they repeatedly failed to retain it.
- In `round_4`, the only family that both built and retained large upside is
  the much simpler OTM basket centered on `5300`, `5400`, and `5500`.
- The right transfer from `round_3` is therefore:
  - keep retention control,
  - keep toxic-strike veto logic,
  - do not reopen the broad toxic basket itself.

## Top Round 4 Scoreboard

| Rank | Run / Bot | End PnL | Peak PnL | End From Peak | Family | Take |
| --- | --- | ---: | ---: | ---: | --- | --- |
| 1 | `r4_final_05_full_otm_basket` | `8729.104` | `10138.124` | `-1683.082` | `5300+5400+5500` | current champion |
| 2 | `r4_final_03_5300_5400_basket` | `7796.814` | `9079.531` | `-1528.845` | `5300+5400` | strongest two-strike backup |
| 3 | `r4_final_04_5300_vex_combo` | `5579.651` | `6229.675` | `-828.300` | `5300+VEX` | only top positive mixed-family variant |
| 4 | `r4_final_02_5300_giveback_stop` | `5398.998` | `6311.972` | `-1086.757` | `5300 only` | best simple retention fallback |
| 5 | `r4_final_01_5300_pure_max` | `5383.998` | `6296.972` | `-1086.757` | `5300 only` | clean single-strike baseline |
| 6 | `r4_w2_05_5300_clean_value_retest_debugged` | `5336.957` | `6262.270` | `-1101.444` | `5300 only` | positive but no lift over simpler winner family |
| 7 | `r4_w2_06_5300_direct_dislocation_only_debugged` | `5336.957` | `6262.270` | `-1101.444` | `5300 only` | same observed result shape |
| 8 | `r4_w2_07_5300_queue_takeover_probe_debugged` | `5336.957` | `6262.270` | `-1101.444` | `5300 only` | same observed result shape |
| 9 | `r4_w2_12_5300_option_only_veto_debugged` | `5336.957` | `6262.270` | `-1101.444` | `5300 only` | same observed result shape |
| 10 | `r4_s04_vex_5300_overlay` | `5265.045` | `6305.979` | `-1235.679` | `VEX+5300` | best earlier Noel fallback |

## Full Round 4 Run Classification

### Winning OTM family

| Run | End PnL | Peak | Verdict |
| --- | ---: | ---: | --- |
| `r4_final_05_full_otm_basket` | `8729.104` | `10138.124` | champion |
| `r4_final_03_5300_5400_basket` | `7796.814` | `9079.531` | strong backup |
| `r4_final_04_5300_vex_combo` | `5579.651` | `6229.675` | backup with delta-1 sidecar |
| `r4_final_02_5300_giveback_stop` | `5398.998` | `6311.972` | simple retention fallback |
| `r4_final_01_5300_pure_max` | `5383.998` | `6296.972` | simple baseline |

### Positive but lower-ROI `5300` controls

| Run | End PnL | Peak | Verdict |
| --- | ---: | ---: | --- |
| `r4_w2_05_5300_clean_value_retest_debugged` | `5336.957` | `6262.270` | positive duplicate cluster |
| `r4_w2_06_5300_direct_dislocation_only_debugged` | `5336.957` | `6262.270` | positive duplicate cluster |
| `r4_w2_07_5300_queue_takeover_probe_debugged` | `5336.957` | `6262.270` | positive duplicate cluster |
| `r4_w2_12_5300_option_only_veto_debugged` | `5336.957` | `6262.270` | positive duplicate cluster |
| `r4_s04_vex_5300_overlay` | `5265.045` | `6305.979` | proven fallback |
| `r4_s11_5300_horizon_hold` | `5248.482` | `6249.194` | proven fallback |
| `r4_s09_5300_toxic_strike_gate` | `2360.926` | `2846.548` | weak positive, lower priority |

### Useful context, weak monetization

| Run | End PnL | Peak | Verdict |
| --- | ---: | ---: | --- |
| `gemini-code-1777242683660` | `2039.762` | `2536.662` | broad OTM spread idea was positive but clearly worse than the focused family |
| `r4_s01_vex_base_control` | `15.047` | `143.008` | confirms `VEX` can trade but not compete with the OTM winner |
| `r4_s03_vex_4000_overlay` | `15.047` | `143.008` | collapsed to the `VEX` control, no direct `4000` evidence |
| `r4_s10_5200_signal_only_veto` | `3.961` | `86.223` | context useful as veto, not as direct money-maker |

### No-edge or over-shutdown branches

| Run | End PnL | Verdict |
| --- | ---: | --- |
| `nuevo` | `0.000` | no edge |
| `r4_s02_hydro_base_control` | `0.000` | no engagement |
| `r4_s05_mark22_veto_gate` | `0.000` | over-shutdown |
| `r4_s08_family_pressure_overlay` | `0.000` | over-shutdown |
| `r4_s12_upper_passive_probe` | `0.000` | no useful engagement |
| `r4_s15_round3_winner_revalidation` | `0.000` | old winner stack over-filtered |

### Negative or actively misleading branches

| Run | End PnL | Peak | Verdict |
| --- | ---: | ---: | --- |
| `r4_s06_counterparty_concentration_gate` | `-1.516` | `86.223` | weak edge then reversal |
| `r4_s07_trade_to_book_execution_overlay` | `-1.516` | `86.223` | no lift |
| `r4_s13_4000_benign_flow_overlay` | `-1.516` | `86.223` | changed parent path, not `4000` |
| `r4_s14_surface_sanity_filter` | `-1.516` | `86.223` | no lift |
| `prueba` | `-4386.476` | `0.000` | hard reject |

## Round 4 What Worked

- OTM option baskets worked, especially when limited to `5300`, `5400`, and
  `5500`.
- `5300` alone is a real floor strategy family.
- Simpler structures outperformed the richer noisy probes.
- The best counterparty lesson is still veto logic, not standalone alpha.

## Round 4 What Did Not Work

- Direct `4000` work never earned a last-wave slot.
- Broad defensive counterparty architectures mostly shut the bot off or added
  a worse late extension.
- Flat or no-performance bots are not worth carrying live.
- `VEX` alone remained too small versus the OTM basket family.

## Round 3 Transfer Used Here

### Accepted transfer

- late-session no-new-entry is high ROI
- giveback stops are worth one more clean test
- `5100/5200` toxicity is more useful as a veto than as direct inventory

### Rejected transfer

- broad active basket reopening
- raw high-peak salvage without strike pruning
- assuming huge peak PnL is enough to justify a final upload slot

## Final Last-Wave Recommendation

Use a final `10`-bot batch built from:

- `5` proven `round_4` winner-family bots,
- `2` proven positive fallbacks,
- `3` one-axis derivatives that only import:
  - late freeze,
  - `Mark 22 / 5200` veto,
  - giveback stop.

Do not spend the final wave on:

- `4000`,
- flat Wave 2 probes,
- raw `VEX`-only branches,
- or a reopened `round_3` toxic multi-strike basket.
