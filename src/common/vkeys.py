"""A module for simulating low-level keyboard and mouse key presses."""

import ctypes
from ctypes import wintypes
from random import random, gauss, uniform, choice
import time
import win32con
import win32api
from src.common import utils
from src.common.logger import get_logger, get_action_logger

log = get_logger(__name__)
action_log = get_action_logger()


user32 = ctypes.WinDLL("user32", use_last_error=True)

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004
KEYEVENTF_SCANCODE = 0x0008

MAPVK_VK_TO_VSC = 0

# https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes?redirectedfrom=MSDN
KEY_MAP = {
    "left": 0x25,  # Arrow keys
    "up": 0x26,
    "right": 0x27,
    "down": 0x28,
    "backspace": 0x08,  # Special keys
    "tab": 0x09,
    "enter": 0x0D,
    "shift": 0x10,
    "ctrl": 0x11,
    "alt": 0x12,
    "caps lock": 0x14,
    "esc": 0x1B,
    "space": 0x20,
    "page up": 0x21,
    "page down": 0x22,
    "end": 0x23,
    "home": 0x24,
    "insert": 0x2D,
    "delete": 0x2E,
    "0": 0x30,  # Numbers
    "1": 0x31,
    "2": 0x32,
    "3": 0x33,
    "4": 0x34,
    "5": 0x35,
    "6": 0x36,
    "7": 0x37,
    "8": 0x38,
    "9": 0x39,
    "a": 0x41,  # Letters
    "b": 0x42,
    "c": 0x43,
    "d": 0x44,
    "e": 0x45,
    "f": 0x46,
    "g": 0x47,
    "h": 0x48,
    "i": 0x49,
    "j": 0x4A,
    "k": 0x4B,
    "l": 0x4C,
    "m": 0x4D,
    "n": 0x4E,
    "o": 0x4F,
    "p": 0x50,
    "q": 0x51,
    "r": 0x52,
    "s": 0x53,
    "t": 0x54,
    "u": 0x55,
    "v": 0x56,
    "w": 0x57,
    "x": 0x58,
    "y": 0x59,
    "z": 0x5A,
    "f1": 0x70,  # Functional keys
    "f2": 0x71,
    "f3": 0x72,
    "f4": 0x73,
    "f5": 0x74,
    "f6": 0x75,
    "f7": 0x76,
    "f8": 0x77,
    "f9": 0x78,
    "f10": 0x79,
    "f11": 0x7A,
    "f12": 0x7B,
    "num lock": 0x90,
    "scroll lock": 0x91,
    ";": 0xBA,  # Special characters
    "=": 0xBB,
    ",": 0xBC,
    "-": 0xBD,
    ".": 0xBE,
    "/": 0xBF,
    "`": 0xC0,
    "[": 0xDB,
    "\\": 0xDC,
    "]": 0xDD,
    "'": 0xDE,
}


#################################
#     C Struct Definitions      #
#################################
wintypes.ULONG_PTR = wintypes.WPARAM


class KeyboardInput(ctypes.Structure):
    _fields_ = (
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", wintypes.ULONG_PTR),
    )

    def __init__(self, *args, **kwargs):
        super(KeyboardInput, self).__init__(*args, **kwargs)
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk, MAPVK_VK_TO_VSC, 0)


class MouseInput(ctypes.Structure):
    _fields_ = (
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", wintypes.ULONG_PTR),
    )


class HardwareInput(ctypes.Structure):
    _fields_ = (
        ("uMsg", wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD),
    )


class Input(ctypes.Structure):
    class _Input(ctypes.Union):
        _fields_ = (("ki", KeyboardInput), ("mi", MouseInput), ("hi", HardwareInput))

    _anonymous_ = ("_input",)
    _fields_ = (("type", wintypes.DWORD), ("_input", _Input))


LPINPUT = ctypes.POINTER(Input)


def err_check(result, _, args):
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    else:
        return args


user32.SendInput.errcheck = err_check
user32.SendInput.argtypes = (wintypes.UINT, LPINPUT, ctypes.c_int)


#################################
#           Functions           #
#################################

# Arduino output instance (lazy import)
_arduino_output = None


def _get_arduino_output():
    """Get or create Arduino output instance using SharedArduinoConnection"""
    global _arduino_output
    if _arduino_output is None:
        # Check if Arduino is enabled in config
        try:
            from src.common import config

            if hasattr(config, "use_arduino") and config.use_arduino:
                try:
                    from src.common.shared_arduino_connection import (
                        SharedArduinoConnection,
                    )

                    # Use SharedArduinoConnection singleton
                    shared_conn = SharedArduinoConnection()
                    if not shared_conn.connected:
                        log.warning(
                            "Arduino output enabled but connection failed, falling back to SendInput"
                        )
                        _arduino_output = False  # Mark as unavailable
                    else:
                        # Create wrapper object with ArduinoSerialOutput-like interface
                        class ArduinoOutputWrapper:
                            def __init__(self, shared_conn):
                                self.shared_conn = shared_conn
                                self.connected = shared_conn.connected

                            def key_down(self, key):
                                try:
                                    return self.shared_conn.send_command("down", key)
                                except Exception as e:
                                    log.error(
                                        f"[VKEYS] Error in ArduinoOutputWrapper.key_down: {e}"
                                    )
                                    import traceback

                                    log.error(traceback.format_exc())
                                    return False

                            def key_up(self, key):
                                try:
                                    return self.shared_conn.send_command("up", key)
                                except Exception as e:
                                    log.error(
                                        f"[VKEYS] Error in ArduinoOutputWrapper.key_up: {e}"
                                    )
                                    import traceback

                                    log.error(traceback.format_exc())
                                    return False

                            def press(self, key, n, down_time=0.05, up_time=0.1):
                                import time

                                try:
                                    for i in range(n):
                                        self.key_down(key)
                                        time.sleep(down_time)
                                        self.key_up(key)
                                        if i < n - 1:
                                            time.sleep(up_time)
                                except Exception as e:
                                    log.error(
                                        f"[VKEYS] Error in ArduinoOutputWrapper.press: {e}"
                                    )
                                    import traceback

                                    log.error(traceback.format_exc())

                        _arduino_output = ArduinoOutputWrapper(shared_conn)
                        log.info(
                            "Arduino output initialized successfully (using SharedArduinoConnection)"
                        )
                except Exception as e:
                    log.warning(
                        f"Failed to initialize Arduino output: {e}, falling back to SendInput"
                    )
                    _arduino_output = False  # Mark as unavailable
            else:
                # Arduino not enabled
                _arduino_output = False
        except ImportError:
            # Config module not available
            _arduino_output = False
        except Exception as e:
            log.warning(f"Error checking Arduino config: {e}")
            _arduino_output = False

    return _arduino_output


def _key_down_sendinput(key):
    """Original SendInput key_down implementation"""
    key = key.lower()
    if key not in KEY_MAP.keys():
        log.warning("Invalid keyboard input: '%s'", key)
    else:
        action_log.debug("key_down('%s')", key)
        x = Input(type=INPUT_KEYBOARD, ki=KeyboardInput(wVk=KEY_MAP[key]))
        user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


@utils.run_if_enabled
def key_down(key):
    """
    Simulates a key-down action. Can be cancelled by Bot.toggle_enabled.
    Uses Arduino if enabled, otherwise SendInput.
    :param key:     The key to press.
    :return:        None
    """
    # Check if Arduino is enabled and available
    arduino = _get_arduino_output()
    if arduino and arduino.connected:
        arduino.key_down(key)
        return

    # Fallback to SendInput
    _key_down_sendinput(key)


def _key_up_sendinput(key):
    """Original SendInput key_up implementation"""
    key = key.lower()
    if key not in KEY_MAP.keys():
        log.warning("Invalid keyboard input: '%s'", key)
    else:
        action_log.debug("key_up('%s')", key)
        x = Input(
            type=INPUT_KEYBOARD,
            ki=KeyboardInput(wVk=KEY_MAP[key], dwFlags=KEYEVENTF_KEYUP),
        )
        user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


def key_up(key):
    """
    Simulates a key-up action. Cannot be cancelled by Bot.toggle_enabled.
    This is to ensure no keys are left in the 'down' state when the program pauses.
    Uses Arduino if enabled, otherwise SendInput.
    :param key:     The key to press.
    :return:        None
    """
    # Check if Arduino is enabled and available
    arduino = _get_arduino_output()
    if arduino and arduino.connected:
        arduino.key_up(key)
        return

    # Fallback to SendInput
    _key_up_sendinput(key)


def _press_sendinput(key, n, down_time=0.05, up_time=0.1):
    """
    Original SendInput press implementation.
    Presses KEY N times, holding it for DOWN_TIME seconds, and releasing for UP_TIME seconds.
    Enhanced with advanced anti-detect timing randomization.
    :param key:         The keyboard input to press.
    :param n:           Number of times to press KEY.
    :param down_time:   Duration of down-press (in seconds).
    :param up_time:     Duration of release (in seconds).
    :return:            None
    """
    action_log.debug(
        "press('%s', n=%d, down_time=%.3f, up_time=%.3f) [SendInput]",
        key,
        n,
        down_time,
        up_time,
    )

    for i in range(n):
        # Advanced timing randomization
        down_delay = _get_human_like_delay(down_time, "down")
        up_delay = _get_human_like_delay(up_time, "up")

        action_log.debug(
            "press iteration %d/%d -> down_delay=%.3f, up_delay=%.3f",
            i + 1,
            n,
            down_delay,
            up_delay,
        )

        _key_down_sendinput(key)
        time.sleep(down_delay)
        _key_up_sendinput(key)
        time.sleep(up_delay)

        # Add micro-pauses between rapid key presses
        if i < n - 1 and n > 1:
            micro_pause = _get_micro_pause()
            time.sleep(micro_pause)


@utils.run_if_enabled
def press(key, n, down_time=0.05, up_time=0.1):
    """
    Presses KEY N times, holding it for DOWN_TIME seconds, and releasing for UP_TIME seconds.
    Enhanced with advanced anti-detect timing randomization.
    Uses Arduino if enabled, otherwise SendInput.
    :param key:         The keyboard input to press.
    :param n:           Number of times to press KEY.
    :param down_time:   Duration of down-press (in seconds).
    :param up_time:     Duration of release (in seconds).
    :return:            None
    """
    # Check if Arduino is enabled and available
    arduino = _get_arduino_output()
    if arduino and arduino.connected:
        # Use Arduino
        arduino.press(key, n, down_time, up_time)
        return

    # Fallback to SendInput
    _press_sendinput(key, n, down_time, up_time)


@utils.run_if_enabled
def click(position, button="left"):
    """
    Simulate a mouse click with BUTTON at POSITION.
    Enhanced with anti-detect features for more human-like behavior.
    :param position:    The (x, y) position at which to click.
    :param button:      Either the left or right mouse button.
    :return:            None
    """

    if button not in ["left", "right"]:
        log.warning("'%s' is not a valid mouse button", button)
    else:
        action_log.debug("click(%s, button='%s')", position, button)
        # Add slight position randomization for more human-like clicks
        jitter_x = uniform(-1, 1)
        jitter_y = uniform(-1, 1)
        jittered_position = (position[0] + jitter_x, position[1] + jitter_y)

        if button == "left":
            down_event = win32con.MOUSEEVENTF_LEFTDOWN
            up_event = win32con.MOUSEEVENTF_LEFTUP
        else:
            down_event = win32con.MOUSEEVENTF_RIGHTDOWN
            up_event = win32con.MOUSEEVENTF_RIGHTUP

        # Move cursor with slight delay
        win32api.SetCursorPos(jittered_position)
        time.sleep(_get_human_like_delay(0.01, "micro"))

        # Click down
        win32api.mouse_event(
            down_event, jittered_position[0], jittered_position[1], 0, 0
        )

        # Hold duration with randomization
        hold_duration = _get_human_like_delay(0.05, "down")
        time.sleep(hold_duration)

        # Click up
        win32api.mouse_event(up_event, jittered_position[0], jittered_position[1], 0, 0)

        # Post-click delay
        post_click_delay = _get_human_like_delay(0.02, "up")
        time.sleep(post_click_delay)


#################################
#    Anti-Detect Functions     #
#################################


def _get_human_like_delay(base_time, delay_type="down"):
    """
    Generates human-like delays using Gaussian distribution with realistic variance.
    :param base_time:   Base delay time in seconds
    :param delay_type:  Type of delay ('down', 'up', 'micro')
    :return:            Randomized delay time
    """

    # Different variance for different delay types
    variance_multipliers = {
        "down": 0.15,  # 15% variance for key down
        "up": 0.20,  # 20% variance for key up
        "micro": 0.30,  # 30% variance for micro pauses
    }

    variance = base_time * variance_multipliers.get(delay_type, 0.15)

    # Use Gaussian distribution for more natural timing
    randomized_time = gauss(base_time, variance)

    # Ensure minimum and maximum bounds
    min_time = base_time * 0.3
    max_time = base_time * 2.0

    return max(min_time, min(randomized_time, max_time))


def _get_micro_pause():
    """
    Generates micro-pauses between rapid key presses to simulate human behavior.
    :return:    Micro-pause duration in seconds
    """

    # Micro-pause ranges (in seconds)
    micro_pauses = [0.001, 0.002, 0.003, 0.005, 0.008, 0.012, 0.018, 0.025]

    # Weighted selection (shorter pauses more common)
    # weights = [0.25, 0.20, 0.15, 0.12, 0.10, 0.08, 0.06, 0.04]

    return choice(micro_pauses)


def _get_behavioral_pause():
    """
    Generates longer behavioral pauses to simulate human thinking/hesitation.
    :return:    Behavioral pause duration in seconds
    """

    # Behavioral pause ranges (in seconds)
    behavioral_pauses = [0.1, 0.2, 0.3, 0.5, 0.8, 1.2, 1.8, 2.5]

    # Weighted selection (shorter pauses more common)
    # weights = [0.30, 0.25, 0.20, 0.15, 0.05, 0.03, 0.01, 0.01]

    return choice(behavioral_pauses)


def _should_add_behavioral_pause():
    """
    Determines if a behavioral pause should be added based on probability.
    :return:    True if pause should be added
    """

    # 5% chance of adding behavioral pause
    return random() < 0.05


def _get_input_pattern_variation():
    """
    Generates input pattern variations to avoid detection.
    :return:    Variation factor (0.8 to 1.2)
    """

    # Slight variation in input patterns
    return uniform(0.8, 1.2)


def press_with_behavioral_pause(key, n, down_time=0.05, up_time=0.1):
    """
    Enhanced press function with pattern variation (behavioral pause DISABLED).
    :param key:         The keyboard input to press.
    :param n:           Number of times to press KEY.
    :param down_time:   Duration of down-press (in seconds).
    :param up_time:     Duration of release (in seconds).
    :return:            None
    """

    for i in range(n):
        # Behavioral pause DISABLED - removed for better performance

        # Apply input pattern variation
        variation = _get_input_pattern_variation()
        adjusted_down_time = down_time * variation
        adjusted_up_time = up_time * variation

        # Advanced timing randomization
        down_delay = _get_human_like_delay(adjusted_down_time, "down")
        up_delay = _get_human_like_delay(adjusted_up_time, "up")

        key_down(key)
        time.sleep(down_delay)
        key_up(key)
        time.sleep(up_delay)

        # Add micro-pauses between rapid key presses
        if i < n - 1 and n > 1:
            micro_pause = _get_micro_pause()
            time.sleep(micro_pause)


def press_sequence_with_variation(keys, delays=None):
    """
    Presses a sequence of keys with human-like variations.
    :param keys:        List of keys to press in sequence
    :param delays:      Optional list of delays between keys
    :return:            None
    """

    if delays is None:
        delays = [_get_human_like_delay(0.1, "micro") for _ in range(len(keys) - 1)]

    for i, key in enumerate(keys):
        # Press key with variation
        press_with_behavioral_pause(key, 1)

        # Add delay between keys
        if i < len(keys) - 1:
            delay = (
                delays[i] if i < len(delays) else _get_human_like_delay(0.1, "micro")
            )
            time.sleep(delay)


def simulate_human_typing(text, base_delay=0.1):
    """
    Simulates human typing with realistic timing variations.
    :param text:        Text to type
    :param base_delay:  Base delay between keystrokes
    :return:            None
    """

    for char in text:
        if char == " ":
            press_with_behavioral_pause("space", 1)
        elif char.isupper():
            # Simulate shift + key
            key_down("shift")
            time.sleep(_get_human_like_delay(0.01, "micro"))
            key_down(char.lower())
            time.sleep(_get_human_like_delay(0.05, "down"))
            key_up(char.lower())
            time.sleep(_get_human_like_delay(0.01, "micro"))
            key_up("shift")
        else:
            press_with_behavioral_pause(char.lower(), 1)

        # Variable delay between characters
        char_delay = _get_human_like_delay(base_delay, "micro")
        time.sleep(char_delay)
