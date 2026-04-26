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
- `../../data/processed/derived_round_4_counterparty_stability_scores.csv`
- `../../data/processed/derived_round_4_counterparty_conditioned_summary.csv`
- `../../data/processed/derived_round_4_counterparty_markout_by_side.csv`
- `../../data/processed/derived_round_4_counterparty_markout_by_symbol_side.csv`
- `../../data/processed/derived_round_4_counterparty_pair_summary.csv`
- `../../data/processed/derived_round_4_counterparty_book_context.csv`
- `../../data/processed/derived_round_4_candidate_online_features.csv`

## Headline Findings

- Counterparty activity is highly concentrated.
- Several names are stable enough across all three days to treat as structural context.
- Specialization is more informative than raw name frequency alone.
- `Mark 01` and `Mark 22` dominate the upper/floor voucher complex in opposite directions.
- `Mark 14` and `Mark 38` repeatedly dominate `HYDROGEL_PACK` and `VEV_4000`.
- `Mark 55`, `Mark 67`, `Mark 49`, and `Mark 01` matter most inside `VELVETFRUIT_EXTRACT`.
- Side-aware markouts matter more than raw trade counts.
- Engineered counterparty-role features are more useful than raw name buckets alone.

## Stable Counterparty Roles

The new stability score compresses the visible names into reusable classes:

- `stable broad`: `Mark 14`, `Mark 01`, `Mark 22`, `Mark 38`
- `stable specialist`: `Mark 55`, `Mark 67`, `Mark 49`
- `mixed / rotating`: none among the names that matter in the current sample
- `small sample`: none among the names that matter in the current sample

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
- Markout note:
  seller-side aligned `5`-step markout is `+20.48` bps overall, which is the strongest large-sample side-aware effect in the file set

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
- Markout note:
  buyer-side aligned markouts stay positive at `1`, `5`, and `10` steps

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

## Markouts By Counterparty And Side

- `Mark 22` as seller is the clearest side-aware contextual signal:
  `+16.70` bps at `1` step and `+20.48` bps at `5` steps, with most activity concentrated in `5200+`.
- `Mark 01` as buyer is much weaker than raw frequency might suggest:
  buyer-aligned markouts are negative at `1` and `5` steps overall because so much of that flow lives in the upper/floor voucher complex.
- `Mark 67` buyer flow in `VEX` is one of the cleanest positive specialist signals:
  `+3.75`, `+3.71`, `+4.27` bps at `1`, `5`, `10` steps.
- `Mark 55` is structurally important in `VEX`, but its side-aware markouts are close to flat; this makes it more useful as state context than as directional flow.
- `Mark 49` is a persistent `VEX` seller, but the sample is smaller and the seller-aligned markouts are negative, so it should stay below first-wave strategy priority.

## Buyer-Seller Pair Ecology

- The largest recurring pair by far is `Mark 01` buyer vs `Mark 22` seller with `1339` trades, mostly in `VEV_6000/6500`, `5400`, and `5500`.
- `Mark 14` buyer vs `Mark 22` seller in `VEV_5200` is much smaller (`83` trades) but much more violent, with very negative raw future returns after prints.
- `Mark 67` buyer vs `Mark 49` seller in `VEX` is a cleaner specialist pair with positive short-horizon follow-through and low spreads.
- Pair structure is real, but pair recurrence should still stay exploratory as a direct feature because the sample is only `3` days and concentration/product role already explains a lot.

## Trade-To-Book Context

- The strong names differ not just by product and side, but by how they print against the book.
- `Mark 22` seller flow is overwhelmingly at or below bid, in wide-spread products, and with poor raw follow-through for buyers.
- `Mark 67` and `Mark 49` in `VEX` print almost entirely at or above ask, but in a very tight-spread environment; that is a different ecology from the upper voucher loop.
- The `trade_location_bucket` feature turns out to be one of the highest-ROI engineered features because it connects counterparty events with microstructure instead of treating names in isolation.

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
- buyer-seller pair recurrence as a direct online trigger

## Downstream Use

- Understanding:
  use this annex to describe the participant ecology of the market.
- Strategy:
  use counterparty names only as context candidates, not as naked directional triggers.
- Spec:
  any name-based feature must declare stability caveats explicitly.
