# Spec Pack G: VEX Retention And Entry Quality

## Review Status

- Status: `COMPLETED`
- Owner: Codex
- Reviewer: Human
- Reviewed on: 2026-04-28

## Pack Members

| Candidate | Role In Pack | Target Bot Path |
| --- | --- | --- |
| `r4_w2_01_vex_late_no_new_entry` | retained rescue control | `rounds/round_4/bots/noel/canonical/r4_w2_01_vex_late_no_new_entry_debugged.py` |
| `r4_w2_02_vex_inside_book_only` | clean-tape entry probe | `rounds/round_4/bots/noel/canonical/r4_w2_02_vex_inside_book_only_debugged.py` |
| `r4_w2_03_vex_micro_reversal_entry` | aggression-reversal entry probe | `rounds/round_4/bots/noel/canonical/r4_w2_03_vex_micro_reversal_entry_debugged.py` |
| `r4_w2_04_vex_depth_supported_entry` | depth-supported entry probe | `rounds/round_4/bots/noel/canonical/r4_w2_04_vex_depth_supported_entry_debugged.py` |

## Why This Pack Exists

Wave 1 told us `VEX` is alive but retention-limited. After the Wave 2 debug
incident, the next high-ROI question is whether cleaner entry conditions teach
us more than piling on more tiny retention tweaks.

## Feature Contract Summary

| Candidate | Main Feature | Inputs | Intended Learning |
| --- | --- | --- | --- |
| `r4_w2_01` | late no-new-entry | `timestamp`, `VEX` book, position | whether late timing is still the main giveback source |
| `r4_w2_02` | inside-book only entry | `VEX` spread, recent `VEX` trade bucket | whether clean-tape windows dominate edge quality |
| `r4_w2_03` | micro reversal entry | recent aggressive `VEX` bucket, current imbalance | whether fading short aggressive bursts is better than continuous quoting |
| `r4_w2_04` | depth-supported entry | top-of-book depth, spread, side signal | whether book support matters more than late retention |

## Execution Contract

- Product traded: `VELVETFRUIT_EXTRACT` only.
- Shared base: lightweight `VEX` quoting / crossing engine.
- Distinguishing rule: each candidate changes only one entry or retention axis.
- Manual products: excluded.

## Validation Plan

- Confirm all four actually engage `VEX`.
- Compare trade count, fill timing, and close quality against `r4_w2_01`.
- Classify each branch as:
  `protect winner`, `entry-quality lift`, `execution-limited`, or `no edge`.

## Notes

- This pack intentionally no longer contains the older `peak_giveback_stop`,
  `toxic_window_cooldown`, or `smaller_second_clip` variants.
- Those superseded versions now live in `historical/` and should not drive new
  upload decisions.
