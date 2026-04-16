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
| `candidate_01_ipr_directional` | `INTARIAN_PEPPER_ROOT` | Linear drift +~100 ticks/sim-day; holding max long captures full drift gain | `01_eda/eda_round_1.md` — IPR drift fair value | drift +0.001/tick across 3 days; platform run confirmed ~7,286 P&L from holding +80 | drift rate continues in live round | Understanding: IPR drifts predictably; max-long captures drift gain, MM would sell on the way up | Drift holds in live round; position carries over between days | Drift stops or reverses in live round | strong | low | high | medium | high | high | approved by testing |
| `candidate_02_aco_fixedfv` | `ASH_COATED_OSMIUM` | Fixed fair value 10,000 with tight market spread | `01_eda/eda_round_1.md` — ACO fixed fair value | FV=10,000 across 3 days, stdev 4–5, AR(1) autocorr 0.79, bot spread 16 | live level remains around 10,000; slow reversion continues | Understanding: ACO should trade fixed FV with inventory skew | FV=10,000 holds in live round; slow reversion continues | Position accumulates before reversion; inventory risk | strong | low | high | low | medium | high | draft |
| `candidate_03_combined` | `INTARIAN_PEPPER_ROOT` + `ASH_COATED_OSMIUM` | Candidates 01 + 02 combined into one submission bot | linked signals from candidates 01 and 02 | no new feature evidence; packaging of two independent signals | products remain independent enough to run separately in one trader | Understanding: combined independent trader should be tried after individual validation | Both individual candidates are valid | Either individual strategy fails and drags overall P&L | strong | low | high | low | high | high | draft |

---

## Candidate Detail

### candidate_01_ipr_directional — IPR Buy-Max-Long

**Edge:** INTARIAN_PEPPER_ROOT drifts upward ~100 ticks per simulation day. Holding 80 units (position limit) captures drift gain of 80 × 100 ≈ 8,000 — far more than spread income from market-making (~1,000–2,000). Testing confirmed: P&L ~7,286 from holding max long for one simulation day.

**Why not drift-tracking market maker?** Market making requires selling at ask quotes, which reduces the long position on the way up. With a drift this large relative to spread, the lost drift gain from each sell dwarfs the spread captured.

**Execution sketch:**
1. Each tick: compute `capacity = 80 - current_position`.
2. If `capacity > 0`: sweep all ask levels in the book (buy as many as possible, up to capacity).
3. If capacity remains after sweeping: place a resting bid at `best_bid + 1` to attract incoming sellers.
4. Never sell (no ask orders placed).

**Parameters:** None — fully mechanical. Position limit = 80.

**Validation check:** P&L should grow with the drift. Position should reach +80 within the first few ticks and stay there. If position is not reaching +80, the order book has insufficient ask volume early in the day.

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

| Idea | Reason | Evidence Gap Or Risk |
| --- | --- | --- |
| Drift-tracking market maker for IPR | Testing showed buy-max-long earns ~7,286 vs ~1,000–2,000 from MM; drift gain far exceeds spread income | drift must continue in live round |
| Aggressive mean-reversion for ACO | Slow reversion (autocorr 0.79) makes timing unreliable; market making is safer | position can accumulate before reversion |
| Static fair value for IPR | EDA shows drift of +1,000/day — a static FV is wrong within the first tick | contradicted by core signal |
| Manual challenge as algorithmic strategy | Requires human submission via platform UI, not bot code | not executable by `Trader.run()` |

## Shortlist

- **candidate_03_combined** — primary submission candidate (packages 01 + 02).
- Implement and validate 01 and 02 individually first, then combine.

Rationale: both products have strong EDA evidence. Implementation cost is low. Validating separately isolates bugs before combining.

## Human Decisions Needed

- **Shortlist review:** Approve candidates 01, 02, and 03; approve with caveats; or request changes. Specs were already written under deadline deferral, so any shortlist changes must update downstream specs and implementation tracking.
- **Manual challenge:** Recommended bids — DRYLAND_FLAX ≤ 29, EMBER_MUSHROOM ≤ 19.80. Human platform action.

## Next Action

- Human reviews shortlist. If approved or approved with caveats, restore/create the missing canonical `candidate_03_combined.py` from the linked specs before platform validation.
