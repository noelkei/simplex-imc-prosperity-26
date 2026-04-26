# Strategy Spec: Round 3 Final Exploitation Batch Wave 5

## Status

`deferred under deadline`

## Review Status

- Status: `COMPLETED`
- Owner: `amin`
- Reviewer: `Unassigned`
- Reviewed on: `2026-04-26 (deadline deferral)`
- Deadline deferral reason: the user explicitly requested writing the Wave 5
  spec and implementing the full 12-bot batch immediately after the Wave 4
  synthesis, so the spec is being frozen operationally and consumed right away

## Candidate

- Candidate ID: `Wave5-final-exploitation-batch`
- Candidate priority tier: `spec-first`
- Evidence strength: `strong`
- Product scope: `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, `VEV_4000`,
  `VEV_4500`, `VEV_5000`, `VEV_5100`, `VEV_5200`, `VEV_5300`
- Linked candidate file:
  [`../03_next_wave_bot_planning.md`](../03_next_wave_bot_planning.md)

## Review Decision

- `_index.md` spec status: `deferred under deadline`
- Approved for implementation: `deferred under deadline`
- Reviewer decision notes: the user explicitly wants the Wave 5 spec plus
  implementation now, and the `94`-run evidence base is already narrow enough
  that one last exploitation batch can be specified without reopening broad
  exploration
- Required changes before coding: none

## Objective

Implement the last major Round 3 exploitation batch before final winner
selection.

Wave 5 has two responsibilities at once:

1. protect and refine the current clean winner axis around `W4-03/W4-04`,
2. convert the old `>10k` / `~18k` upside into pruned, `VEX`-anchored,
   retention-disciplined descendants instead of reopening the broad toxic
   active basket.

Total batch size: **12**

## Sources

- Wiki facts:
  [`../../../docs/prosperity_wiki/rounds/round_3.md`](../../../docs/prosperity_wiki/rounds/round_3.md)
  plus the shared API and trading docs
- EDA evidence:
  [`../01_eda/eda_option_surface_and_microstructure.md`](../01_eda/eda_option_surface_and_microstructure.md)
- Understanding summary:
  [`../02_understanding.md`](../02_understanding.md)
- Post-run research memory:
  [`../post_run_research_memory.md`](../post_run_research_memory.md)
- Full synthesis:
  [`../06_testing/round_3_full_performance_synthesis.md`](../06_testing/round_3_full_performance_synthesis.md)
- Key full-synthesis artifacts:
  - [`../06_testing/artifacts/full_synthesis/full_wave4_probe_summary.csv`](../06_testing/artifacts/full_synthesis/full_wave4_probe_summary.csv)
  - [`../06_testing/artifacts/full_synthesis/full_wave4_decision_board.csv`](../06_testing/artifacts/full_synthesis/full_wave4_decision_board.csv)
  - [`../06_testing/artifacts/full_synthesis/full_high_peak_gt10k_runs.csv`](../06_testing/artifacts/full_synthesis/full_high_peak_gt10k_runs.csv)
  - [`../06_testing/artifacts/full_synthesis/full_high_peak_gt10k_product_giveback.csv`](../06_testing/artifacts/full_synthesis/full_high_peak_gt10k_product_giveback.csv)
  - [`../06_testing/artifacts/full_synthesis/full_trade_markout_by_product.csv`](../06_testing/artifacts/full_synthesis/full_trade_markout_by_product.csv)
  - [`../06_testing/artifacts/full_synthesis/full_trade_markout_by_run_product.csv`](../06_testing/artifacts/full_synthesis/full_trade_markout_by_run_product.csv)
- Strategy planning:
  [`../03_next_wave_bot_planning.md`](../03_next_wave_bot_planning.md)
- External paper research:
  - [`../../research/papers_processed/choi_2022_bachelier_guide_processed.md`](../../research/papers_processed/choi_2022_bachelier_guide_processed.md)
  - [`../../research/papers_processed/stoikov_saglam_2009_option_mm_inventory_processed.md`](../../research/papers_processed/stoikov_saglam_2009_option_mm_inventory_processed.md)
  - [`../../research/papers_processed/muravyev_2015_option_order_flow_processed.md`](../../research/papers_processed/muravyev_2015_option_order_flow_processed.md)
  - [`../../research/papers_processed/garcia_ares_2023_expiration_days_processed.md`](../../research/papers_processed/garcia_ares_2023_expiration_days_processed.md)

## Selection Trace

- Based on candidate: `03_next_wave_bot_planning.md`
- Signals used:
  - `W4-03 = 1606.305` and `W4-04 = 1604.305` define the best clean family in
    the whole round
  - `W4-01 = W4-02 = W3-15 = 1527.305` confirms the pure Kalman delta-1 base
    as the best fallback benchmark
  - the only `>10k` peaks still belong to legacy broad-active runs, so the
    remaining upside question is one of retention and pruning, not of broad
    re-exploration
  - `VEV_5100`, `VEV_5000`, and `VEV_5200` dominate giveback in giant-peak
    runs, but that does not mean they are useless as information inputs
  - `VEV_5300` remains the least-toxic active strike, yet still subtractive in
    ordinary finalist overlays
- Important new implementation-design fact:
  - the path study shows useful trading windows on the real platform timestamp
    scale of roughly `0..100000`, so older huge values like `720000+` were not
    meaningful active gates
  - Wave 5 must therefore use realistic cutoff windows and hard-flatten times
- Why selected:
  - the clean winner deserves protection slots
  - the `>10k` ceiling deserves direct, controlled descendants
  - toxic strikes deserve one final information-first treatment

## Batch Scope

- Batch size cap: `12`
- Recommended implemented set in this spec: `12`
- Intent: `winner protection / upside distillation / final submission narrowing`

## Strategy Families Covered

| Family | Products | Why Included |
| --- | --- | --- |
| Winner controls | `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, `VEV_4000`, `VEV_4500` | preserve and refine the current best clean family |
| Pure fallback benchmark | `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT` | keep a conservative baseline for final comparison |
| `VEX`-anchored upside-distillation | `VELVETFRUIT_EXTRACT`, selective `VEV_5000/5100/5300` | attack the old `>10k` ceiling without reopening the broad basket |
| Winner-plus-tiny-salvage overlays | champion stack plus tiny active legs | test whether legacy upside can ride on top of the proven base |
| Toxic-strike-as-signal | `VEV_5300` or compact active pair, with `VEV_5100/5200` as filters | test transformed-threshold / veto logic instead of default inventory |

## Round-Specific Mechanics Contract

| Mechanic / Field | Source | Decision | Bot Behavior | Validation Check |
| --- | --- | --- | --- | --- |
| `Trader.run(state)` | wiki API docs | implement | all bots return `result, conversions, traderData` | compile and smoke-check |
| Round 3 product list | round doc | implement | use only official Round 3 symbols | symbols match spec and files |
| Position limits `200` / `300` | round doc | implement | all sizing and working limits remain safely below official caps | aggregate order capacity remains valid |
| Integer prices | exchange docs | implement | all quotes and active prices are rounded to `int` | no float order prices |
| Conversions | round doc | exclude | all Wave 5 bots return `conversions = 0` | constant zero |
| Manual Bio-Pod challenge | round doc | not applicable | excluded from all bot files | no Bio-Pod logic |
| Live `TTE=5d` regime | round doc + live brief | implement | all voucher pricing keeps the live `TTE=5d` framing | no stale `6d-8d` constants |
| Real platform timestamp scale | post-run synthesis | implement | all late cutoffs and hard flattens use real-scale thresholds around `45k-98.5k`, not inert oversized values | bot configs show realistic windows |
| `traderData` persistence | API docs | implement | keep compact state only: anchors, Kalman, short histories, per-symbol entry state, cooldowns | serializable and bounded |

## Feature Contract

| Feature | Role | Product Linkage | Core Parameters | Expected Use |
| --- | --- | --- | --- | --- |
| F01 Kalman delta-1 base | direct signal | independent `HYDRO` + `VEX` | Kalman fair, delta thresholds, inventory skew | base family and fallback benchmark |
| F02 Winner ITM overlay | additive overlay | `VEV_4000/4500` explicitly linked to `VEX` | centered Bachelier residual, smaller sizes, calm-state caps | `W4-03/W4-04` winner path and retention siblings |
| F03 Real-time retention gates | risk control | applies to both delta and voucher legs | realistic `no_new_entry_after`, `hard_flat_after`, max entries, cooldown | protect winner family and salvage branches from late churn |
| F04 Distilled active salvage | direct signal + retention control | `VEV_5000/5100/5300` linked to `VEX` | small limits, short hold, giveback stop, early cutoff | descendants of old `>10k` runs |
| F05 Winner-plus-tiny-overlay | additive upside test | champion base + tiny salvage legs | micro sizing, tiny caps, hard cutoffs | safest test of whether old upside can coexist with the winner |
| F06 Toxic-strike transformed threshold | filter / veto | `VEV_5100/5200` influence `5300` or compact cluster | same-side penalty, opposite-side bonus, veto caps | information-first use of toxic strikes |
| F07 Compact Kalman salvage | direct signal cleaner | `VEX`-anchored compact active pair | Kalman underlying anchor, simple trend gate, toxic veto | one last smoother-enabled salvage slot |

## Feature Exclusions

| Feature | Why Excluded |
| --- | --- |
| Broad `5000/5100/5200/5300` basket reruns | giant peaks but catastrophic retention and poor interpretability |
| Normal direct `5200` active trading | strongest reject-by-default strike in live evidence |
| Standalone ordinary `5300` finalist reruns | already resolved as not good enough for normal finalist slots |
| HMM / hidden-state logic | lower ROI and higher overfit risk than simple observable gates |
| New upper / floor / surface branches | not on the critical path to final winner selection |

## Proposed Bot Set

| Bot ID | Role | Core Idea |
| --- | --- | --- |
| `W5-01` | live control | freeze `W4-03` winner family |
| `W5-02` | winner retention | `W4-03` sibling with realistic late lock, cooldown, and entry caps |
| `W5-03` | winner retention | earlier stop / fewer reentries version of the winner family |
| `W5-04` | fallback benchmark | pure Kalman delta-1 benchmark |
| `W5-05` | upside-distillation | `VEX + {5000,5100,5300}` pruned descendant |
| `W5-06` | upside-distillation | `VEX + {5100,5300}` with TTE-style decay |
| `W5-07` | upside-distillation | one-shot pure active cluster salvage |
| `W5-08` | upside-distillation | `VEX`-anchored `5100/5300` cross-strike salvage |
| `W5-09` | upside-distillation overlay | winner plus tiny `5000/5100/5300` overlay |
| `W5-10` | upside-distillation overlay | winner plus tiny `5100/5300` overlay |
| `W5-11` | toxic-strike signal | trade `5300` while `5100/5200` shape threshold and veto |
| `W5-12` | Kalman salvage | compact `5100/5300` salvage with Kalman anchor and trend gate |

## Implementation Guidance

- Keep the shared-generator pattern so all Wave 5 files stay comparable.
- Reuse the Wave 4 engine only where it still matches the new thesis.
- Extend the engine for:
  - realistic late cutoffs,
  - per-symbol entry caps,
  - cooldowns,
  - watch-only toxic-strike contexts,
  - transformed-threshold adjustments,
  - and compact Kalman-linked salvage gating.
- Do not add any new round mechanic not supported by the wiki.

## Promotion Rules After Wave 5

After Wave 5, the decision should be one of:

1. **final winner now** if no upside-distillation bot beats the `W5-01/02/03`
   winner axis cleanly,
2. **mini runoff** if one or two distilled bots finish clearly above the clean
   finalists while keeping retention under control,
3. **close active-upside exploration** if the old `>10k` logic still cannot be
   converted into a positive, retainable architecture.

## Next Priority Action

Generate the Wave 5 manifest and implement the 12 bots under
`../bots/amin/canonical/`.
