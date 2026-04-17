# EDA Advanced Signal Research

## Question

Which lightweight high-edge directions are promising for Round 1 without using known sample length, time-to-end, or end-of-sample liquidation behavior?

## Data Sources

- Raw prices: `rounds/round_1/data/raw/prices_round_1_day_{-2,-1,0}.csv`
- Raw trades: `rounds/round_1/data/raw/trades_round_1_day_{-2,-1,0}.csv`
- Output metrics: `rounds/round_1/data/processed/advanced_signal_research_metrics.json`

## Data Quality

| Product | Rows | Valid Mid | Zero Mid | Both-Sided | One-Sided |
| --- | ---: | ---: | ---: | ---: | ---: |
| `INTARIAN_PEPPER_ROOT` | 30000 | 29946 | 54 | 27688 | 2258 |
| `ASH_COATED_OSMIUM` | 30000 | 29951 | 49 | 27644 | 2307 |

## Signal Verdicts

| Product | Direction | Verdict | Evidence Note |
| --- | --- | --- | --- |
| `INTARIAN_PEPPER_ROOT` | microprice + imbalance | weak-medium | micro corr 0.314 / imbalance corr 0.646 |
| `INTARIAN_PEPPER_ROOT` | residual z-score | strong | best z50 threshold 2.0 hit 0.9703703703703703 n 2835 |
| `INTARIAN_PEPPER_ROOT` | OU / half-life | medium | mean phi 0.00913105579625657 |
| `INTARIAN_PEPPER_ROOT` | trade flow pressure | medium | sign acc 0.6716604244694132 n 1007 |
| `ASH_COATED_OSMIUM` | microprice + imbalance | medium | micro corr 0.322 / imbalance corr 0.646 |
| `ASH_COATED_OSMIUM` | residual z-score | strong | best z50 threshold 2.0 hit 0.9643962848297214 n 2584 |
| `ASH_COATED_OSMIUM` | OU / half-life | medium | mean phi 0.7264981476225275 |
| `ASH_COATED_OSMIUM` | trade flow pressure | weak | sign acc 0.49430051813471504 n 1264 |

## Product Details

### `INTARIAN_PEPPER_ROOT`

| Check | Result | Use |
| --- | --- | --- |
| Microprice offset | corr `0.314`, sign `0.8798`, n `8587` | execution overlay only |
| L1 imbalance | corr `0.6458`, sign `0.8977`, n `10843` | quote skew / gate |
| Residual reversion | best threshold `10`, hit `0.9934`, n `152` | FV mean-reversion / taker gate |
| Rolling z-score | best z50 threshold `2.0`, hit `0.9704`, n `2835` | normalize entries; do not use as standalone model |
| OU half-life | mean phi `0.0091`, mean half-life obs `0.1443` | short local horizon only; beware bid-ask bounce |
| Trade pressure proxy | sign `0.6717`, corr `0.3941`, rows `1007` | weak unless paired with book state |
| Taker edge >= 5 | buy n `0`, buy markout `None`, sell n `43`, sell markout `2.8953` | high-confidence sweep when capacity allows |
| Taker edge >= 8 | buy n `0`, buy markout `None`, sell n `0`, sell markout `None` | high-confidence sweep when capacity allows |

### `ASH_COATED_OSMIUM`

| Check | Result | Use |
| --- | --- | --- |
| Microprice offset | corr `0.3222`, sign `0.9012`, n `8789` | execution overlay only |
| L1 imbalance | corr `0.6455`, sign `0.9162`, n `11051` | quote skew / gate |
| Residual reversion | best threshold `10`, hit `0.7339`, n `2300` | FV mean-reversion / taker gate |
| Rolling z-score | best z50 threshold `2.0`, hit `0.9644`, n `2584` | normalize entries; do not use as standalone model |
| OU half-life | mean phi `0.7265`, mean half-life obs `2.2804` | short local horizon only; beware bid-ask bounce |
| Trade pressure proxy | sign `0.4943`, corr `-0.01`, rows `1264` | weak unless paired with book state |
| Taker edge >= 5 | buy n `246`, buy markout `-0.6606`, sell n `287`, sell markout `-3.8362` | high-confidence sweep when capacity allows |
| Taker edge >= 8 | buy n `81`, buy markout `1.5679`, sell n `56`, sell markout `0.0714` | high-confidence sweep when capacity allows |

## Downstream Use

- Strong enough to use: IPR +80 carry, ACO fixed-FV two-sided market making, ACO residual/z-score gates, inventory skew, and quote-quality filtering.
- Use as overlays: microprice, imbalance, one-sided-book handling, volatility/spread regimes, and CUSUM as a defensive guard.
- Weak or not standalone: trade-flow proxy, PCA-only, end-of-sample liquidation, and broad HMM/controller complexity.

## Caveats

- All horizons are local product-observation horizons; no feature uses known sample length or time remaining.
- Sample data supports strategy selection, not official rules.
- Passive maker fill quality is better judged from platform logs than CSV-only replay.
