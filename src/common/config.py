"""A collection of variables shared across multiple modules."""

from src.common.bot_config import BotConfig

#########################
#       Constants       #
#########################
RESOURCES_DIR = "resources"


#################################
#       Global Variables        #
#################################
# The player's position relative to the minimap
player_pos = (0, 0)

# Enable/disable việc cập nhật vị trí liên tục phục vụ record (tắt = giữ tối ưu CPU)
record_position_live_update = False

# Describes whether the main bot loop is currently running or not
enabled = False

# If there is another player in the map, Auto Maple will purposely make random human-like mistakes
stage_fright = False

# Represents the current shortest path that the bot is taking
path = []


#############################
#       Shared Modules      #
#############################
# A Routine object that manages the 'machine code' of the current routine
routine = None

# Stores the Layout object associated with the current routine
layout = None

# Shares the main bot loop
bot = None

# Shares the video capture loop
capture = None

# Manual capture rectangle (left, top, width, height) provided by GUI
manual_capture_rect = None

# Shares the notifier module
notifier = None

# Shares the mirror input module
mirror_input = None

# Shares the keyboard listener
listener = None

# Enable/disable global keyboard listener (uses low-level hook)
enable_keyboard_listener = True

# Shares the gui to all modules
gui = None

# Centralised bot configuration
bot_config = BotConfig()

# Key output runtime values (defaults)
key_output_mode = "sendinput"
tcp_key_host = "127.0.0.1"
tcp_key_port = 12345
tcp_key_auto_reconnect = True
tcp_key_reconnect_delay = 1.0
mirror_prev_key_mode = None

# Mirror input defaults (hardware forwarding)
mirror_input_enabled = False
mirror_input_host = "127.0.0.1"
mirror_input_port = 12345
mirror_input_block_original = False
mirror_input_auto_connect = False


def _load_key_output_settings():
    global key_output_mode
    global tcp_key_host
    global tcp_key_port
    global tcp_key_auto_reconnect
    global tcp_key_reconnect_delay
    global mirror_prev_key_mode

    key_output_mode = bot_config.get("key_output.mode", key_output_mode).strip().lower()
    tcp_key_host = bot_config.get("key_output.tcp.host", tcp_key_host)
    tcp_key_port = int(bot_config.get("key_output.tcp.port", tcp_key_port))
    tcp_key_auto_reconnect = bool(
        bot_config.get("key_output.tcp.auto_reconnect", tcp_key_auto_reconnect)
    )
    tcp_key_reconnect_delay = float(
        bot_config.get("key_output.tcp.reconnect_delay", tcp_key_reconnect_delay)
    )
    if key_output_mode != "tcp":
        mirror_prev_key_mode = None


def update_key_output_settings(
    mode=None,
    host=None,
    port=None,
    auto_reconnect=None,
    reconnect_delay=None,
):
    """Persist new key-output settings to BotConfig and refresh globals."""
    changed = False
    if mode is not None:
        bot_config.set("key_output.mode", mode.lower(), persist=True)
        changed = True
    if host is not None:
        bot_config.set("key_output.tcp.host", host, persist=True)
        changed = True
    if port is not None:
        bot_config.set("key_output.tcp.port", int(port), persist=True)
        changed = True
    if auto_reconnect is not None:
        bot_config.set(
            "key_output.tcp.auto_reconnect", bool(auto_reconnect), persist=True
        )
        changed = True
    if reconnect_delay is not None:
        bot_config.set(
            "key_output.tcp.reconnect_delay", float(reconnect_delay), persist=True
        )
        changed = True
    if changed:
        _load_key_output_settings()


_load_key_output_settings()


def _load_mirror_input_settings():
    global mirror_input_enabled, mirror_input_host, mirror_input_port
    global mirror_input_block_original, mirror_input_auto_connect

    mirror_input_enabled = bool(
        bot_config.get("mirror_input.enabled", mirror_input_enabled)
    )
    mirror_input_host = bot_config.get("mirror_input.host", mirror_input_host)
    mirror_input_port = int(bot_config.get("mirror_input.port", mirror_input_port))
    mirror_input_block_original = bool(
        bot_config.get("mirror_input.block_original_input", mirror_input_block_original)
    )
    mirror_input_auto_connect = bool(
        bot_config.get("mirror_input.auto_connect", mirror_input_auto_connect)
    )


def update_mirror_input_settings(
    enabled=None, host=None, port=None, block=None, auto_connect=None
):
    changed = False
    if enabled is not None:
        bot_config.set("mirror_input.enabled", bool(enabled), persist=True)
        changed = True
    if host is not None:
        bot_config.set("mirror_input.host", host, persist=True)
        changed = True
    if port is not None:
        bot_config.set("mirror_input.port", int(port), persist=True)
        changed = True
    if block is not None:
        bot_config.set("mirror_input.block_original_input", bool(block), persist=True)
        changed = True
    if auto_connect is not None:
        bot_config.set("mirror_input.auto_connect", bool(auto_connect), persist=True)
        changed = True
    if changed:
        _load_mirror_input_settings()


_load_mirror_input_settings()

#################################
#    Arduino Output Config      #
#################################
# Enable/disable Arduino Serial output (instead of SendInput)
use_arduino = True

# Arduino Serial port (None = auto-detect)
arduino_com_port = None

# Arduino Serial baudrate
arduino_baudrate = 115200

# Key remapping for game customization (e.g., {'a': 'rbracket', 'w': 'lbracket', 'e': 'p'})
# Use Arduino key names. Set to None or {} to disable remapping.
arduino_key_mapping = {"e": "p"}  # Example: Press 'e' → outputs 'p'

# Enable/disable key remapping (can be toggled at runtime)
arduino_remapping_enabled = False

# Enable/disable serial obfuscation (binary framing & XOR keystream)
arduino_obfuscation_enabled = True

# Flag to track if we're in floor-only reverse movement
# This is set by Routine when floor_direction == 'reverse' in floor-only variants
is_floor_reverse_movement = False

#################################
#  VMware Receiver Integration  #
#################################
# Enable/disable VMware Receiver TCP server (integrated into GUI)
# When enabled, TCP server runs in background to receive commands from Host
enable_vmware_receiver = False  # Set to True to enable TCP server

# VMware Receiver TCP server port
vmware_receiver_port = 12345

# Enable/disable keyboard hook for End key hotkey (disabled by default for zero delay)
vmware_receiver_hotkey_hook = False

# VMware Receiver instance (set by main.py)
vmware_receiver = None
