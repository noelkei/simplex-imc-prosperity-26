# Strategy Candidates

## Status

READY_FOR_REVIEW

## Reopen Reason

This is now a round-closeout and last-upload-wave strategy pass, not another
broad exploration cycle.

- All prior `round_4` canonical bots now either have performance evidence and
  were archived to `historical/`, or had no useful run evidence and were
  archived as dead ends.
- The final queue should maximize expected real platform PnL from what already
  worked in `round_4`, while importing only the highest-ROI retention and veto
  lessons from `round_3`.

## Sources

- Wiki facts:
  - [`../../../docs/prosperity_wiki/rounds/round_4.md`](../../../docs/prosperity_wiki/rounds/round_4.md)
- Round 4 run evidence:
  - [`06_testing/round_4_full_performance_synthesis.md`](06_testing/round_4_full_performance_synthesis.md)
  - [`post_run_research_memory.md`](post_run_research_memory.md)
- Round 3 carry-forward evidence:
  - [`../../round_3/workspace/06_testing/round_3_full_performance_synthesis.md`](../../round_3/workspace/06_testing/round_3_full_performance_synthesis.md)
  - [`../../round_3/workspace/06_testing/round_3_closeout_retrospective.md`](../../round_3/workspace/06_testing/round_3_closeout_retrospective.md)
  - [`../../round_3/workspace/post_run_research_memory.md`](../../round_3/workspace/post_run_research_memory.md)

## Strategy Objective

Build a final upload batch of at most `10` bots that:

1. keeps the best proven `round_4` money-making family intact,
2. preserves a few proven fallbacks for diversity,
3. spends only three slots on one-axis derivatives that directly target the
   main retained failure mode: `peak -> giveback -> late extension`,
4. avoids reopening the broad toxic active basket that produced `>10k` and
   `~18k` peaks in `round_3` but repeatedly failed to retain them.

## Cross-Round Evidence Summary

### What is clearly alive in `round_4`

- The strongest real platform family is the simple OTM option basket centered
  on `VEV_5300`, extended to `VEV_5400`, and best of all to
  `VEV_5500`.
- The top `round_4` run is
  `r4_final_05_full_otm_basket = 8729.104`, with a still-positive retained
  peak structure instead of the catastrophic reversal seen in the old toxic
  baskets.
- The clean `5300` floor is real and repeatable:
  `r4_final_01`, `r4_final_02`, `r4_s04`, `r4_s11`, and the four observed
  Wave 2 reruns all cluster around `5.2k-5.4k`.

### What should only survive as control logic, not as a reopened architecture

- `round_3` confirmed that raw wide active baskets can print huge peaks, but
  the same family also produced the worst givebacks in the repo:
  `r3_b08_regime_composite` peaked near `17.47k` and finished negative,
  `candidate_c06_composite_base` peaked near `17.34k` and finished negative,
  and multiple other broad voucher composites crossed `10k` before collapsing.
- The transferable part from that family is not the raw basket itself. It is:
  - late-session no-new-entry discipline,
  - giveback-aware flattening,
  - treating `5100/5200` toxicity as veto or danger-state information rather
    than default inventory.

### What should be de-prioritized for the last wave

- Direct `VEV_4000` work remains unproven in `round_4`.
- `VEX`-only and broad counterparty-architecture bots did not beat the OTM
  basket family.
- Unrun or flat-PnL Wave 2 branches are not good final-wave slots.

## Final Last-Wave Queue

| Order | Candidate ID | Bot Path | Role | Origin | Why It Is In The Last 10 |
| --- | --- | --- | --- | --- | --- |
| 1 | `r4_finalbatch_01_full_otm_basket_champion` | `../bots/noel/canonical/r4_finalbatch_01_full_otm_basket_champion.py` | primary champion | proven `round_4` winner | best real PnL in the round |
| 2 | `r4_finalbatch_02_5300_5400_basket` | `../bots/noel/canonical/r4_finalbatch_02_5300_5400_basket.py` | backup basket | proven `round_4` winner | strongest two-strike fallback |
| 3 | `r4_finalbatch_03_5300_vex_combo` | `../bots/noel/canonical/r4_finalbatch_03_5300_vex_combo.py` | mixed-family backup | proven `round_4` winner | only positive `VEX` sidecar among top bots |
| 4 | `r4_finalbatch_04_5300_giveback_stop` | `../bots/noel/canonical/r4_finalbatch_04_5300_giveback_stop.py` | retention fallback | proven `round_4` winner | keeps the best observed simple retention control |
| 5 | `r4_finalbatch_05_5300_pure_max` | `../bots/noel/canonical/r4_finalbatch_05_5300_pure_max.py` | simple baseline | proven `round_4` winner | clean single-strike benchmark |
| 6 | `r4_finalbatch_06_vex_5300_overlay_fallback` | `../bots/noel/canonical/r4_finalbatch_06_vex_5300_overlay_fallback.py` | cross-team fallback | proven `round_4` fallback | best earlier Noel `VEX + 5300` positive branch |
| 7 | `r4_finalbatch_07_5300_horizon_hold_fallback` | `../bots/noel/canonical/r4_finalbatch_07_5300_horizon_hold_fallback.py` | horizon fallback | proven `round_4` fallback | positive slower-hold `5300` control |
| 8 | `r4_finalbatch_08_full_otm_late_freeze` | `../bots/noel/canonical/r4_finalbatch_08_full_otm_late_freeze.py` | new one-axis derivative | `round_4` champion + `round_3/4` retention lesson | imports the cleanest no-new-entry lesson without reopening toxic strikes |
| 9 | `r4_finalbatch_09_full_otm_mark22_veto` | `../bots/noel/canonical/r4_finalbatch_09_full_otm_mark22_veto.py` | new one-axis derivative | `round_4` champion + `round_4` counterparty lesson | imports the best `5200` / `Mark 22` veto idea as a family filter |
| 10 | `r4_finalbatch_10_full_otm_giveback_stop` | `../bots/noel/canonical/r4_finalbatch_10_full_otm_giveback_stop.py` | new one-axis derivative | `round_4` champion + `round_3/4` giveback lesson | tests basket-level retention instead of raw upside reopening |

## Rejected Or Deferred Ideas

| Idea | Reason | Reopen Only If |
| --- | --- | --- |
| Raw `4000` reopening | current `round_4` evidence is still too weak for a last-wave slot | all OTM finalists fail live |
| Re-uploading flat or unrun Wave 2 probes | user rule for this pass is to treat missing useful performance as dead weight | a human explicitly wants one more diagnostic wave |
| Reopening the broad toxic `5000/5100/5200/5300` basket | `round_3` peak study says the raw upside is real but non-retainable | the final OTM family itself collapses and only a danger-state redesign remains |
| Fresh standalone `HYDRO` or `VEX` architecture | far below the current OTM family in real `round_4` PnL | OTM finalists fail and delta-1 becomes the only live fallback |

## Handoff To Phase 04

The spec layer should treat this as a final distillation pack:

- `01-05`: proven champion and close proven backups
- `06-07`: proven fallback diversity
- `08-10`: new one-axis retention and veto derivatives only

Do not treat the new derivatives as permission to reopen the old broad active
voucher thesis.
