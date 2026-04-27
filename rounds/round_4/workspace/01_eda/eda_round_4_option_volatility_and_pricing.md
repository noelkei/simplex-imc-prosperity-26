# Round 4 EDA Annex - Option Volatility And Pricing

## Purpose

This annex adds the advanced option-pricing layer requested for `round_4`.

It answers four practical questions:

- what the implied-volatility surface looks like for the `VEV_*` family,
- whether a constant-volatility Black-Scholes fit is materially underfitting the
  cross-strike data relative to a stochastic-volatility Heston fit,
- what the basic Greek profile says about strike roles,
- and which classic option-market diagnostics are genuinely available versus
  structurally unavailable in the current data.

## Scope And Caveats

- Scope:
  algorithmic `VEV_*` family only.
- Contract assumption:
  `VEV_*` vouchers are treated as call-like instruments on
  `VELVETFRUIT_EXTRACT`, consistent with the `round_3` and `round_4` wiki
  framing.
- TTE assumption:
  `day 1 -> 4d`, `day 2 -> 3d`, `day 3 -> 2d`, using the Round 4 example and a
  simple trading-year normalization of `252` days.
- Important caveat:
  this is an EDA pricing layer, not a claim that a full Heston engine belongs
  inside the uploadable bot.

## Primary Sources

- `../../data/processed/derived_round_4_option_panel_metrics.csv`
- `../../data/processed/derived_round_4_option_iv_surface_summary.csv`
- `../../data/processed/derived_round_4_option_smile_summary.csv`
- `../../data/processed/derived_round_4_option_bs_vs_heston_fit.csv`
- `../../data/processed/derived_round_4_option_model_residuals.csv`
- `../../data/processed/derived_round_4_option_volume_by_strike.csv`
- `../../data/processed/derived_round_4_option_metric_availability.csv`
- `artifacts/round_4_iv_smile_by_day.png`
- `artifacts/round_4_option_model_fit_comparison.png`

## Metric Availability

| Metric | Status | Why |
| --- | --- | --- |
| Implied volatility surface | implemented | feasible from call-like `VEV_*` mids, strikes, and same-time `VEX` anchor |
| Black-Scholes fit | implemented | simple constant-vol benchmark for cross-strike fitting |
| Heston fit | implemented | stochastic-volatility benchmark via COS pricing |
| COS method | implemented | used as the numerical engine for Heston pricing |
| Greeks | implemented | computed from panel BS implied vols |
| Put-call parity | not available | no paired put series exists in the uploaded algorithmic data |
| Volume / Open Interest relation | partially available | trade volume exists; official open interest does not |

## Implied Volatility Surface

### Main observations

- The active and upper voucher zone mostly lives in a relatively compact
  implied-vol regime around `0.24` to `0.31`.
- `VEV_4000` often sits exactly on intrinsic value in the panel medians, so BS
  IV is not stably invertible there. That is a structural ITM boundary effect,
  not a data error.
- `VEV_6000` / `VEV_6500` admit mechanical BS IV values because the price is
  nonzero, but those values should not be read as economically trustworthy
  volatility estimates because the instruments are floor-like and nearly
  inactive.

### Shape by strike

- The useful smile lives mainly in `VEV_5000` to `VEV_5500`.
- The active center is fairly flat in level, but curvature increases on the
  shorter TTE panels.
- Smile curvature is strongest in late `day 3`, which is consistent with the
  option family becoming more terminal and more execution-fragmented as expiry
  approaches.

### Term-structure interpretation

- There is no full same-time multi-maturity term structure in the algorithmic
  data.
- What we do have is a `day-linked short-maturity decay` view:
  `4d -> 3d -> 2d`.
- That is enough for a short-dated EDA reading:
  the surface becomes more curved and more strike-sensitive as TTE compresses.

## Greeks

The BS Greek layer is mainly useful as a `role sanity check`, not as a direct
bot signal.

### What it confirms

- Delta decreases monotonically with strike in the expected way.
- Gamma and vega are most relevant in the active center, especially
  `VEV_5200/5300`.
- Theta is most negative in the same active region, which matches the intuition
  that this is where time value and short-dated decay matter most.
- `VEV_6000/6500` have very small delta / gamma / vega despite nonzero implied
  vols, which reinforces the view that they are structurally floor-like rather
  than truly active options.

### Practical implication

- If a later strategy wants a lightweight role-aware option feature set, the
  Greeks suggest that `5200/5300` deserve the highest sensitivity attention,
  while `4000` behaves closer to intrinsic and `6000/6500` behave closer to
  monitoring/floor instruments.

## Black-Scholes vs Heston

### What was implemented

- Black-Scholes:
  one constant-volatility fit per `(day, time_bucket)` panel.
- Heston:
  one `(v0, kappa, theta, volvol, rho)` calibration per `(day, time_bucket)`
  panel.
- Numerical method:
  COS pricing under Heston.

### Fit comparison

- Heston improves the panel RMSE in `7` of `9` panels.
- Average RMSE improvement is about `0.0170`.
- The biggest improvements appear late in the sample, especially:
  - `day 3 / mid`: `+0.0598`
  - `day 3 / late`: `+0.0447`
  - `day 2 / early`: `+0.0292`

### Interpretation

- Constant-vol BS is already a decent first approximation.
- Heston does fit the cross-strike surface a bit better, especially nearer to
  expiry and in more curved panels.
- But the improvement is `moderate`, not transformative.

### Strategic takeaway

- This is strong enough to say:
  `surface curvature is real and not perfectly captured by one flat sigma`.
- It is not strong enough to say:
  `the live bot should become a Heston engine`.

The right downstream use is:

- keep role/surface/residual thinking first-class,
- use BS or a simpler fair-value kernel operationally if needed,
- and treat Heston here as evidence that volatility is not fully flat across
  strikes and shrinking maturities.

## COS Method

Why COS was worth using here:

- short-dated panels make Fourier-cosine pricing fast and stable enough for EDA,
- it gives a cleaner Heston benchmark than a noisy Monte Carlo layer,
- and it lets us compare model fit panel by panel without adding simulation
  variance.

Why it is still an EDA tool first:

- calibration quality depends on the voucher-family contract simplification,
- floor-like strikes distort any full-surface interpretation,
- and the live strategy problem is still dominated by microstructure,
  concentration, and execution texture.

## Volume And Open Interest

- Volume is available and already integrated into the panel metrics and strike
  summaries.
- Official open interest is not present in the current files.
- No honest OI reconstruction is possible from the current algorithmic data
  alone, so the EDA does not invent one.

## Promotion Decision

Promote into understanding:

- short-dated `VEV_*` surface is real and curved
- Greeks reinforce the strike-role split
- Heston improves fit enough to validate non-flat volatility thinking

Keep as research-only / secondary:

- the full Heston stack itself
- any attempt to use panel-calibrated parameters directly in `Trader.run()`

## Downstream Use

- Understanding:
  use this annex to state that the voucher family is not only linked, but also
  mildly non-flat in volatility structure.
- Strategy:
  prefer residual / role / surface-aware candidates over flat-sigma naive
  treatment.
- Spec:
  if a pricing backbone is used later, document clearly whether it is intrinsic,
  BS-like, Bachelier-like, or another simplified surface anchor.
