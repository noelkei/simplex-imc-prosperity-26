# Wave 2 Passive Quoting Vs Wave 1

## Status

Open

## Date

2026-04-28

## Reproduction

- Compare Wave 1 bot `r4_s09_5300_toxic_strike_gate` against active Wave 2
  bots on reconstructed `day_1` snapshots from
  `rounds/round_4/data/raw/prices_round_4_day_1.csv` and
  `trades_round_4_day_1.csv`.
- Use the standalone uploadable files under:
  - `rounds/round_4/bots/noel/historical/r4_s09_5300_toxic_strike_gate.py`
  - `rounds/round_4/bots/noel/canonical/r4_w2_01_vex_late_no_new_entry_debugged.py`
  - `rounds/round_4/bots/noel/canonical/r4_w2_05_5300_clean_value_retest_debugged.py`
  - `rounds/round_4/bots/noel/canonical/r4_w2_07_5300_queue_takeover_probe_debugged.py`
  - `rounds/round_4/bots/noel/canonical/r4_w2_08_5300_with_5200_veto_debugged.py`
  - `rounds/round_4/bots/noel/canonical/r4_w2_13_4000_forced_activation_debugged.py`
  - `rounds/round_4/bots/noel/canonical/r4_w2_15_4000_quote_ladder_probe_debugged.py`

## Expected Behavior

- Active Wave 2 bots should show at least some aggressive or near-aggressive
  behavior comparable to the live Wave 1 family when their theses are active.
- In particular, winner-style probes should occasionally cross or take obvious
  mispricings rather than only rest passive quotes.

## Observed Behavior

- Wave 2 bots do emit orders locally, but the observed order flow is almost
  entirely passive.
- On the sampled `day_1` window:
  - `w1_s09`: `167` orders, `45` classified as crossing, `122` passive
  - `w2_01`: `32` orders, `0` crossing, `32` passive
  - `w2_05`: `432` orders, `0` crossing, `432` passive
  - `w2_07`: `432` orders, `0` crossing, `432` passive
  - `w2_08`: `432` orders, `0` crossing, `432` passive
  - `w2_13`: `42` orders, `0` crossing, `42` passive
  - `w2_15`: `42` orders, `0` crossing, `42` passive
- Example at `timestamp=0`, `VEV_5300` book `46 x 48`:
  - Wave 1 `r4_s09` emits an immediate sell at `46` plus passive reposting.
  - Wave 2 `r4_w2_05` emits only passive quotes around `46/49`.

## Patch Applied

- Recalibrated the active Wave 2 option branches toward fill-seeking behavior:
  - lowered option edge thresholds
  - moved passive reposting closer to fair
  - allowed winner-style branches to take when fair touches the touch
  - replaced purely centered BS execution fair with a more aggressive
    execution-fair blend anchored by a Wave 1-style heuristic
- Regenerated all active `*_debugged.py` uploadables after the engine change.

## Post-Patch Local Check

- On the same sampled `day_1` window:
  - `w2_05`: `626` orders, `200` crossing, `426` passive
  - `w2_07`: `626` orders, `200` crossing, `426` passive
  - `w2_08`: `626` orders, `200` crossing, `426` passive
  - `w2_13`: `47` orders, `5` crossing, `42` passive
  - `w2_15`: `47` orders, `5` crossing, `42` passive
- This does not prove profitability, but it does remove the specific passivity
  regression diagnosed in this issue.

## Root Cause Hypothesis

- This is primarily a **pricing / execution posture regression**, not a pure
  “bot does nothing” bug.
- Wave 1 overlays use a coarse intrinsic-plus-constant fair value that often
  makes the bot aggressive enough to cross and get filled.
- Wave 2 option branches use a Black-Scholes / rolling-IV fair value that sits
  much closer to the observed market, so the conditions
  `ask <= fair - edge` and `bid >= fair + edge` rarely trigger.
- As a result, the winner-style probes (`r4_w2_07`, `r4_w2_15`) almost never
  enter their intended take-first behavior because their fair band is too
  centered.

## Classification

- `implementation behavior regression`
- `execution-limited / too-passive`

## Linked Specs

- `rounds/round_4/workspace/04_strategy_specs/spec_pack_h_5300_winner_style_and_veto.md`
- `rounds/round_4/workspace/04_strategy_specs/spec_pack_j_4000_activation_and_execution.md`
- `rounds/round_4/workspace/04_strategy_specs/spec_pack_g_vex_retention_rescue.md`

## Linked Validation Context

- `rounds/round_4/workspace/phase_06_testing_context.md`
- `rounds/round_4/workspace/phase_07_debugging_context.md`

## Next Action

- Re-upload the active `_debugged.py` queue and rerun:
  `r4_w2_05`, `r4_w2_07`, `r4_w2_08`, `r4_w2_13`, `r4_w2_15`.
- Compare live fills and path quality against the pre-patch flat runs before
  changing queue composition again.
