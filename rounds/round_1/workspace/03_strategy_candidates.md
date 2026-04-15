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

| Candidate ID | Product Scope | Source Of Edge | Evidence / Heuristic Basis | Key Assumptions | Main Risk | Evidence Strength | Implementation Cost | Validation Speed | Risk Level | Expected Upside | Priority | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `candidate_01_ipr_drift` | `INTARIAN_PEPPER_ROOT` | Predictable linear drift — fair value is knowable tick-by-tick | EDA: drift +0.001/tick confirmed across 3 days; residual stdev 2.36 vs spread 12–14 | Drift rate ~0.001/tick holds in live round; `day_start_price` observable on first tick | Drift rate wrong or absent in live round | strong | low | high | low | medium | high | draft |
| `candidate_02_aco_fixedfv` | `ASH_COATED_OSMIUM` | Fixed fair value 10,000 with tight market spread | EDA: FV=10,000 confirmed 3 days, stdev 4–5, AR(1) autocorr 0.79, bot spread 16 | FV=10,000 holds in live round; slow reversion continues | Position accumulates before reversion; inventory risk | strong | low | high | low | medium | high | draft |
| `candidate_03_combined` | `INTARIAN_PEPPER_ROOT` + `ASH_COATED_OSMIUM` | Candidates 01 + 02 combined into one submission bot | Derived from candidates 01 and 02 — no new edge, just packaging | Both individual candidates are valid | Either individual strategy fails and drags overall P&L | strong | low | high | low | high | high | draft |

---

## Candidate Detail

### candidate_01_ipr_drift — IPR Drift Market Maker

**Edge:** INTARIAN_PEPPER_ROOT has a known, linear fair value. At any timestamp `t`, `fv = day_start_price + t * 0.001`. Quoting symmetrically around this value captures the bot spread without directional risk.

**Execution sketch:**
1. On first tick, record `day_start_price` = mid price from order book.
2. Each tick: `fv = day_start_price + state.timestamp * 0.001`
3. Place buy order at `fv - HALF_SPREAD` (rounded to int), sell order at `fv + HALF_SPREAD`.
4. Clip order quantities to stay within position limit 80.
5. `HALF_SPREAD` initial target: 4–5 ticks (inside bot spread of 12–14).

**Position management:** If position > +40, reduce ask size. If position < -40, reduce bid size.

**Parameters (tunable):** `HALF_SPREAD` (default 4), `day_start_price` (observed), `drift_rate` (default 0.001).

**Validation check:** P&L should grow roughly linearly. If flat or negative, check day_start_price initialization and drift_rate accuracy.

---

### candidate_02_aco_fixedfv — ACO Fixed-FV Market Maker

**Edge:** ASH_COATED_OSMIUM mean-reverts around a fixed fair value of 10,000. Quoting around 10,000 with a spread tighter than the bot spread (16) captures the bid-ask spread.

**Execution sketch:**
1. Each tick: `fv = 10000` (constant).
2. Place buy order at `fv - HALF_SPREAD`, sell order at `fv + HALF_SPREAD`.
3. Clip quantities to position limit 80.
4. Position skew: if `position > 40`, raise both quotes by 2 ticks. If `position < -40`, lower both by 2 ticks.

**Parameters (tunable):** `HALF_SPREAD` (default 5), `FV` (default 10000), `POS_SKEW_THRESHOLD` (default 40), `SKEW_TICKS` (default 2).

**Validation check:** P&L should grow. Position should oscillate around 0, rarely hitting ±80.

---

### candidate_03_combined — Combined Submission Bot

Both strategies run inside one `Trader.run()`. Products are independent — no cross-product logic. This is the intended submission candidate.

---

## Rejected Or Deferred Ideas

| Idea | Reason |
| --- | --- |
| Trend-following for IPR (buy and hold) | Position limit 80 caps absolute gain; market making captures spread continuously |
| Aggressive mean-reversion for ACO | Slow reversion (autocorr 0.79) makes timing unreliable; market making is safer |
| Static fair value for IPR | EDA shows drift of +1,000/day — a static FV is wrong within the first tick |
| Manual challenge as algorithmic strategy | Requires human submission via platform UI, not bot code |

## Shortlist

- **candidate_03_combined** — primary submission candidate (packages 01 + 02).
- Implement and validate 01 and 02 individually first, then combine.

Rationale: both products have strong EDA evidence. Implementation cost is low. Validating separately isolates bugs before combining.

## Human Decisions Needed

- **Shortlist approval:** Approve candidates 01, 02, and 03? If yes, agent writes full specs next.
- **Manual challenge:** Recommended bids — DRYLAND_FLAX ≤ 29, EMBER_MUSHROOM ≤ 19.80. Human platform action.

## Next Action

- Human approves shortlist → agent writes specs for candidates 01 and 02, then implements candidate 03.
