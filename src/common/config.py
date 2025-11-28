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

# Shares the notifier module
notifier = None

# Shares the keyboard listener
listener = None

# Enable/disable global keyboard listener (uses low-level hook)
enable_keyboard_listener = True

# Shares the gui to all modules
gui = None

# Centralised bot configuration
bot_config = BotConfig()

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
