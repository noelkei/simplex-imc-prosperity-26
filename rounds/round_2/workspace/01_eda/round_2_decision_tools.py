#!/usr/bin/env python3
"""Round 2 scenario helpers for manual allocation and Market Access Fee.

This script uses only formulas and mechanics from the Round 2 wiki page.
It is a decision-support tool, not an official source of rules.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from typing import Iterable


BUDGET = 50_000.0


@dataclass(frozen=True)
class AllocationResult:
    research_pct: float
    scale_pct: float
    speed_pct: float
    speed_multiplier: float
    gross_pnl: float
    budget_used: float
    net_pnl: float


def research_outcome(percent: float) -> float:
    return 200_000.0 * math.log1p(percent) / math.log1p(100.0)


def scale_outcome(percent: float) -> float:
    return 7.0 * percent / 100.0


def manual_pnl(
    research_pct: float,
    scale_pct: float,
    speed_pct: float,
    speed_multiplier: float,
) -> AllocationResult:
    gross = research_outcome(research_pct) * scale_outcome(scale_pct) * speed_multiplier
    budget_used = BUDGET * (research_pct + scale_pct + speed_pct) / 100.0
    return AllocationResult(
        research_pct=research_pct,
        scale_pct=scale_pct,
        speed_pct=speed_pct,
        speed_multiplier=speed_multiplier,
        gross_pnl=gross,
        budget_used=budget_used,
        net_pnl=gross - budget_used,
    )


def parse_float_list(raw: str) -> list[float]:
    return [float(part.strip()) for part in raw.split(",") if part.strip()]


def percent_grid(step: float, max_percent: float = 100.0) -> Iterable[float]:
    value = 0.0
    while value <= max_percent + 1e-9:
        yield round(value, 10)
        value += step


def best_manual_for_fixed_speed(
    speed_pct: float,
    speed_multiplier: float,
    step: float,
) -> AllocationResult:
    best: AllocationResult | None = None
    remaining = 100.0 - speed_pct
    for research_pct in percent_grid(step, remaining):
        scale_max = remaining - research_pct
        for scale_pct in percent_grid(step, scale_max):
            result = manual_pnl(research_pct, scale_pct, speed_pct, speed_multiplier)
            if best is None or result.net_pnl > best.net_pnl:
                best = result
    if best is None:
        raise ValueError("No feasible allocation found")
    return best


def print_manual_grid(args: argparse.Namespace) -> None:
    speed_pcts = parse_float_list(args.speed_pcts)
    speed_multipliers = parse_float_list(args.speed_multipliers)

    print("| Speed pct | Speed multiplier | Research pct | Scale pct | Budget used | Gross PnL | Net PnL |")
    print("| ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for speed_pct in speed_pcts:
        if speed_pct < 0 or speed_pct > 100:
            raise ValueError(f"Speed pct out of range: {speed_pct}")
        for multiplier in speed_multipliers:
            result = best_manual_for_fixed_speed(speed_pct, multiplier, args.step)
            print(
                "| "
                f"{result.speed_pct:.2f} | "
                f"{result.speed_multiplier:.3f} | "
                f"{result.research_pct:.2f} | "
                f"{result.scale_pct:.2f} | "
                f"{result.budget_used:.2f} | "
                f"{result.gross_pnl:.2f} | "
                f"{result.net_pnl:.2f} |"
            )


def print_maf_grid(args: argparse.Namespace) -> None:
    incremental_pnls = parse_float_list(args.incremental_pnls)
    bids = parse_float_list(args.bids)
    accept_probs = parse_float_list(args.accept_probs)

    print("| Incremental full-access PnL | Bid | Acceptance probability | Expected value | Break-even? |")
    print("| ---: | ---: | ---: | ---: | --- |")
    for incremental_pnl in incremental_pnls:
        for bid in bids:
            for accept_prob in accept_probs:
                ev = accept_prob * (incremental_pnl - bid)
                breakeven = "yes" if bid <= incremental_pnl else "no"
                print(
                    "| "
                    f"{incremental_pnl:.2f} | "
                    f"{bid:.2f} | "
                    f"{accept_prob:.3f} | "
                    f"{ev:.2f} | "
                    f"{breakeven} |"
                )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    manual = subparsers.add_parser(
        "manual-grid",
        help="Grid-search best Research/Scale allocation for fixed Speed pct and assumed multiplier.",
    )
    manual.add_argument("--step", type=float, default=1.0, help="Percentage grid step.")
    manual.add_argument(
        "--speed-pcts",
        default="0,10,20,30,40,50,60,70,80,90",
        help="Comma-separated Speed percentage scenarios.",
    )
    manual.add_argument(
        "--speed-multipliers",
        default="0.1,0.3,0.5,0.7,0.9",
        help="Comma-separated rank-result multipliers to test.",
    )
    manual.set_defaults(func=print_manual_grid)

    maf = subparsers.add_parser(
        "maf-grid",
        help="Evaluate Market Access Fee scenarios from assumed incremental full-access PnL.",
    )
    maf.add_argument(
        "--incremental-pnls",
        default="500,1000,2500,5000,10000",
        help="Comma-separated expected incremental PnL values from full access.",
    )
    maf.add_argument(
        "--bids",
        default="100,250,500,1000,2500,5000,10000",
        help="Comma-separated bid values.",
    )
    maf.add_argument(
        "--accept-probs",
        default="0.25,0.5,0.75,1.0",
        help="Comma-separated assumed acceptance probabilities.",
    )
    maf.set_defaults(func=print_maf_grid)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if getattr(args, "step", 1.0) <= 0:
        raise ValueError("--step must be positive")
    args.func(args)


if __name__ == "__main__":
    main()
