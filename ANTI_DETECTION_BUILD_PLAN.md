# 🛡️ Anti-Detection Build Plan - Codebase Stealth

## 📋 Tổng quan

Plan để build codebase này với các tính năng anti-detection để tránh bị detect bởi NGS (Nexon Game Security) và các anti-cheat systems khác.

---

## 🎯 Mục tiêu

1. **Giảm khả năng bị detect** bởi NGS và anti-cheat systems
2. **Che giấu bot process** khỏi monitoring tools
3. **Obfuscate code** để khó phân tích
4. **Giảm signatures** có thể bị detect
5. **Stealth GUI** và process name

---

## 📊 Phân tích hiện trạng

### **✅ Có sẵn:**

1. **Anti-detect features** (`src/common/anti_detect.py`)

    - Timing randomization
    - Behavioral simulation (disabled)
    - Pattern diversification
    - Memory optimization

2. **Process stealth** (`src/common/process_stealth.py`)

    - Hide console window
    - Minimize memory footprint
    - Memory pattern obfuscation
    - Process monitoring

3. **Screenshot blocking** (`src/common/screenshot_blocker.py`)

    - Block Print Screen
    - Block Snipping Tool
    - Block third-party tools
    - Window protection (disabled)

4. **Build scripts:**

    - `build_stealth.bat` - Basic PyInstaller build
    - `build_stealth.ps1` - PowerShell build
    - `ExplorerSettings.spec` - PyInstaller spec file

5. **GUI Stealth:**
    - Icon: `explorer-icon.ico` (Explorer Settings)
    - Window title: "Explorer Settings"
    - Process name: "ExplorerSettings.exe"

### **⚠️ Thiếu/Cần cải thiện:**

1. **Code Obfuscation:** Chưa có obfuscation cho Python code
2. **String Encryption:** Strings trong code có thể bị scan
3. **UPX Packing:** Chưa dùng UPX để compress/pack
4. **Signature Removal:** Chưa remove Python signatures
5. **Process Name Obfuscation:** Chưa đổi process name runtime
6. **Memory Encryption:** Chưa encrypt sensitive data trong memory
7. **Import Obfuscation:** Chưa obfuscate imports
8. **Advanced Stealth:** Chưa có advanced techniques

---

## 🏗️ Build Plan - Phases

### **Phase 1: Basic Stealth (Low Risk)** ⭐⭐⭐ HIGH PRIORITY

**Mục tiêu:** Cải thiện build hiện tại với các tính năng stealth cơ bản

#### **1.1 PyInstaller Obfuscation**

-   ✅ **UPX Packing:** Enable UPX compression (`--upx-dir`)
-   ✅ **One-file Build:** Single executable (đã có)
-   ✅ **Windowed Mode:** No console window (đã có)
-   ✅ **Icon Stealth:** Explorer icon (đã có)
-   ✅ **Name Stealth:** ExplorerSettings.exe (đã có)

**Files to modify:**

-   `ExplorerSettings.spec` - Update PyInstaller options
-   `build_stealth.bat` - Add UPX packing
-   `build_stealth.ps1` - Add UPX packing

**Risk:** LOW - Chỉ là build configuration

---

#### **1.2 Process Stealth Enhancement**

-   ✅ **Enable Process Stealth:** Uncomment trong `bot.py`
-   ✅ **Hide Console:** Đã có sẵn
-   ✅ **Process Name Change:** Runtime process name change (nếu có thể)
-   ✅ **Memory Minimization:** Đã có sẵn

**Files to modify:**

-   `src/modules/bot.py` - Enable process stealth
-   `src/common/process_stealth.py` - Enhance process name change

**Risk:** LOW - Chỉ enable existing features

---

#### **1.3 Screenshot Blocking**

-   ✅ **Enable Screenshot Blocking:** Uncomment trong `bot.py`
-   ✅ **Window Protection:** Protect MapleStory window
-   ✅ **Print Screen Block:** Block Print Screen key
-   ✅ **Tool Blocking:** Block screenshot tools

**Files to modify:**

-   `src/modules/bot.py` - Enable screenshot blocking
-   `src/common/screenshot_blocker.py` - Enhance blocking

**Risk:** LOW-MEDIUM - Cần test với game

---

### **Phase 2: Code Obfuscation (Medium Risk)** ⭐⭐ MEDIUM PRIORITY

**Mục tiêu:** Obfuscate Python code để khó phân tích

#### **2.1 PyArmor Integration**

-   ✅ **Install PyArmor:** Python code obfuscator
-   ✅ **Obfuscate Source:** Obfuscate `.py` files trước khi build
-   ✅ **String Encryption:** Encrypt strings trong code
-   ✅ **Import Obfuscation:** Obfuscate imports

**Implementation:**

```python
# Install PyArmor
pip install pyarmor

# Obfuscate before build
pyarmor gen --obf-code 1 --obf-mod 1 --wrap-mode 1 src/
```

**Files to create:**

-   `build_obfuscate.bat` - Build với PyArmor
-   `build_obfuscate.ps1` - PowerShell version

**Risk:** MEDIUM - Có thể ảnh hưởng performance

---

#### **2.2 String Encryption**

-   ✅ **Encrypt Strings:** Encrypt sensitive strings (key names, paths, etc.)
-   ✅ **Runtime Decryption:** Decrypt tại runtime
-   ✅ **Avoid Hardcoded Strings:** Remove hardcoded suspicious strings

**Files to modify:**

-   `src/common/vkeys.py` - Encrypt key names
-   `src/modules/listener.py` - Encrypt config keys
-   `src/common/config.py` - Encrypt paths

**Risk:** LOW - Chỉ encrypt strings

---

#### **2.3 Import Obfuscation**

-   ✅ **Dynamic Imports:** Use `__import__()` thay vì `import`
-   ✅ **Import Aliasing:** Use aliases để hide imports
-   ✅ **Lazy Loading:** Load modules khi cần

**Files to modify:**

-   All import statements trong codebase
-   Critical modules only (anti-detect, stealth)

**Risk:** MEDIUM - Có thể break code nếu không cẩn thận

---

### **Phase 3: Advanced Stealth (High Risk)** ⭐ LOW PRIORITY

**Mục tiêu:** Advanced stealth techniques (cần test kỹ)

#### **3.1 Process Injection**

-   ⚠️ **DLL Injection:** Inject vào process khác (không recommend)
-   ⚠️ **Process Hollowing:** Hollow process để hide (không recommend)

**Risk:** HIGH - Có thể bị detect bởi anti-virus

---

#### **3.2 Memory Encryption**

-   ✅ **Encrypt Sensitive Data:** Encrypt data trong memory
-   ✅ **Runtime Decryption:** Decrypt khi cần
-   ✅ **Clear Memory:** Clear sensitive data sau khi dùng

**Files to modify:**

-   `src/common/config.py` - Encrypt config data
-   `src/modules/bot.py` - Encrypt routine data

**Risk:** MEDIUM - Có thể ảnh hưởng performance

---

#### **3.3 Advanced Process Stealth**

-   ⚠️ **Process Hiding:** Hide từ Task Manager (không recommend)
-   ✅ **Process Name Spoofing:** Spoof process name
-   ✅ **Parent Process Spoofing:** Spoof parent process

**Risk:** HIGH - Có thể bị detect

---

## 📋 Detailed Implementation Plan

### **Phase 1: Basic Stealth**

#### **Step 1.1: Enhance PyInstaller Build**

**File:** `ExplorerSettings.spec`

**Changes:**

```python
# Add UPX packing
upx=True,
upx_exclude=[],

# Add obfuscation options
debug=False,
strip=True,  # Strip debug symbols

# Add console=False (already have)
console=False,

# Add optimized imports
optimize=2,  # Python optimization level
```

**File:** `build_stealth.bat`

**Changes:**

```batch
REM Add UPX packing
--upx-dir "%USERPROFILE%\upx" ^

REM Add strip option
--strip ^

REM Add optimize
--optimize 2 ^
```

---

#### **Step 1.2: Enable Process Stealth**

**File:** `src/modules/bot.py`

**Changes:**

```python
# Line 74-78: Already enabled, ensure it works
try:
    enable_process_stealth()
except Exception as e:
    log.warning("Failed to enable process stealth: %s", e)
```

**File:** `src/common/process_stealth.py`

**Enhancements:**

-   Improve `change_process_name()` để thực sự đổi tên process
-   Add process name spoofing
-   Add memory pattern randomization

---

#### **Step 1.3: Enable Screenshot Blocking**

**File:** `src/modules/bot.py`

**Changes:**

```python
# Line 80-86: Uncomment screenshot blocking
try:
    enable_screenshot_blocking()
    protect_maplestory_window()
    print("[Bot] Screenshot blocking enabled")
except Exception as e:
    print(f"[Bot] Failed to enable screenshot blocking: {e}")
```

**File:** `src/common/screenshot_blocker.py`

**Enhancements:**

-   Improve API blocking
-   Add more screenshot tool detection
-   Enhance window protection

---

### **Phase 2: Code Obfuscation**

#### **Step 2.1: PyArmor Integration**

**Create:** `build_obfuscate.bat`

```batch
@echo off
REM Obfuscate source code với PyArmor
pyarmor gen --obf-code 1 --obf-mod 1 --wrap-mode 1 src/

REM Build với PyInstaller
pyinstaller ExplorerSettings.spec
```

**Note:** Cần test kỹ vì PyArmor có thể ảnh hưởng performance

---

#### **Step 2.2: String Encryption**

**Create:** `src/common/string_encrypt.py`

```python
"""String encryption utilities."""

import base64
import hashlib
from cryptography.fernet import Fernet

# Simple XOR encryption (lightweight)
def encrypt_string(s: str, key: str) -> str:
    """Encrypt string với XOR."""
    key_bytes = key.encode()
    encrypted = bytearray()
    for i, c in enumerate(s.encode()):
        encrypted.append(c ^ key_bytes[i % len(key_bytes)])
    return base64.b64encode(encrypted).decode()

def decrypt_string(encrypted: str, key: str) -> str:
    """Decrypt string."""
    encrypted_bytes = base64.b64decode(encrypted.encode())
    decrypted = bytearray()
    key_bytes = key.encode()
    for i, c in enumerate(encrypted_bytes):
        decrypted.append(c ^ key_bytes[i % len(key_bytes)])
    return decrypted.decode()
```

**Usage:**

```python
from src.common.string_encrypt import encrypt_string, decrypt_string

# Encrypt sensitive strings
ENCRYPTED_KEY = encrypt_string('insert', 'secret_key')
decrypted = decrypt_string(ENCRYPTED_KEY, 'secret_key')
```

---

#### **Step 2.3: Import Obfuscation**

**Example:**

```python
# Before:
import keyboard as kb

# After:
kb = __import__('keyboard', globals(), locals(), [], 0)
```

**Risk:** Có thể break code, chỉ apply cho critical modules

---

### **Phase 3: Advanced Stealth (Optional)**

#### **Step 3.1: Memory Encryption**

**Create:** `src/common/memory_encrypt.py`

```python
"""Memory encryption utilities."""

import ctypes
from cryptography.fernet import Fernet

class SecureMemory:
    """Encrypt sensitive data trong memory."""

    def __init__(self, key=None):
        if key is None:
            key = Fernet.generate_key()
        self.cipher = Fernet(key)

    def encrypt(self, data: bytes) -> bytes:
        """Encrypt data."""
        return self.cipher.encrypt(data)

    def decrypt(self, encrypted: bytes) -> bytes:
        """Decrypt data."""
        return self.cipher.decrypt(encrypted)

    def clear(self, data: bytes):
        """Clear memory."""
        ctypes.memset(ctypes.addressof(data), 0, len(data))
```

---

## 🎯 Recommended Implementation Order

### **Priority 1: Quick Wins (Low Risk)** ⭐⭐⭐

1. ✅ **Enable Process Stealth** - Uncomment trong `bot.py`
2. ✅ **Enable Screenshot Blocking** - Uncomment trong `bot.py`
3. ✅ **Enhance PyInstaller Build** - Add UPX packing, strip symbols
4. ✅ **Test Build** - Ensure build works với stealth features

### **Priority 2: Code Obfuscation (Medium Risk)** ⭐⭐

1. ⚠️ **PyArmor Integration** - Test trước khi apply
2. ⚠️ **String Encryption** - Encrypt sensitive strings
3. ⚠️ **Import Obfuscation** - Critical modules only

### **Priority 3: Advanced (High Risk)** ⭐

1. ❌ **Memory Encryption** - Optional, có thể ảnh hưởng performance
2. ❌ **Advanced Process Stealth** - Optional, risk cao

---

## 📊 Risk Assessment

| Feature                 | Risk       | Impact | Priority |
| ----------------------- | ---------- | ------ | -------- |
| **Process Stealth**     | LOW        | HIGH   | ⭐⭐⭐   |
| **Screenshot Blocking** | LOW-MEDIUM | HIGH   | ⭐⭐⭐   |
| **UPX Packing**         | LOW        | MEDIUM | ⭐⭐⭐   |
| **PyArmor Obfuscation** | MEDIUM     | HIGH   | ⭐⭐     |
| **String Encryption**   | LOW        | MEDIUM | ⭐⭐     |
| **Import Obfuscation**  | MEDIUM     | LOW    | ⭐       |
| **Memory Encryption**   | MEDIUM     | LOW    | ⭐       |
| **Process Hiding**      | HIGH       | MEDIUM | ❌       |

---

## 🛠️ Build Scripts

### **1. Basic Stealth Build**

**File:** `build_stealth_enhanced.bat`

```batch
@echo off
REM Enhanced stealth build với UPX packing

pyinstaller --noconfirm --clean ^
  --name "ExplorerSettings" ^
  --windowed ^
  --icon "assets/explorer-icon.ico" ^
  --add-data "assets;assets" ^
  --add-data "resources;resources" ^
  --add-data "src;src" ^
  --upx-dir "%USERPROFILE%\upx" ^
  --strip ^
  --optimize 2 ^
  main.py
```

---

### **2. Obfuscated Build**

**File:** `build_obfuscate.bat`

```batch
@echo off
REM Obfuscate source code trước khi build

REM Install PyArmor
pip install pyarmor

REM Obfuscate source
pyarmor gen --obf-code 1 --obf-mod 1 --wrap-mode 1 src/

REM Build với PyInstaller
pyinstaller ExplorerSettings.spec
```

---

## ⚠️ Important Notes

### **1. Testing Requirements:**

-   ✅ **Test build** sau mỗi phase
-   ✅ **Test với game** để ensure không bị detect
-   ✅ **Test performance** để ensure không lag
-   ✅ **Test stability** để ensure không crash

### **2. Compatibility:**

-   ⚠️ **PyArmor** có thể không compatible với một số Python versions
-   ⚠️ **UPX** có thể không work với một số Windows versions
-   ⚠️ **Screenshot blocking** có thể conflict với một số tools

### **3. Legal/Ethical:**

-   ⚠️ **Obfuscation** không phải là cách để bypass security
-   ⚠️ **Use responsibly** - chỉ dùng cho legitimate purposes
-   ⚠️ **Respect ToS** - tuân thủ Terms of Service

---

## 📋 Checklist

### **Phase 1: Basic Stealth**

-   [ ] Enable process stealth trong `bot.py`
-   [ ] Enable screenshot blocking trong `bot.py`
-   [ ] Add UPX packing vào build scripts
-   [ ] Add strip symbols vào build scripts
-   [ ] Test build với stealth features
-   [ ] Test với game để ensure không bị detect

### **Phase 2: Code Obfuscation**

-   [ ] Install PyArmor
-   [ ] Create obfuscation build script
-   [ ] Test obfuscated build
-   [ ] Implement string encryption
-   [ ] Test string encryption
-   [ ] Implement import obfuscation (critical modules only)
-   [ ] Test import obfuscation

### **Phase 3: Advanced (Optional)**

-   [ ] Implement memory encryption
-   [ ] Test memory encryption
-   [ ] Advanced process stealth (nếu cần)

---

## 🎯 Final Recommendations

### **Best Approach:**

1. **Start với Phase 1** - Low risk, high impact
2. **Test thoroughly** sau mỗi phase
3. **Evaluate results** trước khi proceed
4. **Only implement Phase 2** nếu Phase 1 không đủ
5. **Skip Phase 3** trừ khi thực sự cần

### **Minimal Stealth Build:**

-   ✅ Process stealth enabled
-   ✅ Screenshot blocking enabled
-   ✅ UPX packing
-   ✅ Strip symbols
-   ✅ Windowed mode (no console)

### **Maximum Stealth Build:**

-   ✅ All Phase 1 features
-   ✅ PyArmor obfuscation
-   ✅ String encryption
-   ✅ Import obfuscation (critical only)
-   ✅ Memory encryption (optional)

---

## 📝 Next Steps

1. **Review plan** này với team/user
2. **Decide priority** - Phase nào muốn implement
3. **Test existing features** - Ensure chúng work
4. **Implement Phase 1** - Quick wins
5. **Test và evaluate** - Xem có đủ không
6. **Proceed to Phase 2** nếu cần

---

**Note:** Tất cả changes đều cần test kỹ trước khi deploy. Focus vào Phase 1 trước (low risk, high impact).
