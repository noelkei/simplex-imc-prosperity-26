# Strategy Candidates

Use [`docs/templates/strategy_candidates_template.md`](../../../docs/templates/strategy_candidates_template.md) as the structure for this file.

Candidate count is ROI-driven, not fixed. Keep every non-duplicative high-ROI
candidate, then use role, priority tier, and implementation wave to manage
focus.

## Status

READY_FOR_REVIEW

## Sources

- Wiki facts: `../../../docs/prosperity_wiki/rounds/round_3.md`, shared API and trading docs
- Understanding summary: [`02_understanding.md`](02_understanding.md)
- External paper research: [`02b_external_paper_research.md`](02b_external_paper_research.md), 8 processed papers in `../research/papers_processed/`
- EDA evidence: [`01_eda/eda_option_surface_and_microstructure.md`](01_eda/eda_option_surface_and_microstructure.md), processed tables under `../data/processed/`
- Post-run research memory: absent for Round 3
- Playbook heuristics: feature-light quoting, inventory-aware skew, validate execution before adding complexity
- Extra reference material: `docs/ML_finance/prosperity4_repo_additions.md` (feature pipeline, inventory control, mean-reversion modules), `docs/slides_options/` (BS/CRR pricing theory, Greeks)

## Paper Intake Pass

| Paper ID | Current-Round Mapping | Strategy Use | Candidate Impact | Note |
| --- | --- | --- | --- | --- |
| `choi_2022_bachelier_guide` | VEX anchor for voucher fair value; extrinsic_dev_day residual frame; short-dated TTE=5d regime | `used` | Directly provides the Bachelier fair-value backbone for C03, C04, C05, C06, C07 | Core pricing kernel for all voucher candidates |
| `stoikov_saglam_2009_option_mm_inventory` | Multi-symbol voucher inventory coupling; per-symbol + family exposure risk | `hybrid` | Creates C04 variant with inventory-aware quote skew on top of C03 | Use simplified linear skew, not full control recursion |
| `muravyev_2015_option_order_flow` | imbalance_1 as modest secondary modifier; family-level flow interpretation | `hybrid` | Supports imbalance confirmation filter in C04; keeps imbalance out of primary role | Interprets imbalance as inventory pressure, not standalone alpha |
| `garcia_ares_2023_expiration_days` | TTE=5d is out-of-sample; near-expiry regime may sharpen or break historical residual behavior | `validation` | Creates C07 cautious variant with tightened thresholds; adds validation posture to all voucher candidates | Risk framing, not a new signal |
| `fengler_2005_surface_smoothing` | Voucher surface is 99.9-100% monotone and convex; structural guardrail for residual logic | `validation` | Adds surface monotonicity/convexity guardrail block to all voucher candidates | Sanity filter, not alpha source |
| `bergault_2022_multi_asset_mm` | Family-level correlated inventory across active vouchers | `inspiration-only` | Inspires escalation path if C04 simple per-symbol skew fails; not first-wave complexity | Too heavy for wave 1; only if simple skew is insufficient |
| `crr_1979_simplified_approach` | Discrete no-arbitrage benchmark for Bachelier fair values | `validation` | Benchmark cross-check for Bachelier-based fair values, especially at extreme strikes | Offline benchmark, not live engine |
| `west_2004_cumulative_normal` | norm_cdf implementation quality for Bachelier pricing | `used` | Implementation requirement for Bachelier-based candidates; robust CDF approximation in spec | Infrastructure, not strategy direction |

Paper import stopped after these 8 because additional papers would not change candidate priority, validation posture, or rejection logic for this round.

## Feature Budget

All serious candidates below follow the feature-light constraint:

- Primary edge: max 1 feature, signal, or fair-value model.
- Supporting logic: max 2 execution filters or risk controls.
- Diagnostics may be included when they do not change trading decisions.

Feature chains for serious candidates:

```text
C01: imbalance_1 + mid reversion -> short-horizon directional lean -> quote skew -> spread capture edge -> fill-aware markout PnL
C02: imbalance_1 + mid reversion -> short-horizon directional lean -> quote skew -> spread capture edge -> fill-aware markout PnL
C03: extrinsic_dev_day around Bachelier fair -> residual mispricing -> quote around fair -> residual reversion edge -> replay residual PnL
C04: extrinsic_dev_day + inventory penalty -> residual + skewed quotes -> position-aware quoting -> reversion + flattening edge -> replay PnL with inventory metrics
C05: extrinsic_dev_day (ITM) -> deep-ITM residual snap-back -> quote around Bachelier fair -> structural anchor edge -> sparse-fill replay PnL
C06: composite C01+C02+C03 per product -> aggregate independent product PnL -> combined Trader -> total round PnL -> per-product attribution replay
C07: extrinsic_dev_day + TTE-adaptive thresholds -> cautious residual entry -> wider entry bands near expiry -> robust edge under regime shift -> compare vs C03 PnL stability
```

## Candidate Count And Roles

7 candidates across 4 product branches plus 2 variants and 1 composite.
All are differentiated, online-usable, testable, and evidence-backed.

- Primary candidates: C03, C06
- Secondary candidates: C01, C02, C04
- Exploratory/validation: C05, C07

## Round Coverage Check

| Item | Source | Candidate Impact | Decision |
| --- | --- | --- | --- |
| TTE=5d live regime (history only covers 6d-8d) | wiki fact + EDA | Affects residual calibration, decay speed, and entry thresholds for all voucher candidates | use as explicit risk; C07 tests cautious posture |
| 10 voucher symbols with independent 300 limit each | wiki fact | Inventory management across correlated products; C04 addresses directly | use in C04 and as spec requirement |
| Integer prices | wiki fact | All fair values must round to int before order placement | use in all candidates |
| No external scientific libraries in bot | wiki fact | Bachelier needs hand-coded norm_cdf (West 2004) | use in spec; West 2004 paper classified `used` |
| VEV_6000/VEV_6500 floor behavior | EDA evidence | Excluded from active trading in all wave 1 candidates | exclude from wave 1 |
| VEV_5400/VEV_5500 wide spreads (900-1859 bps) | EDA evidence | Deprioritized; only passive execution in later variants | defer |
| HYDROGEL_PACK independent from voucher family | EDA evidence (corr 0.006) | Separate product branch (C01) with no cross-product linkage | use as separate branch |
| Voucher surface nearly monotone/convex | EDA evidence | Surface guardrail in all voucher candidates | use as sanity filter |

## Exploration Board

| Idea ID | Product | Source Signal | Primary Feature / Signal | Supporting Features | Process Hypothesis | Online Proxy Needed? | Approach | Expected Edge | Main Risk | Implementation Realism | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B1 | HYDROGEL_PACK | delta_acf_1 reversion + imbalance | mid-price reversion | spread filter, imbalance | noisy delta-1 mean reversion | no | microstructure MM | spread capture from reversion | edge < cost | high | candidate (C01) |
| B2 | VELVETFRUIT_EXTRACT | delta_acf_1 reversion + imbalance | mid-price reversion | spread filter, imbalance | tighter delta-1 anchor with mild reversion | no | microstructure MM + anchor | spread capture + anchoring | modest standalone alpha | high | candidate (C02) |
| B3 | VEV_5000-5300 | extrinsic_dev_day reversion | Bachelier residual | spread filter, surface guardrail | active option regime with tradable residual dynamics | no | Bachelier fair + residual reversion | residual mean-reversion | TTE 5d extrapolation, costs | high | candidate (C03) |
| B4 | VEV_5000-5300 | extrinsic_dev_day + inventory | Bachelier residual + inventory skew | imbalance filter, spread | same as B3 + inventory pressure | no | Bachelier fair + reversion + inventory skew | reversion + better flattening | over-suppression of alpha | medium | candidate (C04) |
| B5 | VEV_4000/4500 | deep-ITM residual snap-back | Bachelier residual (ITM) | spread filter, underlying coupling | ITM dominated by intrinsic with residual snap-back | no | Bachelier fair + ITM residual | structural anchor reversion | sparse trades | medium | candidate (C05) |
| B6 | all active products | composite independent branches | per-product primary features | per-product support | independent product processes | no | combined Trader | aggregate PnL | debugging complexity | high | candidate (C06) |
| B7 | VEV_5000-5300 | extrinsic_dev_day + expiry caution | Bachelier residual + TTE-adaptive thresholds | same as C03 | same as B3 + near-expiry liquidity/flow shift | no | cautious C03 variant | robust edge under TTE shift | undertrade if too cautious | medium | candidate (C07) |

## Per-Product Branches

| Product | Top Branches | Strongest Signal | Weakest Assumption | Pruning Note |
| --- | --- | --- | --- | --- |
| HYDROGEL_PACK | C01 microstructure MM | delta_acf_1 = -0.1292 + imbalance_corr 0.1387 | edge survives 15.7 bps spread cost | standalone; no cross-product dependency |
| VELVETFRUIT_EXTRACT | C02 delta-1 MM + anchor | delta_acf_1 = -0.1585 + imbalance_corr 0.1441 | standalone alpha vs anchor-only role | dual role makes it high-value regardless |
| VEV_5000-VEV_5300 | C03 Bachelier residual, C04 +inventory, C07 +TTE-cautious | extrinsic_dev_day MI 0.3358 + reversion corrs -0.4 to -0.7 | TTE 5d extrapolation from 6d-8d history | highest-ROI option subset; strongest same-time coupling to VEX |
| VEV_4000/VEV_4500 | C05 ITM anchor residual | extrinsic reversion corrs -0.70 | sparse printed trades vs book signals | second wave; strong residual but thin execution |
| VEV_5400/VEV_5500 | deferred | spread-aware execution filter | passive fills may not materialize | too wide spread for wave 1 |
| VEV_6000/VEV_6500 | excluded | none (constant floor) | floor may break live | no evidence for signal; excluded from all waves |

## Combination / Compatibility Matrix

| Pairing | Compatibility | Risk Interaction | Execution Alignment | Cross-Product Dependency | Verdict |
| --- | --- | --- | --- | --- | --- |
| C01 (HYDROGEL) + C02 (VEX) | high | independent (corr 0.006) | independent | none | move forward; combine in C06 |
| C02 (VEX) + C03/C04 (vouchers) | high | VEX anchor feeds voucher fair values | aligned (VEX mid drives voucher pricing) | useful (anchor-option link) | move forward; combine in C06 |
| C01 (HYDROGEL) + C03/C04 (vouchers) | high | independent | independent | none | move forward; combine in C06 |
| C03 (base voucher) + C04 (inventory variant) | mutually exclusive | same product scope | C04 replaces C03 | full overlap | pick one for implementation |
| C03 (base voucher) + C07 (cautious variant) | mutually exclusive | same product scope | C07 replaces C03 | full overlap | validate both; pick one |
| C03/C04 (active vouchers) + C05 (ITM) | high | mildly correlated via VEX anchor | can coexist in same Trader | weak (separate strike regimes) | combine in wave 2 if wave 1 validates |

## Candidate Table

### C01 — Hydrogel Microstructure Market-Maker

| Field | Value |
| --- | --- |
| Candidate ID | `C01` |
| Role | secondary |
| Source Classification | data-driven |
| Product Scope | `HYDROGEL_PACK` |
| Source Of Edge | Short-horizon mean reversion with imbalance-aided quote skew |
| Primary Feature / Signal | Mid-price lag-1 reversion (`delta_acf_1 = -0.1292`) |
| Supporting Features | `imbalance_1` (corr `0.1387` to future delta-5), spread filter (mean rel spread `15.7` bps) |
| Feature Role | primary: direct signal; imbalance: execution filter/directional lean; spread: risk control |
| Linked EDA Signals | hydrogel imbalance-plus-reversion |
| Feature Evidence | `derived_round_3_product_signal_metrics.csv`: delta_acf_1, imbalance_corr, mean_rel_spread |
| External Research Input | none |
| Paper Idea Handling | none |
| Multivariate Evidence | HYDROGEL_PACK independent from VEX (same-time corr 0.006) |
| Supporting Process Hypothesis | noisy delta-1 mean reversion with imbalance sensitivity |
| Redundancy Note | not applicable (single product, no feature overlap) |
| Online Proxy Needed? | no |
| Regime Assumptions | stable delta-1 regime throughout round |
| Understanding Insight | separate hydrogel branch; edge likely but execution-sensitive |
| Key Assumptions | reversion survives cost after spread crossing; imbalance effect is real |
| Main Risk | edge < spread cost (15.7 bps); execution cost eats reversion alpha |
| Why Not Feature Dumping | one primary (reversion) + one filter (imbalance) + one gate (spread); diagnostics only |
| ROI / Pruning Rationale | independent PnL stream; low implementation cost; even modest edge compounds |
| Evidence Strength | medium |
| Implementation Cost | low |
| Validation Speed | high |
| Risk Level | medium |
| Expected Upside | medium |
| Priority Tier | implement-first |
| Implementation Wave | wave 1 |
| Status | draft |

### C02 — Velvetfruit Delta-1 Market-Maker + Voucher Anchor

| Field | Value |
| --- | --- |
| Candidate ID | `C02` |
| Role | secondary |
| Source Classification | data-driven |
| Product Scope | `VELVETFRUIT_EXTRACT` |
| Source Of Edge | Tight-spread delta-1 reversion + imbalance; dual role as voucher pricing anchor |
| Primary Feature / Signal | Mid-price lag-1 reversion (`delta_acf_1 = -0.1585`) |
| Supporting Features | `imbalance_1` (corr `0.1441` to future delta-5), spread filter (mean rel spread `9.5` bps) |
| Feature Role | primary: direct signal; imbalance: execution filter/directional lean; spread: risk control |
| Linked EDA Signals | velvetfruit anchor imbalance-plus-reversion |
| Feature Evidence | `derived_round_3_product_signal_metrics.csv`: delta_acf_1, imbalance_corr, mean_rel_spread |
| External Research Input | none directly; VEX mid used as `S` in Bachelier for voucher candidates |
| Paper Idea Handling | none (delta-1 logic is data-driven; anchoring role is structural) |
| Multivariate Evidence | VEX–voucher same-time coupling is strongest asset of the round (0.75+); VEX–HYDROGEL near-zero |
| Supporting Process Hypothesis | tighter delta-1 anchor with mild reversion and modest imbalance signal |
| Redundancy Note | not applicable (single product) |
| Online Proxy Needed? | no |
| Regime Assumptions | VEX remains stable and tradable throughout the round |
| Understanding Insight | VEX is anchor not just delta-1; tightest spread in the round |
| Key Assumptions | standalone alpha exists beyond anchor role; spread capture is positive net of cost |
| Main Risk | standalone directional effect is modest; main value may be anchoring only |
| Why Not Feature Dumping | one primary (reversion) + one filter (imbalance) + one gate (spread) |
| ROI / Pruning Rationale | high leverage: even if standalone edge is small, anchor role makes VEX quoting essential for voucher strategies |
| Evidence Strength | medium/high |
| Implementation Cost | low |
| Validation Speed | high |
| Risk Level | low |
| Expected Upside | medium |
| Priority Tier | implement-first |
| Implementation Wave | wave 1 |
| Status | draft |

### C03 — Bachelier Residual Reversion (Active Vouchers)

| Field | Value |
| --- | --- |
| Candidate ID | `C03` |
| Role | primary |
| Source Classification | hybrid |
| Product Scope | `VEV_5000`, `VEV_5100`, `VEV_5200`, `VEV_5300` |
| Source Of Edge | Extrinsic-value residual mean reversion around Bachelier-derived fair values |
| Primary Feature / Signal | `extrinsic_dev_day` — deviation of observed extrinsic from day-baseline, measured against Bachelier fair (MI `0.3358`, reversion corrs `-0.40` to `-0.70`) |
| Supporting Features | (1) Spread filter — skip or narrow when rel spread is too wide; (2) Surface monotonicity/convexity guardrail — clamp or require larger edge when cross-strike shape breaks |
| Feature Role | primary: direct signal (residual reversion); spread: risk control; surface check: risk control |
| Linked EDA Signals | intrinsic/extrinsic decomposition, extrinsic residual reversion, surface sanity frame |
| Feature Evidence | `derived_round_3_option_reversion_metrics.csv`, `derived_round_3_option_extrinsic_by_tte.csv`, `derived_round_3_option_surface_summary.csv`, `derived_round_3_option_mutual_information.csv` |
| External Research Input | `choi_2022_bachelier_guide_processed.md` (pricing backbone), `fengler_2005_surface_smoothing_processed.md` (guardrails), `west_2004_cumulative_normal_processed.md` (CDF implementation) |
| Paper Idea Handling | Choi: `used` — provides Bachelier fair-value kernel; Fengler: `validation` — monotonicity/convexity guardrail; West: `used` — robust norm_cdf for implementation |
| Multivariate Evidence | VEX–voucher same-time coupling 0.75+; MI ranks extrinsic_dev_day >> underlying_delta_1; PCA PC1=72% price-anchor redundancy supports choosing one anchor (Bachelier) |
| Supporting Process Hypothesis | active option regime with meaningful extrinsic, same-time underlying coupling, and tradable residual dynamics |
| Redundancy Note | intrinsic_value and mid_price merged into single Bachelier fair anchor (avoids price-anchor feature dumping per PCA evidence) |
| Online Proxy Needed? | no — all features computable from top-of-book and strike metadata |
| Regime Assumptions | residual reversion behavior at TTE=5d is directionally similar to TTE=6d-8d history; surface shape holds |
| Understanding Insight | first-wave option work should focus on residual mispricing, not delayed-follow; VEX anchors valuation |
| Key Assumptions | Bachelier fair with simple vol proxy is a better residual baseline than intrinsic-only; TTE=5d behavior is compatible with historical calibration; VEV_5000-5300 have enough book activity for execution |
| Main Risk | TTE=5d out-of-sample extrapolation; spreads may dominate alpha; vol proxy miscalibration |
| Why Not Feature Dumping | one primary (Bachelier residual), two support filters (spread gate + surface guardrail); all online-computable |
| ROI / Pruning Rationale | highest-evidence candidate; addresses the core round opportunity (option mispricing); paper-validated backbone; strongest EDA signals |
| Evidence Strength | strong |
| Implementation Cost | medium |
| Validation Speed | medium |
| Risk Level | medium |
| Expected Upside | high |
| Priority Tier | spec-first |
| Implementation Wave | wave 1 |
| Status | draft |

### C04 — Bachelier Residual Reversion + Inventory Skew (Active Vouchers)

| Field | Value |
| --- | --- |
| Candidate ID | `C04` |
| Role | secondary |
| Source Classification | hybrid |
| Product Scope | `VEV_5000`, `VEV_5100`, `VEV_5200`, `VEV_5300` |
| Source Of Edge | Same residual reversion as C03 + inventory-aware quote skew across correlated vouchers |
| Primary Feature / Signal | `extrinsic_dev_day` around Bachelier fair (same as C03) |
| Supporting Features | (1) Per-symbol inventory penalty: `penalty_i = a * pos_i / limit_i`; (2) `imbalance_1` confirmation filter: strengthen residual entry when imbalance agrees, soften when it disagrees |
| Feature Role | primary: direct signal (residual); inventory penalty: risk control; imbalance: execution filter |
| Linked EDA Signals | extrinsic residual reversion, multi-symbol inventory coupling, imbalance_1 as modifier |
| Feature Evidence | same as C03 + `derived_round_3_product_signal_metrics.csv` imbalance_corr fields |
| External Research Input | `stoikov_saglam_2009_option_mm_inventory_processed.md` (inventory skew), `muravyev_2015_option_order_flow_processed.md` (imbalance interpretation) |
| Paper Idea Handling | Stoikov-Saglam: `hybrid` — simplified linear inventory skew from full control model; Muravyev: `hybrid` — imbalance-as-confirmation from option order-flow lens |
| Multivariate Evidence | same as C03 + imbalance is PCA PC2 (16.7%), orthogonal to price-anchor family |
| Supporting Process Hypothesis | same active-option regime as C03, plus inventory pressure drives quote degradation when positions concentrate |
| Redundancy Note | imbalance is non-redundant with residual (separate PCA component); inventory skew is a risk overlay not a feature |
| Online Proxy Needed? | no |
| Regime Assumptions | same as C03 + inventory concentration is a real risk in correlated vouchers |
| Understanding Insight | multi-symbol inventory coupling is a key open risk; imbalance is modest directional aid |
| Key Assumptions | simple per-symbol linear skew is sufficient (full matrix coupling deferred); imbalance confirmation improves net fills |
| Main Risk | inventory skew may suppress profitable trades; imbalance may add noise not signal; more complexity than C03 |
| Why Not Feature Dumping | one primary (residual), two supporting (inventory skew + imbalance filter); incremental over C03 with distinct purpose each |
| ROI / Pruning Rationale | targeted variant of C03 addressing its main risk (position concentration); paper-grounded inventory logic |
| Evidence Strength | medium/high |
| Implementation Cost | medium |
| Validation Speed | medium |
| Risk Level | medium |
| Expected Upside | high |
| Priority Tier | validate-next |
| Implementation Wave | wave 1 |
| Status | draft |

### C05 — ITM Structural-Anchor Residual Reversion

| Field | Value |
| --- | --- |
| Candidate ID | `C05` |
| Role | exploratory |
| Source Classification | data-driven |
| Product Scope | `VEV_4000`, `VEV_4500` |
| Source Of Edge | Deep-ITM residual snap-back where extrinsic is near zero but reverts strongly |
| Primary Feature / Signal | `extrinsic_dev_day` around Bachelier fair for ITM strikes (reversion corrs `-0.7023`, `-0.7030`) |
| Supporting Features | (1) Spread filter; (2) Underlying coupling anchor |
| Feature Role | primary: direct signal (ITM residual snap-back); spread: risk control; coupling: validation |
| Linked EDA Signals | ITM residual snap-back, intrinsic/extrinsic decomposition |
| Feature Evidence | `derived_round_3_option_reversion_metrics.csv`, `derived_round_3_option_extrinsic_by_tte.csv` |
| External Research Input | uses same Bachelier backbone as C03 |
| Paper Idea Handling | Choi: `used` (shared backbone); others: none specific to ITM logic |
| Multivariate Evidence | VEX-VEV_4000 same-time coupling strong; ITM extrinsic near zero means residuals are small but sharp |
| Supporting Process Hypothesis | deep ITM call-like instruments dominated by intrinsic value with residual snap-back |
| Redundancy Note | distinct from C03 by strike regime (ITM vs near-ATM) |
| Online Proxy Needed? | no |
| Regime Assumptions | ITM structure holds at TTE=5d; sparse books still offer execution opportunities |
| Understanding Insight | ITM vouchers are useful structural anchors but not first execution focus |
| Key Assumptions | sparse trade prints do not invalidate book-derived signals; ITM residual logic is cleaner than it looks from print count alone |
| Main Risk | sparse printed trades; thin books may not fill passive orders; execution quality unknown |
| Why Not Feature Dumping | one primary (ITM residual), one support (spread gate), one validation (anchor coupling) |
| ROI / Pruning Rationale | differentiated strike regime with strong reversion signal; validates whether ITM is cleaner than near-ATM net of cost |
| Evidence Strength | medium/high |
| Implementation Cost | low (extends C03 logic to different strikes) |
| Validation Speed | low (sparse fills need longer replay) |
| Risk Level | medium/high |
| Expected Upside | medium |
| Priority Tier | backlog |
| Implementation Wave | wave 2 |
| Status | draft |

### C06 — Full-Scope Combined Trader (Delta-1 + Active Vouchers)

| Field | Value |
| --- | --- |
| Candidate ID | `C06` |
| Role | primary |
| Source Classification | hybrid |
| Product Scope | `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, `VEV_5000`, `VEV_5100`, `VEV_5200`, `VEV_5300` |
| Source Of Edge | Aggregate PnL across independent product branches: C01 + C02 + best-of(C03, C04, C07) |
| Primary Feature / Signal | Per-product: mid reversion (delta-1) and Bachelier residual reversion (vouchers) |
| Supporting Features | Per-product spread filters, imbalance filters (optional), surface guardrail (vouchers), inventory skew (if C04 chosen) |
| Feature Role | composite of individual candidate roles |
| Linked EDA Signals | all promoted signals from C01, C02, C03/C04 |
| Feature Evidence | all evidence from component candidates |
| External Research Input | all paper inputs from C03/C04 |
| Paper Idea Handling | composite of component classifications |
| Multivariate Evidence | HYDROGEL independent (corr 0.006); VEX anchors vouchers (corr 0.75+); cross-product risk is additive not interactive |
| Supporting Process Hypothesis | independent product processes aggregate cleanly |
| Redundancy Note | no feature redundancy across branches (different products, different processes) |
| Online Proxy Needed? | no |
| Regime Assumptions | products remain independent in live data as in sample |
| Understanding Insight | Round 3 should be treated as separate hydrogel branch + option family anchored on VEX |
| Key Assumptions | component strategies are individually valid; aggregate Trader does not introduce interaction bugs |
| Main Risk | debugging complexity; one bad branch can drag aggregate PnL; total code size must stay manageable |
| Why Not Feature Dumping | each product branch is individually feature-light; combination is compositional not multiplicative |
| ROI / Pruning Rationale | the submission is one Trader file, so the full-scope bot is the practical implementation target; component validation happens via individual branch logic |
| Evidence Strength | strong (aggregate of strong/medium individual candidates) |
| Implementation Cost | medium/high |
| Validation Speed | medium |
| Risk Level | medium |
| Expected Upside | high |
| Priority Tier | spec-first |
| Implementation Wave | wave 1 |
| Status | draft |

### C07 — TTE-5d Cautious Residual Reversion (Active Vouchers)

| Field | Value |
| --- | --- |
| Candidate ID | `C07` |
| Role | exploratory |
| Source Classification | hybrid |
| Product Scope | `VEV_5000`, `VEV_5100`, `VEV_5200`, `VEV_5300` |
| Source Of Edge | Same residual reversion as C03 with tightened entry thresholds and faster decay for near-expiry regime |
| Primary Feature / Signal | `extrinsic_dev_day` with TTE-adaptive entry/exit thresholds (wider entry, faster exit) |
| Supporting Features | same as C03 (spread filter + surface guardrail) |
| Feature Role | primary: direct signal (residual); spread: risk control; surface: risk control; TTE caution: regime modifier |
| Linked EDA Signals | extrinsic residual reversion, TTE 5d out-of-sample risk |
| Feature Evidence | same as C03 |
| External Research Input | `garcia_ares_2023_expiration_days_processed.md` (near-expiry regime evidence) |
| Paper Idea Handling | Garcia-Ares: `validation` — regime warning that justifies stricter thresholds at TTE=5d |
| Multivariate Evidence | same as C03 |
| Supporting Process Hypothesis | same active-option regime as C03, but live TTE=5d may behave as a flow-driven near-expiry regime |
| Redundancy Note | mutually exclusive with C03; same scope, different calibration |
| Online Proxy Needed? | no |
| Regime Assumptions | TTE=5d is meaningfully different from 6d-8d in residual decay speed and book behavior |
| Understanding Insight | TTE 5d is out-of-sample; do not assume historical half-lives port directly |
| Key Assumptions | wider entry thresholds and faster decay improve robustness even if they reduce raw alpha |
| Main Risk | being too cautious kills the edge entirely; undertrade in a regime where residual alpha actually increases |
| Why Not Feature Dumping | same feature count as C03; difference is calibration, not feature addition |
| ROI / Pruning Rationale | cheap to test alongside C03; directly addresses the round's biggest systematic risk (TTE extrapolation) |
| Evidence Strength | medium |
| Implementation Cost | low (parameter variant of C03) |
| Validation Speed | high |
| Risk Level | low |
| Expected Upside | medium |
| Priority Tier | validate-next |
| Implementation Wave | wave 1 |
| Status | draft |

## Rejected Or Deferred Ideas

| Idea | Source Classification | Paper Idea Handling | Reason | Evidence Gap Or Risk |
| --- | --- | --- | --- | --- |
| Delayed underlying-follow into vouchers | data-driven | none (paper-rejected by negative EDA evidence) | Lag-1+ correlations collapse toward zero; Understanding marks this as strong negative evidence | Using it adds complexity with no sample support |
| Hydrogel-voucher hedge framework | data-driven | none | Same-time return correlation is 0.006; products are independent | No evidence for cross-product hedge value |
| Dynamic alpha in VEV_6000/VEV_6500 | data-driven | none | Constant 0.5 mids, zero variance, 20000 bps spread in sample | Floor may break live, but no evidence to trade on |
| Full Black-Scholes implied-vol stack | paper-rejected | rejected | Bachelier is simpler, sufficient for short-dated single-expiry; BS adds conversion complexity without round-specific benefit | Overkill for Prosperity runtime and discrete ticks |
| Full multi-asset Bergault matrix control | paper-inspired | inspiration-only | Too heavy for first wave; requires covariance estimation and matrix operations in Trader | Escalation path only if C04 simple skew is insufficient |
| VEV_5400/VEV_5500 active trading | data-driven | none | Relative spreads 900-1859 bps; trade alignment skewed heavily to bid side | Only viable as passive-only in later wave with strong execution filters |
| Trade-flow-based features for vouchers | data-driven | none | Too few printed trades in most voucher symbols to build reliable flow signals | May revisit only if live logs provide richer tape |
| PCA-component or cluster-label strategies | data-driven | none | Research-only features without online proxy; PCA is explanatory, not predictive in Trader | No online implementation path |
| Full CRR lattice as live pricing engine | paper-inspired | validation | CRR is useful as offline benchmark, not as live alternative when Bachelier is available | Adds implementation complexity without marginal edge over Bachelier |
| Uncertainty-aware order sizing (Bayesian/GP) | paper-inspired (ML_finance ref) | inspiration-only | Interesting concept from ML_finance docs but requires research-only libraries and offline model calibration | No online proxy; overkill for competition Trader |

## Prioritized Candidate Queue

| Order | Candidate ID | Priority Tier | Implementation Wave | Why This Early / Later | Spec Action |
| --- | --- | --- | --- | --- | --- |
| 1 | `C06` | spec-first | wave 1 | Practical implementation target: one Trader handles all products; subsumes C01+C02+C03 as components; highest aggregate upside | write spec (composite, references component logic) |
| 2 | `C03` | spec-first | wave 1 | Core voucher logic within C06; strongest individual evidence; must be specified first to ground the composite | write spec (component, referenced by C06) |
| 3 | `C01` | implement-first | wave 1 | Simple, independent, low-cost; component of C06; validates delta-1 reversion separately | write spec (component, referenced by C06) |
| 4 | `C02` | implement-first | wave 1 | Dual-role (standalone + anchor); component of C06; essential for voucher pricing | write spec (component, referenced by C06) |
| 5 | `C04` | validate-next | wave 1 | Variant of C03 addressing inventory risk; test if C03 shows position concentration | write spec after C03 validates |
| 6 | `C07` | validate-next | wave 1 | Cheap calibration variant of C03 testing TTE-5d robustness; compare vs C03 PnL stability | write spec as parameter variant of C03 |
| 7 | `C05` | backlog | wave 2 | Differentiated strike regime but sparse execution; only pursue after wave 1 validates and capacity allows | defer spec |

## Decision Trace

| Candidate | Signals Used | Alternatives Rejected Or Deferred | Reason For Priority | Caveat |
| --- | --- | --- | --- | --- |
| `C06` | all promoted signals (reversion, residual, imbalance, surface, anchor coupling) | standalone single-product bots as final submission | one Trader file is the submission unit; aggregate PnL matters; component branches are independently testable within the composite | risk of integration complexity; validate components first |
| `C03` | extrinsic_dev_day, Bachelier fair, surface guardrail, spread filter | delayed-follow (rejected), raw intrinsic residual (weaker baseline), full BS/IV stack (overkill) | strongest evidence with paper-validated backbone; core of the round's option opportunity; MI and reversion metrics are best-in-class | TTE=5d is out-of-sample; vol proxy quality is untested |
| `C01` | delta_acf_1, imbalance_1, spread | hydrogel hedge with vouchers (rejected) | independent product branch; low cost; adds PnL stream without cross-product risk | edge may be < spread cost; medium evidence only |
| `C02` | delta_acf_1, imbalance_1, spread; anchor coupling to vouchers | VEX as anchor-only (too conservative), VEX hedge with HYDROGEL (rejected) | dual role provides value even if standalone alpha is modest; essential for voucher pricing anchor | main standalone risk is modest alpha |
| `C04` | same as C03 + inventory penalty + imbalance confirmation | Bergault full matrix (deferred, too complex), per-symbol-only stops (weaker) | addresses C03's main operational risk (position concentration) with paper-grounded logic | may suppress alpha; more complex than C03 |
| `C07` | same as C03 + TTE-5d regime caution | extrapolating historical thresholds directly (risky), dropping voucher trading entirely near expiry (too drastic) | cheap variant that directly tests the round's biggest systematic risk; Garcia-Ares paper supports caution | may undertrade if TTE=5d is actually friendlier than 6d-8d |
| `C05` | ITM extrinsic_dev_day, strong reversion corrs (-0.70) | skipping ITM entirely (loses some PnL), aggressive ITM sizing (sparse fills make this risky) | differentiated reversion signal in a distinct moneyness regime | sparse execution is a real risk; only wave 2 |

## Exploration Stop Rule

- Stop reason: 7 candidates cover all viable product branches (hydrogel, VEX, active vouchers, ITM vouchers) and all differentiated strategy axes (base, inventory-aware, TTE-cautious). Additional ideas are either duplicate, unsupported, non-online-usable, or would not change the candidate queue.
- Low-ROI branching signal: `duplicate ideas` (VEV_5400/5500 passive-only is a minor variant, not a new direction), `weak evidence` (trade-flow, floor-break speculation), `unimplementable` (PCA/cluster labels, full Bergault matrix), `unlikely to change candidate queue` (more delta-1 variants beyond reversion+imbalance), `implementation/validation bottleneck` (limited time to validate more)
- Ready to write specs: `yes`

## Human Checkpoint

| Decision Needed | Default If No Answer | Options | Why It Matters |
| --- | --- | --- | --- |
| Should we write specs for C06 (composite) + individual components, or start with C03 (voucher-only) first and add delta-1 branches later? | Write C06 spec that references C01/C02/C03 as components; implement as one Trader from the start | (a) composite C06 first, (b) C03-only first then extend | Affects whether the first implementation tests all products or focuses on the highest-edge voucher logic first |
| Should C04 (inventory skew) or C07 (TTE-cautious) be the priority variant to validate against C03? | C04 first (addresses operational risk), C07 second (addresses calibration risk) | (a) C04 first, (b) C07 first, (c) both simultaneously as parameter variants | Determines which risk axis we probe first after the baseline works |

## Next Action

- Write strategy spec for C06 (composite Trader) with C01, C02, C03 as documented component blocks.
- Include Feature Contract and Round-Specific Mechanics Contract per the workflow requirements.
- Then implement, validate, and iterate. C04 and C07 are the priority variants to test once C06 baseline is running.
