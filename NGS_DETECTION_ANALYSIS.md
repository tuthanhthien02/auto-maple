# 🔍 NGS Detection Analysis - Phần Nào Trigger NGS?

## ✅ **4 Scripts Keyboard Hooks KHÔNG phải vấn đề**

Nếu bạn **CHỈ DÙNG BOT** (không chạy 4 scripts keyboard hooks):

-   ❌ `keyboard_to_arduino.py` - KHÔNG chạy
-   ❌ `keyboard_block_arduino.py` - KHÔNG chạy
-   ❌ `host_sender.py` - KHÔNG chạy
-   ❌ `vmware_receiver.py` - KHÔNG chạy

**→ 4 scripts này KHÔNG liên quan đến vấn đề NGS detection khi chỉ dùng bot.**

---

## 🚨 **PHẦN TRIGGER NGS TRONG BOT**

### **1. Process Stealth (HIGH RISK)**

**File:** `src/modules/bot.py` (dòng 80-83)

```python
# Enable process stealth (optional)
try:
    enable_process_stealth()
except Exception as e:
    log.warning("Failed to enable process stealth: %s", e)
```

**Vấn đề:**

-   ✅ **Hide console** - NGS có thể detect process không có console window
-   ✅ **Minimize memory footprint** - NGS có thể detect memory manipulation
-   ✅ **Obfuscate memory patterns** - NGS có thể detect memory obfuscation
-   ✅ **Process monitoring** - NGS có thể detect process monitoring behavior

**NGS Detection Risk:** ⚠️ **HIGH RISK**

**Lý do:**

-   Process stealth features thay đổi process behavior
-   NGS có thể detect các thay đổi này như dấu hiệu của automation tool
-   Memory obfuscation và process hiding là các kỹ thuật thường được dùng bởi cheats/bots

---

### **2. SendInput API (MEDIUM-HIGH RISK)**

**File:** `src/common/vkeys.py` (dòng 174-337)

```python
user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))
```

**Vấn đề:**

-   ✅ **SendInput API** - NGS có thể detect simulated input
-   ✅ **Timing patterns** - NGS có thể detect timing patterns không tự nhiên
-   ✅ **Input patterns** - NGS có thể detect input patterns giống automation

**NGS Detection Risk:** ⚠️ **MEDIUM-HIGH RISK**

**Lý do:**

-   SendInput là một API phổ biến cho automation tools
-   NGS có thể detect simulated input thông qua timing analysis
-   Nếu không dùng Arduino, bot sẽ dùng SendInput → NGS có thể detect

---

### **3. Anti-Detect Features (LOW-MEDIUM RISK)**

**File:** `src/common/anti_detect.py`, `src/common/anti_detect_config.py`

**Vấn đề:**

-   ✅ **Timing randomization** - NGS có thể detect timing patterns ngay cả khi randomized
-   ✅ **Pattern diversification** - NGS có thể detect pattern changes
-   ✅ **Memory optimization** - NGS có thể detect memory cleanup patterns

**NGS Detection Risk:** ⚠️ **LOW-MEDIUM RISK**

**Lý do:**

-   Anti-detect features có thể làm giảm detection risk
-   Nhưng nếu implementation không tốt, có thể tạo ra patterns mới
-   Memory optimization có thể tạo ra memory patterns có thể detect

---

### **4. Screenshot Blocking (DISABLED - OK)**

**File:** `src/modules/bot.py` (dòng 85-91)

```python
# Enable screenshot blocking (recommended) - DISABLED TEMPORARILY
# try:
#     enable_screenshot_blocking()
#     protect_maplestory_window()
#     print("[Bot] Screenshot blocking enabled")
# except Exception as e:
#     print(f"[Bot] Failed to enable screenshot blocking: {e}")
```

**Status:** ✅ **DISABLED** - Không trigger NGS

---

## 📊 **TỔNG KẾT NGS RISK**

| Feature                  | Status      | NGS Risk       | Trigger NGS? |
| ------------------------ | ----------- | -------------- | ------------ |
| **Process Stealth**      | ✅ Enabled  | ⚠️ HIGH        | **YES**      |
| **SendInput API**        | ✅ Enabled  | ⚠️ MEDIUM-HIGH | **YES**      |
| **Anti-Detect Features** | ✅ Enabled  | ⚠️ LOW-MEDIUM  | **MAYBE**    |
| **Screenshot Blocking**  | ❌ Disabled | ✅ NONE        | **NO**       |
| **Keyboard Hooks**       | ❌ Not used | ✅ NONE        | **NO**       |

---

## 🎯 **NGUYÊN NHÂN CHÍNH: Process Stealth + SendInput**

### **Tại sao Process Stealth trigger NGS?**

1. **Hide Console:**

    - Bot process không có console window
    - NGS có thể detect process không có console → automation tool

2. **Memory Obfuscation:**

    - Bot tạo memory noise patterns
    - NGS có thể detect memory obfuscation → cheat signature

3. **Process Monitoring:**
    - Bot monitor process behavior
    - NGS có thể detect process monitoring → suspicious activity

### **Tại sao SendInput trigger NGS?**

1. **Simulated Input:**

    - SendInput là API phổ biến cho automation
    - NGS có thể detect simulated input → automation tool

2. **Timing Patterns:**

    - SendInput có timing patterns không tự nhiên
    - NGS có thể detect timing patterns → automation signature

3. **Input Patterns:**
    - Bot có input patterns giống automation
    - NGS có thể detect input patterns → bot behavior

---

## 🔧 **GIẢI PHÁP**

### **1. Disable Process Stealth (RECOMMENDED)**

**File:** `src/modules/bot.py`

```python
# Disable process stealth
# try:
#     enable_process_stealth()
# except Exception as e:
#     log.warning("Failed to enable process stealth: %s", e)
```

**Lý do:**

-   Process stealth có HIGH RISK trigger NGS
-   Disable process stealth giảm NGS detection risk đáng kể

---

### **2. Use Arduino Instead of SendInput (RECOMMENDED)**

**File:** `src/common/config.py`

```python
# Enable Arduino
use_arduino = True
arduino_com_port = 'COM3'  # Your Arduino port
arduino_baudrate = 115200
```

**Lý do:**

-   Arduino HID keyboard là hardware thật → NGS khó detect
-   SendInput là software API → NGS dễ detect
-   Arduino giảm NGS detection risk đáng kể

---

### **3. Keep Anti-Detect Features (OPTIONAL)**

**File:** `src/common/anti_detect_config.py`

-   ✅ **Keep timing randomization** - Giúp giảm timing patterns
-   ✅ **Keep pattern diversification** - Giúp giảm input patterns
-   ⚠️ **Monitor memory optimization** - Có thể tạo memory patterns

**Lý do:**

-   Anti-detect features có thể giúp giảm detection risk
-   Nhưng cần monitor để đảm bảo không tạo patterns mới

---

## 📋 **WORKFLOW AN TOÀN**

### **Option 1: Disable Process Stealth + Use Arduino (BEST)**

```
1. Disable process stealth trong bot.py
2. Enable Arduino trong config
3. Kill ALL → kill_all_before_game.bat
4. Start game
5. Wait for game loaded
6. Start bot
```

**NGS Risk:** ✅ **LOW**

---

### **Option 2: Disable Process Stealth + Use SendInput (ACCEPTABLE)**

```
1. Disable process stealth trong bot.py
2. Use SendInput (default)
3. Kill ALL → kill_all_before_game.bat
4. Start game
5. Wait for game loaded
6. Start bot
```

**NGS Risk:** ⚠️ **MEDIUM**

---

## ⚠️ **QUAN TRỌNG**

### **Process Stealth là nguyên nhân chính:**

1. ✅ **Process stealth** có HIGH RISK trigger NGS
2. ✅ **SendInput** có MEDIUM-HIGH RISK trigger NGS
3. ✅ **Anti-detect features** có LOW-MEDIUM RISK trigger NGS

### **Khuyến nghị:**

1. ✅ **Disable process stealth** - Giảm NGS risk đáng kể
2. ✅ **Use Arduino** - Giảm NGS risk đáng kể
3. ✅ **Keep anti-detect features** - Có thể giúp giảm detection risk

---

## 🎯 **KẾT LUẬN**

### **Nguyên nhân chính:**

1. ⚠️ **Process Stealth** - HIGH RISK → **DISABLE**
2. ⚠️ **SendInput API** - MEDIUM-HIGH RISK → **USE ARDUINO**
3. ⚠️ **Anti-Detect Features** - LOW-MEDIUM RISK → **KEEP (monitor)**

### **4 scripts keyboard hooks:**

-   ✅ **KHÔNG liên quan** - Nếu bạn chỉ dùng bot, không chạy 4 scripts này

---

**REMEMBER:** Process Stealth + SendInput = NGS Detection Risk. Disable Process Stealth + Use Arduino = Giảm NGS Risk!
