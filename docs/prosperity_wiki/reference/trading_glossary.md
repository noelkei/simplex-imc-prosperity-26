# Trading Glossary

Source basis: `docs/prosperity_wiki_raw/08_trading_glossary.md`.

## Exchange

A central marketplace where buyers and sellers arrange trades in products.

Prosperity focuses on limit orders sent to Prosperity's own exchange.

## Order

A binding message indicating willingness to buy or sell a quantity of a product.

Common order types in the source:

| Term | Definition |
| --- | --- |
| Market order | Buy or sell immediately at the best available prices in the market. |
| Limit order | Buy or sell at a specified price or better. |
| Stop order | Becomes active only when market price reaches a trigger level; then typically sent as a market order. |

Core order properties:

- participant / account
- product
- quantity
- side
- price
- validity

## Bid order

- Bid order means BUY order.
- Bid price is the price of a BUY order.
- Best bid usually means the highest active buy order price for a product.

## Ask order / offer

Ask order or offer means SELL order.

## Order matching

Matching rules are documented in [../trading/01_exchange_mechanics.md](../trading/01_exchange_mechanics.md).

## Order book

An order book collects orders for a product.

- The bid side shows combined quantity of BUY orders at each price.
- The ask side shows combined quantity of SELL orders at each price.
- An uncrossed book has no bid orders at or above the lowest ask.
- A crossed book has buy orders above the lowest ask, so trading is possible.

## Priority

See [../trading/01_exchange_mechanics.md](../trading/01_exchange_mechanics.md).

## Market making

The source defines market making as trading where the trader does not necessarily have a strong opinion on price direction, but conducts business through the attempt of simultaneous buying and selling of products.
