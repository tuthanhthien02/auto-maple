import tkinter as tk
from src.gui.interfaces import LabelFrame, Frame
from src.common.interfaces import Configurable
from src.common.anti_detect_config import is_feature_enabled

# Constants for settings keys
POINT_SELECTION_KEY = "Point Selection Enabled"
POINT_SELECTION_PROBABILITY_KEY = "Point Selection Skip Probability"
RANDOM_BACKWARD_KEY = "Random Backward Enabled"
RANDOM_BACKWARD_PROBABILITY_KEY = "Random Backward Probability"
ROUTINE_PATTERN_KEY = "Routine Pattern Enabled"
ROUTINE_PATTERN_FLOOR_CHANCE_KEY = "Routine Pattern Floor Only Chance"
COMMAND_SEQUENCE_KEY = "Command Sequence Enabled"
POSITION_OFFSET_KEY = "Position Offset Enabled"
MICRO_GESTURE_KEY = "Micro Gesture Enabled"
DYNAMIC_PATHS_KEY = "Dynamic Paths Enabled"
DYNAMIC_PATHS_COUNT_KEY = "Dynamic Paths Count"
DYNAMIC_PATHS_STRATEGY_KEY = "Dynamic Paths Generation Strategy"
DYNAMIC_PATHS_SKIP_MIN_KEY = "Dynamic Paths Skip Min"
DYNAMIC_PATHS_SKIP_MAX_KEY = "Dynamic Paths Skip Max"
DYNAMIC_PATHS_SELECTION_MODE_KEY = "Dynamic Paths Selection Mode"
DYNAMIC_PATHS_SWITCH_MIN_KEY = "Dynamic Paths Switch Min Loops"
DYNAMIC_PATHS_SWITCH_MAX_KEY = "Dynamic Paths Switch Max Loops"
DYNAMIC_PATHS_STAY_PROBABILITY_KEY = "Dynamic Paths Stay Probability"

SCROLL_HEIGHT = 400


class RoutineRandomization(LabelFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, "Routine Randomization", **kwargs)

        self.settings = RoutineRandomizationSettings("routine_randomization")

        # Scrollable container to keep UI compact
        self._scroll_container = Frame(self)
        self._scroll_container.pack(
            side=tk.TOP, fill="both", expand=True, padx=0, pady=0
        )

        self._canvas = tk.Canvas(
            self._scroll_container, bd=0, highlightthickness=0, height=SCROLL_HEIGHT
        )
        self._canvas.pack(side=tk.LEFT, fill="both", expand=True)
        self._scrollbar = tk.Scrollbar(
            self._scroll_container, orient=tk.VERTICAL, command=self._canvas.yview
        )
        self._scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._canvas.configure(yscrollcommand=self._scrollbar.set)

        self._content = Frame(self._canvas)
        self._content.bind(
            "<Configure>",
            lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all")),
        )
        self._canvas.create_window((0, 0), window=self._content, anchor=tk.NW)

        # Point Selection Randomization Panel
        self.point_selection_frame = LabelFrame(
            self._content, "Point Selection Randomization"
        )
        self.point_selection_frame.pack(
            side=tk.TOP, fill="x", expand=True, padx=5, pady=5
        )

        # Load settings with validation
        point_enabled = self.settings.get(POINT_SELECTION_KEY)
        if not isinstance(point_enabled, bool):
            point_enabled = False

        point_probability = self.settings.get(POINT_SELECTION_PROBABILITY_KEY)
        # Validate and convert probability
        try:
            if isinstance(point_probability, str) and point_probability == "":
                point_probability = 0.30  # Default
            else:
                point_probability = float(point_probability)
                if point_probability < 0 or point_probability > 1:
                    point_probability = 0.30  # Default
        except (ValueError, TypeError):
            point_probability = 0.30  # Default

        # Point Selection: Enable checkbox
        self.point_var = tk.BooleanVar(value=point_enabled)
        point_check = tk.Checkbutton(
            self.point_selection_frame,
            variable=self.point_var,
            text="Enable Point Selection Randomization",
            command=self._on_point_change,
        )
        point_check.pack(side=tk.TOP, anchor="w", padx=5, pady=2)

        # Point Selection: Skip Probability slider
        prob_row = Frame(self.point_selection_frame)
        prob_row.pack(side=tk.TOP, fill="x", expand=True, padx=5, pady=(0, 5))

        prob_label = tk.Label(prob_row, text="Skip Probability:")
        prob_label.pack(side=tk.LEFT, padx=(0, 10))

        self.point_probability_var = tk.IntVar(value=int(point_probability * 100))
        prob_slider = tk.Scale(
            prob_row,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.point_probability_var,
            command=self._on_point_probability_change,
            length=150,
        )
        prob_slider.pack(side=tk.LEFT, padx=(0, 5))

        self.point_probability_label = tk.Label(
            prob_row, text=f"{int(point_probability * 100)}%"
        )
        self.point_probability_label.pack(side=tk.LEFT)

        # Random Move Backward Panel
        self.random_backward_frame = LabelFrame(self._content, "Random Move Backward")
        self.random_backward_frame.pack(
            side=tk.TOP, fill="x", expand=True, padx=5, pady=5
        )

        # Load settings with validation
        backward_enabled = self.settings.get(RANDOM_BACKWARD_KEY)
        if not isinstance(backward_enabled, bool):
            backward_enabled = False

        backward_probability = self.settings.get(RANDOM_BACKWARD_PROBABILITY_KEY)
        # Validate and convert probability
        try:
            if isinstance(backward_probability, str) and backward_probability == "":
                backward_probability = 0.10  # Default
            else:
                backward_probability = float(backward_probability)
                if backward_probability < 0 or backward_probability > 1:
                    backward_probability = 0.10  # Default
        except (ValueError, TypeError):
            backward_probability = 0.10  # Default

        # Random Backward: Enable checkbox
        self.backward_var = tk.BooleanVar(value=backward_enabled)
        backward_check = tk.Checkbutton(
            self.random_backward_frame,
            variable=self.backward_var,
            text="Enable Random Move Backward",
            command=self._on_backward_change,
        )
        backward_check.pack(side=tk.TOP, anchor="w", padx=5, pady=2)

        # Random Backward: Backward Probability slider
        backward_prob_row = Frame(self.random_backward_frame)
        backward_prob_row.pack(side=tk.TOP, fill="x", expand=True, padx=5, pady=(0, 5))

        backward_prob_label = tk.Label(backward_prob_row, text="Backward Probability:")
        backward_prob_label.pack(side=tk.LEFT, padx=(0, 10))

        self.backward_probability_var = tk.IntVar(value=int(backward_probability * 100))
        backward_prob_slider = tk.Scale(
            backward_prob_row,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.backward_probability_var,
            command=self._on_backward_probability_change,
            length=150,
        )
        backward_prob_slider.pack(side=tk.LEFT, padx=(0, 5))

        self.backward_probability_label = tk.Label(
            backward_prob_row, text=f"{int(backward_probability * 100)}%"
        )
        self.backward_probability_label.pack(side=tk.LEFT)

        # Routine Pattern Variation Panel
        self.routine_pattern_frame = LabelFrame(
            self._content, "Routine Pattern Variation"
        )
        self.routine_pattern_frame.pack(
            side=tk.TOP, fill="x", expand=True, padx=5, pady=5
        )

        # Load settings with validation
        pattern_enabled = self.settings.get(ROUTINE_PATTERN_KEY)
        if not isinstance(pattern_enabled, bool):
            pattern_enabled = False

        floor_chance = self.settings.get(ROUTINE_PATTERN_FLOOR_CHANCE_KEY)
        # Validate and convert chance
        try:
            if isinstance(floor_chance, str) and floor_chance == "":
                floor_chance = 0.10  # Default
            else:
                floor_chance = float(floor_chance)
                if floor_chance < 0 or floor_chance > 1:
                    floor_chance = 0.10  # Default
        except (ValueError, TypeError):
            floor_chance = 0.10  # Default

        # Routine Pattern: Enable checkbox
        self.pattern_var = tk.BooleanVar(value=pattern_enabled)
        pattern_check = tk.Checkbutton(
            self.routine_pattern_frame,
            variable=self.pattern_var,
            text="Enable Routine Pattern Variation",
            command=self._on_pattern_change,
        )
        pattern_check.pack(side=tk.TOP, anchor="w", padx=5, pady=2)

        # Routine Pattern: Floor-Only Activation Chance slider
        chance_row = Frame(self.routine_pattern_frame)
        chance_row.pack(side=tk.TOP, fill="x", expand=True, padx=5, pady=(0, 5))

        chance_label = tk.Label(chance_row, text="Floor-Only Activation Chance:")
        chance_label.pack(side=tk.LEFT, padx=(0, 10))

        self.floor_chance_var = tk.IntVar(value=int(floor_chance * 100))
        chance_slider = tk.Scale(
            chance_row,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.floor_chance_var,
            command=self._on_floor_chance_change,
            length=150,
        )
        chance_slider.pack(side=tk.LEFT, padx=(0, 5))

        self.floor_chance_label = tk.Label(
            chance_row, text=f"{int(floor_chance * 100)}%"
        )
        self.floor_chance_label.pack(side=tk.LEFT)

        # Command Sequence Randomization Panel
        self.command_sequence_frame = LabelFrame(
            self._content, "Command Sequence Randomization"
        )
        self.command_sequence_frame.pack(
            side=tk.TOP, fill="x", expand=True, padx=5, pady=5
        )

        command_enabled = self._load_bool_setting(
            COMMAND_SEQUENCE_KEY, "routine_randomization.command_sequence.enabled"
        )
        self.command_sequence_var = tk.BooleanVar(value=command_enabled)
        command_check = tk.Checkbutton(
            self.command_sequence_frame,
            variable=self.command_sequence_var,
            text="Enable Command Sequence Randomization",
            command=self._on_command_sequence_change,
        )
        command_check.pack(side=tk.TOP, anchor="w", padx=5, pady=2)

        # Movement Randomization Panel
        self.movement_frame = LabelFrame(self._content, "Movement Randomization")
        self.movement_frame.pack(side=tk.TOP, fill="x", expand=True, padx=5, pady=5)

        position_enabled = self._load_bool_setting(
            POSITION_OFFSET_KEY,
            "routine_randomization.movement.position_offset.enabled",
        )
        self.position_offset_var = tk.BooleanVar(value=position_enabled)
        position_check = tk.Checkbutton(
            self.movement_frame,
            variable=self.position_offset_var,
            text="Enable Position Offset",
            command=self._on_position_offset_change,
        )
        position_check.pack(side=tk.TOP, anchor="w", padx=5, pady=2)

        micro_enabled = self._load_bool_setting(
            MICRO_GESTURE_KEY, "routine_randomization.movement.micro_gesture.enabled"
        )
        self.micro_gesture_var = tk.BooleanVar(value=micro_enabled)
        micro_check = tk.Checkbutton(
            self.movement_frame,
            variable=self.micro_gesture_var,
            text="Enable Micro Gesture",
            command=self._on_micro_gesture_change,
        )
        micro_check.pack(side=tk.TOP, anchor="w", padx=5, pady=2)

        # Dynamic Paths Panel
        self.dynamic_paths_frame = LabelFrame(self._content, "Dynamic Paths")
        self.dynamic_paths_frame.pack(
            side=tk.TOP, fill="x", expand=True, padx=5, pady=5
        )

        dynamic_paths_enabled = self._load_bool_setting(
            DYNAMIC_PATHS_KEY, "routine_randomization.dynamic_paths.enabled"
        )
        self.dynamic_paths_var = tk.BooleanVar(value=dynamic_paths_enabled)
        dynamic_paths_check = tk.Checkbutton(
            self.dynamic_paths_frame,
            variable=self.dynamic_paths_var,
            text="Enable Dynamic Paths",
            command=self._on_dynamic_paths_change,
        )
        dynamic_paths_check.pack(side=tk.TOP, anchor="w", padx=5, pady=2)

        # Path Count
        count_row = Frame(self.dynamic_paths_frame)
        count_row.pack(side=tk.TOP, fill="x", expand=True, padx=5, pady=2)

        count_label = tk.Label(count_row, text="Path Count:")
        count_label.pack(side=tk.LEFT, padx=(0, 10))

        path_count = self._load_int_setting(
            DYNAMIC_PATHS_COUNT_KEY, "routine_randomization.dynamic_paths.path_count", 4
        )
        self.path_count_var = tk.IntVar(value=path_count)
        count_slider = tk.Scale(
            count_row,
            from_=2,
            to=10,
            orient=tk.HORIZONTAL,
            variable=self.path_count_var,
            command=self._on_path_count_change,
            length=150,
        )
        count_slider.pack(side=tk.LEFT, padx=(0, 5))

        self.path_count_label = tk.Label(count_row, text=f"{path_count}")
        self.path_count_label.pack(side=tk.LEFT)

        # Generation Strategy
        strategy_row = Frame(self.dynamic_paths_frame)
        strategy_row.pack(side=tk.TOP, fill="x", expand=True, padx=5, pady=2)

        strategy_label = tk.Label(strategy_row, text="Generation Strategy:")
        strategy_label.pack(side=tk.LEFT, padx=(0, 10))

        strategy_value = self._load_str_setting(
            DYNAMIC_PATHS_STRATEGY_KEY,
            "routine_randomization.dynamic_paths.generation_strategy",
            "random_skip",
        )
        self.strategy_var = tk.StringVar(value=strategy_value)
        strategy_menu = tk.OptionMenu(
            strategy_row,
            self.strategy_var,
            "random_skip",
            "partial",
            "mixed",
            command=self._on_strategy_change,
        )
        strategy_menu.pack(side=tk.LEFT)

        # Skip Percentage Range
        skip_row = Frame(self.dynamic_paths_frame)
        skip_row.pack(side=tk.TOP, fill="x", expand=True, padx=5, pady=2)

        skip_label = tk.Label(skip_row, text="Skip Range:")
        skip_label.pack(side=tk.LEFT, padx=(0, 10))

        skip_min = self._load_float_setting(
            DYNAMIC_PATHS_SKIP_MIN_KEY,
            "routine_randomization.dynamic_paths.skip_percentage_range[0]",
            0.1,
        )
        skip_max = self._load_float_setting(
            DYNAMIC_PATHS_SKIP_MAX_KEY,
            "routine_randomization.dynamic_paths.skip_percentage_range[1]",
            0.3,
        )

        self.skip_min_var = tk.IntVar(value=int(skip_min * 100))
        self.skip_max_var = tk.IntVar(value=int(skip_max * 100))

        skip_min_slider = tk.Scale(
            skip_row,
            from_=0,
            to=90,
            orient=tk.HORIZONTAL,
            variable=self.skip_min_var,
            command=self._on_skip_range_change,
            length=100,
            label="Min",
        )
        skip_min_slider.pack(side=tk.LEFT, padx=(0, 5))

        skip_max_slider = tk.Scale(
            skip_row,
            from_=0,
            to=90,
            orient=tk.HORIZONTAL,
            variable=self.skip_max_var,
            command=self._on_skip_range_change,
            length=100,
            label="Max",
        )
        skip_max_slider.pack(side=tk.LEFT, padx=(0, 5))

        self.skip_range_label = tk.Label(
            skip_row, text=f"{int(skip_min * 100)}%-{int(skip_max * 100)}%"
        )
        self.skip_range_label.pack(side=tk.LEFT)

        # Selection Mode
        selection_row = Frame(self.dynamic_paths_frame)
        selection_row.pack(side=tk.TOP, fill="x", expand=True, padx=5, pady=2)

        selection_label = tk.Label(selection_row, text="Selection Mode:")
        selection_label.pack(side=tk.LEFT, padx=(0, 10))

        selection_value = self._load_str_setting(
            DYNAMIC_PATHS_SELECTION_MODE_KEY,
            "routine_randomization.dynamic_paths.selection_mode",
            "transition_matrix",
        )
        self.selection_mode_var = tk.StringVar(value=selection_value)
        selection_menu = tk.OptionMenu(
            selection_row,
            self.selection_mode_var,
            "random",
            "weighted",
            "transition_matrix",
            "sequential",
            command=self._on_selection_mode_change,
        )
        selection_menu.pack(side=tk.LEFT)

        # Switch Interval
        switch_row = Frame(self.dynamic_paths_frame)
        switch_row.pack(side=tk.TOP, fill="x", expand=True, padx=5, pady=2)

        switch_label = tk.Label(switch_row, text="Switch Interval:")
        switch_label.pack(side=tk.LEFT, padx=(0, 10))

        switch_min = self._load_int_setting(
            DYNAMIC_PATHS_SWITCH_MIN_KEY,
            "routine_randomization.dynamic_paths.switch_interval.min_loops",
            2,
        )
        switch_max = self._load_int_setting(
            DYNAMIC_PATHS_SWITCH_MAX_KEY,
            "routine_randomization.dynamic_paths.switch_interval.max_loops",
            5,
        )

        self.switch_min_var = tk.IntVar(value=switch_min)
        self.switch_max_var = tk.IntVar(value=switch_max)

        switch_min_slider = tk.Scale(
            switch_row,
            from_=1,
            to=10,
            orient=tk.HORIZONTAL,
            variable=self.switch_min_var,
            command=self._on_switch_interval_change,
            length=100,
            label="Min",
        )
        switch_min_slider.pack(side=tk.LEFT, padx=(0, 5))

        switch_max_slider = tk.Scale(
            switch_row,
            from_=1,
            to=10,
            orient=tk.HORIZONTAL,
            variable=self.switch_max_var,
            command=self._on_switch_interval_change,
            length=100,
            label="Max",
        )
        switch_max_slider.pack(side=tk.LEFT, padx=(0, 5))

        self.switch_interval_label = tk.Label(
            switch_row, text=f"{switch_min}-{switch_max} loops"
        )
        self.switch_interval_label.pack(side=tk.LEFT)

        # Stay Probability (only shown when selection_mode is transition_matrix)
        stay_prob_row = Frame(self.dynamic_paths_frame)
        stay_prob_row.pack(side=tk.TOP, fill="x", expand=True, padx=5, pady=2)

        stay_prob_label = tk.Label(stay_prob_row, text="Stay Probability:")
        stay_prob_label.pack(side=tk.LEFT, padx=(0, 10))

        stay_probability = self._load_float_setting(
            DYNAMIC_PATHS_STAY_PROBABILITY_KEY,
            "routine_randomization.dynamic_paths.transition_matrix.stay_probability",
            0.2,
        )
        self.stay_probability_var = tk.IntVar(value=int(stay_probability * 100))
        stay_prob_slider = tk.Scale(
            stay_prob_row,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.stay_probability_var,
            command=self._on_stay_probability_change,
            length=150,
        )
        stay_prob_slider.pack(side=tk.LEFT, padx=(0, 5))

        self.stay_probability_label = tk.Label(
            stay_prob_row, text=f"{int(stay_probability * 100)}%"
        )
        self.stay_probability_label.pack(side=tk.LEFT)

        # Sync với anti_detect_config và routine khi load
        self._sync_to_anti_detect()
        self._sync_to_routine()

    def _load_bool_setting(self, settings_key, feature_path, default=False):
        try:
            value = bool(is_feature_enabled(feature_path))
        except Exception:
            value = default
        self.settings.set(settings_key, value)
        return value

    def _load_int_setting(self, settings_key, feature_path, default):
        try:
            from src.common.anti_detect_config import get_feature_value

            value = int(get_feature_value(feature_path, default))
        except Exception:
            value = default
        self.settings.set(settings_key, value)
        return value

    def _load_float_setting(self, settings_key, feature_path, default):
        try:
            from src.common.anti_detect_config import get_feature_value

            value = float(get_feature_value(feature_path, default))
        except Exception:
            value = default
        self.settings.set(settings_key, value)
        return value

    def _load_str_setting(self, settings_key, feature_path, default):
        try:
            from src.common.anti_detect_config import get_feature_value

            value = str(get_feature_value(feature_path, default))
        except Exception:
            value = default
        self.settings.set(settings_key, value)
        return value

    def _on_point_change(self):
        """Handle Point Selection enable/disable change."""
        enabled = self.point_var.get()
        self.settings.set(POINT_SELECTION_KEY, enabled)
        self.settings.save_config()
        self._set_bot_config_bool(
            "routine_randomization.point_selection.enabled", enabled
        )
        self._sync_to_anti_detect()
        self._sync_to_routine()

    def _on_point_probability_change(self, value):
        """Handle Point Selection probability change."""
        probability = int(value) / 100.0
        self.point_probability_label.config(text=f"{int(value)}%")
        self.settings.set(POINT_SELECTION_PROBABILITY_KEY, probability)
        self.settings.save_config()
        self._sync_to_routine()

    def _on_pattern_change(self):
        """Handle Routine Pattern enable/disable change."""
        enabled = self.pattern_var.get()
        self.settings.set(ROUTINE_PATTERN_KEY, enabled)
        self.settings.save_config()
        self._set_bot_config_bool(
            "routine_randomization.routine_pattern.enabled", enabled
        )
        self._sync_to_anti_detect()
        self._sync_to_routine()

    def _on_floor_chance_change(self, value):
        """Handle Floor-Only activation chance change."""
        chance = int(value) / 100.0
        self.floor_chance_label.config(text=f"{int(value)}%")
        self.settings.set(ROUTINE_PATTERN_FLOOR_CHANCE_KEY, chance)
        self.settings.save_config()
        self._sync_to_routine()

    def _on_backward_change(self):
        """Handle Random Backward enable/disable change."""
        enabled = self.backward_var.get()
        self.settings.set(RANDOM_BACKWARD_KEY, enabled)
        self.settings.save_config()
        self._set_bot_config_bool(
            "routine_randomization.random_backward.enabled", enabled
        )
        self._sync_to_anti_detect()
        self._sync_to_routine()

    def _on_backward_probability_change(self, value):
        """Handle Random Backward probability change."""
        probability = int(value) / 100.0
        self.backward_probability_label.config(text=f"{int(value)}%")
        self.settings.set(RANDOM_BACKWARD_PROBABILITY_KEY, probability)
        self.settings.save_config()
        self._sync_to_routine()

    def _on_command_sequence_change(self):
        """Handle Command Sequence enable/disable change."""
        enabled = self.command_sequence_var.get()
        self.settings.set(COMMAND_SEQUENCE_KEY, enabled)
        self.settings.save_config()
        self._set_bot_config_bool(
            "routine_randomization.command_sequence.enabled", enabled
        )
        self._sync_to_anti_detect()
        self._sync_to_routine()

    def _on_position_offset_change(self):
        """Handle Position Offset enable/disable change."""
        enabled = self.position_offset_var.get()
        self.settings.set(POSITION_OFFSET_KEY, enabled)
        self.settings.save_config()
        self._set_bot_config_bool(
            "routine_randomization.movement.position_offset.enabled", enabled
        )
        self._sync_to_anti_detect()
        self._sync_to_routine()

    def _on_micro_gesture_change(self):
        """Handle Micro Gesture enable/disable change."""
        enabled = self.micro_gesture_var.get()
        self.settings.set(MICRO_GESTURE_KEY, enabled)
        self.settings.save_config()
        self._set_bot_config_bool(
            "routine_randomization.movement.micro_gesture.enabled", enabled
        )
        self._sync_to_anti_detect()
        self._sync_to_routine()

    def _on_dynamic_paths_change(self):
        """Handle Dynamic Paths enable/disable change."""
        enabled = self.dynamic_paths_var.get()
        self.settings.set(DYNAMIC_PATHS_KEY, enabled)
        self.settings.save_config()
        self._set_bot_config_bool(
            "routine_randomization.dynamic_paths.enabled", enabled
        )
        self._sync_to_anti_detect()
        self._sync_to_routine()

    def _on_path_count_change(self, value):
        """Handle Path Count change."""
        count = int(value)
        self.path_count_label.config(text=f"{count}")
        self.settings.set(DYNAMIC_PATHS_COUNT_KEY, count)
        self.settings.save_config()
        self._sync_to_routine()

    def _on_strategy_change(self, value):
        """Handle Generation Strategy change."""
        self.settings.set(DYNAMIC_PATHS_STRATEGY_KEY, value)
        self.settings.save_config()
        self._sync_to_routine()

    def _on_skip_range_change(self, value):
        """Handle Skip Range change."""
        skip_min = self.skip_min_var.get() / 100.0
        skip_max = self.skip_max_var.get() / 100.0
        if skip_min > skip_max:
            skip_min, skip_max = skip_max, skip_min
        self.skip_range_label.config(
            text=f"{int(skip_min * 100)}%-{int(skip_max * 100)}%"
        )
        self.settings.set(DYNAMIC_PATHS_SKIP_MIN_KEY, skip_min)
        self.settings.set(DYNAMIC_PATHS_SKIP_MAX_KEY, skip_max)
        self.settings.save_config()
        self._sync_to_routine()

    def _on_selection_mode_change(self, value):
        """Handle Selection Mode change."""
        self.settings.set(DYNAMIC_PATHS_SELECTION_MODE_KEY, value)
        self.settings.save_config()
        self._sync_to_routine()

    def _on_switch_interval_change(self, value):
        """Handle Switch Interval change."""
        switch_min = self.switch_min_var.get()
        switch_max = self.switch_max_var.get()
        if switch_min > switch_max:
            switch_min, switch_max = switch_max, switch_min
        self.switch_interval_label.config(text=f"{switch_min}-{switch_max} loops")
        self.settings.set(DYNAMIC_PATHS_SWITCH_MIN_KEY, switch_min)
        self.settings.set(DYNAMIC_PATHS_SWITCH_MAX_KEY, switch_max)
        self.settings.save_config()
        self._sync_to_routine()

    def _on_stay_probability_change(self, value):
        """Handle Stay Probability change."""
        probability = int(value) / 100.0
        self.stay_probability_label.config(text=f"{int(value)}%")
        self.settings.set(DYNAMIC_PATHS_STAY_PROBABILITY_KEY, probability)
        self.settings.save_config()
        self._sync_to_routine()

    def _set_bot_config_bool(self, feature_path, value):
        try:
            from src.common import config

            config.bot_config.set(feature_path, bool(value), persist=True)
        except Exception:
            pass

    def _sync_to_anti_detect(self):
        """Sync settings to ANTI_DETECT_CONFIG."""
        from src.common.anti_detect_config import ANTI_DETECT_CONFIG

        ANTI_DETECT_CONFIG["routine_randomization"]["point_selection"]["enabled"] = (
            self.settings.get(POINT_SELECTION_KEY)
        )
        ANTI_DETECT_CONFIG["routine_randomization"]["routine_pattern"]["enabled"] = (
            self.settings.get(ROUTINE_PATTERN_KEY)
        )
        ANTI_DETECT_CONFIG["routine_randomization"]["routine_pattern"][
            "floor_variant_chance"
        ] = self.settings.get(ROUTINE_PATTERN_FLOOR_CHANCE_KEY)
        ANTI_DETECT_CONFIG["routine_randomization"]["command_sequence"]["enabled"] = (
            self.settings.get(COMMAND_SEQUENCE_KEY)
        )
        ANTI_DETECT_CONFIG["routine_randomization"]["movement"]["position_offset"][
            "enabled"
        ] = self.settings.get(POSITION_OFFSET_KEY)
        ANTI_DETECT_CONFIG["routine_randomization"]["movement"]["micro_gesture"][
            "enabled"
        ] = self.settings.get(MICRO_GESTURE_KEY)
        ANTI_DETECT_CONFIG["routine_randomization"]["dynamic_paths"]["enabled"] = (
            self.settings.get(DYNAMIC_PATHS_KEY)
        )

    def _sync_to_routine(self):
        """Sync settings to config.routine object."""
        try:
            from src.common import config

            if hasattr(config, "routine") and config.routine is not None:
                # Update Point Selection settings
                config.routine.skip_enabled = self.settings.get(POINT_SELECTION_KEY)
                config.routine.skip_probability = self.settings.get(
                    POINT_SELECTION_PROBABILITY_KEY
                )

                # Update Random Backward settings
                config.routine.backward_enabled = self.settings.get(RANDOM_BACKWARD_KEY)
                config.routine.backward_probability = self.settings.get(
                    RANDOM_BACKWARD_PROBABILITY_KEY
                )

                # Update Routine Pattern settings
                config.routine.variant_enabled = self.settings.get(ROUTINE_PATTERN_KEY)
                config.routine.floor_variant_chance = self.settings.get(
                    ROUTINE_PATTERN_FLOOR_CHANCE_KEY
                )
                # Update command sequence toggle
                config.routine.command_randomization["enabled"] = self.settings.get(
                    COMMAND_SEQUENCE_KEY
                )
                # Update movement toggles
                config.routine.position_offset_config["enabled"] = self.settings.get(
                    POSITION_OFFSET_KEY
                )
                config.routine.micro_gesture_config["enabled"] = self.settings.get(
                    MICRO_GESTURE_KEY
                )

                # Update Dynamic Paths settings
                config.routine.dynamic_paths_enabled = self.settings.get(
                    DYNAMIC_PATHS_KEY
                )
                if config.routine.dynamic_paths_enabled:
                    config.routine.dynamic_paths_config["path_count"] = (
                        self.settings.get(DYNAMIC_PATHS_COUNT_KEY)
                    )
                    config.routine.dynamic_paths_config["generation_strategy"] = (
                        self.settings.get(DYNAMIC_PATHS_STRATEGY_KEY)
                    )
                    config.routine.dynamic_paths_config["skip_percentage_range"] = (
                        self.settings.get(DYNAMIC_PATHS_SKIP_MIN_KEY),
                        self.settings.get(DYNAMIC_PATHS_SKIP_MAX_KEY),
                    )
                    config.routine.dynamic_paths_config["selection_mode"] = (
                        self.settings.get(DYNAMIC_PATHS_SELECTION_MODE_KEY)
                    )
                    config.routine.dynamic_paths_config["switch_interval"] = {
                        "min_loops": self.settings.get(DYNAMIC_PATHS_SWITCH_MIN_KEY),
                        "max_loops": self.settings.get(DYNAMIC_PATHS_SWITCH_MAX_KEY),
                    }
                    # Update transition_matrix stay_probability
                    if "transition_matrix" not in config.routine.dynamic_paths_config:
                        config.routine.dynamic_paths_config["transition_matrix"] = {}
                    config.routine.dynamic_paths_config["transition_matrix"][
                        "stay_probability"
                    ] = self.settings.get(DYNAMIC_PATHS_STAY_PROBABILITY_KEY)
                    # Regenerate paths if routine is loaded
                    if config.routine.sequence:
                        config.routine._generate_dynamic_paths()
                        if config.routine.dynamic_paths:
                            config.routine._generate_transition_matrix()
                            if not config.routine.current_path_id:
                                config.routine._select_initial_path()
        except Exception:
            # Routine might not be loaded yet, ignore
            pass


class RoutineRandomizationSettings(Configurable):
    DEFAULT_CONFIG = {
        POINT_SELECTION_KEY: False,  # DISABLED by default
        POINT_SELECTION_PROBABILITY_KEY: 0.10,  # 10% default
        RANDOM_BACKWARD_KEY: False,  # DISABLED by default
        RANDOM_BACKWARD_PROBABILITY_KEY: 0.10,  # 10% default
        ROUTINE_PATTERN_KEY: False,  # DISABLED by default
        ROUTINE_PATTERN_FLOOR_CHANCE_KEY: 0.10,  # 10% default
        COMMAND_SEQUENCE_KEY: False,  # DISABLED by default
        POSITION_OFFSET_KEY: False,  # DISABLED by default
        MICRO_GESTURE_KEY: False,  # DISABLED by default
        DYNAMIC_PATHS_KEY: False,  # DISABLED by default
        DYNAMIC_PATHS_COUNT_KEY: 4,
        DYNAMIC_PATHS_STRATEGY_KEY: "random_skip",
        DYNAMIC_PATHS_SKIP_MIN_KEY: 0.1,
        DYNAMIC_PATHS_SKIP_MAX_KEY: 0.3,
        DYNAMIC_PATHS_SELECTION_MODE_KEY: "transition_matrix",
        DYNAMIC_PATHS_SWITCH_MIN_KEY: 2,
        DYNAMIC_PATHS_SWITCH_MAX_KEY: 5,
        DYNAMIC_PATHS_STAY_PROBABILITY_KEY: 0.2,  # 20% stay, 80% switch
    }

    def get(self, key):
        return self.config[key]

    def set(self, key, value):
        assert key in self.config
        self.config[key] = value
