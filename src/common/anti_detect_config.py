"""Configuration for anti-detect features."""

# Anti-Detect Configuration
ANTI_DETECT_CONFIG = {
    # Timing Randomization
    'timing': {
        'enabled': True,
        'gaussian_distribution': True,
        'variance_multipliers': {
            'fast': 0.1,      # 10% variance for fast actions
            'normal': 0.15,   # 15% variance for normal actions
            'slow': 0.25,     # 25% variance for slow actions
            'thinking': 0.5   # 50% variance for thinking pauses
        },
        'min_time_multiplier': 0.2,  # Minimum 20% of base time
        'max_time_multiplier': 3.0   # Maximum 300% of base time
    },
    
    # Behavioral Simulation
    'behavioral': {
        'enabled': False,  # DISABLED - Behavioral simulation turned off
        'afk_enabled': False,  # DISABLED
        'afk_probability': 0.0,      # 0% chance per check - DISABLED
        'afk_duration_range': (30, 300),  # 30 seconds to 5 minutes
        'behavioral_pause_probability': 0.0,  # 0% chance - DISABLED
        'behavioral_pause_range': (0.5, 3.0),  # 0.5 to 3 seconds
        'typing_mistake_probability': 0.0,    # 0% chance - DISABLED
        'activity_update_interval': 1.0        # Update every second
    },
    
    # Input Pattern Diversification
    'pattern_diversification': {
        'enabled': True,
        'skip_key_probability': 0.05,      # 5% chance to skip a key
        'add_random_key_probability': 0.02, # 2% chance to add random key
        'timing_variation_range': (0.9, 1.1),  # 10% variation
        'max_history_size': 100
    },
    
    # Memory Optimization
    'memory_optimization': {
        'enabled': True,
        'cleanup_interval': 300,  # 5 minutes
        'force_gc': True,
        'clear_cached_data': True
    },
    
    # Mouse Anti-Detect
    'mouse': {
        'enabled': True,
        'position_jitter': True,
        'jitter_range': (-1, 1),  # ±1 pixel
        'cursor_movement_delay': True,
        'hold_duration_randomization': True,
        'post_click_delay': True
    },
    
    # Keyboard Anti-Detect
    'keyboard': {
        'enabled': True,
        'micro_pauses': True,
        'micro_pause_range': [0.001, 0.002, 0.003, 0.005, 0.008, 0.012, 0.018, 0.025],
        'micro_pause_weights': [0.25, 0.20, 0.15, 0.12, 0.10, 0.08, 0.06, 0.04],
        'key_sequence_variation': True,
        'typing_speed_variation': True
    },
    
    # Process Stealth
    'process_stealth': {
        'enabled': False,  # Disabled by default (requires admin privileges)
        'hide_console': True,
        'obfuscate_process_name': False,
        'minimize_memory_footprint': True
    },
    
    # Advanced Features
    'advanced': {
        'enabled': True,
        'human_like_rhythm': True,
        'fatigue_simulation': False,  # Simulate human fatigue over time
        'learning_adaptation': False,  # Adapt patterns based on usage
        'time_based_patterns': True,   # Different patterns at different times
        'day_night_cycle': False      # Different behavior during day/night
    },
    
    # Routine Randomization
    'routine_randomization': {
        'enabled': True,
        'point_selection': {
            'enabled': True,
            'skip_probability': 0.10,  # 10% chance to skip a point
            'randomize_order': False,  # Randomize order (disabled by default - too risky)
            'max_skip_per_loop': 2,   # Maximum points to skip per loop
            'min_points_between_skips': 3,  # Minimum points between skips
            'never_skip_labels': True,  # Never skip Label components
            'never_skip_jumps': True,   # Never skip Jump components
            'never_skip_transitions': True  # Never skip transition points (adjust=True)
        },
        'routine_pattern': {
            'enabled': True,
            'variant_switch_probability': 0.15,  # 15% chance to switch variant after loop
            'min_loops_before_switch': 3,  # Minimum loops before switching variant
            'variants': {
                'normal': {'weight': 0.70, 'description': 'Normal routine execution'},
                'reverse': {'weight': 0.15, 'description': 'Reverse floor order'},
                'floor1_only': {'weight': 0.10, 'description': 'Floor 1 only'},
                'floor2_only': {'weight': 0.05, 'description': 'Floor 2 only'}
            }
        }
    }
}

# Time-based patterns (if enabled)
TIME_PATTERNS = {
    'morning': {  # 6 AM - 12 PM
        'typing_speed_multiplier': 1.1,  # Slightly faster in morning
        'pause_frequency_multiplier': 0.8,  # Fewer pauses
        'afk_probability_multiplier': 0.5   # Less likely to go AFK
    },
    'afternoon': {  # 12 PM - 6 PM
        'typing_speed_multiplier': 1.0,  # Normal speed
        'pause_frequency_multiplier': 1.0,  # Normal pauses
        'afk_probability_multiplier': 1.0   # Normal AFK probability
    },
    'evening': {  # 6 PM - 12 AM
        'typing_speed_multiplier': 0.9,  # Slightly slower in evening
        'pause_frequency_multiplier': 1.2,  # More pauses
        'afk_probability_multiplier': 1.5   # More likely to go AFK
    },
    'night': {  # 12 AM - 6 AM
        'typing_speed_multiplier': 0.8,  # Slower at night
        'pause_frequency_multiplier': 1.5,  # More pauses
        'afk_probability_multiplier': 2.0   # Much more likely to go AFK
    }
}

# Fatigue simulation (if enabled)
FATIGUE_CONFIG = {
    'enabled': False,
    'fatigue_start_hours': 4,  # Start showing fatigue after 4 hours
    'max_fatigue_multiplier': 2.0,  # Maximum 2x slower when fatigued
    'fatigue_recovery_rate': 0.1,  # 10% recovery per hour of rest
    'fatigue_affects': ['typing_speed', 'pause_frequency', 'afk_probability']
}

# Learning adaptation (if enabled)
LEARNING_CONFIG = {
    'enabled': False,
    'pattern_memory_size': 1000,  # Remember last 1000 patterns
    'adaptation_rate': 0.01,  # 1% adaptation per pattern
    'max_adaptation': 0.3,  # Maximum 30% adaptation
    'adaptation_factors': ['timing', 'patterns', 'behavior']
}

def get_config():
    """Get the current anti-detect configuration."""
    return ANTI_DETECT_CONFIG.copy()

def get_time_pattern():
    """Get the current time-based pattern."""
    from datetime import datetime
    
    hour = datetime.now().hour
    
    if 6 <= hour < 12:
        return TIME_PATTERNS['morning']
    elif 12 <= hour < 18:
        return TIME_PATTERNS['afternoon']
    elif 18 <= hour < 24:
        return TIME_PATTERNS['evening']
    else:
        return TIME_PATTERNS['night']

def is_feature_enabled(feature_path):
    """Check if a specific feature is enabled.
    
    Args:
        feature_path: Dot-separated path to feature (e.g., 'timing.enabled')
    
    Returns:
        bool: True if feature is enabled
    """
    config = ANTI_DETECT_CONFIG
    keys = feature_path.split('.')
    
    for key in keys:
        if isinstance(config, dict) and key in config:
            config = config[key]
        else:
            return False
    
    return config if isinstance(config, bool) else False

def get_feature_value(feature_path, default=None):
    """Get a specific feature value.
    
    Args:
        feature_path: Dot-separated path to feature (e.g., 'timing.variance_multipliers.normal')
        default: Default value if feature not found
    
    Returns:
        The feature value or default
    """
    config = ANTI_DETECT_CONFIG
    keys = feature_path.split('.')
    
    for key in keys:
        if isinstance(config, dict) and key in config:
            config = config[key]
        else:
            return default
    
    return config
