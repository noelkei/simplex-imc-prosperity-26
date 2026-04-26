# Round 4 EDA Annex - Option Book Structure

## Purpose

This annex deepens the option-book side of Phase 01:

- how the `VEV_*` family trades in raw data,
- how it links to `VELVETFRUIT_EXTRACT`,
- and where the family is structurally continuous versus execution-fragmented.

Primary sources:

- `../../data/processed/derived_round_4_option_book_summary.csv`
- `../../data/processed/derived_round_4_local_cross_strike_context.csv`
- `../../data/processed/derived_round_4_same_time_return_corr.csv`
- `../../data/processed/derived_round_4_lead_lag_summary.csv`
- `../../data/processed/derived_round_4_product_regime_summary.csv`
- `../../data/processed/derived_round_4_family_conditioned_regime_summary.csv`
- `../../data/processed/derived_round_4_trade_alignment_summary.csv`

## Main Structural Findings

### 1. The family is still clearly a linked option book

Same-time `VEX` return correlation remains strongest in the active and near-ITM zone:

- `VEV_4000`: `0.5806`
- `VEV_5000`: `0.7542`
- `VEV_5100`: `0.7600`
- `VEV_5200`: `0.7315`
- `VEV_5300`: `0.6169`
- `VEV_5400`: `0.4671`
- `VEV_5500`: `0.2492`

Lagged correlations collapse after lag `0`, so the family still looks like
same-time anchor logic rather than delayed-follow logic.

### 2. Structural linkage does not mean homogeneous tradability

Local cross-strike correlations remain strong in the center and decay outward:

- `5000-5100`: `0.8985`
- `5100-5200`: `0.8460`
- `5200-5300`: `0.6686`
- `5300-5400`: `0.4236`
- `5400-5500`: `0.1688`

But friction diverges much faster than correlation:

- `VEV_5000`: `237.6` bps mean relative spread
- `VEV_5100`: `260.1` bps
- `VEV_5200`: `312.7` bps
- `VEV_5300`: `493.6` bps
- `VEV_5400`: `1147.1` bps
- `VEV_5500`: `3227.4` bps
- `VEV_6000/6500`: `20000` bps

Conclusion:
the family is structurally continuous but execution-fragmented.

### 3. Trade activity is not centered where quote coverage is richest

Trade counts:

- `VEV_4000`: `442`
- `VEV_4500`: `3`
- `VEV_5000`: `3`
- `VEV_5100`: `3`
- `VEV_5200`: `47`
- `VEV_5300`: `164`
- `VEV_5400`: `276`
- `VEV_5500`: `306`
- `VEV_6000`: `317`
- `VEV_6500`: `317`

This is important:
the book is not telling us “most trades = best inventory candidate”.
Instead, many upper/floor trades are counterparty loops with terrible friction.

### 4. Short-horizon trade alignment gets worse quickly from `5200` upward

Average future `5`-step return after trades:

- `VEV_4000`: `-0.0379` bps
- `VEV_5200`: `-20.9456` bps
- `VEV_5300`: `-47.1721` bps
- `VEV_5400`: `-26.5688` bps
- `VEV_5500`: `-51.1060` bps
- `VEV_6000/6500`: `0.0`

This does not prove strategy PnL, but it is strong raw caution against naive
inventory-taking in much of the active/upper range.

## Role Implications By Strike Bucket

### `VEV_4000` / `VEV_4500`

- best interpreted as `ITM structural`
- `4000` has enough tape to matter
- `4500` remains too sparse for strong tape conclusions

### `VEV_5000` / `VEV_5100`

- same-time `VEX` linkage is still strongest here
- raw trade tape is too sparse to claim direct tradability
- useful for structural anchor analysis, not for strong tape-based claims

### `VEV_5200`

- still in the active zone structurally
- tape is thin but no longer empty
- seller side is almost monopolized by `Mark 22`
- short-horizon trade alignment is poor

Best current interpretation:
candidate for contextual or veto-style use, not default inventory.

### `VEV_5300`

- still the special strike in the active zone
- meaningfully traded
- concentrated on `Mark 01` buys vs `Mark 22` sells
- much higher spread than `5200`
- poor short-horizon trade alignment

Best current interpretation:
special-case candidate that needs anchor-aware and counterparty-aware treatment.

### `VEV_5400` / `VEV_5500`

- upper/passive regime
- friction explodes
- trade flow becomes almost deterministic by counterparty
- raw evidence supports passive-only, signal-only, or default exclusion

### `VEV_6000` / `VEV_6500`

- pure floor regime
- constant `0.5` mids
- zero trade notional
- dynamic alpha should be rejected

## Time-Bucket Regime Notes

Upper/floor friction worsens as the day progresses:

- `VEV_5400` mean relative spread:
  `976.9` early, `1308.5` mid, `1155.8` late
- `VEV_5500` mean relative spread:
  `2432.8` early, `4023.4` mid, `3226.4` late

Active-zone spreads also widen from early to mid/late, though less violently.

This is strong enough for a `defensive-only` regime conclusion:
time bucket should matter to execution and no-trade policy, especially in upper
strikes.

## Promotion Decision

Promote:

- option book remains linked to `VEX`
- delayed-follow still weak
- role-based strike segmentation is mandatory
- upper/floor range should be treated primarily as passive, signal, or monitor scope

Keep exploratory:

- whether `5200` is fully signal-only
- whether `5300` still deserves active-trading attempts
- whether sparse `5000/5100` prints hide useful edge or just missing opportunity

## Downstream Use

- Understanding:
  treat the book as `linked but execution-fragmented`.
- Strategy:
  separate `5000/5100`, `5200`, `5300`, `5400/5500`, and `6000/6500`.
- Spec:
  any option strategy should declare both role and friction posture, not just strike.
