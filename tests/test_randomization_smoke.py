import json
import tempfile
import unittest
from io import StringIO
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from src.common import config
from src.common.bot_config import BotConfig
from src.routine.components import Point, Label
from src.routine.routine import Routine


def _noop(*_, **__):
    return None


def _build_gui_stub():
    details = SimpleNamespace(update_details=_noop, display_info=_noop)
    routine_view = SimpleNamespace(select=_noop)
    status = SimpleNamespace(set_routine=_noop)
    minimap = SimpleNamespace(draw_default=_noop)
    view = SimpleNamespace(details=details, routine=routine_view, status=status, minimap=minimap)
    edit = SimpleNamespace(minimap=minimap)
    return SimpleNamespace(set_routine=_noop, view=view, edit=edit, clear_routine_info=_noop)


class RoutineForTest(Routine):
    def _load_randomization_settings(self):
        # Bỏ qua việc đọc GUI settings trong môi trường test
        return


class StubCommandBase:
    def __init__(self):
        self.executed = False

    def execute(self):
        self.executed = True


class BuffStub(StubCommandBase):
    pass


class AttackStub(StubCommandBase):
    pass


class SkillStub(StubCommandBase):
    pass


class TeleportStub(StubCommandBase):
    def __init__(self):
        super().__init__()
        self.direction = 'left'


class RandomizationSmokeTests(unittest.TestCase):
    def setUp(self):
        config.gui = _build_gui_stub()
        config.bot = SimpleNamespace(command_book={})
        config.enabled = True

        self.routine = RoutineForTest()
        config.routine = self.routine

        self.points = [
            Point(0.1, 0.2, adjust='False'),
            Point(0.2, 0.3, adjust='False'),
            Point(0.3, 0.4, adjust='False'),
        ]
        self.routine.sequence = self.points.copy()
        self.routine.index = 0

    def tearDown(self):
        config.routine = None

    def test_skip_disabled_never_skips(self):
        self.routine.skip_enabled = False
        with patch('src.routine.routine.random.random', return_value=0.0):
            self.assertFalse(self.routine.should_skip_current_point())

    def test_skip_enabled_probability_one(self):
        self.routine.skip_enabled = True
        self.routine.skip_probability = 1.0
        with patch('src.routine.routine.random.random', return_value=0.0):
            self.assertTrue(self.routine.should_skip_current_point())
            self.assertEqual(self.routine.consecutive_skips, 1)

    def test_backward_triggers_and_applies(self):
        self.routine.backward_enabled = True
        self.routine.backward_probability = 1.0
        self.routine.backward_range = (2, 2)
        self.routine.index = 2

        with patch('src.routine.routine.random.random', return_value=0.0), \
             patch('src.routine.routine.random.randint', return_value=2):
            should_back, steps = self.routine.should_backward()

        self.assertTrue(should_back)
        self.assertEqual(steps, 2)

        self.routine.apply_backward(steps)
        self.assertEqual(self.routine.index, 0)
        self.assertTrue(self.routine.is_backwarding_context)

    def test_variant_label_validation(self):
        label_f1 = Label('f1_pos_0')
        label_f1.set_index(0)
        self.routine.labels[label_f1.label] = label_f1
        self.assertFalse(self.routine._has_required_labels('reverse'))

        label_f2 = Label('f2_pos_1')
        label_f2.set_index(1)
        self.routine.labels[label_f2.label] = label_f2
        self.assertTrue(self.routine._has_required_labels('reverse'))

    def test_command_sequence_randomization_shuffle_skip_wait(self):
        point = Point(0.1, 0.2, adjust='False')
        point.commands = [BuffStub(), AttackStub(), SkillStub()]

        cfg = self.routine.command_randomization
        cfg.update({
            'enabled': True,
            'shuffle_probability': 1.0,
            'skip_probability': 0.5,
            'extra_wait_probability': 1.0,
            'extra_wait_range': (0.05, 0.05),
            'skip_blacklist': {'BuffStub'},
            'shuffle_blacklist': {'BuffStub'}
        })

        with patch('src.routine.components.random.random',
                   side_effect=[0.0, 0.0, 0.9, 0.0, 0.0]), \
             patch('src.routine.components.random.shuffle',
                   side_effect=lambda seq: seq.reverse()), \
             patch('src.routine.components.random.uniform', return_value=0.05):
            decisions = list(point._iter_commands(False, False))

        command_names = [d.command.__class__.__name__ for d in decisions]
        self.assertEqual(command_names, ['BuffStub', 'SkillStub', 'AttackStub'])

        self.assertIsNone(decisions[0].skip_reason)
        self.assertAlmostEqual(decisions[0].wait_duration, 0.05, places=3)

        self.assertIsNone(decisions[1].skip_reason)
        self.assertAlmostEqual(decisions[1].wait_duration, 0.05, places=3)

        self.assertEqual(decisions[2].skip_reason, 'probabilistic skip')
        self.assertIsNone(decisions[2].wait_duration)

    def test_iter_commands_skip_teleport_in_reverse(self):
        point = Point(0.1, 0.2, adjust='False')
        point.commands = [TeleportStub()]

        decisions = list(point._iter_commands(is_reverse_variant=True, is_floor_reverse=False))
        self.assertEqual(len(decisions), 1)
        self.assertIn('teleport disabled', decisions[0].skip_reason)

    def test_floor_descriptor_detection(self):
        label_a = Label('F1_LABEL')
        label_a.set_index(0)
        point_a = Point(0.1, 0.5, adjust='False')
        label_b = Label('F2_LABEL')
        label_b.set_index(2)
        point_b = Point(0.2, 0.05, adjust='False')

        self.routine.sequence = [label_a, point_a, label_b, point_b]
        self.routine.labels = {label_a.label: label_a, label_b.label: label_b}
        self.routine._load_floor_descriptor_config([
            {'id': 'floor1', 'labels': ['F1_LABEL'], 'priority': 10},
            {'id': 'floor2', 'y_range': (-1.0, 0.2), 'priority': 20}
        ])
        self.routine.detect_floors()

        self.assertEqual(self.routine.floor_indices_map.get('floor1'), [1])
        self.assertEqual(self.routine.floor_indices_map.get('floor2'), [3])

    def test_load_floor_metadata_overrides_config(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            routine_path = Path(tmpdir) / "dummy.csv"
            routine_path.write_text("Label,start_routine\n", encoding='utf-8')
            meta_path = Path(tmpdir) / "dummy.meta.json"
            meta_data = {
                "floor_descriptors": [
                    {"id": "upper", "labels": ["upper_label"], "priority": 1}
                ]
            }
            meta_path.write_text(json.dumps(meta_data), encoding='utf-8')

            self.routine._load_floor_descriptor_config([])
            self.routine._load_floor_metadata(str(routine_path))

            descriptor_ids = [d.floor_id for d in self.routine.floor_descriptors]
            self.assertIn("upper", descriptor_ids)

    def test_default_floor_descriptor_generation(self):
        self.routine._load_floor_descriptor_config(None)
        descriptors = self.routine.floor_descriptors
        ids = [d.floor_id for d in descriptors]
        self.assertIn('floor1', ids)
        self.assertIn('floor2', ids)

        label_a = Label('f1_pos_0')
        label_a.set_index(0)
        point_a = Point(0.11, 0.20, adjust='False')
        label_b = Label('f2_pos_1')
        label_b.set_index(2)
        point_b = Point(0.12, 0.03, adjust='False')
        self.routine.sequence = [label_a, point_a, label_b, point_b]
        self.routine.labels = {label_a.label: label_a, label_b.label: label_b}

        self.routine.detect_floors()
        self.assertEqual(self.routine.floor_indices_map.get('floor1'), [1])
        self.assertEqual(self.routine.floor_indices_map.get('floor2'), [3])

    def test_descriptor_with_only_y_range(self):
        point_a = Point(0.1, 0.50, adjust='False')
        point_b = Point(0.2, 0.00, adjust='False')
        self.routine.sequence = [point_a, point_b]

        self.routine._load_floor_descriptor_config([
            {'id': 'upper', 'y_range': (0.30, 1.0), 'priority': 5},
            {'id': 'lower', 'y_range': (-1.0, 0.20), 'priority': 10}
        ])
        self.routine.detect_floors()
        self.assertEqual(self.routine.floor_indices_map.get('upper'), [0])
        self.assertEqual(self.routine.floor_indices_map.get('lower'), [1])

    def test_get_current_floor_position_legacy_and_custom(self):
        descriptors = [
            {'id': 'floor1', 'labels': ['f1_label'], 'priority': 5},
            {'id': 'mezzanine', 'labels': ['mez_label'], 'priority': 10}
        ]
        self.routine._load_floor_descriptor_config(descriptors)

        label_floor = Label('f1_label')
        label_floor.set_index(0)
        point_floor = Point(0.1, 0.2, adjust='False')
        label_mez = Label('mez_label')
        label_mez.set_index(2)
        point_mez = Point(0.2, 0.25, adjust='False')
        self.routine.sequence = [label_floor, point_floor, label_mez, point_mez]
        self.routine.labels = {label_floor.label: label_floor, label_mez.label: label_mez}

        self.routine.detect_floors()
        legacy = self.routine.get_current_floor_position(1)
        self.assertEqual(legacy, ('f1', 0, 1))

        custom = self.routine.get_current_floor_position(3)
        self.assertEqual(custom, ('mezzanine', 0, 3))

    def test_load_floor_floor_json_metadata(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            routine_path = Path(tmpdir) / "dummy.csv"
            routine_path.write_text("Label,start_routine\n", encoding='utf-8')
            meta_path = Path(tmpdir) / "dummy.floor.json"
            meta_data = {"floor_descriptors": [{'id': 'roof', 'labels': ['roof_label'], 'priority': 3}]}
            meta_path.write_text(json.dumps(meta_data), encoding='utf-8')

            self.routine._load_floor_descriptor_config([])
            self.routine._load_floor_metadata(str(routine_path))
            descriptor_ids = [d.floor_id for d in self.routine.floor_descriptors]
            self.assertIn("roof", descriptor_ids)

    def test_invalid_descriptor_entries_are_skipped(self):
        self.routine._load_floor_descriptor_config([
            {'id': 'valid_floor', 'labels': ['label1'], 'priority': 1},
            {'labels': ['missing_id']},      # invalid
            {'id': 'bad_range', 'y_range': [0, 1, 2]},  # invalid range
            'not_a_dict'                     # invalid type
        ])
        descriptor_ids = [d.floor_id for d in self.routine.floor_descriptors]
        self.assertEqual(descriptor_ids, ['valid_floor'])

    def test_teleport_not_skipped_in_normal_variant(self):
        point = Point(0.1, 0.2, adjust='False')
        teleport_command = TeleportStub()
        point.commands = [teleport_command]

        decisions = list(point._iter_commands(is_reverse_variant=False, is_floor_reverse=False))
        self.assertEqual(len(decisions), 1)
        self.assertIsNone(decisions[0].skip_reason)

    def test_floor_variant_uses_descriptor(self):
        descriptors = [
            {'id': 'floor1', 'labels': ['f1'], 'priority': 5},
            {'id': 'floor2', 'labels': ['f2'], 'priority': 10}
        ]
        self.routine._load_floor_descriptor_config(descriptors)

        label_f1 = Label('f1')
        label_f1.set_index(0)
        point_f1 = Point(0.1, 0.2, adjust='False')
        label_f2 = Label('f2')
        label_f2.set_index(2)
        point_f2 = Point(0.3, 0.4, adjust='False')
        self.routine.sequence = [label_f1, point_f1, label_f2, point_f2]
        self.routine.labels = {label_f1.label: label_f1, label_f2.label: label_f2}

        self.routine.detect_floors()
        self.assertEqual(self.routine.floor_indices_map.get('floor1'), [1])
        self.assertEqual(self.routine.floor_indices_map.get('floor2'), [3])

    def test_position_offset_applies_within_bounds(self):
        self.routine.position_offset_config.update({
            'enabled': True,
            'range': 0.05,
            'axes': {'x': True, 'y': True}
        })
        original = (0.0, 1.0)
        offsets_before = self.routine.observability_metrics['offsets']
        for _ in range(5):
            new_location = self.routine.get_position_with_offset(original)
            self.assertGreaterEqual(new_location[0], 0.0)
            self.assertLessEqual(new_location[0], 1.0)
            self.assertGreaterEqual(new_location[1], 0.0)
            self.assertLessEqual(new_location[1], 1.0)
        self.assertGreater(
            self.routine.observability_metrics['offsets'],
            offsets_before
        )

    def test_bot_config_profile_switch(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "bot_config.json"
            sample_data = {
                "active_profile": "default",
                "defaults": {"foo": {"bar": 1}},
                "profiles": {
                    "default": {},
                    "custom": {"foo": {"bar": 5}}
                }
            }
            config_path.write_text(json.dumps(sample_data), encoding='utf-8')
            bot_cfg = BotConfig(config_path)
            self.assertEqual(bot_cfg.get("foo.bar"), 1)
            bot_cfg.active_profile = "custom"
            self.assertEqual(bot_cfg.get("foo.bar"), 5)
            bot_cfg.set("foo.baz", 42)
            self.assertEqual(bot_cfg.get("foo.baz"), 42)

    def test_get_feature_value_uses_bot_config_override(self):
        with patch.object(config, 'bot_config', BotConfig()) as _:
            config.bot_config.set("routine_randomization.point_selection.skip_probability", 0.33)
            from src.common.anti_detect_config import get_feature_value
            self.assertAlmostEqual(
                get_feature_value("routine_randomization.point_selection.skip_probability", 0.1),
                0.33
            )

    def test_routine_load_uses_bot_config_defaults(self):
        config.bot_config.set("routine_randomization.point_selection.enabled", True)
        config.bot_config.set("routine_randomization.movement.position_offset.enabled", True)
        config.bot_config.set("routine_randomization.movement.position_offset.range", 0.02)
        config.bot_config.set("routine_randomization.movement.observability.log_every_loops", 1)
        config.bot_config.set("routine_randomization.enabled", True)
        self.routine._apply_config_fallbacks()
        self.assertTrue(self.routine.skip_enabled)
        self.assertTrue(self.routine.position_offset_config['enabled'])
        self.assertEqual(self.routine.position_offset_config['range'], 0.02)
        self.assertEqual(self.routine.observability_config['log_every_loops'], 1)

    def test_observability_logging_snapshot(self):
        config.bot_config.set("routine_randomization.movement.observability.log_every_loops", 3)
        self.routine._apply_config_fallbacks()
        self.routine.observability_metrics['offsets'] = 2
        with patch('src.routine.routine.log.info') as mock_log:
            self.routine.loop_count = 1
            self.routine._log_observability_snapshot()
            mock_log.assert_not_called()
            self.routine.loop_count = 3
            self.routine._log_observability_snapshot()
            mock_log.assert_called()

    def test_load_floor_metadata_integration(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            routine_path = Path(tmpdir) / "routine.csv"
            routine_path.write_text("Label,start_routine\n", encoding='utf-8')
            meta_path = Path(tmpdir) / "routine.floor.json"
            meta_path.write_text(json.dumps({
                "floor_descriptors": [
                    {"id": "upper", "labels": ["up_label"], "priority": 1}
                ]
            }), encoding='utf-8')
            self.routine._load_floor_descriptor_config([])
            self.routine._load_floor_metadata(str(routine_path))
            descriptor_ids = [d.floor_id for d in self.routine.floor_descriptors]
            self.assertIn("upper", descriptor_ids)

    def test_bot_config_set_persist(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "bot_config.json"
            config_path.write_text(json.dumps({"defaults": {}, "profiles": {"default": {}}}), encoding='utf-8')
            bot_cfg = BotConfig(config_path)
            bot_cfg.set("foo.bar", 1, persist=True)
            loaded = json.loads(config_path.read_text(encoding='utf-8'))
            self.assertEqual(loaded["profiles"]["default"]["foo"]["bar"], 1)

    def test_get_feature_value_without_bot_config(self):
        from src.common.anti_detect_config import get_feature_value, ANTI_DETECT_CONFIG
        with patch.object(config, 'bot_config', None):
            expected = ANTI_DETECT_CONFIG['routine_randomization']['point_selection']['skip_probability']
            self.assertEqual(
                get_feature_value("routine_randomization.point_selection.skip_probability", 0.1),
                expected
            )


if __name__ == '__main__':
    unittest.main()

