"""Local sanity replay for the Round 1 high-ROI/threshold variant batch.

This is not an official Prosperity PnL calculator. It compares the current
control against selected high-ROI variants using immediate visible fills only.
Platform JSON `profit` remains the promotion score once real runs exist.
"""

from __future__ import annotations

import json
from pathlib import Path

from replay_five_bot_batch import PRODUCTS, ROOT, install_fake_datamodel, run_bot_day


CANONICAL_BOT_DIR = ROOT / "rounds" / "round_1" / "bots" / "noel" / "canonical"
HISTORICAL_BOT_DIR = ROOT / "rounds" / "round_1" / "bots" / "noel" / "historical"

BOT_CANDIDATES = (
    HISTORICAL_BOT_DIR / "candidate_10_bot02_carry_tight_mm.py",
    HISTORICAL_BOT_DIR / "candidate_24_v1_a1b1_size_skew_refine.py",
    HISTORICAL_BOT_DIR / "candidate_25_v2_a2b1_conservative_regime_gate.py",
    CANONICAL_BOT_DIR / "candidate_26_v3_a3b1_one_sided_exit_overlay.py",
    CANONICAL_BOT_DIR / "candidate_27_v1_c26_soft_flatten.py",
    CANONICAL_BOT_DIR / "candidate_28_v1_c26_strict_one_sided.py",
)


OUT_JSON = (
    Path(__file__).resolve().parents[0]
    / "run_20260417_high_roi_variant_replay_metrics.json"
)
OUT_MD = (
    Path(__file__).resolve().parents[0]
    / "run_20260417_high_roi_variant_replay_summary.md"
)


def high_roi_bot_paths() -> list[Path]:
    return [path for path in BOT_CANDIDATES if path.exists()]


def write_markdown(output: dict) -> str:
    lines = [
        "# High-ROI Threshold Variant Immediate-Fill Replay",
        "",
        "## Method",
        "",
        "- This is a local sanity replay, not official Prosperity PnL.",
        "- It models immediate fills against visible sample books only.",
        "- Resting orders that platform bots may hit later are not modeled.",
        "- Platform ranking must use JSON `profit` once platform artifacts exist.",
        "- This batch includes archived controls where current canonical files have already been narrowed.",
        "- Baseline bar: total `10007.0`, IPR `7286.0`, ACO `2721.0` from platform-style artifact analysis.",
        "",
        "## Ranking",
        "",
        "| Rank | Bot | Total Replay PnL | IPR Replay PnL | ACO Replay PnL | Rejections | Errors |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for idx, item in enumerate(output["ranking"], start=1):
        metrics = output["results"][item["bot"]]["totals"]
        rejections = sum(metrics["rejections"].values())
        lines.append(
            "| {} | `{}` | {:.2f} | {:.2f} | {:.2f} | {} | {} |".format(
                idx,
                item["bot"],
                metrics["total_pnl"],
                metrics["pnl_by_product"]["INTARIAN_PEPPER_ROOT"],
                metrics["pnl_by_product"]["ASH_COATED_OSMIUM"],
                rejections,
                metrics["errors"],
            )
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Use this replay only to catch contract, limit, or obvious immediate-fill issues.",
            "- Do not use this replay PnL scale for promotion.",
            "- Upload selected bots to Prosperity, save `.py` + `.json` + `.log`, then rerun `analyze_platform_artifacts.py`.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    install_fake_datamodel()
    bot_paths = high_roi_bot_paths()
    results = {}
    for bot_path in bot_paths:
        day_results = [run_bot_day(bot_path, day) for day in (-2, -1, 0)]
        totals = {
            "total_pnl": sum(day["total_pnl"] for day in day_results),
            "pnl_by_product": {
                product: sum(day["pnl_by_product"][product] for day in day_results)
                for product in PRODUCTS
            },
            "max_abs_position": {
                product: max(day["max_abs_position"][product] for day in day_results)
                for product in PRODUCTS
            },
            "order_count": {
                product: sum(day["order_count"][product] for day in day_results)
                for product in PRODUCTS
            },
            "fill_count": {
                product: sum(day["fill_count"][product] for day in day_results)
                for product in PRODUCTS
            },
            "filled_qty": {
                product: sum(day["filled_qty"][product] for day in day_results)
                for product in PRODUCTS
            },
            "rejections": {
                product: sum(day["rejections"][product] for day in day_results)
                for product in PRODUCTS
            },
            "errors": sum(day["errors"] for day in day_results),
        }
        results[bot_path.name] = {"days": day_results, "totals": totals}

    ordered = sorted(results.items(), key=lambda item: item[1]["totals"]["total_pnl"], reverse=True)
    output = {
        "method": "Immediate-fill replay against visible sample order books; passive future fills are not modeled.",
        "official_pnl_caveat": "Official ranking requires platform JSON `profit`; this is only a local sanity ranking.",
        "days": [-2, -1, 0],
        "ranking": [
            {"bot": name, "total_pnl": metrics["totals"]["total_pnl"]}
            for name, metrics in ordered
        ],
        "results": results,
    }
    OUT_JSON.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    OUT_MD.write_text(write_markdown(output))
    print(json.dumps(output["ranking"], indent=2))
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
