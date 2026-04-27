# 02b Strategy Handoff

## Purpose

Provide a short paper-driven handoff for `03 Strategy` without requiring a full
re-read of the larger `02b_external_paper_research.md` artifact.

## Use First

These are the first papers `03 Strategy` should actively consume when deciding
candidate directions:

| Paper ID | Why Read First | Best Use |
| --- | --- | --- |
| `doshi_2025_risky_intraday_order_flow` | strongest external basis for unstable-flow defensive gating | `danger-state`, `no-trade`, upper-strike execution filters |
| `vasios_2015_mimicking_non_anonymous` | best direct support for non-anonymous participant flow as contextual state | `counterparty-conditioned context`, `dominance-state` features |
| `cartea_2018_order_book_signals` | strongest lightweight execution overlay | `imbalance gating`, `quote suppression`, `bad-book-state filtering` |
| `kaeck_2019_informed_index_options` | best family / cross-strike flow framing paper | `linked option-book`, `family-level pressure`, strike-role variants |

## Use As Guardrail

These should constrain how we trust signals rather than generate aggressive new
candidates by themselves:

| Paper ID | Guardrail Role |
| --- | --- |
| `bollen_whaley_2004_net_buying_pressure` | residuals can be demand-distorted, especially around active strikes |
| `goncalves_pinto_sala_2025_incremental_option_volume` | flow-heavy stories need incremental-value tests over simple baselines |
| `nimalendran_son_2024_cream_skimming_toxic_flow` | concentrated participant flow can reflect selective liquidity extraction rather than clean alpha |

## Keep In Mental Cache From `round_3`

These are not part of the new raw-derived `round_4` core, but they still have
real value and should be kept available as secondary references:

| Paper ID | Why It Still Matters | Best Use In `03 Strategy` |
| --- | --- | --- |
| `muravyev_2015_option_order_flow` | strongest carry-forward lens for `inventory pressure` vs `information` in option flow | interpreting family-level pressure and counterparty-conditioned inventory stories |
| `stoikov_saglam_2009_option_mm_inventory` | strongest carry-forward lens for short-dated inventory-aware quote tilting | inventory-risk overlays, quote skew, and incomplete-hedge framing |
| `bergault_2022_multi_asset_mm` | best carry-forward reference for family exposure rather than symbol-only exposure | portfolio / family-level exposure controls across `VEV_*` and `VEX` |
| `choi_2022_bachelier_guide` | strongest carry-forward pricing reference for normal-model intuition and simple Greeks | simple pricing backbone, delta/gamma intuition, and spec support |
| `fengler_2005_surface_smoothing` | strongest carry-forward warning against trusting raw noisy surface kinks | surface sanity checks and residual caution |
| `garcia_ares_2023_expiration_days` | strongest carry-forward reminder that TTE `<= 5` behaves differently | near-expiry caution, timing discipline, and horizon-aware validation |

Use these as `secondary support`, not as replacements for current-round EDA or
the top-level nine-paper `round4_raw_derived` core.

## Use For Framing Or Validation Only

These are useful, but they should not become default live-bot logic at the
start of `03 Strategy`:

| Paper ID | Why It Stays Secondary |
| --- | --- |
| `garleanu_pedersen_poteshman_2005_demand_based_option_pricing` | strong theory for family-demand distortion, but best used as framing and candidate-shaping |
| `roos_2026_arbitrage_free_interpolation` | valuable for residual / surface sanity, but mainly as `EDA-follow-up` or validation support |

## Not For Live Logic By Default

- `roos_2026_arbitrage_free_interpolation` full interpolation machinery
- anything from `knowledge_draft/` unless a current-round candidate explicitly
  needs it and current-round evidence supports it
- anything from `manual_reference/` for algorithmic `VEX` / `VEV_*` strategy
- heavy pricing stacks such as full Heston / COS deployment

## Best Candidate Ideas Suggested By Papers

- `counterparty-conditioned danger-state gate` for `VEV_5200+`
- `imbalance / trade-to-book execution overlay` on top of anchor-first logic
- `family-level flow / pressure framing` for linked voucher decisions
- `strike-role-specific quote suppression` instead of broad basket trading

## Best Validation Ideas Suggested By Papers

- require `baseline -> context` model-ladder improvement before trusting
  counterparty-heavy features
- benchmark residual claims against `VEX` anchor and simple local surface state
- validate `danger-state` ideas on post-trade markout and fill quality, not
  only terminal PnL
- keep `counterparty identity` as context unless a cleaner incremental edge
  appears in run evidence

## Recommended Strategy Reading Order

1. `doshi`
2. `vasios`
3. `cartea`
4. `kaeck`
5. `bollen_whaley`
6. `goncalves_pinto_sala`
7. `nimalendran_son`
8. `garleanu`
9. `roos`
10. `muravyev`
11. `stoikov_saglam`
12. `bergault`
13. `choi`
14. `fengler`
15. `garcia_ares`

## Main Anti-Misuse Warnings

- Do not treat any paper as stronger than current-round EDA or understanding.
- Do not promote participant names to naked alpha just because the literature
  says identity can matter in non-anonymous markets.
- Do not let surface/pricing papers outrank stronger `VEX` anchor and
  microstructure evidence.
- Do not reopen broad active voucher baskets because family-flow theory sounds
  elegant.
- Do not let a `round_3` carry-forward reference outrank a contradictory
  `round_4` raw-derived paper or `round_4` EDA finding.

## Next Use

Use this note as the paper bridge when opening `03 Strategy`, and treat
[`02b_external_paper_research.md`](02b_external_paper_research.md) as the
long-form backing artifact.
