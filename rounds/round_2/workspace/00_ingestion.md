# Round Ingestion

## Status

COMPLETED

## Sources

- Active round wiki: [https://imc-prosperity.notion.site/Round-2-Growing-Your-Outpost-345e8453a09380b29132fdf4de9174d4](https://imc-prosperity.notion.site/Round-2-Growing-Your-Outpost-345e8453a09380b29132fdf4de9174d4)
- Raw factual source: `docs/prosperity_wiki_raw/13_round_2.md`
- Shared wiki facts: `docs/prosperity_wiki/` (Round 1 trading rules still apply)

## Algorithmic Products

| Product | Symbol | Position Limit | Caveat |
| --- | --- | ---: | --- |
| Ash Coated Osmium | `ASH_COATED_OSMIUM` | 80 | Same symbol/limit as Round 1. Round 2 data is a fresh 3-day sample. Round 1 behavior (FV≈10000, AR(1)-like reversion) is a prior, not a rule. |
| Intarian Pepper Root | `INTARIAN_PEPPER_ROOT` | 80 | Same symbol/limit as Round 1. Round 2 data may have a different level/slope; EDA must re-estimate the drift model from Round 2 CSVs, not inherit from Round 1. |

## Manual Products

| Product | Symbol | Manual Mechanics Source | Caveat |
| --- | --- | --- | --- |
| Invest & Expand budget allocation | `INVEST_EXPAND` | Round 2 wiki | 50,000 XIRECs to split across Research / Scale / Speed. Research is logarithmic, Scale is linear, Speed is rank-based relative to other teams (zero-sum). Not in algorithm scope. |

## Round-Specific Facts

- Market Access Fee (MAF): `class Trader` must expose a `bid()` method returning an integer. Top 50% of bids (strictly above the median) get 25% more quotes in the book.
- MAF fee is one-time, deducted from Round 2 profit only if the bid is accepted.
- During local testing, all participants interact with 80% of generated quotes regardless of bid.
- `bid()` is only read in Round 2; ignored in other rounds.
- Two new raw CSV days are provided (`day_-1`, `day_0`, `day_1`) with the same schema as Round 1.
- Position limits unchanged (80 each).
- Round 2 is the last qualifier before Phase 2; cumulative target: ≥ 200,000 XIRECs.

## Source Caveats

- The MAF "top 50%" rule is strict-above-median: ties at the median are rejected.
- Wiki notes that identical submissions give "very limited payoff" because 80% of quotes are slightly randomized per submission.
- The wiki also includes a pre-computed Lagrangian optimum for Invest & Expand assuming fixed Speed multipliers; this is a heuristic, not a guarantee because Speed is rank-based against unknown opponents.
- Round 1 EDA findings (IPR linear drift, ACO FV≈10000) must NOT be assumed to carry over; Round 2 CSVs must be re-profiled.

## Unknowns That May Affect Downstream Work

| Unknown | Affects | Why It Matters | Next Action |
| --- | --- | --- | --- |
| Round 2 IPR drift rate and start level | EDA, strategy, impl | Bot must re-initialize `fair_value(t) = start + slope * t`; wrong prior destroys IPR P&L | EDA (phase 01) — fit per-day slope from Round 2 CSV |
| Round 2 ACO fair-value level and reversion speed | EDA, strategy | If ACO level has shifted, hardcoding 10,000 mis-centers all quotes | EDA (phase 01) — compute daily mean/variance, AR(1) coefficient, Kalman calibration |
| Median MAF bid across competitors | Strategy | Controls whether our bid is top-50% | Game-theory modeling in phase 03 strategy |
| Opponent Speed allocations | Manual | Speed is rank-based; our 10% could be overkill or underkill | Not in algo scope; phase 03 manual sub-plan |
| Whether Round 2 adds any new regime mid-day | EDA, strategy | Round 1 showed flat ACO across days; Round 2 may differ | Phase 01 — HMM / changepoint analysis |

Unknowns must stay separate from facts. Each material unknown needs a next action or explicit deadline-risk deferral before ingestion can be `COMPLETED`.

## Ingestion Quality Checklist

- [x] Official round wiki link is present.
- [x] Accepted factual sources were reviewed.
- [x] Algorithmic products, symbols, and limits are explicit or marked unknown.
- [x] Manual-only mechanics are separated from bot requirements.
- [x] Round-specific mechanics are separated from shared API/trading facts.
- [x] Source caveats and conflicts are recorded.
- [x] Available and missing data artifacts are noted.
- [x] Unknowns that may affect EDA, strategy, or implementation are actionable.
- [x] No facts were inferred from bots, performances, memory, or playbook heuristics.

## Data Artifacts Present

| File | Status |
| --- | --- |
| `rounds/round_2/data/raw/prices_round_2_day_-1.csv` | 20,001 rows (10k per product incl. header) |
| `rounds/round_2/data/raw/prices_round_2_day_0.csv`  | 20,001 rows |
| `rounds/round_2/data/raw/prices_round_2_day_1.csv`  | 20,001 rows |
| `rounds/round_2/data/raw/trades_round_2_day_-1.csv` | 791 rows |
| `rounds/round_2/data/raw/trades_round_2_day_0.csv`  | 804 rows |
| `rounds/round_2/data/raw/trades_round_2_day_1.csv`  | 799 rows |

## Downstream Actions

- EDA: re-profile IPR drift and ACO microstructure for Round 2; apply Kalman calibration and HMM regime detection to identify hidden modes.
- Understanding: translate EDA into signal hypotheses with confidence levels.
- Strategy: draft candidates including MAF bid game theory and manual allocation.
- Implementation: carry over Round 1 best bot as baseline; add `bid()` and any Round 2 regime adjustments.

## Review

- Reviewer: Self-review (Bruno)
- Status: Ready for phase 01 EDA
