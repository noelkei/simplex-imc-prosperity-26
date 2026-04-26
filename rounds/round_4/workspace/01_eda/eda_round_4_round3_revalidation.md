# Round 4 EDA Annex - Round 3 Carry-Forward Revalidation

## Purpose

This annex checks which `round_3` carry-forward principles survive contact with
`round_4` raw data.

It does not try to prove run-quality conclusions from raw data alone.
It only decides whether the old framing still deserves trust at EDA level.

Primary sources:

- `../00_prior_round_intake.md`
- `../../round_3/workspace/01_eda/eda_round_3_retrospective_carry_forward.md`
- `../../round_3/workspace/06_testing/round_3_closeout_retrospective.md`
- current `round_4` processed Phase 01 outputs

## Revalidation Table

| Carry-forward from `round_3` | Round 4 raw-data verdict | Basis |
| --- | --- | --- |
| `delta-1 first` as default clean base | `still plausible but not yet validated as a final strategy claim` | `HYDRO` and `VEX` remain the cleanest liquid products, but raw data alone cannot prove champion status |
| `VEX` as likely anchor/context | `supported by round_4 raw data` | strongest same-time linkage to the voucher family, lowest major spread, no delayed-follow evidence |
| `5000/5100/5200/5300` are not homogeneous | `supported by round_4 raw data` | spreads, trade counts, concentration, and trade alignment differ sharply across the cluster |
| `5100/5200` may be better as danger-state inputs than default inventory | `still plausible but not yet validated` | `5100` tape is too sparse; `5200` is concentrated and looks weak short-horizon, but raw data alone cannot fully decide inventory vs signal-only |
| `5300` deserves special handling | `supported by round_4 raw data` | meaningful trade count, distinct concentration structure, much higher spread than `5200`, and special-case alignment behavior |
| late-session deterioration and no-trade logic matter | `still plausible but not yet validated` | top names trade all day, so there is no universal timing collapse, but upper-strike friction worsens later |
| family-level framing matters more than symbol-only framing | `supported by round_4 raw data` | role-conditioned spread, concentration, and linkage structure are more informative than isolated symbol views |

## What Survived Cleanly

These `round_3` lessons should now be treated as live carry-forward principles
for `round_4` understanding:

- use role-first framing
- use `VEX` as the primary option-book anchor candidate
- keep `HYDRO` structurally separate from the voucher family
- avoid homogeneous treatment of the active voucher basket
- keep family-level and cross-strike views first-class

## What Survived Only Partially

These are not dead, but they need validation rather than blind reuse:

- `delta-1 first` as actual champion architecture
- `5100/5200` as pure signal-only strikes
- late-session deterioration as a universal rule
- `5300` as a tradable rescue candidate rather than only a structural curiosity

## What Round 4 Already Weakens

- any claim that raw time-of-day alone proves toxic late-session behavior
- any claim that visible counterparties automatically create strong standalone alpha

## What Round 4 Already Reinforces

- do not reopen the broad `5000/5100/5200/5300` basket by default
- do not treat vouchers as independent delta-1 symbols
- do not promote `round_3` winners directly into `round_4` without counterparty-aware revalidation

## Downstream Use

- Understanding:
  split carry-forwards into `supported`, `partially supported`, and `still only hypotheses`.
- Strategy:
  use the supported items as framing; use the partial items as explicit test candidates.
- Spec:
  require any `buyer` / `seller` use to state which prior-round assumption it is modifying.
