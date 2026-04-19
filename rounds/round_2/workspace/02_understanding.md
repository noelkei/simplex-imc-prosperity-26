# Understanding Summary

## Status

READY_FOR_REVIEW

## Sources

- Wiki facts: `docs/prosperity_wiki_raw/13_round_2.md`
- EDA evidence: `rounds/round_2/workspace/01_eda/eda_round_2.md`, `rounds/round_2/workspace/01_eda/outputs/eda_summary.json`
- Ingestion: `rounds/round_2/workspace/00_ingestion.md`
- Round 1 carry-over evidence: `rounds/round_1/workspace/02_understanding.md`, `rounds/round_1/bots/bruno/canonical/candidate_04_kalman_imb.py`
- Playbook heuristics: not used as evidence

---

## Current Understanding

### INTARIAN_PEPPER_ROOT (IPR)

- **Fact**: Position limit 80 (unchanged from Round 1).
- **Fact**: Wiki describes it as "quite steady" (Round 1 wiki language carried over).
- **Evidence (R2 data)**: Mid drifts upward at **+1000 XIRECs per day**, day-over-day deltas measured: +999.74 (day −1 → 0), +1000.19 (day 0 → 1). OLS per-tick drift ≈ +0.001/tick — **identical to Round 1**.
- **Evidence**: Day-start mids ≈ 11500 → 12500 → 13500. The cross-day +1000 jump persists in R2.
- **Evidence**: Within-day intra-trend std ≈ 3 (after detrending), spread 13/14/15 (rising +1 per day).
- **Evidence**: ADF test rejects unit root (p=0) on first-differenced series → returns are stationary; the level is non-stationary trend + noise.
- **Hypothesis (high prior)**: The +1000/day drift continues on submission day. Two independent rounds (3 days each = 6 day-segments) all show the same +0.001/tick rate. This is the strongest cross-data invariant we have.
- **Hypothesis**: The slight spread widening (+1/day) may continue to ~16 on submission day. Negligible P&L impact.

#### Why directional dominates market-making for IPR

| Strategy | Avg position | Drift gain (per day, per round) | Spread income | Total per day |
| --- | ---: | ---: | ---: | ---: |
| Directional max-long (buy 80 ASAP, hold) | +80 | 80 × 1000 = **80,000** | ~0 | ~80,000 |
| Drift-tracking market maker | ~0 (buys ≈ sells) | ~0 | 1,000-2,000 | 1,000-2,000 |

A market maker that sells at the rising ask surrenders ~0.001/tick × N ticks of future drift gain in exchange for ~1-2 ticks of spread. Drift signal-to-noise is 5-6x: every sell loses in expectation. **Buy 80 ASAP and hold** remains the optimal IPR strategy. This is now confirmed by 6 day-segments of identical evidence.

---

### ASH_COATED_OSMIUM (ACO)

- **Fact**: Position limit 80 (unchanged).
- **Fact**: Round 2 wiki carries the "hidden pattern" hint from Round 1.
- **Evidence (R2 data)**: Mid is anchored at ~10000 across all 3 R2 days (10000.83 / 10001.61 / 10000.21). Within-day std ≤ 5.7. Day-over-day drift +0.78 / −1.40 → effectively zero.
- **Evidence**: Spread = **16 ticks** (median, all 3 days). Half-spread = 8. One-sided book ~7.5% of ticks.
- **Evidence**: ACF(Δmid, lag 1) = −0.50 → bid-ask bounce at 1-tick scale. Lags 2-5 ≈ 0 → no longer-horizon momentum.
- **Evidence**: ACF(Δmid², lag 1) = +0.40 with ARCH-LM p=0 → real volatility clustering at 1-2 tick scale.
- **Evidence (NEW from deep EDA)**: Order book imbalance at top-of-book has **information coefficient +0.647** vs next-tick mid change. Signal dies at lag 2. This is one of the strongest microstructure signals we have ever measured.
- **Evidence (NEW from deep EDA)**: Kalman MLE on 3 days gives **Q=0.092, R=6.75** (steady-state K≈0.10) for ACO. Round 1 final calibration used Q=0.005, R=25 — substantially under-reactive. The Round 1 Kalman lag is part of why scores plateaued at ~10,094.
- **Hypothesis**: Fair value 10,000 holds on submission day (no cross-day drift in 6 day-segments).
- **Hypothesis**: A re-tuned Kalman + stronger imbalance skew can lift ACO market-making P&L meaningfully above the ~10,094 baseline.
- **Hypothesis (revised from R1)**: The Round 1 long-horizon autocorrelation reading (lag 50 ≈ 0.78) was likely contaminated by zero-mid rows; the R2 deep EDA finds white-noise tails after lag 1. The "much more persistent than AR(1)" interpretation needs revisiting before being relied on.

---

### Market Access Fee (MAF) — new mechanic

- **Fact**: `bid()` method returns an integer XIRECs; one-time fee deducted from R2 P&L if bid lands in **top 50%** of all participants' bids.
- **Fact**: Reward = 25% extra quotes injected into the order book → roughly 25% extra fills on the market-making leg.
- **Fact**: Blind auction — bids are not revealed until final scoring.
- **Evidence (heuristic)**: Round 1 best P&L ≈ 10,094 ⇒ marginal value of 25% extra fills ≈ **+2,500 XIRECs**. Above this bid is destruction of value. Below this risks falling under the median.
- **Hypothesis**: The participant median is somewhere in the 1,500-2,500 range (rational players cluster near the marginal value).
- **Strategy**: Bid in the **2,000-2,500 range**. This is top-50%-likely without overpaying. Bidding 3,000+ guarantees acceptance but burns ~500-1,000 of value if accepted.

---

## Evidence Synthesis

| Claim | Source | Strength | Decision Impact | What Would Change This |
| --- | --- | --- | --- | --- |
| IPR drifts +1000/day | R1 + R2 EDA (6 day-segments) | **strong** | high | One day-segment with no drift in live data |
| ACO mid anchored at ~10000 | R1 + R2 EDA | **strong** | high | Day-over-day drift > 5 in any segment |
| Imbalance IC = 0.65 (lag 1) on R2 data | R2 deep EDA | **strong** (n≈30k per product) | high | Lower IC after live submission; would drop signal weight |
| Bid-ask spread = 16 (ACO), 13-15 (IPR) | R2 EDA | strong | medium | Spreads narrow significantly in live env |
| Kalman MLE Q≈0.09, R≈6.75 for ACO | R2 EDA (3-day MLE) | medium-strong | high | Different tuning beats it in backtest |
| HMM regimes are not actionable | R1 + R2 EDA | medium | low (rule out) | New evidence of long-persistent regimes |
| Cross-asset return correlation ≈ 0 | R2 EDA | strong | low (no hedge) | Live correlation > 0.1 |
| MAF marginal value ~2,500 | Heuristic from R1 baseline | weak | medium | Live P&L without MAF much higher than 10k |
| MAF median bid in 1,500-2,500 range | Game-theoretic guess | **weak** | medium | Any participant-distribution data |

---

## Confidence and Impact

- **Overall confidence**: high on per-product mechanics; medium on MAF auction outcome.
- **Highest-impact implication**: Max-long IPR is essentially free money. Failing to hold +80 on day 1 costs ~80,000 XIRECs.
- **Main caveat**: Submission-day environment may differ from historical CSVs (other bots adapt; spreads may move). All numerical edges should be treated as *expected* not *guaranteed*.

---

## Assumptions

- IPR upward drift continues on submission day at ~+0.001/tick.
- ACO fair value remains ~10,000 with no cross-day shift.
- The order-book imbalance signal IC=0.65 holds in the live environment (no aggressive arbitrageurs that have already priced it in faster than us).
- Position limits, spread mechanics, and MAF rules in the wiki are accurate.
- The 80% market-access during testing is replaced by 100% if MAF bid wins (we cannot test this directly).
- Other competitors will bid for MAF rationally, with median in 1,000-3,000 range.

---

## Open Questions

- **Will the +1000/day IPR drift continue on submission day?** 6/6 day-segments observed support yes, but the live test is ultimately a single sample.
- **What is the actual MAF median bid?** Cannot be measured ex-ante. Game theory only.
- **Should the IPR Kalman use a 2-state model** (level + slope) instead of a 1-state local-level filter? Possible Phase-04 spec consideration.
- **Is the imbalance signal already saturated by other market makers?** If yes, our marginal edge from increasing the skew is smaller than the IC=0.65 backtest suggests.
- **How much does Kalman re-tuning (Q=0.09 vs 0.005) actually move the P&L?** Need a controlled A/B run vs candidate_04 / candidate_07 baseline.

---

## Prioritized Unknowns

| Unknown | Affects | Priority | Next Action |
| --- | --- | --- | --- |
| Submission-day IPR drift continues? | Strategy, P&L | high | Defer with risk; monitor first ticks if observable |
| MAF participant median | MAF bid value | medium | Game-theoretic decision; pick 2,000-2,500 |
| Imbalance IC saturation in live env | Signal weight in spec | medium | Test conservatively first, then increase |
| Optimal imbalance shift coefficient | Spec for ACO MM | high | A/B variants in implementation phase |
| Optimal Kalman Q,R | Spec for ACO MM | medium | A/B vs MLE tuning + fixed Round 1 tuning |
| Best MAF bid value | MAF bid | high | Game-theoretic; pick mid-range 2,000-2,500 |

---

## Strategy Implications

- **Candidate direction (primary)**: Max-long IPR + re-tuned Kalman ACO market maker with strengthened imbalance skew. MAF bid 2,000-2,500.
- **Candidate direction (secondary)**: Variants on imbalance gain (linear vs sigmoid scaling), Kalman parameters (MLE vs Round 1 tuned vs adaptive), and quote sizing schedules.
- **Risk or constraint**: Position limits ±80 on each product. IPR strategy reaches the limit very quickly; downside is symmetric (no IPR drift would mean no loss but also no gain).
- **Validation/debug implication**: Backtest each candidate on R2 day −1/0/1; primary metric = P&L; secondary metric = drawdown / position trajectory.

---

## Next Action

Next: Phase 03 (Strategy Candidates) — enumerate 3-5 specific candidate bots that explore the axes identified above (Kalman tuning × imbalance gain × quote sizing × MAF bid).
