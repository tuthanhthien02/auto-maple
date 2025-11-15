"""Health check system for monitoring bot components."""

import threading
import time
from typing import Dict, Optional, Callable
from enum import Enum

from src.common.logger import get_logger

log = get_logger(__name__)


class HealthStatus(Enum):
    """Health status enumeration."""

    HEALTHY = "healthy"
    WARNING = "warning"
    ERROR = "error"
    UNKNOWN = "unknown"


class ComponentHealth:
    """Represents health status of a component."""

    def __init__(self, name: str):
        self.name = name
        self.status = HealthStatus.UNKNOWN
        self.last_check_time = 0.0
        self.last_success_time = 0.0
        self.consecutive_failures = 0
        self.message = ""
        self.check_interval = 30.0  # Default: check every 30 seconds
        self.warning_threshold = 3  # Warn after 3 consecutive failures
        self.error_threshold = 5  # Error after 5 consecutive failures

    def update(
        self, status: HealthStatus, message: str = "", success: bool = True
    ) -> None:
        """Update component health status."""
        self.status = status
        self.message = message
        self.last_check_time = time.time()

        if success:
            self.last_success_time = time.time()
            self.consecutive_failures = 0
        else:
            self.consecutive_failures += 1
            if self.consecutive_failures >= self.error_threshold:
                self.status = HealthStatus.ERROR
            elif self.consecutive_failures >= self.warning_threshold:
                self.status = HealthStatus.WARNING

    def is_healthy(self) -> bool:
        """Check if component is healthy."""
        return self.status == HealthStatus.HEALTHY

    def get_status_string(self) -> str:
        """Get human-readable status string."""
        status_emoji = {
            HealthStatus.HEALTHY: "✓",
            HealthStatus.WARNING: "⚠",
            HealthStatus.ERROR: "✗",
            HealthStatus.UNKNOWN: "?",
        }
        emoji = status_emoji.get(self.status, "?")
        return f"{emoji} {self.name}: {self.status.value.upper()} - {self.message}"


class HealthMonitor:
    """Monitors health of all bot components."""

    def __init__(self):
        self.components: Dict[str, ComponentHealth] = {}
        self.checkers: Dict[str, Callable[[], tuple[HealthStatus, str, bool]]] = {}
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()

    def register_component(
        self,
        name: str,
        checker: Callable[[], tuple[HealthStatus, str, bool]],
        check_interval: float = 30.0,
        warning_threshold: int = 3,
        error_threshold: int = 5,
    ) -> None:
        """Register a component for health monitoring.

        Args:
            name: Component name
            checker: Function that returns (HealthStatus, message, success)
            check_interval: How often to check (seconds)
            warning_threshold: Consecutive failures before warning
            error_threshold: Consecutive failures before error
        """
        with self._lock:
            component = ComponentHealth(name)
            component.check_interval = check_interval
            component.warning_threshold = warning_threshold
            component.error_threshold = error_threshold
            self.components[name] = component
            self.checkers[name] = checker
            log.info(
                "Registered health check for component: %s (interval=%.1fs)",
                name,
                check_interval,
            )

    def unregister_component(self, name: str) -> None:
        """Unregister a component."""
        with self._lock:
            if name in self.components:
                del self.components[name]
            if name in self.checkers:
                del self.checkers[name]
            log.info("Unregistered health check for component: %s", name)

    def check_component(self, name: str) -> Optional[ComponentHealth]:
        """Manually check a component."""
        # Bug fix: Get component and checker outside lock to avoid deadlock
        # if checker() needs to access other components or acquire locks
        with self._lock:
            if name not in self.components or name not in self.checkers:
                return None

            component = self.components[name]
            checker = self.checkers[name]

        # Bug fix: Call checker() outside lock to prevent deadlock
        # This allows checker functions to safely access other components
        try:
            status, message, success = checker()
            # Bug fix: Update component with lock to ensure thread safety
            with self._lock:
                if name in self.components:  # Check component still exists
                    component.update(status, message, success)
                    return component
                return None
        except Exception as e:
            log.error("Health check failed for %s: %s", name, e, exc_info=True)
            # Bug fix: Update component with lock
            with self._lock:
                if name in self.components:  # Check component still exists
                    component.update(HealthStatus.ERROR, f"Check exception: {e}", False)
                    return component
                return None

    def check_all(self) -> Dict[str, ComponentHealth]:
        """Check all registered components."""
        results = {}
        with self._lock:
            component_names = list(self.components.keys())

        for name in component_names:
            component = self.check_component(name)
            if component:
                results[name] = component

        return results

    def get_status(self) -> Dict[str, Dict]:
        """Get status of all components."""
        with self._lock:
            status = {}
            for name, component in self.components.items():
                status[name] = {
                    "status": component.status.value,
                    "is_healthy": component.is_healthy(),
                    "message": component.message,
                    "last_check": component.last_check_time,
                    "last_success": component.last_success_time,
                    "consecutive_failures": component.consecutive_failures,
                }
            return status

    def start_monitoring(self, interval: float = 30.0) -> None:
        """Start periodic health monitoring."""
        if self.monitoring:
            log.warning("Health monitoring already started")
            return

        self.monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop, args=(interval,), daemon=True
        )
        self.monitor_thread.start()
        log.info("Health monitoring started (interval=%.1fs)", interval)

    def stop_monitoring(self) -> None:
        """Stop periodic health monitoring."""
        # Bug fix: Check if already stopped to avoid duplicate calls
        if not self.monitoring:
            return

        self.monitoring = False
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=5.0)
            if self.monitor_thread.is_alive():
                log.warning("Health monitor thread did not stop within timeout")
        log.info("Health monitoring stopped")

    def _monitor_loop(self, base_interval: float) -> None:
        """Main monitoring loop."""
        while self.monitoring:
            try:
                results = self.check_all()

                # Log summary
                healthy_count = sum(1 for c in results.values() if c.is_healthy())
                total_count = len(results)

                if healthy_count < total_count:
                    # Some components unhealthy - log details
                    unhealthy = [
                        c.get_status_string()
                        for c in results.values()
                        if not c.is_healthy()
                    ]
                    log.warning(
                        "Health Check: %d/%d components healthy. Issues: %s",
                        healthy_count,
                        total_count,
                        "; ".join(unhealthy),
                    )
                else:
                    log.debug("Health Check: All %d components healthy", total_count)

                # Bug fix: Check monitoring flag before sleep to allow immediate stop
                # Sleep in small increments to allow faster shutdown
                sleep_interval = 0.5  # Check every 0.5 seconds
                elapsed = 0.0
                while self.monitoring and elapsed < base_interval:
                    time.sleep(sleep_interval)
                    elapsed += sleep_interval

            except Exception as e:
                log.error("Health monitor loop error: %s", e, exc_info=True)
                # Bug fix: Check monitoring flag before sleep
                if self.monitoring:
                    time.sleep(min(base_interval, 5.0))  # Max 5s sleep on error

    def log_summary(self) -> None:
        """Log a summary of all component health."""
        results = self.check_all()
        if not results:
            log.info("Health Check: No components registered")
            return

        healthy_count = sum(1 for c in results.values() if c.is_healthy())
        total_count = len(results)

        log.info(
            "Health Check Summary: %d/%d components healthy",
            healthy_count,
            total_count,
        )

        for component in results.values():
            log.info("  %s", component.get_status_string())


# Global health monitor instance
_health_monitor = HealthMonitor()


def get_health_monitor() -> HealthMonitor:
    """Get the global health monitor instance."""
    return _health_monitor


def register_arduino_health_check() -> None:
    """Register Arduino connection health check."""
    try:
        from src.common.shared_arduino_connection import SharedArduinoConnection

        def check_arduino() -> tuple[HealthStatus, str, bool]:
            """Check Arduino connection health."""
            try:
                # Bug fix: Handle case where SharedArduinoConnection singleton not yet created
                shared_conn = SharedArduinoConnection()
                if not shared_conn:
                    return (
                        HealthStatus.UNKNOWN,
                        "SharedArduinoConnection not initialized",
                        False,
                    )

                # Bug fix: Use try-except for thread-safe access to connected property
                try:
                    connected = shared_conn.connected
                except Exception as conn_error:
                    return (
                        HealthStatus.ERROR,
                        f"Connection check failed: {conn_error}",
                        False,
                    )

                if connected:
                    return (
                        HealthStatus.HEALTHY,
                        "Connected and operational",
                        True,
                    )
                else:
                    return (
                        HealthStatus.WARNING,
                        "Not connected",
                        False,
                    )
            except Exception as e:
                return (
                    HealthStatus.ERROR,
                    f"Check failed: {e}",
                    False,
                )

        _health_monitor.register_component(
            "Arduino",
            check_arduino,
            check_interval=15.0,  # Check every 15 seconds
            warning_threshold=2,
            error_threshold=4,
        )
        log.info("Arduino health check registered")

    except ImportError:
        log.warning("Could not register Arduino health check: module not available")


def register_capture_health_check() -> None:
    """Register Capture module health check."""
    try:
        from src.common import config

        def check_capture() -> tuple[HealthStatus, str, bool]:
            """Check Capture module health."""
            try:
                if not hasattr(config, "capture") or config.capture is None:
                    return (
                        HealthStatus.UNKNOWN,
                        "Capture module not initialized",
                        False,
                    )

                capture = config.capture

                # Check if capture is ready
                if not capture.ready:
                    return (
                        HealthStatus.WARNING,
                        "Not ready (calibrating?)",
                        False,
                    )

                # Check if calibrated
                if not capture.calibrated:
                    return (
                        HealthStatus.WARNING,
                        "Not calibrated",
                        False,
                    )

                # Check if thread is alive
                if not hasattr(capture, "thread") or not capture.thread.is_alive():
                    return (
                        HealthStatus.ERROR,
                        "Capture thread not alive",
                        False,
                    )

                # Check if minimap is being updated (recent update)
                if capture.minimap is None:
                    return (
                        HealthStatus.WARNING,
                        "Minimap not available",
                        False,
                    )

                return (
                    HealthStatus.HEALTHY,
                    "Ready and operational",
                    True,
                )
            except Exception as e:
                return (
                    HealthStatus.ERROR,
                    f"Check failed: {e}",
                    False,
                )

        _health_monitor.register_component(
            "Capture",
            check_capture,
            check_interval=20.0,  # Check every 20 seconds
            warning_threshold=3,
            error_threshold=5,
        )
        log.info("Capture health check registered")

    except ImportError:
        log.warning("Could not register Capture health check: module not available")


def register_routine_health_check() -> None:
    """Register Routine execution health check."""
    try:
        from src.common import config

        def check_routine() -> tuple[HealthStatus, str, bool]:
            """Check Routine execution health."""
            try:
                if not hasattr(config, "routine") or config.routine is None:
                    return (
                        HealthStatus.UNKNOWN,
                        "Routine not initialized",
                        False,
                    )

                routine = config.routine

                # Check if routine has points
                if len(routine) == 0:
                    return (
                        HealthStatus.WARNING,
                        "Routine is empty",
                        False,
                    )

                # Check if routine index is valid
                if routine.index < 0 or routine.index >= len(routine):
                    return (
                        HealthStatus.ERROR,
                        f"Invalid routine index: {routine.index}/{len(routine)}",
                        False,
                    )

                return (
                    HealthStatus.HEALTHY,
                    f"Executing routine ({len(routine)} points, index {routine.index})",
                    True,
                )
            except Exception as e:
                return (
                    HealthStatus.ERROR,
                    f"Check failed: {e}",
                    False,
                )

        _health_monitor.register_component(
            "Routine",
            check_routine,
            check_interval=30.0,  # Check every 30 seconds
            warning_threshold=2,
            error_threshold=4,
        )
        log.info("Routine health check registered")

    except ImportError:
        log.warning("Could not register Routine health check: module not available")


def initialize_health_checks() -> None:
    """Initialize all health checks."""
    log.info("Initializing health checks...")
    register_arduino_health_check()
    register_capture_health_check()
    register_routine_health_check()
    log.info("Health checks initialized")


def start_health_monitoring(interval: float = 30.0) -> None:
    """Start health monitoring."""
    _health_monitor.start_monitoring(interval)


def stop_health_monitoring() -> None:
    """Stop health monitoring."""
    _health_monitor.stop_monitoring()
