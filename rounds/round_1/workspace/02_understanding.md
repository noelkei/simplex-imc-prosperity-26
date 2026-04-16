# Round 1 — Understanding Summary

## Status

COMPLETED

## Sources

- Wiki facts: `docs/prosperity_wiki/rounds/round_1.md` via `workspace/00_ingestion.md`
- EDA evidence: `workspace/01_eda/eda_round_1.md`
- Playbook heuristics: none applied
- Assumptions: labeled inline

---

## Current Understanding

- **Fact (wiki)**: Two algorithmic products — `INTARIAN_PEPPER_ROOT` (IPR) and `ASH_COATED_OSMIUM` (ACO) — both with position limit +/-80.
- **Fact (wiki)**: IPR described as "quite steady"; ACO described as volatile with possible hidden pattern.
- **Evidence (EDA)**: IPR fair value drifts linearly at exactly +0.001/tick with R2=0.9999 and residual std ~2 units. It is predictably steady, not flat.
- **Evidence (EDA)**: ACO fair value is fixed near 10000. 94.4% of nonzero mid_price within +/-10; trade median = 10000 exactly. No evidence of a hidden pattern in 3 days of data.
- **Hypothesis**: Both products support a market-making strategy quoting around an estimated fair value with a spread buffer.
- **Assumption**: The drift slope of IPR (0.001/tick) and ACO FV (10000) will hold in the actual round. Only 3 historical days observed.

---

## Evidence Synthesis

| Claim Or Observation | Source | Evidence Strength | Decision Impact | What Would Change This |
| --- | --- | --- | --- | --- |
| IPR FV drifts at +0.001/tick | EDA eda_round_1.md | Strong - R2=0.9999, 3 days consistent | High - wrong FV = systematic directional loss | Different slope observed in live round |
| IPR day-start resets to round number | EDA | Strong - 3 days consistent | High - intercept must be re-estimated each day | Day-start not at a round number in live round |
| ACO FV fixed ~10000 | EDA (book + trades) | Strong | High - quoting wrong FV = adverse selection | Sustained deviation from 10000 in live round |
| ACO has hidden pattern | Wiki hint only | Weak - no EDA evidence | Medium | Detect structural move > +/-30 from 10000 |
| Spread IPR ~13, ACO ~16 | EDA | Strong | Medium - sets minimum profitable edge | Structural liquidity change |
| ~12% one-sided book rows | EDA | Strong | Low strategy / High implementation | N/A |
| ~0.3% zero mid_price rows | EDA | Strong | Low strategy / High implementation | N/A |

---

## Strategy-Relevant Insights

| Insight | Linked EDA Signal | Feature Evidence | Regime Assumption | Confidence | Strategy Impact |
| --- | --- | --- | --- | --- | --- |
| IPR has deterministic linear drift FV | FV(t) = day_start + 0.001*t, R2=0.9999 | mid_price, timestamp, per-day linear fit | Slope stable across days; day-start ~ previous close | High | Must update FV every tick; static quote loses money |
| ACO mean-reverts to 10000 with tight range | aco_fv=10000, 94.4% within +/-10 | mid_price (excl zeros), trade price | FV stable across all 3 days | High | Fixed-FV market-making viable; inventory skew helps |
| Spread is quoted, not directional | Lag-1 autocorr = -0.50 for both | mid_price returns | No momentum | High | Market-making appropriate; no evidence for momentum |
| Book gaps require defensive handling | ~12% one-sided, ~0.3% zero mid_price | bid_price_1, ask_price_1, mid_price | Occurs throughout all 3 days | High | Implementation must handle without crashing |

---

## What Should Be Tried

| Candidate Direction | Supporting Insight | Product Scope | Why Try It | Validation Needed |
| --- | --- | --- | --- | --- |
| Market-making around drifting FV for IPR | Linear drift R2=0.9999 | INTARIAN_PEPPER_ROOT | FV predictable; spread capture with minimal adverse selection | Day-start estimation at tick 0; backtest P&L |
| Market-making around fixed FV=10000 for ACO | ACO FV confirmed by book + trades | ASH_COATED_OSMIUM | Mean-reversion strong; spread capture feasible within +/-80 | Monitor early live ticks for FV deviation |
| Combine both products in one bot | Products are independent | Both | One submission required; strategies are independent | No cross-product dependency found; safe to combine |

---

## What Should Not Be Trusted Yet

| Signal Or Claim | Why Not Trusted | Risk If Used | Next Validation |
| --- | --- | --- | --- |
| ACO hidden pattern | No EDA evidence; wiki hint speculative | Miss regime shift; stale FV | Watch for mid_price > +/-30 from 10000 for >50 ticks |
| IPR slope exactly 0.001 in live round | Historical only; 3 days | Systematic drift loss if slope differs | Check first ~100 ticks vs expected FV |
| IPR day-start continues from 13000 | Pattern 10k/11k/12k observed but future unknown | Wrong intercept = adverse selection | Estimate from first valid mid_price; do not hardcode |
| Lag-1 autocorr as directional signal | Bid-ask bounce artifact | Net negative if used | Do not use |

---

## Confidence And Impact

- **Overall confidence**: high
- **Highest-impact implication**: IPR requires per-tick FV update. Static quoting loses ~0.001 * position per tick.
- **Main caveat**: Slope and ACO FV are historical assumptions. Monitor in live round and adapt if early ticks deviate.

---

## Assumptions

1. IPR drift slope ~0.001/tick will hold in live round.
2. IPR day-start estimated from first non-zero mid_price at runtime.
3. ACO FV ~10000 will hold in live round.
4. Products are independent - no cross-product signal.
5. Position limit enforcement: +/-80 absolute; all product orders cancelled if limit breached.

---

## Open Risks And Unknowns

| Risk Or Unknown | Affects | Severity | Mitigation Or Next Action |
| --- | --- | --- | --- |
| IPR slope changes in live round | Spec parameter, P&L | Medium | Hardcode 0.001 initially; optional online adaptation in spec |
| ACO hidden pattern materialises | Strategy FV, P&L | Medium | Monitor early ticks; fall back to observed mid_price if deviation > +/-30 |
| IPR day-start level unknown at tick 0 | Implementation | Medium | Use first valid mid_price as day-start intercept |
| One-sided book rows | Implementation correctness | Low-Medium | Do not quote on missing side; handle in spec and implementation |
| Manual auction products | Manual P&L | Low for bot | Use guaranteed buyback floors as risk anchor |

---

## Prioritized Unknowns

| Unknown | Affects | Priority | Next Action |
| --- | --- | --- | --- |
| IPR day-start estimation at tick 0 | Implementation | High | Define in strategy spec |
| ACO FV monitoring / fallback trigger | Spec risk control | Medium | Define threshold in spec (e.g. > +/-30 for N ticks) |
| Manual auction bid strategy | Manual P&L | Low | Use buyback floor; not blocking bot spec |

---

## Strategy Implications

- **Candidate 1**: IPR linear-drift market maker - quote around FV(t) = day_start + 0.001*t, spread buffer ~3-5 units, position-aware sizing.
- **Candidate 2**: ACO fixed-FV market maker - quote around FV=10000, spread buffer ~8-10 units, inventory skew to manage +/-80 limit.
- **Candidate 3**: Combined bot with both candidates in one Trader.run() - independent per product.
- **Risk constraint**: Both must stay within +/-80. Spread buffer and order sizing must prevent limit violations.
- **Validation implication**: Backtest on historical CSV; check P&L sign and position limit events.

---

## Next Action

Proceed to Fase 03 Strategy Candidates. Both products have strong, implementation-ready signals. No blocking unknowns.

---

## Review

- Reviewer: Unassigned
- Review outcome: approved
- Date: 2026-04-16
