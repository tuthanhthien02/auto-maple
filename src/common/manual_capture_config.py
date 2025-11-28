"""
Helpers to persist and retrieve manual capture regions selected via the GUI.
"""

from __future__ import annotations

import json
import os
from typing import Dict, Optional

from src.common import config


MANUAL_CAPTURE_CONFIG_PATH = os.path.join(
    "configs",
    "manual_capture_region.json",
)


def _ensure_directory() -> None:
    directory = os.path.dirname(MANUAL_CAPTURE_CONFIG_PATH)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def load_manual_region() -> Optional[Dict[str, int]]:
    """
    Load the saved manual capture rectangle if it exists.
    """
    try:
        with open(MANUAL_CAPTURE_CONFIG_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
            if not isinstance(data, dict):
                return None
            required_keys = {"left", "top", "width", "height"}
            if not required_keys.issubset(data.keys()):
                return None
            rect = {key: int(data[key]) for key in required_keys}
            return rect
    except FileNotFoundError:
        return None
    except Exception:
        return None


def save_manual_region(rect: Dict[str, int]) -> None:
    """
    Persist a manual capture rectangle to disk.
    """
    _ensure_directory()
    with open(MANUAL_CAPTURE_CONFIG_PATH, "w", encoding="utf-8") as file:
        json.dump(rect, file, ensure_ascii=False, indent=2)
    config.manual_capture_rect = rect


def clear_manual_region() -> None:
    """
    Remove the stored manual capture rectangle.
    """
    if os.path.exists(MANUAL_CAPTURE_CONFIG_PATH):
        try:
            os.remove(MANUAL_CAPTURE_CONFIG_PATH)
        except OSError:
            pass
    config.manual_capture_rect = None


def initialize_manual_region() -> None:
    """
    Load manual capture data into global config on startup.
    """
    config.manual_capture_rect = load_manual_region()
