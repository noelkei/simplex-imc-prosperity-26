# Processed Paper Summary: Fengler (2005)

## Status

`draft`

## Paper Metadata

- Paper ID: `fengler_2005_surface_smoothing`
- Title: `Arbitrage-Free Smoothing of the Implied Volatility Surface`
- Authors: Matthias R. Fengler
- Year: 2005
- Link: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=603280

## Core Claim

An implied volatility surface computed by strike-by-strike calibration is
generically non-arbitrage-free: it can violate the call-price monotonicity
and convexity conditions required for absence of static arbitrage. Fengler
provides a least-squares smoothing algorithm that enforces these conditions
while staying close to market-implied prices. The key no-arbitrage conditions
for a call surface C(K) at fixed T are:
1. Monotone: ∂C/∂K ≤ 0 (calls are non-increasing in strike)
2. Convex: ∂²C/∂K² ≥ 0 (butterfly spreads are non-negative)
3. Bounded: max(F-K, 0) ≤ C ≤ F

## Assumptions

- Continuous strike grid (the paper's smoothing is over continuous K; we
  discretize to our 6–8 active strikes).
- Single maturity (term structure consistency is out of scope for us).
- Static arbitrage only (no dynamic hedging argument needed).

## Problem Addressed for Round 4

- We need to ensure our Bachelier fair-value surface does not give butterfly
  arbitrage (e.g., C(5200) < C(5300) after sigma fluctuations).
- The "Fengler check" prevents the bot from quoting or taking based on an
  internally inconsistent surface.
- With TTE=4 and higher gamma, surface violations are more likely near ATM.

## What This Paper Gives Us

- Implementable check (discrete version):
  For sorted strikes K₁ < K₂ < K₃ with calls C₁, C₂, C₃:
  Butterfly condition: C₁ - 2·C₂ + C₃ ≥ 0
  This must hold for every triple of adjacent strikes.

- Monotonicity check (discrete):
  C(Kᵢ) ≥ C(Kᵢ₊₁) for all i (lower strike call ≥ higher strike call).

- Standard pre-trade gate in bot code:
```python
# Monotonicity gate (already in prior bots)
surface_ok = all(
    fairs[ks[i]] >= fairs[ks[i+1]] - 0.5
    for i in range(len(ks) - 1)
)

# Butterfly gate (new for Round 4)
butterfly_ok = all(
    fairs[ks[i]] - 2*fairs[ks[i+1]] + fairs[ks[i+2]] >= -0.5
    for i in range(len(ks) - 2)
)

surface_ok = surface_ok and butterfly_ok
```

## Relevance To Round 4

- Near TTE=4, gamma is elevated for ATM strikes (5200/5300). Small changes in
  VEX mid can produce surface violations if sigma table is fixed.
- The butterfly check adds one additional layer of protection.
- Cost: O(n) per tick — negligible.

## Action Classification

`promote` — the discrete check is already partially implemented; add butterfly gate.

## Implementation Notes

The `surface_ok` flag should gate all aggressive takes. Passive quoting can
continue even when surface_ok=False (posting at fair independently per strike
is still valid even if the surface is temporarily non-convex).

## Downstream Use

- Spec: add butterfly check to all option bot templates.
- Validation: log surface_ok rate to traderData to audit how often violations occur.
