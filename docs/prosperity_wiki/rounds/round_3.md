# Round 3 - "Gloves Off"

Source basis: `docs/prosperity_wiki_raw/14_round_3.md`.

## Objective

Create a new Python program that trades `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, and the Round 3 Velvetfruit Extract voucher products.

Also submit two manual bids for Ornamental Bio-Pods. The source states acquired Bio-Pods are sold automatically before the next trading round begins.

The source states Round 3 starts GOAT, all teams begin with zero PnL, and the leaderboard is reset.

## Tradable products

Algorithmic products:

| Product name | Symbol |
| --- | --- |
| Hydrogel Packs | `HYDROGEL_PACK` |
| Velvetfruit Extract | `VELVETFRUIT_EXTRACT` |
| Velvetfruit Extract Voucher (strike 4000) | `VEV_4000` |
| Velvetfruit Extract Voucher (strike 4500) | `VEV_4500` |
| Velvetfruit Extract Voucher (strike 5000) | `VEV_5000` |
| Velvetfruit Extract Voucher (strike 5100) | `VEV_5100` |
| Velvetfruit Extract Voucher (strike 5200) | `VEV_5200` |
| Velvetfruit Extract Voucher (strike 5300) | `VEV_5300` |
| Velvetfruit Extract Voucher (strike 5400) | `VEV_5400` |
| Velvetfruit Extract Voucher (strike 5500) | `VEV_5500` |
| Velvetfruit Extract Voucher (strike 6000) | `VEV_6000` |
| Velvetfruit Extract Voucher (strike 6500) | `VEV_6500` |

Manual challenge product:

| Product name | Symbol |
| --- | --- |
| Ornamental Bio-Pods | not stated in source |

## Position limits

General position-limit mechanics are defined in [../trading/02_orders_and_position_limits.md](../trading/02_orders_and_position_limits.md).

| Product | Limit |
| --- | ---: |
| `HYDROGEL_PACK` | 200 |
| `VELVETFRUIT_EXTRACT` | 200 |
| `VEV_4000` | 300 |
| `VEV_4500` | 300 |
| `VEV_5000` | 300 |
| `VEV_5100` | 300 |
| `VEV_5200` | 300 |
| `VEV_5300` | 300 |
| `VEV_5400` | 300 |
| `VEV_5500` | 300 |
| `VEV_6000` | 300 |
| `VEV_6500` | 300 |

## Product behavior hints

The source states:

- `HYDROGEL_PACK` and `VELVETFRUIT_EXTRACT` are "delta 1" products, similar to the products in the Tutorial round and Rounds 1 and 2.
- The ten `VELVETFRUIT_EXTRACT_VOUCHER` products are options and follow different dynamics.
- All products are traded independently, even though voucher prices may be related to `VELVETFRUIT_EXTRACT` because of the nature of options.
- The voucher symbols are `VEV_4000`, `VEV_4500`, `VEV_5000`, `VEV_5100`, `VEV_5200`, `VEV_5300`, `VEV_5400`, `VEV_5500`, `VEV_6000`, and `VEV_6500`.
- The number in each voucher symbol represents the strike price.
- The vouchers have a 7-day expiration deadline starting from Round 1; time to expiry is 5 days in Round 3.
- The historical data mapping given by the source is: tutorial historical day 0 -> TTE 8d, Round 1 historical day 1 -> TTE 7d, Round 2 historical day 2 -> TTE 6d.

## Algorithmic challenge details

- Challenge name: "Options Require Decisions".
- There are 2 asset classes in the Round 3 algorithmic challenge: delta-1 products and option products.
- The algorithmic challenge products are `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, and the ten voucher symbols listed above.
- The round page refers to the voucher family both generically as `VELVETFRUIT_EXTRACT_VOUCHER` and concretely by the `VEV_*` symbols.
- Solvenarian trading rounds last 48 hours.

## Manual challenge details

- Challenge name: "The Celestial Gardeners' Guild".
- You may submit two bids for Ornamental Bio-Pods.
- Counterparty reserve prices range from 670 to 920.
- The source states the reserve prices are uniformly distributed in increments of 5 between 670 and 920.
- On the next trading day, all acquired Bio-Pods can be sold for 920.
- If the first bid is higher than a counterparty reserve price, the trade occurs at the first bid.
- If the second bid is higher than a counterparty reserve price and higher than the mean of all players' second bids, the trade occurs at the second bid.
- If the second bid is higher than a counterparty reserve price but lower than the mean second bid, the source says the chance of a trade rapidly decreases and PnL is penalized by:

```text
((920 - avg_b2) / (920 - b2))^3
```

## Execution-relevant facts

- The round page instructs participants to create a new Python trading program but does not define a new round-specific `Trader` method. The shared `Trader.run(state)` contract remains defined in [../api/01_trader_contract.md](../api/01_trader_contract.md).
- The Round 3 algorithmic products and limits are listed above.
- The voucher family is time-dependent through time to expiry.
- All Round 3 algorithmic products are traded independently.
- The source states GOAT begins in Round 3 with all teams reset to zero PnL.
- The manual challenge is separate from the Python trading algorithm.

## Manual-only mechanics

- Submit two bids in the Manual Challenge Overview window.
- Participants can resubmit bids until the end of the trading round.
- When the round ends, the last submitted bids are offered to the Celestial Gardeners' Guild.
- Acquired Bio-Pods are automatically converted into profit before the next trading round begins.

## Source caveats

- The source capture comes from a pasted Notion page stored in `docs/prosperity_wiki_raw/14_round_3.md`.
- The source refers to the voucher family both as `VELVETFRUIT_EXTRACT_VOUCHER` and as ten concrete `VEV_*` symbols. The page does not state whether a separate generic voucher symbol appears in data or whether only the listed `VEV_*` symbols are tradable.
- The symbol for Ornamental Bio-Pods is not stated.
- The exact number of Gardeners / counterparties is not stated.
- For the second-bid case below the mean second bid, the source states both that trade chance "rapidly decreases" and that the participant trades at the second bid with a PnL penalty. The exact fill-probability rule is not stated.
- The exact calendar deadline is not stated, only that Solvenarian trading rounds last 48 hours.
