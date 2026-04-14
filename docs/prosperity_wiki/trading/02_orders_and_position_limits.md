# Orders and Position Limits

Source basis:

- `docs/prosperity_wiki_raw/10_writing_an_algorithm_in_python.md`
- `docs/prosperity_wiki_raw/08_trading_glossary.md`

## `Order` fields

An `Order` has:

- `symbol`: product symbol.
- `price`: maximum buy price for a BUY order, or minimum sell price for a SELL order.
- `quantity`: maximum quantity to buy or sell.

See [../api/02_datamodel_reference.md](../api/02_datamodel_reference.md) for the class reference.

## Quantity signs

In an `Order`:

- positive `quantity` means BUY
- negative `quantity` means SELL

In `OrderDepth`:

- `buy_orders` volumes are positive.
- `sell_orders` volumes are negative.

Example from the source:

- `buy_orders = {9: 5, 10: 4}` means buy quantity 5 at price 9 and buy quantity 4 at price 10.
- `sell_orders = {12: -3, 11: -2}` means sell volume 3 at price 12 and sell volume 2 at price 11.

## Position

- Each trade changes the algorithm's position in that product.
- Buying increases position.
- Selling decreases position.
- A negative position is a short position.

## Absolute position limits

- Position limits are defined per product.
- They refer to absolute allowable position size.
- For a limit of 10, position cannot be greater than 10 or less than -10.
- Per-product limits are listed in the relevant round docs:
  - [../rounds/tutorial.md](../rounds/tutorial.md)
  - [../rounds/round_1.md](../rounds/round_1.md)

## Enforcement and rejection

The exchange enforces position limits.

If, in one iteration, aggregated BUY orders for a product would exceed the long limit if fully executed:

- the exchange rejects the orders automatically.

If aggregated SELL orders for a product would exceed the short limit if fully executed:

- the exchange rejects the orders automatically.

The source also states that if aggregated buy or sell quantity would cause the position limit to be exceeded, all orders are cancelled by the exchange.

## Capacity example from source

If:

- product limit is 30
- current position is `-5`

Then:

- aggregated BUY order volume above `30 - (-5) = 35` would be rejected
- an order with volume 35 is legal
