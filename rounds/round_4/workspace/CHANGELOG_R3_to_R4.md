# Changelog: Round 3 → Round 4

## Status

`READY_FOR_REVIEW`

## What We Were Doing In Round 3 That We Are Still Doing

| Category | Item | Status |
| --- | --- | --- |
| Architecture | `delta-1 first` framing for `HYDROGEL_PACK` and `VELVETFRUIT_EXTRACT` | carry-forward |
| Architecture | `VEX` as anchor/context for the voucher family | carry-forward |
| Architecture | Role-based strike segmentation (ITM / active / upper / floor) | carry-forward |
| Pricing | Bachelier model for option fair value | carry-forward, recalibrated |
| Pricing | Per-strike implied vol table (sigma_abs by strike) | carry-forward, new values |
| Risk | Inventory skew and position clamping | carry-forward |
| Risk | Fengler convexity check on the vol surface | carry-forward |

---

## What We Were NOT Doing In Round 3 That We Are NOW Doing

### 1. Counterparty-Aware Trading (`Trade.buyer` / `Trade.seller`)

- **What was missing**: Round 3 data had `buyer=None`, `seller=None` for all trades.
  We had zero signal about WHO was on the other side.
- **What we have now**: Named `Mark XX` participants in every trade record.
- **Impact**:
  - `Mark 22` is a near-deterministic OTM seller (5200–6500). When Mark 22 is
    the active seller, buying those strikes has strongly negative short-horizon
    markout. This is a hard **no-buy** signal for upper vouchers.
  - `Mark 67` is a VEX-only buyer with positive short-horizon follow-through.
    Observing Mark 67 buys gives a mild directional lean for VEX.
  - `Mark 01` is the matching OTM buyer against Mark 22. The Mark 01/22 loop
    is a synthetic market, not a natural one — avoid participating.
  - `Mark 14` and `Mark 38` are structural market makers in HYDROGEL and
    ITM vouchers. Their presence is context, not signal.
  - These counterparty states are now **online-usable features** via
    `state.market_trades` in the Trader API.

### 2. Calibrated Per-Strike Sigma Table (Updated for TTE=4)

- **What was missing**: Round 3 bots inherited `SIGMA_DEFAULT = 95.0` which
  gave near-zero Bachelier fair values and caused aggressive erroneous selling.
- **What we have now**: Per-strike Bachelier sigma calibrated from Round 4
  raw price data at S≈5247.6, TTE=4/365:

  | Strike | Bachelier σ | BS IV | Delta (Bach) |
  |-------:|------------:|------:|-------------:|
  | 4000 | 3199.8 | 69.64% | 0.9999 |
  | 4500 | 1982.5 | 40.76% | 0.9998 |
  | 5000 | 1469.7 | 28.69% | 0.9463 |
  | 5100 | 1446.0 | 27.95% | 0.8353 |
  | 5200 | 1491.5 | 28.55% | 0.6199 |
  | 5300 | 1531.8 | 29.05% | 0.3720 |
  | 5400 | 1452.8 | 27.29% | 0.1582 |
  | 5500 | 1590.4 | 29.60% | 0.0648 |

### 3. IV/RV Ratio Analysis → Confirmed Theta Harvest Opportunity

- **What was missing**: We had not formally computed the IV/RV ratio from data.
- **What we have now**: VEX annualized realized vol = 571. Bachelier IV ranges
  from 1446–1592 for active strikes → IV/RV ≈ **2.5–2.8×**.
- **Impact**: Selling ATM/NTM options is EV-positive. Per-round theta from short
  300 units of each active strike: 5200→2373, 5300→2418, 5100→1403, 5400→1367.
- **Round 4 TTE=4** (vs TTE=5 in R3): theta per day is HIGHER now (shorter
  expiry → faster time decay). The opportunity is larger than in R3.

### 4. Black-Scholes vs Bachelier Model Comparison

- **What was missing**: We only used Bachelier. No formal BS comparison.
- **What we have now**: Full BS implied vol surface computed from market data.
  The BS smile is remarkably flat (0.2795–0.2960) for strikes 5000–5500,
  confirming that a simple constant-vol model (Bachelier or BS) captures most
  of the active-zone pricing. Deep ITM (4000/4500) shows elevated BS IV,
  consistent with a structural skew.

### 5. Vol Surface Shape / Smile Analysis

- **What was missing**: No smile analysis in Round 3 EDA.
- **What we have now**: Bachelier smile ratio from 0.969 (K=5100) to 1.066
  (K=5500), nearly flat in the active zone. The "smile" is actually a **smirk**:
  deep ITM carries significantly elevated implied vol (ratio=2.145 for K=4000).
  This is consistent with a discrete jump distribution rather than pure GBM.

### 6. Heston Stochastic Vol Assessment

- **What was missing**: No consideration of stochastic volatility.
- **What we have now**: Formal test shows VEX rolling vol has CoV=0.119 < 0.30
  threshold for "meaningful stochastic vol". Conclusion: **Bachelier with fixed
  sigma is adequate for this market**. Heston adds marginal calibration quality
  at significant implementation cost.

### 7. Greeks Portfolio Management

- **What was missing**: No formal Greek computation. Delta hedging was ad-hoc.
- **What we have now**: Full Greek table (Δ, Γ, ν, Θ) computed from Bachelier.
  Portfolio Greeks for the target short strategy are explicitly quantified.
  VEX hedge requirement is now computed analytically, not approximated.

### 8. Exotic Options Pricing (Manual Challenge)

- **What was missing**: No treatment of exotic options in Round 3.
- **What we have now**: Aether Crystal (GBM, σ=251%, 252d/yr, 4 steps/d).
  Closed-form and simulation pricing for: chooser option, binary put,
  knock-out put. Pricing implemented in `analyze_round_4_advanced_eda.py`.

---

## Anti-Patterns From Round 3 That Round 4 Must Not Repeat

| Anti-Pattern | Root Cause | Round 4 Fix |
| --- | --- | --- |
| `sigma_abs=95` giving near-zero fair values | wrong sigma default | hardcoded calibrated SIGMA_TABLE |
| V_OFFSET=2 placing passive quotes outside the spread | misread of spread magnitude | V_OFFSET=1 for 2-tick-spread options |
| Delta hedge firing on zero-option-position | no gate condition | gate: only hedge if \|opt_delta\| > 15 |
| Selling aggressively at bid (below fair) | theta harvest attempted within-round | post passive asks at fair, let buyers come |
| Treating 5100/5200 as normal inventory | ignored toxicity evidence | use as danger-state veto only |
| Ignoring buyer/seller fields | fields were None in R3 | now first-class online features |

---

## TTE Calendar

| Round | TTE (days) | TTE (years) |
| --- | ---: | ---: |
| Round 1 | 7 | 0.01918 |
| Round 2 | 6 | 0.01644 |
| Round 3 | 5 | 0.01370 |
| **Round 4** | **4** | **0.01096** |
| Round 5 | 3 | 0.00822 |
| Round 6 | 2 | 0.00548 |
| Round 7 | 1 | 0.00274 |

Theta accelerates as TTE decreases. We are now at the steepest part of the
time-decay curve for the NTM strikes.
