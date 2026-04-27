# Processed Paper Summary: Carr and Madan (1999)

## Status

`draft`

## Paper Metadata

- Paper ID: `carr_madan_1999_fft_options`
- Title: `Option Valuation Using the Fast Fourier Transform`
- Authors: Peter Carr, Dilip B. Madan
- Year: 1999
- Link: https://doi.org/10.1002/futures.10005

## Core Claim

European option prices can be computed for a GRID of strikes simultaneously using
the Fast Fourier Transform (FFT), exploiting the fact that option prices are
related to the characteristic function of log-returns via a Fourier transform.

FFT formula: for a grid of N strikes with spacing η,
```
C(k_j) ≈ (e^{-αk_j} / π) × Re[FFT(ψ(v_m))]_j
```
where α > 0 is a damping parameter and ψ is the modified characteristic function.

This prices N strikes at cost O(N log N) instead of O(N × integration_cost).

## Assumptions

- Characteristic function of log-returns is analytically known (as in BS, Heston,
  VG, CGMY, NIG, etc.).
- European options only.
- Uniform grid of strikes in log-strike space.

## Problem Addressed for Round 4

**Assessment**: The FFT method is an OFFLINE computation tool. It is not relevant
for live bot pricing (same constraint as COS method: no numpy/FFT in stdlib).

**Why it is listed as inspiration-only**:
1. Requires numpy.fft or equivalent — not available in Prosperity runtime.
2. We have only 6-8 active strikes, so computing all simultaneously has no
   advantage over individual Bachelier evaluations.
3. Heston (which motivates FFT) was eliminated from live pricing.

**What FFT IS useful for**: calibrating the Bachelier sigma table offline by
computing a dense grid of BS/Bachelier prices from market data and then
backing out implied vols. This was already done in the EDA phase.

## What This Paper Gives Us

- **Conceptual**: the FFT connection shows why the vol smile shape (as a function
  of log-strike) is smooth — it's the Fourier transform of a bounded density.
- **Calibration methodology**: the paper's approach informed how we calibrate the
  SIGMA_TABLE from observed market prices (though we used simpler root-finding
  rather than full FFT calibration).
- **Implementation template** (offline only): useful if we later need to calibrate
  a Heston or jump-diffusion model to the VEV smile for academic purposes.

## Relevance To Round 4

| Use Case | FFT Relevant? | Status |
|:--|:--|:--|
| Live bot pricing | No | Bachelier handles this |
| Offline sigma calibration | Indirectly | Already done via root-finding |
| Heston calibration | Offline only | Heston eliminated for live use |
| Dense strike grid pricing | N/A (6-8 strikes only) | No advantage over per-strike |

## Action Classification

`inspiration-only` — FFT method informed the calibration methodology but is
not directly implemented in any bot or offline script. The Bachelier sigma table
was calibrated using simpler per-strike root-finding (no FFT needed for 8 strikes).

## Implementation Notes

No live implementation. For reference, the offline calibration approach
that FFT theory inspired:

```python
# Per-strike Bachelier implied vol calibration (already done in EDA)
# This is what FFT would do in bulk, but we only have 8 strikes
# so per-strike bisection is equivalent and simpler.

def bachelier_iv_from_market(market_price, S, K, T, tol=0.01):
    """Back out Bachelier sigma from observed market price."""
    from math import sqrt, exp
    from statistics import NormalDist
    nd = NormalDist()

    def bachelier_call(sigma):
        if sigma <= 0:
            return max(S - K, 0)
        vt = sigma * sqrt(T)
        d = (S - K) / vt
        return (S - K) * nd.cdf(d) + vt * nd.pdf(d)

    lo, hi = 1.0, 10000.0
    for _ in range(50):
        mid = (lo + hi) / 2
        if bachelier_call(mid) < market_price:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    return (lo + hi) / 2

# Result was the SIGMA_TABLE in choi_2022_bachelier_guide_processed.md
```

## Downstream Use

- Strategy: no direct use. The sigma table that FFT theory would calibrate
  is already hardcoded from the EDA phase.
- Spec: no FFT code in bots.
- Validation: the smooth vol smile (nearly flat for K=5000-5500) is consistent
  with the FFT-theory prediction of a smooth Fourier transform.
