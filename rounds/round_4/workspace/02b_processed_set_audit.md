# Phase 02b Processed Set Audit

## Purpose

Audit the current `round_4` `papers_processed/` set before strategy use.

This audit distinguishes:

- `round4_raw_derived`: summaries that should come from the current local
  `papers_raw -> papers_md -> papers_processed` pipeline
- `round3_carry_forward`: useful prior-round papers reused as references
- `manual_reference`: papers relevant to the manual challenge, not the
  algorithmic voucher/VEX strategy core
- `knowledge_draft`: notes written from general domain knowledge or generic
  references, not anchored to the current local raw set
- `duplicate_or_junk`: files that should not remain in the canonical set

## Current Structural Verdict

- A nine-paper `round4_raw_derived` processed core now exists at the top level
  of `papers_processed/`.
- The previous flat processed set has been normalized into:
  - `papers_processed/carry_forward/`
  - `papers_processed/manual_reference/`
  - `papers_processed/knowledge_draft/`
- The duplicate `glosten_milgrom ... (1)` file has been removed.
- `03 Strategy` can now treat the uploaded raw-paper set as fully represented
  in canonical processed summaries, while still treating the auxiliary buckets
  as lower-priority references.

## File Audit

| Paper ID / File | Current Path | Origin | Type | Recommended Status | Notes |
| --- | --- | --- | --- | --- | --- |
| `bergault_2022_multi_asset_mm_processed.md` | `papers_processed/carry_forward/` | `round_3` | `round3_carry_forward` | keep | Useful family-exposure framing carry-forward |
| `choi_2022_bachelier_guide_processed.md` | `papers_processed/carry_forward/` | `round_3` | `round3_carry_forward` | keep | Useful pricing/Greek carry-forward |
| `fengler_2005_surface_smoothing_processed.md` | `papers_processed/carry_forward/` | `round_3` | `round3_carry_forward` | keep | Useful surface sanity carry-forward |
| `garcia_ares_2023_expiration_days_processed.md` | `papers_processed/carry_forward/` | `round_3` | `round3_carry_forward` | keep | Useful near-expiry carry-forward |
| `muravyev_2015_option_order_flow_processed.md` | `papers_processed/carry_forward/` | `round_3` | `round3_carry_forward` | keep | Useful option-flow carry-forward |
| `stoikov_saglam_2009_option_mm_inventory_processed.md` | `papers_processed/carry_forward/` | `round_3` | `round3_carry_forward` | keep | Useful inventory-risk carry-forward |
| `binary_put_bsm_digital_processed.md` | `papers_processed/manual_reference/` | local note | `manual_reference` | keep | Manual challenge only |
| `reiner_rubinstein_1991_barrier_options_processed.md` | `papers_processed/manual_reference/` | local note | `manual_reference` | keep | Manual challenge only |
| `rubinstein_1991_chooser_options_processed.md` | `papers_processed/manual_reference/` | local note | `manual_reference` | keep | Manual challenge only |
| `avellaneda_stoikov_2008_hft_mm_processed.md` | `papers_processed/knowledge_draft/` | local note | `knowledge_draft` | keep-for-now | Needs caution downgrade later; not raw-derived |
| `carr_madan_1999_fft_options_processed.md` | `papers_processed/knowledge_draft/` | local note | `knowledge_draft` | keep-for-now | Likely `inspiration-only` / low ROI for strategy |
| `easley_ohara_1987_price_trade_size_processed.md` | `papers_processed/knowledge_draft/` | local note | `knowledge_draft` | keep-for-now | Useful but not raw-derived |
| `fang_oosterlee_2008_cos_method_processed.md` | `papers_processed/knowledge_draft/` | local note | `knowledge_draft` | keep-for-now | Likely validation/inspiration only |
| `glosten_milgrom_1985_adverse_selection_processed.md` | `papers_processed/knowledge_draft/` | local note | `knowledge_draft` | keep-for-now | Useful framework note, not canonical raw-derived |
| `heston_1993_stochastic_vol_processed.md` | `papers_processed/knowledge_draft/` | local note | `knowledge_draft` | keep-for-now | Likely `inspiration-only` / caution |
| `glosten_milgrom_1985_adverse_selection_processed (1).md` | removed | duplicate | `duplicate_or_junk` | removed | Duplicate file deleted in Batch 2 |

## Canonical Raw-Derived Core Status

All nine uploaded `round4_raw_derived` papers now have canonical processed
summaries at the top level of `papers_processed/`:

- `doshi_2025_risky_intraday_order_flow_processed.md`
- `kaeck_2019_informed_index_options_processed.md`
- `vasios_2015_mimicking_non_anonymous_processed.md`
- `bollen_whaley_2004_net_buying_pressure_processed.md`
- `cartea_2018_order_book_signals_processed.md`
- `garleanu_pedersen_poteshman_2005_demand_based_option_pricing_processed.md`
- `nimalendran_son_2024_cream_skimming_toxic_flow_processed.md`
- `goncalves_pinto_sala_2025_incremental_option_volume_processed.md`
- `roos_2026_arbitrage_free_interpolation_processed.md`

These should drive `03 Strategy` more than the auxiliary `knowledge_draft`
layer.

## Batch 2 + Batch 3 Outcome

- Structural ambiguity reduced.
- Duplicate removed.
- Processed set now has explicit role buckets.
- A nine-paper canonical `round4_raw_derived` core now exists.
- Auxiliary files are now explicitly marked in-file as `carry-forward reference`,
  `manual challenge reference`, or `knowledge draft`, reducing strategy-time
  ambiguity.
- The next step is to rewrite the main `02b` artifact around the final state,
  then reconcile phase status and hand off cleanly to `03 Strategy`.
