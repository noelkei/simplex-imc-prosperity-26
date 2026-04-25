# Phase 04 - Spec Context

## Status

COMPLETED

## Owner / Reviewer

- Owner: amin
- Reviewer: Unassigned

## Last Updated

2026-04-25

## What Has Been Done

- Wrote `spec_c06_composite_base.md` for C06 (composite Trader: C01+C02+C03).
- Wrote `spec_c06_composite_inv.md` for C06-inv (controlled C04 variant on top of the base spec).
- Wrote `spec_learning_batch_wave1.md` for the learning-first Wave 1 bot batch after the first live challenger runs failed.
- Wrote `spec_learning_batch_wave2.md` for the post-synthesis Wave 2 batch after the 39-run synthesis and next-wave planning pass.
- Explicitly deadline-deferred the Wave 2 spec after the user requested immediate implementation, and the spec has now been consumed by the concrete Wave 2 manifest and 19-bot canonical batch.
- Corrected the base spec so the voucher signal uses an explicit online proxy for `extrinsic_dev_day` and the surface guardrail checks observed mids, not model fair values.
- Corrected the inventory variant so it stays on a clean C04 axis instead of mixing in TTE-cautious changes.
- The earlier C06 and Wave 1 specs remain `deferred under deadline` as historical implementation references.
- Feature Contracts are now aligned with the corrected challengers and round-specific mechanics; the tested legacy base is kept only as a historical comparison reference.
- After detecting the paired artifact for `candidate_c06_composite_base`, the tested legacy base was archived under `historical/`, the corrected base spec was first routed into `../bots/amin/canonical/candidate_c06_v01_centered_base.py`, and that tested challenger now also lives under `historical/`.

## Current Findings

- Two distinct corrected approaches were validated and then archived: base (`candidate_c06_v01_centered_base.py`) with centered residual + observed-surface guardrail, and the controlled inventory variant (`candidate_c06_composite_inv.py`) with the same core plus inventory skew + imbalance confirmation.
- Both archival specs still matter as evidence references, but they are no longer the next implementation target.
- The broad corrected active-voucher basket is no longer the next implementation target after the first live runs.
- The new implementation-ready spec is the post-synthesis learning batch that isolates branches, overlays, rescue logic, and full-universe coverage slots.
- The new Wave 2 spec is now the active implementation driver and is no longer blocked on review state.
- The Wave 2 cut uses a 14-bot high-confidence core plus a 5-bot coverage-extension layer because the user explicitly wants broader tradable-product coverage.

## Decisions Made

- Historical specs used deadline deferral to preserve implementation velocity earlier in the round.
- The Wave 2 spec was also deferred under deadline once the user explicitly requested implementation.
- C07 remains separate from C06-inv so later validation can isolate inventory effects from TTE-calibration effects.
- The learning batch uses centered intrinsic / extrinsic residual learners, upper-strike passive/residual learners, and surface-pair learners as controlled next probes.
- Wave 2 is now specified as delta-1-first, with `L03/L11` carry-forwards, selective active-voucher rescue bots, and limited coverage bots for the remaining tradable symbols.

## Open Questions / Blockers

- No immediate spec blocker remains.
- The next uncertainty is no longer spec shape; it is how the implemented Wave 2 batch performs live.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`04_strategy_specs/spec_c06_composite_base.md`](04_strategy_specs/spec_c06_composite_base.md)
- [`04_strategy_specs/spec_c06_composite_inv.md`](04_strategy_specs/spec_c06_composite_inv.md)
- [`04_strategy_specs/spec_learning_batch_wave1.md`](04_strategy_specs/spec_learning_batch_wave1.md)
- [`04_strategy_specs/spec_learning_batch_wave2.md`](04_strategy_specs/spec_learning_batch_wave2.md)
- [`03_next_wave_bot_planning.md`](03_next_wave_bot_planning.md)
- [`05_implementation/learning_batch_wave2_manifest.md`](05_implementation/learning_batch_wave2_manifest.md)

## Next Priority Action

Move to Phase 05/06 execution: the spec is complete enough for implementation, and the next decision must come from the first Wave 2 platform runs.

## Deadline Risk

Unknown.
