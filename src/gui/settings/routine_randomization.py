import tkinter as tk
from src.gui.interfaces import LabelFrame
from src.common.interfaces import Configurable

# Constants for settings keys
POINT_SELECTION_KEY = 'Point Selection Enabled'
ROUTINE_PATTERN_KEY = 'Routine Pattern Enabled'


class RoutineRandomization(LabelFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, 'Routine Randomization', **kwargs)

        self.settings = RoutineRandomizationSettings('routine_randomization')

        # Load từ settings file
        point_enabled = self.settings.get(POINT_SELECTION_KEY)
        pattern_enabled = self.settings.get(ROUTINE_PATTERN_KEY)

        # Create checkboxes
        self.point_var = tk.BooleanVar(value=point_enabled)
        self.pattern_var = tk.BooleanVar(value=pattern_enabled)

        tk.Checkbutton(
            self,
            variable=self.point_var,
            text='Point Selection Randomization',
            command=self._on_change
        ).pack(side=tk.TOP, anchor='w', padx=5, pady=2)

        tk.Checkbutton(
            self,
            variable=self.pattern_var,
            text='Routine Pattern Randomization',
            command=self._on_change
        ).pack(side=tk.TOP, anchor='w', padx=5, pady=2)

        # Sync với anti_detect_config khi load
        self._sync_to_anti_detect()

    def _on_change(self):
        # Save to settings file
        self.settings.set(POINT_SELECTION_KEY, self.point_var.get())
        self.settings.set(ROUTINE_PATTERN_KEY, self.pattern_var.get())
        self.settings.save_config()

        # Sync với anti_detect_config
        self._sync_to_anti_detect()

    def _sync_to_anti_detect(self):
        """Sync settings to ANTI_DETECT_CONFIG."""
        from src.common.anti_detect_config import ANTI_DETECT_CONFIG
        ANTI_DETECT_CONFIG['routine_randomization']['point_selection']['enabled'] = \
            self.settings.get(POINT_SELECTION_KEY)
        ANTI_DETECT_CONFIG['routine_randomization']['routine_pattern']['enabled'] = \
            self.settings.get(ROUTINE_PATTERN_KEY)


class RoutineRandomizationSettings(Configurable):
    DEFAULT_CONFIG = {
        POINT_SELECTION_KEY: True,
        ROUTINE_PATTERN_KEY: True
    }

    def get(self, key):
        return self.config[key]

    def set(self, key, value):
        assert key in self.config
        self.config[key] = value

