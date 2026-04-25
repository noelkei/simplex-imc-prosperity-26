# Round 3 Next-Wave Bot Planning

## Status

READY_FOR_REVIEW

## Objective

Turn the current Round 3 evidence into a **clean next-wave decision artifact**
before writing new specs or bots. This document answers:

- which old backlog ideas are still untested and worth carrying forward,
- which paper-derived ideas were really tested versus only partially covered,
- which new hypotheses appeared after the 39-run synthesis and the path-quality
  analysis,
- which branches should now be paused or hard-pruned,
- what the next bot batch should optimize for.

## Source Inputs

- [`03_strategy_candidates.md`](03_strategy_candidates.md)
- [`03_signal_strategy_learning_matrix.md`](03_signal_strategy_learning_matrix.md)
- [`06_testing/round_3_full_performance_synthesis.md`](06_testing/round_3_full_performance_synthesis.md)
- [`06_testing/artifacts/full_synthesis/full_run_metrics.csv`](06_testing/artifacts/full_synthesis/full_run_metrics.csv)
- [`06_testing/artifacts/full_synthesis/full_path_family_summary.csv`](06_testing/artifacts/full_synthesis/full_path_family_summary.csv)
- [`06_testing/artifacts/full_synthesis/full_path_reversal_candidates.csv`](06_testing/artifacts/full_synthesis/full_path_reversal_candidates.csv)
- [`post_run_research_memory.md`](post_run_research_memory.md)
- 8 processed paper summaries under `../research/papers_processed/`

## Executive Planning Verdict

- The next wave should be **smaller and sharper** than Wave 1. We no longer
  need another 25-bot scattershot batch.
- Recommended next-wave size: **12 to 16 bots**, not 25 by default.
- The base architecture should be **delta-1 first**.
- `ITM` survives as an **overlay / execution refinement** branch.
- Selective active vouchers are still alive only as a **path-rescue** branch:
  they showed entry edge in several runs, but not retention.
- `VEV_5100` and `VEV_5200` should be treated as **excluded by default**.
- The current surface branch should be **paused**, not expanded.
- The upper branch stays **research-only**, with at most one or two tightly
  scoped follow-ups if capacity remains.

## Decision Rules For The Next Wave

Every new bot should satisfy at least one of these:

1. It tests an old backlog idea that is still genuinely untested.
2. It tests a paper-derived idea that has not yet had a clean online test.
3. It tests a new hypothesis created by the path analysis.
4. It materially reduces uncertainty on the champion architecture.

And every new bot should avoid these:

1. Re-running a branch that is already strongly rejected without a new thesis.
2. Mixing too many axes at once.
3. Spending bot budget on pure diagnostics unless the hypothesis is otherwise
   unobservable.
4. Treating all negative-final runs as equally bad.

## Coverage Audit Against The Old Backlog

### Untested Backlog Items From The Original Wave 1 Matrix

These are the items from the original learner backlog that were **not**
implemented in the 25-bot Wave 1 batch.

| Bot ID | Original Idea | Current Relevance | Carry Forward? | Why |
| --- | --- | --- | --- | --- |
| `L03` | HYDRO passive / wider-spread execution | still relevant | yes | HYDRO is now clearly alive, so execution-style follow-up has high ROI |
| `L11` | ITM passive pair | still relevant | yes | ITM looks low-damage but under-monetized; passive execution is a fair missing test |
| `L28` | full local surface ladder | lower relevance | no for now | current surface family looks structurally wrong; broader ladder is premature |
| `L29` | active/upper bridge (`5300 + 5400 + 5500`) | medium/low | maybe later | useful only after deciding whether upper stays open |
| `L30` | `VEX + upper` combo | medium | maybe later | one reasonable upper follow-up if capacity remains |
| `L31` | floor watcher | low | no bot needed now | the logger and current evidence already cover the floor regime sufficiently |
| `L32` | floor passive experiment | very low | no | not worth bot budget unless the floor visibly breaks |

### Interpretation

- There are only **2 clearly carry-forward old backlog items** right now:
  `L03` and `L11`.
- The rest of the old untested backlog should **not** automatically roll into
  the next wave.

## Coverage Audit Against Formal Strategy Families

| Family | Current Coverage | Coverage Quality | Verdict |
| --- | --- | --- | --- |
| `C01` HYDRO delta-1 | tested directly in `L01`, `L02`, `L06` | clean | covered well |
| `C02` VEX delta-1 | tested directly in `L04`, `L05`, `L06` | clean | covered well |
| `C03` active residual | tested broadly and by strike/subset | mixed | covered, but branch now split into `reject` versus `rescue via exits` |
| `C04` inventory overlay | tested on broad basket and one clean subset (`L20`) | partial | still not fully resolved on the surviving subset |
| `C05` ITM residual | tested directly and with VEX | good | covered enough to demote to overlay, but passive execution remains missing |
| `C06` broad composite | tested repeatedly | clean enough | reject as broad architecture |
| `C07` expiry caution | only tested in old broad form (`B06`) | weak / contaminated | needs redesign if kept alive |

### Interpretation

- The biggest remaining formal gap is **not a missing product family**. It is a
  missing **clean test of expiry-aware / path-aware exit logic** on the
  surviving selective voucher subset.

## Paper Coverage Audit

| Paper | Intended Round-3 Use | Cleanly Tested? | Current Verdict | Next-Wave Handling |
| --- | --- | --- | --- | --- |
| `choi_2022_bachelier_guide` | fair-value backbone for vouchers | partial | broad Bachelier-style paths failed, but selective subset retest is still missing | carry forward on `5300` and `5000 + 5300` only |
| `stoikov_saglam_2009_option_mm_inventory` | inventory-aware quote skew | partial | broad-basket version failed; clean-subset inventory helped somewhat in `L20` | carry forward only on selective subset |
| `muravyev_2015_option_order_flow` | imbalance as modifier / caution | partial | imbalance works on delta-1, but voucher imbalance-as-filter was not cleanly tested | carry forward on selective active and maybe upper passive |
| `garcia_ares_2023_expiration_days` | expiry caution near `TTE=5d` | partial / weak | old broad cautious bot is not enough; path analysis now makes this more relevant, not less | carry forward in redesigned fast-exit / late-session-flattening form |
| `fengler_2005_surface_smoothing` | shape guardrail | yes as guardrail, no as alpha | surface as standalone alpha is weak; guardrail use still valid | keep as validation only, not a new family |
| `bergault_2022_multi_asset_mm` | family-level inventory coupling | not really | no fair live test yet | only reopen after selective subset survives simpler tests |
| `crr_1979_simplified_approach` | alternative pricing benchmark | not really | no evidence it deserves immediate online bot budget | keep as research benchmark, not next-wave bot priority |
| `west_2004_cumulative_normal` | math helper quality | yes enough | infrastructure only | no separate bot implication |

### Interpretation

- The papers do **not** justify reopening a broad voucher or surface wave.
- The strongest paper-derived gaps still alive are:
  - selective **Bachelier** retests,
  - selective **inventory** overlays,
  - redesigned **expiry-caution / fast-unwind** bots,
  - selective **imbalance-as-filter** bots.

## New Hypotheses Created By The 39-Run Synthesis

These hypotheses did **not** exist clearly before the path analysis.

| Hypothesis ID | New Hypothesis | Evidence | Priority |
| --- | --- | --- | --- |
| `NH01` | Some selective active-voucher bots have **entry edge but broken retention** | many active losers peaked strongly intra-run before collapsing | very high |
| `NH02` | The next active-voucher tests should optimize **faster profit capture** rather than only better fair-value estimation | path reversals are often late and severe | very high |
| `NH03` | Late-session behavior may be toxic for selective active vouchers, so **time-based shutdown / flattening** deserves a clean test | many reversal peaks occurred deep into the session | high |
| `NH04` | `VEV_5300` deserves treatment as a **combo leg only**, not as a standalone promoted winner | `L15` is still negative, `L25` is positive only because VEX dominates | high |
| `NH05` | Selective Bachelier retests should be run only after **hard-pruning `5100/5200`** | those two strikes remain the strongest negative evidence | very high |
| `NH06` | The surface family currently looks like **wrong signal / wrong implementation**, not merely a closing problem | `L26` showed almost no positive path | very high |
| `NH07` | Upper strikes might still deserve one refined passive / anchored test, but they are not a promotion path today | upper losses are small relative to active, and passive got zero fills | medium |

## Hard Exclusions And Pauses

### Exclude By Default

- `VEV_5100`
- `VEV_5200`
- broad active baskets such as `5000 + 5100 + 5200 + 5300`
- broad centered composites of the old `C06` type

### Pause Unless A New Theory Appears

- pure surface relative-value branch
- full surface ladder bots
- floor watcher / floor passive bots as upload budget consumers

### Keep Only As Narrow Research Branch

- upper-strike residual family
- `VEX + upper` hybrid
- portfolio-style family inventory coupling beyond the simple selective subset

## What The Next Wave Should Actually Optimize For

The next wave should not maximize branch count. It should maximize:

1. confidence in the **champion base family**,
2. confidence in whether selective active vouchers can be **rescued by exits**,
3. confidence in whether `ITM` deserves a **passive execution follow-up**,
4. coverage of the most important **paper-derived gaps** still open.

## Recommended Next-Wave Structure

### Bucket A: Champion Controls

Purpose: confirm what the new base architecture is built around.

- delta-1 base control
- delta-1 plus ITM overlay control
- delta-1 plus selective active overlay control

### Bucket B: Untested Old Backlog With High ROI

Purpose: close the only two old gaps that still matter.

- `L03` HYDRO passive / wider-spread execution
- `L11` ITM passive pair

### Bucket C: Selective Voucher Rescue

Purpose: test whether the surviving active subset has real edge that can be
retained with better exit logic.

- `5300` fast take-profit / time-stop
- `5000 + 5300` fast take-profit / time-stop
- `5300` late-session shutdown / flattening
- `5000 + 5300` late-session shutdown / flattening
- `5000 + 5300` inventory overlay on top of the above, not as a standalone first test
- `VEX + 5300` fast-unwind combo

### Bucket D: Paper-Gap / Research Slots

Purpose: cover ideas that matter but were not cleanly tested yet.

- selective Bachelier retest on `5300`
- selective Bachelier retest on `5000 + 5300`
- voucher imbalance-as-filter on the surviving subset
- one optional upper passive / anchored refinement if capacity remains

## Recommended Candidate Queue

This is the recommended **next-wave queue**, ordered by decision value rather
than by implementation convenience.

| Queue ID | Type | Main Hypothesis | Products | Why It Should Exist |
| --- | --- | --- | --- | --- |
| `W2-01` | control | delta-1-only should be the new base champion control | `HYDRO + VEX` | keeps a clean comparison point for every overlay |
| `W2-02` | carry-forward | HYDRO needs a passive/wider-spread variant before we call its execution solved | `HYDRO` | closes `L03` cleanly |
| `W2-03` | carry-forward | ITM may need more passive execution rather than more model complexity | `VEV_4000 + VEV_4500` | closes `L11` cleanly |
| `W2-04` | overlay control | `delta-1 + ITM` is the best low-risk overlay architecture | `HYDRO + VEX + VEV_4000 + VEV_4500` | tests whether ITM deserves to stay in the main stack |
| `W2-05` | paper-gap | selective Bachelier residual on `5300` still lacks a fair clean test | `VEV_5300` | tests Choi fairly after strike pruning |
| `W2-06` | paper-gap | selective Bachelier residual on `5000 + 5300` still lacks a fair clean test | `VEV_5000 + VEV_5300` | tests whether `5000` survives only next to `5300` |
| `W2-07` | path-rescue | `5300` has entry edge but needs fast take-profit / time-stop | `VEV_5300` | directly targets `edge then reversal` |
| `W2-08` | path-rescue | `5000 + 5300` has entry edge but needs fast take-profit / time-stop | `VEV_5000 + VEV_5300` | directly targets subset reversal |
| `W2-09` | path-rescue | late-session flattening can preserve active-voucher gains | `VEV_5300` | paper-aligned expiry caution in cleaner form |
| `W2-10` | path-rescue | late-session flattening can preserve subset gains | `VEV_5000 + VEV_5300` | tests whether session tail is the real killer |
| `W2-11` | paper-gap | inventory overlay helps only after strike pruning and fast exits | `VEV_5000 + VEV_5300` | cleaner Stoikov-style test than the broad basket |
| `W2-12` | combo | `VEX + 5300` can work if the voucher leg is unwound faster | `VEX + VEV_5300` | upgrades `L25` from descriptive to targeted |
| `W2-13` | paper-gap | imbalance should be tested as a filter, not a primary voucher alpha | `VEV_5300` or `VEV_5000 + VEV_5300` | clean Muravyev-style test |
| `W2-14` | optional research | upper passive / anchored refinement may still deserve one last slot | `VEX + VEV_5400 + VEV_5500` or `VEV_5400 + VEV_5500` | only if batch size exceeds 12 |

## Recommended Cut

If we want the **most efficient** next wave, the recommended cut is:

- Core cut: `W2-01` to `W2-12`
- Optional additions: `W2-13` and `W2-14`

That gives a recommended next-wave size of:

- **12 bots** for a sharp, high-ROI batch
- **14 bots** if we want a little more paper-gap and upper-branch coverage

## User-Directed Expanded Coverage Layer

The user additionally asked for better exploitation coverage across the full
tradable CSV universe, not only the strongest current branches. Under that
directive, a **quality-preserving expansion layer** is justified on top of the
14-bot core.

These extra slots should remain small, hypothesis-driven, and clearly marked as
coverage bots rather than promotion bots.

| Queue ID | Type | Main Hypothesis | Products | Why It Should Exist |
| --- | --- | --- | --- | --- |
| `W2-15` | coverage rescue | `VEV_5100` should only be reopened as a tiny-size anchored fast-unwind scalp, not as a normal active strike | `VEX + VEV_5100` or `VEV_5100 + VEV_5300` | gives one last controlled chance to a toxic-but-tradable strike |
| `W2-16` | coverage rescue | `VEV_5200` should only be reopened as a tiny-size anchored fast-unwind scalp, not as a normal active strike | `VEX + VEV_5200` or `VEV_5200 + VEV_5300` | covers the strike while respecting the strong negative evidence |
| `W2-17` | coverage bridge | the active/upper transition may be monetizable only when `5300` carries the branch | `VEV_5300 + VEV_5400 + VEV_5500` | broadens product coverage without reopening the whole basket |
| `W2-18` | coverage bridge | upper strikes may need VEX anchoring plus passive quoting to become tradable | `VEX + VEV_5400 + VEV_5500` | gives the upper family one last anchored test |
| `W2-19` | coverage microstructure | floor names may still offer tiny passive/floor-break opportunities if treated as micro probes, not directional bets | `VEV_6000 + VEV_6500` | provides deliberate coverage of the remaining tradable symbols |

### Expanded Batch Recommendation

Under the user-directed full-product-coverage goal, the recommended expanded
cut is:

- Core plus optional strategy slots: `W2-01` to `W2-14`
- Coverage-extension slots: `W2-15` to `W2-19`

That yields a **19-bot Wave 2**. This is still well below the round cap of
`25` and remains interpretable enough to validate cleanly.

## What Should Not Enter The Next Wave

- any new bot containing `VEV_5100` unless there is a fresh rescue thesis
- any new bot containing `VEV_5200` unless there is a fresh rescue thesis
- any broad active basket
- any broad surface family
- any floor watcher bot that consumes a real upload slot
- any “kitchen sink” composite mixing delta-1, ITM, active, upper, and surface

## Handoff

This artifact is intended to make the next step deterministic:

1. choose the cut size (`12` or `14`),
2. write the next-wave spec from `W2-01` onward,
3. only then implement the batch.

## Recommended Next Step

The spec step is now completed via
[`04_strategy_specs/spec_learning_batch_wave2.md`](04_strategy_specs/spec_learning_batch_wave2.md).

The next step is to:

1. review or explicitly deadline-defer that spec,
2. write the Wave 2 implementation manifest,
3. only then implement the batch.
