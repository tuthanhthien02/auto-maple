# Auto Maple Search Guide

## 🔍 Effective Codebase Search Strategies

### 🎯 Quick Search Patterns

#### Find Functions by Purpose

```bash
# Input simulation
grep -r "press\|click\|key_down\|key_up" src/

# Computer vision
grep -r "multi_match\|single_match\|template" src/

# Routine execution
grep -r "execute\|main\|routine" src/

# AI/ML detection
grep -r "model\|tensorflow\|detection" src/

# Configuration
grep -r "config\|settings\|DEFAULT_CONFIG" src/

# GUI components
grep -r "tkinter\|LabelFrame\|Button" src/
```

#### Find Classes and Functions

```bash
# Find all class definitions
grep -r "^class " src/

# Find all function definitions
grep -r "^def " src/

# Find specific class
grep -r "class Bot" src/

# Find specific function
grep -r "def press" src/
```

#### Find Imports and Dependencies

```bash
# Find all imports
grep -r "^from\|^import" src/

# Find specific module imports
grep -r "from src\." src/

# Find external library imports
grep -r "import cv2\|import numpy\|import tensorflow" src/
```

## 🗂️ Search by File Type

### Core Logic Files

```bash
# Bot logic
grep -r "pattern" src/modules/bot.py

# Input simulation
grep -r "pattern" src/common/vkeys.py

# Computer vision
grep -r "pattern" src/common/utils.py

# AI detection
grep -r "pattern" src/detection/detection.py
```

### Configuration Files

```bash
# Global config
grep -r "pattern" src/common/config.py

# Settings
grep -r "pattern" src/common/settings.py

# Command book
grep -r "pattern" src/command_book/command_book.py
```

### Routine System Files

```bash
# Routine parser
grep -r "pattern" src/routine/routine.py

# Components
grep -r "pattern" src/routine/components.py

# Pathfinding
grep -r "pattern" src/routine/layout.py
```

## 🔧 Advanced Search Techniques

### Regex Patterns

#### Find Function Calls

```bash
# Find function calls with parameters
grep -r "function_name(" src/

# Find specific function calls
grep -r "press(" src/
grep -r "multi_match(" src/
grep -r "execute(" src/
```

#### Find Variable Usage

```bash
# Find variable assignments
grep -r "variable_name =" src/

# Find variable usage
grep -r "variable_name" src/

# Find config variable usage
grep -r "config\." src/
```

#### Find Error Handling

```bash
# Find try-except blocks
grep -r "try:\|except" src/

# Find error messages
grep -r "Error\|Exception" src/

# Find print statements
grep -r "print(" src/
```

### Context-Aware Search

#### Find Functions with Context

```bash
# Find function with 3 lines of context
grep -r -A 3 -B 3 "function_name" src/

# Find class with context
grep -r -A 5 -B 2 "class ClassName" src/
```

#### Find Related Code

```bash
# Find all references to a variable
grep -r -n "variable_name" src/

# Find all usages of a function
grep -r -n "function_name" src/
```

## 🎯 Specific Search Scenarios

### Debugging Issues

#### Bot Not Moving

```bash
# Check movement functions
grep -r "Move\|move\|key_down\|key_up" src/

# Check routine execution
grep -r "execute\|routine\|step" src/

# Check command book
grep -r "command_book\|CommandBook" src/
```

#### Template Matching Issues

```bash
# Check template matching
grep -r "multi_match\|single_match\|template" src/

# Check image processing
grep -r "cv2\|opencv\|filter" src/

# Check threshold values
grep -r "threshold" src/
```

#### Rune Solving Problems

```bash
# Check rune detection
grep -r "rune\|Rune" src/

# Check TensorFlow usage
grep -r "tensorflow\|model\|inference" src/

# Check detection functions
grep -r "detection\|merge_detection" src/
```

### Adding New Features

#### Find Similar Implementations

```bash
# Find existing command implementations
grep -r "class.*Command" src/

# Find existing GUI components
grep -r "class.*LabelFrame" src/

# Find existing detection methods
grep -r "def.*detect" src/
```

#### Find Configuration Patterns

```bash
# Find settings definitions
grep -r "DEFAULT_CONFIG" src/

# Find config usage
grep -r "config\." src/

# Find settings validation
grep -r "validate" src/
```

## 🛠️ IDE-Specific Search Tips

### VS Code

```
# Quick file search
Ctrl + P

# Search in files
Ctrl + Shift + F

# Go to definition
F12

# Find all references
Shift + F12

# Search with regex
Alt + R (in search box)
```

### PyCharm

```
# Quick file search
Ctrl + Shift + N

# Search everywhere
Double Shift

# Find in path
Ctrl + Shift + F

# Go to declaration
Ctrl + B

# Find usages
Alt + F7
```

### Vim/Neovim

```vim
" Search in current file
/pattern

" Search in all files
:vimgrep /pattern/ **/*.py

" Go to definition
gd

" Find references
gD
```

## 📊 Search Performance Tips

### Optimize Search Speed

```bash
# Search only in Python files
grep -r --include="*.py" "pattern" src/

# Exclude certain directories
grep -r --exclude-dir="__pycache__" "pattern" src/

# Use case-insensitive search
grep -ri "pattern" src/

# Count matches instead of showing content
grep -rc "pattern" src/
```

### Use File Filters

```bash
# Search only in specific modules
grep -r "pattern" src/modules/

# Search only in common utilities
grep -r "pattern" src/common/

# Search only in routine system
grep -r "pattern" src/routine/
```

## 🎯 Common Search Queries

### Find All Bot Controls

```bash
grep -r "enabled\|disabled\|toggle" src/
```

### Find All Input Methods

```bash
grep -r "press\|click\|key\|mouse" src/
```

### Find All Detection Methods

```bash
grep -r "match\|detect\|find\|locate" src/
```

### Find All Configuration Options

```bash
grep -r "setting\|config\|option" src/
```

### Find All Error Messages

```bash
grep -r "Error\|Exception\|Failed\|Invalid" src/
```

## 🔍 Search Best Practices

### 1. Start Broad, Then Narrow

```bash
# Start with broad search
grep -r "keyword" src/

# Narrow down to specific files
grep -r "keyword" src/modules/bot.py

# Get context around matches
grep -r -A 3 -B 3 "keyword" src/modules/bot.py
```

### 2. Use Multiple Search Terms

```bash
# Search for related terms
grep -r "press\|click\|key" src/

# Search for function and its usage
grep -r "def press\|press(" src/
```

### 3. Combine with File Operations

```bash
# Find files containing pattern
find src/ -name "*.py" -exec grep -l "pattern" {} \;

# Count occurrences in each file
find src/ -name "*.py" -exec grep -c "pattern" {} \;
```

### 4. Use Version Control

```bash
# Search in git history
git log -S "pattern" --oneline

# Search in specific commit
git show commit_hash | grep "pattern"

# Search in diff
git diff | grep "pattern"
```

## 📋 Search Checklist

### Before Starting Search

-   [ ] Identify the specific functionality you're looking for
-   [ ] Choose appropriate search terms
-   [ ] Decide on search scope (entire codebase vs specific files)
-   [ ] Consider case sensitivity

### During Search

-   [ ] Use context flags (-A, -B, -C) for better understanding
-   [ ] Try multiple related search terms
-   [ ] Check both function definitions and usages
-   [ ] Look for imports and dependencies

### After Search

-   [ ] Verify results are relevant
-   [ ] Check for related code nearby
-   [ ] Understand the context of matches
-   [ ] Document findings for future reference

## 🚀 Pro Tips

### 1. Use Search History

-   Most IDEs remember search history
-   Reuse successful search patterns
-   Build a personal search pattern library

### 2. Combine Search with Navigation

-   Use search to find entry points
-   Navigate through code using "Go to Definition"
-   Follow the call chain to understand flow

### 3. Search for Patterns, Not Just Text

-   Look for code patterns and structures
-   Search for error handling patterns
-   Find configuration patterns

### 4. Use External Tools

-   Use `ripgrep` for faster searching
-   Use `ag` (the silver searcher) for better performance
-   Use `fd` for file finding

### 5. Create Search Aliases

```bash
# Add to .bashrc or .zshrc
alias gpy="grep -r --include='*.py'"
alias gsrc="grep -r src/"
alias gfunc="grep -r '^def '"
alias gclass="grep -r '^class '"
```
