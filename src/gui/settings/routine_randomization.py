import tkinter as tk
from src.gui.interfaces import LabelFrame, Frame
from src.common.interfaces import Configurable

# Constants for settings keys
POINT_SELECTION_KEY = 'Point Selection Enabled'
POINT_SELECTION_PROBABILITY_KEY = 'Point Selection Skip Probability'
RANDOM_BACKWARD_KEY = 'Random Backward Enabled'
RANDOM_BACKWARD_PROBABILITY_KEY = 'Random Backward Probability'
ROUTINE_PATTERN_KEY = 'Routine Pattern Enabled'
ROUTINE_PATTERN_FLOOR_CHANCE_KEY = 'Routine Pattern Floor Only Chance'


class RoutineRandomization(LabelFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, 'Routine Randomization', **kwargs)

        self.settings = RoutineRandomizationSettings('routine_randomization')

        # Point Selection Randomization Panel
        self.point_selection_frame = LabelFrame(self, 'Point Selection Randomization')
        self.point_selection_frame.pack(side=tk.TOP, fill='x', expand=True, padx=5, pady=5)

        # Load settings with validation
        point_enabled = self.settings.get(POINT_SELECTION_KEY)
        if not isinstance(point_enabled, bool):
            point_enabled = False
        
        point_probability = self.settings.get(POINT_SELECTION_PROBABILITY_KEY)
        # Validate and convert probability
        try:
            if isinstance(point_probability, str) and point_probability == '':
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
            text='Enable Point Selection Randomization',
            command=self._on_point_change
        )
        point_check.pack(side=tk.TOP, anchor='w', padx=5, pady=2)

        # Point Selection: Skip Probability slider
        prob_row = Frame(self.point_selection_frame)
        prob_row.pack(side=tk.TOP, fill='x', expand=True, padx=5, pady=(0, 5))
        
        prob_label = tk.Label(prob_row, text='Skip Probability:')
        prob_label.pack(side=tk.LEFT, padx=(0, 10))

        self.point_probability_var = tk.IntVar(value=int(point_probability * 100))
        prob_slider = tk.Scale(
            prob_row,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.point_probability_var,
            command=self._on_point_probability_change,
            length=150
        )
        prob_slider.pack(side=tk.LEFT, padx=(0, 5))

        self.point_probability_label = tk.Label(prob_row, text=f'{int(point_probability * 100)}%')
        self.point_probability_label.pack(side=tk.LEFT)

        # Random Move Backward Panel
        self.random_backward_frame = LabelFrame(self, 'Random Move Backward')
        self.random_backward_frame.pack(side=tk.TOP, fill='x', expand=True, padx=5, pady=5)

        # Load settings with validation
        backward_enabled = self.settings.get(RANDOM_BACKWARD_KEY)
        if not isinstance(backward_enabled, bool):
            backward_enabled = False
        
        backward_probability = self.settings.get(RANDOM_BACKWARD_PROBABILITY_KEY)
        # Validate and convert probability
        try:
            if isinstance(backward_probability, str) and backward_probability == '':
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
            text='Enable Random Move Backward',
            command=self._on_backward_change
        )
        backward_check.pack(side=tk.TOP, anchor='w', padx=5, pady=2)

        # Random Backward: Backward Probability slider
        backward_prob_row = Frame(self.random_backward_frame)
        backward_prob_row.pack(side=tk.TOP, fill='x', expand=True, padx=5, pady=(0, 5))
        
        backward_prob_label = tk.Label(backward_prob_row, text='Backward Probability:')
        backward_prob_label.pack(side=tk.LEFT, padx=(0, 10))

        self.backward_probability_var = tk.IntVar(value=int(backward_probability * 100))
        backward_prob_slider = tk.Scale(
            backward_prob_row,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.backward_probability_var,
            command=self._on_backward_probability_change,
            length=150
        )
        backward_prob_slider.pack(side=tk.LEFT, padx=(0, 5))

        self.backward_probability_label = tk.Label(backward_prob_row, text=f'{int(backward_probability * 100)}%')
        self.backward_probability_label.pack(side=tk.LEFT)

        # Routine Pattern Variation Panel
        self.routine_pattern_frame = LabelFrame(self, 'Routine Pattern Variation')
        self.routine_pattern_frame.pack(side=tk.TOP, fill='x', expand=True, padx=5, pady=5)

        # Load settings with validation
        pattern_enabled = self.settings.get(ROUTINE_PATTERN_KEY)
        if not isinstance(pattern_enabled, bool):
            pattern_enabled = False
        
        floor_chance = self.settings.get(ROUTINE_PATTERN_FLOOR_CHANCE_KEY)
        # Validate and convert chance
        try:
            if isinstance(floor_chance, str) and floor_chance == '':
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
            text='Enable Routine Pattern Variation',
            command=self._on_pattern_change
        )
        pattern_check.pack(side=tk.TOP, anchor='w', padx=5, pady=2)

        # Routine Pattern: Floor-Only Activation Chance slider
        chance_row = Frame(self.routine_pattern_frame)
        chance_row.pack(side=tk.TOP, fill='x', expand=True, padx=5, pady=(0, 5))
        
        chance_label = tk.Label(chance_row, text='Floor-Only Activation Chance:')
        chance_label.pack(side=tk.LEFT, padx=(0, 10))

        self.floor_chance_var = tk.IntVar(value=int(floor_chance * 100))
        chance_slider = tk.Scale(
            chance_row,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.floor_chance_var,
            command=self._on_floor_chance_change,
            length=150
        )
        chance_slider.pack(side=tk.LEFT, padx=(0, 5))

        self.floor_chance_label = tk.Label(chance_row, text=f'{int(floor_chance * 100)}%')
        self.floor_chance_label.pack(side=tk.LEFT)

        # Sync với anti_detect_config và routine khi load
        self._sync_to_anti_detect()
        self._sync_to_routine()

    def _on_point_change(self):
        """Handle Point Selection enable/disable change."""
        enabled = self.point_var.get()
        self.settings.set(POINT_SELECTION_KEY, enabled)
        self.settings.save_config()
        self._sync_to_anti_detect()
        self._sync_to_routine()

    def _on_point_probability_change(self, value):
        """Handle Point Selection probability change."""
        probability = int(value) / 100.0
        self.point_probability_label.config(text=f'{int(value)}%')
        self.settings.set(POINT_SELECTION_PROBABILITY_KEY, probability)
        self.settings.save_config()
        self._sync_to_routine()

    def _on_pattern_change(self):
        """Handle Routine Pattern enable/disable change."""
        enabled = self.pattern_var.get()
        self.settings.set(ROUTINE_PATTERN_KEY, enabled)
        self.settings.save_config()
        self._sync_to_anti_detect()
        self._sync_to_routine()

    def _on_floor_chance_change(self, value):
        """Handle Floor-Only activation chance change."""
        chance = int(value) / 100.0
        self.floor_chance_label.config(text=f'{int(value)}%')
        self.settings.set(ROUTINE_PATTERN_FLOOR_CHANCE_KEY, chance)
        self.settings.save_config()
        self._sync_to_routine()

    def _on_backward_change(self):
        """Handle Random Backward enable/disable change."""
        enabled = self.backward_var.get()
        self.settings.set(RANDOM_BACKWARD_KEY, enabled)
        self.settings.save_config()
        self._sync_to_anti_detect()
        self._sync_to_routine()

    def _on_backward_probability_change(self, value):
        """Handle Random Backward probability change."""
        probability = int(value) / 100.0
        self.backward_probability_label.config(text=f'{int(value)}%')
        self.settings.set(RANDOM_BACKWARD_PROBABILITY_KEY, probability)
        self.settings.save_config()
        self._sync_to_routine()

    def _sync_to_anti_detect(self):
        """Sync settings to ANTI_DETECT_CONFIG."""
        from src.common.anti_detect_config import ANTI_DETECT_CONFIG
        ANTI_DETECT_CONFIG['routine_randomization']['point_selection']['enabled'] = \
            self.settings.get(POINT_SELECTION_KEY)
        ANTI_DETECT_CONFIG['routine_randomization']['routine_pattern']['enabled'] = \
            self.settings.get(ROUTINE_PATTERN_KEY)
        ANTI_DETECT_CONFIG['routine_randomization']['routine_pattern']['floor_variant_chance'] = \
            self.settings.get(ROUTINE_PATTERN_FLOOR_CHANCE_KEY)

    def _sync_to_routine(self):
        """Sync settings to config.routine object."""
        try:
            from src.common import config
            if hasattr(config, 'routine') and config.routine is not None:
                # Update Point Selection settings
                config.routine.skip_enabled = self.settings.get(POINT_SELECTION_KEY)
                config.routine.skip_probability = self.settings.get(POINT_SELECTION_PROBABILITY_KEY)
                
                # Update Random Backward settings
                config.routine.backward_enabled = self.settings.get(RANDOM_BACKWARD_KEY)
                config.routine.backward_probability = self.settings.get(RANDOM_BACKWARD_PROBABILITY_KEY)
                
                # Update Routine Pattern settings
                config.routine.variant_enabled = self.settings.get(ROUTINE_PATTERN_KEY)
                config.routine.floor_variant_chance = self.settings.get(ROUTINE_PATTERN_FLOOR_CHANCE_KEY)
        except Exception as e:
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
    }

    def get(self, key):
        return self.config[key]

    def set(self, key, value):
        assert key in self.config
        self.config[key] = value
