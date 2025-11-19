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


class CriticalEventFormatter(logging.Formatter):
    """Formatter that highlights critical events."""

    CRITICAL_EVENTS = {
        "BOT_STARTUP",
        "BOT_SHUTDOWN",
        "UNEXPECTED_EXIT",
        "SIGNAL_RECEIVED",
        "UNCAUGHT_EXCEPTION",
    }

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with critical event highlighting."""
        # Check if this is a critical event
        event_type = getattr(record, "event_type", None)
        is_critical = (
            record.levelno >= logging.CRITICAL or event_type in self.CRITICAL_EVENTS
        )

        if is_critical:
            # Bug fix: Use try-finally to ensure format is always restored
            # even if exception occurs during formatting
            original_fmt = self._style._fmt
            enhanced_fmt = "%(asctime)s | ⚠️  CRITICAL | %(name)s | %(message)s"
            try:
                self._style._fmt = enhanced_fmt
                result = super().format(record)
            finally:
                # Always restore original format
                self._style._fmt = original_fmt
            return result
        else:
            return super().format(record)


class EncryptedFileHandler(logging.handlers.RotatingFileHandler):
    """
    File handler that encrypts log message content before writing.

    Only the message content is encrypted, metadata (timestamp, level, logger name)
    remains readable for easier debugging.
    """

    def __init__(self, *args, **kwargs):
        """Initialize EncryptedFileHandler."""
        super().__init__(*args, **kwargs)
        # Import here to avoid circular dependency
        try:
            from src.common.log_encryption import get_log_encryptor

            self._encryptor = get_log_encryptor()
        except ImportError:
            self._encryptor = None

    def emit(self, record: logging.LogRecord) -> None:
        """
        Emit a log record, encrypting the message content.

        Falls back to plain text if encryption fails.
        """
        try:
            # Format the record normally first
            msg = self.format(record)

            # Extract message content (everything after the last " | ")
            # Format: "timestamp | level | logger | message"
            parts = msg.rsplit(" | ", 1)
            if len(parts) == 2:
                metadata, message = parts
                # Encrypt only the message content
                if self._encryptor:
                    encrypted_message = self._encryptor.encrypt(message)
                    # Reconstruct log line with encrypted message
                    msg = f"{metadata} | {encrypted_message}"
                # If encryption disabled or failed, msg remains unchanged
            # If format doesn't match expected pattern, encrypt entire message
            elif self._encryptor:
                msg = self._encryptor.encrypt(msg)

            # Write to file
            self.stream.write(msg + self.terminator)
            self.flush()

        except Exception:
            # Fallback to parent's emit if encryption fails
            # This ensures logs are still written even if encryption has issues
            self.handleError(record)


def _build_handlers(log_file: Path) -> List[logging.Handler]:
    """Create the default file and optional console handlers (configurable)."""

    formatter = CriticalEventFormatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Check if encryption should be enabled
    encryption_env = os.getenv("AUTO_MAPLE_LOG_ENCRYPTION", "").strip().lower()
    encryption_enabled = encryption_env in {"1", "true", "yes", "on"}

    # Auto-enable in production (frozen executable)
    if not encryption_enabled and getattr(sys, "frozen", False):
        encryption_enabled = True

    # Validate encryption key exists if encryption is enabled
    if encryption_enabled:
        encryption_key = os.getenv("AUTO_MAPLE_LOG_ENCRYPTION_KEY", "").strip()
        if not encryption_key:
            # Key not set, disable encryption and log warning
            encryption_enabled = False
            # Use a temporary logger to avoid circular dependency
            temp_logger = logging.getLogger("auto_maple.logger_init")
            temp_logger.warning(
                "[Logger] AUTO_MAPLE_LOG_ENCRYPTION_KEY not set, encryption disabled"
            )

    # Use EncryptedFileHandler if encryption enabled, otherwise use regular RotatingFileHandler
    if encryption_enabled:
        try:
            file_handler = EncryptedFileHandler(
                log_file,
                maxBytes=5 * 1024 * 1024,  # 5 MB per file
                backupCount=5,
                encoding="utf-8",
            )
            file_handler.setFormatter(formatter)
        except Exception as e:
            # Fallback to regular handler if EncryptedFileHandler fails
            temp_logger = logging.getLogger("auto_maple.logger_init")
            temp_logger.warning(
                "[Logger] Failed to create EncryptedFileHandler: %s, using regular handler",
                e,
            )
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=5 * 1024 * 1024,  # 5 MB per file
                backupCount=5,
                encoding="utf-8",
            )
            file_handler.setFormatter(formatter)
    else:
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=5 * 1024 * 1024,  # 5 MB per file
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)

    handlers: List[logging.Handler] = [file_handler]

    # Console handler: default ON in dev, OFF in frozen/production
    # Note: Console output is never encrypted (for debugging)
    default_console = "0" if getattr(sys, "frozen", False) else "1"
    console_env = os.getenv("AUTO_MAPLE_CONSOLE", default_console).strip().lower()
    if console_env in {"1", "true", "yes", "on"}:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        handlers.append(console_handler)

    return handlers


def _parse_log_level(env_value: str, default: int) -> int:
    value = (env_value or "").strip().upper()
    if not value:
        return default
    if hasattr(logging, value):
        return getattr(logging, value)
    temp_logger = logging.getLogger("auto_maple.logger_init")
    temp_logger.warning(
        "AUTO_MAPLE_LOG_LEVEL '%s' not recognised; falling back to %s",
        value,
        logging.getLevelName(default),
    )
    return default


def _apply_log_level(logger: logging.Logger, level: int) -> None:
    logger.setLevel(level)
    for handler in logger.handlers:
        handler.setLevel(level)


def _configure_root_logger() -> logging.Logger:
    base = _resolve_base_path()
    log_dir = _ensure_log_directory(base)
    log_file = log_dir / "auto_maple.log"

    logger = logging.getLogger("auto_maple")
    if logger.handlers:
        return logger

    # Allow level override via env AUTO_MAPLE_LOG_LEVEL (DEBUG/INFO/WARNING/ERROR/CRITICAL)
    level = _parse_log_level(os.getenv("AUTO_MAPLE_LOG_LEVEL", "INFO"), logging.INFO)
    for handler in _build_handlers(log_file):
        handler.setLevel(level)
        logger.addHandler(handler)
    _apply_log_level(logger, level)
    # Also mirror level to the global root logger so third-party loggers respect it
    _apply_log_level(logging.getLogger(), level)
    logger.propagate = False

    logger.debug("Logger initialised. Writing logs to %s", log_file)
    return logger


_ROOT_LOGGER = _configure_root_logger()


def _clone_handlers(source: logging.Logger, target: logging.Logger) -> None:
    for handler in source.handlers:
        target.addHandler(handler)


def _resolve_action_log_level() -> Optional[int]:
    env_value = os.getenv("AUTO_MAPLE_ACTION_LOG_LEVEL")
    if not env_value:
        return _ROOT_LOGGER.level

    level_name = env_value.strip().upper()
    if level_name in {"NONE", "OFF", "DISABLE", "DISABLED"}:
        return None

    return getattr(logging, level_name, _ROOT_LOGGER.level)


_ACTION_LOGGER = logging.getLogger("auto_maple.action")
_ACTION_LOGGER.propagate = False
_default_action_level = _resolve_action_log_level()
if _default_action_level is None:
    _ACTION_LOGGER.disabled = True
else:
    _ACTION_LOGGER.setLevel(_default_action_level)
    _clone_handlers(_ROOT_LOGGER, _ACTION_LOGGER)


def set_action_logging(enabled: bool) -> None:
    """Enable or disable verbose per-action logging."""

    # When enabled, force DEBUG; otherwise mirror root logger level
    if enabled:
        _ACTION_LOGGER.disabled = False
        _ACTION_LOGGER.setLevel(logging.DEBUG)
    else:
        level = _resolve_action_log_level()
        if level is None:
            _ACTION_LOGGER.disabled = True
        else:
            _ACTION_LOGGER.disabled = False
            _ACTION_LOGGER.setLevel(level)
    state = "enabled" if enabled else "disabled"
    _ROOT_LOGGER.info("Action logging %s", state)


def is_action_logging_enabled() -> bool:
    """Return True when detailed action logging is enabled."""

    return _ACTION_LOGGER.level <= logging.DEBUG


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Return the shared logger or a named child logger.

    Child loggers will inherit the level from the root logger to ensure
    AUTO_MAPLE_LOG_LEVEL is respected across all modules.
    """

    if not name:
        return _ROOT_LOGGER
    child_logger = _ROOT_LOGGER.getChild(name)
    # Ensure child logger always matches root logger level
    # This ensures AUTO_MAPLE_LOG_LEVEL is respected for all loggers
    # Child loggers propagate to root, so setting level ensures filtering happens
    if child_logger.level != _ROOT_LOGGER.level:
        child_logger.setLevel(_ROOT_LOGGER.level)
    return child_logger


# Convenience alias for modules that only need the default logger.
logger = get_logger()


def get_action_logger() -> logging.Logger:
    """Return the logger dedicated to detailed action traces."""

    return _ACTION_LOGGER


if os.getenv("AUTO_MAPLE_ACTION_LOG", "").lower() in {"1", "true", "yes", "on"}:
    set_action_logging(True)
