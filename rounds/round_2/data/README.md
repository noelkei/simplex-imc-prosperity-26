# Round 2 Data

Raw Round 2 sample data artifacts are present under `raw/`.

Store only round-local data artifacts here. Do not treat data observations as official rules; use `docs/prosperity_wiki/` for facts.

## Current Raw Artifacts

| File | Rows incl. header | Product rows / trades |
| --- | ---: | --- |
| `raw/prices_round_2_day_-1.csv` | 20,001 | 10,000 `ASH_COATED_OSMIUM`, 10,000 `INTARIAN_PEPPER_ROOT` |
| `raw/prices_round_2_day_0.csv` | 20,001 | 10,000 `ASH_COATED_OSMIUM`, 10,000 `INTARIAN_PEPPER_ROOT` |
| `raw/prices_round_2_day_1.csv` | 20,001 | 10,000 `ASH_COATED_OSMIUM`, 10,000 `INTARIAN_PEPPER_ROOT` |
| `raw/trades_round_2_day_-1.csv` | 791 | 459 `ASH_COATED_OSMIUM`, 331 `INTARIAN_PEPPER_ROOT` |
| `raw/trades_round_2_day_0.csv` | 804 | 471 `ASH_COATED_OSMIUM`, 332 `INTARIAN_PEPPER_ROOT` |
| `raw/trades_round_2_day_1.csv` | 799 | 465 `ASH_COATED_OSMIUM`, 333 `INTARIAN_PEPPER_ROOT` |

Prices schema:

```text
day;timestamp;product;bid_price_1;bid_volume_1;bid_price_2;bid_volume_2;bid_price_3;bid_volume_3;ask_price_1;ask_volume_1;ask_price_2;ask_volume_2;ask_price_3;ask_volume_3;mid_price;profit_and_loss
```

Trades schema:

```text
timestamp;buyer;seller;symbol;currency;price;quantity
```

Source caveat: the Round 2 wiki source references `Wiki_ROUND_2_data.zip`; this folder currently stores extracted CSV files, not the original zip attachment.

## Folders

- `raw/`: unmodified platform, sample, or run files. Treat this as append-only; do not clean or edit files in place.
- `processed/`: derived or cleaned data created from named sources. Each artifact must link or state its source and processing method.
- `external/`: teammate-provided or non-platform context. These artifacts are non-authoritative and must not be treated as official Prosperity facts.

## Naming

- `raw/`: `<source>_<day_or_run>_<description>.<ext>`
- `processed/`: `derived_<source>_<purpose>.<ext>`
- `external/`: `external_<source>_<description>.<ext>`

## Update Rules

- Link any data used by EDA from `workspace/01_eda/` or `workspace/phase_01_eda_context.md`.
- When processed data changes, update the EDA summary or phase context with the source and method.
- If data contradicts wiki facts, keep the wiki as authoritative and record the data issue as a caveat.
