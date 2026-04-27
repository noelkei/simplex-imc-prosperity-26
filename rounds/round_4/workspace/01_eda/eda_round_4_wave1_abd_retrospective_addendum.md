# Retrospective EDA Addendum: Wave 1 Packs A, B, D

## Status

`READY_FOR_REVIEW`

## Scope

- Round: `round_4`
- Source runs:
  - `r4_s01`, `r4_s02`
  - `r4_s03`, `r4_s13`, `r4_s15`
  - `r4_s05`, `r4_s06`, `r4_s10`
- Why retrospective EDA is needed: meaningful run evidence changed product-role interpretation and exposed a concrete late-session retention / veto question that should not live only in testing artifacts
- Downstream decision impacted: the next `Phase 03` candidate shortlist and `Phase 04` mini-wave specs

## Product / Role Review

| Product Or Scope | Role Class | Interaction Class | Evidence From Runs | Downstream Implication |
| --- | --- | --- | --- | --- |
| `VELVETFRUIT_EXTRACT` | base / anchor | standalone usable | all live A/B/D branches reduced to `VEX` timing decisions | keep central in Wave 2 |
| `HYDROGEL_PACK` | base | standalone usable but weak | `r4_s02` never engaged | remove from the next mini-wave |
| `VEV_4000` | structural overlay | usable only with anchor | zero direct `VEV_4000` fills in all Pack B runs | treat as untested, not validated or disproven |
| `VEV_5200` | monitor / floor | mainly veto / anti-signal | `r4_s10` improved final path by skipping the late `VEX` extension | reuse as signal-only context |

## Cross-Product / Cross-Strike Context

| Relationship | Evidence | What It Suggests | Strategy Impact | Caveat |
| --- | --- | --- | --- | --- |
| `VEX` base versus `HYDRO` base | `r4_s01` traded; `r4_s02` did not | base selection should stay `VEX`-first | remove standalone `HYDRO` from the next batch | partial evidence from one day |
| `VEX` plus direct `4000` overlay | `r4_s03` matched `r4_s01` exactly and `r4_s13` / `r4_s15` never traded `4000` | current Pack B design does not produce a real `4000` test | simplify or prune Pack B | lack of direct `4000` fills limits the verdict |
| `VEX` path versus `5200/5300` danger-state prints | `r4_s10` skipped the `99400` `VEX` sell after `98900` `VEV_5200` and `VEV_5300` `Mark 22` seller activity | toxic-family state is more useful as veto than as direct inventory thesis | spec a veto overlay, not a standalone defensive bot | signal still needs validation on a stronger parent branch |

## Family Exposure / Book-Level Findings

- Family-level exposure issue: the differentiated Pack B and D branches often changed only the final `VEX` inventory path rather than expressing their intended family thesis directly.
- Products that amplify giveback: late `VEX` short extensions after the `86600` local peak.
- Products that behave more like signal than inventory: `VEV_5200`.

## Timing / Churn Findings

| Finding | Evidence | Downstream Use |
| --- | --- | --- |
| late-session giveback dominates the active base path | `r4_s01` and `r4_s06` both ended far below earlier peaks | retention should be a direct Wave 2 axis |
| composite hard gating destroys test cleanliness | `r4_s05` and `r4_s15` produced zero own trades | break future protective ideas into lighter one-axis overlays |
| the useful contextual signal is close to the final decision window | `98900` toxic-family prints preceded the `99400` extra sell that `r4_s10` avoided | late veto or cooldown logic deserves explicit spec treatment |

## Carry-Forward Implications

- Promote into understanding:
  - `VEX` remains the primary anchor
  - `5200` should be framed as monitor / veto first
- Promote into strategy framing:
  - keep the next batch small and retention-focused
  - do not treat Pack B as a dead `4000` idea; treat it as an unclean test
- Keep as EDA-only caution:
  - base-leg PnL can hide whether an overlay ever actually traded
- Needs fresh current-round validation:
  - any direct `4000` overlay
  - any `5200` veto when attached to a stronger active family

## Negative Evidence

| Idea | Evidence Against | Reopen Only If |
| --- | --- | --- |
| standalone `HYDRO` control | `r4_s02` never engaged | new linked-product role appears |
| hard whole-bot danger veto | `r4_s05`, `r4_s15` | a lighter overlay shows real edge |
| "Pack B already tested `4000`" | all three Pack B runs lacked direct `VEV_4000` fills | direct `4000` attribution is visible |

## Linked Artifacts

- Synthesis: `../06_testing/round_4_wave1_pack_abd_partial_synthesis.md`
- Run summaries:
  - `../../performances/noel/canonical/run_20260427_1900_r4_s01_vex_base_control.md`
  - `../../performances/noel/canonical/run_20260427_1910_r4_s10_5200_signal_only_veto.md`
- Post-run memory: `../post_run_research_memory.md`
- Next action: reopen `Phase 03` and `Phase 04` with one retention branch, one `5200` veto overlay branch, and at most one simplified `4000` re-test
