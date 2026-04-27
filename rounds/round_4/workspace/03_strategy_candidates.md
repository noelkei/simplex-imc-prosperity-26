# Strategy Candidates

Use [`docs/templates/strategy_candidates_template.md`](../../../docs/templates/strategy_candidates_template.md) as the structure for this file.

## Status

READY_FOR_REVIEW

## Reopen Reason

`Phase 03` is reopened because Wave 1 Pack `A/B/D` validation changed the
candidate map materially:

- insight `r4_w1_i01_vex_over_hydro`: `VEX` is the only live delta-1 base in
  the reviewed subset
- insight `r4_w1_i02_4000_untested`: Pack `B` did not actually test direct
  `VEV_4000` inventory
- insight `r4_w1_i03_5200_signal_only`: `VEV_5200` is more useful as veto
  context than as inventory or broad defensive architecture
- insight `r4_w1_i04_late_session_retention`: late-session giveback is now the
  main failure axis worth attacking directly

This Wave 2 is still exploratory by design. The goal is not to produce the
final winner yet; it is to maximize decision value per run slot before the
winner-oriented wave.

## Sources

- Wiki facts:
  - [`../../../docs/prosperity_wiki/rounds/round_4.md`](../../../docs/prosperity_wiki/rounds/round_4.md)
- Understanding summary:
  - [`02_understanding.md`](02_understanding.md)
- External paper research:
  - [`02b_external_paper_research.md`](02b_external_paper_research.md)
  - [`02b_strategy_handoff.md`](02b_strategy_handoff.md)
- EDA evidence:
  - [`01_eda/eda_round_4_counterparty_and_option_book.md`](01_eda/eda_round_4_counterparty_and_option_book.md)
  - [`01_eda/eda_round_4_counterparty_profiles.md`](01_eda/eda_round_4_counterparty_profiles.md)
  - [`01_eda/eda_round_4_option_book_structure.md`](01_eda/eda_round_4_option_book_structure.md)
  - [`01_eda/eda_round_4_option_volatility_and_pricing.md`](01_eda/eda_round_4_option_volatility_and_pricing.md)
  - [`01_eda/eda_round_4_round3_revalidation.md`](01_eda/eda_round_4_round3_revalidation.md)
  - [`01_eda/eda_round_4_wave1_abd_retrospective_addendum.md`](01_eda/eda_round_4_wave1_abd_retrospective_addendum.md)
- Run evidence:
  - [`06_testing/round_4_wave1_pack_abd_partial_synthesis.md`](06_testing/round_4_wave1_pack_abd_partial_synthesis.md)
  - [`post_run_research_memory.md`](post_run_research_memory.md)
- Uploaded winner references:
  - [`../research/algo run for round 4.py`](../research/algo%20run%20for%20round%204.py)
  - [`../research/big_volcano_man_fixed.py`](../research/big_volcano_man_fixed.py)
  - [`../research/big_volcano_man_IV_window.py`](../research/big_volcano_man_IV_window.py)

## Strategy Objective

Wave 2 should answer five unresolved questions cleanly:

1. Can `VEX` base edge be rescued by retention logic?
2. Does `VEV_5300` deserve serious exploitation in current `round_4`, not just
   carry-forward attention from `round_3`?
3. How much value survives when `VEV_5200` is reused only as timing/veto
   context on a stronger parent branch?
4. Is `VEV_4000` truly weak, or merely still untested because the prior Pack
   `B` never forced direct activation?
5. Do strike-specific quoting and inventory-aware execution ideas from the
   uploaded winner bots improve the learnability of `5300` or `4000` branches
   without dragging in incompatible prior-round machinery?

## Carry-Forward Ledger

### Validated carry-forward principles

| Principle | Evidence | Why It Survives | Revalidation Need |
| --- | --- | --- | --- |
| `VEX` should stay the main delta-1 base | `r4_w1_i01`, Pack `A/B/D` synthesis | only live anchor in the reviewed subset | light |
| counterparty info should be context first | `r4_w1_i03`, Pack `D` synthesis | best result was a timing veto, not a standalone bot | light |
| retention must be a first-class design axis | `r4_w1_i04`, Pack `A/B/D` synthesis | repeated giveback is the dominant failure mode | none |
| one-axis variants beat composite retests right now | Pack `B` and `D` failures | composite over-filtering answered too little | none |

### Untested hypotheses worth paying for

| Hypothesis | Evidence Gap | Why It Still Matters | Clean Test Needed |
| --- | --- | --- | --- |
| `VEV_4000` can add value if direct activation is forced | `r4_w1_i02` | Pack `B` was invalid as an online `4000` test | yes |
| `VEV_5200` veto improves a stronger active parent | `r4_w1_i03` | strongest new feature is still under-reused | yes |
| `VEV_5300` can be exploited with strike-specific execution | round understanding + prior carry-forward | likely active family but current-round proof is incomplete | yes |
| lighter execution overlays beat hard whole-bot vetoes | Pack `D` results | preserves thesis while avoiding shutdown | yes |
| inventory-aware quote management can separate `execution-limited` from `no edge` | uploaded winner architecture | high information value if kept simple | yes |

### Default anti-patterns

| Anti-Pattern | Evidence | Why To Avoid | Reopen Only If |
| --- | --- | --- | --- |
| standalone `HYDRO` control slots | `r4_s02` | zero engagement and no new learning | linked-product role emerges |
| hard whole-bot contextual vetoes | `r4_s05`, `r4_s15` | branch shuts off before testing thesis | thresholds are materially lighter |
| declaring overlay success with zero overlay inventory | `r4_s03`, `r4_s13`, `r4_s15` | attribution becomes false | direct leg activation is visible |
| broad active voucher baskets | prior memory + Wave 1 design lessons | hides which strike is helping or hurting | a new isolated family proves otherwise |
| importing old-product constants from winner bots | uploaded winner `.py` files | incompatible symbols and calibration | current-round evidence supports new constants |

## Wave 1 Coverage Audit

| Area | Current Posture | What We Actually Learned | Wave 2 Response |
| --- | --- | --- | --- |
| `VEX` base | `edge then reversal` | live base exists but bleeds late | retention challengers |
| `HYDRO` base | `no edge` | no engagement in reviewed subset | prune standalone slot |
| `VEV_4000` overlay | `not cleanly tested` | prior bots changed `VEX`, not `4000` | force activation / execution probe |
| `VEV_5200` contextual layer | `signal-only candidate` | useful veto on bad late extension | reuse on stronger parents |
| broad defensive counterparty bots | `not cleanly tested` / `over-suppressed` | whole-bot vetoes are too blunt | lighter overlays only |
| `VEV_5300` active family | `still strategically open` | current-round canonical proof still incomplete | isolate with simple strike-specific tests |

## Uploaded Winner Bot Intake Pass

Compatibility verdict for all three uploaded `.py` files: `partially
compatible`.

- Incompatible as direct strategy templates:
  - old product universe: `VOLCANIC_ROCK`, old vouchers, and prior-round
    constants
  - no current-round `VEX/HYDRO/VEV_*` calibration
  - no current-round counterparty-first design
- Useful as architecture references:
  - strike-by-strike treatment instead of one uniform voucher family
  - fair-value quoting plus opportunistic crossing when market is clearly off
  - inventory-aware quote tilt and spread-conditioned expansion discipline

| Uploaded File | Compatibility | What We Reuse | Handling | Candidate Impact |
| --- | --- | --- | --- | --- |
| [`../research/algo run for round 4.py`](../research/algo%20run%20for%20round%204.py) | partial | strike-specific treatment, cross-then-requote flow | inspiration-only | informs `5300` and `4000` execution probes |
| [`../research/big_volcano_man_fixed.py`](../research/big_volcano_man_fixed.py) | partial | inventory-aware quoting, fair-value ladder discipline | used | changes `5300` and `4000` execution candidate design |
| [`../research/big_volcano_man_IV_window.py`](../research/big_volcano_man_IV_window.py) | partial | windowed sanity / simple value guard | validation | only justifies tiny value guards, not full IV machinery |

## Design Rules For Wave 2

- Keep exactly one primary changed axis per bot.
- Use at most two supporting filters.
- Prefer parent branches with known life: `VEX` or `5300`, not `HYDRO`.
- If a bot claims to test `4000`, direct `VEV_4000` inventory or quote intent
  must be visible in validation.
- If a bot uses an uploaded winner idea, keep it to architecture:
  quote shape, strike specificity, queue-takeover behavior, or inventory tilt.
- Do not import old-product fair values, IV constants, or voucher baskets.
- Wave 2 stops at `15` because the marginal information after these branches
  becomes duplicate, low-ROI, or blocked on Pack `C/E/F` validation.

## Wave 2 Pack Structure

| Pack | Learning Goal | Candidate IDs |
| --- | --- | --- |
| `G` | rescue live `VEX` edge through retention | `r4_w2_01` to `r4_w2_04` |
| `H` | isolate whether `5300` deserves serious current-round exploitation | `r4_w2_05` to `r4_w2_08` |
| `I` | reuse context features only where a parent branch is already alive | `r4_w2_09` to `r4_w2_12` |
| `J` | close the `4000` attribution gap cleanly | `r4_w2_13` to `r4_w2_15` |

## Candidate Table

| Candidate ID | Role | Product Scope | Changed Axis | Source Classification | Research Handling | Expected Learning | Validation Check | Priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `r4_w2_01_vex_late_no_new_entry` | primary | `VEX` | no-new-entry after late cutoff | data-driven | none | whether late giveback is mostly entry timing | path improves after late cutoff without killing early edge | highest |
| `r4_w2_02_vex_peak_giveback_stop` | primary | `VEX` | hard giveback stop after local peak | data-driven | none | whether the branch is `retention-limited` rather than `no edge` | peak-to-close drawdown compresses materially | high |
| `r4_w2_03_vex_toxic_window_cooldown` | secondary | `VEX` | short cooldown after `5200/Mark 22` warning | hybrid | used via `r4_w1_i03` | whether narrow veto timing rescues `VEX` without over-shutdown | skips late bad extension and still trades earlier | medium-high |
| `r4_w2_04_vex_smaller_second_clip` | exploratory | `VEX` | size-down repeat same-direction clip | data-driven | none | whether late giveback is sizing-related, not signal-related | second clip shrinks damage without flattening trade count | medium |
| `r4_w2_05_5300_clean_value_retest` | primary | `VEX + VEV_5300` | simple strike-specific `5300` overlay | hybrid | validation from `round_3` carry-forward | whether `5300` still has standalone current-round life | direct `5300` inventory and cleaner attribution appear | highest |
| `r4_w2_06_5300_horizon_hold_v2` | primary | `VEX + VEV_5300` | longer hold plus no-new-entry | hybrid | validation | whether `5300` is `edge then reversal` rather than `no edge` | later hold preserves path better than clean retest | high |
| `r4_w2_07_5300_queue_takeover_probe` | secondary | `VEV_5300` focused | cross-when-off, then requote around simple value | paper-inspired | inspiration-only from uploaded winners | whether `5300` needs execution style, not new signal | direct fills appear with healthier markout | medium-high |
| `r4_w2_08_5300_with_5200_veto` | primary | `VEX + VEV_5300 + VEV_5200 context` | add `5200` veto to strongest active family | hybrid | used | whether best new context signal improves the most interesting active leg | same `5300` intent, fewer toxic late entries | highest |
| `r4_w2_09_vex_plus_5200_veto` | primary | `VEX + VEV_5200 context` | pure veto reuse on live base | hybrid | used | whether `r4_s10` scales cleanly onto the simplest live parent | better close with similar early behavior to `r4_s01` | high |
| `r4_w2_10_vex_trade_to_book_light` | secondary | `VEX` | light execution gate only | hybrid | used from papers, not winners | whether Pack `E` idea survives when reduced to one axis | fill quality improves without killing branch | medium-high |
| `r4_w2_11_vex_family_pressure_light` | exploratory | `VEX + family context` | one compact family-pressure proxy | hybrid | validation | whether family-state adds incremental timing value over `5200` veto | changes decisions in distinct windows from `5200` | medium |
| `r4_w2_12_5300_spread_conditioned_parent_gate` | secondary | `VEX + VEV_5300` | deploy `5300` only when parent book quality is clean | hybrid | used from uploaded winner architecture | whether active overlay failures are parent-book driven | `5300` trades occur in cleaner parent states only | medium |
| `r4_w2_13_4000_forced_activation` | primary | `VEX + VEV_4000` | simplify thresholds until direct `4000` intent is visible | data-driven | none | whether `4000` is genuinely tradeable online | direct `VEV_4000` inventory or quotes appear | highest |
| `r4_w2_14_4000_benign_tape_only` | secondary | `VEX + VEV_4000` | add one benign-tape filter after forcing activation | hybrid | validation | whether Pack `B` only needed lighter context, not abandonment | direct `4000` activation still survives after filter | medium-high |
| `r4_w2_15_4000_quote_ladder_probe` | secondary | `VEV_4000` focused | strike-specific quote ladder around simple value | paper-inspired | used from uploaded winner architecture | whether `4000` is execution-limited rather than no edge | quote placement produces direct `4000` engagement | high |

## Prioritized Candidate Queue

| Order | Candidate ID | Why This Early | Expected Decision Value |
| --- | --- | --- | --- |
| 1 | `r4_w2_01_vex_late_no_new_entry` | strongest repeated failure mode and cheapest rescue test | confirms whether live base is salvageable |
| 2 | `r4_w2_08_5300_with_5200_veto` | best new context signal on the most interesting active family | tests a high-ROI combination without feature dumping |
| 3 | `r4_w2_13_4000_forced_activation` | closes the largest attribution hole left by Wave 1 | tells us whether `4000` is alive at all |
| 4 | `r4_w2_05_5300_clean_value_retest` | establishes clean current-round `5300` baseline | separates active-family life from stale narrative |
| 5 | `r4_w2_09_vex_plus_5200_veto` | simplest clean reuse of the best contextual feature | checks portability onto the safest parent |
| 6 | `r4_w2_02_vex_peak_giveback_stop` | second-best retention axis after no-new-entry | distinguishes timing from exit-control failure |
| 7 | `r4_w2_15_4000_quote_ladder_probe` | uses winner-inspired execution ideas without old-product baggage | separates execution-limited from no-edge |
| 8 | `r4_w2_06_5300_horizon_hold_v2` | tests whether `5300` failure is mostly hold design | retention diagnosis for active family |
| 9 | `r4_w2_07_5300_queue_takeover_probe` | probes execution style on the most plausible active leg | high learning if `5300` is fill-constrained |
| 10 | `r4_w2_10_vex_trade_to_book_light` | keeps Pack `E` alive in a disciplined form | tells us if execution overlay still matters |
| 11 | `r4_w2_14_4000_benign_tape_only` | only worth paying after direct activation is proven | determines whether context helps `4000` |
| 12 | `r4_w2_12_5300_spread_conditioned_parent_gate` | compact parent-quality overlay from winner architecture | shows whether parent-book gating is enough |
| 13 | `r4_w2_03_vex_toxic_window_cooldown` | useful but partly overlaps with pure veto reuse | narrower answer than top retention tests |
| 14 | `r4_w2_04_vex_smaller_second_clip` | lower-conviction sizing diagnosis | useful only if base still bleeds after timing fixes |
| 15 | `r4_w2_11_vex_family_pressure_light` | interesting but lower-confidence incremental context | likely dominated by `5200` veto unless distinct windows appear |

## Decision Trace

| Candidate | Signals Used | Alternative Rejected | Why Selected | Caveat |
| --- | --- | --- | --- | --- |
| `r4_w2_01` | `r4_w1_i04`, Pack `A` path shape | broad `VEX` rewrite | cheapest direct retention rescue | may undertrade if cutoff is too early |
| `r4_w2_02` | `r4_w1_i04` | composite exit stack | isolates giveback control cleanly | stop logic can be noisy on tiny sample |
| `r4_w2_03` | `r4_w1_i03`, `r4_w1_i04` | hard whole-bot veto | keeps thesis alive while testing narrow warning window | partly overlaps with `r4_w2_09` |
| `r4_w2_04` | Pack `A/B/D` late extra sell pattern | full inventory rewrite | tests whether damage is clip-sizing, not signal | weak if only one late clip exists |
| `r4_w2_05` | `5300` carry-forward + round understanding | broad active basket reopen | cleanest current-round `5300` attribution test | canonical Pack `C` proof still pending |
| `r4_w2_06` | `5300` carry-forward + retention thesis | richer `5300` composite | targets `edge then reversal` directly | depends on `5300` actually engaging |
| `r4_w2_07` | uploaded winner architecture | full old IV-window port | high information execution probe with minimal baggage | fair value proxy must stay simple |
| `r4_w2_08` | `r4_w1_i03`, `5300` carry-forward | hard defensive bot | best likely combination of live edge and useful context | still needs clean `5300` activation |
| `r4_w2_09` | `r4_w1_i03`, `r4_s01` | raw-name alpha reopen | simplest portability test for the veto | may just redescribe `r4_w2_01` windows |
| `r4_w2_10` | Pack `E` hypothesis, `cartea_2018` | full Pack `E` reopen | execution overlay only, no feature pile | current-round evidence still incomplete |
| `r4_w2_11` | family-state EDA, `kaeck_2019` | full family composite | keeps unresolved family question alive cheaply | low confidence incremental value |
| `r4_w2_12` | uploaded winner spread discipline | explicit hedge machinery port | tests parent-book quality with one compact gate | may be too similar to trade-to-book light |
| `r4_w2_13` | `r4_w1_i02` | giving up on `4000` | required before any honest `4000` conclusion | activation may require unattractive thresholds |
| `r4_w2_14` | `r4_w1_i02`, benign-flow theme | repeat current Pack `B` composite | only one added filter after activation | still useless if `4000` never engages |
| `r4_w2_15` | uploaded winner ladder / queue discipline | rich IV or Greek engine | tests execution-limited hypothesis cleanly | must not drift into market-making complexity |

## Rejected Or Deferred Ideas

| Idea | Reason | Reopen Only If |
| --- | --- | --- |
| new standalone `HYDRO` branches | Wave 1 already gave zero-engagement negative evidence | linked-product role becomes compelling |
| another broad 15-bot context family using many correlated filters | too much attribution contamination | a small parent branch shows very strong lift |
| direct `5100/5200` inventory branches | best current role is contextual, not inventory | a clean isolated run shows real positive markout |
| full IV-surface or volcanic-style prior winner port | incompatible products and complexity too high | a tiny online proxy shows clear lift first |

## Stop Rule

Wave 2 should stop after these `15` candidates because the remaining branches
would mostly be:

- duplicates of the same retention question
- context overlays on already weak parents
- richer versions of the uploaded winner architecture without current-round fit
- or retests that should wait for canonical Pack `C/E/F` summaries

## Handoff To Phase 04

Write grouped specs in this order:

1. Pack `G` retention rescue
2. Pack `H` `5300` isolation and current-round exploitation
3. Pack `J` honest `4000` attribution closure
4. Pack `I` light context overlays on proven parents

The preferred implementation order should mirror the prioritized queue rather
than forcing all `15` bots into one immediate batch.
