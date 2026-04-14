# Round 1 - "Trading groundwork"

Source basis: `docs/prosperity_wiki_raw/12_round_1.md`.

## Objective

Translate the first trading strategy into a Python program that trades `ASH_COATED_OSMIUM` and `INTARIAN_PEPPER_ROOT`. Also participate in the Exchange Auction to generate additional profit.

## Tradable products

Algorithmic products:

| Product name | Symbol |
| --- | --- |
| Ash-Coated Osmium | `ASH_COATED_OSMIUM` |
| Intarian Pepper Root | `INTARIAN_PEPPER_ROOT` |

Manual auction products:

| Product name | Symbol |
| --- | --- |
| Dryland Flax | `DRYLAND_FLAX` |
| Ember Mushrooms | `EMBER_MUSHROOM` |

## Position limits

General position-limit mechanics are defined in [../trading/02_orders_and_position_limits.md](../trading/02_orders_and_position_limits.md).

| Product | Limit |
| --- | ---: |
| `ASH_COATED_OSMIUM` | 80 |
| `INTARIAN_PEPPER_ROOT` | 80 |

## Product behavior hints

The source states:

- Similar to the `EMERALDS` products in the Tutorial round, the value of `INTARIAN_PEPPER_ROOT` is quite steady.
- `INTARIAN_PEPPER_ROOT` is a hardy, slow-growing root.
- `ASH_COATED_OSMIUM` is rumored to be more volatile.
- The source says one may speculate that `ASH_COATED_OSMIUM`'s apparent unpredictability may follow a hidden pattern.

## Algorithmic challenge details

- Challenge name: "First Intarian Goods".
- The algorithmic challenge products are `ASH_COATED_OSMIUM` and `INTARIAN_PEPPER_ROOT`.
- Round 1 trading days on Intara last 72 hours according to the round page.

## Manual challenge details

- Challenge name: "An Intarian Welcome".
- Manual challenge format: Exchange Auction.
- Manual products: `DRYLAND_FLAX` and `EMBER_MUSHROOM`.
- You submit your orders last.
- No other bids or asks arrive after your order.
- No volumes change after you place your order.

## Execution-relevant facts

- Products available for the algorithmic challenge: `ASH_COATED_OSMIUM`, `INTARIAN_PEPPER_ROOT`.
- Product limits are listed above.
- Shared trading mechanics are defined in [../trading/01_exchange_mechanics.md](../trading/01_exchange_mechanics.md).
- Round-specific manual submission behavior is listed under Manual-only mechanics.

## Manual-only mechanics

Auction order:

- Submit a single limit order: price and quantity.
- When the auction ends, the exchange selects a single clearing price.

Clearing price selection:

1. Maximize total traded volume.
2. Break ties by choosing the higher price.

Execution:

- All bids with price >= clearing price execute at the clearing price.
- All asks with price <= clearing price execute at the clearing price.
- Allocation is price priority, then time priority.
- Since you submit last, you are last in line at any price level you join.

Guaranteed buyback:

| Product | Buyback |
| --- | --- |
| `DRYLAND_FLAX` | 30 per unit, no fees |
| `EMBER_MUSHROOM` | 20 per unit, fee: 0.10 per unit traded |

Submission:

- Enter orders in the Manual Challenge Overview window and click "Submit".
- You can resubmit new orders until the end of the trading round.
- When the round ends, the last submitted orders are executed.
