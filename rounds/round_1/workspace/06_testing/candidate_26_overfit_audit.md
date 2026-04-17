# Candidate 26 Overfit / Cheat Audit

## Decision

`candidate_26_v3_a3b1_one_sided_exit_overlay.py` does not appear to cheat, use sample-ending behavior, or depend on platform logs/results. It remains the recommended Round 1 upload candidate.

## File Audited

- Bot: `rounds/round_1/bots/noel/canonical/candidate_26_v3_a3b1_one_sided_exit_overlay.py`
- SHA-256: `18a52ebe6af5f4156427461d031cfca205105d85c3293ba1ae1cf0d940809edc`
- Platform JSON: `rounds/round_1/performances/noel/canonical/candidate_26_v3_a3b1_one_sided_exit_overlay.json`
- Platform log: `rounds/round_1/performances/noel/canonical/candidate_26_v3_a3b1_one_sided_exit_overlay.log`

## Checks Passed

- No use of `state.timestamp`.
- No use of day number, sample index, iteration count, end-of-run timing, or 1000/10000-run horizon logic.
- No final-liquidation, late-flatten, or close-before-sample-end rule.
- No reading of files, JSON artifacts, logs, graph logs, activities logs, or trade-history files.
- No `print`, logging, randomization, eval/exec, file IO, or external package use.
- No dependence on `own_trades`, `market_trades`, or `observations`.
- `traderData` is parsed and returned as a small JSON string, but no strategy state is actually accumulated from it.
- Products and limits match the Round 1 wiki facts: `ASH_COATED_OSMIUM`, `INTARIAN_PEPPER_ROOT`, and position limit `80` for both.
- Order signs match the wiki contract: positive buys, negative sells.
- Aggregate buy/sell capacity is clipped from the starting position for each product, matching the exchange's per-iteration side-cap enforcement.

## Strategy Constants Assessment

- `ACO_FV = 10000` is a fair-value assumption for Ash-Coated Osmium, not a reference to 10,000 final iterations.
- Numeric constants such as `2`, `3`, `5`, `12`, `18`, `35`, `40`, `42`, `60`, and `72` are execution thresholds, quote widths, inventory bands, and order sizes.
- These constants are tuned strategy parameters, so they can be overfit in the ordinary modeling sense, but they are not sample-count tricks or log-dependent hacks.

## Remaining Overfit Risk

- The main residual risk is normal parameter overfitting to available platform/sample behavior: fixed FV, quote widths, and one-sided thresholds may be less optimal on the final hidden 10k run.
- This risk is mitigated by the fact that `candidate_28` made the one-sided overlay stricter and still scored close to `candidate_26`, which supports the family rather than a single brittle setting.
- `candidate_27` underperformed, so soft flattening should not be promoted.

## Recommendation

Promote `candidate_26_v3_a3b1_one_sided_exit_overlay.py`. Use `candidate_28_v1_c26_strict_one_sided.py` only as a lower-PnL robustness backup, not as the primary submission.
