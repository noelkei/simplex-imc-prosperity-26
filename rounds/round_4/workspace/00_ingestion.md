# Round Ingestion

## Status

READY_FOR_REVIEW

## Sources

- Active round wiki: [`../../docs/prosperity_wiki/rounds/round_4.md`](../../docs/prosperity_wiki/rounds/round_4.md)
- Raw factual source: [`../../docs/prosperity_wiki_raw/15_round_4.md`](../../docs/prosperity_wiki_raw/15_round_4.md)
- Prior-round carry-forward source:
  - [`../round_3/workspace/06_testing/round_3_closeout_retrospective.md`](../../round_3/workspace/06_testing/round_3_closeout_retrospective.md)
  - [`../round_3/workspace/post_run_research_memory.md`](../../round_3/workspace/post_run_research_memory.md)
- Shared wiki facts:
  - [`../../docs/prosperity_wiki/README.md`](../../docs/prosperity_wiki/README.md)
  - [`../../docs/prosperity_wiki/api/01_trader_contract.md`](../../docs/prosperity_wiki/api/01_trader_contract.md)
  - [`../../docs/prosperity_wiki/api/02_datamodel_reference.md`](../../docs/prosperity_wiki/api/02_datamodel_reference.md)
  - [`../../docs/prosperity_wiki/trading/01_exchange_mechanics.md`](../../docs/prosperity_wiki/trading/01_exchange_mechanics.md)
  - [`../../docs/prosperity_wiki/trading/02_orders_and_position_limits.md`](../../docs/prosperity_wiki/trading/02_orders_and_position_limits.md)

## Available Data Artifacts

Raw data is now present under [`../data/raw/`](../data/raw/):

| Artifact | Rows | Coverage | Notes |
| --- | ---: | --- | --- |
| `prices_round_4_day_1.csv` | 120000 | all 12 algorithmic products, timestamps `0..999900` | 10000 rows per product |
| `prices_round_4_day_2.csv` | 120000 | all 12 algorithmic products, timestamps `0..999900` | 10000 rows per product |
| `prices_round_4_day_3.csv` | 120000 | all 12 algorithmic products, timestamps `0..999900` | 10000 rows per product |
| `trades_round_4_day_1.csv` | 1407 | trade flow across algorithmic products | includes `buyer` / `seller` names |
| `trades_round_4_day_2.csv` | 1333 | trade flow across algorithmic products | includes `buyer` / `seller` names |
| `trades_round_4_day_3.csv` | 1541 | trade flow across algorithmic products | includes `buyer` / `seller` names |

Observed raw schemas:

- `prices_*`: `day`, `timestamp`, `product`, top-3 bid/ask levels, `mid_price`, `profit_and_loss`
- `trades_*`: `timestamp`, `buyer`, `seller`, `symbol`, `currency`, `price`, `quantity`

Observed counterparty evidence from the uploaded trade files:

- Named counterparties are present in `buyer` and `seller`, matching the Round 4 `"Mark XX"` description.
- Trade flow is already visibly concentrated in a small set of counterparties, so counterparty-aware EDA is now actionable.

## Prior-Round Compatibility Gate

- Prior round checked: `round_3`
- Compatibility verdict: `compatible`
- Product overlap: identical algorithmic universe (`HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, `VEV_*`)
- Mechanics overlap: shared core trading problem plus one material Round 4 delta
- Changed field / state: counterparty identity via `Trade.buyer` and `Trade.seller`
- Strategy implication:
  - carry forward validated framing and anti-patterns from `round_3`
  - revalidate all strategy conclusions that may change once counterparty behavior is visible

Compact intake note:

- Carry forward as validated principles:
  - think in `delta-1` versus option-book roles, not one homogeneous basket
  - treat `VEX` as anchor/context candidate, not just another symbol
  - force explicit `aggressive / passive / no-trade` and hold-horizon framing
- Carry forward as untested hypotheses:
  - toxic-strike veto
  - family imbalance
  - regime gating
  - late-session deterioration
- Carry forward as anti-patterns:
  - do not reopen the broad `5000/5100/5200/5300` basket by default
  - do not treat vouchers as independent delta-1 assets
  - do not assume `round_3` winners port unchanged just because products match

## Algorithmic Products

| Product | Symbol | Position Limit | Caveat |
| --- | --- | ---: | --- |
| Hydrogel Packs | `HYDROGEL_PACK` | 200 | None from provided source |
| Velvetfruit Extract | `VELVETFRUIT_EXTRACT` | 200 | None from provided source |
| Velvetfruit Extract Voucher | `VEV_4000` | 300 | Voucher family also referred to generically as `VELVETFRUIT_EXTRACT_VOUCHER` |
| Velvetfruit Extract Voucher | `VEV_4500` | 300 | Voucher family also referred to generically as `VELVETFRUIT_EXTRACT_VOUCHER` |
| Velvetfruit Extract Voucher | `VEV_5000` | 300 | Round 4 example says TTE is 4 days in Round 4 |
| Velvetfruit Extract Voucher | `VEV_5100` | 300 | Voucher TTE tracked by round day |
| Velvetfruit Extract Voucher | `VEV_5200` | 300 | Voucher TTE tracked by round day |
| Velvetfruit Extract Voucher | `VEV_5300` | 300 | Voucher TTE tracked by round day |
| Velvetfruit Extract Voucher | `VEV_5400` | 300 | Voucher TTE tracked by round day |
| Velvetfruit Extract Voucher | `VEV_5500` | 300 | Voucher TTE tracked by round day |
| Velvetfruit Extract Voucher | `VEV_6000` | 300 | Voucher TTE tracked by round day |
| Velvetfruit Extract Voucher | `VEV_6500` | 300 | Voucher TTE tracked by round day |

## Manual Products

| Product | Symbol | Manual Mechanics Source | Caveat |
| --- | --- | --- | --- |
| Aether Crystal | `AETHER_CRYSTAL` | Round 4 manual challenge | Separate from algorithmic bot |
| 2 week vanilla calls and puts | not individually listed | Round 4 manual challenge | Concrete symbols, strikes, and displayed max volumes not provided |
| 3 week vanilla calls and puts | not individually listed | Round 4 manual challenge | Concrete symbols, strikes, and displayed max volumes not provided |
| Chooser option | not individually listed | Round 4 manual challenge | Concrete symbol and strike not provided |
| Binary put option | not individually listed | Round 4 manual challenge | Concrete symbol, strike, and payout not provided |
| Knock-out put option | not individually listed | Round 4 manual challenge | Concrete symbol, strike, and barrier not provided |

## Round-Specific Facts

- Algorithmic challenge name: `"Hello, I'm Mark"`.
- Manual challenge name: `"Vanilla Just Isn't Exotic Enough"`.
- Round 4 algorithmic products are the same as Round 3: `HYDROGEL_PACK`,
  `VELVETFRUIT_EXTRACT`, and ten `VEV_*` option products.
- Counterparty IDs are now available in historical trade data and can be used
  to study participant behavior.
- The disclosed counterparties are described as IDs named `"Mark"` followed by
  a number.
- The `Trade.buyer` and `Trade.seller` fields now represent participant names
  in this round's trade data.
- All voucher products have a TTE of 7 Solvenarian days starting from day 1.
- The supplied example states `VEV_5000` has TTE 4 days in Round 4.
- Manual challenge products are all written on `AETHER_CRYSTAL`.
- Manual scoring is average PnL across 100 simulations.
- Manual underlying simulation uses GBM with zero risk-neutral drift, 251%
  annualized volatility, 252 trading days per year, and 4 steps per trading
  day.

## Round Mechanics Delta

- Active products/limits:
  - Algorithmic scope unchanged from Round 3 products and limits.
  - Manual scope changes to `AETHER_CRYSTAL` and vanilla/exotic options.
- New or changed Trader/API mechanics:
  - No new `Trader` method is stated.
  - Round-specific datamodel behavior change: `Trade.buyer` and
    `Trade.seller` now expose participant names.
- Data/schema changes:
  - Historical trade data now includes counterparty IDs.
  - Raw files are now present for days `1-3`, with separate `prices_*` and `trades_*` CSVs.
- Manual-only mechanics:
  - Separate manual order entry for `AETHER_CRYSTAL` derivatives.
- Prior-round assumptions at risk:
  - Any Round 3 logic that ignored buyer/seller fields should be rechecked.
  - Any prior assumption that historical trade counterparties are unavailable is
    now stale.
  - Any Round 3 carry-forward that depends only on price/book state should be treated as `compatible but revalidatable`, not auto-promoted.

## Source Caveats

- The shared datamodel reference says `buyer` and `seller` are only non-empty
  when the algorithm itself is buyer or seller, but the Round 4 source
  explicitly changes that behavior.
- The raw Round 4 source includes one supplementary-note sentence that says
  "Protein Snackpacks", while the main round page lists `HYDROGEL_PACK`; treat
  that as a source inconsistency, not a product change.
- The manual challenge source does not include concrete option symbols, strikes,
  knockout barriers, binary payouts, or displayed max volumes.
- The exact round deadline is still unknown from the provided source.

## Unknowns That May Affect Downstream Work

| Unknown | Affects | Why It Matters | Next Action |
| --- | --- | --- | --- |
| Exact manual-product symbols, strikes, barriers, payouts, and displayed max volumes | manual strategy | Manual pricing and order selection need concrete contract specs | clarify from platform or accepted round source before manual submission work |
| Exact deadline / remaining time for Round 4 | prioritization | Affects standard vs fast-mode execution and review strictness | clarify from platform or team tracker |
| Behavioral meaning of the observed `Mark XX` clusters by product, side, and time | EDA / strategy | Counterparty-aware alpha depends on whether names map to stable trading styles | start targeted EDA on participant concentration, product preference, and timing |
| Exact scope of non-`SUBMISSION` buyer/seller population in all trade feeds | implementation / validation | We should verify whether named counterparties appear only in market trades or more broadly in practice | confirm from uploaded sample data during EDA and keep bot logic defensive |

Unknowns must stay separate from facts. Each material unknown needs a next action or explicit deadline-risk deferral before ingestion can be `COMPLETED`.

## Ingestion Quality Checklist

- [x] Official round wiki link is present.
- [x] Accepted factual sources were reviewed.
- [x] Algorithmic products, symbols, and limits are explicit or marked unknown.
- [x] Manual-only mechanics are separated from bot requirements.
- [x] Round-specific mechanics are separated from shared API/trading facts.
- [x] Source caveats and conflicts are recorded.
- [x] Available and missing data artifacts are noted.
- [x] Unknowns that may affect EDA, strategy, or implementation are actionable.
- [x] No facts were inferred from bots, performances, memory, or playbook heuristics.

## Downstream Actions

- EDA: ingest the Round 4 Data Capsule as soon as it is available and profile
  counterparty-aware trade patterns for `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`,
  and the `VEV_*` family; begin with participant concentration, product coverage,
  and whether Round 3 carry-forward framing survives once counterparties are visible.
- Understanding: separate hard Round 4 facts from any observed Mark-behavior
  hypotheses derived from data.
- Strategy: revisit Round 3 assumptions and explicitly decide where
  counterparty identity changes signal quality or execution behavior.
- Implementation: treat `buyer`/`seller` handling as a reviewed Round-Specific
  Mechanics Contract item before coding.

## Review

- Reviewer: Unassigned
- Status: not reviewed
