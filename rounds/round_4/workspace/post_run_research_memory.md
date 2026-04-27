# Post-Run Research Memory

## Status

- Round: `round_4`
- Last updated: `2026-04-27`
- Current champion: unresolved from the A/B/D partial only
- Latest platform artifact: `rounds/round_4/workspace/06_testing/round_4_wave1_pack_abd_partial_synthesis.md`
- Memory confidence: `medium`

## Source Runs

| Run | Candidate | Artifacts | PnL Source | Decision Relevance | Notes |
| --- | --- | --- | --- | --- | --- |
| `run_20260427_1900` | `r4_s01_vex_base_control` | `.py / .json / .log / summary` | real platform PnL | research | only active Pack A control; weak retention |
| `run_20260427_1902` | `r4_s02_hydro_base_control` | `.py / .json / .log / summary` | real platform PnL | rejected | no engagement |
| `run_20260427_1904` | `r4_s03_vex_4000_overlay` | `.py / .json / .log / summary` | real platform PnL | research | collapsed to `r4_s01`; no `4000` trades |
| `run_20260427_1906` | `r4_s05_mark22_veto_gate` | `.py / .json / .log / summary` | real platform PnL | research | hard veto over-suppressed branch |
| `run_20260427_1908` | `r4_s06_counterparty_concentration_gate` | `.py / .json / .log / summary` | real platform PnL | rejected | late extra `VEX` sell hurt final path |
| `run_20260427_1910` | `r4_s10_5200_signal_only_veto` | `.py / .json / .log / summary` | real platform PnL | research | strongest reusable contextual feature |
| `run_20260427_1912` | `r4_s13_4000_benign_flow_overlay` | `.py / .json / .log / summary` | real platform PnL | research | changed `VEX` path, not `4000` behavior |
| `run_20260427_1914` | `r4_s15_round3_winner_revalidation` | `.py / .json / .log / summary` | real platform PnL | research | over-filtered old winner test |

## Run Knowledge Index

| Run | Candidate | Strategy Family | Changed Axis | Tested Feature / Signal | PnL Source | Comparable To | Knowledge Delta | Memory Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `run_20260427_1900` | `r4_s01` | delta-1 control | baseline | `VEX` anchor | real platform | none | new | update |
| `run_20260427_1902` | `r4_s02` | delta-1 control | baseline | `HYDRO` anchor | real platform | `r4_s01` | new | update |
| `run_20260427_1904` | `r4_s03` | Pack B overlay baseline | feature toggle | direct `4000` overlay | real platform | `r4_s01` | contradicts | update |
| `run_20260427_1906` | `r4_s05` | hard defensive gate | feature toggle | `Mark 22` veto | real platform | `r4_s10` | contradicts | update |
| `run_20260427_1908` | `r4_s06` | engineered defensive gate | feature toggle | concentration gate | real platform | `r4_s10` | contradicts | update |
| `run_20260427_1910` | `r4_s10` | signal-only veto | feature toggle | `5200` monitor | real platform | `r4_s06` | new | update |
| `run_20260427_1912` | `r4_s13` | conditioned Pack B overlay | feature toggle | benign-flow `4000` conditioning | real platform | `r4_s03` | contradicts | update |
| `run_20260427_1914` | `r4_s15` | winner revalidation | feature toggle | old winner plus round-4 filters | real platform | `r4_s03` | contradicts | update |

## Current Reusable Insights

| Insight ID | Products | Based On Runs | Analysis Mode | Finding | Confidence | Portability | Reuse In | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `r4_w1_i01_vex_over_hydro` | `VEX`, `HYDRO` | `r4_s01`, `r4_s02` | edge | `VEX` is the only live base product in this subset | medium | likely reusable | strategy / spec / variant | `r4_s01` itself still had weak retention |
| `r4_w1_i02_4000_untested` | `VEX`, `VEV_4000` | `r4_s03`, `r4_s13`, `r4_s15` | failure | Pack B failed to test direct `4000` inventory at all | medium | round-specific | EDA / strategy / spec | do not misread this as proof that `4000` is dead |
| `r4_w1_i03_5200_signal_only` | `VEX`, `VEV_5200`, `VEV_5300` | `r4_s06`, `r4_s10` | counterfactual | `5200` works better as timing veto than as inventory or broad defensive thesis | medium | round-specific | strategy / spec / variant | still needs validation on a stronger parent branch |
| `r4_w1_i04_late_session_retention` | `VEX` | `r4_s01`, `r4_s06`, `r4_s10`, `r4_s13` | failure | late-session short extensions cause large giveback | medium | likely reusable | EDA / strategy / spec | current evidence is still based on open-short paths |

## Carry-Forward Principles

| Principle | Runs / Artifacts | Why It Is Validated | Reuse In | Revalidation Need |
| --- | --- | --- | --- | --- |
| Keep `VEX` as the primary delta-1 base over `HYDRO` | `r4_s01`, `r4_s02`, partial synthesis | only `VEX` engaged meaningfully in this subset | strategy / spec / variant | light |
| Treat counterparty information as context or veto first, not standalone alpha | `r4_s05`, `r4_s06`, `r4_s10`, partial synthesis | the most useful contextual branch improved timing by suppressing a bad extension, not by defining a full bot | strategy / spec / variant | light |
| Make retention a first-class design axis | `r4_s01`, `r4_s06`, `r4_s10`, `r4_s13` | multiple branches showed large giveback after earlier positive path | strategy / spec / variant | none |

## Untested Hypotheses Worth Revisiting

| Hypothesis | Origin | Why It Is Interesting | Clean Test Or EDA Needed | Status |
| --- | --- | --- | --- | --- |
| `4000` can still add value if we force real `VEV_4000` activation | Pack B runs | current Pack B did not test the leg it claimed to test | simplified spec or threshold-focused EDA | open |
| a `5200` veto improves the strongest active family, not only a standalone defensive bot | `r4_s10` | best reusable Pack D signal so far | one-axis overlay challenger | open |
| a late-session no-new-entry rule rescues the live `VEX` base | `r4_s01`, `r4_s06`, `r4_s10` | strongest repeated failure pattern in A/B/D | retention variant | open |

## Default Anti-Patterns

| Anti-Pattern | Evidence | Why It Should Stay Closed | Reopen Only If |
| --- | --- | --- | --- |
| standalone `HYDRO` control slots | `r4_s02` | zero engagement and no positive evidence | later linked-product analysis creates a real role |
| hard whole-bot contextual vetoes | `r4_s05`, `r4_s15` | they shut off the branch before it tested the thesis | thresholds are materially loosened and still decision-relevant |
| calling an overlay validated when the overlay leg never traded | `r4_s03`, `r4_s13`, `r4_s15` | it confuses base-leg PnL with overlay value | direct overlay attribution is visible |

## Feature Feedback

| Feature Or Signal | Runs | Outcome | Evidence Method | Confidence Change | Next Action |
| --- | --- | --- | --- | --- | --- |
| `VEX` anchor | `r4_s01`, `r4_s03` | helped, but retention weak | platform path + fills | unchanged | keep |
| `HYDRO` standalone control | `r4_s02` | failed | zero engagement | down | discard |
| direct `4000` overlay | `r4_s03`, `r4_s13`, `r4_s15` | unclear | no direct `4000` inventory | unchanged | EDA |
| concentration gate | `r4_s06` | failed | late-path comparison | down | discard |
| `5200` signal-only veto | `r4_s10` | helped | controlled run comparison versus `r4_s06` | up | variant |

## Process Hypothesis Feedback

| Process Hypothesis | Products | Runs | Run Evidence | Confidence Change | Strategy / Spec Impact |
| --- | --- | --- | --- | --- | --- |
| late-session family-state warnings matter more than broad contextual gating | `VEX`, `VEV_5200`, `VEV_5300` | `r4_s06`, `r4_s10` | supports | up | prefer narrow veto overlays |
| direct `4000` overlay remains naturally active enough to test cleanly | `VEX`, `VEV_4000` | `r4_s03`, `r4_s13`, `r4_s15` | weakens | down | reopen Pack B before reimplementation |

## Counterfactual Backlog

| Idea | Source Run | Improvement Axis | Expected ROI | Status | Next Action |
| --- | --- | --- | --- | --- | --- |
| no-new-entry after late-session warning or after `98000` | `r4_s01`, `r4_s06`, `r4_s10`, `r4_s13` | timing | high | untested | spec a retention challenger |
| apply `5200` veto to a stronger parent branch | `r4_s10` | filter | high | untested | variant |
| simplify Pack B to force direct `4000` activation | `r4_s03`, `r4_s13`, `r4_s15` | threshold / signal isolation | medium | untested | targeted EDA + spec revision |
| hard-flat or giveback stop after local peak | `r4_s01`, `r4_s06`, `r4_s10` | inventory | medium | untested | variant |

## Negative Evidence / Do Not Rediscover

| Idea | Runs | Why It Failed Or Was Weak | Reopen Only If |
| --- | --- | --- | --- |
| standalone `HYDRO` control wave | `r4_s02` | no engagement | role changes materially |
| hard `Mark 22` whole-bot veto | `r4_s05` | over-suppressed branch | a lighter veto shows real incremental edge |
| current composite old-winner revalidation stack | `r4_s15` | over-filtered and answered nothing | it is decomposed into one-axis tests |

## Downstream Notes

- EDA: add a retrospective run-informed note on late-session retention and `5200` veto context.
- Understanding: separate `4000 untested` from `4000 disproven`.
- Strategy generation: next wave should be a mini-batch focused on retention and signal-only reuse, not another broad exploration wave.
- Spec writing: cap the next wave to 1 clear change axis per bot.
- Variant generation: prioritize one `VEX` retention challenger and one `5200` veto overlay challenger.
