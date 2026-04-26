# Round 4 - "The More The Merrier"

Source capture: Round 4 Notion wiki content pasted by Noel on 2026-04-26.

For this second round of the Great Orbital Ascension Trials, the Frontier Trade Watch (FTW) has disclosed information about the counterparties active in the market. Their IDs have been added to the historical trade data available in the Data Capsule.

You will continue trading Hydrogel Packs (`HYDROGEL_PACK`), Velvetfruit Extract (`VELVETFRUIT_EXTRACT`), and 10 Velvetfruit Extract Vouchers (`VELVETFRUIT_EXTRACT_VOUCHER`). This time, however, having insight into your counterparties, and understanding what defines their trading behavior and the unique opportunities they bring, could shift the balance for teams that know how to separate profit from pretense.

In addition to your algorithmic trading activities, you will also have the opportunity to manually trade the Aether Crystal, along with a collection of option contracts based on it. Some of these contracts are more exotic than others. You must determine a strategy that turns this one-time opportunity into profit.

Be aware that these exotic options operate independently from your algorithmic trading activities.

## Round Objective

Optimize your Python program to trade `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, and `VELVETFRUIT_EXTRACT_VOUCHER`, incorporating the newly disclosed counterparty information into your strategy.

Select from the available Aether Crystal and corresponding option contracts, and submit your orders to generate additional profit.

## Algorithmic trading challenge: "Hello, I'm Mark"

The products are the same as in Round 3 (`HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, and 10 `VELVETFRUIT_EXTRACT_VOUCHER` options), but now you have counterparty information available. That is, you can identify every other participant in the market and study their behavior.

In the datamodel described in Appendix B: datamodel.py file in Writing an Algorithm in Python, you will find the `Trade` class defined. For previous rounds 1, 2, and 3, the `self.buyer` and `self.seller` fields were always `None` as no counterparty information was available.

Code snippet for `class Trade`:

```python
class Trade:
    def __init__(self, symbol: Symbol, price: int, quantity: int, buyer: UserId = None, seller: UserId = None, timestamp: int = 0) -> None:
        self.symbol = symbol
        self.price: int = price
        self.quantity = quantity
        self.buyer = buyer
        self.seller = seller
        self.timestamp = timestamp
```

With increased transparency in the market, however, these `self.buyer` and `self.seller` fields now represent the names of the participants. Please feel free to leverage this information however you see fit, and refine your strategy using this extra visibility.

The position limits are still:

- `HYDROGEL_PACK`: 200
- `VELVETFRUIT_EXTRACT`: 200
- `VELVETFRUIT_EXTRACT_VOUCHER`: 300 for each of the 10 vouchers

Example: `VEV_5000` is an option with strike price 5000, has TTE=4 days in round 4, and has a position limit of 300.

## Manual trading challenge: "Vanilla Just Isn't Exotic Enough"

As the Intarian economy evolved, trading expanded beyond standard calls and puts. In this round, you can trade `AETHER_CRYSTAL`, vanilla options with 2 and 3 week expiries, and several exotic derivatives written on the same underlying. Please note that a "week" here refers to 5 trading days and that the standard number of trading days per year is 252.

Your objective is to construct positions that generate positive expected PnL. But be aware: unhedged exposure can lead to large losses, so risk management matters.

All products are written on `AETHER_CRYSTAL`. You can trade the underlying, 2 week and 3 week vanilla calls and puts, and the following exotics:

### Chooser Option

Expires in 3 weeks. After 2 weeks, the buyer chooses whether it becomes a call or a put, selecting whichever would be in the money at that time. It then behaves like a standard option for the final week until expiry.

### Binary Put Option

Has an all-or-nothing payoff. If the underlying is below the strike at expiry, it pays the specified amount. Otherwise, it expires worthless.

### Knock-Out Put Option

Behaves like a regular put unless the underlying ever trades below the knockout barrier before expiry. If the barrier is breached at any point, the option immediately becomes worthless.

You may buy or sell up to the displayed volume in each product. Your final score is the average PnL across 100 simulations of the underlying.

The underlying `AETHER_CRYSTAL` is simulated using Geometric Brownian Motion with zero risk-neutral drift and fixed annualized volatility of 251%. Prices evolve on a discrete grid of 4 steps per trading day, assuming 252 trading days per year.

And remember, when payoffs become conditional, so does risk. Good luck!

## Submit your orders

Input your orders for the Aether Crystal and corresponding option contracts directly in the Manual Challenge Overview window and click the "Submit" button. You can re-submit new orders until the end of the trading round. When the round ends, the last submitted orders will be locked in and processed.

## Supplementary note captured with the round page

The FTW has identified your trading counterparties as products of several local neuro-robotics research programs. Surprisingly, they are all named "Mark" followed by a number. These IDs have been added to the historical trade data in the Data Capsule. Use this information to re-evaluate your strategy for trading Protein Snackpacks, Velvetfruit Extract, and VEVs.

This Data Capsule contains historical performance data for all available tradable goods.

Download the data file to analyze the performance history of Hydrogel Packs and Velvetfruit Extract and gain insight into counterparty trading behavior.

All the Velvetfruit Extract Vouchers have a Time To Expiry (TTE) of 7 Solvenarian days, starting from day 1. The available VEVs are:

- `VEV_4000`; Strike price: 4000
- `VEV_4500`; Strike price: 4500
- `VEV_5000`; Strike price: 5000
- `VEV_5100`; Strike price: 5100
- `VEV_5200`; Strike price: 5200
- `VEV_5300`; Strike price: 5300
- `VEV_5400`; Strike price: 5400
- `VEV_5500`; Strike price: 5500
- `VEV_6000`; Strike price: 6000
- `VEV_6500`; Strike price: 6500

## Source caveat

- The supplementary note says "Protein Snackpacks" in one sentence, but the main Round 4 page lists `HYDROGEL_PACK`. Treat that line as a source inconsistency and do not infer a product change from it.
