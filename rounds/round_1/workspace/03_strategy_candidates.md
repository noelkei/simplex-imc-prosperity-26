# Round 1 — Strategy Candidates

## Status

COMPLETED

## Sources

- Wiki facts: `workspace/00_ingestion.md`
- Understanding: `workspace/02_understanding.md`
- EDA evidence: `workspace/01_eda/eda_round_1.md`
- Playbook heuristics: none applied

---

## Candidate Table

| Candidate ID | Product Scope | Source Of Edge | Linked EDA Signals | Feature Evidence | Regime Assumptions | Understanding Insight | Key Assumptions | Main Risk | Evidence Strength | Impl Cost | Validation Speed | Risk Level | Expected Upside | Priority | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `candidate_01_ipr_drift_mm` | `INTARIAN_PEPPER_ROOT` | Drifting fair value + spread capture | IPR drift slope 0.001/tick, R2=0.9999; spread ~13 | `FV(t) = day_start + 0.001*t`; `deviation = mid_price - FV(t)` | Slope stable; day-start estimated from first valid mid_price | Linear drift is deterministic; quoting static price loses money | Slope 0.001 holds in live round; day-start estimable at tick 0 | Day-start estimation fails at tick 0; slope changes in live round | strong | low | high | low | high | **high** | shortlisted |
| `candidate_02_aco_fixed_fv_mm` | `ASH_COATED_OSMIUM` | Fixed fair value + spread capture + inventory skew | ACO FV ~10000 (94.4% within +-10); trade median=10000; spread ~16 | `FV = 10000`; `deviation = mid_price - 10000`; inventory skew signal | FV stable; no regime shift detected in 3 days | Mean-reversion to 10000 is strong; market-making viable | FV 10000 holds in live round; hidden pattern does not activate | Hidden ACO pattern causes sustained FV shift | strong | low | high | low | high | **high** | shortlisted |
| `candidate_03_combined` | Both | Independent combination of candidates 01 + 02 in one bot | All signals from candidates 01 and 02 | Combined feature set from both candidates | Both regime assumptions apply independently | Both products are independent; single submission covers both | Both assumptions from 01 and 02 hold simultaneously | Compounded risk if either product's assumption breaks | strong | low | high | low | high | **high** | shortlisted |

---

## Rejected Or Deferred Ideas

| Idea | Reason | Evidence Gap Or Risk |
| --- | --- | --- |
| Momentum / directional trading | Lag-1 autocorr = -0.50 for both products; purely mechanical bounce | No directional signal in data; would trade noise |
| ACO hidden-pattern exploitation | No EDA evidence across 3 days; wiki hint is speculative | Pattern unobserved; implementing without evidence adds spec complexity and risk |
| Cross-product arbitrage | No cross-product correlation found in EDA | No evidence of linkage between IPR and ACO |

---

## Shortlist

**Shortlisted candidates (max 3):**
1. `candidate_01_ipr_drift_mm` — IPR drift market maker
2. `candidate_02_aco_fixed_fv_mm` — ACO fixed-FV market maker
3. `candidate_03_combined` — both in one submission bot

**Rationale:**
- Candidates 01 and 02 each have strong independent EDA backing (R2=0.9999 and trade-confirmed FV respectively).
- Candidate 03 is the natural production candidate: a single bot covering both products with independent logic. Implementation cost is low since it simply combines 01 and 02.
- Candidates 01 and 02 are also useful as isolated validation targets before combining.
- No other direction has evidence strong enough to shortlist.

**Recommended spec order:** Write spec for `candidate_03_combined` (covers both products). Candidates 01 and 02 specs can be written as sub-sections or standalone references.

---

## Human Decisions Needed

- **Shortlist approval**: Approve this shortlist to proceed to Fase 04 Strategy Specs. If you want to add, remove, or re-prioritize a candidate, request changes before specs are written.
- **Spec order**: Confirm whether to write a single combined spec (candidate 03) or separate specs for 01 and 02 first.

---

## Next Action

Human approves shortlist → write strategy specs (Fase 04).

---

## Review

- Reviewer: Unassigned
- Review outcome: approved
- Date: 2026-04-16
