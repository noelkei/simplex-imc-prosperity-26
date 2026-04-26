# Phase 04 - Spec Context

## Status

COMPLETED

## Owner / Reviewer

- Owner: amin
- Reviewer: Unassigned

## Last Updated

2026-04-26

## What Has Been Done

- Wrote `spec_c06_composite_base.md` for C06 (composite Trader: C01+C02+C03).
- Wrote `spec_c06_composite_inv.md` for C06-inv (controlled C04 variant on top of the base spec).
- Wrote `spec_learning_batch_wave1.md` for the learning-first Wave 1 bot batch after the first live challenger runs failed.
- Wrote `spec_learning_batch_wave2.md` for the post-synthesis Wave 2 batch after the 39-run synthesis and next-wave planning pass.
- Explicitly deadline-deferred the Wave 2 spec after the user requested immediate implementation, and the spec has now been consumed by the concrete Wave 2 manifest and 19-bot canonical batch.
- Wrote `spec_learning_batch_wave3.md` for the final exploratory Wave 3 batch after the 58-run synthesis, refreshed planning artifact, and the user's follow-up requests on regime logic, inverse tests, transformed thresholds, trend gates, and Kalman.
- Wrote `spec_learning_batch_wave4.md` for the winner-focused 12-bot finalist
  batch after the full 82-run synthesis, the `>10k` retention study, and the
  final architecture planning pass.
- Wrote `spec_learning_batch_wave5.md` for the final exploitation /
  upside-distillation batch after the full 94-run synthesis, the Wave 4
  finalist comparison, and the focused `>10k` descendant planning pass.
- Corrected the base spec so the voucher signal uses an explicit online proxy for `extrinsic_dev_day` and the surface guardrail checks observed mids, not model fair values.
- Corrected the inventory variant so it stays on a clean C04 axis instead of mixing in TTE-cautious changes.
- The earlier C06 and Wave 1 specs remain `deferred under deadline` as historical implementation references.
- Feature Contracts are now aligned with the corrected challengers and round-specific mechanics; the tested legacy base is kept only as a historical comparison reference.
- After detecting the paired artifact for `candidate_c06_composite_base`, the tested legacy base was archived under `historical/`, the corrected base spec was first routed into `../bots/amin/canonical/candidate_c06_v01_centered_base.py`, and that tested challenger now also lives under `historical/`.

## Current Findings

- Two distinct corrected approaches were validated and then archived: base (`candidate_c06_v01_centered_base.py`) with centered residual + observed-surface guardrail, and the controlled inventory variant (`candidate_c06_composite_inv.py`) with the same core plus inventory skew + imbalance confirmation.
- Both archival specs still matter as evidence references, but they are no longer the next implementation target.
- The broad corrected active-voucher basket is no longer the next implementation target after the first live runs.
- The historical Wave 2 spec remains the last executed spec, but it is no longer the next design target.
- The refreshed strategy planning artifact now points to a much smaller Wave 3 cut focused on delta-1 exploitation, VEX-linked `5300` rescue, regime/no-trade logic, and optional tiny inverse diagnostics.
- The Wave 3 spec ultimately froze a `24`-bot last-exploration batch: `14` core decision bots plus `10` extension bots.
- The Wave 3 spec explicitly keeps HMM/Markov out, but includes transformed-threshold, lightweight trend, and Kalman variants where they remain online-usable and interpretable.
- The Wave 4 spec keeps the same online-usable boundaries but compresses the
  whole design space into four near-final questions: pure champion, champion
  plus ITM, whether `5300` deserves a micro-overlay slot, and whether `5100`
  deserves one last inverse closure test.
- The Wave 5 spec keeps the same online-usable boundaries, but converts them
  into the last major exploitation cut: winner protection, realistic
  timestamp-scale retention gates, distilled `>10k` descendants, and
  toxic-strike-as-signal variants.

## Decisions Made

- Historical specs used deadline deferral to preserve implementation velocity earlier in the round.
- The Wave 2 spec was also deferred under deadline once the user explicitly requested implementation.
- C07 remains separate from C06-inv so later validation can isolate inventory effects from TTE-calibration effects.
- The learning batch uses centered intrinsic / extrinsic residual learners, upper-strike passive/residual learners, and surface-pair learners as controlled next probes.
- Wave 2 is now specified as delta-1-first, with `L03/L11` carry-forwards, selective active-voucher rescue bots, and limited coverage bots for the remaining tradable symbols.
- Wave 3 is now specified as delta-1-first plus VEX-linked `5300` rescue, selective `VEX + ITM` refresh, tiny inverse toxic-strike diagnostics, and two Kalman tests.

## Open Questions / Blockers

- No factual spec blocker remains.
- The next uncertainty is no longer spec shape, but which Wave 5 bots win once
  they are run.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`04_strategy_specs/spec_c06_composite_base.md`](04_strategy_specs/spec_c06_composite_base.md)
- [`04_strategy_specs/spec_c06_composite_inv.md`](04_strategy_specs/spec_c06_composite_inv.md)
- [`04_strategy_specs/spec_learning_batch_wave1.md`](04_strategy_specs/spec_learning_batch_wave1.md)
- [`04_strategy_specs/spec_learning_batch_wave2.md`](04_strategy_specs/spec_learning_batch_wave2.md)
- [`04_strategy_specs/spec_learning_batch_wave3.md`](04_strategy_specs/spec_learning_batch_wave3.md)
- [`04_strategy_specs/spec_learning_batch_wave4.md`](04_strategy_specs/spec_learning_batch_wave4.md)
- [`04_strategy_specs/spec_learning_batch_wave5.md`](04_strategy_specs/spec_learning_batch_wave5.md)
- [`03_next_wave_bot_planning.md`](03_next_wave_bot_planning.md)
- [`05_implementation/learning_batch_wave2_manifest.md`](05_implementation/learning_batch_wave2_manifest.md)
- [`05_implementation/learning_batch_wave3_manifest.md`](05_implementation/learning_batch_wave3_manifest.md)
- [`05_implementation/learning_batch_wave4_manifest.md`](05_implementation/learning_batch_wave4_manifest.md)
- [`05_implementation/learning_batch_wave5_manifest.md`](05_implementation/learning_batch_wave5_manifest.md)

## Next Priority Action

Phase 04 is done again. The next step is platform execution of the Wave 5
final exploitation batch and post-run comparison.

## Deadline Risk

Unknown.
