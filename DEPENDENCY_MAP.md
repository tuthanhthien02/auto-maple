# Auto Maple Dependency Map

## 🗺️ Module Dependency Overview

```
main.py (Entry Point)
│
├── Bot Module
│   ├── CommandBook System
│   ├── Routine System
│   ├── Detection System
│   └── Common Utilities
│
├── Capture Module
│   ├── Common Utilities
│   └── Config System
│
├── Listener Module
│   ├── Common Interfaces
│   └── Common Utilities
│
├── Notifier Module
│   ├── Common Utilities
│   └── Routine Components
│
└── GUI Module
    ├── Common Config
    └── GUI Components
```

## 📦 Detailed Dependencies

### Core Modules Dependencies

#### `main.py`

```python
from src.modules.bot import Bot
from src.modules.capture import Capture
from src.modules.notifier import Notifier
from src.modules.listener import Listener
from src.modules.gui import GUI
```

#### `src/modules/bot.py`

```python
from src.common import config, utils
from src.detection import detection
from src.routine import components
from src.routine.routine import Routine
from src.command_book.command_book import CommandBook
from src.routine.components import Point
from src.common.vkeys import press, click
from src.common.interfaces import Configurable
```

#### `src/modules/capture.py`

```python
from src.common import config, utils
```

#### `src/modules/listener.py`

```python
from src.common.interfaces import Configurable
from src.common import config, utils
```

#### `src/modules/notifier.py`

```python
from src.common import config, utils
from src.routine.components import Point
```

#### `src/modules/gui.py`

```python
from src.common import config, settings
from src.gui import Menu, View, Edit, Settings
```

### Common System Dependencies

#### `src/common/config.py`

```python
# No internal dependencies - base configuration
```

#### `src/common/settings.py`

```python
# No internal dependencies - settings validation
```

#### `src/common/utils.py`

```python
from src.common import config, settings
```

#### `src/common/vkeys.py`

```python
from src.common import utils
```

#### `src/common/interfaces.py`

```python
# No internal dependencies - base interfaces
```

### Routine System Dependencies

#### `src/routine/routine.py`

```python
from src.common import config, settings, utils
from src.routine.components import Point, Label, Jump, Setting, Command, SYMBOLS
from src.routine.layout import Layout
```

#### `src/routine/components.py`

```python
from src.common import config, settings, utils
from src.common.vkeys import key_down, key_up, press
```

#### `src/routine/layout.py`

```python
from src.common import config, settings, utils
```

### Detection System Dependencies

#### `src/detection/detection.py`

```python
from src.common import utils
```

### Command Book System Dependencies

#### `src/command_book/command_book.py`

```python
from src.common import config, utils
from src.routine import components
from src.common.interfaces import Configurable
```

## 🔄 Circular Dependencies

### Potential Issues

-   **Bot ↔ Routine**: Bot uses Routine, Routine components may reference Bot
-   **Config ↔ All Modules**: Config is imported by all modules
-   **GUI ↔ All Modules**: GUI may need to access all module states

### Resolution Strategy

-   **Config**: Centralized, no circular imports
-   **Bot-Routine**: Bot controls Routine, Routine components are passive
-   **GUI**: Uses config to access module states, no direct imports

## 📊 Dependency Levels

### Level 0 (No Dependencies)

-   `src/common/config.py`
-   `src/common/settings.py`
-   `src/common/interfaces.py`

### Level 1 (Depends on Level 0)

-   `src/common/utils.py`
-   `src/detection/detection.py`

### Level 2 (Depends on Level 0-1)

-   `src/common/vkeys.py`
-   `src/routine/layout.py`
-   `src/routine/components.py`

### Level 3 (Depends on Level 0-2)

-   `src/routine/routine.py`
-   `src/command_book/command_book.py`

### Level 4 (Depends on Level 0-3)

-   `src/modules/capture.py`
-   `src/modules/listener.py`
-   `src/modules/notifier.py`

### Level 5 (Depends on Level 0-4)

-   `src/modules/bot.py`
-   `src/modules/gui.py`

### Level 6 (Depends on Level 0-5)

-   `main.py`

## 🔧 Import Patterns

### Standard Import Pattern

```python
# 1. Standard library imports
import os
import time
import threading

# 2. Third-party imports
import cv2
import numpy as np

# 3. Local imports (src modules)
from src.common import config, utils
from src.common.vkeys import press, click
```

### Config Access Pattern

```python
# All modules access global state through config
config.bot = self
config.player_pos = (x, y)
config.enabled = True
```

### Utility Usage Pattern

```python
# Common utilities are imported and used directly
from src.common.utils import multi_match, distance
result = multi_match(frame, template, threshold=0.8)
```

## 🚨 Dependency Issues & Solutions

### Common Problems

#### 1. Circular Import

```python
# BAD: Module A imports Module B, Module B imports Module A
# File A
from src.B import something

# File B
from src.A import something_else
```

**Solution**: Use config for communication

```python
# File A
config.some_value = value

# File B
value = config.some_value
```

#### 2. Missing Dependencies

```python
# BAD: Import not found
from src.nonexistent import something
```

**Solution**: Check file structure and imports

#### 3. Relative Import Issues

```python
# BAD: Relative imports in wrong context
from .common import config
```

**Solution**: Use absolute imports

```python
# GOOD: Absolute imports
from src.common import config
```

## 🎯 Refactoring Guidelines

### When Adding New Features

#### 1. Identify Dependency Level

-   Determine which level your new module belongs to
-   Import only from lower levels

#### 2. Use Config for Communication

-   Avoid direct module-to-module imports
-   Use config for shared state

#### 3. Follow Import Order

-   Standard library first
-   Third-party second
-   Local imports last

#### 4. Minimize Dependencies

-   Only import what you need
-   Avoid importing entire modules when possible

### Example: Adding New Detection Feature

```python
# src/detection/new_detection.py
import cv2
import numpy as np
from src.common import utils, config

class NewDetection:
    def __init__(self):
        # Initialize detection system
        pass

    def detect(self, frame):
        # Detection logic
        result = utils.multi_match(frame, template)
        config.new_detection_result = result
        return result
```

## 📋 Dependency Checklist

### Before Adding New Module

-   [ ] Identify correct dependency level
-   [ ] List all required imports
-   [ ] Check for circular dependencies
-   [ ] Use config for shared state
-   [ ] Follow import order convention

### Before Modifying Existing Module

-   [ ] Check all dependent modules
-   [ ] Update imports if needed
-   [ ] Test all dependent functionality
-   [ ] Update documentation

### Before Refactoring

-   [ ] Map all current dependencies
-   [ ] Identify breaking changes
-   [ ] Plan migration strategy
-   [ ] Test thoroughly
