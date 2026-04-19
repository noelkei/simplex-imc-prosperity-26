# Round 2 - Ingestion

## Status

COMPLETED

## Sources

- Active round wiki: `docs/prosperity_wiki/rounds/round_2.md`
- Raw factual source: `docs/prosperity_wiki_raw/13_round_2.md`
- Shared wiki facts:
  - `docs/prosperity_wiki/api/01_trader_contract.md`
  - `docs/prosperity_wiki/api/02_datamodel_reference.md`
  - `docs/prosperity_wiki/api/03_runtime_and_resources.md`
  - `docs/prosperity_wiki/trading/01_exchange_mechanics.md`
  - `docs/prosperity_wiki/trading/02_orders_and_position_limits.md`
  - `docs/prosperity_wiki/platform/01_submission_flow.md`

## Algorithmic Products

| Product | Symbol | Position Limit | Caveat |
| --- | --- | ---: | --- |
| Ash-Coated Osmium | `ASH_COATED_OSMIUM` | 80 | Same product as Round 1; Round 2 source gives no new fair value or signal. |
| Intarian Pepper Root | `INTARIAN_PEPPER_ROOT` | 80 | Same product as Round 1; Round 2 source gives no new fair value or signal. |

## Manual Products

| Product | Symbol | Manual Mechanics Source | Caveat |
| --- | --- | --- | --- |
| Research pillar | N/A | `docs/prosperity_wiki/rounds/round_2.md` | Manual-only budget allocation; not a `Trader.run()` product. |
| Scale pillar | N/A | `docs/prosperity_wiki/rounds/round_2.md` | Manual-only budget allocation; not a `Trader.run()` product. |
| Speed pillar | N/A | `docs/prosperity_wiki/rounds/round_2.md` | Final multiplier depends on rank versus other players. |

## Round-Specific Facts

- Round name: "Growing Your Outpost".
- Algorithmic challenge: "limited Market Access".
- Manual challenge: "Invest & Expand".
- Qualifier context: Round 2 is the final opportunity before the Phase 2 leaderboard reset to reach a net PnL threshold of `200 000` XIRECs or more.
- Algorithmic products remain `ASH_COATED_OSMIUM` and `INTARIAN_PEPPER_ROOT`.
- Position limit for each algorithmic product is 80.
- Round 2 supports a `Trader.bid()` method for the Market Access Fee.
- Extra market access gives access to 25% more order-book quotes.
- Extra quotes' prices and volumes fit into the distribution of already available quotes.
- The Market Access Fee is paid only if accepted.
- Accepted bids are the top 50% of all participant bids.
- Accepted bids are subtracted from Round 2 profits.
- Rejected bids do not pay the fee and do not receive extra market access.
- The Market Access Fee affects access to extra flow, not simulation dynamics.
- Round 2 testing ignores `bid()` and uses no extra market access.
- Round 2 testing quote flow is 80% of generated quotes and is slightly randomized per submission.
- `bid()` in Rounds 1, 3, 4, and 5 is ignored.
- Manual budget is `50 000` XIRECs allocated across Research, Scale, and Speed.
- Manual PnL is `(Research x Scale x Speed) - Budget_Used`.
- Research uses `200_000 * np.log(1 + x) / np.log(1 + 100)` for percentage allocation `x`.
- Scale is linear from 0 to 7 over 0 to 100 allocation.
- Speed is rank-based across all players from 0.9 for highest Speed investment to 0.1 for lowest Speed investment; equal investments share rank.

## Data Availability

| File | Rows incl. header | Product rows / trades |
| --- | ---: | --- |
| `rounds/round_2/data/raw/prices_round_2_day_-1.csv` | 20,001 | 10,000 `ASH_COATED_OSMIUM`, 10,000 `INTARIAN_PEPPER_ROOT` |
| `rounds/round_2/data/raw/prices_round_2_day_0.csv` | 20,001 | 10,000 `ASH_COATED_OSMIUM`, 10,000 `INTARIAN_PEPPER_ROOT` |
| `rounds/round_2/data/raw/prices_round_2_day_1.csv` | 20,001 | 10,000 `ASH_COATED_OSMIUM`, 10,000 `INTARIAN_PEPPER_ROOT` |
| `rounds/round_2/data/raw/trades_round_2_day_-1.csv` | 791 | 459 `ASH_COATED_OSMIUM`, 331 `INTARIAN_PEPPER_ROOT` |
| `rounds/round_2/data/raw/trades_round_2_day_0.csv` | 804 | 471 `ASH_COATED_OSMIUM`, 332 `INTARIAN_PEPPER_ROOT` |
| `rounds/round_2/data/raw/trades_round_2_day_1.csv` | 799 | 465 `ASH_COATED_OSMIUM`, 333 `INTARIAN_PEPPER_ROOT` |

Prices schema: `day; timestamp; product; bid_price_1..3; bid_volume_1..3; ask_price_1..3; ask_volume_1..3; mid_price; profit_and_loss`

Trades schema: `timestamp; buyer; seller; symbol; currency; price; quantity`

## Source Caveats

- The source references `Wiki_ROUND_2_data.zip`; the zip itself is not stored in the wiki source capture.
- The exact tie behavior at the Market Access Fee cutoff is not specified beyond the median example and top-50% language.
- The source does not specify the final challenge day or final data distribution.
- The source does not specify the exact Round 2 deadline.
- The source does not specify the exact randomization method for the 80% testing quote subset.
- Manual Speed multiplier cannot be known from wiki facts alone because it depends on all players' Speed investments.

## Unknowns That May Affect Downstream Work

| Unknown | Affects | Why It Matters | Next Action |
| --- | --- | --- | --- |
| Round 2 final deadline | Planning / phase mode | Determines whether standard or fast mode is appropriate. | Clarify from platform / team. |
| Expected incremental PnL from extra market access | MAF bid / final PnL | Bid should be below the value of accepted extra flow. | Targeted EDA and platform/log experiments; keep as assumption until tested. |
| Competitive bid distribution | MAF bid | Acceptance depends on other participants' bids. | Human strategy decision; scenario analysis only. |
| Manual Speed rank outcome | Manual allocation | Final Speed multiplier depends on other players. | Scenario analysis across plausible Speed rank outcomes. |
| Whether Round 1 champion remains robust on Round 2 data | Strategy / implementation | Products are same but market is stated as more dynamic. | Compare Round 1 strategy assumptions against Round 2 sample data. |
| Effect of randomized 80% testing quotes on platform result variance | Validation | Testing output may vary per submission. | Track repeated run variance only if ROI justifies it; do not over-optimize resubmissions. |

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

- EDA: compare Round 2 sample distributions to Round 1 assumptions; estimate extra-access value; run manual allocation scenario grid.
- Understanding: compress Round 2 changes into actionable assumptions for algorithm, MAF, and manual challenge.
- Strategy: decide whether to carry over Round 1 champion, modify for Round 2 data, and choose a MAF bid range.
- Implementation: add or verify `Trader.bid()` only after a reviewed strategy spec exists.

## Review

- Reviewer: Human
- Review outcome: approved with caveats
- Status: COMPLETED

Caveats:

- Exact Round 2 deadline remains unknown.
- Market Access Fee bid value, manual Speed rank, and extra-access value remain
  downstream strategy/EDA questions rather than ingestion facts.
- Pre-kickoff EDA outputs were found in the EDA workspace and archived as
  historical/unreviewed artifacts before fresh Round 2 EDA begins.
