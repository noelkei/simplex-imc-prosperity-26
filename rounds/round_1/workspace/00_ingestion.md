# Round Ingestion

## Status

READY_FOR_REVIEW

## Sources

- Active round wiki: `docs/prosperity_wiki/rounds/round_1.md`
- Raw factual source: `docs/prosperity_wiki_raw/12_round_1.md`
- Shared wiki facts:
  - `docs/prosperity_wiki/api/01_trader_contract.md`
  - `docs/prosperity_wiki/api/02_datamodel_reference.md`
  - `docs/prosperity_wiki/trading/01_exchange_mechanics.md`
  - `docs/prosperity_wiki/trading/02_orders_and_position_limits.md`

## Algorithmic Products

| Product | Symbol | Position Limit | Caveat |
| --- | --- | ---: | --- |
| Ash-Coated Osmium | `ASH_COATED_OSMIUM` | 80 | Source hints at volatile behavior that "may follow a hidden pattern" — unverified |
| Intarian Pepper Root | `INTARIAN_PEPPER_ROOT` | 80 | Source describes as "quite steady", comparable to `EMERALDS` in Tutorial round |

## Manual Products

| Product | Symbol | Manual Mechanics Source | Caveat |
| --- | --- | --- | --- |
| Dryland Flax | `DRYLAND_FLAX` | `docs/prosperity_wiki/rounds/round_1.md` §Manual-only mechanics | Guaranteed buyback 30/unit, no fee |
| Ember Mushrooms | `EMBER_MUSHROOM` | `docs/prosperity_wiki/rounds/round_1.md` §Manual-only mechanics | Guaranteed buyback 20/unit, fee 0.10/unit traded |

## Round-Specific Facts

- Round name: "Trading groundwork". Challenge name (algorithmic): "First Intarian Goods".
- Round 1 trading days on Intara last 72 hours.
- Manual challenge name: "An Intarian Welcome". Format: Exchange Auction.
- Manual submission: single limit order (price + quantity) per product.
- Auction clearing price logic: (1) maximize total traded volume; (2) ties broken by higher price.
- Execution: all bids >= clearing price execute at clearing price; all asks <= clearing price execute at clearing price.
- Allocation: price priority, then time priority.
- Player submits last — last in queue at any price level joined.
- Guaranteed buybacks: `DRYLAND_FLAX` at 30/unit (no fee); `EMBER_MUSHROOM` at 20/unit (fee 0.10/unit).
- Orders can be resubmitted until round end; last submitted orders are executed.

## Source Caveats

- The "hidden pattern" in `ASH_COATED_OSMIUM` is mentioned as speculation ("rumored", "one may speculate") — not a confirmed mechanic. Do not hardcode any assumed pattern without EDA evidence.
- "Quite steady" for `INTARIAN_PEPPER_ROOT` is qualitative guidance, not a quantified spread or drift bound. Fair value and spread must be estimated from data or treated as an assumption.
- Raw data was added after initial ingestion. Treat derived patterns from that data as EDA evidence, not official round rules.

## Data Availability

- Current raw data: 6 CSV files in `rounds/round_1/data/raw/`:
  - `prices_round_1_day_-2.csv`, `prices_round_1_day_-1.csv`, `prices_round_1_day_0.csv`
  - `trades_round_1_day_-2.csv`, `trades_round_1_day_-1.csv`, `trades_round_1_day_0.csv`
- Missing data: none recorded for the initial EDA scope.
- Last checked: 2026-04-16 during robustness pass.
- EDA artifact using this data: `workspace/01_eda/eda_round_1.md`.

## Unknowns That May Affect Downstream Work

| Unknown | Affects | Why It Matters | Next Action |
| --- | --- | --- | --- |
| Human review of ingestion | Phase closure | Ingestion facts and caveats need sign-off before marking `COMPLETED` | Human review: approve, approve with caveats, or request corrections |
| EDA-derived fair value models | Strategy confidence | Data supports candidate strategies but is not official wiki fact | Keep labeled as EDA evidence; review `01_eda/eda_round_1.md` |
| Manual auction: other participants' bids/asks not known | Manual submission decision | Optimal price/quantity depends on where others bid; player submits last but cannot see others' orders before submitting | Treat as a decision under uncertainty; use guaranteed buyback floors as risk anchors |
| Manual fee impact on `EMBER_MUSHROOM` net P&L | Manual submission decision | 0.10/unit fee reduces effective buyback from 20.00 to 19.90; affects whether buying at certain prices is profitable | Include fee in all manual P&L calculations |
 
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

- EDA: `READY_FOR_REVIEW` — raw data was analyzed in `workspace/01_eda/eda_round_1.md`; human review is pending.
- Understanding: `READY_FOR_REVIEW` — downstream synthesis exists but still inherits ingestion/EDA review debt.
- Strategy: `READY_FOR_REVIEW` — candidates exist but remain pending shortlist approval.
- Implementation: blocked until the canonical bot file exists and validation can run.

## Review

- Reviewer: Unassigned
- Review outcome: not reviewed
- Status: READY_FOR_REVIEW (pending human sign-off; data is now available and EDA exists)
