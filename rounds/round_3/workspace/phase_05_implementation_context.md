# Phase 05 - Implementation Context

## Status

READY_FOR_REVIEW

## Owner / Reviewer

- Owner: amin
- Reviewer: Unassigned

## Last Updated

2026-04-26

## What Has Been Done

- Implemented the legacy composite reference, the corrected centered base, the corrected inventory variant, and the diagnostic state logger.
- Implemented the learning-first Wave 1 batch of 25 learner bots from `spec_learning_batch_wave1.md`.
- Generated `05_implementation/learning_batch_wave1_manifest.md` and compiled the whole Wave 1 batch.
- After the user uploaded paired platform artifacts, every tested Round 3 bot was moved from `canonical/` to `historical/`.
- After that archival step, `rounds/round_3/bots/amin/canonical/` was temporarily empty until Wave 2 was generated.
- Wrote `05_implementation/generate_learning_batch_wave2.py`, generated `05_implementation/learning_batch_wave2_manifest.md`, and materialized the full 19-bot Wave 2 batch under `../bots/amin/canonical/`.
- Ran `py_compile` successfully on the Wave 2 generator and all 19 generated Wave 2 bot files.
- After the user uploaded paired platform artifacts for the full Wave 2 batch, all 19 `candidate_w2_*` bots were also moved from `canonical/` to `historical/`.
- Wrote `05_implementation/generate_learning_batch_wave3.py`, generated `05_implementation/learning_batch_wave3_manifest.md`, and materialized the full 24-bot Wave 3 batch under `../bots/amin/canonical/`.
- Ran `py_compile` successfully on the Wave 3 generator and all 24 generated Wave 3 bot files.
- After the user uploaded paired platform artifacts for the full Wave 3 batch, all 24 `candidate_w3_*` bots were moved from `canonical/` to `historical/`.
- Wrote `05_implementation/generate_learning_batch_wave4.py`, generated
  `05_implementation/learning_batch_wave4_manifest.md`, and materialized the
  12-bot Wave 4 finalist batch under `../bots/amin/canonical/`.
- Ran `py_compile` successfully on the Wave 4 generator and all 12 generated
  Wave 4 bot files.
- After the user uploaded paired platform artifacts for the full Wave 4 batch,
  all 12 `candidate_w4_*` bots were moved from `canonical/` to
  `historical/`.
- Wrote `05_implementation/generate_learning_batch_wave5.py`, generated
  `05_implementation/learning_batch_wave5_manifest.md`, and materialized the
  12-bot Wave 5 exploitation / upside-distillation batch under
  `../bots/amin/canonical/`.
- Ran `py_compile` successfully on the Wave 5 generator and all 12 generated
  Wave 5 bot files.

## Current Findings

- The implementation work is no longer waiting on first runs; the whole Wave 1 batch has already been exercised on platform and analyzed.
- The strongest newly validated implementation family is the clean isolated delta-1 stack (`L01`, `L02`, `L04`, `L05`, `L06`).
- The Wave 1 active, upper, and surface learners were valuable for learning, but not ready for promotion.
- The Wave 2 implementation uses a single shared generator/template so the batch stays parameter-comparable while still respecting the spec's branch differences.
- `rounds/round_3/bots/amin/canonical/` is no longer holding active Wave 3 or
  Wave 4 challengers; both batches have already completed the
  canonical-to-historical lifecycle.
- The Wave 3 implementation keeps the shared-generator approach, but extends the engine with simple regime gates, transformed thresholds, lightweight trend gates, inverse direction mode, and compact Kalman state.
- The implementation bottleneck has now shifted from coding to analyzing the new Wave 3 evidence and deciding the winner-focused architecture cut.
- The implementation bottleneck has now shifted again from coding to post-Wave-4
  synthesis and Wave 5 design: decide whether to simply promote the clean
  finalists or to spend one last batch on distilled `>10k` upside descendants.
- The implementation bottleneck has now shifted back to platform execution:
  Wave 5 is coded and compile-clean, and the next uncertainty is live outcome
  rather than implementation mechanics.

## Decisions Made

- Tested bots with paired platform artifacts are frozen under `historical/`.
- The full Wave 1 implementation should now be treated as a completed learning batch, not as a pending queue.
- The next implementation wave should be redesigned from the full synthesis report rather than extended mechanically from the old manifest.
- The full 19-bot Wave 2 cut requested by the user was implemented, not reduced to the earlier 12-14 recommendation.
- Wave 2 bots have now completed that lifecycle: implemented in `canonical/`, run on platform, and archived to `historical/` once paired artifacts existed.
- The Wave 3 batch is explicitly intended as a last or penultimate exploratory wave, not as a blind coverage sweep.
- Wave 3 bots have now also completed that lifecycle: implemented in `canonical/`, run on platform, and archived to `historical/` once paired artifacts existed.
- Wave 4 intentionally stopped being a broad exploration batch. Its bots have
  now completed the full lifecycle: implemented in `canonical/`, run on
  platform, and archived to `historical/` once paired artifacts existed.
- Wave 5 intentionally keeps the shared-generator pattern while extending the
  engine with realistic timestamp-scale cutoffs, per-symbol entry caps,
  cooldowns, watch-only toxic-strike contexts, and transformed-threshold
  gating.

## Open Questions / Blockers

- No blocker on implementation mechanics remains.
- No implementation blocker remains before the next implementation pass.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`04_strategy_specs/spec_c06_composite_base.md`](04_strategy_specs/spec_c06_composite_base.md)
- [`04_strategy_specs/spec_c06_composite_inv.md`](04_strategy_specs/spec_c06_composite_inv.md)
- [`04_strategy_specs/spec_learning_batch_wave1.md`](04_strategy_specs/spec_learning_batch_wave1.md)
- [`04_strategy_specs/spec_learning_batch_wave2.md`](04_strategy_specs/spec_learning_batch_wave2.md)
- [`04_strategy_specs/spec_learning_batch_wave3.md`](04_strategy_specs/spec_learning_batch_wave3.md)
- [`04_strategy_specs/spec_learning_batch_wave4.md`](04_strategy_specs/spec_learning_batch_wave4.md)
- [`04_strategy_specs/spec_learning_batch_wave5.md`](04_strategy_specs/spec_learning_batch_wave5.md)
- [`05_implementation/learning_batch_wave1_manifest.md`](05_implementation/learning_batch_wave1_manifest.md)
- [`05_implementation/learning_batch_wave2_manifest.md`](05_implementation/learning_batch_wave2_manifest.md)
- [`05_implementation/generate_learning_batch_wave2.py`](05_implementation/generate_learning_batch_wave2.py)
- [`05_implementation/learning_batch_wave3_manifest.md`](05_implementation/learning_batch_wave3_manifest.md)
- [`05_implementation/generate_learning_batch_wave3.py`](05_implementation/generate_learning_batch_wave3.py)
- [`05_implementation/learning_batch_wave4_manifest.md`](05_implementation/learning_batch_wave4_manifest.md)
- [`05_implementation/generate_learning_batch_wave4.py`](05_implementation/generate_learning_batch_wave4.py)
- [`05_implementation/learning_batch_wave5_manifest.md`](05_implementation/learning_batch_wave5_manifest.md)
- [`05_implementation/generate_learning_batch_wave5.py`](05_implementation/generate_learning_batch_wave5.py)
- [`03_next_wave_bot_planning.md`](03_next_wave_bot_planning.md)
- [`06_testing/round_3_full_performance_synthesis.md`](06_testing/round_3_full_performance_synthesis.md)

## Next Priority Action

Implementation is ready again. The next step is to run the Wave 5 batch on the
platform and bring back the paired artifacts for final comparison.

## Deadline Risk

Unknown.
