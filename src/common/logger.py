"""Central logging configuration for Auto-Maple."""

import logging
import logging.handlers
import os
import sys
from pathlib import Path
from typing import List, Optional


def _resolve_base_path() -> Path:
    """Return directory suitable for writing logs.

    When running as a PyInstaller executable, prefer the directory that
    contains the executable (sys.executable). Otherwise, fall back to the
    project root (two levels up from this file).
    """

    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent

    return Path(__file__).resolve().parents[2]


def _load_dotenv() -> None:
    """Load environment variables from a local .env file if present."""

    env_path = _resolve_base_path() / ".env"
    if not env_path.exists():
        return

    try:
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            if not key:
                continue
            os.environ.setdefault(key, value.strip())
    except OSError:
        # Ignore read errors; environment variables simply won't be loaded.
        return


# Load .env BEFORE configuring any loggers/handlers so env can control logging
_load_dotenv()


def _ensure_log_directory(base: Path) -> Path:
    """Ensure the logs directory exists and return its path."""

    log_dir = base / "logs"
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        # As a fallback (e.g., read-only directory), use current working dir.
        log_dir = Path.cwd() / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir


def _build_handlers(log_file: Path) -> List[logging.Handler]:
    """Create the default file and optional console handlers (configurable)."""

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,  # 5 MB per file
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    handlers: List[logging.Handler] = [file_handler]

    # Console handler: default ON in dev, OFF in frozen/production
    default_console = "0" if getattr(sys, "frozen", False) else "1"
    console_env = os.getenv("AUTO_MAPLE_CONSOLE", default_console).strip().lower()
    if console_env in {"1", "true", "yes", "on"}:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        handlers.append(console_handler)

    return handlers


def _configure_root_logger() -> logging.Logger:
    base = _resolve_base_path()
    log_dir = _ensure_log_directory(base)
    log_file = log_dir / "auto_maple.log"

    logger = logging.getLogger("auto_maple")
    if logger.handlers:
        return logger

    # Allow level override via env AUTO_MAPLE_LOG_LEVEL (DEBUG/INFO/WARNING/ERROR/CRITICAL)
    level_name = os.getenv("AUTO_MAPLE_LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    logger.setLevel(level)
    for handler in _build_handlers(log_file):
        logger.addHandler(handler)
    logger.propagate = False

    logger.debug("Logger initialised. Writing logs to %s", log_file)
    return logger


_ROOT_LOGGER = _configure_root_logger()


def _clone_handlers(source: logging.Logger, target: logging.Logger) -> None:
    for handler in source.handlers:
        target.addHandler(handler)


_ACTION_LOGGER = logging.getLogger("auto_maple.action")
# By default, action logger follows the root logger level
_ACTION_LOGGER.setLevel(_ROOT_LOGGER.level)
_ACTION_LOGGER.propagate = False
_clone_handlers(_ROOT_LOGGER, _ACTION_LOGGER)


def set_action_logging(enabled: bool) -> None:
    """Enable or disable verbose per-action logging."""

    # When enabled, force DEBUG; otherwise mirror root logger level
    level = logging.DEBUG if enabled else _ROOT_LOGGER.level
    _ACTION_LOGGER.setLevel(level)
    state = "enabled" if enabled else "disabled"
    _ROOT_LOGGER.info("Action logging %s", state)


def is_action_logging_enabled() -> bool:
    """Return True when detailed action logging is enabled."""

    return _ACTION_LOGGER.level <= logging.DEBUG


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Return the shared logger or a named child logger."""

    if not name:
        return _ROOT_LOGGER
    return _ROOT_LOGGER.getChild(name)


# Convenience alias for modules that only need the default logger.
logger = get_logger()


def get_action_logger() -> logging.Logger:
    """Return the logger dedicated to detailed action traces."""

    return _ACTION_LOGGER


if os.getenv("AUTO_MAPLE_ACTION_LOG", "").lower() in {"1", "true", "yes", "on"}:
    set_action_logging(True)
