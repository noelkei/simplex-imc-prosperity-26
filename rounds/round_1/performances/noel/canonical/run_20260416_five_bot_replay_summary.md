# Performance Run Summary: Five-Bot Immediate-Fill Replay

## Run Metadata

- Run ID: `run_20260416_five_bot_replay`
- Date: 2026-04-16
- Round: `round_1`
- Member / owner: `noel`
- Candidate IDs: `candidate_09_baseline_fv_combo`, `candidate_10_carry_tight_mm`, `candidate_11_microstructure_scalper`, `candidate_12_aco_markov_overlay`, `candidate_13_hybrid_adaptive_model`
- Decision relevance: canonical
- Strategy spec: `rounds/round_1/workspace/04_strategy_specs/spec_experimental_5_bot_matrix.md`
- Raw artifact path: `rounds/round_1/performances/noel/canonical/run_20260416_five_bot_replay_metrics.json`
- Replay script: `rounds/round_1/performances/noel/canonical/replay_five_bot_batch.py`
- Data day / source: `rounds/round_1/data/raw/prices_round_1_day_{-2,-1,0}.csv`
- Baseline / comparison run: same replay settings for all five bots
- Validation check: immediate fills against visible sample order books; passive future fills are not modeled

## Result Summary

| Rank | Bot | Total PnL | IPR PnL | ACO PnL | Max Pos IPR | Max Pos ACO | Rejections | Errors | Decision |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | `candidate_10_bot02_carry_tight_mm.py` | 247628.0 | 238054.0 | 9574.0 | 80 | 80 | 0 | 0 | promote to active platform/backtest validation |
| 2 | `candidate_13_bot05_hybrid_adaptive.py` | 157468.0 | 152629.0 | 4839.0 | 69 | 78 | 0 | 0 | promote as second active candidate |
| 3 | `candidate_12_bot04_aco_markov.py` | 154812.0 | 146232.0 | 8580.0 | 78 | 78 | 0 | 0 | keep as close fallback |
| 4 | `candidate_09_bot01_baseline_fv_combo.py` | 152123.0 | 146232.0 | 5891.0 | 78 | 76 | 0 | 0 | keep as baseline reference |
| 5 | `candidate_11_bot03_micro_scalper.py` | 41236.5 | 35757.5 | 5479.0 | 64 | 64 | 0 | 0 | keep as differentiated but lower-priority |

## Comparability

- Comparable to baseline: yes, within this local replay method.
- Same data/source: yes.
- Same bot/spec version basis: yes, all five came from `spec_experimental_5_bot_matrix.md`.
- Known differences: this replay is not the official Prosperity simulator and does not model later fills of passive orders.

## Interpretation Limits

- Non-authoritative evidence: sample-data replay is validation evidence, not an official rule or final platform result.
- Missing artifacts: no official platform run/log yet for these five files.
- Comparability caveat: immediate-fill replay favors strategies that cross the spread or sweep visible liquidity; passive market-making edge may be understated.

## Findings

- Finding: `candidate_10_bot02_carry_tight_mm.py` is clearly best in this replay.
- Signal/regime evidence verdict: supports IPR directional carry and ACO tight FV MM.
- Verdict basis: +238054.0 IPR PnL and +9574.0 ACO PnL, no errors or rejections.

- Finding: `candidate_13_bot05_hybrid_adaptive.py` and `candidate_12_bot04_aco_markov.py` are close second-tier candidates.
- Signal/regime evidence verdict: supports keeping one adaptive/model candidate alive.
- Verdict basis: both exceed 154k total PnL with no rejections; bot_05 has stronger total PnL, bot_04 has stronger ACO PnL.

- Finding: pure microstructure is differentiated but weaker.
- Signal/regime evidence verdict: weakens microstructure-only priority.
- Verdict basis: bot_03 is profitable but much lower total PnL than carry/hybrid variants.

## Decision

- Promote `candidate_10_bot02_carry_tight_mm.py` and `candidate_13_bot05_hybrid_adaptive.py` to active implementation candidates for the next validation step.
- Keep `candidate_12_bot04_aco_markov.py` as the first fallback because its ACO result is strong and total PnL is close to bot_05.
- Do not select a final submission from this replay alone.

## Next Action

- Run the promoted top two bots through the most platform-like runner available.
- If only manual platform runs are available, submit/run `candidate_10_bot02_carry_tight_mm.py` first, then `candidate_13_bot05_hybrid_adaptive.py`, and preserve logs/results under `rounds/round_1/performances/noel/canonical/`.
