"""Crash detection and unexpected exit handling."""

import atexit
import signal
import sys
import threading
import time

from src.common.logger import get_logger

log = get_logger(__name__)

# Track if we're shutting down gracefully
# Bug fix: Use threading.Lock for thread-safe access to global variables
_shutdown_lock = threading.Lock()
_graceful_shutdown = False
_shutdown_reason = "unknown"
_startup_time = time.time()
_crash_handler_registered = False


def _log_critical_event(event_type: str, message: str, exc_info=None) -> None:
    """Log a critical event with highlighting."""
    log.critical(
        "=" * 80,
        extra={"event_type": event_type},
    )
    log.critical(
        "🚨 CRITICAL EVENT: %s",
        event_type,
        extra={"event_type": event_type},
    )
    log.critical(
        "📝 Message: %s",
        message,
        extra={"event_type": event_type},
    )
    if exc_info:
        log.critical(
            "📋 Traceback:",
            exc_info=exc_info,
            extra={"event_type": event_type},
        )
    log.critical(
        "=" * 80,
        extra={"event_type": event_type},
    )


def _handle_unexpected_exit() -> None:
    """Handle unexpected exit/crash."""
    global _graceful_shutdown, _shutdown_reason

    # Bug fix: Thread-safe access to global variables
    with _shutdown_lock:
        is_graceful = _graceful_shutdown
        reason = _shutdown_reason

    if is_graceful:
        # Expected shutdown
        uptime = time.time() - _startup_time
        log.info(
            "Bot shutting down gracefully (reason: %s, uptime: %.1f seconds)",
            reason,
            uptime,
        )
        return

    # Unexpected exit
    uptime = time.time() - _startup_time
    _log_critical_event(
        "UNEXPECTED_EXIT",
        f"Bot exited unexpectedly after {uptime:.1f} seconds. "
        "This may indicate a crash or forced termination.",
    )

    # Try to log stack trace if available
    try:
        import traceback

        frames = traceback.extract_stack()
        if frames:
            log.critical("Last known stack trace:")
            for frame in frames[-10:]:  # Last 10 frames
                log.critical(
                    "  File %s, line %d, in %s: %s",
                    frame.filename,
                    frame.lineno,
                    frame.name,
                    frame.line or "",
                )
    except Exception:
        pass


def _handle_signal(signum, frame) -> None:
    """Handle system signals (SIGTERM, SIGINT, etc.)."""
    global _graceful_shutdown, _shutdown_reason

    signal_names = {
        signal.SIGTERM: "SIGTERM",
        signal.SIGINT: "SIGINT",
        signal.SIGBREAK: "SIGBREAK",
    }
    signal_name = signal_names.get(signum, f"Signal {signum}")

    _log_critical_event(
        "SIGNAL_RECEIVED",
        f"Received {signal_name}. Initiating graceful shutdown...",
    )

    # Bug fix: Thread-safe update of global variables
    with _shutdown_lock:
        _graceful_shutdown = True
        _shutdown_reason = signal_name

    # Re-raise to allow normal signal handling
    if signum == signal.SIGINT:
        # SIGINT (Ctrl+C) - allow normal KeyboardInterrupt
        raise KeyboardInterrupt


def _handle_exception(exc_type, exc_value, exc_traceback) -> None:
    """Handle uncaught exceptions."""
    global _graceful_shutdown, _shutdown_reason

    # Don't log KeyboardInterrupt or SystemExit as crashes
    if exc_type in (KeyboardInterrupt, SystemExit):
        # Bug fix: Thread-safe update
        with _shutdown_lock:
            _graceful_shutdown = True
            _shutdown_reason = exc_type.__name__
        return

    # Log uncaught exception as crash
    _log_critical_event(
        "UNCAUGHT_EXCEPTION",
        f"Uncaught exception: {exc_type.__name__}: {exc_value}",
        exc_info=(exc_type, exc_value, exc_traceback),
    )


def register_crash_handlers() -> None:
    """Register crash detection handlers."""
    global _crash_handler_registered, _startup_time

    # Bug fix: Thread-safe check and set
    with _shutdown_lock:
        if _crash_handler_registered:
            log.warning("Crash handlers already registered")
            return
        _crash_handler_registered = True
        _startup_time = time.time()

    # Register atexit handler for unexpected exits
    # Bug fix: Check if already registered to avoid duplicate handlers
    # atexit handlers are called in reverse order of registration
    # We only want one handler, so check if it's already there
    atexit.register(_handle_unexpected_exit)

    # Register signal handlers (Windows)
    try:
        signal.signal(signal.SIGTERM, _handle_signal)
        signal.signal(signal.SIGINT, _handle_signal)
        # SIGBREAK is Windows-specific
        if hasattr(signal, "SIGBREAK"):
            signal.signal(signal.SIGBREAK, _handle_signal)
    except (ValueError, OSError) as e:
        log.warning("Could not register some signal handlers: %s", e)

    # Register exception handler for uncaught exceptions
    sys.excepthook = _handle_exception

    log.info("Crash detection handlers registered")


def mark_graceful_shutdown(reason: str = "user_request") -> None:
    """Mark that shutdown is graceful (not a crash)."""
    global _graceful_shutdown, _shutdown_reason
    # Bug fix: Thread-safe update
    with _shutdown_lock:
        _graceful_shutdown = True
        _shutdown_reason = reason
    log.info("Marked graceful shutdown (reason: %s)", reason)


def is_graceful_shutdown() -> bool:
    """Check if shutdown is graceful."""
    # Bug fix: Thread-safe read
    with _shutdown_lock:
        return _graceful_shutdown


def get_uptime() -> float:
    """Get bot uptime in seconds."""
    return time.time() - _startup_time


def log_startup() -> None:
    """Log bot startup event."""
    _log_critical_event(
        "BOT_STARTUP",
        "Bot starting up...",
    )


def log_shutdown() -> None:
    """Log bot shutdown event."""
    uptime = get_uptime()
    # Bug fix: Thread-safe read of _shutdown_reason
    with _shutdown_lock:
        reason = _shutdown_reason
    _log_critical_event(
        "BOT_SHUTDOWN",
        f"Bot shutting down (uptime: {uptime:.1f} seconds, reason: {reason})",
    )
