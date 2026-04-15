# Round Ingestion

## Status

IN_PROGRESS

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
- No data artifacts are present in `rounds/round_1/data/raw/` as of ingestion. EDA phase is blocked until data is provided.

## Unknowns That May Affect Downstream Work

| Unknown | Affects | Why It Matters | Next Action |
| --- | --- | --- | --- |
| No price/order-book data in `data/raw/` | EDA (blocked), strategy confidence, parameter estimation | Cannot estimate fair value, volatility, or pattern shape without data | Human to commit raw log/price files to `rounds/round_1/data/raw/` |
| Hidden pattern shape for `ASH_COATED_OSMIUM` | Strategy type selection (mean reversion vs. trend vs. pattern exploitation) | Determines whether a parametric model or reactive approach is correct | EDA once data is available; defer strategy choice until pattern is observed |
| Fair value estimate for `INTARIAN_PEPPER_ROOT` | Market-making spread and quoting logic | Stable product market-making requires an anchor fair value | EDA or use mid-price from first available order book snapshot |
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

- EDA: **BLOCKED** — no data in `rounds/round_1/data/raw/`. Once data lands: (1) classify `INTARIAN_PEPPER_ROOT` price stability and estimate fair value range; (2) test for periodicity, trend, or mean-reversion signature in `ASH_COATED_OSMIUM`.
- Understanding: Can begin partial structure from wiki facts alone (product roles, manual mechanics, position limits). Full understanding requires EDA output.
- Strategy: Provisional framing possible without data (see notes below); shortlist requires EDA confirmation.
  - `INTARIAN_PEPPER_ROOT`: market making around a stable fair value — analogous to `EMERALDS` (Tutorial). Low-risk baseline candidate.
  - `ASH_COATED_OSMIUM`: strategy class depends on observed pattern. Candidates: (a) market making with wider spread; (b) mean reversion; (c) pattern/cycle exploitation if periodicity confirmed in EDA.
  - Manual (`DRYLAND_FLAX`, `EMBER_MUSHROOM`): use guaranteed buyback prices as floor. Bid aggressively below buyback net of fees. Treat as bounded-upside separate track.
- Implementation: Blocked behind reviewed strategy spec gate.

## Review

- Reviewer: Unassigned
- Status: READY_FOR_REVIEW (pending human sign-off; blocked on data for EDA downstream)
