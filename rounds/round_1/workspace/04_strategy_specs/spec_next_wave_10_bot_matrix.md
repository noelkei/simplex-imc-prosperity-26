# Spec: Next-Wave 10 Bot Matrix

## Status

APPROVED_WITH_CAVEATS

## Review

- Reviewer: user request, 2026-04-17
- Review outcome: approved with caveats
- Caveat: these are exploration bots; promotion still requires platform JSON/log evidence and `activitiesLog` PnL split.

## Source Candidates

- Strategy branches: `../03_strategy_next_wave_branches.md`
- Platform artifact analysis: `../../../performances/noel/canonical/run_20260417_platform_artifact_analysis.md`
- Current baseline bot: `../../../bots/noel/canonical/candidate_10_bot02_carry_tight_mm.py`

## Common Rules

- Products: `INTARIAN_PEPPER_ROOT`, `ASH_COATED_OSMIUM`.
- Limits: `+/-80` per product.
- Interface: implement only `Trader.run(state)` and return `result, conversions, traderData`.
- Imports: standard library only plus `datamodel`.
- IPR baseline: reach and hold `+80` as early as possible unless the candidate explicitly tests IPR execution.
- ACO baseline: fixed FV around `10000`, with each bot changing one conceptual ACO module.
- Capacity: aggregate buy and sell order quantities must be clipped against position-limit capacity.
- State: `traderData` may store small JSON state for filters/posteriors; keep it compact.

## Bot Matrix

| Candidate | Bot File | IPR Module | ACO Module | Main Question |
| --- | --- | --- | --- | --- |
| `candidate_14_aco_kalman_latent_fv` | `candidate_14_aco_kalman_latent_fv.py` | +80 carry | conservative Kalman latent FV | can a latent FV filter improve quote trust? |
| `candidate_15_aco_hmm_regime_mm` | `candidate_15_aco_hmm_regime_mm.py` | +80 carry | 3-state HMM-like regime posterior | can hidden regimes improve mean-reversion timing? |
| `candidate_16_aco_edge_quality_gate` | `candidate_16_aco_edge_quality_gate.py` | +80 carry | contextual edge gate | can fewer cleaner fills beat raw volume? |
| `candidate_17_aco_inventory_lifecycle` | `candidate_17_aco_inventory_lifecycle.py` | +80 carry | late flatten / target inventory lifecycle | does planned inventory decay improve ACO? |
| `candidate_18_aco_offline_policy_table` | `candidate_18_aco_offline_policy_table.py` | +80 carry | residual x inventory policy table | can an interpretable action table beat hand skew? |
| `candidate_19_ipr_execution_upgrade` | `candidate_19_ipr_execution_upgrade.py` | guarded/frontloaded +80 carry | baseline tight ACO | can IPR execution improve without hurting ACO? |
| `candidate_20_dual_product_risk_scheduler` | `candidate_20_dual_product_risk_scheduler.py` | +80 carry | barbell high-quality ACO | can total-score protection avoid ACO drag? |
| `candidate_21_one_sided_book_specialist` | `candidate_21_one_sided_book_specialist.py` | +80 carry | one-sided book specialist | can one-sided states help exits/provision? |
| `candidate_22_micro_alpha_rescue` | `candidate_22_micro_alpha_rescue.py` | +80 carry | imbalance/spread micro overlay | can microstructure help as overlay only? |
| `candidate_23_adaptive_aco_controller` | `candidate_23_adaptive_aco_controller.py` | +80 carry | conservative multi-signal controller | can a controller combine filters safely? |

## Validation Plan

1. Static compile every bot.
2. Run local immediate-fill replay as a sanity/ranking heuristic only.
3. Upload selected bots to Prosperity, preserving `.py`, `.json`, and `.log` together.
4. Rerun `analyze_platform_artifacts.py`.
5. Rank official results by platform JSON `profit`, then attribute by final `activitiesLog` product PnL.

## Promotion Bar

- Current total: `10007.0`.
- Current IPR PnL: `7286.0`.
- Current ACO PnL: `2721.0`.
- Preferred improvement: increase ACO without reducing IPR `+80`.
