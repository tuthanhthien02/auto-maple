# Auto Maple Codebase Index

## 📁 File Structure Overview

### 🚀 Entry Points

-   `main.py` - Application entry point, initializes all modules
-   `setup.py` - Creates desktop shortcut, requires admin privileges

### 🧠 Core Modules (`src/modules/`)

-   `bot.py` - Main bot logic, routine execution, rune solving
-   `capture.py` - Screenshot capture, minimap analysis, player tracking
-   `listener.py` - Keyboard input listener, hotkey handling
-   `notifier.py` - Event detection (elite boss, other players, runes)
-   `gui.py` - Main GUI application, window management

### 🔧 Common Utilities (`src/common/`)

-   `vkeys.py` - Keyboard/mouse simulation using Windows API
-   `config.py` - Global configuration variables
-   `settings.py` - Settings validation and management
-   `utils.py` - Helper functions (template matching, math, etc.)
-   `interfaces.py` - Base classes for configurable components

### 🎯 Detection & AI (`src/detection/`)

-   `detection.py` - TensorFlow model for rune arrow detection

### 📋 Routine System (`src/routine/`)

-   `routine.py` - Routine parser and execution engine
-   `components.py` - Routine components (Point, Label, Jump, Commands)
-   `layout.py` - Pathfinding system with quadtree and A\* algorithm

### ⚔️ Command Books (`src/command_book/`)

-   `command_book.py` - Command book loader and manager
-   `resources/keybindings/` - Class-specific key mappings

### 🖥️ GUI Components (`src/gui/`)

-   `__init__.py` - GUI package initialization
-   `menu/` - Menu bar components (File, Update)
-   `view/` - Main view components (Routine, Minimap, Details, Status)
-   `edit/` - Edit mode components
-   `settings/` - Settings panels (Main, Pets)
-   `interfaces.py` - GUI base classes and widgets

### 🎨 Assets

-   `assets/` - Template images, TensorFlow models, sound files
-   `resources/` - Community resources (command books, routines)

## 🔍 Quick Reference

### Key Functions by Category

#### Bot Control

-   `Bot._main()` - Main bot execution loop
-   `Bot._solve_rune()` - Automatic rune solving
-   `Bot.load_commands()` - Load command book

#### Input Simulation

-   `press(key, n, down_time, up_time)` - Simulate key press
-   `click(position, button)` - Simulate mouse click
-   `key_down(key)` / `key_up(key)` - Key hold/release

#### Computer Vision

-   `multi_match(frame, template, threshold)` - Template matching
-   `filter_color(image, ranges)` - Color filtering
-   `canny(image)` - Edge detection

#### Routine Components

-   `Point.execute()` - Execute point actions
-   `Move.main()` - Movement logic
-   `Buff.main()` - Buff management

#### Detection & AI

-   `load_model()` - Load TensorFlow model
-   `merge_detection(model, image)` - Rune arrow detection
-   `sort_by_confidence(model, image)` - Get top predictions

## 🗺️ Dependency Map

```
main.py
├── Bot (src/modules/bot.py)
│   ├── CommandBook (src/command_book/command_book.py)
│   ├── Routine (src/routine/routine.py)
│   ├── Detection (src/detection/detection.py)
│   └── VKeys (src/common/vkeys.py)
├── Capture (src/modules/capture.py)
│   ├── Utils (src/common/utils.py)
│   └── Config (src/common/config.py)
├── Listener (src/modules/listener.py)
├── Notifier (src/modules/notifier.py)
└── GUI (src/modules/gui.py)
    ├── Menu Components (src/gui/menu/)
    ├── View Components (src/gui/view/)
    └── Edit Components (src/gui/edit/)
```

## 🎯 Search Patterns

### Finding Specific Functionality

#### Keyboard/Mouse Input

-   Search: `press|click|key_down|key_up`
-   Files: `src/common/vkeys.py`

#### Template Matching

-   Search: `multi_match|single_match|template`
-   Files: `src/common/utils.py`, `src/modules/capture.py`

#### Routine Execution

-   Search: `execute|main|routine`
-   Files: `src/routine/components.py`, `src/modules/bot.py`

#### AI/ML Detection

-   Search: `model|tensorflow|detection|inference`
-   Files: `src/detection/detection.py`

#### GUI Components

-   Search: `tkinter|LabelFrame|Button|Canvas`
-   Files: `src/gui/`

#### Configuration

-   Search: `config|settings|DEFAULT_CONFIG`
-   Files: `src/common/config.py`, `src/common/settings.py`

## 🔧 Development Workflow

### Adding New Features

1. **Core Logic**: Add to appropriate module in `src/modules/`
2. **GUI Integration**: Add UI components in `src/gui/`
3. **Configuration**: Update `src/common/settings.py` if needed
4. **Documentation**: Update this index

### Debugging

1. **Check logs**: Console output shows module initialization
2. **GUI Debug**: Use GUI status panels to monitor state
3. **Template Issues**: Check `assets/` template images
4. **Model Issues**: Verify TensorFlow model in `assets/models/`

### Testing

1. **Unit Tests**: Test individual functions
2. **Integration Tests**: Test module interactions
3. **Game Tests**: Test with actual MapleStory running
4. **Performance Tests**: Monitor CPU/memory usage

## 📖 Learning Path

### Beginner

1. Start with `main.py` to understand initialization
2. Read `src/common/vkeys.py` for input simulation
3. Explore `src/modules/bot.py` for main logic
4. Try creating simple routines

### Intermediate

1. Study `src/routine/components.py` for routine system
2. Learn `src/detection/detection.py` for AI features
3. Understand `src/common/utils.py` for computer vision
4. Create custom command books

### Advanced

1. Modify `src/modules/capture.py` for new detection
2. Extend `src/routine/layout.py` for pathfinding
3. Customize `src/gui/` for new UI features
4. Optimize performance and add new features

## 🚨 Common Issues & Solutions

### Template Matching Fails

-   Check template images in `assets/`
-   Verify color ranges in detection code
-   Adjust threshold values

### Bot Not Moving

-   Check command book is loaded
-   Verify routine has valid points
-   Ensure game window is focused

### Rune Solving Fails

-   Verify TensorFlow model is present
-   Check rune template images
-   Monitor detection confidence scores

### GUI Issues

-   Check tkinter installation
-   Verify GUI thread safety
-   Monitor console for errors

## 📝 Notes

-   Always run as Administrator for full functionality
-   Keep MapleStory window visible and focused
-   Test changes on secondary account first
-   Backup important routines and configurations
