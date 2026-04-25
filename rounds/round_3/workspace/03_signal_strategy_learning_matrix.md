# Round 3 Signal And Learning-Bot Matrix

## Purpose

This artifact expands the Round 3 strategy space from "best current composite"
into a learning-first bot matrix. The goal of the next upload batch is to
learn:

- which signals survive on the live `TTE=5d` day,
- which products or strike subsets are worth promoting,
- which branches should be pruned,
- which failures are signal failures versus execution failures.

## Source Inputs

- [`03_strategy_candidates.md`](03_strategy_candidates.md)
- [`02_understanding.md`](02_understanding.md)
- [`01_eda/eda_option_surface_and_microstructure.md`](01_eda/eda_option_surface_and_microstructure.md)
- [`post_run_research_memory.md`](post_run_research_memory.md)
- [`06_testing/round_3_historical_performance_analysis.md`](06_testing/round_3_historical_performance_analysis.md)
- [`06_testing/round_3_canonical_run_analysis.md`](06_testing/round_3_canonical_run_analysis.md)

## Product Signal Map

| Product / Family | Current Signal View | Learning Priority | Notes |
| --- | --- | --- | --- |
| `HYDROGEL_PACK` | live reversion + live imbalance still present; execution historically poor | high | isolate before trusting in composites |
| `VELVETFRUIT_EXTRACT` | cleanest live delta-1 book; positive contribution in current runs | high | standalone edge + voucher anchor |
| `VEV_4000` | strongest live residual reversion | very high | candidate for direct promotion path if isolated run holds |
| `VEV_4500` | strong live residual reversion | very high | pair with `VEV_4000` and with VEX |
| `VEV_5000` | weak but still directionally mean-reverting | medium/high | keep as learning branch, not default leader |
| `VEV_5100` | weak live residual reversion, strong VEX coupling | medium | test in isolation before pruning |
| `VEV_5200` | main losing strike in current challengers | very high | must be isolated to confirm reject / rescue decision |
| `VEV_5300` | only active strike that stayed consistently positive in current composite runs | very high | strongest active-strike learner |
| `VEV_5400` | live movement + tight spreads | high | previously deferred, now reopened |
| `VEV_5500` | live movement + very tight spreads | high | high-ROI upper-strike learner |
| `VEV_6000` | frozen at `0.5` | low | monitor / diagnostic only |
| `VEV_6500` | frozen at `0.5` | low | monitor / diagnostic only |

## Signal / Strategy Families

| Family ID | Family | Products | Status | Why It Matters |
| --- | --- | --- | --- | --- |
| `F01` | delta-1 mid reversion MM | `HYDRO`, `VEX` | known, under-isolated | core microstructure learner |
| `F02` | delta-1 imbalance-led MM | `HYDRO`, `VEX` | known, under-isolated | live imbalance still looks predictive |
| `F03` | dual delta-1 independent combo | `HYDRO + VEX` | known, needs cleaner rerun | tests whether the two streams still add independently |
| `F04` | centered intrinsic/extrinsic residual | vouchers by strike | not yet cleanly isolated | strongest learning axis after current failures |
| `F05` | ITM intrinsic residual | `VEV_4000/4500` | historically strongest branch | best current path to a strong learner |
| `F06` | active-strike residual | `VEV_5000-5300` | mixed / partially failing | needs strike-level breakup |
| `F07` | upper-strike residual | `VEV_5400/5500` | newly reopened | logger says these are active enough |
| `F08` | surface relative-value spread | adjacent voucher strikes | not previously implemented cleanly | useful when absolute residual is noisy but local shape mean-reverts |
| `F09` | inventory-clean residual | voucher subsets | partially tried, not solved | keep as axis, but after strike isolation |
| `F10` | VEX + voucher combo | `VEX` plus voucher subset | partially observed | tests whether positive VEX leg helps specific voucher branches |
| `F11` | passive upper-strike maker | `VEV_5400/5500` | not previously isolated | tight spreads justify passive experiments |
| `F12` | floor watcher / no-trade monitor | `VEV_6000/6500` | diagnostic only | keep coverage without spending bot budget |

## Full Bot Backlog

This is the complete current learning-bot backlog, including lower-priority
diagnostics. The top-25 batch below is the implemented priority cut.

| Bot ID | Family | Products | Goal | Priority |
| --- | --- | --- | --- | --- |
| `L01` | delta-1 reversion | `HYDRO` | isolate pure hydro mean reversion | high |
| `L02` | delta-1 imbalance | `HYDRO` | separate hydro imbalance from hydro reversion | high |
| `L03` | delta-1 passive wide-spread | `HYDRO` | test whether hydro fails because it crosses too much | medium |
| `L04` | delta-1 reversion | `VEX` | isolate pure VEX mean reversion | high |
| `L05` | delta-1 imbalance | `VEX` | isolate VEX imbalance edge | high |
| `L06` | dual delta-1 combo | `HYDRO + VEX` | test clean independent additivity | high |
| `L07` | ITM residual | `VEV_4000` | strongest single-strike ITM test | very high |
| `L08` | ITM residual | `VEV_4500` | second single-strike ITM test | very high |
| `L09` | ITM residual pair | `VEV_4000 + VEV_4500` | test combined ITM branch | very high |
| `L10` | ITM residual + VEX | `VEX + VEV_4000 + VEV_4500` | reproduce the strongest historical family in cleaner form | very high |
| `L11` | ITM passive | `VEV_4000 + VEV_4500` | test whether ITM needs more passive execution | medium |
| `L12` | active residual | `VEV_5000` | isolate `5000` | high |
| `L13` | active residual | `VEV_5100` | isolate `5100` | high |
| `L14` | active residual | `VEV_5200` | confirm whether `5200` is truly toxic | very high |
| `L15` | active residual | `VEV_5300` | isolate best active strike | very high |
| `L16` | active residual subset | `VEV_5000 + VEV_5300` | remove suspect middle strikes | very high |
| `L17` | active residual subset | `VEV_5100 + VEV_5300` | keep strongest VEX-coupled active strike plus `5300` | high |
| `L18` | active residual subset | `VEV_5200 + VEV_5300` | test whether `5200` only fails in the broader basket | high |
| `L19` | active residual subset | `VEV_5000 + VEV_5100 + VEV_5300` | full active branch excluding `5200` | very high |
| `L20` | inventory-clean active residual | `VEV_5000 + VEV_5300` | keep inventory axis but on a cleaner subset | high |
| `L21` | upper residual | `VEV_5400` | isolate `5400` | high |
| `L22` | upper residual | `VEV_5500` | isolate `5500` | high |
| `L23` | upper residual pair | `VEV_5400 + VEV_5500` | combined upper branch | high |
| `L24` | upper passive maker | `VEV_5400 + VEV_5500` | test one-tick passive upper execution | high |
| `L25` | VEX + active best strike | `VEX + VEV_5300` | combine two positive live legs | high |
| `L26` | surface relative value | `VEV_5200 vs VEV_5300` | test local surface spread mean reversion | high |
| `L27` | surface relative value | `VEV_5300 vs VEV_5400` | test upper/local surface transition | high |
| `L28` | surface relative value | `VEV_5000-VEV_5500` ladder | broader local-shape probe | medium |
| `L29` | upper hybrid | `VEV_5300 + VEV_5400 + VEV_5500` | bridge active and upper branch | medium/high |
| `L30` | VEX + upper | `VEX + VEV_5400 + VEV_5500` | test upper branch with anchor sidecar | medium |
| `L31` | floor watcher | `VEV_6000 + VEV_6500` | monitor only; verify floor still holds | low |
| `L32` | floor passive experiment | `VEV_6000 + VEV_6500` | ultra-low-priority one-tick passive test | very low |

## Prioritized Batch To Implement Now

The user-set cap for this round of learning uploads is `25`. The batch below is
the implemented priority cut.

| Bot ID | Why It Made The Cut |
| --- | --- |
| `L01` | HYDRO signal still exists live; execution needs isolation |
| `L02` | HYDRO imbalance may survive better than hydro pure reversion |
| `L04` | VEX standalone learner is mandatory |
| `L05` | VEX imbalance learner is mandatory |
| `L06` | clean delta-1 combo baseline |
| `L07` | strongest live ITM strike |
| `L08` | second strongest live ITM strike |
| `L09` | clean ITM pair |
| `L10` | strongest historical family in cleaner form |
| `L12` | isolate `VEV_5000` |
| `L13` | isolate `VEV_5100` |
| `L14` | isolate `VEV_5200` and decide whether to kill it |
| `L15` | isolate `VEV_5300`, best active strike |
| `L16` | active subset without `5100/5200` |
| `L17` | test `5100` only in presence of `5300` |
| `L18` | test whether `5200` only fails in wider baskets |
| `L19` | full active branch excluding `5200` |
| `L20` | inventory axis on a cleaner active subset |
| `L21` | reopen `5400` |
| `L22` | reopen `5500` |
| `L23` | combined upper residual branch |
| `L24` | passive upper execution branch |
| `L25` | best active strike plus best delta-1 anchor leg |
| `L26` | direct test of the `5200/5300` misallocation |
| `L27` | direct test of the `5300/5400` surface transition |

## What Is Explicitly Not In The Top-25 Batch

- `L03`: keep as a later hydro execution follow-up if `L01/L02` still fail.
- `L11`: ITM passive variation is lower ROI than the direct ITM branch first.
- `L28`: full ladder relative-value is too broad before the smaller pair probes.
- `L29/L30`: useful, but less urgent than isolated strike/pair learning.
- `L31/L32`: keep out of the bot budget unless the live floor regime breaks.

## Batch Design Rules

- Keep learners small and interpretable.
- One main idea per bot.
- Prefer isolated products or small subsets over global composites.
- Use the live `TTE=5d` logger evidence as the primary product-selection filter.
- Treat `VEV_6000/6500` as monitoring only unless new contradictory evidence appears.
- Treat `VEV_5200` as "must re-earn inclusion."

## Recommended Reading Order For The Next Agent

1. [`06_testing/round_3_canonical_run_analysis.md`](06_testing/round_3_canonical_run_analysis.md)
2. [`post_run_research_memory.md`](post_run_research_memory.md)
3. [`04_strategy_specs/spec_learning_batch_wave1.md`](04_strategy_specs/spec_learning_batch_wave1.md)
4. [`05_implementation/learning_batch_wave1_manifest.md`](05_implementation/learning_batch_wave1_manifest.md)
