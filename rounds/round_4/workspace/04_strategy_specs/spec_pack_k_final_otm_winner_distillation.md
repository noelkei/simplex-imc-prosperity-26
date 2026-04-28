# Spec Pack K: Final OTM Winner Distillation

## Review Status

- Status: `COMPLETED`
- Owner: Codex
- Reviewer: Human
- Reviewed on: 2026-04-28

## Review Basis

- Explicit user instruction to produce the final `round_4` batch now.
- Evidence basis:
  - [`../03_strategy_candidates.md`](../03_strategy_candidates.md)
  - [`../06_testing/round_4_full_performance_synthesis.md`](../06_testing/round_4_full_performance_synthesis.md)
  - [`../post_run_research_memory.md`](../post_run_research_memory.md)
  - [`../../../round_3/workspace/06_testing/round_3_full_performance_synthesis.md`](../../../round_3/workspace/06_testing/round_3_full_performance_synthesis.md)
  - [`../../../round_3/workspace/06_testing/round_3_closeout_retrospective.md`](../../../round_3/workspace/06_testing/round_3_closeout_retrospective.md)

## Pack Members

| Candidate | Role In Pack | Target Bot Path |
| --- | --- | --- |
| `r4_finalbatch_01_full_otm_basket_champion` | primary champion | `rounds/round_4/bots/noel/canonical/r4_finalbatch_01_full_otm_basket_champion.py` |
| `r4_finalbatch_02_5300_5400_basket` | two-strike basket backup | `rounds/round_4/bots/noel/canonical/r4_finalbatch_02_5300_5400_basket.py` |
| `r4_finalbatch_03_5300_vex_combo` | mixed-family backup | `rounds/round_4/bots/noel/canonical/r4_finalbatch_03_5300_vex_combo.py` |
| `r4_finalbatch_04_5300_giveback_stop` | simple retention backup | `rounds/round_4/bots/noel/canonical/r4_finalbatch_04_5300_giveback_stop.py` |
| `r4_finalbatch_05_5300_pure_max` | single-strike clean baseline | `rounds/round_4/bots/noel/canonical/r4_finalbatch_05_5300_pure_max.py` |
| `r4_finalbatch_06_vex_5300_overlay_fallback` | cross-team fallback | `rounds/round_4/bots/noel/canonical/r4_finalbatch_06_vex_5300_overlay_fallback.py` |
| `r4_finalbatch_07_5300_horizon_hold_fallback` | slower-horizon fallback | `rounds/round_4/bots/noel/canonical/r4_finalbatch_07_5300_horizon_hold_fallback.py` |
| `r4_finalbatch_08_full_otm_late_freeze` | one-axis no-new-entry derivative | `rounds/round_4/bots/noel/canonical/r4_finalbatch_08_full_otm_late_freeze.py` |
| `r4_finalbatch_09_full_otm_mark22_veto` | one-axis toxic-flow veto derivative | `rounds/round_4/bots/noel/canonical/r4_finalbatch_09_full_otm_mark22_veto.py` |
| `r4_finalbatch_10_full_otm_giveback_stop` | one-axis giveback-stop derivative | `rounds/round_4/bots/noel/canonical/r4_finalbatch_10_full_otm_giveback_stop.py` |

## Why This Pack Exists

The final `round_4` batch should no longer behave like a research sweep.

- The strongest real money family in `round_4` is already known:
  `5300 -> 5300+5400 -> 5300+5400+5500`.
- The best `round_3` transfer is no longer raw active-basket aggression. It is
  retention control and toxic-family veto framing.
- The highest-ROI final wave is therefore a winner-protection and
  upside-distillation pack, not a fresh architecture wave.

## Selection Trace

- `01-05` are kept because they are directly supported by real `round_4`
  platform PnL and already span the best observed winner family from simple to
  richer.
- `06-07` survive because they are the cleanest positive non-Bruno fallbacks
  and preserve some family diversity without reopening dead branches.
- `08-10` are the only new derivatives because they each test one portable
  lesson with low integration risk:
  - late-session freeze,
  - `5200 / Mark 22` veto,
  - basket-level giveback stop.

## Feature Contract Summary

| Candidate Group | Main Feature | Inputs | Learning / Role |
| --- | --- | --- | --- |
| `01-05` | direct OTM fair-value basket trading | `VEX` book, `5300/5400/5500` books, local imbalance | preserve the proven winner family |
| `06-07` | positive `VEX + 5300` / horizon fallback behavior | `VEX` book, `5300` book, stored state | keep non-basket fallback diversity |
| `08` | late-session no-new-entry on the champion basket | `timestamp`, current option positions, OTM books | test whether simple late freeze preserves more of the peak |
| `09` | `5200 / Mark 22` toxic-flow veto on new sell extension | `Trade.seller`, `VEV_5200` market trades, trade bucket, OTM books | test whether round-4 counterparty information should suppress fresh basket shorts |
| `10` | per-strike giveback stop on the champion basket | current option positions, per-strike mid, stored entry / peak state | test whether basket retention improves without changing entry logic |

## Round-Specific Mechanics Contract

| Mechanic | Verdict | Implementation Note |
| --- | --- | --- |
| `Trader.run(state)` | implement | all bots return `result, 0, traderData` |
| Round 4 product list and limits | implement | only `VEX` and the documented `VEV_*` symbols are used |
| `Trade.buyer` / `Trade.seller` counterparty fields | implement where relevant | only `r4_finalbatch_09` uses this field as a veto input |
| Manual products | exclude | no bot references `AETHER_CRYSTAL` or manual options |
| Round 2 `bid()` method | not applicable | absent from all bots |

## Feature Exclusions

- No reopening of direct `5000/5100/5200` inventory.
- No reopening of broad `4000` work for the final wave.
- No hidden-state or research-only model imports.
- No attempt to port the raw `round_3` `>10k` / `~18k` basket as-is.

## Validation Plan

- Rank challengers by real platform JSON `profit`.
- Compare every bot first against `r4_finalbatch_01_full_otm_basket_champion`.
- For `08-10`, explicitly check:
  - whether the peak is lower or higher than `01`,
  - whether end-from-peak improves materially,
  - whether the retained profit beats or closely protects the champion.
- Treat `09` as successful even if it trades slightly less, provided the veto
  clearly removes toxic late expansion without crushing the core basket edge.
- If `08-10` do not show a real retention improvement, fall back to the proven
  winner family rather than reopening more design work.

## Notes

- This pack intentionally converts all prior live `canonical/` bots into
  `historical/` evidence before creating the new final wave.
- The raw high-peak `round_3` voucher baskets are classified as
  `inspiration-only` for retention and veto ideas, not as direct templates.
