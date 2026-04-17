# Performance Run Summary: Cross-Bot Log And Replay Insights

## Run Metadata

- Run ID: `run_20260416_cross_bot_log_insights`
- Date: 2026-04-16
- Round: `round_1`
- Member / owner: `noel`
- Decision relevance: canonical
- Strategy spec: `rounds/round_1/workspace/04_strategy_specs/spec_experimental_5_bot_matrix.md`
- Primary bot under review: `rounds/round_1/bots/noel/canonical/candidate_10_bot02_carry_tight_mm.py`
- Related bot evidence:
  - `rounds/round_1/bots/amin/canonical/26-candidate_03_combined.py`
  - `rounds/round_1/bots/bruno/canonical/new_bot.py`
  - `rounds/round_1/bots/amin/historical/22-candidate_03_combined.py`
  - `rounds/round_1/bots/amin/historical/23-bot.py`
  - `rounds/round_1/bots/amin/historical/24-bot.py`
  - `rounds/round_1/bots/amin/historical/25-bot.py`
- Raw artifact paths:
  - `rounds/round_1/performances/noel/canonical/run_20260416_five_bot_replay_metrics.json`
  - `rounds/round_1/performances/amin/historical/22-candidate_03_combined.json`
  - `rounds/round_1/performances/amin/historical/23-bot.json`
  - `rounds/round_1/performances/amin/historical/23-bot.log`
  - `rounds/round_1/performances/amin/historical/24-bot.json`
  - `rounds/round_1/performances/amin/historical/24-bot.log`
  - `rounds/round_1/performances/amin/historical/25-bot.json`
  - `rounds/round_1/performances/amin/historical/25-bot.log`
  - `rounds/round_1/bots/amin/canonical/26-candidate_03_combined.json`
- Data day / source:
  - Platform-style JSON/logs cover day 0 timestamps `0..99900` (1000 iterations).
  - Local immediate-fill replay covers raw CSV days `-2`, `-1`, and `0` through timestamp `999900` (10000 iterations per day).
- Validation check: cross-artifact comparison of platform PnL, product PnL, final positions, tradeHistory, and local replay behavior.

## Result Summary

Platform-style JSON results:

| Artifact | Total PnL | IPR PnL | ACO PnL | Final IPR | Final ACO | Note |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `26-candidate_03_combined.json` | 9432.0625 | 7286.0000 | 2146.0625 | 80 | 46 | best platform-style JSON; artifact is currently under `bots/amin/canonical/` |
| `22-candidate_03_combined.json` | 8975.8438 | 6836.5000 | 2139.3438 | 75 | 45 | strong ACO, IPR capped at 75 |
| `24-bot.json` | 8975.8438 | 6836.5000 | 2139.3438 | 75 | 45 | identical result to 22 |
| `25-bot.json` | 8907.5000 | 7286.0000 | 1621.5000 | 80 | 16 | max-long IPR, weaker ACO |
| `23-bot.json` | 8545.5938 | 7286.0000 | 1259.5938 | 80 | 5 | max-long IPR, weakest ACO among Amin platform logs |

TradeHistory attribution from Amin logs:

| Log | Product | Own Trades | Buy Qty @ Avg | Sell Qty @ Avg | Net Own Pos | Activity Final PnL |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `23-bot.log` | `INTARIAN_PEPPER_ROOT` | 5 | 80 @ 12008.83 | 0 @ 0.00 | 80 | 7286.0000 |
| `23-bot.log` | `ASH_COATED_OSMIUM` | 92 | 280 @ 9997.66 | 275 @ 10002.15 | 5 | 1259.5938 |
| `24-bot.log` | `INTARIAN_PEPPER_ROOT` | 5 | 75 @ 12008.75 | 0 @ 0.00 | 75 | 6836.5000 |
| `24-bot.log` | `ASH_COATED_OSMIUM` | 78 | 260 @ 9995.45 | 215 @ 10003.88 | 45 | 2139.3438 |
| `25-bot.log` | `INTARIAN_PEPPER_ROOT` | 5 | 80 @ 12008.83 | 0 @ 0.00 | 80 | 7286.0000 |
| `25-bot.log` | `ASH_COATED_OSMIUM` | 89 | 275 @ 9996.92 | 259 @ 10002.83 | 16 | 1621.5000 |

Local immediate-fill replay, all available round 1 bots over full CSV days `-2/-1/0`:

| Rank | Bot | Total PnL | IPR PnL | ACO PnL | Max IPR | Max ACO |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | `amin/historical/23-bot.py` | 248629.0 | 238054.0 | 10575.0 | 80 | 80 |
| 2 | `amin/historical/25-bot.py` | 247643.0 | 238054.0 | 9589.0 | 80 | 80 |
| 3 | `noel/canonical/candidate_10_bot02_carry_tight_mm.py` | 247628.0 | 238054.0 | 9574.0 | 80 | 80 |
| 4 | `amin/canonical/26-candidate_03_combined.py` | 247628.0 | 238054.0 | 9574.0 | 80 | 80 |
| 5 | `bruno/canonical/new_bot.py` | 247628.0 | 238054.0 | 9574.0 | 80 | 80 |
| 6 | `amin/historical/22-candidate_03_combined.py` | 232567.0 | 223166.5 | 9400.5 | 75 | 75 |
| 7 | `amin/historical/24-bot.py` | 232567.0 | 223166.5 | 9400.5 | 75 | 75 |

The local replay does not model passive future fills, so it is useful for immediate-fill and position-limit sanity checks but incomplete for ACO passive quote tuning.

## Findings

- Finding: IPR max-long is the strongest actionable signal.
- Signal/regime evidence verdict: supports.
- Verdict basis: platform-style JSONs with final IPR `80` earn `7286.0` IPR PnL in the 1000-tick window, while the `75` cap earns `6836.5`; full local replay shows the same direction at larger scale (`238054.0` vs `223166.5` IPR PnL across three full CSV days).

- Finding: ACO edge depends materially on passive platform fills, not only immediate crossing.
- Signal/regime evidence verdict: supports fixed-FV passive market making, but weakens immediate-fill replay as the sole ACO ranking tool.
- Verdict basis: local first-1000 immediate replay assigns only about `662-710` ACO PnL to the Amin fixed-FV variants, while platform-style logs report `1259.5938` to `2146.0625`. TradeHistory shows ACO PnL comes from many own fills around `9995-10004`, including passive-style fills absent from the replay model.

- Finding: The best-supported family is max-long IPR plus ACO fixed-FV market making around `10000` with full-capacity passive quotes.
- Signal/regime evidence verdict: supports.
- Verdict basis: `26-candidate_03_combined.json` has the best platform-style total PnL (`9432.0625`) and best ACO PnL (`2146.0625`) while preserving max-long IPR. Its bot family matches the approved `bot_02` purpose more closely than microstructure or adaptive variants.

- Finding: Noel `candidate_10_bot02_carry_tight_mm.py` was under-posting ACO passive size relative to the approved spec.
- Signal/regime evidence verdict: implementation issue found and repaired.
- Verdict basis: the spec says bot 02 should post full-capacity ACO quotes, while the file previously posted fixed `24`-unit passive ACO orders. The file was updated to submit remaining capacity via the existing capacity clipper. Local replay ranking and no-error/no-rejection status are unchanged because passive future fills are not modeled.

- Finding: Microstructure-only and defensive hybrid variants are not primary candidates by current evidence.
- Signal/regime evidence verdict: weakens as primary submission path.
- Verdict basis: `candidate_11_bot03_micro_scalper.py` is far behind in full local replay (`41236.5` total PnL). `candidate_13_bot05_hybrid_adaptive.py` is second among Noel-only local replay results but lacks platform-style evidence and gives up much of the IPR carry.

## Comparability

- Comparable to baseline: yes within each run family; unclear across platform-style logs vs full local replay.
- Same data/source: no. Platform-style JSON/logs use day 0 first 1000 timestamps; full local replay uses three full CSV days.
- Same bot/spec version basis: mixed. Noel candidate 10, Amin 26, and Bruno `new_bot.py` are the same strategy family, but code differs in passive order sizing and exception/state handling.
- Known differences:
  - Local replay does not model passive future fills.
  - Some logs are ignored/untracked by `rg --files`; `find` located them.
  - `26-candidate_03_combined.json` is currently under `rounds/round_1/bots/amin/canonical/`, not under `rounds/round_1/performances/amin/canonical/`.

## Interpretation Limits

- Non-authoritative evidence: round-local bots, local replays, platform-style logs, and performance files are execution artifacts, not official rules.
- Missing artifacts: no platform JSON/log exists yet for the patched Noel `candidate_10_bot02_carry_tight_mm.py`.
- Comparability caveat: the highest-confidence final decision still requires a platform-like run of the patched candidate under `rounds/round_1/performances/noel/canonical/`.

## Decision

- Promote the patched `rounds/round_1/bots/noel/canonical/candidate_10_bot02_carry_tight_mm.py` as the primary platform validation target.
- Keep `rounds/round_1/bots/noel/canonical/candidate_13_bot05_hybrid_adaptive.py` as a defensive fallback, not the primary path.
- Do not promote the microstructure-only variant without new evidence.

## Next Action

- Run the patched Noel `candidate_10_bot02_carry_tight_mm.py` on the platform or the most platform-like runner available and store both JSON and log under `rounds/round_1/performances/noel/canonical/`.
- If time allows, run `candidate_13_bot05_hybrid_adaptive.py` second only as a regime-risk fallback.
- Move or copy the misfiled `26-candidate_03_combined.json` into the appropriate `performances/amin/canonical/` location in a separate cleanup step if the team wants the artifact tree normalized.
