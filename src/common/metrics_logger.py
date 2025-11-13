"""Performance metrics and statistics logging for bot runtime analysis."""

import time
import threading
from collections import defaultdict, deque
from typing import Dict, Optional
from src.common.logger import get_logger

log = get_logger(__name__)


class MetricsLogger:
    """Tracks and logs performance metrics, randomization effectiveness, and detection risk indicators."""

    def __init__(self):
        self.start_time = time.time()
        self.last_summary_time = time.time()
        self.summary_interval = 300  # Log summary every 5 minutes

        # Performance metrics
        self.loop_count = 0
        self.total_execution_time = 0.0
        self.loop_durations = deque(maxlen=100)  # Keep last 100 loops
        self.error_count = 0
        self.recovery_count = 0

        # Randomization metrics
        self.randomization_stats = {
            "point_skips": 0,
            "point_executions": 0,
            "backward_movements": 0,
            "command_shuffles": 0,
            "command_skips": 0,
            "extra_waits": 0,
            "position_offsets": 0,
            "micro_gestures": 0,
        }

        # Pattern tracking
        self.pattern_history = deque(maxlen=50)  # Last 50 actions
        self.variant_switches = 0
        self.current_variant = "normal"

        # Dynamic paths tracking
        self.path_switches = 0
        self.current_path_id = None
        self.path_usage = defaultdict(int)  # Track how many times each path is used

        # Detection risk indicators
        self.detection_risk_factors = {
            "repetitive_patterns": 0,
            "perfect_timing": 0,
            "no_randomization": 0,
            "stuck_positions": 0,
        }

        # Position tracking for stuck detection
        self.position_history = deque(maxlen=10)
        self.last_position_change = time.time()

        # Thread safety
        self.lock = threading.Lock()

    def record_loop_completion(self, duration: float):
        """Record a completed loop."""
        with self.lock:
            self.loop_count += 1
            self.total_execution_time += duration
            self.loop_durations.append(duration)

    def record_error(self):
        """Record an error occurrence."""
        with self.lock:
            self.error_count += 1

    def record_recovery(self):
        """Record a recovery action."""
        with self.lock:
            self.recovery_count += 1

    def record_point_skip(self):
        """Record a point skip."""
        with self.lock:
            self.randomization_stats["point_skips"] += 1

    def record_point_execution(self):
        """Record a point execution."""
        with self.lock:
            self.randomization_stats["point_executions"] += 1

    def record_backward_movement(self):
        """Record a backward movement."""
        with self.lock:
            self.randomization_stats["backward_movements"] += 1

    def record_command_shuffle(self):
        """Record a command shuffle."""
        with self.lock:
            self.randomization_stats["command_shuffles"] += 1

    def record_command_skip(self):
        """Record a command skip."""
        with self.lock:
            self.randomization_stats["command_skips"] += 1

    def record_extra_wait(self):
        """Record an extra wait."""
        with self.lock:
            self.randomization_stats["extra_waits"] += 1

    def record_position_offset(self):
        """Record a position offset."""
        with self.lock:
            self.randomization_stats["position_offsets"] += 1

    def record_micro_gesture(self):
        """Record a micro gesture."""
        with self.lock:
            self.randomization_stats["micro_gestures"] += 1

    def record_variant_switch(self, variant: str):
        """Record a variant switch."""
        with self.lock:
            self.variant_switches += 1
            self.current_variant = variant

    def record_path_switch(self, path_id: str):
        """Record a path switch."""
        with self.lock:
            self.path_switches += 1
            self.current_path_id = path_id
            self.path_usage[path_id] += 1

    def record_action(self, action_type: str):
        """Record an action for pattern tracking."""
        with self.lock:
            self.pattern_history.append((time.time(), action_type))

    def update_position(self, position: tuple):
        """Update position for stuck detection."""
        with self.lock:
            current_time = time.time()
            if not self.position_history or self.position_history[-1][1] != position:
                self.last_position_change = current_time
            self.position_history.append((current_time, position))

    def check_stuck(self) -> bool:
        """Check if bot is stuck (same position for > 30 seconds)."""
        with self.lock:
            if len(self.position_history) < 2:
                return False
            time_since_change = time.time() - self.last_position_change
            return time_since_change > 30.0

    def calculate_randomization_effectiveness(self) -> float:
        """Calculate randomization effectiveness score (0-1)."""
        with self.lock:
            total_actions = (
                self.randomization_stats["point_executions"]
                + self.randomization_stats["point_skips"]
            )
            if total_actions == 0:
                return 0.0

            # Calculate variation score
            skip_rate = self.randomization_stats["point_skips"] / total_actions
            backward_rate = self.randomization_stats["backward_movements"] / max(
                total_actions, 1
            )
            shuffle_rate = self.randomization_stats["command_shuffles"] / max(
                total_actions, 1
            )

            # Ideal: 5-15% skip rate, some backward, some shuffles
            effectiveness = min(
                1.0,
                (
                    (skip_rate * 10 if 0.05 <= skip_rate <= 0.15 else 0)
                    + (backward_rate * 5 if backward_rate > 0 else 0)
                    + (shuffle_rate * 3 if shuffle_rate > 0 else 0)
                ),
            )
            return effectiveness

    def calculate_detection_risk(self) -> float:
        """Calculate detection risk score (0-1, higher = more risky)."""
        with self.lock:
            risk = 0.0

            # Check if randomization is disabled
            total_actions = (
                self.randomization_stats["point_executions"]
                + self.randomization_stats["point_skips"]
            )
            if total_actions > 0:
                skip_rate = self.randomization_stats["point_skips"] / total_actions
                if skip_rate == 0:
                    risk += 0.3  # No randomization = high risk
                elif skip_rate < 0.02:
                    risk += 0.2  # Very low randomization

            # Check for repetitive patterns
            if len(self.pattern_history) >= 10:
                recent_actions = [a[1] for a in list(self.pattern_history)[-10:]]
                unique_actions = len(set(recent_actions))
                if unique_actions < 3:
                    risk += 0.3  # Very repetitive

            # Check for stuck
            if self.check_stuck():
                risk += 0.2

            # Check error rate
            if self.loop_count > 0:
                error_rate = self.error_count / self.loop_count
                if error_rate > 0.1:
                    risk += 0.2  # High error rate

            return min(1.0, risk)

    def get_summary(self) -> Dict:
        """Get current metrics summary."""
        with self.lock:
            uptime = time.time() - self.start_time
            avg_loop_duration = (
                sum(self.loop_durations) / len(self.loop_durations)
                if self.loop_durations
                else 0.0
            )

            total_actions = (
                self.randomization_stats["point_executions"]
                + self.randomization_stats["point_skips"]
            )
            skip_rate = (
                self.randomization_stats["point_skips"] / total_actions
                if total_actions > 0
                else 0.0
            )

            return {
                "uptime_seconds": uptime,
                "uptime_formatted": self._format_duration(uptime),
                "loop_count": self.loop_count,
                "avg_loop_duration": avg_loop_duration,
                "error_count": self.error_count,
                "recovery_count": self.recovery_count,
                "error_rate": self.error_count / max(self.loop_count, 1),
                "randomization_stats": self.randomization_stats.copy(),
                "skip_rate": skip_rate,
                "randomization_effectiveness": self.calculate_randomization_effectiveness(),
                "detection_risk": self.calculate_detection_risk(),
                "current_variant": self.current_variant,
                "variant_switches": self.variant_switches,
                "current_path_id": self.current_path_id,
                "path_switches": self.path_switches,
                "path_usage": dict(self.path_usage),
                "is_stuck": self.check_stuck(),
            }

    def log_summary(self):
        """Log a periodic summary of metrics."""
        summary = self.get_summary()

        log.info("=" * 80)
        log.info("📊 BOT METRICS SUMMARY")
        log.info("=" * 80)
        log.info("⏱️  Uptime: %s", summary["uptime_formatted"])
        log.info("🔄 Loops completed: %d", summary["loop_count"])
        log.info("⏱️  Avg loop duration: %.2fs", summary["avg_loop_duration"])
        log.info(
            "❌ Errors: %d (rate: %.2f%%)",
            summary["error_count"],
            summary["error_rate"] * 100,
        )
        log.info("🔧 Recoveries: %d", summary["recovery_count"])
        log.info("")
        log.info("🎲 RANDOMIZATION STATS:")
        log.info(
            "   Point skips: %d (%.1f%%)",
            summary["randomization_stats"]["point_skips"],
            summary["skip_rate"] * 100,
        )
        log.info(
            "   Point executions: %d",
            summary["randomization_stats"]["point_executions"],
        )
        log.info(
            "   Backward movements: %d",
            summary["randomization_stats"]["backward_movements"],
        )
        log.info(
            "   Command shuffles: %d",
            summary["randomization_stats"]["command_shuffles"],
        )
        log.info(
            "   Command skips: %d", summary["randomization_stats"]["command_skips"]
        )
        log.info("   Extra waits: %d", summary["randomization_stats"]["extra_waits"])
        log.info(
            "   Position offsets: %d",
            summary["randomization_stats"]["position_offsets"],
        )
        log.info(
            "   Micro gestures: %d", summary["randomization_stats"]["micro_gestures"]
        )
        log.info(
            "   Effectiveness score: %.2f/1.0", summary["randomization_effectiveness"]
        )
        log.info("")
        log.info("⚠️  DETECTION RISK:")
        risk_score = summary["detection_risk"]
        risk_level = (
            "LOW" if risk_score < 0.3 else "MEDIUM" if risk_score < 0.6 else "HIGH"
        )
        log.info("   Risk score: %.2f/1.0 (%s)", risk_score, risk_level)
        if summary["is_stuck"]:
            log.warning("   ⚠️ Bot appears to be STUCK (no position change > 30s)")
        log.info("")
        log.info("🔄 PATTERN VARIATION:")
        log.info("   Current variant: %s", summary["current_variant"])
        log.info("   Variant switches: %d", summary["variant_switches"])
        if summary.get("current_path_id"):
            log.info("🛤️ DYNAMIC PATHS:")
            log.info("   Current path: %s", summary["current_path_id"])
            log.info("   Path switches: %d", summary["path_switches"])
            log.info("   Path usage: %s", dict(summary.get("path_usage", {})))
        log.info("=" * 80)

    def should_log_summary(self) -> bool:
        """Check if it's time to log a summary."""
        current_time = time.time()
        if current_time - self.last_summary_time >= self.summary_interval:
            self.last_summary_time = current_time
            return True
        return False

    @staticmethod
    def _format_duration(seconds: float) -> str:
        """Format duration in seconds to human-readable string."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        if hours > 0:
            return f"{hours}h {minutes}m {secs}s"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"


# Global instance
_metrics_logger: Optional[MetricsLogger] = None


def get_metrics_logger() -> MetricsLogger:
    """Get the global metrics logger instance."""
    global _metrics_logger
    if _metrics_logger is None:
        _metrics_logger = MetricsLogger()
    return _metrics_logger


def reset_metrics():
    """Reset metrics (useful for testing or new session)."""
    global _metrics_logger
    _metrics_logger = MetricsLogger()
