# Datamodel Reference

Source basis: `docs/prosperity_wiki_raw/10_writing_an_algorithm_in_python.md`.

## Type aliases

The raw datamodel lists:

```python
Time = int
Symbol = str
Product = str
Position = int
UserId = str
ObservationValue = int
```

## `TradingState`

Constructor fields:

```python
TradingState(
    traderData: str,
    timestamp: Time,
    listings: Dict[Symbol, Listing],
    order_depths: Dict[Symbol, OrderDepth],
    own_trades: Dict[Symbol, List[Trade]],
    market_trades: Dict[Symbol, List[Trade]],
    position: Dict[Product, Position],
    observations: Observation,
)
```

Fields:

| Field | Meaning |
| --- | --- |
| `traderData` | String state returned by the previous `Trader.run()` call. |
| `timestamp` | Current timestamp. |
| `listings` | Product listing data by symbol. |
| `order_depths` | Available order book per symbol. |
| `own_trades` | Trades done by the algorithm since the previous state. |
| `market_trades` | Trades done by other market participants since the previous state. |
| `position` | Current signed position by product. |
| `observations` | Simple and conversion observations. |

## `Listing`

Constructor fields:

```python
Listing(symbol: Symbol, product: Product, denomination: Product)
```

Fields:

- `symbol`
- `product`
- `denomination`

## `Order`

Constructor fields:

```python
Order(symbol: Symbol, price: int, quantity: int)
```

Fields:

- `symbol`: product symbol.
- `price`: order price.
- `quantity`: signed order quantity.

Quantity sign rules are defined in [../trading/02_orders_and_position_limits.md](../trading/02_orders_and_position_limits.md).

## `OrderDepth`

Fields:

```python
buy_orders: Dict[int, int]
sell_orders: Dict[int, int]
```

- Dict keys are price levels.
- Dict values are aggregated volumes at those price levels.
- Sell-side volume sign rules are defined in [../trading/02_orders_and_position_limits.md](../trading/02_orders_and_position_limits.md).

## `Trade`

Constructor fields:

```python
Trade(
    symbol: Symbol,
    price: int,
    quantity: int,
    buyer: UserId = None,
    seller: UserId = None,
    timestamp: int = 0,
)
```

Fields:

- `symbol`
- `price`
- `quantity`
- `buyer`
- `seller`
- `timestamp`

Counterparty information:

- `buyer` and `seller` are only non-empty strings if the algorithm itself is the buyer or seller.
- If the algorithm is the buyer, `buyer = "SUBMISSION"`.
- If the algorithm is the seller, `seller = "SUBMISSION"`.

## `Observation`

Constructor fields:

```python
Observation(
    plainValueObservations: Dict[Product, ObservationValue],
    conversionObservations: Dict[Product, ConversionObservation],
)
```

Fields:

- `plainValueObservations`: simple product-to-value dictionary.
- `conversionObservations`: conversion observations by product.

## `ConversionObservation`

Raw constructor:

```python
ConversionObservation(
    bidPrice: float,
    askPrice: float,
    transportFees: float,
    exportTariff: float,
    importTariff: float,
    sunlight: float,
    humidity: float,
)
```

Raw assignment block:

```python
self.bidPrice = bidPrice
self.askPrice = askPrice
self.transportFees = transportFees
self.exportTariff = exportTariff
self.importTariff = importTariff
self.sugarPrice = sugarPrice
self.sunlightIndex = sunlightIndex
```

Conversion request rules are documented in [03_runtime_and_resources.md](03_runtime_and_resources.md).

## `ProsperityEncoder`

The raw datamodel includes:

```python
class ProsperityEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
```

## Source caveats

- The source alternates between `TraderState`, `TradingState`, and `Tradingstate`.
- `ConversionObservation` assigns `sugarPrice` and `sunlightIndex` even though the shown constructor parameters include `sunlight` and `humidity`.
- One `TradingState` example uses `denomination: "XIRECS"` instead of `denomination= "XIRECS"`.
