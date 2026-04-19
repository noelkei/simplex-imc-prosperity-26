# Strategy Candidates — Round 2

Maximum active candidates per round: 3 (shortlist; all 10 implemented per explicit request).

## Status

READY_FOR_REVIEW

## Sources

- Wiki facts: `docs/prosperity_wiki_raw/13_round_2.md`
- Understanding summary: `rounds/round_2/workspace/02_understanding.md`
- EDA evidence: `rounds/round_2/workspace/01_eda/eda_round_2.md`, `rounds/round_2/workspace/01_eda/outputs/eda_summary.json`
- Round 1 performance logs: `rounds/round_1/performances/bruno/canonical/190076.log`, `200823.log`
- Round 1 best bots: `candidate_26_v3_a3b1_one_sided_exit_overlay.py`, `candidate_07_kf_tuned.py`

---

## Evidence Summary (R1 Performance Logs + R2 EDA)

| Signal | Value | Trading Implication |
| --- | --- | --- |
| IPR daily drift | +1000/day (+0.001/timestamp) | Max-long +80 yields ~7,286 ACO P&L per run |
| ACO cross-day drift | ±1.4 ticks over 3 R2 days | FV=10000 robust; no drift risk |
| ACO imbalance IC (lag 1) | **0.647** (n=30k ticks) | β≈6.85 ticks/unit imb; 1-tick predictive |
| ACO imbalance IC (lag 2+) | ≈0.00 | No EWM smoothing — signal is purely instantaneous |
| ACO return ACF (lag 1) | −0.50 | Bid-ask bounce; NOT a tradeable signal |
| ACO Kalman MLE (R2) | Q=0.092, R=6.75, K≈0.11 | 8× more reactive than R1 c_07 (K≈0.014) |
| R1 baseline ACO P&L (log 190076) | 2,132/run | With gain=2; 29% of IC signal captured |
| R1 baseline IPR P&L (log 190076) | 7,286/run | Stable across runs; max-long is optimal |
| MAF estimated extra value | ~+2,524 XIREC | +25% fills on top of 80% baseline access |

**Critical gap identified:** baseline imb_gain=2 captures only **29%** of the IC=0.647 signal.
Raising to gain=4 → 58%; gain=6 → 88%. This is the highest-value single improvement available.

---

## Candidate Table

| Candidate ID | Product | Edge Source | KF_Q/KF_R | IMB_GAIN/CLIP | TAKE_IMB_ADJ | MAX_IMB_TAKE | SIZE_ADAPT | MAF | Evidence Strength | Priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `r2_b01_baseline` | IPR+ACO | Control: R1 c_07 + bid() | 0.005/25.0 | 2.0/2.0 | No | — | No | 2500 | strong | low |
| `r2_b02_imb4` | IPR+ACO | Imbalance gain ×2 | 0.005/25.0 | 4.0/4.0 | No | — | No | 2500 | strong | medium |
| `r2_b03_imb6` | IPR+ACO | Imbalance gain ×3 | 0.005/25.0 | 6.0/5.0 | No | — | No | 2500 | strong | **high** |
| `r2_b04_kf_mle` | IPR+ACO | R2 MLE Kalman only | 0.092/6.75 | 2.0/2.0 | No | — | No | 2500 | medium | medium |
| `r2_b05_kf_imb4` | IPR+ACO | R2 Kalman + gain=4 | 0.092/6.75 | 4.0/4.0 | No | — | No | 2500 | medium | medium |
| `r2_b06_take_adj` | IPR+ACO | Imb-adjusted take threshold | 0.005/25.0 | 4.0/4.0 | Yes | 4 | No | 2500 | medium | **high** |
| `r2_b07_kf_take_adj` | IPR+ACO | R2 Kalman + imb takes | 0.092/6.75 | 4.0/4.0 | Yes | 4 | No | 2500 | medium | medium |
| `r2_b08_size_adapt` | IPR+ACO | Adaptive quote sizing | 0.005/25.0 | 4.0/4.0 | Yes | 3 | Yes | 2500 | medium | medium |
| `r2_b09_full` | IPR+ACO | ALL combined | 0.092/6.75 | 5.0/5.0 | Yes | 5 | Yes | 2500 | strong | **high** |
| `r2_b10_maf3000` | IPR+ACO | b09 + higher MAF bid | 0.092/6.75 | 5.0/5.0 | Yes | 5 | Yes | 3000 | weak | medium |

---

## Candidate Detail

### r2_b01_baseline — Control (R1 c_07 + MAF bid)

**Edge:** Identical to Round 1 candidate_07_kf_tuned. Adds bid()=2500 for MAF.
Verified R1 performance: IPR=7,286, ACO=2,132 → total=9,418 per backtest run.

**Purpose:** All other bots measured against this. If a bot shows ACO > 2,132, its axis adds value.

**File:** `../bots/bruno/canonical/r2_b01_baseline.py`

---

### r2_b02_imb4 — Imbalance Signal Gain=4

**Edge:** Gain=4 captures 58% of IC=0.647 signal (vs 29% at gain=2).
- When imb=0.7: qfair shifts +2.8 ticks → ask raised 2.8 ticks, bid lowered 2.8 ticks
- At imb=1.0: qfair shifts +4 → ask at FV+9 (vs FV+7 baseline), bid at FV-9

**Expected gain:** +150-400 ACO P&L vs baseline.

**File:** `../bots/bruno/canonical/r2_b02_imb4.py`

---

### r2_b03_imb6 — Imbalance Signal Gain=6, Clip=5 ⭐ Shortlisted

**Edge:** Gain=6 captures 88% of the IC=0.647 regression signal. Clip=5 limits max
shift to 5 ticks to prevent runaway exposure.

**Key math:** When imb=0.8, expected next-tick Δmid = 0.647 × (3.7/0.35) × 0.8 = 5.5 ticks.
Our ask shifts to FV+10 (HS=5 + inv_skew + micro=5). A buyer hitting our ask at FV+10
gives us 5 extra ticks premium on a correctly-predicted upward move.

**Risk vs reward (per fill at imb=0.8):**
- Signal correct (est. ~82% directional accuracy): extra 5-tick premium vs baseline
- Signal wrong (18%): opponent fills us at "expensive" price; inventory risk manageable
  since position filter prevents runaway accumulation

**File:** `../bots/bruno/canonical/r2_b03_imb6.py`

---

### r2_b04_kf_mle — R2 MLE Kalman (Reactive FV Tracking)

**Edge:** K≈0.11 vs K≈0.014 in R1. Adapts FV 8× faster to intraday mid-price shifts.
When ACO price holds off 10000 for 50+ ticks (transient drift event), the reactive
filter re-centers quotes ~10 ticks sooner than the stable R1 filter.

**Risk:** Partly tracks bid-ask bounce → ±0.33 tick FV oscillation (vs ±0.04 in R1).
Both magnitudes are small enough to be benign.

**File:** `../bots/bruno/canonical/r2_b04_kf_mle.py`

---

### r2_b05_kf_imb4 — R2 Kalman + Gain=4 (Compounding Axes)

**Edge:** Tests whether reactive KF and stronger imbalance compound. When KF FV drifts
+2 ticks (intraday event) AND imb=0.8 bullish: qfair = (10002) + 3.2 = 10005.2 → we
hold our ask 5 ticks above raw FV with dual confirmation.

**File:** `../bots/bruno/canonical/r2_b05_kf_imb4.py`

---

### r2_b06_take_adj — Imbalance-Adjusted Take Threshold ⭐ Shortlisted

**Edge (new mechanism):** Baseline only takes asks BELOW raw FV (edge > 0). This bot
uses the imbalance-adjusted FV (qfair = FV + micro) as the take threshold, capped
at FV ± MAX_IMB_TAKE.

**Mathematical justification for buying at FV+3 when imb=0.7:**
- E[Δmid | imb=0.7] = IC × β × imb = 0.647 × (3.7/0.35) × 0.7 = 4.8 ticks
- Buy at FV+3 (3 above raw FV): expected gain = 4.8 - 3 = +1.8 ticks → positive EV
- Buy at FV+4: expected gain = 4.8 - 4 = +0.8 ticks → still positive
- MAX_IMB_TAKE=4 ensures we never take more than 4 ticks above raw FV

Symmetric on the sell side: sell at FV-3 when imb=-0.7, expected gain = 4.8-3 = +1.8.

**New fills captured:** ~40% of ticks have |imb|>0.5; of those, some have asks in
[FV, FV+4] range. Each such fill earns +0.5-2.5 tick above what baseline would earn.

**File:** `../bots/bruno/canonical/r2_b06_take_adj.py`

---

### r2_b07_kf_take_adj — R2 Kalman + Imbalance Takes

**Edge:** Combines reactive KF (b04) + imbalance-adjusted takes (b06). Higher-variance
version: the reactive KF means fv_int itself drifts, and the take threshold follows
both KF drift AND imbalance — potentially very aggressive when both signals align.

**File:** `../bots/bruno/canonical/r2_b07_kf_take_adj.py`

---

### r2_b08_size_adapt — Adaptive Quote Sizing by Imbalance

**Edge:** When imb=1 (price rising): buy_sz amplified by up to 40%, sell_sz reduced
by 30%. Amplifies profitable fills (buying before predicted rise) and reduces
adversely-selected sells (selling cheap before further rise).

Sizes at imb=1.0 with pos=0: buy_sz = 60×1.40=84 (capped 80); sell_sz = 60×0.70=42.

**File:** `../bots/bruno/canonical/r2_b08_size_adapt.py`

---

### r2_b09_full — Full Combined Candidate ⭐ Shortlisted (Primary Submission)

**Edge:** All four R2 improvements combined:
1. R2 MLE Kalman (K≈0.11)
2. IMB_GAIN=5, IMB_CLIP=5 (73% of IC signal)
3. TAKE_IMB_ADJ=True, MAX_IMB_TAKE=5 (takes up to 5 ticks beyond raw FV on signal)
4. SIZE_ADAPTIVE=True (±40% quote size scaling by imbalance)

**Behavior at imb=1.0 (strongly bullish), pos=0:**
- KF FV≈10000; micro=+5; qfair=10005
- take_buy_thr = min(10005, 10005) = 10005 → takes all asks at 9995-10004
- bid_px = min(bb+1, 10000) → aggressive buy at FV; ask_px = max(ba-1, 10010)
- buy_sz=80 (max amplified); sell_sz=42 (reduced)
- Net: large aggressive buy + high passive ask → positioned for predicted rise

**Expected total P&L:** b01 baseline (~9,418) + ACO improvement (+300-1,000) +
MAF win (+0 or +2,500) = **9,700-12,900 per run** depending on MAF outcome.

**File:** `../bots/bruno/canonical/r2_b09_full.py`

---

### r2_b10_maf3000 — Full Combined + MAF Bid=3000

**Edge:** Identical to b09 but bid()=3000. Tests whether paying extra 500 improves
MAF win probability enough to be net positive. Key comparison: b10_total vs b09_total.
If b10 wins MAF more often, the extra 500 is recouped by extra fills.

**File:** `../bots/bruno/canonical/r2_b10_maf3000.py`

---

## Experiment Design

| Experiment | Bots | Metric |
| --- | --- | --- |
| Imbalance gain sweet spot | b01, b02, b03 | ACO P&L; b03 target = 2,600+ |
| Kalman tuning effect | b01, b04; b02, b05 | ACO P&L isolated; small expected delta |
| Take threshold innovation | b02, b06; b05, b07 | ACO P&L delta; b06 target = +200 vs b02 |
| Sizing adaptation | b06, b08 | ACO P&L; small expected delta |
| Full combination | b01, b09 | Total P&L; target ≥ 10,000 without MAF |
| MAF sensitivity | b09, b10 | P&L after fee; confirms optimal bid |

---

## Rejected or Deferred Ideas

| Idea | Reason |
| --- | --- |
| HMM regime-adaptive spread (c_05/c_06 logic) | persistence_diag=0.28-0.47 in R2 (too short-lived); IC(HMM_state→ret)=-0.31 (wrong sign) |
| EWM-smoothed imbalance | Signal is purely lag-1 (IC_lag2≈0.00); smoothing adds stale past signal |
| Exit overlay (liquidate at cross) | R1 proven: 13-tick loss per exit vs 5-tick passive; destroys ACO P&L |
| IPR spread-crossing entry (bid at ask price) | Drift >> spread, but cost = 6-8 ticks spread × 80 units = 480-640 ticks wasted |
| Cross-product hedge (ACO+IPR) | Return correlation ≈ 0 (day-1: -0.007; day_0: +0.008; day_1: +0.002) — no hedge signal |
| Pure imbalance market taker | Half-spread=8 ticks (ACO) >> E[Δmid|imb=1.0]=4.8 ticks → negative EV |
| HMM k=4 states | IC(k4_state→ret)=-0.48; negative predictive power; state variance dominated by one outlier |

---

## Shortlist

1. **r2_b03_imb6** — Primary single-axis test. Clean IC=0.647 evidence. Lowest risk, high reward.
2. **r2_b06_take_adj** — Novel mechanism with positive-EV mathematical proof. Medium risk.
3. **r2_b09_full** — Highest expected P&L. All axes combined. Test vs b01 baseline to confirm.

Rationale: b03 is the "must-have" improvement. b06 adds a new fill source with justified EV.
b09 is the "swing for the fences" candidate that combines everything into one submission bot.

## Human Decisions Needed

- **Which bot to submit as final candidate?** Run all 10 against days -1/0/1 and compare.
- **MAF bid calibration:** If b09 ACO P&L improves to 3,000+, the MAF extra value increases
  proportionally. Consider whether 2,500 or 3,000 better reflects expected extra value.
- **If live IC is saturated:** Fall back to b02 or b03 (moderate gain, safe). Watch b09 ACO P&L
  — if it underperforms b01 by more than 200, the live IC has degraded.

## Next Action

1. Backtest all 10 bots against R2 CSV data (days -1, 0, 1).
2. Compare ACO P&L columns. Rank candidates.
3. Select best 2-3 for Phase 04 formal spec.
4. Choose final submission candidate for Phase 05.
