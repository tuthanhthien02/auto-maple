"""Smoke tests for Dynamic Paths feature."""

import unittest
from types import SimpleNamespace
from unittest.mock import patch

from src.common import config
from src.routine.components import Point
from src.routine.routine import Routine


def _noop(*_, **__):
    return None


def _build_gui_stub():
    details = SimpleNamespace(update_details=_noop, display_info=_noop)
    routine_view = SimpleNamespace(select=_noop)
    status = SimpleNamespace(set_routine=_noop)
    minimap = SimpleNamespace(draw_default=_noop)
    view = SimpleNamespace(
        details=details, routine=routine_view, status=status, minimap=minimap
    )
    edit = SimpleNamespace(minimap=minimap)
    return SimpleNamespace(
        set_routine=_noop, view=view, edit=edit, clear_routine_info=_noop
    )


class RoutineForTest(Routine):
    def _load_randomization_settings(self):
        # Skip GUI settings loading in test environment
        pass


class DynamicPathsSmokeTests(unittest.TestCase):
    def setUp(self):
        config.gui = _build_gui_stub()
        config.bot = SimpleNamespace(command_book={})
        config.enabled = True

        self.routine = RoutineForTest()
        config.routine = self.routine

        # Create a routine with multiple points
        self.points = [
            Point(0.1, 0.2, adjust="False"),
            Point(0.2, 0.3, adjust="False"),
            Point(0.3, 0.4, adjust="False"),
            Point(0.4, 0.5, adjust="False"),
            Point(0.5, 0.6, adjust="False"),
        ]
        self.routine.sequence = self.points.copy()
        self.routine.index = 0

        # Enable dynamic paths
        self.routine.dynamic_paths_enabled = True
        self.routine.dynamic_paths_config = {
            "path_count": 3,
            "generation_strategy": "random_skip",
            "skip_percentage_range": (0.1, 0.3),
            "selection_mode": "transition_matrix",
            "switch_interval": {"min_loops": 2, "max_loops": 5},
            "transition_matrix": {},
        }

    def tearDown(self):
        config.routine = None

    def test_generate_paths_creates_correct_count(self):
        """Test that path generation creates the correct number of paths."""
        self.routine._generate_dynamic_paths()

        self.assertGreaterEqual(
            len(self.routine.dynamic_paths), 1
        )  # At least path1 (full path)
        self.assertLessEqual(
            len(self.routine.dynamic_paths),
            self.routine.dynamic_paths_config["path_count"],
        )

        # Path1 should always be full path
        path1 = next(
            (p for p in self.routine.dynamic_paths if p["id"] == "path1"), None
        )
        self.assertIsNotNone(path1)
        self.assertEqual(len(path1["indices"]), len(self.points))

    def test_generate_paths_all_paths_have_valid_indices(self):
        """Test that all generated paths have valid indices."""
        self.routine._generate_dynamic_paths()

        for path in self.routine.dynamic_paths:
            self.assertGreaterEqual(len(path["indices"]), 2)  # At least 2 points
            self.assertLessEqual(
                len(path["indices"]), len(self.points)
            )  # Not more than total

            # All indices should be valid
            for idx in path["indices"]:
                self.assertGreaterEqual(idx, 0)
                self.assertLess(idx, len(self.routine.sequence))
                # Should be a Point
                self.assertIsInstance(self.routine.sequence[idx], Point)

    def test_generate_paths_random_skip_strategy(self):
        """Test random_skip generation strategy."""
        self.routine.dynamic_paths_config["generation_strategy"] = "random_skip"

        with patch("src.routine.routine.random.uniform", return_value=0.2), patch(
            "src.routine.routine.random.sample",
            side_effect=lambda seq, k: sorted(seq)[:k],
        ):
            self.routine._generate_dynamic_paths()

        # Should have paths with different lengths
        path_lengths = [len(p["indices"]) for p in self.routine.dynamic_paths]
        # At least one path should be shorter than full path (if random worked)
        self.assertIn(len(self.points), path_lengths)  # Full path should exist

    def test_generate_paths_partial_strategy(self):
        """Test partial generation strategy."""
        self.routine.dynamic_paths_config["generation_strategy"] = "partial"

        with patch("src.routine.routine.random.uniform", return_value=0.2), patch(
            "src.routine.routine.random.random", return_value=0.0
        ):  # First N%
            self.routine._generate_dynamic_paths()

        # Should have paths
        self.assertGreater(len(self.routine.dynamic_paths), 1)

    def test_transition_matrix_auto_generation(self):
        """Test that transition matrix is auto-generated correctly."""
        self.routine._generate_dynamic_paths()
        self.routine._generate_transition_matrix()

        matrix = self.routine.dynamic_paths_config.get("transition_matrix", {})
        self.assertIsInstance(matrix, dict)

        # Each path should have transitions
        path_ids = [p["id"] for p in self.routine.dynamic_paths]
        for path_id in path_ids:
            self.assertIn(path_id, matrix)
            transitions = matrix[path_id]

            # Should have transitions to all paths
            self.assertEqual(set(transitions.keys()), set(path_ids))

            # Probabilities should sum to ~1.0
            total_prob = sum(transitions.values())
            self.assertAlmostEqual(total_prob, 1.0, places=2)

    def test_select_initial_path(self):
        """Test initial path selection."""
        self.routine._generate_dynamic_paths()
        self.routine._generate_transition_matrix()
        self.routine._select_initial_path()

        self.assertIsNotNone(self.routine.current_path_id)
        self.assertIn(
            self.routine.current_path_id, [p["id"] for p in self.routine.dynamic_paths]
        )

        # Index should be set to first point in selected path
        current_path = next(
            (
                p
                for p in self.routine.dynamic_paths
                if p["id"] == self.routine.current_path_id
            ),
            None,
        )
        if current_path:
            self.assertEqual(self.routine.index, current_path["indices"][0])

    def test_select_next_path_random_mode(self):
        """Test path selection in random mode."""
        self.routine.dynamic_paths_config["selection_mode"] = "random"
        self.routine._generate_dynamic_paths()
        self.routine.current_path_id = "path1"

        with patch(
            "src.routine.routine.random.choice",
            side_effect=lambda seq: seq[1] if len(seq) > 1 else seq[0],
        ):
            self.routine._select_next_path()

        # Should switch to a different path (if multiple paths exist)
        if len(self.routine.dynamic_paths) > 1:
            self.assertNotEqual(self.routine.current_path_id, "path1")

    def test_select_next_path_transition_matrix_mode(self):
        """Test path selection using transition matrix."""
        self.routine.dynamic_paths_config["selection_mode"] = "transition_matrix"
        self.routine._generate_dynamic_paths()
        self.routine._generate_transition_matrix()
        self.routine.current_path_id = "path1"

        # Mock transition matrix selection
        matrix = self.routine.dynamic_paths_config["transition_matrix"]
        if "path1" in matrix:
            # Get most likely next path
            transitions = matrix["path1"]
            next_path = max(transitions.items(), key=lambda x: x[1])[0]

            with patch("src.routine.routine.random.choices", return_value=[next_path]):
                self.routine._select_next_path()

            self.assertEqual(self.routine.current_path_id, next_path)

    def test_path_stepping_within_path(self):
        """Test that stepping only moves within current path indices."""
        self.routine._generate_dynamic_paths()
        self.routine._generate_transition_matrix()
        self.routine._select_initial_path()

        current_path = next(
            (
                p
                for p in self.routine.dynamic_paths
                if p["id"] == self.routine.current_path_id
            ),
            None,
        )
        if current_path and len(current_path["indices"]) > 1:
            path_indices = current_path["indices"]
            self.routine.index = path_indices[0]

            # Step should move to next index in path
            next_idx = self.routine._get_variant_next_index(self.routine.index)
            self.assertIn(next_idx, path_indices)
            self.assertEqual(next_idx, path_indices[1])

    def test_path_loop_completion_detection(self):
        """Test that path loop completion is detected correctly."""
        self.routine._generate_dynamic_paths()
        self.routine._generate_transition_matrix()
        self.routine._select_initial_path()

        current_path = next(
            (
                p
                for p in self.routine.dynamic_paths
                if p["id"] == self.routine.current_path_id
            ),
            None,
        )
        if current_path and len(current_path["indices"]) > 1:
            path_indices = current_path["indices"]

            # Simulate reaching end of path and stepping to start
            old_index = path_indices[-1]  # Last index in path
            self.routine.index = path_indices[0]  # After step, at first index
            self.routine.last_index = old_index  # Previous index was last

            # Should detect loop completion (old_index was last, current index is first)
            loop_completed = self.routine._detect_loop_completion(old_index)
            self.assertTrue(loop_completed)

    def test_path_switching_on_loop_completion(self):
        """Test that path switches after completing switch_interval loops."""
        self.routine._generate_dynamic_paths()
        self.routine._generate_transition_matrix()
        self.routine._select_initial_path()

        initial_path = self.routine.current_path_id
        self.routine.path_switch_interval = 2
        self.routine.path_switch_counter = 0

        # Complete 2 loops
        for _ in range(2):
            self.routine._on_loop_completed()

        # Should have switched path
        self.assertNotEqual(self.routine.current_path_id, initial_path)
        self.assertEqual(self.routine.path_switch_counter, 0)  # Reset after switch

    def test_path_generation_with_insufficient_points(self):
        """Test that path generation handles insufficient points gracefully."""
        # Only 1 point
        self.routine.sequence = [Point(0.1, 0.2, adjust="False")]

        self.routine._generate_dynamic_paths()

        # Should not generate paths (need at least 2 points)
        self.assertEqual(len(self.routine.dynamic_paths), 0)

    def test_path_generation_with_empty_sequence(self):
        """Test that path generation handles empty sequence gracefully."""
        self.routine.sequence = []

        self.routine._generate_dynamic_paths()

        # Should not generate paths
        self.assertEqual(len(self.routine.dynamic_paths), 0)

    def test_apply_path_to_index(self):
        """Test that applying path sets index correctly."""
        self.routine._generate_dynamic_paths()
        self.routine.current_path_id = "path1"

        self.routine._apply_path_to_index()

        current_path = next(
            (p for p in self.routine.dynamic_paths if p["id"] == "path1"), None
        )
        if current_path:
            self.assertEqual(self.routine.index, current_path["indices"][0])
            self.assertEqual(self.routine.last_index, -1)  # Reset for loop detection


if __name__ == "__main__":
    unittest.main()
