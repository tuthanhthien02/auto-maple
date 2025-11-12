"""A collection of variables shared across multiple modules."""


#########################
#       Constants       #
#########################
RESOURCES_DIR = 'resources'


#################################
#       Global Variables        #
#################################
# The player's position relative to the minimap
player_pos = (0, 0)

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

# Shares the keyboard listener
listener = None

# Shares the gui to all modules
gui = None

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
arduino_key_mapping = {
    'e': 'p'  # Example: Press 'e' → outputs 'p'
}

# Enable/disable key remapping (can be toggled at runtime)
arduino_remapping_enabled = False

# Flag to track if we're in floor-only reverse movement
# This is set by Routine when floor_direction == 'reverse' in floor-only variants
is_floor_reverse_movement = False