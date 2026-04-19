# EDA — Round 2

## Status

READY_FOR_REVIEW

Review outcome: not reviewed.

## Product Scope

| Product | Symbol | Position Limit | Present In Data | Decision |
| --- | --- | ---: | --- | --- |
| Ash-Coated Osmium | `ASH_COATED_OSMIUM` (ACO) | 80 | yes | include for algorithmic trader; mean-reverting around 10000, 16-tick spread |
| Intarian Pepper Root | `INTARIAN_PEPPER_ROOT` (IPR) | 80 | yes | include for algorithmic trader; **strong +1000/day deterministic drift** |

Source: `rounds/round_2/data/raw/{prices,trades}_round_2_day_{-1,0,1}.csv`.

## Data Sources

| File | Rows | Notes |
| --- | ---: | --- |
| `prices_round_2_day_-1.csv` | 20,000 | 10k ticks × 2 products; 28 dirty mid=0 rows (one per product per ~1.4k ticks) |
| `prices_round_2_day_0.csv` | 20,000 | Same shape; 34 dirty rows |
| `prices_round_2_day_1.csv` | 20,000 | Same shape; 38 dirty rows |
| `trades_round_2_day_*.csv` | ~800 each | Anonymous trades (buyer/seller blanked) |

**Cleaning rule**: rows with `mid_price == 0` reflect empty book ticks; dropped from all stats.

Methods/script: [`scripts/eda_r2_deep.py`](scripts/eda_r2_deep.py); raw outputs in [`outputs/eda_summary.json`](outputs/eda_summary.json); plots in [`plots/`](plots/).

---

## 1. Descriptive Statistics (clean data)

### ACO — Ash-Coated Osmium

| Day | mid mean | mid std | spread median | spread mean | one-sided % | level-1 depth bid | level-1 depth ask |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| −1 | 10000.83 | 4.47 | 16 | 16.22 | 7.6% | 30.2 | 30.1 |
| 0 | 10001.61 | 5.66 | 16 | 16.25 | 7.4% | 30.1 | 30.4 |
| 1 | 10000.21 | 5.02 | 16 | 16.23 | 7.9% | 30.2 | 30.4 |

- **Mid is anchored to ~10000**, std ≤ 5.7 across 3 days.
- Bid-ask spread is essentially fixed at 16 (median = 16 every day; std ≈ 2.5).
- Order book has ~1.6 levels populated per side on average.
- Skewness ≈ 0, kurtosis ≈ 0.5 → roughly Gaussian mid.

### IPR — Intarian Pepper Root

| Day | mid mean | mid std (raw) | spread median | spread mean | one-sided % | depth bid | depth ask |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| −1 | 11500.12 | 288.65 | 13 | 13.07 | 7.5% | 24.2 | 24.0 |
| 0 | 12499.87 | 288.61 | 14 | 14.12 | 7.7% | 24.1 | 24.1 |
| 1 | 13500.06 | 288.75 | 15 | 15.18 | 7.5% | 24.3 | 24.2 |

- Mid std of ~289 is **NOT volatility around a constant**; it's the within-day spread of a slowly-rising line. After detrending, intra-day noise is similar to ACO (see §3).
- Spread median **increases by 1 tick per day** (13 → 14 → 15). Could continue to widen on submission day.
- Depth ~24 per side (lower than ACO).

### Trade activity

- Trades are sparse (~800 rows per day for both products combined).
- Buyer/seller fields are blanked → no attribution signal available.

---

## 2. Day-Over-Day Drift (THE big finding)

| Product | Day −1 → 0 | Day 0 → 1 | Per-tick OLS drift |
| --- | ---: | ---: | ---: |
| ACO | +0.78 | −1.40 | ~ ±1e-6 (≈ 0) |
| **IPR** | **+999.74** | **+1000.19** | **≈ +0.001 / tick** |

- IPR mid rises by an extraordinarily consistent **+1000 XIRECs per day** (~10k ticks).
- That's **+0.10 mid points per tick** on average — small per-tick, but massive cumulatively.
- ACO has no meaningful drift.

### Implication for trading

- **IPR is a directional asset**, not a market-making target. Holding 80 long for one full day → +80,000 XIRECs.
- A naïve "max-long IPR" bot collects the full +1000 per day per unit (assuming full position). Round 1 already used that pattern.
- **Risk**: trend may not persist. ADF strongly rejects a unit root on returns (p≈0), but the drift is a deterministic component, not the random walk part. We have only 3 days of evidence.

---

## 3. Returns: bid-ask bounce + volatility clustering

For each product per day, after taking `Δmid` on clean data:

| Product / day | ret std | ret kurt | ACF(ret, lag 1) | ACF(ret², lag 1) | ARCH-LM p |
| --- | ---: | ---: | ---: | ---: | ---: |
| ACO −1 | 3.70 | 3.19 | **−0.51** | 0.39 | 0 |
| ACO 0 | 3.69 | 3.26 | −0.51 | 0.41 | 0 |
| ACO 1 | 3.69 | 3.03 | −0.49 | 0.38 | 0 |
| IPR −1 | 3.11 | 2.98 | −0.50 | 0.40 | 0 |
| IPR 0 | 3.32 | 2.83 | −0.49 | 0.38 | 0 |
| IPR 1 | 3.58 | 3.00 | −0.51 | 0.41 | 0 |

- **ACF(returns, lag 1) ≈ −0.50 everywhere** → classic bid-ask bounce: when the trade prints at the ask, next move tends to be back to the bid. Pure mean-reversion at the 1-tick scale; **not exploitable as a directional signal**, but it is the reason "take-and-flip" tactics work.
- ACF at lags 2-5 ≈ 0 → no longer-horizon momentum/reversal in mid changes.
- **ACF(ret², lag 1) ≈ 0.40** with ARCH-LM p = 0 → real **volatility clustering**. When the market just moved, it tends to move again next tick. This is consistent across both products and all 3 days.
- Kurtosis ≈ 3 (after cleaning the dirty rows) → returns are roughly Gaussian + slight fat tails, not power-law extreme.

---

## 4. Stationarity: ADF + KPSS

Run on clean mid level (per day):

| Product / day | ADF stat | ADF p | KPSS stat | KPSS p |
| --- | ---: | ---: | ---: | ---: |
| ACO −1 | −4.14 | 0.006 | 0.74 | 0.01 |
| ACO 0 | −3.22 | 0.08 | 0.71 | 0.01 |
| ACO 1 | −4.45 | 0.002 | 0.17 | 0.03 |
| IPR −1 | −99.94 | 0 | 0.41 | 0.01 |
| IPR 0 | −98.17 | 0 | 0.08 | 0.10 |
| IPR 1 | −48.82 | 0 | 0.38 | 0.01 |

- ADF (H0: unit root) is generally rejected → first-differenced series is stationary.
- KPSS (H0: trend-stationary) is mostly rejected → the level series is not perfectly trend-stationary; there is residual drift / level-shift behaviour beyond a clean linear trend.
- Reading both jointly: **mid is best modelled as a random walk around a slow level (ACO ≈ 10000) plus a deterministic trend (IPR ≈ +1000/day)**, with white-noise + bid-ask-bounce returns plus volatility clustering.

---

## 5. Microstructure — Order Book Imbalance Predicts Next Tick

Definition: `imb1 = (bid_vol_1 − ask_vol_1) / (bid_vol_1 + ask_vol_1)` ∈ [−1, +1].

| Product | imb1 std | IC(imb1[t], Δmid[t+1]) | IC(imb1[t], Δmid[t+2]) | IC(imb1[t], Δmid[t+5]) |
| --- | ---: | ---: | ---: | ---: |
| ACO | 0.353 | **+0.647** | −0.008 | +0.005 |
| IPR | 0.329 | **+0.647** | −0.002 | +0.010 |

- **IC at lag 1 is +0.65 — extremely strong**. This is one of the most powerful microstructure signals you ever see.
- The signal **dies completely after one tick** (lags 2-10 ≈ 0).
- Interpretation: when bids dominate the top of book (imb1 > 0), mid moves up next tick; when asks dominate, mid moves down. Information is fully consumed in one tick.
- This was not visible in the previous rough analysis (got contaminated by zero-mid rows).

### Practical use
- Skew our quotes by a function of `imb1`. Round 1 candidate already used `micro = clip(2.0 * imb, ±2)` — that is **way too small** for a signal with IC=0.65.
- Should test a much stronger imbalance shift (perhaps 4-6 ticks at imb1 = ±1).
- Mid-changes happen 65-72% of ticks; our quote skews matter on most ticks.

### Mid-change frequency

| Product | frac with Δmid ≠ 0 | frac with |Δmid| > 1 |
| --- | ---: | ---: |
| ACO | 72.2% | 44.2% |
| IPR | 65.2% | 53.5% |

---

## 6. Kalman Filter — MLE Calibration

Local-level model: `mid[t] = x[t] + v[t]`, `x[t] = x[t-1] + w[t]`, `w ~ N(0, Q)`, `v ~ N(0, R)`.

MLE per day (Nelder-Mead on Gaussian log-likelihood):

| Product | Day | Q (process) | R (measurement) | log-lik | Steady K |
| --- | ---: | ---: | ---: | ---: | ---: |
| ACO | −1 | 0.083 | 6.77 | −24,268 | 0.095 |
| ACO | 0 | 0.096 | 6.69 | −24,253 | 0.102 |
| ACO | 1 | 0.097 | 6.80 | −24,316 | 0.101 |
| ACO | pooled | **0.092** | **6.75** | −72,838 | ≈ 0.10 |
| IPR | −1 | 0.198 | 4.53 | −22,761 | 0.159 |
| IPR | 0 | 0.214 | 5.27 | −23,463 | 0.154 |
| IPR | 1 | 0.226 | 6.09 | −24,147 | 0.149 |
| IPR | pooled | **0.213** | **5.30** | −70,469 | ≈ 0.15 |

### Key reads vs Round 1 calibration

- Round 1 final used **Q=0.005, R=25** (`candidate_07_kf_tuned`). MLE on Round 2 ACO data gives **Q=0.09, R=6.7** — 18× larger Q, 4× smaller R. Round 1's filter under-reacts.
- IPR has higher Q because the filter is also fitting the trend with a random-walk component. A better model for IPR is local-level + linear trend (state = [level, slope]), which would push IPR's Q lower for the noise component.
- Steady-state Kalman gain for ACO ≈ 0.10 → FV moves ~10% of the way toward each new mid observation. Filter responds in roughly 10 ticks.
- The Q/R values are remarkably stable across the 3 days → calibration is robust.

---

## 7. Hidden Markov Models — Regime Detection

Gaussian HMM (`hmmlearn`) on per-day `Δmid`, K ∈ {2,3,4}, full covariance. BIC values:

| Product | K=2 BIC | K=3 BIC | **K=4 BIC** | persistence (mean diag of trans) |
| --- | ---: | ---: | ---: | ---: |
| ACO | 160,800 | 138,917 | **47,607** | 0.28 (k=4) |
| IPR | 155,808 | 131,992 | **13,353** | 0.27 (k=4) |

- BIC strongly prefers K=4 for both products.
- State variances at K=4 (sorted): **ACO** [≈0, 2.6, 8.1, 8.6]; **IPR** [≈0, 2.7, 5.3, 5.5].
- The "≈0 variance" state corresponds to ticks where mid did not change (the no-update regime). The other 3 states are low/medium/high jump magnitudes.
- Persistence ≈ 0.28-0.34 → states switch quickly (expected duration ~1.5 ticks). Not a regime that persists for hundreds of ticks.
- IC of state-mean to next-tick return = −0.48 (ACO K=4) — but this is dominated by the bid-ask bounce, not new information beyond what `imb1` already captures.

### Read

- HMM identifies a "no-move" state (expected) and 3 "moving" states. **It does NOT find a persistent volatility regime** that we can trade on.
- Combined with the volatility-clustering evidence (ARCH LM strongly rejected), the regimes are short-lived and well-modelled by a GARCH-like structure rather than discrete states.
- **HMM does not appear actionable** for a market-making bot. Confirmed by Round 1 result that an HMM-aware bot scored worse (~9,800 vs 10,094).

---

## 8. Cross-Product

| Pair | day −1 | day 0 | day 1 |
| --- | ---: | ---: | ---: |
| Level corr ACO–IPR | −0.03 | +0.08 | −0.41 |
| Return corr ACO–IPR | −0.007 | +0.008 | +0.002 |

- **Returns are essentially uncorrelated** → no cross-asset hedging signal.
- The day-1 level correlation of −0.41 reflects coincidental drift directions, not real co-movement.

---

## 9. Market Access Fee (MAF) — Value Estimate

Round 1 baseline P&L (best bot) = ~10,094, achieved with default 80% market access during testing.

If MAF wins → +25% extra quotes in book → roughly +25% extra fills → +25% extra P&L on the market-making part (ACO).

- Marginal value of MAF acceptance on ACO ≈ **+2,500 XIRECs** (rough upper bound).
- IPR contribution to MAF value ≈ marginal: it's a directional bet, not market-making, so extra quotes barely change the fills if we are always trying to be max-long.
- **Recommended bid range**: 1,500-3,000 XIRECs (median expected to land near 2,000). Bid 2,000-2,500 is top-50% likely; bidding > 5,000 is wasteful.

---

## 10. Reusable Metrics

For downstream specs (passed back to Phase 02/03):

| Metric | ACO | IPR |
| --- | ---: | ---: |
| Mid level | ~10000 | rises +1000/day |
| Within-day intra-trend std | ~5 | ~5 (after detrend) |
| Bid-ask spread (median) | 16 | 13-15 (rising) |
| Δmid std (per tick) | 3.7 | 3.1-3.6 |
| Δmid lag-1 ACF | −0.50 | −0.50 |
| Δmid² lag-1 ACF | +0.40 | +0.40 |
| Kalman Q (MLE) | 0.09 | 0.21 (incl. trend) |
| Kalman R (MLE) | 6.75 | 5.30 |
| Steady-state K | 0.10 | 0.15 |
| imb1 → Δmid IC (lag 1) | +0.65 | +0.65 |
| Level-1 depth (bid≈ask) | ~30 | ~24 |
| Mid-change frequency | 72% | 65% |
| Daily drift | ~0 | +1000 |

---

## 11. Facts vs Patterns vs Hypotheses

### Facts (directly from data)

- ACO mid is anchored at ~10000 across all 3 days (std ≤ 5.7).
- IPR mid drifts +999.7 / +1000.2 across consecutive days — almost exactly +1000/day.
- Bid-ask spread is 16 for ACO and 13/14/15 for IPR (rising by 1 tick per day).
- 7.4-7.9% of ticks have a one-sided book.
- Level-1 depth: ACO ~30, IPR ~24 per side.
- ACF(Δmid, lag 1) = −0.50 across all 6 product-day combinations.
- ACF(Δmid², lag 1) = +0.40 → real volatility clustering (ARCH LM p=0).
- Imbalance(t) → Δmid(t+1) IC = +0.65 for both products.
- ADF rejects unit root on first-differenced series; KPSS rejects trend-stationarity on raw mid.

### Patterns (statistically significant but not laws)

- Round 1 → Round 2 spreads widened (ACO 12 → 16; IPR was new). May continue.
- IPR drift is 0.10 per tick on average, executed via many small +1 jumps interspersed with mean-reverting noise.
- Kalman MLE Q,R are stable across days (Q stable to within ±15%).

### Hypotheses (need testing)

- The +1000/day IPR drift continues on submission day. **High prior** (3/3 days observed), but only n=3.
- Quoting passively at top-of-book with imbalance-aware skew (IC=0.65) outperforms a constant-skew quote.
- A two-state Kalman (level + drift) for IPR will outperform a one-state Kalman.
- HMM does not add value for either product.
- A bid of 2,000 for MAF lands in the top 50%.

### Open questions / Risks

- Will the IPR drift continue or reverse on submission day? 1-day reversal could cost ~80,000 XIRECs at max long.
- Are the dirty `mid=0` rows present in the live submission environment? If yes, our bot must handle empty books (already does in candidate_04).
- Is the MAF median bid in the test population ≤ 2,000 or higher? No data; can only reason game-theoretically.
- What is the participant-level distribution of the imbalance signal? If many bots already use it strongly, our edge from it is smaller.

---

## 12. Downstream Use

| Phase | Take from this EDA |
| --- | --- |
| Understanding (02) | IPR is directional (+1000/day); ACO is market-making (~10000). Imbalance has IC=0.65 (lag 1). HMM not actionable. |
| Strategy (03) | Candidate set: (a) max-long IPR + Kalman-MM ACO with strong imbalance skew; (b) variants tuning imbalance gain, Kalman Q/R, and quote sizing; (c) MAF bid 2,000-2,500. |
| Spec (04) | Calibrated Kalman: Q=0.09, R=6.75 for ACO. For IPR, prefer trend-aware filter. Imbalance shift in quote ~ 4-6 ticks at imb1=±1. |
| Implementation (05) | Re-use Round 1 candidate_04 code skeleton (one-sided book handling, asymmetric sizes), tune the imbalance multiplier and Kalman params. |
| Testing (06) | A/B vs Round 1 candidate_04 baseline on R2 day −1/0/1 data. |
