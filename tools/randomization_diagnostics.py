"""
Quick diagnostics for routine randomization behaviour.

Usage:
    python -m tools.randomization_diagnostics --routine resources/routines/example.csv --loops 10 --enable-skip --enable-pattern
"""

import argparse
import logging
import random
from collections import Counter, deque
from pathlib import Path
from types import SimpleNamespace

from src.common import config
from src.routine.routine import Routine


def _noop(*_, **__):
    return None


def _build_gui_stub():
    """Create a minimal GUI stub so Routine can operate without launching the real GUI."""
    details = SimpleNamespace(update_details=_noop, display_info=_noop)
    routine_view = SimpleNamespace(select=_noop)
    status = SimpleNamespace(set_routine=_noop)
    minimap = SimpleNamespace(draw_default=_noop)
    view = SimpleNamespace(
        details=details, routine=routine_view, status=status, minimap=minimap
    )
    edit = SimpleNamespace(minimap=minimap)
    return SimpleNamespace(
        set_routine=_noop, view=view, edit=edit, clear_routine_info=_noop
    )


def _setup_environment():
    """Prepare config state for headless diagnostics."""
    config.gui = _build_gui_stub()
    config.bot = SimpleNamespace(command_book={})
    config.enabled = True


def _maybe_enable_skip(routine: Routine, args):
    if args.enable_skip is not None:
        routine.skip_enabled = args.enable_skip
    if args.skip_probability is not None:
        routine.skip_probability = args.skip_probability


def _maybe_enable_pattern(routine: Routine, args):
    if args.enable_pattern is not None:
        routine.variant_enabled = args.enable_pattern
    if args.floor_variant_chance is not None:
        routine.floor_variant_chance = args.floor_variant_chance

    if routine.variant_enabled:
        routine.detect_floors()
        routine._build_variant_cycle()
        routine.index = routine._get_variant_start_index()


def _simulate(routine: Routine, steps: int):
    """Simulate routine execution without GUI to gather statistics."""
    stats = {
        "steps": 0,
        "skip_events": 0,
        "backward_events": 0,
        "variants": Counter(),
        "variant_transitions": deque(),
    }

    prev_loop_count = routine.loop_count
    prev_variant = routine.current_variant

    for _ in range(steps):
        stats["steps"] += 1

        should_backward, backward_steps = routine.should_backward()
        if should_backward:
            routine.apply_backward(backward_steps)
            stats["backward_events"] += 1

        skip_current = routine.should_skip_current_point()
        if skip_current:
            stats["skip_events"] += 1
            routine.is_skipping_context = True
            routine.step()
            continue

        routine.is_skipping_context = False
        routine.is_backwarding_context = False
        routine.step()

        if routine.loop_count > prev_loop_count:
            loops_delta = routine.loop_count - prev_loop_count
            stats["variants"][prev_variant] += loops_delta
            prev_loop_count = routine.loop_count

        if routine.current_variant != prev_variant:
            stats["variant_transitions"].append(
                (stats["steps"], prev_variant, routine.current_variant)
            )
            prev_variant = routine.current_variant

    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Routine randomization diagnostics (headless)."
    )
    parser.add_argument(
        "--routine", type=Path, required=True, help="Đường dẫn file routine (.csv)."
    )
    parser.add_argument(
        "--loops", type=int, default=10, help="Số vòng lặp muốn mô phỏng."
    )
    parser.add_argument(
        "--enable-skip",
        dest="enable_skip",
        action="store_true",
        help="Bật skip points.",
    )
    parser.add_argument(
        "--disable-skip",
        dest="enable_skip",
        action="store_false",
        help="Tắt skip points.",
    )
    parser.add_argument(
        "--skip-probability", type=float, help="Xác suất skip (0.0 - 1.0)."
    )
    parser.add_argument(
        "--enable-pattern",
        dest="enable_pattern",
        action="store_true",
        help="Bật pattern variants.",
    )
    parser.add_argument(
        "--disable-pattern",
        dest="enable_pattern",
        action="store_false",
        help="Tắt pattern variants.",
    )
    parser.add_argument(
        "--floor-variant-chance", type=float, help="Xác suất kích hoạt floor-only."
    )
    parser.add_argument("--seed", type=int, help="Seed cho random module để tái lập.")
    parser.add_argument("--verbose", action="store_true", help="In thêm log DEBUG.")
    parser.set_defaults(enable_skip=None, enable_pattern=None)
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(message)s",
    )

    if args.seed is not None:
        random.seed(args.seed)

    _setup_environment()

    routine_path = args.routine.resolve()
    if not routine_path.exists():
        raise FileNotFoundError(f"Routine không tồn tại: {routine_path}")

    routine = Routine()
    config.routine = routine
    routine.load(str(routine_path))

    _maybe_enable_skip(routine, args)
    _maybe_enable_pattern(routine, args)

    total_points = len(routine.sequence)
    if total_points == 0:
        logging.warning("Routine trống – không thể mô phỏng.")
        return

    steps = max(args.loops * total_points, total_points)
    stats = _simulate(routine, steps)

    print("\n===== RANDOMIZATION SUMMARY =====")
    print(f"Routine: {routine_path.name}")
    print(f"Tổng bước mô phỏng: {stats['steps']}")
    print(f"Skip events: {stats['skip_events']}")
    print(f"Backward events: {stats['backward_events']}")
    print(f"Variant hiện tại kết thúc: {routine.current_variant}")

    if stats["variants"]:
        print("\nSố loop ghi nhận theo variant:")
        for variant, count in stats["variants"].items():
            print(f"  - {variant}: {count}")
    else:
        print("\nKhông có loop nào hoàn thành trong quá trình mô phỏng.")

    if stats["variant_transitions"]:
        print("\nBiến thể chuyển đổi (step, từ -> tới):")
        for step_index, from_variant, to_variant in stats["variant_transitions"]:
            print(f"  - Step {step_index}: {from_variant} -> {to_variant}")
    else:
        print("\nKhông có chuyển đổi variant trong phạm vi mô phỏng.")


if __name__ == "__main__":
    main()
