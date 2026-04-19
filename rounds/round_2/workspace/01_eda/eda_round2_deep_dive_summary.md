# Round 2 Deep-Dive EDA Summary

Generated on 2026-04-19 from raw Round 2 price data.

## Why this was run

After the 8975 platform result, the goal was to identify whether a final bot should become more aggressive, more depth-aware, or more selective under Round 2's partial-visibility constraint.

Round 2-specific constraints used for interpretation:

- testing only exposes a randomized 80% of generated quotes
- final accepted bidders get 25% more quotes
- therefore strategies should remain robust under partial books while preserving upside from richer visible depth

## Main findings

### 1. Depth-price shift is consistently useful

Across both products and multiple horizons, the depth-weighted price shift is a strong predictor of the next mid move.

This supports the use of:
- microprice / imbalance for top-level pressure
- depth-price shift for richer fair-value estimation

It does **not** support naive deeper-book imbalance aggregation as a standalone signal.

### 2. ACO is regime-sensitive

For `ASH_COATED_OSMIUM`:

- tight-spread and wide-spread states are the live regimes
- the middle spread regime is comparatively weak / dead for alpha extraction
- this means selective participation is more sensible than uniform aggression

Implication:
- ACO should trust predictive signals more in tight and wide regimes
- ACO should quote more conservatively in the middle regime

### 3. IPR is stronger than a pure carry story

For `INTARIAN_PEPPER_ROOT`:

- imbalance is highly predictive across multiple horizons
- depth-shift also has consistent predictive value
- regime dependence exists, but the signal remains broadly usable

Implication:
- IPR should not be treated only as "always buy drift"
- smarter entry throttling and repost intensity are justified
- however, in lightweight replay the more complex state-aware IPR variants still did not beat the best existing combined bot

### 4. Aggressive conviction sprinting did not survive validation

The aggressive `_05` branch was a plausible upside shot, but local validation did not prefer it.

Interpretation:
- directional bursts exist, but the current sprint implementation likely overpaid for them
- aggressive burst capture remains a possible avenue, but would need better persistence gating or better exit logic

## Best practical conclusion for today

Despite the deeper research, the strongest validated candidate remains:

- `candidate_r2_amin_regime_depth_04.py`

Reason:
- it best balances Round 2 robustness on randomized 80% test books with upside from extra visible depth if the bid is accepted
- later variants became either too aggressive or too conservative in local checks

## Files produced

- `01_eda/eda_round2_deep_dive.json`
- `01_eda/eda_round2_deep_dive_summary.md`

## Next-session ideas

If work continues later, the most promising next branch is likely:

1. keep `_04` as the backbone
2. improve only the ACO inventory unwind / re-entry logic
3. avoid large structural changes that degrade the validated base
4. test whether bid value should remain at `9` or move slightly higher for final submission strategy
