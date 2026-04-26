# Round 4 EDA Annex - Counterparty Profiles

## Purpose

This annex deepens the new Round 4 information layer:
named counterparties in `buyer` and `seller`.

Use it together with the canonical EDA when strategy or understanding needs to
know whether a `Mark XX` looks like:

- a stable product specialist,
- a side specialist,
- a timing specialist,
- or mostly noise.

Primary sources:

- `../../data/processed/derived_round_4_counterparty_summary.csv`
- `../../data/processed/derived_round_4_counterparty_product_mix.csv`
- `../../data/processed/derived_round_4_counterparty_time_bucket.csv`
- `../../data/processed/derived_round_4_counterparty_side_asymmetry.csv`
- `../../data/processed/derived_round_4_counterparty_concentration.csv`
- `../../data/processed/derived_round_4_counterparty_stability.csv`
- `../../data/processed/derived_round_4_counterparty_conditioned_summary.csv`

## Headline Findings

- Counterparty activity is highly concentrated.
- Several names are stable enough across all three days to treat as structural context.
- Specialization is more informative than raw name frequency alone.
- `Mark 01` and `Mark 22` dominate the upper/floor voucher complex in opposite directions.
- `Mark 14` and `Mark 38` repeatedly dominate `HYDROGEL_PACK` and `VEV_4000`.
- `Mark 55`, `Mark 67`, `Mark 49`, and `Mark 01` matter most inside `VELVETFRUIT_EXTRACT`.

## Stable Counterparty Roles

### `Mark 01`

- Buy-heavy overall:
  `1599` buys vs `244` sells
- Product specialization:
  upper/floor voucher buyer, plus meaningful `VEX` and `5300` participation
- Cross-day stability:
  buyer-dominant every day, with `6-7` products touched
- Raw interpretation:
  strong candidate for `upper/passive` and `5300` state context

### `Mark 22`

- Sell-heavy overall:
  `1542` sells vs `42` buys
- Product specialization:
  near-deterministic seller in `5200+`, especially `5300`, `5400`, `5500`, `6000`, `6500`
- Cross-day stability:
  seller-dominant every day, very broad product reach, but strongest in upper/floor
- Raw interpretation:
  strongest `danger-state / opposing-liquidity` contextual candidate in the voucher family

### `Mark 14`

- Nearly balanced overall:
  `1127` buys vs `1045` sells
- Product specialization:
  `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, `VEV_4000`, and some `VEV_5200/5300`
- Cross-day stability:
  always large, product mix stable, side flips slightly by day
- Raw interpretation:
  broad core-market participant; useful as structural context, not obviously directional

### `Mark 38`

- Nearly balanced overall:
  `733` buys vs `745` sells
- Product specialization:
  `HYDROGEL_PACK` and `VEV_4000`, with tiny exploratory prints in `4500-5300`
- Cross-day stability:
  stable in hydro + `4000`, with small side changes
- Raw interpretation:
  another core structural participant, especially for hydro and ITM vouchers

### `Mark 55`

- Almost perfectly balanced overall:
  `598` buys vs `600` sells
- Product specialization:
  pure `VELVETFRUIT_EXTRACT`
- Cross-day stability:
  exactly one-product participant in all three days
- Raw interpretation:
  likely `VEX`-specific state context, not general book participant

### `Mark 67`

- Buy-only overall:
  `165` buys, `0` sells
- Product specialization:
  pure `VELVETFRUIT_EXTRACT`
- Cross-day stability:
  one-product participant in all three days
- Raw interpretation:
  strongest raw candidate for a simple `VEX`-buyer context feature

### `Mark 49`

- Sell-heavy overall:
  `17` buys vs `105` sells
- Product specialization:
  mostly `VELVETFRUIT_EXTRACT`
- Cross-day stability:
  small but persistent `VEX` seller
- Raw interpretation:
  secondary `VEX` context name, likely too small for first-wave strategy use

## Concentration Findings By Product

| Product | Buyer structure | Seller structure | Interpretation |
| --- | --- | --- | --- |
| `HYDROGEL_PACK` | top buyer share `0.5039` (`Mark 38`) | top seller share `0.4961` (`Mark 14`) | concentrated but still two-sided |
| `VELVETFRUIT_EXTRACT` | top buyer share `0.4330` (`Mark 55`) | top seller share `0.4345` (`Mark 55`) | richer and less deterministic than upper vouchers |
| `VEV_4000` | top buyer share `0.5249` (`Mark 14`) | top seller share `0.5271` (`Mark 38`) | concentrated ITM micro-ecosystem |
| `VEV_5200` | top buyer share `0.7021` (`Mark 14`) | top seller share `0.9787` (`Mark 22`) | highly asymmetric and concentrated |
| `VEV_5300` | top buyer share `0.8049` (`Mark 01`) | top seller share `0.9939` (`Mark 22`) | special-case active strike, not generic |
| `VEV_5400` | top buyer share `0.9529` (`Mark 01`) | seller top1 `1.0000` (`Mark 22`) | almost deterministic upper loop |
| `VEV_5500` | top buyer share `0.9771` (`Mark 01`) | seller top1 `1.0000` (`Mark 22`) | even more deterministic |
| `VEV_6000/6500` | buyer top1 `1.0000` (`Mark 01`) | seller top1 `1.0000` (`Mark 22`) | floor products, not normal market structure |

## Timing Findings

- Top names are active across `early`, `mid`, and `late` buckets.
- There is no strong raw-data evidence that the main names are only late-session participants.
- This weakens any universal “late-only” claim.
- It does not remove the possibility that late trading is still toxic for specific products or later run behavior.

## Counterparty-Conditioned Follow-Through

The simple aligned-trade summaries show some pockets of future move asymmetry,
but they should stay below promoted-signal level for now:

- `VEX` trades involving `Mark 67` as buyer show positive short-horizon follow-through.
- `VEV_5200+` combinations involving `Mark 22` as dominant seller often align with poor short-horizon trade outcomes.
- These effects are suggestive enough for understanding and strategy framing.
- They are not clean enough yet to become standalone alpha claims.

## Promotion Decision

Promote into `Phase 02 Understanding`:

- top counterparty role map
- symbol-level concentration map
- warning that upper/floor and `5300` are counterparty-structured markets

Keep exploratory only:

- direct counterparty alpha
- pure timing-specialist logic
- small-name (`Mark 49`) specific logic

## Downstream Use

- Understanding:
  use this annex to describe the participant ecology of the market.
- Strategy:
  use counterparty names only as context candidates, not as naked directional triggers.
- Spec:
  any name-based feature must declare stability caveats explicitly.
