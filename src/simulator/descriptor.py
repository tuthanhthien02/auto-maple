"""Parser for routine descriptor CSV files used by the simulator."""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional


@dataclass
class DescriptorCommand:
    """Represents a single command attached to a routine point."""

    name: str
    args: List[str] = field(default_factory=list)

    @classmethod
    def from_row(cls, tokens: List[str]) -> "DescriptorCommand":
        if not tokens:
            raise ValueError("Cannot build DescriptorCommand from empty tokens")
        name, *raw_args = tokens
        args = [arg.strip() for arg in raw_args if arg is not None and arg.strip()]
        return cls(name=name.strip(), args=args)


@dataclass
class PointInstruction:
    """A point entry describing coordinates and associated commands."""

    x: float
    y: float
    adjust: bool = False
    frequency: int = 1
    labels: List[str] = field(default_factory=list)
    comments: List[str] = field(default_factory=list)
    commands: List[DescriptorCommand] = field(default_factory=list)

    def primary_label(self) -> Optional[str]:
        return self.labels[0] if self.labels else None


@dataclass
class JumpInstruction:
    """Represents a jump to a label, used for loop control."""

    target: str
    frequency: int = 1


Instruction = PointInstruction | JumpInstruction


@dataclass
class DescriptorRoutine:
    """Structured representation of a descriptor CSV file."""

    instructions: List[Instruction]
    labels: Dict[str, int]
    metadata_comments: List[str] = field(default_factory=list)
    source_path: Optional[Path] = None

    @classmethod
    def from_csv(cls, path: Path | str) -> "DescriptorRoutine":
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(path)

        instructions: List[Instruction] = []
        labels: Dict[str, int] = {}
        metadata_comments: List[str] = []
        pending_labels: List[str] = []

        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.reader(handle)
            for raw_row in reader:
                row = cls._sanitize_row(raw_row)
                if not row:
                    continue

                head = row[0]
                if head.startswith("#"):
                    metadata_comments.append(" ".join(row))
                    continue

                lower_head = head.lower()

                if head == "*":
                    point = cls._parse_point_row(row)
                    instructions.append(point)
                    cls._apply_pending_labels(instructions, labels, pending_labels)
                    continue

                if lower_head == "label":
                    label_name = cls._require_arg(row, "Label")
                    cls._apply_label_to_latest_instruction(
                        label_name, instructions, labels, pending_labels
                    )
                    continue

                if lower_head == "comment":
                    comment = ",".join(row[1:]).strip()
                    if instructions and isinstance(instructions[-1], PointInstruction):
                        instructions[-1].comments.append(comment)
                    else:
                        metadata_comments.append(comment)
                    continue

                if lower_head == "jump":
                    target_label = cls._require_arg(row, "Jump")
                    frequency = cls._parse_int_kwarg(row[2:], "frequency", default=1)
                    instructions.append(
                        JumpInstruction(target=target_label, frequency=frequency)
                    )
                    cls._apply_pending_labels(instructions, labels, pending_labels)
                    continue

                # Otherwise treat as a command for the current point.
                if not instructions or not isinstance(
                    instructions[-1], PointInstruction
                ):
                    raise ValueError(
                        f"Command '{head}' encountered before any point declaration in {path}"
                    )
                instructions[-1].commands.append(DescriptorCommand.from_row(row))

        if pending_labels:
            raise ValueError(
                f"Unattached labels found in descriptor {path}: {pending_labels}"
            )

        return cls(
            instructions=instructions,
            labels=labels,
            metadata_comments=metadata_comments,
            source_path=path,
        )

    @staticmethod
    def _sanitize_row(row: Iterable[str]) -> List[str]:
        tokens = [token.strip() for token in row if token is not None]
        # Remove trailing empty tokens
        while tokens and not tokens[-1]:
            tokens.pop()
        return tokens

    @staticmethod
    def _parse_point_row(row: List[str]) -> PointInstruction:
        if len(row) < 3:
            raise ValueError(f"Point row requires at least x and y values: {row}")
        try:
            x = float(row[1])
            y = float(row[2])
        except ValueError as exc:
            raise ValueError(f"Invalid point coordinates: {row}") from exc

        adjust = DescriptorRoutine._parse_bool_kwarg(row[3:], "adjust", default=False)
        frequency = DescriptorRoutine._parse_int_kwarg(row[3:], "frequency", default=1)
        return PointInstruction(x=x, y=y, adjust=adjust, frequency=frequency)

    @staticmethod
    def _parse_bool_kwarg(tokens: Iterable[str], key: str, default: bool) -> bool:
        for token in tokens:
            if "=" not in token:
                continue
            name, _, value = token.partition("=")
            if name.strip().lower() != key.lower():
                continue
            normalized = value.strip().lower()
            if normalized in {"1", "true", "yes", "on"}:
                return True
            if normalized in {"0", "false", "no", "off"}:
                return False
            raise ValueError(f"Invalid boolean for {key}: {value}")
        return default

    @staticmethod
    def _parse_int_kwarg(tokens: Iterable[str], key: str, default: int) -> int:
        for token in tokens:
            if "=" not in token:
                continue
            name, _, value = token.partition("=")
            if name.strip().lower() != key.lower():
                continue
            try:
                return int(value.strip())
            except ValueError as exc:
                raise ValueError(f"Invalid integer for {key}: {value}") from exc
        return default

    @staticmethod
    def _apply_pending_labels(
        instructions: List[Instruction],
        labels: Dict[str, int],
        pending_labels: List[str],
    ) -> None:
        if not pending_labels:
            return
        idx = len(instructions) - 1
        instruction = instructions[idx]

        if isinstance(instruction, PointInstruction):
            for label in pending_labels:
                instruction.labels.append(label)
                labels[label] = idx
        else:
            for label in pending_labels:
                labels[label] = idx
        pending_labels.clear()

    @staticmethod
    def _apply_label_to_latest_instruction(
        label_name: str,
        instructions: List[Instruction],
        labels: Dict[str, int],
        pending_labels: List[str],
    ) -> None:
        if instructions and isinstance(instructions[-1], PointInstruction):
            instructions[-1].labels.append(label_name)
            labels[label_name] = len(instructions) - 1
            return
        pending_labels.append(label_name)

    @staticmethod
    def _require_arg(row: List[str], label: str) -> str:
        if len(row) < 2 or not row[1].strip():
            raise ValueError(f"{label} row requires a value: {row}")
        return row[1].strip()

    def first_point_index(self) -> Optional[int]:
        for idx, instruction in enumerate(self.instructions):
            if isinstance(instruction, PointInstruction):
                return idx
        return None

    def primary_start_label(self) -> Optional[str]:
        for instruction in self.instructions:
            if isinstance(instruction, PointInstruction) and instruction.labels:
                return instruction.labels[0]
        return None

    def infer_loop_start_label(self) -> Optional[str]:
        """Attempt to identify the label that marks the start of a loop."""

        for idx, instruction in enumerate(self.instructions):
            if isinstance(instruction, JumpInstruction):
                target_idx = self.labels.get(instruction.target)
                if target_idx is not None and target_idx < idx:
                    return instruction.target

        for instruction in self.instructions:
            if not isinstance(instruction, PointInstruction) or not instruction.labels:
                continue
            for label in instruction.labels:
                if label.lower() not in {"start_routine", "start"}:
                    return label
            return instruction.labels[0]

        return None
