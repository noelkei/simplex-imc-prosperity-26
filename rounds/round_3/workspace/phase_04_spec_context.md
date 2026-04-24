# Phase 04 - Spec Context

## Status

READY_FOR_REVIEW

## Owner / Reviewer

- Owner: amin
- Reviewer: Unassigned

## Last Updated

2026-04-24

## What Has Been Done

- Wrote `spec_c06_composite_base.md` for C06 (composite Trader: C01+C02+C03).
- Wrote `spec_c06_composite_inv.md` for C06-inv (variant: C01+C02+C04 with inventory skew, imbalance confirmation, TTE-cautious thresholds).
- Both specs are `deferred under deadline` for fast-mode implementation.
- Feature Contracts defined for all 8 features (F1-F6 in base, F7-F8 added in variant).
- Round-Specific Mechanics Contract filled.

## Current Findings

- Two distinct approaches: base (simpler, relies on raw residual reversion) vs inventory variant (adds inventory skew + imbalance confirmation + wider thresholds).
- Both share the same Bachelier pricing backbone and delta-1 MM logic.

## Decisions Made

- Deadline deferral for both specs: no time for formal review cycle.
- Two bots will be tested to compare approaches.

## Open Questions / Blockers

- None blocking implementation.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`04_strategy_specs/spec_c06_composite_base.md`](04_strategy_specs/spec_c06_composite_base.md)
- [`04_strategy_specs/spec_c06_composite_inv.md`](04_strategy_specs/spec_c06_composite_inv.md)

## Next Priority Action

Validate both implementations and compare performance.

## Deadline Risk

Unknown.
