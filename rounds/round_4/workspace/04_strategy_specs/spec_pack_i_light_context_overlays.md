# Spec Pack I: Context As Entry Quality

## Review Status

- Status: `COMPLETED`
- Owner: Codex
- Reviewer: Human
- Reviewed on: 2026-04-28

## Pack Members

| Candidate | Role In Pack | Target Bot Path |
| --- | --- | --- |
| `r4_w2_09_vex_tape_clean_entry` | clean-tape contextual entry | `rounds/round_4/bots/noel/canonical/r4_w2_09_vex_tape_clean_entry_debugged.py` |
| `r4_w2_10_vex_imbalance_surge_entry` | event-driven imbalance entry | `rounds/round_4/bots/noel/canonical/r4_w2_10_vex_imbalance_surge_entry_debugged.py` |
| `r4_w2_11_vex_low_concentration_entry` | family-ecology regime gate | `rounds/round_4/bots/noel/canonical/r4_w2_11_vex_low_concentration_entry_debugged.py` |
| `r4_w2_12_5300_option_only_veto` | direct `5300` plus useful veto | `rounds/round_4/bots/noel/canonical/r4_w2_12_5300_option_only_veto_debugged.py` |

## Why This Pack Exists

Wave 1 showed that context can help, but broad defensive overlays were too
blunt. This pack reuses context mainly as entry-quality control instead of
whole-bot shutdown.

## Feature Contract Summary

| Candidate | Main Feature | Inputs | Intended Learning |
| --- | --- | --- | --- |
| `r4_w2_09` | clean-tape entry | `VEX` tape, `5200` warning state, family pressure | whether context should improve entry selection directly |
| `r4_w2_10` | imbalance surge entry | `VEX` imbalance and spread | whether event-driven `VEX` entry beats always-on quoting |
| `r4_w2_11` | low-concentration entry | family participant concentration, pressure state | whether fragmented family flow is a better `VEX` regime |
| `r4_w2_12` | option-only `5300` plus veto | `5300` fair value plus `5200` warning state | whether context survives once parent contamination is removed |

## Execution Contract

- `r4_w2_09` to `r4_w2_11` trade `VEX` only.
- `r4_w2_12` trades `VEV_5300` only.
- Context remains secondary; if the pack kills engagement everywhere, it should
  be pruned quickly.

## Validation Plan

- Compare trade windows against the retained structural bots.
- Look for distinct engagement windows, not just lower trade count.
- If a branch only suppresses activity without cleaner path quality, classify
  it as `no lift`.

## Notes

- This pack no longer spends slots on the older `trade_to_book_light`,
  `family_pressure_light`, or `parent_gate` variants.
