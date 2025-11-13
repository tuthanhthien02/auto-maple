"""Smoke tests for Luminous distance-based movement (hold vs press key)."""

import unittest
import importlib
from unittest.mock import patch, MagicMock

from src.common import config, settings

# Import luminous command book module
luminous = importlib.import_module("resources.command_books.luminous")


class LuminousDistanceMovementSmokeTests(unittest.TestCase):
    """Test distance-based movement logic in Luminous step() function."""

    def setUp(self):
        """Set up test fixtures."""
        # Mock config
        config.player_pos = (0.0, 0.0)
        config.enabled = True
        config.stage_fright = False

        # Mock settings
        settings.move_tolerance = 0.03  # 3% map size

        # Mock vkeys functions
        self.key_down_mock = MagicMock()
        self.key_up_mock = MagicMock()
        self.press_mock = MagicMock()

        # Mock time.sleep to speed up tests
        self.sleep_mock = MagicMock()

    @patch("resources.command_books.luminous.key_down")
    @patch("resources.command_books.luminous.key_up")
    @patch("resources.command_books.luminous.press")
    @patch("resources.command_books.luminous.time.sleep")
    @patch("resources.command_books.luminous.utils.bernoulli")
    def test_horizontal_movement_far_distance_hold_key(
        self, bernoulli_mock, sleep_mock, press_mock, key_up_mock, key_down_mock
    ):
        """Test that far distance triggers hold key behavior."""
        bernoulli_mock.return_value = False  # No stage_fright delay

        # Calculate threshold using TimingConfig
        _hold_threshold = (
            settings.move_tolerance
            * luminous.TimingConfig.STEP_MOVEMENT["hold_threshold_multiplier"]
        )

        # Test with distance > threshold (far)
        target = (0.15, 0.0)  # Distance = 0.15 (far)
        distance = 0.15

        luminous.step("right", target, distance=distance)

        # Verify hold key was used (key_down + key_up, not press)
        key_down_mock.assert_called_once_with("right")
        key_up_mock.assert_called_once_with("right")
        press_mock.assert_not_called()

        # Verify sleep was called (for hold timing)
        assert sleep_mock.call_count >= 2  # At least 2 sleeps (hold + delay)

    @patch("resources.command_books.luminous.key_down")
    @patch("resources.command_books.luminous.key_up")
    @patch("resources.command_books.luminous.press")
    @patch("resources.command_books.luminous.time.sleep")
    @patch("resources.command_books.luminous.utils.bernoulli")
    def test_horizontal_movement_near_distance_press_key(
        self, bernoulli_mock, sleep_mock, press_mock, key_up_mock, key_down_mock
    ):
        """Test that near distance triggers press key behavior."""
        bernoulli_mock.return_value = False  # No stage_fright delay

        # Calculate threshold using TimingConfig
        _hold_threshold = (
            settings.move_tolerance
            * luminous.TimingConfig.STEP_MOVEMENT["hold_threshold_multiplier"]
        )

        # Test with distance <= threshold (near)
        target = (0.05, 0.0)  # Distance = 0.05 (near)
        distance = 0.05

        luminous.step("left", target, distance=distance)

        # Verify press key was used (not key_down/key_up)
        press_mock.assert_called_once()
        # Verify press was called with correct parameters
        call_args = press_mock.call_args
        assert call_args[0][0] == "left"  # direction key
        assert call_args[0][1] == 1  # n=1
        assert "down_time" in call_args[1]  # Has down_time parameter
        assert "up_time" in call_args[1]  # Has up_time parameter

        # key_down/key_up should NOT be called for near distance
        key_down_mock.assert_not_called()
        key_up_mock.assert_not_called()

    @patch("resources.command_books.luminous.key_down")
    @patch("resources.command_books.luminous.key_up")
    @patch("resources.command_books.luminous.press")
    @patch("resources.command_books.luminous.time.sleep")
    @patch("resources.command_books.luminous.utils.bernoulli")
    @patch("resources.command_books.luminous.utils.distance")
    def test_distance_calculation_when_not_provided(
        self,
        distance_mock,
        bernoulli_mock,
        sleep_mock,
        press_mock,
        key_up_mock,
        key_down_mock,
    ):
        """Test that distance is calculated when not provided."""
        bernoulli_mock.return_value = False
        distance_mock.return_value = 0.12  # Far distance

        target = (0.12, 0.0)

        # Call step() without distance parameter
        luminous.step("right", target)

        # Verify distance was calculated
        distance_mock.assert_called_once_with(config.player_pos, target)

        # Verify hold key was used (since distance > threshold)
        key_down_mock.assert_called_once()
        key_up_mock.assert_called_once()

    @patch("resources.command_books.luminous.key_down")
    @patch("resources.command_books.luminous.key_up")
    @patch("resources.command_books.luminous.press")
    @patch("resources.command_books.luminous.time.sleep")
    @patch("resources.command_books.luminous.utils.bernoulli")
    @patch("resources.command_books.luminous.log")
    def test_log_far_distance_hold_key(
        self,
        log_mock,
        bernoulli_mock,
        sleep_mock,
        press_mock,
        key_up_mock,
        key_down_mock,
    ):
        """Test that log message is generated for far distance (hold key)."""
        bernoulli_mock.return_value = False

        target = (0.15, 0.0)
        distance = 0.15
        _hold_threshold = settings.move_tolerance * 3

        luminous.step("right", target, distance=distance)

        # Verify log.debug was called with hold key message
        log_calls = [str(call) for call in log_mock.debug.call_args_list]
        assert any(
            "distance xa" in str(call) and "hold key" in str(call) for call in log_calls
        )

    @patch("resources.command_books.luminous.key_down")
    @patch("resources.command_books.luminous.key_up")
    @patch("resources.command_books.luminous.press")
    @patch("resources.command_books.luminous.time.sleep")
    @patch("resources.command_books.luminous.utils.bernoulli")
    @patch("resources.command_books.luminous.log")
    def test_log_near_distance_press_key(
        self,
        log_mock,
        bernoulli_mock,
        sleep_mock,
        press_mock,
        key_up_mock,
        key_down_mock,
    ):
        """Test that log message is generated for near distance (press key)."""
        bernoulli_mock.return_value = False

        target = (0.05, 0.0)
        distance = 0.05
        _hold_threshold = settings.move_tolerance * 3

        luminous.step("left", target, distance=distance)

        # Verify log.debug was called with press key message
        log_calls = [str(call) for call in log_mock.debug.call_args_list]
        assert any(
            "distance gần" in str(call) and "press key" in str(call)
            for call in log_calls
        )

    @patch("resources.command_books.luminous.key_down")
    @patch("resources.command_books.luminous.key_up")
    @patch("resources.command_books.luminous.press")
    @patch("resources.command_books.luminous.time.sleep")
    @patch("resources.command_books.luminous.utils.bernoulli")
    def test_threshold_boundary_far(
        self, bernoulli_mock, sleep_mock, press_mock, key_up_mock, key_down_mock
    ):
        """Test behavior at threshold boundary (slightly above = far)."""
        bernoulli_mock.return_value = False

        _hold_threshold = settings.move_tolerance * 3  # 0.09
        # Distance slightly above threshold
        distance = _hold_threshold + 0.001  # 0.091

        target = (distance, 0.0)

        luminous.step("right", target, distance=distance)

        # Should use hold key (distance > threshold)
        key_down_mock.assert_called_once()
        key_up_mock.assert_called_once()
        press_mock.assert_not_called()

    @patch("resources.command_books.luminous.key_down")
    @patch("resources.command_books.luminous.key_up")
    @patch("resources.command_books.luminous.press")
    @patch("resources.command_books.luminous.time.sleep")
    @patch("resources.command_books.luminous.utils.bernoulli")
    def test_threshold_boundary_near(
        self, bernoulli_mock, sleep_mock, press_mock, key_up_mock, key_down_mock
    ):
        """Test behavior at threshold boundary (at threshold = near)."""
        bernoulli_mock.return_value = False

        _hold_threshold = settings.move_tolerance * 3  # 0.09
        # Distance at threshold
        distance = _hold_threshold  # 0.09

        target = (distance, 0.0)

        luminous.step("left", target, distance=distance)

        # Should use press key (distance <= threshold)
        press_mock.assert_called_once()
        key_down_mock.assert_not_called()
        key_up_mock.assert_not_called()

    @patch("resources.command_books.luminous.key_down")
    @patch("resources.command_books.luminous.key_up")
    @patch("resources.command_books.luminous.press")
    @patch("resources.command_books.luminous.time.sleep")
    @patch("resources.command_books.luminous.utils.bernoulli")
    def test_both_directions_left_and_right(
        self, bernoulli_mock, sleep_mock, press_mock, key_up_mock, key_down_mock
    ):
        """Test that both left and right directions work correctly."""
        bernoulli_mock.return_value = False

        # Test left direction - far
        target_left = (0.15, 0.0)
        luminous.step("left", target_left, distance=0.15)

        # Test right direction - near
        target_right = (0.05, 0.0)
        luminous.step("right", target_right, distance=0.05)

        # Verify left used hold (key_down/key_up)
        left_calls = [
            call for call in key_down_mock.call_args_list if call[0][0] == "left"
        ]
        assert len(left_calls) > 0

        # Verify right used press
        right_press_calls = [
            call for call in press_mock.call_args_list if call[0][0] == "right"
        ]
        assert len(right_press_calls) > 0


if __name__ == "__main__":
    unittest.main()
