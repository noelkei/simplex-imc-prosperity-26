# Top-Level Artifact Audit

Audit date: 2026-04-14
Cleanup status: completed. The top-level `bots/` and `performances/` folders were removed after audit approval. This inventory is historical only.

This audit covered legacy top-level `bots/` and `performances/` artifacts. Active execution artifacts now belong only under `rounds/round_X/`.

## Summary

- No top-level artifact should be treated as a source of Prosperity facts, API rules, product limits, or strategy correctness.
- No artifact below has a reliable visible link to a reviewed round-local strategy spec.
- No artifact below has a reliable visible target round in the new `rounds/round_X/` structure.
- Cleanup action: deleted top-level artifacts because no reliable round-local migration target was identified.

## Top-Level `bots/`

The action column records the pre-cleanup recommendation; all delete recommendations were executed.

| Artifact | Type | Current assessment | Recommended action |
| --- | --- | --- | --- |
| `bots/README.md` | guidance | Legacy/global guidance now superseded by round-local bot folders. | Delete with top-level folder after cleanup approval. |
| `bots/amin/README.md` | guidance | Empty/person-local legacy scaffold. | Delete after cleanup approval. |
| `bots/amin/canonical/.gitkeep` | placeholder | No active round value. | Delete after cleanup approval. |
| `bots/amin/historical/.gitkeep` | placeholder | No active round value. | Delete after cleanup approval. |
| `bots/bruno/README.md` | guidance | Person-local legacy scaffold. | Delete after cleanup approval. |
| `bots/bruno/canonical/.gitkeep` | placeholder | No active round value. | Delete after cleanup approval. |
| `bots/bruno/historical/.gitkeep` | placeholder | No active round value. | Delete after cleanup approval. |
| `bots/bruno/trader.py` | bot implementation | Legacy implementation with no visible round-local spec link. | Delete after approval unless a human identifies a target round and spec. |
| `bots/daniela/README.md` | guidance | Person-local legacy scaffold. | Delete after cleanup approval. |
| `bots/daniela/canonical/.gitkeep` | placeholder | No active round value. | Delete after cleanup approval. |
| `bots/daniela/historical/.gitkeep` | placeholder | No active round value. | Delete after cleanup approval. |
| `bots/daniela/historical/first_Try.py` | bot implementation | Legacy attempt with no visible round-local spec link. | Delete after approval unless a human identifies a target round and spec. |
| `bots/daniela/historical/second_try.py` | bot implementation | Legacy attempt with no visible round-local spec link. | Delete after approval unless a human identifies a target round and spec. |
| `bots/isaac/README.md` | guidance | Person-local legacy scaffold. | Delete after cleanup approval. |
| `bots/isaac/canonical/.gitkeep` | placeholder | No active round value. | Delete after cleanup approval. |
| `bots/isaac/historical/.gitkeep` | placeholder | No active round value. | Delete after cleanup approval. |
| `bots/isaac/historical/analyze_trading.py` | EDA script | Legacy script; not a reusable workflow tool and not round-local. | Delete after approval unless a human wants to preserve a non-authoritative example note. |
| `bots/isaac/historical/trader.py` | bot implementation | Legacy implementation with no visible round-local spec link. | Delete after approval unless a human identifies a target round and spec. |
| `bots/isaac/historical/output/*.png` | EDA outputs | Legacy plots; non-authoritative and not linked from a round EDA summary. | Delete after cleanup approval. |
| `bots/isaac/historical/output/*.csv` | EDA outputs | Legacy derived summaries; non-authoritative and not linked from a round EDA summary. | Delete after cleanup approval. |
| `bots/noel/README.md` | guidance | Empty/person-local legacy scaffold. | Delete after cleanup approval. |
| `bots/noel/canonical/.gitkeep` | placeholder | No active round value. | Delete after cleanup approval. |
| `bots/noel/historical/.gitkeep` | placeholder | No active round value. | Delete after cleanup approval. |

## Top-Level `performances/`

The action column records the pre-cleanup recommendation; all delete recommendations were executed.

| Artifact | Type | Current assessment | Recommended action |
| --- | --- | --- | --- |
| `performances/README.md` | guidance | Legacy/global guidance now superseded by round-local member-first performance folders. | Delete with top-level folder after cleanup approval. |
| `performances/amin/README.md` | guidance | Empty/person-local legacy scaffold. | Delete after cleanup approval. |
| `performances/amin/canonical/.gitkeep` | placeholder | No active round value. | Delete after cleanup approval. |
| `performances/amin/historical/.gitkeep` | placeholder | No active round value. | Delete after cleanup approval. |
| `performances/bruno/README.md` | guidance | Person-local legacy scaffold. | Delete after cleanup approval. |
| `performances/bruno/85156.json` | run artifact | Legacy run artifact with no visible round-local spec link. | Delete after approval unless a human identifies a target round and candidate. |
| `performances/bruno/85156.log` | raw log | Legacy raw log; durable evidence should be a round-local run summary. | Delete after approval unless a human identifies a target round and candidate. |
| `performances/bruno/canonical/.gitkeep` | placeholder | No active round value. | Delete after cleanup approval. |
| `performances/bruno/historical/.gitkeep` | placeholder | No active round value. | Delete after cleanup approval. |
| `performances/daniela/README.md` | guidance | Empty/person-local legacy scaffold. | Delete after cleanup approval. |
| `performances/daniela/canonical/.gitkeep` | placeholder | No active round value. | Delete after cleanup approval. |
| `performances/daniela/historical/.gitkeep` | placeholder | No active round value. | Delete after cleanup approval. |
| `performances/isaac/README.md` | guidance | Empty/person-local legacy scaffold. | Delete after cleanup approval. |
| `performances/isaac/canonical/.gitkeep` | placeholder | No active round value. | Delete after cleanup approval. |
| `performances/isaac/historical/.gitkeep` | placeholder | No active round value. | Delete after cleanup approval. |
| `performances/noel/README.md` | guidance | Empty/person-local legacy scaffold. | Delete after cleanup approval. |
| `performances/noel/canonical/.gitkeep` | placeholder | No active round value. | Delete after cleanup approval. |
| `performances/noel/historical/.gitkeep` | placeholder | No active round value. | Delete after cleanup approval. |

## Cleanup Result

Top-level artifacts were removed. Do not recreate top-level execution folders; use `rounds/round_X/bots/<member>/` and `rounds/round_X/performances/<member>/` for all future round work.
