# 📋 Workflow: keyboard_to_arduino.py vs keyboard_block_arduino.py

## 🎯 Tổng Quan

Bạn có **2 scripts** với **mục đích khác nhau**:

1. **`keyboard_to_arduino.py`** - Forward hardware keyboard input → Arduino
2. **`keyboard_block_arduino.py`** - Block Arduino input, allow hardware input

---

## 📖 Script 1: keyboard_to_arduino.py

### **Mục Đích:**

**Forward hardware keyboard input từ máy tính → Arduino HID Keyboard**

### **Workflow:**

```
Hardware Keyboard (Physical)
    ↓
[keyboard_to_arduino.py] - Keyboard Hook
    ↓
Arduino Pro Micro (qua Serial/USB)
    ↓
Arduino HID Keyboard (simulate input)
    ↓
Game (nhận input từ Arduino HID)
```

### **Chức Năng:**

1. **Capture hardware keyboard input** (keyboard vật lý của máy)
2. **Forward qua Serial** đến Arduino Pro Micro
3. **Arduino HID** simulate input như hardware keyboard thật
4. **Block original input** (optional) - để game chỉ nhận từ Arduino

### **Khi Nào Dùng:**

✅ **Dùng khi:**

-   Bạn muốn forward input từ hardware keyboard → Arduino
-   Bạn muốn game nhận input từ Arduino HID (hardware thật, có VID/PID)
-   Tránh NGS detection bằng cách dùng hardware keyboard thật

❌ **KHÔNG dùng khi:**

-   Bạn chỉ dùng bot (không cần forward hardware input)
-   Bạn đang dùng VM keyboard (không có hardware keyboard thật)

### **NGS Detection Risk:**

⚠️ **HIGH RISK** - Script này có **keyboard hook**:

-   NGS có thể detect keyboard hook ngay cả khi bot chưa chạy
-   **PHẢI kill** script này TRƯỚC KHI start game
-   Nếu script đang chạy khi start game → NGS detect → Crash → Ban

### **Cách Dùng:**

```bash
# Chạy script
python keyboard_to_arduino.py [COM_PORT] [BAUDRATE] [BLOCK_INPUT] [STUCK_KEY_TIMEOUT] [ENABLE_LOGGING]

# Example:
python keyboard_to_arduino.py COM3 115200 true 10.0 false
```

**Hotkeys:**

-   **PageDown**: Toggle block original input
-   **PageUp**: Toggle forwarding
-   **Home**: Show statistics
-   **End**: Exit

---

## 📖 Script 2: keyboard_block_arduino.py

### **Mục Đích:**

**Block Arduino simulate input, allow hardware input to pass through**

### **Workflow:**

```
Arduino HID Keyboard (simulate input)
    ↓
[keyboard_block_arduino.py] - Keyboard Hook
    ↓
BLOCK (Arduino input không đến game)

Hardware Keyboard (Physical)
    ↓
[keyboard_block_arduino.py] - Keyboard Hook
    ↓
ALLOW (Hardware input pass through)
    ↓
Game (chỉ nhận hardware input)
```

### **Chức Năng:**

1. **Detect Arduino simulate input** (từ Arduino HID)
2. **BLOCK Arduino input** - không cho đến game
3. **ALLOW hardware input** - cho hardware keyboard pass through

### **Khi Nào Dùng:**

✅ **Dùng khi:**

-   Bạn muốn **chỉ dùng hardware keyboard** (không dùng Arduino input)
-   Bạn muốn **block Arduino input** để tránh conflict
-   Bạn muốn game chỉ nhận input từ hardware keyboard thật

❌ **KHÔNG dùng khi:**

-   Bạn đang dùng Arduino input (không cần block)
-   Bạn muốn forward input qua Arduino

### **NGS Detection Risk:**

⚠️ **HIGH RISK** - Script này cũng có **keyboard hook**:

-   NGS có thể detect keyboard hook
-   **PHẢI kill** script này TRƯỚC KHI start game
-   Nếu script đang chạy khi start game → NGS detect → Crash → Ban

### **Cách Dùng:**

```bash
# Chạy script
python keyboard_block_arduino.py [BLOCK_INPUT] [IGNORE_WINDOW_MS] [ENABLE_LOGGING]

# Example:
python keyboard_block_arduino.py true 200 false
```

**Hotkeys:**

-   **PageDown**: Toggle blocking
-   **End**: Exit

---

## 🔍 So Sánh 2 Scripts

| Tính Năng                  | keyboard_to_arduino.py     | keyboard_block_arduino.py     |
| -------------------------- | -------------------------- | ----------------------------- |
| **Mục đích**               | Forward hardware → Arduino | Block Arduino, allow hardware |
| **Keyboard Hook**          | ✅ Có                      | ✅ Có                         |
| **Arduino Connection**     | ✅ Cần (Serial)            | ❌ Không cần                  |
| **Block Arduino Input**    | ❌ Không                   | ✅ Có                         |
| **Block Hardware Input**   | ✅ Có (optional)           | ❌ Không                      |
| **Forward Hardware Input** | ✅ Có                      | ❌ Không                      |
| **NGS Detection Risk**     | ⚠️ HIGH                    | ⚠️ HIGH                       |

---

## 🚨 NGS DETECTION RISK

### **Cả 2 Scripts Đều Có Keyboard Hook:**

**Vấn đề:**

-   NGS **PHÁT HIỆN** keyboard hooks ngay cả khi bot chưa chạy
-   Hooks đang chạy trong background → NGS detect → Crash game → Ban

**Giải pháp:**

1. ✅ **KHÔNG CHẠY** scripts này khi start game
2. ✅ **KILL** scripts TRƯỚC KHI start game
3. ✅ Chỉ start scripts SAU KHI game đã fully loaded

---

## 📋 WORKFLOW AN TOÀN

### **Nếu Bạn Dùng Arduino HID Keyboard:**

#### **Option 1: Dùng keyboard_to_arduino.py (Forward Hardware → Arduino)**

```
1. Kill ALL processes → kill_all_before_game.bat
2. Start game (MapleStory)
3. Wait for game fully loaded
4. Start keyboard_to_arduino.py (SAU KHI game loaded)
5. Start bot (ExplorerSettings.exe)
```

**Lưu ý:**

-   Script phải chạy SAU KHI game loaded
-   Nếu script chạy TRƯỚC game → NGS detect → Crash

#### **Option 2: KHÔNG Dùng Scripts (Chỉ Dùng Arduino)**

```
1. Kill ALL processes → kill_all_before_game.bat
2. Start game (MapleStory)
3. Wait for game fully loaded
4. Start bot (ExplorerSettings.exe) - Bot dùng Arduino trực tiếp
```

**Lưu ý:**

-   Bot có thể dùng Arduino trực tiếp (không cần keyboard_to_arduino.py)
-   Không cần keyboard hook → Không bị NGS detect

---

## 🎯 KHUYẾN NGHỊ

### **Nếu Bạn Chỉ Dùng Bot (Không Dùng Hardware Keyboard):**

✅ **KHÔNG CẦN** chạy 2 scripts này:

-   Bot có thể dùng Arduino trực tiếp
-   Không cần keyboard hook
-   Giảm NGS detection risk

### **Nếu Bạn Muốn Forward Hardware Keyboard → Arduino:**

✅ **CÓ THỂ** dùng `keyboard_to_arduino.py`:

-   Nhưng **PHẢI** kill script TRƯỚC KHI start game
-   Chỉ start script SAU KHI game loaded
-   Vẫn có NGS detection risk

### **Nếu Bạn Muốn Block Arduino Input:**

✅ **CÓ THỂ** dùng `keyboard_block_arduino.py`:

-   Nhưng **PHẢI** kill script TRƯỚC KHI start game
-   Chỉ start script SAU KHI game loaded
-   Vẫn có NGS detection risk

---

## ⚠️ QUAN TRỌNG NHẤT

### **NGUYÊN TẮC VÀNG:**

1. **KHÔNG BAO GIỜ** chạy keyboard hooks TRƯỚC KHI start game
2. **LUÔN** kill tất cả processes TRƯỚC KHI start game
3. **LUÔN** verify không có processes trước khi start game
4. **CHỈ** start scripts SAU KHI game đã fully loaded

### **Workflow Đúng:**

```
1. Kill ALL → kill_all_before_game.bat
2. Verify → check_ngs_processes.bat
3. Start game
4. Wait for game loaded
5. Start scripts (nếu cần)
6. Start bot
```

### **Workflow SAI (SẼ BỊ DETECT):**

```
❌ Start scripts → Start game (SAI!)
❌ Start game → Immediately start scripts (SAI!)
❌ Start game khi có keyboard hooks đang chạy (SAI!)
```

---

## 📝 TÓM TẮT

### **keyboard_to_arduino.py:**

-   **Mục đích:** Forward hardware keyboard → Arduino
-   **Cần:** Arduino connection (Serial)
-   **NGS Risk:** HIGH (keyboard hook)
-   **Dùng khi:** Muốn forward hardware input qua Arduino

### **keyboard_block_arduino.py:**

-   **Mục đích:** Block Arduino input, allow hardware input
-   **Cần:** Không cần Arduino connection
-   **NGS Risk:** HIGH (keyboard hook)
-   **Dùng khi:** Muốn block Arduino input, chỉ dùng hardware keyboard

### **Quan Trọng:**

-   ✅ **Cả 2 scripts** đều có keyboard hook → NGS detection risk
-   ✅ **PHẢI kill** scripts TRƯỚC KHI start game
-   ✅ **CHỈ** start scripts SAU KHI game loaded
-   ✅ **Nếu không cần** → Không chạy scripts (giảm risk)

---

## 🎯 KHUYẾN NGHỊ CHO BẠN

### **Nếu Bạn Chỉ Dùng Bot:**

✅ **KHÔNG CẦN** chạy 2 scripts này:

-   Bot có thể dùng Arduino trực tiếp
-   Không cần keyboard hooks
-   Giảm NGS detection risk đáng kể

### **Workflow Đơn Giản:**

```
1. Kill ALL → kill_all_before_game.bat
2. Start game
3. Wait for game loaded
4. Start bot (ExplorerSettings.exe)
```

**Không cần chạy keyboard_to_arduino.py hoặc keyboard_block_arduino.py!**

---

**REMEMBER:** Keyboard hooks = NGS detection risk. Nếu không cần, không chạy scripts này!
