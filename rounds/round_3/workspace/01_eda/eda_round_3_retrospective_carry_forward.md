# Round 3 Retrospective EDA Addendum

## Status

`READY_FOR_REVIEW`

## Question

What additional EDA-style conclusions became visible only after the full run
history existed, and which of those should be carried into `round_4` as
decision-relevant framing rather than left buried inside validation notes?

## Purpose

This addendum does not replace the original raw-data EDA in
[`eda_option_surface_and_microstructure.md`](eda_option_surface_and_microstructure.md).
It complements it with retrospective diagnostics that only became possible
after the `101`-run closeout synthesis existed.

Use this artifact to bridge:

- raw sample-data EDA,
- run-informed structural EDA,
- and carry-forward framing for `round_4`.

Primary numerical source:
[`../06_testing/round_3_full_performance_synthesis.md`](../06_testing/round_3_full_performance_synthesis.md)

## Data Sources

- Retrospective run-derived inputs:
  - [`../06_testing/artifacts/full_synthesis/full_run_metrics.csv`](../06_testing/artifacts/full_synthesis/full_run_metrics.csv)
  - [`../06_testing/artifacts/full_synthesis/full_trade_markout_by_product.csv`](../06_testing/artifacts/full_synthesis/full_trade_markout_by_product.csv)
  - [`../06_testing/artifacts/full_synthesis/full_trade_markout_by_run_product.csv`](../06_testing/artifacts/full_synthesis/full_trade_markout_by_run_product.csv)
  - [`../06_testing/artifacts/full_synthesis/full_high_peak_gt10k_runs.csv`](../06_testing/artifacts/full_synthesis/full_high_peak_gt10k_runs.csv)
  - [`../06_testing/artifacts/full_synthesis/full_high_peak_gt10k_product_giveback.csv`](../06_testing/artifacts/full_synthesis/full_high_peak_gt10k_product_giveback.csv)
  - [`../06_testing/artifacts/full_synthesis/full_moneyness_role_summary.csv`](../06_testing/artifacts/full_synthesis/full_moneyness_role_summary.csv)
  - [`../06_testing/artifacts/full_synthesis/full_cross_strike_context.csv`](../06_testing/artifacts/full_synthesis/full_cross_strike_context.csv)
  - [`../06_testing/artifacts/full_synthesis/full_portfolio_exposure_summary.csv`](../06_testing/artifacts/full_synthesis/full_portfolio_exposure_summary.csv)
  - [`../06_testing/artifacts/full_synthesis/full_late_entry_summary.csv`](../06_testing/artifacts/full_synthesis/full_late_entry_summary.csv)
  - [`../06_testing/artifacts/full_synthesis/full_wave5_probe_summary.csv`](../06_testing/artifacts/full_synthesis/full_wave5_probe_summary.csv)
  - [`../06_testing/artifacts/full_synthesis/full_wave5_decision_board.csv`](../06_testing/artifacts/full_synthesis/full_wave5_decision_board.csv)
- Closeout framing:
  - [`../06_testing/round_3_closeout_retrospective.md`](../06_testing/round_3_closeout_retrospective.md)
  - [`../post_run_research_memory.md`](../post_run_research_memory.md)

## Why This EDA Matters

The original EDA told us how the products looked in raw sample data.
This retrospective EDA tells us how those same product families behaved once
they were actually traded through many strategy forms.

That distinction matters because several important conclusions were not visible
from raw quotes alone:

- some active-option families had real upside but terrible retention,
- some strikes are better as signals than as inventory,
- and some product roles only become obvious after path-quality and giveback
  analysis.

## New Decision-Relevant EDA Findings

### 1. Product roles should be treated as first-class features

The run-derived moneyness-role audit is strong enough to formalize product
roles as an EDA output, not just a strategy intuition.

- `delta-1 base`: cleanest realized family across stability and final PnL
- `ITM structural`: small additive overlay, not standalone engine
- `active zone`: highest upside and worst giveback at the same time
- `upper passive/execution`: mostly execution-sensitive and low-ROI
- `floor monitor`: no meaningful active role

Carry-forward EDA implication:
future EDA should be organized by `role` first, not just by symbol.

### 2. Cross-strike context matters more than single-strike standalone quality

The original EDA already suggested surface structure mattered.
The retrospective cross-strike audit strengthens that into a practical rule:

- `VEV_5300` can look acceptable in isolation,
- but `VEV_5100/5200` often tell you whether that acceptance is safe or toxic,
- so cross-strike disagreement/agreement should be an explicit EDA axis.

Carry-forward EDA implication:
future EDA should bucket residuals and outcomes not only by product but also by
neighbor-strike context.

### 3. Portfolio exposure is itself an EDA feature

The run history shows that the active cluster problem was not just
per-symbol bad selection; it was also family-level exposure concentration.

- legacy broad active families carried much larger final active exposure,
- those same families also carried the largest givebacks,
- and symbol-level limits were not enough to describe the true risk state.

Carry-forward EDA implication:
exposure should be analyzed at family level, not only per symbol.

### 4. Timing and churn are EDA-level variables, not just execution afterthoughts

The late-entry and post-peak summaries show a repeated pattern:

- many selective active runs peaked early,
- then kept placing a large share of trades after the useful window,
- and gave back much of the edge.

Carry-forward EDA implication:
future EDA should explicitly bucket by:

- early / mid / late session,
- pre-peak / post-peak trade share,
- and plausible no-new-entry cutoffs.

### 5. Trade horizon must be treated as part of the signal definition

The run-derived markouts reinforce a key raw-EDA hint:

- `VEV_5300` is not a fast scalp,
- `1k` and `5k` can look mediocre while `10k` becomes meaningfully better,
- and `5000/5100/5200` remain weak even after longer horizons.

Carry-forward EDA implication:
future EDA should classify candidate signals by natural holding horizon, not
just by direction.

## EDA Promotions Into Round 4

These should now count as promoted EDA conclusions for future work:

| EDA Output | Promote? | Why |
| --- | --- | --- |
| role-based product grouping (`delta-1`, `ITM`, `active`, `upper`, `floor`) | yes | repeatedly decision-relevant in run history |
| cross-strike context around `5300` using `5100/5200` | yes | changed the interpretation of whether a strike was tradable or merely informative |
| family-level exposure / inventory state | yes | symbol-level limits did not explain the real giveback behavior |
| post-peak churn and late-entry timing | yes | strong recurring pattern in active-option families |
| hold-horizon classification by strike/setup | yes | especially important for `5300` |

## EDA Rejections / De-Prioritizations

These should now count as stronger EDA-level negative evidence:

| Idea | Decision | Why |
| --- | --- | --- |
| treating the broad `5000/5100/5200/5300` cluster as one homogeneous family | reject | strike roles and toxicity diverge too much |
| evaluating vouchers mainly as independent delta-1-like assets | reject | book-level and cross-strike context matter materially |
| using only symbol-level inventory or imbalance views | reject | family-level concentration is part of the true state |
| assuming fast-unwind is the right default rescue axis | reject | horizon evidence contradicts it, especially for `5300` |

## Suggested Round 4 EDA Checklist

Before strategy work in `round_4`, the EDA should explicitly answer:

1. Which products belong to `delta-1`, `ITM`, `active`, `upper`, and `floor` roles in the new round data?
2. Which active strikes look toxic as inventory but informative as state signals?
3. When the active family works, is it early-session only, horizon-specific, or regime-specific?
4. Which cross-strike relationships matter most for gating `5300`-like trades?
5. Does family-level exposure explain path damage better than symbol-level views?

## Hand-off

Use this addendum alongside:

- [`eda_option_surface_and_microstructure.md`](eda_option_surface_and_microstructure.md)
- [`../06_testing/round_3_closeout_retrospective.md`](../06_testing/round_3_closeout_retrospective.md)
- [`../post_run_research_memory.md`](../post_run_research_memory.md)

The original EDA remains the raw-data foundation.
This addendum is the run-informed EDA bridge that should feed `round_4`.
