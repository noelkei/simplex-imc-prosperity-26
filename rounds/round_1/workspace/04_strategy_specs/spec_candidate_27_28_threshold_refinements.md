# Round 1 Spec - Candidate 27/28 Threshold Refinements

## Review Status

- Status: `COMPLETED`
- Owner: Codex
- Reviewer: user approved implementation request
- Reviewed on: 2026-04-17

## Review Decision

- `_index.md` spec status: `approved with caveats`
- Approved for implementation: `yes`
- Reviewer decision notes: user requested implementation of `candidate_27` and `candidate_28` after deciding threshold optimization has ROI, without adding new strategy families or sample-ending tricks.
- Required changes before coding: keep IPR +80 carry unchanged; only modify ACO threshold/execution behavior inherited from `candidate_26`.

## Shared Scope

- Parent bot: `rounds/round_1/bots/noel/canonical/candidate_26_v3_a3b1_one_sided_exit_overlay.py`
- Product scope: `ASH_COATED_OSMIUM`, `INTARIAN_PEPPER_ROOT`
- Wiki facts: both products have position limit +/-80; `Trader.run(state)` returns `result, conversions, traderData`; positive order quantity buys, negative sells.
- Evidence basis: `candidate_26` is the current platform-style leader at total `10090.46875`, with unchanged IPR `7286.0`, ACO `2804.46875`, final ACO position `9`, and no replay rejections/errors.
- Shared implementation rule: IPR module remains B1 max-long carry in every variant.
- Shared validation rule: local replay is only a contract/limit sanity check; promotion still requires Prosperity platform JSON/log.

## Candidate 27 - C26 Soft Flatten

- Candidate ID: `candidate_27_v1_c26_soft_flatten`
- Parent strategy: A3+B1 via `candidate_26`
- Changed axis: ACO risk band and inventory-reducing execution thresholds
- Insight being tested: `candidate_26` improved ACO but retained small final ACO inventory; a softer flatten band may keep most one-sided edge while reducing mark-to-market dependence.
- Falsification metric: if ACO replay volume/PnL collapses or platform ACO PnL drops below the `candidate_10` ACO bar, reject.

### Signal / Fair Value Logic

- IPR: B1 max-long carry, unchanged.
- ACO: fixed FV `10000` plus the existing one-sided/book-state overlay.
- Missing-signal behavior: if no ACO book or no visible side exists, place no ACO order.

### Execution Logic

- Keep `candidate_26` as the core.
- Start flattening ACO inventory earlier once absolute position is above a small band.
- Make inventory-reducing one-sided exits slightly more permissive.
- Make inventory-adding one-sided provision stricter.
- Keep two-sided passive quoting active, but reduce add-side size and improve flatten-side size when inventory is already directional.

### Risk / Failure Case

- Main risk: flattening too early loses profitable carry inside ACO oscillations.
- Mitigation: threshold changes are mild and do not change FV, product scope, IPR behavior, or runtime profile.

### Handoff

- Target bot: `rounds/round_1/bots/noel/canonical/candidate_27_v1_c26_soft_flatten.py`

## Candidate 28 - C26 Strict One-Sided

- Candidate ID: `candidate_28_v1_c26_strict_one_sided`
- Parent strategy: A3+B1 via `candidate_26`
- Changed axis: ACO one-sided threshold strictness
- Insight being tested: `candidate_26`'s uplift may come from one-sided opportunities, but some of that edge may be noisy; a stricter one-sided overlay tests whether the same structure is more robust.
- Falsification metric: if stricter one-sided gates reduce fills without improving platform robustness or final inventory quality, reject.

### Signal / Fair Value Logic

- IPR: B1 max-long carry, unchanged.
- ACO: fixed FV `10000` plus the existing book-state overlay.
- Missing-signal behavior: if no visible counterparty side exists, place no ACO order.

### Execution Logic

- Keep `candidate_26` two-sided ACO behavior unchanged.
- Tighten one-sided inventory exits for small inventory and require stronger edge for adding short/long exposure.
- Place missing-side passive quotes only when inventory or visible edge justifies doing so.
- Preserve capacity clipping and order-sign behavior from the parent.

### Risk / Failure Case

- Main risk: over-filtering removes the trades that made `candidate_26` better.
- Mitigation: this variant changes only one-sided logic, so platform comparison against `candidate_26` identifies whether the permissive overlay is real or noise.

### Handoff

- Target bot: `rounds/round_1/bots/noel/canonical/candidate_28_v1_c26_strict_one_sided.py`

## Validation Plan

- Run `python3 -m py_compile` on `candidate_26`, `candidate_27`, and `candidate_28`.
- Run the high-ROI immediate-fill replay including control `candidate_10`, historical `candidate_24`/`candidate_25`, and canonical `candidate_26`/`candidate_27`/`candidate_28`.
- Confirm `0` errors and `0` position-limit rejections.
- Upload `candidate_27` and `candidate_28` to Prosperity only if static checks and replay sanity pass.
- Rank platform results by JSON `profit`; use final `activitiesLog` rows for IPR/ACO split.
