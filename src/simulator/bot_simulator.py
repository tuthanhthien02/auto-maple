"""Offline simulator that replays descriptor routines and emits synthetic logs."""

from __future__ import annotations

import json
import math
import random
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from statistics import mean, pstdev
from typing import Dict, List, Optional, Sequence, Tuple

from src.common.logger import get_logger

from .descriptor import (
    DescriptorCommand,
    DescriptorRoutine,
    JumpInstruction,
    PointInstruction,
)

log = get_logger(__name__)


@dataclass
class SimulationLogEntry:
    timestamp: float
    event: str
    instruction_index: int
    label: Optional[str]
    details: Dict[str, object] = field(default_factory=dict)

    def as_dict(self) -> Dict[str, object]:
        payload = {
            "timestamp_sim": round(self.timestamp, 4),
            "event": self.event,
            "instruction_index": self.instruction_index,
        }
        if self.label:
            payload["label"] = self.label
        if self.details:
            payload["details"] = self.details
        return payload


@dataclass
class MetricsSummary:
    loops_completed: int
    total_time: float
    point_distances: List[float] = field(default_factory=list)
    wait_durations: List[float] = field(default_factory=list)
    direction_changes: int = 0
    teleport_counts: Counter = field(default_factory=Counter)
    command_counts: Counter = field(default_factory=Counter)
    loop_durations: List[float] = field(default_factory=list)
    flags: List[str] = field(default_factory=list)
    score: float = 0.0
    human_like: bool = False

    def as_dict(self) -> Dict[str, object]:
        wait_stats = self._build_wait_stats()
        distance_stats = self._build_distance_stats()

        return {
            "loops_completed": self.loops_completed,
            "total_time": round(self.total_time, 4),
            "wait_random": wait_stats,
            "movement_distances": distance_stats,
            "direction_changes": self.direction_changes,
            "teleport_counts": dict(self.teleport_counts),
            "command_counts": dict(self.command_counts),
            "loop_durations": [round(v, 4) for v in self.loop_durations],
            "analysis": {
                "is_human_like": self.human_like,
                "score": round(self.score, 3),
                "flags": self.flags,
            },
        }

    def _build_wait_stats(self) -> Dict[str, object]:
        if not self.wait_durations:
            return {"count": 0}
        avg = mean(self.wait_durations)
        std = pstdev(self.wait_durations) if len(self.wait_durations) > 1 else 0.0
        return {
            "count": len(self.wait_durations),
            "mean": round(avg, 4),
            "stdev": round(std, 4),
            "cv": round(std / avg, 4) if avg else 0.0,
            "min": round(min(self.wait_durations), 4),
            "max": round(max(self.wait_durations), 4),
        }

    def _build_distance_stats(self) -> Dict[str, object]:
        if not self.point_distances:
            return {"count": 0}
        avg = mean(self.point_distances)
        std = pstdev(self.point_distances) if len(self.point_distances) > 1 else 0.0
        return {
            "count": len(self.point_distances),
            "mean": round(avg, 4),
            "stdev": round(std, 4),
            "min": round(min(self.point_distances), 4),
            "max": round(max(self.point_distances), 4),
        }


@dataclass
class SimulationResult:
    logs: List[SimulationLogEntry]
    metrics: MetricsSummary
    routine: DescriptorRoutine
    metadata: Dict[str, object] = field(default_factory=dict)

    def write_to_directory(self, output_dir: Path) -> Tuple[Path, Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        base_name = self.metadata.get("run_id", "simulation")
        log_path = output_dir / f"{base_name}.jsonl"
        metrics_path = output_dir / f"{base_name}_metrics.json"

        with log_path.open("w", encoding="utf-8") as handle:
            for entry in self.logs:
                handle.write(json.dumps(entry.as_dict(), ensure_ascii=False) + "\n")

        with metrics_path.open("w", encoding="utf-8") as handle:
            json.dump(self.metrics.as_dict(), handle, ensure_ascii=False, indent=2)

        return log_path, metrics_path


@dataclass
class BotState:
    time: float = 0.0
    position: Optional[Tuple[float, float]] = None
    facing: str = "right"
    loop_count: int = 0
    loop_start_time: float = 0.0
    pending_jump_counts: Dict[int, int] = field(default_factory=dict)


class MetricsCollector:
    def __init__(self) -> None:
        self.point_distances: List[float] = []
        self.wait_durations: List[float] = []
        self.direction_changes: int = 0
        self.teleport_counts: Counter = Counter()
        self.command_counts: Counter = Counter()
        self.loop_durations: List[float] = []

    def record_distance(self, distance: float) -> None:
        self.point_distances.append(distance)

    def record_wait(self, duration: float) -> None:
        self.wait_durations.append(duration)

    def record_direction_change(self) -> None:
        self.direction_changes += 1

    def record_teleport(self, direction: str, steps: int) -> None:
        key = f"{direction}:{steps}"
        self.teleport_counts[key] += 1

    def record_command(self, name: str) -> None:
        self.command_counts[name] += 1

    def record_loop(self, duration: float) -> None:
        self.loop_durations.append(duration)


class BotRunSimulator:
    """Simulate command execution for a descriptor routine."""

    def __init__(
        self,
        routine: DescriptorRoutine,
        *,
        random_seed: Optional[int] = None,
    ) -> None:
        self.routine = routine
        self.random = random.Random(random_seed)
        self._seed = random_seed
        self.state = BotState()
        self.metrics = MetricsCollector()
        self.logs: List[SimulationLogEntry] = []
        self._event_counter = 0
        self._start_label = (
            routine.infer_loop_start_label() or routine.primary_start_label()
        )

    def run(
        self, *, max_loops: int = 1, max_iterations: int | None = None
    ) -> SimulationResult:
        instructions = self.routine.instructions
        if not instructions:
            raise ValueError("Routine contains no instructions")

        iteration_budget = max_iterations or max(
            1000, len(instructions) * max(1, max_loops) * 5
        )

        ip = 0
        iterations = 0
        while ip < len(instructions):
            if iterations >= iteration_budget:
                log.warning(
                    "Simulation aborted: exceeded iteration budget (%s). "
                    "Consider increasing max_iterations.",
                    iteration_budget,
                )
                break

            if max_loops and self.state.loop_count >= max_loops:
                break

            instruction = instructions[ip]
            if isinstance(instruction, PointInstruction):
                self._execute_point(instruction, ip)
                ip += 1
            elif isinstance(instruction, JumpInstruction):
                jump_target = self._execute_jump(instruction, ip)
                ip = jump_target if jump_target is not None else ip + 1
            else:
                ip += 1

            iterations += 1

        metrics_summary = self._build_metrics_summary()

        source_stem = (
            self.routine.source_path.stem if self.routine.source_path else "routine"
        )
        seed_part = f"seed{self._seed}" if self._seed is not None else "seedNA"
        metadata = {
            "run_id": f"{source_stem}_{seed_part}",
            "loops_requested": max_loops,
            "iterations": iterations,
        }

        return SimulationResult(
            logs=self.logs,
            metrics=metrics_summary,
            routine=self.routine,
            metadata=metadata,
        )

    # ----------------------------
    # Execution helpers
    # ----------------------------
    def _execute_point(self, point: PointInstruction, index: int) -> None:
        prev_position = self.state.position
        target_position = (point.x, point.y)

        travel_distance = 0.0
        if prev_position is not None:
            travel_distance = distance(prev_position, target_position)

        travel_duration = self._movement_duration(travel_distance)
        if travel_duration:
            self._advance_time(travel_duration)

        self.state.position = target_position
        self.metrics.record_distance(travel_distance)

        self._record_event(
            event="point_reached",
            instruction_index=index,
            label=point.primary_label(),
            details={
                "position": {"x": point.x, "y": point.y},
                "travel_distance": round(travel_distance, 4),
                "travel_duration": round(travel_duration, 4),
                "labels": point.labels,
                "adjust": point.adjust,
                "comments": point.comments,
            },
        )

        if point.adjust:
            adjust_duration = self._command_base_duration("adjust")
            self._advance_time(adjust_duration)
            self.metrics.record_command("adjust")
            self._record_event(
                event="adjust",
                instruction_index=index,
                label=point.primary_label(),
                details={"duration": round(adjust_duration, 4)},
            )

        for command in point.commands:
            self._execute_command(command, index, point.primary_label())

    def _execute_jump(self, jump: JumpInstruction, index: int) -> Optional[int]:
        jump_duration = self._command_base_duration("jump")
        self._advance_time(jump_duration)
        self.metrics.record_command("Jump")

        should_jump = True
        if jump.frequency > 1:
            count = self.state.pending_jump_counts.get(index, 0) + 1
            if count >= jump.frequency:
                self.state.pending_jump_counts[index] = 0
                should_jump = True
            else:
                self.state.pending_jump_counts[index] = count
                should_jump = False

        target_index = self.routine.labels.get(jump.target)
        self._record_event(
            event="jump",
            instruction_index=index,
            label=jump.target,
            details={
                "duration": round(jump_duration, 4),
                "frequency": jump.frequency,
                "effective_jump": should_jump and (target_index is not None),
                "target_index": target_index,
            },
        )

        if not should_jump or target_index is None:
            return None

        if self._start_label and jump.target == self._start_label:
            loop_duration = self.state.time - self.state.loop_start_time
            if loop_duration > 0:
                self.metrics.record_loop(loop_duration)
            self.state.loop_start_time = self.state.time
            self.state.loop_count += 1

        return target_index

    def _execute_command(
        self, command: DescriptorCommand, instruction_index: int, label: Optional[str]
    ) -> None:
        name = command.name.lower()
        self.metrics.record_command(command.name)

        if name == "wait_random":
            duration = self._wait_random_duration(command.args)
            self.metrics.record_wait(duration)
            self._advance_time(duration)
            self._record_event(
                event="wait_random",
                instruction_index=instruction_index,
                label=label,
                details={
                    "duration": round(duration, 4),
                    "args": command.args,
                },
            )
            return

        if name == "teleport":
            direction, steps = self._parse_direction_steps(command.args)
            duration = self._command_base_duration("teleport") * max(1, steps)
            self._advance_time(duration)
            self.metrics.record_teleport(direction, steps)
            self._update_position_by_direction(direction, steps, scale=0.06)
            self._record_event(
                event="teleport",
                instruction_index=instruction_index,
                label=label,
                details={
                    "direction": direction,
                    "steps": steps,
                    "duration": round(duration, 4),
                    "position_after": self._position_dict(),
                },
            )
            return

        if name in {"jump_down", "jump_teleport_up"}:
            direction = "down" if name == "jump_down" else "up"
            duration = self._command_base_duration(name)
            self._advance_time(duration)
            self._update_position_by_direction(direction, 1, scale=0.09)
            self._record_event(
                event=name,
                instruction_index=instruction_index,
                label=label,
                details={
                    "duration": round(duration, 4),
                    "position_after": self._position_dict(),
                },
            )
            return

        if name in {"face_left", "face_right"}:
            new_direction = "left" if name == "face_left" else "right"
            if self.state.facing != new_direction:
                self.metrics.record_direction_change()
                self.state.facing = new_direction
            duration = self._command_base_duration("face")
            self._advance_time(duration)
            self._record_event(
                event=name,
                instruction_index=instruction_index,
                label=label,
                details={"duration": round(duration, 4)},
            )
            return

        duration = self._command_base_duration(command.name)
        self._advance_time(duration)
        self._record_event(
            event=command.name,
            instruction_index=instruction_index,
            label=label,
            details={
                "duration": round(duration, 4),
                "args": command.args,
            },
        )

    def _advance_time(self, delta: float) -> None:
        self.state.time = max(0.0, self.state.time + max(0.0, delta))

    def _movement_duration(self, distance_travelled: float) -> float:
        if distance_travelled <= 0:
            return 0.0
        base_speed = 1.8  # arbitrary speed units per second
        duration = distance_travelled / base_speed
        jitter = self.random.uniform(-0.05, 0.08)
        return max(0.05, duration + jitter)

    def _command_base_duration(self, name: str) -> float:
        normalized = name.lower()
        base = COMMAND_BASE_DURATIONS.get(normalized, COMMAND_BASE_DURATIONS["default"])
        jitter_range = COMMAND_JITTER.get(normalized, COMMAND_JITTER["default"])
        jitter = self.random.uniform(*jitter_range)
        return max(0.01, base + jitter)

    def _wait_random_duration(self, args: Sequence[str]) -> float:
        if len(args) < 2:
            raise ValueError(
                f"wait_random requires min and max arguments, received: {args}"
            )
        try:
            low = float(args[0])
            high = float(args[1])
        except ValueError as exc:
            raise ValueError(f"Invalid wait_random arguments: {args}") from exc
        if high < low:
            low, high = high, low
        return self.random.uniform(low, high)

    def _parse_direction_steps(self, args: Sequence[str]) -> Tuple[str, int]:
        if not args:
            raise ValueError("teleport requires direction argument")
        direction = args[0].lower()
        steps = 1
        if len(args) >= 2:
            try:
                steps = max(1, int(args[1]))
            except ValueError as exc:
                raise ValueError(f"Invalid teleport step count: {args[1]}") from exc
        return direction, steps

    def _update_position_by_direction(
        self, direction: str, steps: int, *, scale: float
    ) -> None:
        if self.state.position is None:
            return
        x, y = self.state.position
        delta = scale * steps
        if direction == "right":
            x += delta
        elif direction == "left":
            x -= delta
        elif direction == "up":
            y -= delta
        elif direction == "down":
            y += delta
        self.state.position = (clamp(x, 0.0, 1.0), clamp(y, 0.0, 1.0))

    def _position_dict(self) -> Dict[str, float]:
        if self.state.position is None:
            return {"x": None, "y": None}
        x, y = self.state.position
        return {"x": round(x, 4), "y": round(y, 4)}

    def _record_event(
        self,
        *,
        event: str,
        instruction_index: int,
        label: Optional[str],
        details: Dict[str, object],
    ) -> None:
        self._event_counter += 1
        entry = SimulationLogEntry(
            timestamp=self.state.time,
            event=event,
            instruction_index=instruction_index,
            label=label,
            details=details,
        )
        self.logs.append(entry)

    def _build_metrics_summary(self) -> MetricsSummary:
        summary = MetricsSummary(
            loops_completed=self.state.loop_count,
            total_time=self.state.time,
            point_distances=self.metrics.point_distances,
            wait_durations=self.metrics.wait_durations,
            direction_changes=self.metrics.direction_changes,
            teleport_counts=self.metrics.teleport_counts,
            command_counts=self.metrics.command_counts,
            loop_durations=self.metrics.loop_durations,
        )
        flags, score = evaluate_human_like(
            summary, loops_expected=self.state.loop_count
        )
        summary.flags = flags
        summary.score = score
        summary.human_like = not flags
        return summary


# ----------------------------
# Metrics evaluation helpers
# ----------------------------
def evaluate_human_like(
    metrics: MetricsSummary, *, loops_expected: int
) -> Tuple[List[str], float]:
    flags: List[str] = []
    score_components: List[float] = []

    wait_stats = metrics._build_wait_stats()
    if wait_stats["count"] == 0:
        flags.append("missing_wait_random")
        score_components.append(0.0)
    else:
        cv = wait_stats.get("cv", 0.0)
        if cv < 0.2:
            flags.append("low_wait_variance")
            score_components.append(0.2 + cv)
        else:
            score_components.append(min(1.0, 0.6 + cv))

    if loops_expected and len(metrics.loop_durations) < loops_expected:
        flags.append("incomplete_loops")
        score_components.append(0.2)
    elif metrics.loop_durations:
        loop_std = (
            pstdev(metrics.loop_durations) if len(metrics.loop_durations) > 1 else 0.0
        )
        loop_cv = (
            loop_std / mean(metrics.loop_durations)
            if mean(metrics.loop_durations)
            else 0.0
        )
        score_components.append(0.5 + min(loop_cv, 0.5))

    if metrics.direction_changes == 0:
        flags.append("no_direction_changes")
        score_components.append(0.1)
    else:
        score_components.append(min(1.0, 0.4 + metrics.direction_changes * 0.15))

    teleport_penalty = sum(
        count for key, count in metrics.teleport_counts.items() if key.endswith(":1")
    )
    if teleport_penalty <= 0:
        score_components.append(0.6)
    else:
        score_components.append(max(0.2, 0.8 - teleport_penalty * 0.1))

    score = sum(score_components) / max(1, len(score_components))
    return flags, max(0.0, min(score, 1.0))


# ----------------------------
# Utility helpers
# ----------------------------
COMMAND_BASE_DURATIONS: Dict[str, float] = {
    "default": 0.25,
    "teleport": 0.18,
    "jump_teleport_up": 0.9,
    "jump_down": 0.65,
    "buff": 0.45,
    "buff_secondary": 0.35,
    "reflection_mix_random": 0.55,
    "face": 0.12,
    "adjust": 0.2,
    "jump": 0.05,
}

COMMAND_JITTER: Dict[str, Tuple[float, float]] = {
    "default": (-0.04, 0.06),
    "teleport": (-0.02, 0.03),
    "jump_teleport_up": (-0.1, 0.12),
    "jump_down": (-0.08, 0.1),
    "buff": (-0.05, 0.08),
    "buff_secondary": (-0.05, 0.07),
    "reflection_mix_random": (-0.04, 0.07),
    "face": (-0.02, 0.02),
    "adjust": (-0.03, 0.04),
    "jump": (-0.01, 0.01),
}


def distance(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))
