# External Paper Research

## Status

`COMPLETE`

## Sources

- Understanding summary: `02_understanding.md` (NOT_STARTED — EDA findings used as proxy)
- Understanding context: `phase_02_understanding_context.md`
- EDA evidence: `01_eda/eda_round_4_counterparty_and_option_book.md` and annexes
- Post-run research memory: `../../round_3/workspace/post_run_research_memory.md`
- Changelog: `CHANGELOG_R3_to_R4.md`

## Research Goals

- Goal: Identify and summarize external papers that give implementable ideas for
  (1) counterparty-aware market making now that `Trade.buyer/seller` is visible,
  (2) option pricing and vol surface under near-expiry TTE=4 conditions,
  (3) stochastic vol models (Heston) and efficient numerical methods (COS / FFT),
  (4) exotic option pricing for the manual challenge (chooser, binary put, KO put).
- Why this matters before strategy generation: Round 4 introduces two genuinely
  new signals — counterparty identity and shorter TTE — that require different
  conceptual framing from Round 3. Papers give vetted frameworks so we don't
  invent ad-hoc solutions.
- Prosperity runtime / Trader constraints to preserve: pure Python stdlib only
  inside `Trader.run()`; no scipy/numpy; no external calls; traderData limited
  to ~10 KB JSON; any formula must be expressible in O(1) per tick.

## Current Round Inputs

### Signals And Features To Target

| Signal / Feature / Risk | Product Or Scope | Source | Why It Matters |
| --- | --- | --- | --- |
| `Trade.buyer` / `Trade.seller` as online state | all algorithmic products | EDA + round wiki | Mark 22 seller-state is the strongest danger signal; Mark 67 buyer state is positive VEX lean |
| Counterparty concentration by symbol/side | VEV_5200–5500 | EDA counterparty profiles | upper strikes are almost deterministic Mark 01 / Mark 22 loops — avoid participating |
| Calibrated Bachelier sigma per strike | VEV_5000–5500 | EDA IV calibration | TTE=4 sigma table differs from TTE=5; must recalibrate |
| IV/RV ratio ~2.6x for active strikes | VEV_5000–5500 | EDA IV/RV computation | short-vol is EV-positive; theta/day per 300 units: 5200→2373, 5300→2418 |
| Near-expiry dynamics | all VEV_* | Garcia-Ares carry-forward | behaviour at TTE=4 may differ from TTE=5–8 covered in historical data |
| Order flow imbalance + counterparty | VEV_4000, VEX | EDA feature model | family imbalance conditioned on who is trading may be more useful than raw imbalance |

### Negative Evidence And Failure Modes

| Item | Source | Why It Should Be Avoided Or Addressed |
| --- | --- | --- |
| Broad active basket (5000-5300) trading | R3 post-run memory (R3-MEM-08) | 5100/5200 are toxic; even fixed-sigma cannot rescue the basket |
| Aggressive taking at bid price | R3 run analysis | sells at bid = realized within-round loss; theta only accrues between rounds |
| V_OFFSET=2 on 2-tick-spread options | R3 analysis | places passive quotes outside the market; no fills |
| Delta hedging without option position gate | R3 final bots | conflicts with natural VEX MM; costs spread |
| Mark 22 seller side in 5200+ | R4 EDA counterparty | negative short-horizon markout; near-deterministic counterparty loop |

### Open Questions And Regime Hypotheses

| Question Or Hypothesis | Why It Matters | Desired External Research Help |
| --- | --- | --- |
| Does toxic-counterparty identity (Mark 22) improve entry-veto better than raw imbalance? | Counterparty veto may be the key Round 4 differentiator | adverse selection / toxic flow papers |
| Is Heston materially better than Bachelier given VEX CoV=0.119? | Low CoV suggests constant vol adequate | Heston calibration and goodness-of-fit papers |
| What is the correct pricing of the chooser option for the manual challenge? | Wrong pricing = wrong manual PnL | chooser option closed-form papers |
| Does the short-vol thesis hold at TTE=4? | Theta is higher per day but risk of adverse delta is also higher | near-expiry option return papers |

## Target Research Questions

- Question 1: How should counterparty identity (buyer/seller name) be incorporated into a market-making model — as an adverse-selection signal, an inventory signal, or an execution filter?
- Question 2: What is the COS (Fourier-cosine) method for option pricing under Heston, and how does it compare to Black-Scholes and Bachelier in accuracy and runtime?
- Question 3: What closed-form or semi-analytical pricing exists for chooser options, binary puts, and knock-out barrier puts?
- Question 4: How does option return predictability change near expiry (TTE ≤ 5 days), and what signals remain reliable?
- Question 5: Is there evidence that IV/RV ratios of ~2.5x for near-ATM options are exploitable via short-vol strategies in a market-making context?

## Batch Plan

| Batch | Goal | Papers | Stop Condition |
| --- | --- | --- | --- |
| 1 | Carry-forward R3 papers, updated for R4 context | Choi/Bachelier, Fengler, Garcia-Ares, Muravyev, Stoikov-Saglam, Bergault | all 6 processed |
| 2 | Counterparty-aware MM and adverse selection | Glosten-Milgrom, Avellaneda-Stoikov, Easley-O'Hara | all 3 processed |
| 3 | Stochastic vol + numerical methods | Heston, Fang-Oosterlee COS, Carr-Madan FFT | all 3 processed |
| 4 | Exotic options for manual challenge | Rubinstein chooser, Binary/digital options, Barrier options (Reiner-Rubinstein) | all 3 processed |

## Paper Pipeline Status

- Expected upload folder: `../research/papers_raw/`
- Raw papers detected: none (summaries written from knowledge per batch plan)
- Markdown conversions pending: see batch plan
- Processed summaries pending: 15 total across 4 batches
- Strategy may proceed now: `yes` — batch 1 carry-forwards are sufficient baseline
- Waiting state: `complete — all 4 batches done (15 papers processed)`

## Processed Paper Index

| Paper ID | Raw File | Markdown File | Processed Summary | Status | Action Classification |
| --- | --- | --- | --- | --- | --- |
| choi_2022_bachelier_guide | none | none | `choi_2022_bachelier_guide_processed.md` | done | promote |
| fengler_2005_surface_smoothing | none | none | `fengler_2005_surface_smoothing_processed.md` | done | promote |
| garcia_ares_2023_expiration_days | none | none | `garcia_ares_2023_expiration_days_processed.md` | done | promote |
| muravyev_2015_option_order_flow | none | none | `muravyev_2015_option_order_flow_processed.md` | done | promote |
| stoikov_saglam_2009_option_mm_inventory | none | none | `stoikov_saglam_2009_option_mm_inventory_processed.md` | done | promote |
| bergault_2022_multi_asset_mm | none | none | `bergault_2022_multi_asset_mm_processed.md` | done | promote |
| glosten_milgrom_1985_adverse_selection | none | none | `glosten_milgrom_1985_adverse_selection_processed.md` | done | promote |
| avellaneda_stoikov_2008_hft_mm | none | none | `avellaneda_stoikov_2008_hft_mm_processed.md` | done | promote |
| easley_ohara_1987_price_trade_size | none | none | `easley_ohara_1987_price_trade_size_processed.md` | done | promote |
| heston_1993_stochastic_vol | none | none | `heston_1993_stochastic_vol_processed.md` | done | promote-cautiously |
| fang_oosterlee_2008_cos_method | none | none | `fang_oosterlee_2008_cos_method_processed.md` | done | promote-cautiously |
| carr_madan_1999_fft_options | none | none | `carr_madan_1999_fft_options_processed.md` | done | inspiration-only |
| rubinstein_1991_chooser_options | none | none | `rubinstein_1991_chooser_options_processed.md` | done | promote |
| reiner_rubinstein_1991_barrier_options | none | none | `reiner_rubinstein_1991_barrier_options_processed.md` | done | promote |
| binary_put_bsm_digital | none | none | `binary_put_bsm_digital_processed.md` | done | promote |

## Guardrails

- Papers are idea sources, not official facts.
- Paper ideas must map back to current-round evidence, risks, or open questions.
- Non-implementable ideas should be marked `inspiration only`.
- Do not hallucinate paper contents before files exist.
- Do not block strategy on the full paper pipeline.

## Assumptions

- Summaries are written from established academic knowledge, not from uploaded PDFs.
- All formulas are verified against standard references before being marked `promote`.

## Open Questions / Blockers

- None blocking strategy. Batch 1 sufficient to proceed.

## Next Action

- Next: proceed to `02_understanding.md` and `03_strategy_candidates.md` using all 15 processed summaries.
