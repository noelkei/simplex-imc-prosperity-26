# Strategy Candidates

Use [`docs/templates/strategy_candidates_template.md`](../../../docs/templates/strategy_candidates_template.md) as the structure for this file.

## Status

READY_FOR_REVIEW

## Reopen Reason

Wave 2 was refined after the first debugged upload cycle because the remaining
runway is short: this wave plus only two more rounds before final selection.
That changes the correct optimization target.

- keep only the bots that answer structural thesis questions cleanly
- replace low-information overlays with entry-logic probes
- preserve comparability, but stop spending many slots on tiny retention
  variations over the same parent

## Sources

- Wiki facts:
  - [`../../../docs/prosperity_wiki/rounds/round_4.md`](../../../docs/prosperity_wiki/rounds/round_4.md)
- Understanding summary:
  - [`02_understanding.md`](02_understanding.md)
- EDA evidence:
  - [`01_eda/eda_round_4_counterparty_and_option_book.md`](01_eda/eda_round_4_counterparty_and_option_book.md)
  - [`01_eda/eda_round_4_wave1_abd_retrospective_addendum.md`](01_eda/eda_round_4_wave1_abd_retrospective_addendum.md)
- Run evidence:
  - [`06_testing/round_4_wave1_pack_abd_partial_synthesis.md`](06_testing/round_4_wave1_pack_abd_partial_synthesis.md)
  - [`post_run_research_memory.md`](post_run_research_memory.md)
- Uploaded winner references:
  - [`../research/algo run for round 4.py`](../research/algo%20run%20for%20round%204.py)
  - [`../research/big_volcano_man_fixed.py`](../research/big_volcano_man_fixed.py)
  - [`../research/big_volcano_man_IV_window.py`](../research/big_volcano_man_IV_window.py)

## Strategy Objective

This refined Wave 2 should answer four things before the winner wave:

1. Is `VEX` still mainly a retention problem, or do better entry conditions
   matter more now?
2. Does `VEV_5300` have direct current-round life, and does it need cleaner
   execution or cleaner activation?
3. Can `VEV_5200` and family-state context act as entry-quality filters rather
   than only post-hoc vetoes?
4. Is `VEV_4000` weak, execution-limited, or simply parent-contaminated?

## Keep / Replace Decision

### Kept from the previous Wave 2 draft

| Candidate | Why It Stays |
| --- | --- |
| `r4_w2_01_vex_late_no_new_entry` | cheapest direct retention rescue on the live `VEX` base |
| `r4_w2_05_5300_clean_value_retest` | cleanest `5300` baseline |
| `r4_w2_07_5300_queue_takeover_probe` | best winner-style execution probe on the strongest active family |
| `r4_w2_08_5300_with_5200_veto` | highest-ROI `5300 + 5200` combination |
| `r4_w2_13_4000_forced_activation` | closes the biggest unresolved `4000` evidence gap |
| `r4_w2_15_4000_quote_ladder_probe` | best direct `4000` execution-style test |

### Replaced

The replaced slots were too concentrated in tiny retention or overlay changes.
They are now used for entry-logic probes and cleaner option isolation.

## Wave 2 Pack Structure

| Pack | Learning Goal | Candidate IDs |
| --- | --- | --- |
| `G` | test whether `VEX` needs cleaner entry, not only cleaner retention | `r4_w2_01` to `r4_w2_04` |
| `H` | isolate `5300` signal quality versus execution style | `r4_w2_05` to `r4_w2_08` |
| `I` | test lightweight context as entry-quality gating rather than pure veto | `r4_w2_09` to `r4_w2_12` |
| `J` | separate `4000` activation quality from parent contamination | `r4_w2_13` to `r4_w2_15` |

## Candidate Table

| Candidate ID | Role | Product Scope | Changed Axis | Source Classification | Expected Learning | Validation Check | Priority |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `r4_w2_01_vex_late_no_new_entry` | keep | `VEX` | retention cutoff | data-driven | whether late giveback is still mostly timing | path improves without killing early activity | highest |
| `r4_w2_02_vex_inside_book_only` | replacement | `VEX` | enter only when recent `VEX` tape is clean/inside and spread is very tight | data-driven | whether `VEX` edge is mostly a clean-tape problem | fewer but cleaner `VEX` fills | high |
| `r4_w2_03_vex_micro_reversal_entry` | replacement | `VEX` | enter only on micro reversal after aggressive tape | data-driven | whether fading short aggressive bursts is better than continuous quoting | directional fills appear after aggression flips | high |
| `r4_w2_04_vex_depth_supported_entry` | replacement | `VEX` | enter only when top-of-book depth supports the side | data-driven | whether depth support matters more than late retention | fills cluster in deeper books | medium-high |
| `r4_w2_05_5300_clean_value_retest` | keep | `VEX + VEV_5300` | clean `5300` baseline | hybrid | whether `5300` has standalone current-round life | direct `5300` inventory appears cleanly | highest |
| `r4_w2_06_5300_direct_dislocation_only` | replacement | `VEV_5300` only | take only strong direct dislocations, no parent `VEX` trading | hybrid | whether `5300` has signal without parent noise | direct `5300` fills from obvious dislocations | high |
| `r4_w2_07_5300_queue_takeover_probe` | keep | `VEX + VEV_5300` | winner-style queue takeover | inspiration-only from winners | whether `5300` is execution-limited | healthier fill quality than plain baseline | highest |
| `r4_w2_08_5300_with_5200_veto` | keep | `VEX + VEV_5300 + 5200 context` | `5200` veto on active family | hybrid | whether best contextual feature improves strongest family | same `5300` intent, fewer toxic entries | highest |
| `r4_w2_09_vex_tape_clean_entry` | replacement | `VEX + family context` | clean-tape entry requiring low family pressure and no bad `5200` | hybrid | whether context should improve entry, not only exit | trades concentrate in visibly cleaner windows | medium-high |
| `r4_w2_10_vex_imbalance_surge_entry` | replacement | `VEX` | enter only on strong imbalance surge | data-driven | whether `VEX` should be event-driven rather than always-on | fewer but more directional fills | medium-high |
| `r4_w2_11_vex_low_concentration_entry` | replacement | `VEX + family ecology` | enter only when participant concentration is low | hybrid | whether fragmented family flow is a better regime for `VEX` | trade windows differ from pure `5200` veto | medium |
| `r4_w2_12_5300_option_only_veto` | replacement | `VEV_5300 + 5200 context` | trade `5300` without parent `VEX`, but keep the useful veto | hybrid | whether `5300 + 5200` works without parent contamination | direct `5300` attribution survives | medium-high |
| `r4_w2_13_4000_forced_activation` | keep | `VEX + VEV_4000` | force visible `4000` intent | data-driven | whether `4000` is alive at all | direct `4000` inventory or quotes appear | highest |
| `r4_w2_14_4000_option_only_band_entry` | replacement | `VEV_4000` only | trade only when direct `4000` band mispricing is large enough | hybrid | whether `4000` can work without parent `VEX` noise | direct `4000` engagement with cleaner attribution | high |
| `r4_w2_15_4000_quote_ladder_probe` | keep | `VEX + VEV_4000` | winner-style quote ladder | inspiration-only from winners | whether `4000` is execution-limited | better `4000` engagement than plain activation | highest |

## Prioritized Candidate Queue

| Order | Candidate ID | Why This Early |
| --- | --- | --- |
| 1 | `r4_w2_01_vex_late_no_new_entry` | fast sanity check that the live base still behaves |
| 2 | `r4_w2_05_5300_clean_value_retest` | clean active-family baseline |
| 3 | `r4_w2_07_5300_queue_takeover_probe` | best direct test of winner-style execution value |
| 4 | `r4_w2_08_5300_with_5200_veto` | best likely exploitative combo if `5300` is real |
| 5 | `r4_w2_13_4000_forced_activation` | necessary before any honest `4000` conclusion |
| 6 | `r4_w2_15_4000_quote_ladder_probe` | tests execution-limited versus no-edge |
| 7 | `r4_w2_02_vex_inside_book_only` | first clean `VEX` entry-quality probe |
| 8 | `r4_w2_06_5300_direct_dislocation_only` | direct `5300` without parent contamination |
| 9 | `r4_w2_14_4000_option_only_band_entry` | direct `4000` without parent contamination |
| 10 | `r4_w2_03_vex_micro_reversal_entry` | tests mean-reversion style entry |
| 11 | `r4_w2_09_vex_tape_clean_entry` | context as entry gate, not only veto |
| 12 | `r4_w2_12_5300_option_only_veto` | context plus direct `5300` attribution |
| 13 | `r4_w2_04_vex_depth_supported_entry` | depth-supported entry probe |
| 14 | `r4_w2_10_vex_imbalance_surge_entry` | event-driven `VEX` entry |
| 15 | `r4_w2_11_vex_low_concentration_entry` | lower-confidence family-ecology entry probe |

## Rejected Or Deferred Ideas

| Idea | Reason | Reopen Only If |
| --- | --- | --- |
| further tiny `VEX` retention variants | too much slot cost for too little new information | one retained branch still gives ambiguous path quality |
| more broad context overlays on top of the same parent | attribution contamination | a direct-entry probe proves strong |
| full old winner IV or hedge stack | complexity still too high for current evidence | a tiny execution-style port shows clear incremental value |
| new standalone `HYDRO` branches | Wave 1 evidence still too weak | a linked-product role emerges |

## Handoff To Phase 04

The grouped specs remain the right unit, but they must now reflect the refined
queue:

1. Pack `G`: one retained rescue plus three new `VEX` entry probes
2. Pack `H`: one clean baseline, one direct isolated `5300` probe, and two
   execution/context probes
3. Pack `I`: three `VEX` entry-quality/context gates plus one direct `5300`
   context-isolation probe
4. Pack `J`: one parented activation baseline, one direct isolated `4000`
   probe, and one winner-style execution probe
