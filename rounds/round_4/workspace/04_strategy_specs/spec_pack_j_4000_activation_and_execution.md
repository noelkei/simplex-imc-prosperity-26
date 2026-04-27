# Spec Pack J: 4000 Activation And Direct Attribution

## Review Status

- Status: `COMPLETED`
- Owner: Codex
- Reviewer: Human
- Reviewed on: 2026-04-28

## Pack Members

| Candidate | Role In Pack | Target Bot Path |
| --- | --- | --- |
| `r4_w2_13_4000_forced_activation` | parented activation baseline | `rounds/round_4/bots/noel/canonical/r4_w2_13_4000_forced_activation_debugged.py` |
| `r4_w2_14_4000_option_only_band_entry` | direct option-only band test | `rounds/round_4/bots/noel/canonical/r4_w2_14_4000_option_only_band_entry_debugged.py` |
| `r4_w2_15_4000_quote_ladder_probe` | winner-style execution probe | `rounds/round_4/bots/noel/canonical/r4_w2_15_4000_quote_ladder_probe_debugged.py` |

## Why This Pack Exists

Wave 1 never gave an honest `4000` verdict. This pack now asks:

- can `4000` activate at all?
- can it activate without the parent `VEX` branch doing the real work?
- is it execution-limited rather than dead?

## Feature Contract Summary

| Candidate | Main Feature | Inputs | Intended Learning |
| --- | --- | --- | --- |
| `r4_w2_13` | parented forced activation | `VEX` book, `4000` fair gap | whether `4000` is alive at all |
| `r4_w2_14` | option-only band entry | direct `4000` fair gap only | whether `4000` can stand on its own with cleaner attribution |
| `r4_w2_15` | winner-style quote ladder | direct `4000` fair bid/ask versus live book | whether execution quality is the missing ingredient |

## Execution Contract

- `r4_w2_13` and `r4_w2_15` may trade `VEX` plus `VEV_4000`.
- `r4_w2_14` trades `VEV_4000` only.
- No broad contextual stack should be added here until direct activation is
  visible.

## Validation Plan

- First confirm visible `VEV_4000` quotes or inventory.
- If `r4_w2_13` is flat, treat the whole family cautiously.
- If `r4_w2_14` engages but `r4_w2_13` does not, parent contamination is a
  real issue.
- If `r4_w2_15` outperforms `r4_w2_13` on engagement quality, classify `4000`
  as at least partly `execution-limited`.

## Notes

- The older `4000_benign_tape_only` branch was replaced because it spent a slot
  on a small overlay before direct attribution was settled.
