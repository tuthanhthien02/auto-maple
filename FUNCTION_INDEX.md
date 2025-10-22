# Auto Maple Function & Class Index

## 🏗️ Core Classes

### Bot Module (`src/modules/bot.py`)

```python
class Bot(Configurable):
    def __init__(self)                    # Initialize bot with routine and command book
    def start(self)                       # Start bot thread
    def _main(self)                       # Main execution loop
    def _solve_rune(self, model)          # Automatic rune solving
    def load_commands(self, file)         # Load command book
    def update_submodules(self, force)    # Update git submodules
```

### Capture Module (`src/modules/capture.py`)

```python
class Capture:
    def __init__(self)                    # Initialize capture system
    def start(self)                       # Start capture thread
    def _main(self)                       # Main capture loop
    def screenshot(self, delay)           # Take screenshot
    def calibrate(self)                   # Calibrate minimap bounds
```

### Listener Module (`src/modules/listener.py`)

```python
class Listener(Configurable):
    def __init__(self)                    # Initialize keyboard listener
    def start(self)                       # Start listener thread
    def _main(self)                       # Main listener loop
    def restricted_pressed(self, action)  # Check restricted key presses
    def toggle_enabled()                  # Toggle bot on/off
    def reload_routine()                  # Reload current routine
    def record_position()                 # Record current position
```

### Notifier Module (`src/modules/notifier.py`)

```python
class Notifier:
    def __init__(self)                    # Initialize notifier system
    def start(self)                       # Start notifier thread
    def _main(self)                       # Main notification loop
    def _alert(self, name, volume)        # Play alert sound
    def _ping(self, name, volume)         # Play ping sound

def get_alert_path(name)                  # Get path to alert sound file
def distance_to_rune(point)               # Calculate distance to rune
```

### GUI Module (`src/modules/gui.py`)

```python
class GUI:
    def __init__(self)                    # Initialize GUI application
    def start(self)                       # Start GUI main loop
    def _display_minimap(self)            # Display minimap in separate thread
    def _save_layout(self)                # Save layout periodically
```

## 🧩 Routine System Classes

### Routine (`src/routine/routine.py`)

```python
class Routine:
    def __init__(self)                    # Initialize empty routine
    def compile(self, file)               # Compile CSV routine file
    def _eval(self, row, i)               # Evaluate routine line
    def step(self)                        # Move to next routine element
    def clear(self)                       # Clear current routine
    def get_all_components()              # Get all available components
```

### Layout (`src/routine/layout.py`)

```python
class Node:
    def __init__(self, x, y)              # Initialize pathfinding node
    def add_neighbor(self, neighbor)      # Add neighboring node
    def distance_to(self, other)          # Calculate distance to other node

class Layout:
    def __init__(self, name)              # Initialize layout system
    def add(self, x, y)                   # Add position to layout
    def get_shortest_path(self, start, end) # A* pathfinding
    def save(self)                        # Save layout to file
    def load(self)                        # Load layout from file
```

### Components (`src/routine/components.py`)

```python
class Component:
    def __init__(self, *args, **kwargs)   # Base component constructor
    def execute(self)                     # Execute component
    def main(self)                        # Main execution logic
    def update(self, *args, **kwargs)     # Update component parameters
    def info(self)                        # Get component information
    def encode(self)                      # Encode component to string

class Point(Component):
    def __init__(self, x, y, frequency, skip, adjust) # Point constructor
    def main(self)                        # Execute point actions
    def _increment_counter(self)          # Increment execution counter

class Label(Component):
    def __init__(self, label)             # Label constructor
    def set_index(self, index)            # Set label index

class Jump(Component):
    def __init__(self, label)             # Jump constructor
    def main(self)                        # Jump to label

class Setting(Component):
    def __init__(self, key, value)        # Setting constructor
    def main(self)                        # Apply setting

class Command(Component):
    def __init__(self, *args, **kwargs)   # Base command constructor

class Move(Command):
    def __init__(self, x, y)              # Move command constructor
    def main(self)                        # Execute movement
    def _new_direction(self, key)         # Set new movement direction

class Adjust(Command):
    def __init__(self, x, y)              # Adjust command constructor
    def main(self)                        # Fine-tune position

class Wait(Command):
    def __init__(self, duration)          # Wait command constructor
    def main(self)                        # Wait for duration

class Walk(Command):
    def __init__(self, direction, duration) # Walk command constructor
    def main(self)                        # Execute walking

class Fall(Command):
    def __init__(self, distance)          # Fall command constructor
    def main(self)                        # Execute falling

class Buff(Command):
    def __init__(self)                    # Buff command constructor
    def main(self)                        # Execute buffing

def step(direction, target)               # Custom step function
```

## 🔧 Utility Functions

### VKeys (`src/common/vkeys.py`)

```python
def key_down(key)                         # Simulate key press down
def key_up(key)                           # Simulate key release
def press(key, n, down_time, up_time)     # Press key multiple times
def click(position, button)               # Simulate mouse click
```

### Utils (`src/common/utils.py`)

```python
def run_if_enabled(function)              # Decorator for bot control
def run_if_disabled(message)              # Decorator for disabled state
def single_match(frame, template)         # Single template matching
def multi_match(frame, template, threshold) # Multiple template matching
def convert_to_relative(point, frame)     # Convert to relative coordinates
def convert_to_absolute(point, frame)     # Convert to absolute coordinates
def filter_color(img, ranges)             # Filter colors in image
def distance(p1, p2)                      # Calculate distance between points
def bernoulli(p)                          # Bernoulli random variable
def rand_float(start, end)                # Random float in range
```

### Detection (`src/detection/detection.py`)

```python
def load_model()                          # Load TensorFlow model
def canny(image)                          # Canny edge detection
def filter_color(image)                   # Color filtering for arrows
def run_inference_for_single_image(model, image) # Single inference
def sort_by_confidence(model, image)      # Sort predictions by confidence
def get_boxes(model, image)               # Get bounding boxes
def merge_detection(model, image)         # Merge detection results
```

## 🎮 Command Book System

### CommandBook (`src/command_book/command_book.py`)

```python
class CommandBook(Configurable):
    def __init__(self, file)              # Initialize command book
    def load_commands(self, file)         # Load commands from file
    def load_config(self)                 # Load configuration
    def save_config(self)                 # Save configuration
    def _set_keybinds(self)               # Set key bindings
```

## 🖥️ GUI Components

### View Components

```python
class Routine(LabelFrame):                # Routine view panel
class Status(LabelFrame):                 # Status display panel
class Minimap(LabelFrame):                # Minimap display panel
```

## 🔍 Search Patterns

### Find Functions by Purpose

#### Input Simulation

-   Search: `press|click|key_down|key_up`
-   Files: `src/common/vkeys.py`

#### Computer Vision

-   Search: `match|template|filter|canny`
-   Files: `src/common/utils.py`, `src/detection/detection.py`

#### Routine Execution

-   Search: `execute|main|routine|step`
-   Files: `src/routine/`, `src/modules/bot.py`

#### AI/ML

-   Search: `model|inference|detection|tensorflow`
-   Files: `src/detection/detection.py`

#### Configuration

-   Search: `config|settings|DEFAULT_CONFIG`
-   Files: `src/common/config.py`, `src/common/settings.py`

#### GUI

-   Search: `tkinter|LabelFrame|Button|Canvas`
-   Files: `src/gui/`

## 📊 Function Complexity Guide

### Simple Functions (Easy to understand)

-   `key_down()`, `key_up()`, `press()`, `click()`
-   `distance()`, `bernoulli()`, `rand_float()`
-   `Wait.main()`, `Walk.main()`

### Medium Functions (Require some understanding)

-   `Point.main()`, `Move.main()`
-   `multi_match()`, `single_match()`
-   `Bot._main()` (main loop)

### Complex Functions (Advanced understanding required)

-   `Bot._solve_rune()` (AI integration)
-   `Layout.get_shortest_path()` (A\* algorithm)
-   `merge_detection()` (TensorFlow inference)
-   `Routine.compile()` (CSV parsing)

## 🎯 Learning Priority

### Start Here (Essential)

1. `press()`, `click()` - Input simulation
2. `Point.main()` - Basic routine execution
3. `Bot._main()` - Main bot loop
4. `multi_match()` - Template matching

### Next Level (Important)

1. `Move.main()` - Movement logic
2. `Capture._main()` - Screenshot analysis
3. `Routine.compile()` - Routine parsing
4. `CommandBook.load_commands()` - Command loading

### Advanced (Expert)

1. `Bot._solve_rune()` - AI rune solving
2. `Layout.get_shortest_path()` - Pathfinding
3. `merge_detection()` - TensorFlow integration
4. GUI components - User interface
