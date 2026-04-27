# Spec Pack H: 5300 Isolation, Dislocation, And Winner Style

## Review Status

- Status: `COMPLETED`
- Owner: Codex
- Reviewer: Human
- Reviewed on: 2026-04-28

## Pack Members

| Candidate | Role In Pack | Target Bot Path |
| --- | --- | --- |
| `r4_w2_05_5300_clean_value_retest` | clean parented baseline | `rounds/round_4/bots/noel/canonical/r4_w2_05_5300_clean_value_retest_debugged.py` |
| `r4_w2_06_5300_direct_dislocation_only` | option-only dislocation probe | `rounds/round_4/bots/noel/canonical/r4_w2_06_5300_direct_dislocation_only_debugged.py` |
| `r4_w2_07_5300_queue_takeover_probe` | winner-style execution probe | `rounds/round_4/bots/noel/canonical/r4_w2_07_5300_queue_takeover_probe_debugged.py` |
| `r4_w2_08_5300_with_5200_veto` | strongest parent plus useful veto | `rounds/round_4/bots/noel/canonical/r4_w2_08_5300_with_5200_veto_debugged.py` |

## Why This Pack Exists

`5300` still looks like the most interesting active family, but we still need
to separate:

- clean baseline life
- direct signal without parent noise
- execution style value
- contextual veto value

## Feature Contract Summary

| Candidate | Main Feature | Inputs | Intended Learning |
| --- | --- | --- | --- |
| `r4_w2_05` | clean `5300` fair-value baseline | `VEX` book, `5300` book, rolling fair value | whether `5300` has direct current-round life |
| `r4_w2_06` | take-only direct dislocation | `5300` fair gap only | whether `5300` can stand on its own without parent `VEX` activity |
| `r4_w2_07` | winner-style queue takeover | `5300` fair bid/ask versus live book | whether execution style is the missing piece |
| `r4_w2_08` | `5200` veto overlay | recent `5200` trades plus `5300` baseline | whether the best contextual signal improves the active family |

## Execution Contract

- `r4_w2_05`, `r4_w2_07`, `r4_w2_08` may trade both `VEX` and `VEV_5300`.
- `r4_w2_06` trades `VEV_5300` only.
- No direct `VEV_5200` inventory.
- Winner-style adaptation remains limited to portable structure, not old-round
  calibration.

## Validation Plan

- First check whether direct `5300` inventory or quotes appear at all.
- Compare `r4_w2_06` and `r4_w2_08` to the parented baseline for attribution.
- Use `r4_w2_07` to decide whether the family is `execution-limited` or simply
  weak.

## Notes

- The old `5300_horizon_hold_v2` branch was replaced because it spent too much
  slot budget on another retention-style tweak instead of a cleaner signal
  test.
