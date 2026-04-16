# Round 1 — Ingestion

## Status

COMPLETED

## Sources

- Active round wiki: `docs/prosperity_wiki/rounds/round_1.md`
- Raw source: `docs/prosperity_wiki_raw/12_round_1.md`
- Shared mechanics:
  - `docs/prosperity_wiki/api/01_trader_contract.md`
  - `docs/prosperity_wiki/api/02_datamodel_reference.md`
  - `docs/prosperity_wiki/trading/01_exchange_mechanics.md`
  - `docs/prosperity_wiki/trading/02_orders_and_position_limits.md`

---

## Algorithmic Products

| Product | Symbol | Position Limit |
| --- | --- | ---: |
| Ash-Coated Osmium | `ASH_COATED_OSMIUM` | 80 |
| Intarian Pepper Root | `INTARIAN_PEPPER_ROOT` | 80 |

## Manual Products

| Product | Symbol | Mechanic |
| --- | --- | --- |
| Dryland Flax | `DRYLAND_FLAX` | Exchange Auction — guaranteed buyback 30/unit, no fee |
| Ember Mushrooms | `EMBER_MUSHROOM` | Exchange Auction — guaranteed buyback 20/unit, fee 0.10/unit traded |

---

## Round Facts

- Round name: "Trading groundwork"
- Algorithmic challenge: "First Intarian Goods" — trade `ASH_COATED_OSMIUM` and `INTARIAN_PEPPER_ROOT` algorithmically.
- Manual challenge: "An Intarian Welcome" — Exchange Auction format.
- Trading days: 72 hours on Intara.

## Manual Auction Mechanics

- Submit a single limit order (price + quantity) per product.
- Clearing price maximises total volume; ties broken by higher price.
- All bids >= clearing price execute at clearing price.
- All asks <= clearing price execute at clearing price.
- Price priority, then time priority; player submits last → last in queue at any joined price level.
- Orders can be resubmitted until round end; last submitted set is executed.

## Position Limit Enforcement

- Exchange enforces absolute position limits: `[-80, +80]` for both algorithmic products.
- If aggregated BUY/SELL orders in one iteration would exceed the limit when fully executed, **all orders for that product are cancelled**.
- Net capacity formula: `remaining_buy_capacity = 80 - current_position`, `remaining_sell_capacity = 80 + current_position`.

---

## Product Behavior Hints (wiki-stated, not strategy conclusions)

- `INTARIAN_PEPPER_ROOT`: described as "quite steady", comparable to `EMERALDS` in Tutorial. Value is qualitatively stable.
- `ASH_COATED_OSMIUM`: described as "more volatile"; source speculates it "may follow a hidden pattern" — unverified, requires EDA.

**Caveats:**
- "Quite steady" is qualitative; actual spread, drift, and fair value must come from EDA.
- "Hidden pattern" for ACO is speculative; do not hardcode any assumed pattern without data evidence.

---

## Data Availability

| File | Rows (incl. header) | Products present |
| --- | ---: | --- |
| `prices_round_1_day_-2.csv` | 20,001 | `ASH_COATED_OSMIUM`, `INTARIAN_PEPPER_ROOT` |
| `prices_round_1_day_-1.csv` | 20,001 | `ASH_COATED_OSMIUM`, `INTARIAN_PEPPER_ROOT` |
| `prices_round_1_day_0.csv` | 20,001 | `ASH_COATED_OSMIUM`, `INTARIAN_PEPPER_ROOT` |
| `trades_round_1_day_-2.csv` | 774 | `INTARIAN_PEPPER_ROOT` (and possibly ACO) |
| `trades_round_1_day_-1.csv` | 761 | `INTARIAN_PEPPER_ROOT` (and possibly ACO) |
| `trades_round_1_day_0.csv` | 744 | `INTARIAN_PEPPER_ROOT` (and possibly ACO) |

Prices schema: `day; timestamp; product; bid_price_1..3; bid_volume_1..3; ask_price_1..3; ask_volume_1..3; mid_price; profit_and_loss`  
Trades schema: `timestamp; buyer; seller; symbol; currency; price; quantity`

Missing: no DRYLAND_FLAX or EMBER_MUSHROOM data (manual-only products — expected).

---

## Unknowns Affecting Downstream Work

| Unknown | Affects | Next Action |
| --- | --- | --- |
| Fair value of `INTARIAN_PEPPER_ROOT` | Strategy FV model | EDA: compute mid-price distribution, check for drift |
| Pattern / structure of `ASH_COATED_OSMIUM` price series | Strategy signal | EDA: autocorrelation, regime detection |
| Typical spread width for each product | Order placement | EDA: ask-bid spread distribution |
| Market trade frequency / liquidity | Sizing / aggressiveness | EDA: trades-per-timestamp distribution |
| Other participants' auction bids for manual products | Manual submission | Unknown until round — use guaranteed buyback as risk floor |
| Net P&L impact of EMBER_MUSHROOM fee | Manual submission | Fee = 0.10/unit → effective buyback = 19.90; use in manual P&L calc |

---

## Ingestion Checklist

- [x] Official round wiki link is present.
- [x] Accepted factual sources reviewed.
- [x] Algorithmic products, symbols, and limits are explicit.
- [x] Manual-only mechanics separated from bot scope.
- [x] Round-specific mechanics separated from shared API/trading facts.
- [x] Product behavior hints labeled as qualitative, not strategy conclusions.
- [x] Source caveats recorded.
- [x] Data availability documented with schema.
- [x] Unknowns affecting EDA/strategy/implementation listed with next actions.
- [x] No facts inferred from bots, performances, non-canonical drafts, or memory.

---

## Review

- Reviewer: Unassigned
- Review outcome: approved
- Status: COMPLETED
