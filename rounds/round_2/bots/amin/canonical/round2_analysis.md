# Round 2 — Simplex Analysis (Amin)

## Date: 2026-04-19

---

## Phase 00 — Ingestion

- **Products**: `ASH_COATED_OSMIUM` (limit 80), `INTARIAN_PEPPER_ROOT` (limit 80)
- **Round-specific mechanic**: `Trader.bid()` for Market Access Fee
  - Top 50% bids accepted; fee deducted from profit; winners get 25% more quotes
  - Negative bids treated as 0; no-submission teams excluded from Speed ranks
- **Manual challenge**: Allocate 50,000 XIRECs across Research / Scale / Speed
- **Data**: 3 days (day -1, 0, 1), 10,000 timestamps per product per day, 100ms spacing

---

## Phase 01 — EDA Key Findings

### IPR (INTARIAN_PEPPER_ROOT)

| Metric | Value |
|---|---|
| Drift rate | +0.001 per timestamp unit = ~1,000/day |
| Drift linearity | Perfect (R² ≈ 1) across all 3 days |
| Day -1 range | 11,001 → 11,999 (Δ = +998) |
| Day 0 range | 11,998 → 13,000 (Δ = +1,002) |
| Day 1 range | 13,000 → 13,999 (Δ = +1,000) |
| FV residual std | ~2.2, max ~11 |
| Residual autocorr | -0.50 (mean-reverting) |
| Spread mean | 14 |
| Top-book imbalance → next mid corr | 0.38–0.40 |
| Volume at best | ~11.6 per side |

### ACO (ASH_COATED_OSMIUM)

| Metric | Value |
|---|---|
| Drift rate | ~0 (no trend) |
| Mean price | ~10,000 across all days |
| Spread mean | 16 |
| Return autocorr | -0.50 (mean-reverting) |
| Top-book imbalance → next mid corr | 0.37–0.38 |
| Volume at best | ~14.2 per side |
| After up, next return | -1.5 (reverts) |
| After down, next return | +1.5 (reverts) |

### Cross-product

- 100 zero-mid-price rows (book empty at those ticks) — handled by filtering
- No exploitable cross-product lead-lag

---

## Phase 02 — Understanding

1. **IPR is the dominant PnL source**: holding 80 units long for one full day captures ~80,000 XIRECs from drift alone
2. **ACO is secondary market-making**: mean-reversion around stable FV, realistic platform PnL a few thousand per day
3. **Position limit is binding**: the faster we get to +80 IPR, the more drift we capture
4. **Platform testing uses randomized 80% quote subset** → expect run-to-run variance of ~500-1000 XIRECs

---

## Phase 03 — Strategy

### Algorithmic Strategy

| Strategy | Product | Logic |
|---|---|---|
| **Drift capture** | IPR | FV(t) = base + 0.001×t. Aggressively buy to position limit 80. Hold. Only sell on extreme overshoot (>15 above FV). |
| **Mean-reversion MM** | ACO | EMA fair value (α=0.15). Take liquidity when price deviates >1 from FV. Place passive quotes at FV ± 3. Inventory skew (0.05 per unit). |
| **MAF bid** | Both | 150 XIRECs — moderate bid to try for top 50% without significant cost |

### Manual Challenge Strategy

**Formula**: PnL = (Research × Scale × Speed) − Budget_Used

- Research(x) = 200,000 × ln(1+x) / ln(101)
- Scale(x) = 7 × x / 100
- Speed = rank-based 0.1 (worst) to 0.9 (best)
- Budget_Used = (R% + Sc% + Sp%) / 100 × 50,000

**Optimal split is always R=23%, Sc=77%** regardless of Speed multiplier.

| Scenario | R | Sc | Sp | Speed Mult | Expected PnL |
|---|---|---|---|---|---|
| Zero Speed (worst mult=0.1) | 23% | 77% | 0% | 0.1 | 24,233 |
| Zero Speed (mid mult=0.5) | 23% | 77% | 0% | 0.5 | 321,165 |
| Zero Speed (best mult=0.9) | 23% | 77% | 0% | 0.9 | 618,097 |
| Hedged 2% Speed | 23% | 75% | 2% | ~0.5 | 311,524 |

**Recommendation**: **R=23%, Sc=77%, Sp=0%**. If most teams invest 0 in Speed, everyone shares rank 1 → 0.9 multiplier → 618K PnL. Alternatively R=23%, Sc=75%, Sp=2% for insurance (costs only 1,000 XIRECs).

---

## Phase 04 — Implementation

### Bot file

`round2_simplex_v1.py` in this folder.

### Bot parameters

| Parameter | Value | Rationale |
|---|---|---|
| `IPR_DRIFT` | 0.001 | From regression on 3 days of data |
| `ACO_EMA_ALPHA` | 0.15 | Responsive enough for mean-reversion |
| `IPR_TAKE_MARGIN` | 5 | Buy aggressively since drift dominates |
| `ACO_TAKE_EDGE` | 1 | Minimum edge to take ACO liquidity |
| `ACO_QUOTE_OFFSET` | 3 | Passive quote distance from FV |
| `MAF_BID` | 150 | Moderate bid for top-50% acceptance |

### Verification

- ✅ `py_compile` passed
- ✅ Smoke test passed (position limits, order signs, `bid()` returns int)
- ✅ Backtest IPR PnL: ~80K/day (reliable, drift-driven)
- ✅ ACO adds supplementary PnL from mean-reversion

### Backtest Results (approximate)

| Day | IPR PnL | ACO PnL (realistic est.) | Total Est. |
|---|---|---|---|
| -1 | ~79,700 | ~2,000–3,000 | ~82,000 |
| 0 | ~80,100 | ~2,000–3,000 | ~83,000 |
| 1 | ~80,000 | ~2,000–3,000 | ~83,000 |

Note: ACO backtest passive-fill assumptions overestimate. Real platform ACO PnL likely 2,000–4,000 based on Battery 01 evidence.

---

## Key Risks & Caveats

- Platform testing uses randomized 80% quote subset → PnL variance across submissions
- IPR drift rate assumed constant at 0.001; if it changes in final simulation, PnL scales linearly
- ACO spread gates in prior bots over-throttled activity → this bot uses looser thresholds
- MAF bid of 150 is a guess; competitive bid distribution is unknown
- Manual Speed rank depends on other players' choices
- `traderData` string limited to 50,000 chars (our usage is well within this)
