# Round Ingestion

## Status

READY_FOR_REVIEW

## Sources

- Active round wiki: `../../../docs/prosperity_wiki/rounds/round_3.md`
- Raw factual source: `../../../docs/prosperity_wiki_raw/14_round_3.md`
- Shared wiki facts:
  - `../../../docs/prosperity_wiki/api/01_trader_contract.md`
  - `../../../docs/prosperity_wiki/api/02_datamodel_reference.md`
  - `../../../docs/prosperity_wiki/trading/01_exchange_mechanics.md`
  - `../../../docs/prosperity_wiki/trading/02_orders_and_position_limits.md`

## Algorithmic Products

| Product | Symbol | Position Limit | Caveat |
| --- | --- | ---: | --- |
| Hydrogel Packs | `HYDROGEL_PACK` | 200 | None from the round page. |
| Velvetfruit Extract | `VELVETFRUIT_EXTRACT` | 200 | None from the round page. |
| Velvetfruit Extract Voucher (strike 4000) | `VEV_4000` | 300 | The round page also names the voucher family generically as `VELVETFRUIT_EXTRACT_VOUCHER`. |
| Velvetfruit Extract Voucher (strike 4500) | `VEV_4500` | 300 | The round page also names the voucher family generically as `VELVETFRUIT_EXTRACT_VOUCHER`. |
| Velvetfruit Extract Voucher (strike 5000) | `VEV_5000` | 300 | The round page also names the voucher family generically as `VELVETFRUIT_EXTRACT_VOUCHER`. |
| Velvetfruit Extract Voucher (strike 5100) | `VEV_5100` | 300 | The round page also names the voucher family generically as `VELVETFRUIT_EXTRACT_VOUCHER`. |
| Velvetfruit Extract Voucher (strike 5200) | `VEV_5200` | 300 | The round page also names the voucher family generically as `VELVETFRUIT_EXTRACT_VOUCHER`. |
| Velvetfruit Extract Voucher (strike 5300) | `VEV_5300` | 300 | The round page also names the voucher family generically as `VELVETFRUIT_EXTRACT_VOUCHER`. |
| Velvetfruit Extract Voucher (strike 5400) | `VEV_5400` | 300 | The round page also names the voucher family generically as `VELVETFRUIT_EXTRACT_VOUCHER`. |
| Velvetfruit Extract Voucher (strike 5500) | `VEV_5500` | 300 | The round page also names the voucher family generically as `VELVETFRUIT_EXTRACT_VOUCHER`. |
| Velvetfruit Extract Voucher (strike 6000) | `VEV_6000` | 300 | The round page also names the voucher family generically as `VELVETFRUIT_EXTRACT_VOUCHER`. |
| Velvetfruit Extract Voucher (strike 6500) | `VEV_6500` | 300 | The round page also names the voucher family generically as `VELVETFRUIT_EXTRACT_VOUCHER`. |

## Manual Products

| Product | Symbol | Manual Mechanics Source | Caveat |
| --- | --- | --- | --- |
| Ornamental Bio-Pods | UNKNOWN | `../../../docs/prosperity_wiki/rounds/round_3.md` manual challenge section | Manual-only product; the source does not state a symbol. |

## Round-Specific Facts

- Round 3 starts GOAT; the source states all teams begin with zero PnL and the leaderboard is reset.
- Algorithmic challenge name: "Options Require Decisions".
- Round 3 has two asset classes in the algorithmic challenge: delta-1 products (`HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`) and option products (the ten `VEV_*` voucher symbols).
- The voucher symbol suffix represents strike price.
- The voucher family has a 7-day expiry countdown starting from Round 1; time to expiry is 5 days in Round 3.
- The source maps historical days as tutorial day 0 -> TTE 8d, Round 1 day 1 -> TTE 7d, Round 2 day 2 -> TTE 6d.
- All products are traded independently, even though voucher pricing may relate to `VELVETFRUIT_EXTRACT`.
- Solvenarian trading rounds last 48 hours.
- Manual challenge name: "The Celestial Gardeners' Guild".
- Manual reserve prices range from 670 to 920 in increments of 5.
- Manual acquired Bio-Pods can be sold on the next trading day for 920.

## Round Mechanics Delta

- Active products and limits changed materially versus prior rounds: Round 3 adds `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, and ten voucher symbols with a limit of 300 each; prior-round product names and limits must not carry forward.
- New or changed Trader/API mechanics from the official round page: none explicitly stated. The active coding contract remains the shared `Trader.run(state)` interface; there is no Round-3-specific `bid()` requirement in the round page.
- Downstream working assumption for bot and EDA work: treat `VELVETFRUIT_EXTRACT_VOUCHER` as a family label and the concrete `VEV_*` symbols as the orderable products, because orders are sent per product symbol and the raw Round 3 data enumerates only the concrete voucher symbols.
- New execution-relevant round mechanic: vouchers have strike-specific symbols and an explicit time-to-expiry dimension.
- Manual-only mechanics changed materially from prior rounds: Round 3 manual work is a two-bid reserve-price game with a below-mean second-bid penalty, not an auction or budget-allocation task.
- Prior-round assumptions at risk: assuming only delta-1 products, assuming no expiry dimension, assuming a single generic voucher symbol, or carrying forward Round 2 `bid()` logic into Round 3.

## Source Caveats

- The round page refers to the voucher family both generically as `VELVETFRUIT_EXTRACT_VOUCHER` and concretely by the ten `VEV_*` symbols.
- The round page does not state whether a separate generic voucher symbol appears in the simulator or whether only the listed `VEV_*` symbols are tradable.
- The symbol for Ornamental Bio-Pods is not stated.
- The exact number of Gardeners / counterparties is not stated.
- For the second-bid case below the mean second bid, the source says both that the trade chance rapidly decreases and that the participant trades with a PnL penalty; the exact fill-probability rule is not specified.
- The exact round-end timestamp is not stated in the source; only the 48-hour round duration is stated.

## Data Availability

- Raw files present in `../data/raw/`: `prices_round_3_day_0.csv`, `prices_round_3_day_1.csv`, `prices_round_3_day_2.csv`, `trades_round_3_day_0.csv`, `trades_round_3_day_1.csv`, `trades_round_3_day_2.csv`.
- All six raw CSVs are semicolon-delimited.
- Price-file schema observed from raw data: `day`, `timestamp`, `product`, top-3 bid/ask price and volume levels, `mid_price`, `profit_and_loss`.
- Trade-file schema observed from raw data: `timestamp`, `buyer`, `seller`, `symbol`, `currency`, `price`, `quantity`.
- Each prices file has 120001 lines and covers timestamps `0` through `999900`.
- Trades files have 1309, 1408, and 1334 lines respectively for days 0, 1, and 2, with timestamps spanning almost the full day.
- Data evidence only: each prices file contains all 12 algorithmic symbols; trade files show `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, and voucher trading activity, but not every voucher symbol prints trades on every historical day.
- These raw-data observations are EDA inputs, not official round facts.

## Unknowns That May Affect Downstream Work

| Unknown | Affects | Why It Matters | Next Action |
| --- | --- | --- | --- |
| Whether the live simulator exposes only `VEV_*` symbols or also a separate generic `VELVETFRUIT_EXTRACT_VOUCHER` symbol | EDA / strategy / implementation | Symbol iteration, fair-value mapping, positions, and any strike/TTE lookup need the correct tradable symbol set | Proceed with the working assumption that the concrete `VEV_*` symbols are the tradable bot symbols; revisit only if an official simulator-facing source adds a separate generic symbol |
| Exact execution rule when manual second bid is below `avg_b2` | Manual challenge | The manual bid choice depends on the true fill-probability penalty mechanics | Defer with risk for manual decision-making; do not let this block algorithmic phases |
| Ornamental Bio-Pods symbol | Manual challenge / handoff | Useful for documentation consistency, but not for algorithmic trading work | Defer unless an official manual interface exposes a symbol |
| Exact round-end timestamp | Planning / prioritization | Deadline-aware mode changes at 24h and 6h remaining | Clarify with the human if deadline pressure becomes material; otherwise proceed under `UNKNOWN` deadline |

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

- EDA: validate raw schema assumptions, confirm how the `VEV_*` symbols behave relative to `VELVETFRUIT_EXTRACT`, and separate option-specific from delta-1 signals.
- Understanding: compress which strike/TTE relationships look decision-useful, which cross-product links are weak, and which assumptions remain unresolved.
- Strategy: keep manual challenge logic separate and explore delta-1 and voucher/underlying candidates as distinct strategy families before combining them.
- Implementation: require the later spec to classify voucher symbol handling, expiry/TTE handling, and manual-mechanics exclusions in the Round-Specific Mechanics Contract.

## Review

- Reviewer: Unassigned
- Status: not reviewed
