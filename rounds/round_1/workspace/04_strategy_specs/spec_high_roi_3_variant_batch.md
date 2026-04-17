# Round 1 Spec - High-ROI Three Variant Batch

## Review Status

- Status: `COMPLETED`
- Owner: Codex
- Reviewer: user approved exact three-variant implementation direction for platform testing
- Reviewed on: 2026-04-17

## Review Decision

- `_index.md` spec status: `approved with caveats`
- Approved for implementation: `yes`
- Reviewer decision notes: user requested creating exactly the three high-ROI variants for Prosperity upload after narrowing exploration to A2+B1, A3+B1, and a slight A1+B1 refinement.
- Required changes before coding: none; preserve IPR +80 behavior and change only ACO logic.

## Shared Scope

- Product scope: `ASH_COATED_OSMIUM`, `INTARIAN_PEPPER_ROOT`
- Wiki facts: both products have position limit +/-80; `Trader.run(state)` returns `result, conversions, traderData`; positive order quantity buys, negative sells.
- PnL bar: current best platform-style artifact is `candidate_10_bot02_carry_tight_mm`, total `10007.0`, IPR `7286.0`, ACO `2721.0`.
- Shared implementation rule: IPR module remains B1 max-long carry in every variant.
- Shared validation rule: a variant is only interesting if IPR remains near `7286.0` and ACO improves over `2721.0` or shows a useful execution tradeoff.

## Sources

- Strategy research: `../03_strategy_research_per_product_3x3.md`
- Advanced EDA: `../01_eda/eda_advanced_signal_research.md`
- Platform artifact analysis: `../../performances/noel/canonical/run_20260417_platform_artifact_analysis.md`
- Existing control implementation: `../../bots/noel/canonical/candidate_10_bot02_carry_tight_mm.py`

## Variant V1 - A1+B1 Size/Skew Refine

- Candidate ID: `candidate_24_v1_a1b1_size_skew_refine`
- Priority: high
- Evidence strength: strong
- Product scope: both, with only ACO modified

### Signal / Fair Value Logic

- IPR: B1 max-long carry, unchanged.
- ACO: fixed FV `10000`, same as A1.
- Missing-signal behavior: if ACO book is missing, place no ACO orders; if one side is missing, use only safe capacity-clipped orders from visible levels.

### Execution Logic

- Buy ACO below FV and sell ACO above FV as in A1.
- Make inventory-reducing orders more aggressive than inventory-adding orders.
- Reduce passive size on the side that would increase already large inventory.
- Preserve broad two-sided quoting so matched volume does not collapse.

### Risk / Failure Case

- Main risk: over-skewing reduces profitable fills.
- Mitigation: keep FV and crossing logic close to A1; only tune size and skew.

### Handoff

- Target bot: `rounds/round_1/bots/noel/canonical/candidate_24_v1_a1b1_size_skew_refine.py`

## Variant V2 - A2+B1 Conservative Regime Gate

- Candidate ID: `candidate_25_v2_a2b1_conservative_regime_gate`
- Priority: high
- Evidence strength: medium-strong
- Product scope: both, with only ACO modified

### Signal / Fair Value Logic

- IPR: B1 max-long carry, unchanged.
- ACO: fixed FV `10000` plus conservative residual, z-score/proxy, and Kalman-style innovation gates.
- Missing-signal behavior: if mid cannot be computed, fall back to A1-style fixed-FV execution.

### Execution Logic

- Default to A1 in normal ACO states.
- Require cleaner edge for add-side trades when residual, innovation, or inventory says adverse fills are more likely.
- Allow more favorable side quoting when residual regime agrees with FV mean reversion.
- Keep model inference O(1), hardcoded, and state-light.

### Risk / Failure Case

- Main risk: model filters starve ACO volume, as seen in some next-wave runs.
- Mitigation: conservative gate only changes thresholds/widths; it does not replace FV=10000 or B1.

### Handoff

- Target bot: `rounds/round_1/bots/noel/canonical/candidate_25_v2_a2b1_conservative_regime_gate.py`

## Variant V3 - A3+B1 One-Sided Exit Overlay

- Candidate ID: `candidate_26_v3_a3b1_one_sided_exit_overlay`
- Priority: medium-high
- Evidence strength: medium
- Product scope: both, with only ACO modified

### Signal / Fair Value Logic

- IPR: B1 max-long carry, unchanged.
- ACO: fixed FV `10000` plus book-state overlay using one-sided books and mild L1 imbalance.
- Missing-signal behavior: if imbalance cannot be computed, use zero imbalance; if no visible side exists, place no ACO order.

### Execution Logic

- Keep A1 as the core two-sided maker.
- On one-sided books, prioritize inventory-reducing exits at acceptable FV edge.
- Provide a conservative missing-side quote only when capacity and inventory make it safe.
- Use imbalance only as a mild quote skew; it cannot replace fixed FV.

### Risk / Failure Case

- Main risk: microstructure overlay overreacts to book bounce.
- Mitigation: overlay is narrow: one-sided exits and mild skew only.

### Handoff

- Target bot: `rounds/round_1/bots/noel/canonical/candidate_26_v3_a3b1_one_sided_exit_overlay.py`

## Validation Plan

- Run `python3 -m py_compile` on all three bot files.
- Run local immediate-fill replay if available; treat replay as sanity only, not final score.
- Upload each `.py` to Prosperity and save exact platform `.json` and `.log`.
- Rerun `rounds/round_1/performances/noel/canonical/analyze_platform_artifacts.py`.
- Rank by platform JSON `profit`; use final `activitiesLog` rows for IPR/ACO split.

