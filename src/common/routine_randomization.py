"""Routine randomization features for anti-detection."""

import random
from src.common import config
from src.common.logger import get_logger
from src.common.anti_detect_config import get_feature_value, is_feature_enabled
from src.routine.components import Point, Label, Jump

log = get_logger(__name__)


class RoutineRandomizer:
    """Manages routine randomization features."""
    
    def __init__(self):
        self.skip_count = 0
        self.last_skip_index = -1
        self.current_variant = 'normal'
        self.loops_in_current_variant = 0
        self.variant_start_index = 0
        
    def should_skip_point(self, point_index, element):
        """Check if current point should be skipped."""
        if not is_feature_enabled('routine_randomization.point_selection.enabled'):
            return False
        
        skip_prob = get_feature_value('routine_randomization.point_selection.skip_probability', 0.10)
        max_skip = get_feature_value('routine_randomization.point_selection.max_skip_per_loop', 2)
        min_between = get_feature_value('routine_randomization.point_selection.min_points_between_skips', 3)
        never_skip_labels = get_feature_value('routine_randomization.point_selection.never_skip_labels', True)
        never_skip_jumps = get_feature_value('routine_randomization.point_selection.never_skip_jumps', True)
        never_skip_transitions = get_feature_value('routine_randomization.point_selection.never_skip_transitions', True)
        
        # Safety checks: never skip certain components
        if isinstance(element, Label) and never_skip_labels:
            return False
        
        if isinstance(element, Jump) and never_skip_jumps:
            return False
        
        if isinstance(element, Point) and never_skip_transitions and element.adjust:
            return False
        
        # Check if we've already skipped too many points
        if self.skip_count >= max_skip:
            return False
        
        # Check minimum distance between skips
        if self.last_skip_index >= 0:
            distance = point_index - self.last_skip_index
            if distance < min_between:
                return False
        
        # Random chance to skip
        if random.random() < skip_prob:
            self.skip_count += 1
            self.last_skip_index = point_index
            log.debug("Skipping point at index %d", point_index)
            return True
        
        return False
    
    def reset_skip_counter(self):
        """Reset skip counter (called after loop completion)."""
        self.skip_count = 0
        self.last_skip_index = -1
    
    def get_next_index(self, current_index, sequence_length):
        """Get next index with randomization applied."""
        if not is_feature_enabled('routine_randomization.point_selection.enabled'):
            # Normal sequential stepping
            return (current_index + 1) % sequence_length
        
        # Check if we should skip current point
        element = config.routine[current_index]
        if self.should_skip_point(current_index, element):
            # Skip this point, go to next
            next_index = (current_index + 1) % sequence_length
            log.debug("Skipping point %d, moving to %d", current_index, next_index)
            return next_index
        
        # Normal sequential stepping
        return (current_index + 1) % sequence_length
    
    def get_variant_labels(self):
        """Get start/end labels for current variant.
        
        IMPORTANT: Routine file MUST have matching labels for variants to work:
        - 'f1_pos_0': Floor 1 start position (required for floor1_only)
        - 'f2_pos_1': Floor 2 start position (required for reverse, floor2_only)
        - 'jump_up': Transition Floor 1 → Floor 2 (required for floor1_only)
        - 'jump_down': Transition Floor 2 → Floor 1 (required for floor2_only)
        
        If labels don't match, variants will fallback to normal execution.
        See ROUTINE_RANDOMIZATION_LABEL_REQUIREMENTS.md for details.
        """
        if not is_feature_enabled('routine_randomization.routine_pattern.enabled'):
            return None
        
        variant = self.current_variant
        
        # Define variant patterns based on common label names
        # NOTE: Routine file MUST have these exact label names for variants to work!
        # To customize label names, edit this dictionary or update your routine file.
        variant_patterns = {
            'normal': None,  # Normal execution - no label requirements
            'reverse': {
                'start_label': 'f2_pos_1',  # REQUIRED: Floor 2 start label
                'end_label': 'f1_pos_0'     # REQUIRED: Floor 1 start label
            },
            'floor1_only': {
                'start_label': 'f1_pos_0',  # REQUIRED: Floor 1 start label
                'end_label': 'jump_up'      # REQUIRED: Transition label (Floor 1 → 2)
            },
            'floor2_only': {
                'start_label': 'f2_pos_1',  # REQUIRED: Floor 2 start label
                'end_label': 'jump_down'    # REQUIRED: Transition label (Floor 2 → 1)
            }
        }
        
        return variant_patterns.get(variant)
    
    def should_switch_variant(self):
        """Check if we should switch to a different variant."""
        if not is_feature_enabled('routine_randomization.routine_pattern.enabled'):
            return False
        
        min_loops = get_feature_value('routine_randomization.routine_pattern.min_loops_before_switch', 3)
        switch_prob = get_feature_value('routine_randomization.routine_pattern.variant_switch_probability', 0.15)
        
        # Must complete minimum loops before switching
        if self.loops_in_current_variant < min_loops:
            return False
        
        # Random chance to switch
        if random.random() < switch_prob:
            return True
        
        return False
    
    def select_new_variant(self):
        """Select a new variant based on weights."""
        variants_config = get_feature_value('routine_randomization.routine_pattern.variants', {})
        
        if not variants_config:
            self.current_variant = 'normal'
            return
        
        # Extract variants and weights
        variants = []
        weights = []
        for variant_name, variant_data in variants_config.items():
            variants.append(variant_name)
            weights.append(variant_data.get('weight', 0.1))
        
        # Normalize weights
        total_weight = sum(weights)
        if total_weight > 0:
            weights = [w / total_weight for w in weights]
        
        # Select variant based on weights
        self.current_variant = random.choices(variants, weights=weights)[0]
        self.loops_in_current_variant = 0
        
        log.info("Switched to routine variant: %s", self.current_variant)
    
    def increment_loop_count(self):
        """Increment loop count for current variant."""
        self.loops_in_current_variant += 1
        self.reset_skip_counter()  # Reset skip counter after each loop
        
        # Check if we should switch variant
        if self.should_switch_variant():
            self.select_new_variant()
    
    def get_variant_start_index(self):
        """Get starting index for current variant."""
        variant_labels = self.get_variant_labels()
        
        if not variant_labels or 'start_label' not in variant_labels:
            return 0  # Default: start from beginning
        
        start_label_name = variant_labels['start_label']
        
        # Find label in routine
        if start_label_name in config.routine.labels:
            label = config.routine.labels[start_label_name]
            if label.index is not None:
                return label.index
        
        # Fallback: return 0
        log.warning("Could not find start label '%s' for variant, using default", start_label_name)
        return 0


# Global instance
routine_randomizer = RoutineRandomizer()


def initialize_routine_randomization():
    """Initialize routine randomization."""
    # Load settings from file if available (before GUI loads)
    try:
        from src.gui.settings.routine_randomization import (
            RoutineRandomizationSettings,
            POINT_SELECTION_KEY,
            ROUTINE_PATTERN_KEY
        )
        settings = RoutineRandomizationSettings('routine_randomization')
        # Sync với anti_detect_config
        from src.common.anti_detect_config import ANTI_DETECT_CONFIG
        ANTI_DETECT_CONFIG['routine_randomization']['point_selection']['enabled'] = \
            settings.get(POINT_SELECTION_KEY)
        ANTI_DETECT_CONFIG['routine_randomization']['routine_pattern']['enabled'] = \
            settings.get(ROUTINE_PATTERN_KEY)
        log.debug("Loaded routine randomization settings from file")
    except Exception as e:
        log.debug("Could not load routine randomization settings (will use defaults): %s", e)
    
    if is_feature_enabled('routine_randomization.enabled'):
        routine_randomizer.current_variant = 'normal'
        routine_randomizer.loops_in_current_variant = 0
        routine_randomizer.reset_skip_counter()
        log.info("Routine randomization initialized")


def get_next_routine_index(current_index):
    """Get next routine index with randomization applied."""
    sequence_length = len(config.routine)
    
    if sequence_length == 0:
        return 0
    
    # Apply point selection randomization
    next_index = routine_randomizer.get_next_index(current_index, sequence_length)
    
    return next_index


def check_loop_completion(old_index, new_index):
    """Check if a loop has been completed and handle variant switching."""
    # Simple heuristic: if we go back to start (index 0 or very low), we completed a loop
    # This might need adjustment based on actual routine structure
    if new_index < old_index and new_index < 5:  # Probably looped back
        routine_randomizer.increment_loop_count()


def get_variant_start_index():
    """Get starting index for current variant."""
    return routine_randomizer.get_variant_start_index()

