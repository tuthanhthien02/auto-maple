"""Command-line interface for running the bot simulator."""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path

from src.common.logger import get_logger

from .bot_simulator import BotRunSimulator
from .descriptor import DescriptorRoutine

log = get_logger(__name__)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Offline simulator for Auto-Maple routines."
    )
    parser.add_argument(
        "--descriptor",
        required=True,
        type=Path,
        help="Path to descriptor CSV (e.g. resources/routines/luminous/tree_2_floor_descriptor.csv)",
    )
    parser.add_argument(
        "--loops",
        type=int,
        default=1,
        help="Number of loops to simulate (default: 1)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for deterministic runs.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("logs") / "simulations",
        help="Directory to write log and metrics output.",
    )
    return parser


def main(args: list[str] | None = None) -> None:
    parser = build_arg_parser()
    parsed = parser.parse_args(args)

    routine = DescriptorRoutine.from_csv(parsed.descriptor)
    simulator = BotRunSimulator(routine, random_seed=parsed.seed)
    result = simulator.run(max_loops=max(parsed.loops, 0))

    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    result.metadata["run_id"] = f"{routine.source_path.stem}_{timestamp}"

    log_path, metrics_path = result.write_to_directory(parsed.output_dir)
    log.info("Simulation complete: logs=%s metrics=%s", log_path, metrics_path)


if __name__ == "__main__":
    main()
