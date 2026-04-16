# Strategy Candidates

Maximum active candidates per round: 3.

## Status

READY_FOR_REVIEW

## Sources

- Wiki facts: `docs/prosperity_wiki/rounds/round_1.md`, `docs/prosperity_wiki/trading/02_orders_and_position_limits.md`
- Understanding summary: `rounds/round_1/workspace/02_understanding.md`
- EDA evidence: `rounds/round_1/workspace/01_eda/eda_round_1.md`
- Playbook heuristics: not used as primary basis; strategy class selection driven by EDA evidence

## Candidate Table

| Candidate ID | Product Scope | Source Of Edge | Linked EDA Signals | Feature Evidence | Regime Assumptions | Understanding Insight | Key Assumptions | Main Risk | Evidence Strength | Implementation Cost | Validation Speed | Risk Level | Expected Upside | Priority | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `candidate_01_ipr_directional` | `INTARIAN_PEPPER_ROOT` | Linear drift +~1,003/day; holding max long (80 units) captures full drift gain. Directional is 4–8x better than market-making. | `01_eda/eda_round_1.md` — IPR drift (+0.001/tick, consistent 3 days), book depth (11–12 L1), trade qty (avg 5, max 8) | drift +0.001/tick across 3 days; day-start +1,000 above prior day; signal-to-noise 5–6x; L1 depth sufficient for quick fill | drift rate continues in live round | Understanding: drift magnitude makes directional 4–8x better than MM; every sell sacrifices future drift gain | Drift holds in live round; L1 depth allows position fill in first few ticks | Drift stops or reverses in live round | strong | low | high | medium | high | high | draft |
| `candidate_02_aco_fixedfv` | `ASH_COATED_OSMIUM` | Fixed fair value 10,000 with tight market spread; one-sided quoting prevents runaway inventory | `01_eda/eda_round_1.md` — ACO fixed fair value, autocorr profile (lag-1=0.789, lag-50=0.717 >> AR(1) prediction) | FV=10,000 across 3 days, stdev 4–5, market spread 16 dominant, autocorr flat across all lags | live level remains around 10,000; slow persistent reversion continues | Understanding: ACO persistence is far stronger than simple AR(1) implies — positions can accumulate for 100+ ticks; one-sided quoting needed | FV=10,000 holds in live round; one-sided quoting caps inventory | Position accumulates at extreme price before reversion; without one-sided quoting, risk of hitting limit | strong | low | high | low | medium | high | draft |
| `candidate_03_combined` | `INTARIAN_PEPPER_ROOT` + `ASH_COATED_OSMIUM` | Candidates 01 + 02 combined into one submission bot | linked signals from candidates 01 and 02 | no new feature evidence; packaging of two independent signals | products remain independent enough to run separately in one trader | Understanding: combined independent trader should be tried after individual validation | Both individual candidates are valid | Either individual strategy fails and drags overall P&L | strong | low | high | low | high | high | draft |

---

## Candidate Detail

### candidate_01_ipr_directional — IPR Directional Max-Long

**Edge:** INTARIAN_PEPPER_ROOT drifts upward ~1,003 ticks per simulation day. Holding 80 units (position limit) captures the full drift gain: 80 × ~90 price ticks per run ≈ 7,200 realized P&L. A drift-tracking market maker averages ~0 inventory and earns only spread income (~1,000–2,000/run). Directional is 4–8x better.

**Why directional beats market-making:**
- A market maker quotes on both sides and buys and sells in roughly equal quantities.
- In a trending market, each sell order surrenders a unit of long position that would have gained `drift_per_tick × remaining_ticks`.
- With drift >> spread, surrendering drift gain to capture a spread tick is a losing exchange.
- The correct action is: never sell. Hold max long. Let the drift do the work.

**Why not drift-tracking market maker:**
The EDA's own downstream recommendation is "drift-tracking MM." This recommendation does not compute the magnitude comparison. The EDA establishes the drift rate (+0.001/tick). The understanding phase shows that at 80 units × ~90 ticks drift ≈ 7,200 >> ~1,000–2,000 spread income. The MM recommendation is discarded.

**Execution sketch:**
1. Each tick: compute `capacity = 80 - current_position`.
2. If `capacity > 0`: sweep all ask levels in the book (buy as many as possible, up to capacity).
3. If capacity remains after sweeping: place a resting bid at `best_bid + 1` to attract incoming sellers.
4. Never sell (no ask orders placed).

**Parameters:** None — fully mechanical. Position limit = 80.

**Validation check:** Position should reach +80 within the first few ticks (L1 depth 11–12, L2 ~20 at 65% of ticks — sufficient for quick fill at reasonable prices). P&L should grow proportionally with drift throughout the run.

---

### candidate_02_aco_fixedfv — ACO Fixed-FV Market Maker with One-Sided Quoting

**Edge:** ASH_COATED_OSMIUM mean-reverts around a fixed fair value of 10,000. Quoting around 10,000 with a spread tighter than the bot spread (16) captures the bid-ask spread. One-sided quoting prevents inventory accumulation during prolonged deviations.

**Why one-sided quoting matters:**
EDA shows autocorr at lag 50 = 0.717. Pure AR(1) with φ=0.789 would predict lag-50 autocorr ≈ 0. The process is far more persistent. Deviations from 10,000 can sustain for 100+ ticks. If price stays below 10,000 for 100 ticks and we keep bidding, we accumulate ~40 units before price reverts. Without one-sided quoting, position limit risk is real.

**Execution sketch:**
1. Each tick: `fv = 10000` (constant).
2. Compute `skew = round((position / pos_limit) * SKEW_FACTOR)` (proportional inventory skew).
3. `my_bid = fv - HALF_SPREAD - skew`, `my_ask = fv + HALF_SPREAD + skew`.
4. Aggressive: take any ask strictly below fv; hit any bid strictly above fv.
5. Passive: place resting bid only if `position < ONE_SIDED_THRESHOLD`; place resting ask only if `position > -ONE_SIDED_THRESHOLD`.
   - `ONE_SIDED_THRESHOLD = 40` (half of position limit). When |position| ≥ 40, suppress the quote on the accumulating side.

**Parameters (tunable):** `HALF_SPREAD` (default 5), `FV` (default 10000), `SKEW_FACTOR` (default 3), `ONE_SIDED_THRESHOLD` (default 40).

**Validation check:** P&L should grow. Position should oscillate around 0, rarely exceeding ±40 with one-sided quoting active. If position still hits ±80, lower ONE_SIDED_THRESHOLD.

---

### candidate_03_combined — Combined Submission Bot

Both strategies run inside one `Trader.run()`. Products are independent — no cross-product logic. This is the intended submission candidate.

Combines:
- `candidate_01_ipr_directional`: buy max long, hold, never sell
- `candidate_02_aco_fixedfv`: fixed-FV MM with proportional skew and one-sided quoting

Bot file: `rounds/round_1/bots/bruno/canonical/candidate_03_combined.py` (v3)

---

## Rejected Or Deferred Ideas

| Idea | Reason | Evidence Gap Or Risk |
| --- | --- | --- |
| Drift-tracking market maker for IPR | EDA magnitude shows buy-max-long earns ~7,200 vs ~1,000–2,000 from MM (4–8x); drift gain requires holding inventory, not trading around it | even if drift is weaker in live round, directional still likely better unless drift ≈ 0 |
| Static fair value for IPR | EDA shows drift of +1,003/day — a static FV is wrong within the first tick | contradicted by core signal |
| Aggressive mean-reversion for ACO | Slow persistent reversion (lag-50 autocorr = 0.717 >> AR(1) prediction) makes timing unreliable; position risk is high without inventory controls | position can accumulate for 100+ ticks before reversion |
| ACO market-making without one-sided quoting | Without it, passive bids/asks keep filling during prolonged deviations, pushing position to limit | lag-50 autocorr = 0.717 confirms deviations can last 100+ ticks |
| Manual challenge as algorithmic strategy | Requires human submission via platform UI, not bot code | not executable by `Trader.run()` |

## Shortlist

- **candidate_03_combined** — primary submission candidate (packages 01 + 02).
- Implement and validate 01 and 02 individually first, then combine.

Rationale: both products have strong EDA evidence. Implementation cost is low. Validating separately isolates bugs before combining.

## Human Decisions Needed

- **Shortlist review:** Approve candidates 01, 02, and 03; approve with caveats; or request changes.
- **ONE_SIDED_THRESHOLD parameter:** default 40 (half of position limit). May need tuning based on live inventory behavior.
- **Manual challenge:** Recommended bids — DRYLAND_FLAX ≤ 29, EMBER_MUSHROOM ≤ 19.80. Human platform action.

## Next Action

- Human reviews shortlist. If approved, upload `candidate_03_combined.py` (v3) to platform and run. Compare P&L to baseline 9,419.

