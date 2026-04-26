# Learning Batch Wave 1 Manifest

Generated from `generate_learning_batch_wave1.py`.

| Bot ID | File | Family | Hypothesis |
| --- | --- | --- | --- |
| `L01` | `../bots/amin/canonical/probe_l01_hydro_reversion.py` | delta1 reversion | HYDRO still has a tradable reversion signal if we isolate it from composite noise. |
| `L02` | `../bots/amin/canonical/probe_l02_hydro_imbalance.py` | delta1 imbalance | HYDRO may be better captured by imbalance than by pure mid reversion. |
| `L04` | `../bots/amin/canonical/probe_l04_vex_reversion.py` | delta1 reversion | VEX should remain one of the cleanest standalone learners on the live day. |
| `L05` | `../bots/amin/canonical/probe_l05_vex_imbalance.py` | delta1 imbalance | VEX imbalance may carry most of the live delta-1 edge by itself. |
| `L06` | `../bots/amin/canonical/probe_l06_delta1_dual_independent.py` | delta1 dual combo | HYDRO and VEX should still add mostly independently when run as a clean dual delta-1 stack. |
| `L07` | `../bots/amin/canonical/probe_l07_itm_4000_residual.py` | itm residual | VEV_4000 should be one of the cleanest live residual learners. |
| `L08` | `../bots/amin/canonical/probe_l08_itm_4500_residual.py` | itm residual | VEV_4500 should be the second clean ITM residual learner. |
| `L09` | `../bots/amin/canonical/probe_l09_itm_pair_residual.py` | itm residual pair | The ITM edge should survive as a small pair, not just strike by strike. |
| `L10` | `../bots/amin/canonical/probe_l10_itm_pair_plus_vex.py` | itm residual plus vex | A cleaner VEX plus ITM stack should reproduce the best historical family more faithfully. |
| `L12` | `../bots/amin/canonical/probe_l12_active_5000_residual.py` | active residual | VEV_5000 may still have some standalone residual edge despite weak composite behavior. |
| `L13` | `../bots/amin/canonical/probe_l13_active_5100_residual.py` | active residual | VEV_5100 needs isolation before we can prune or rescue it. |
| `L14` | `../bots/amin/canonical/probe_l14_active_5200_residual.py` | active residual | VEV_5200 must be isolated to confirm whether it is a true reject or only a basket interaction problem. |
| `L15` | `../bots/amin/canonical/probe_l15_active_5300_residual.py` | active residual | VEV_5300 is the best active strike and deserves a direct standalone learner. |
| `L16` | `../bots/amin/canonical/probe_l16_active_5000_5300_residual.py` | active residual subset | The cleanest active subset may be the outer pair 5000 plus 5300. |
| `L17` | `../bots/amin/canonical/probe_l17_active_5100_5300_residual.py` | active residual subset | 5100 may work only in the presence of 5300 rather than alone or in the full basket. |
| `L18` | `../bots/amin/canonical/probe_l18_active_5200_5300_residual.py` | active residual subset | If 5200 only works next to 5300, we should see it here before restoring it more broadly. |
| `L19` | `../bots/amin/canonical/probe_l19_active_5000_5100_5300_residual.py` | active residual subset | The right active basket may simply be the current family without VEV_5200. |
| `L20` | `../bots/amin/canonical/probe_l20_active_5000_5300_inventory.py` | active residual inventory subset | Inventory skew should only be judged after removing the known toxic middle strikes. |
| `L21` | `../bots/amin/canonical/probe_l21_upper_5400_residual.py` | upper residual | VEV_5400 now deserves a direct live learner because the logger showed movement plus tight spreads. |
| `L22` | `../bots/amin/canonical/probe_l22_upper_5500_residual.py` | upper residual | VEV_5500 is the highest-ROI reopened upper-strike probe because spreads are exceptionally tight. |
| `L23` | `../bots/amin/canonical/probe_l23_upper_5400_5500_residual.py` | upper residual pair | The upper branch may work better as a small pair than as a single-strike probe. |
| `L24` | `../bots/amin/canonical/probe_l24_upper_5400_5500_passive.py` | upper passive maker | The upper branch may simply need passive spread capture rather than directional residual trading. |
| `L25` | `../bots/amin/canonical/probe_l25_vex_plus_5300.py` | vex plus active best strike | A clean VEX plus 5300 combo may be the best near-term active learner. |
| `L26` | `../bots/amin/canonical/probe_l26_surface_5200_5300_relval.py` | surface relative value | The current active failure may be better explained by the 5200/5300 local surface relationship than by absolute residual alone. |
| `L27` | `../bots/amin/canonical/probe_l27_surface_5300_5400_relval.py` | surface relative value | The upper transition around 5300/5400 may be cleaner than the broader active basket. |
