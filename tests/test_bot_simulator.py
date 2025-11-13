import json
from pathlib import Path

import pytest

from src.simulator.bot_simulator import BotRunSimulator
from src.simulator.descriptor import DescriptorRoutine, PointInstruction

DESCRIPTOR_PATH = Path("resources/routines/luminous/tree_2_floor_descriptor.csv")


@pytest.fixture(scope="module")
def routine() -> DescriptorRoutine:
    return DescriptorRoutine.from_csv(DESCRIPTOR_PATH)


def test_descriptor_parsing_basic(routine: DescriptorRoutine) -> None:
    assert routine.instructions, "Expected instructions to be parsed"
    first_point = next(
        inst for inst in routine.instructions if isinstance(inst, PointInstruction)
    )
    assert first_point.labels, "First point should have at least one label"
    assert first_point.commands, "First point should contain commands"


def test_simulation_produces_logs_and_metrics(tmp_path: Path, routine: DescriptorRoutine) -> None:
    simulator = BotRunSimulator(routine, random_seed=42)
    result = simulator.run(max_loops=1)
    assert result.logs, "Simulation should produce log entries"
    assert result.metrics.total_time > 0
    assert result.metrics.loops_completed >= 1
    assert result.metrics.loop_durations, "Expected at least one loop duration recorded"

    log_path, metrics_path = result.write_to_directory(tmp_path)
    assert log_path.exists()
    assert metrics_path.exists()

    with metrics_path.open("r", encoding="utf-8") as handle:
        metrics_payload = json.load(handle)

    assert "analysis" in metrics_payload
    assert "command_counts" in metrics_payload

