# Round 4 - "The More The Merrier"

Source basis: `docs/prosperity_wiki_raw/15_round_4.md`.

## Objective

Optimize a Python program to trade `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, and
the Round 4 Velvetfruit Extract voucher products while incorporating newly
available counterparty information into the strategy.

Also submit manual orders for `AETHER_CRYSTAL` and the available option
contracts on that underlying to generate additional profit.

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

Manual challenge products:

| Product name | Symbol |
| --- | --- |
| Aether Crystal | `AETHER_CRYSTAL` |
| 2 week vanilla calls and puts | not individually listed in source |
| 3 week vanilla calls and puts | not individually listed in source |
| Chooser option | not individually listed in source |
| Binary put option | not individually listed in source |
| Knock-out put option | not individually listed in source |

## Position limits

General position-limit mechanics are defined in
[../trading/02_orders_and_position_limits.md](../trading/02_orders_and_position_limits.md).

Algorithmic position limits:

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

Manual challenge volume limits:

- The source states participants may buy or sell up to the displayed volume in
  each manual product.
- Product-by-product displayed volumes are not included in the provided source
  text.

## Product behavior hints

The source states:

- The Round 4 algorithmic products are the same as in Round 3.
- Counterparty identities are now available in trade data.
- The disclosed counterparties are named like `"Mark"` followed by a number.
- Historical trade data in the Data Capsule includes these counterparty IDs.
- The round page refers to the voucher family both generically as
  `VELVETFRUIT_EXTRACT_VOUCHER` and concretely by the `VEV_*` symbols.
- All ten voucher products have a time to expiry of 7 Solvenarian days starting
  from day 1.
- The Round 4 example states `VEV_5000` has time to expiry 4 days in Round 4.

## Algorithmic challenge details

- Challenge name: `"Hello, I'm Mark"`.
- The algorithmic products are `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, and the
  ten voucher symbols listed above.
- The `Trade` datamodel fields `buyer` and `seller` now represent participant
  names in this round's historical trade data.
- The round objective explicitly calls out using the newly disclosed
  counterparty information in trading strategy.

## Manual challenge details

- Challenge name: `"Vanilla Just Isn't Exotic Enough"`.
- Manual trading is separate from algorithmic trading activities.
- All manual products are written on `AETHER_CRYSTAL`.
- Participants can trade the underlying, 2 week vanilla options, 3 week vanilla
  options, and several exotics.
- A "week" means 5 trading days.
- The standard trading year for this challenge uses 252 trading days.
- Final score is the average PnL across 100 simulations of the underlying.
- `AETHER_CRYSTAL` is simulated using Geometric Brownian Motion with zero
  risk-neutral drift and fixed annualized volatility of 251%.
- Prices evolve on a discrete grid of 4 steps per trading day.

Exotic payoff descriptions from the provided source:

- Chooser option: expires in 3 weeks; after 2 weeks the buyer chooses whether
  it becomes a call or a put based on whichever would be in the money at that
  time, then it behaves like a standard option for the final week.
- Binary put option: all-or-nothing payoff; if the underlying is below strike
  at expiry, it pays the specified amount, otherwise it expires worthless.
- Knock-out put option: behaves like a regular put unless the underlying ever
  trades below the knockout barrier before expiry; if breached, it immediately
  becomes worthless.

## Execution-relevant facts

- The shared `Trader.run(state)` contract remains defined in
  [../api/01_trader_contract.md](../api/01_trader_contract.md).
- No new round-specific `Trader` method is stated in the provided Round 4
  source.
- The algorithmic products and limits are listed above.
- Counterparty identity fields are a round-specific data change relevant to
  trade analysis and strategy.
- Manual trading products and exotic option mechanics are separate from the
  uploadable Python trading bot.

## Manual-only mechanics

- Submit orders for `AETHER_CRYSTAL` and the corresponding option contracts in
  the Manual Challenge Overview window.
- Participants can resubmit manual orders until the end of the trading round.
- When the round ends, the last submitted manual orders are locked in and
  processed.

## Source caveats

- The shared datamodel reference currently states `buyer` and `seller` are only
  non-empty when the algorithm itself is buyer or seller. Round 4 explicitly
  states participant names are now exposed in these fields, so Round 4 should
  be treated as a round-specific datamodel behavior change.
- The raw source includes a supplementary note that says "Protein Snackpacks" in
  one sentence, while the main Round 4 page consistently names
  `HYDROGEL_PACK`. Treat this as a source inconsistency, not a product change.
- The manual challenge text names product families but does not provide the
  concrete symbols, strikes, barriers, binary payouts, or displayed max volumes
  for the manual products.
- The algorithmic challenge text refers to the voucher family both as
  `VELVETFRUIT_EXTRACT_VOUCHER` and as concrete `VEV_*` symbols. The provided
  text does not state whether any separate generic voucher symbol appears in the
  data.
- The provided text mentions the Data Capsule contains historical performance
  data, but no Round 4 data files are present in the repository yet.
- The exact calendar deadline is not stated in the provided text.
