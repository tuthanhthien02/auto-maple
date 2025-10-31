"""Advanced anti-detection features for auto-maple."""

import time
import random
import threading
from datetime import datetime, timedelta
from src.common import config, utils
from src.common.logger import get_logger


log = get_logger(__name__)


class AntiDetectManager:
    """Manages advanced anti-detection features."""
    
    def __init__(self):
        self.afk_timer = None
        self.last_activity = time.time()
        self.behavioral_patterns = {
            'typing_speed': 0.1,  # Base typing speed
            'pause_frequency': 0.0,  # 0% chance of pause - DISABLED
            'afk_frequency': 0.0,  # 0% chance of AFK - DISABLED
            'pattern_variation': 0.15  # 15% variation in patterns
        }
        self.running = False
        self.afk_thread = None
        
    def start(self):
        """Start the anti-detect manager."""
        self.running = True
        # AFK monitor DISABLED - no auto pause
        # self.afk_thread = threading.Thread(target=self._afk_monitor, daemon=True)
        # self.afk_thread.start()
        
    def stop(self):
        """Stop the anti-detect manager."""
        self.running = False
        if self.afk_thread:
            self.afk_thread.join()
    
    def _afk_monitor(self):
        """Monitor for AFK periods and implement behavioral pauses."""
        while self.running:
            try:
                # Check if we should go AFK
                if self._should_go_afk():
                    self._implement_afk_period()
                
                # Check for behavioral pauses
                if self._should_add_behavioral_pause():
                    self._implement_behavioral_pause()
                
                time.sleep(1)  # Check every second
                
            except Exception:
                log.exception("Anti-detect error")
                time.sleep(5)
    
    def _should_go_afk(self):
        """Determine if we should go AFK based on patterns."""
        time_since_activity = time.time() - self.last_activity
        
        # AFK probability increases with time since last activity
        afk_probability = min(0.1, time_since_activity / 3600)  # Max 10% after 1 hour
        
        return random.random() < afk_probability
    
    def _implement_afk_period(self):
        """Implement an AFK period to simulate human behavior."""
        afk_duration = random.uniform(30, 300)  # 30 seconds to 5 minutes
        log.info("Going AFK for %.1f seconds", afk_duration)
        
        # Temporarily disable bot
        original_enabled = config.enabled
        config.enabled = False
        
        time.sleep(afk_duration)
        
        # Re-enable bot
        config.enabled = original_enabled
        self.last_activity = time.time()
        
        log.info("AFK period ended")
    
    def _should_add_behavioral_pause(self):
        """Determine if we should add a behavioral pause."""
        return random.random() < self.behavioral_patterns['pause_frequency']
    
    def _implement_behavioral_pause(self):
        """Implement a short behavioral pause."""
        pause_duration = random.uniform(0.5, 3.0)  # 0.5 to 3 seconds
        log.info("Behavioral pause for %.1f seconds", pause_duration)
        
        time.sleep(pause_duration)
        self.last_activity = time.time()
    
    def update_activity(self):
        """Update the last activity timestamp."""
        self.last_activity = time.time()
    
    def get_human_like_delay(self, base_delay, delay_type='normal'):
        """Get a human-like delay with realistic variation."""
        variance_multipliers = {
            'fast': 0.1,
            'normal': 0.15,
            'slow': 0.25,
            'thinking': 0.5
        }
        
        variance = base_delay * variance_multipliers.get(delay_type, 0.15)
        
        # Use Gaussian distribution for more natural timing
        randomized_time = random.gauss(base_delay, variance)
        
        # Ensure reasonable bounds
        min_time = base_delay * 0.2
        max_time = base_delay * 3.0
        
        return max(min_time, min(randomized_time, max_time))
    
    def get_typing_pattern(self, text_length):
        """Get a realistic typing pattern for text of given length."""
        # Simulate human typing patterns
        base_speed = self.behavioral_patterns['typing_speed']
        
        # Typing speed varies with text length (longer text = slightly slower)
        length_factor = 1 + (text_length / 1000) * 0.1
        
        # Add random variation
        variation = random.uniform(0.8, 1.2)
        
        return base_speed * length_factor * variation
    
    def should_add_typing_mistake(self):
        """Determine if we should simulate a typing mistake."""
        # 1% chance of typing mistake
        return random.random() < 0.01
    
    def simulate_typing_mistake(self):
        """Simulate a typing mistake and correction."""
        log.info("Simulating typing mistake")
        
        # Press wrong key
        wrong_keys = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l']
        wrong_key = random.choice(wrong_keys)
        
        from src.common.vkeys import press
        press(wrong_key, 1)
        
        # Wait a bit
        time.sleep(random.uniform(0.1, 0.3))
        
        # Press backspace
        press('backspace', 1)
        
        # Wait a bit more
        time.sleep(random.uniform(0.05, 0.15))


class PatternDiversifier:
    """Diversifies input patterns to avoid detection."""
    
    def __init__(self):
        self.pattern_history = []
        self.max_history = 100
        
    def diversify_sequence(self, keys):
        """Diversify a sequence of keys to avoid pattern detection."""
        if len(keys) < 2:
            return keys
        
        # Add slight variations to the sequence
        diversified = []
        
        for i, key in enumerate(keys):
            # Occasionally skip a key (5% chance)
            if random.random() < 0.05 and i > 0:
                continue
            
            # Occasionally add a random key (2% chance)
            if random.random() < 0.02:
                random_keys = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l']
                diversified.append(random.choice(random_keys))
            
            diversified.append(key)
        
        return diversified
    
    def add_timing_variation(self, delays):
        """Add timing variations to avoid detection."""
        varied_delays = []
        
        for delay in delays:
            # Add 10-20% variation
            variation = random.uniform(0.9, 1.1)
            varied_delay = delay * variation
            varied_delays.append(varied_delay)
        
        return varied_delays


class MemoryOptimizer:
    """Optimizes memory usage to reduce detectable signatures."""
    
    def __init__(self):
        self.cleanup_interval = 300  # 5 minutes
        self.last_cleanup = time.time()
    
    def should_cleanup(self):
        """Check if memory cleanup is needed."""
        return time.time() - self.last_cleanup > self.cleanup_interval
    
    def cleanup_memory(self):
        """Perform memory cleanup to reduce signatures."""
        import gc
        
        # Force garbage collection
        gc.collect()
        
        # Clear any cached data
        if hasattr(config, 'capture') and hasattr(config.capture, 'frame'):
            config.capture.frame = None
        
        self.last_cleanup = time.time()
        log.info("Memory cleanup performed")


# Global instances
anti_detect_manager = AntiDetectManager()
pattern_diversifier = PatternDiversifier()
memory_optimizer = MemoryOptimizer()


def initialize_anti_detect():
    """Initialize all anti-detect features."""
    anti_detect_manager.start()
    log.info("Anti-detect features initialized")


def cleanup_anti_detect():
    """Cleanup anti-detect features."""
    anti_detect_manager.stop()
    log.info("Anti-detect features stopped")


def get_human_delay(base_delay, delay_type='normal'):
    """Get a human-like delay."""
    return anti_detect_manager.get_human_like_delay(base_delay, delay_type)


def should_add_behavioral_pause():
    """Check if a behavioral pause should be added."""
    return anti_detect_manager._should_add_behavioral_pause()


def update_activity():
    """Update activity timestamp."""
    anti_detect_manager.update_activity()


def diversify_pattern(keys):
    """Diversify a key pattern."""
    return pattern_diversifier.diversify_sequence(keys)


def optimize_memory():
    """Optimize memory usage."""
    if memory_optimizer.should_cleanup():
        memory_optimizer.cleanup_memory()
