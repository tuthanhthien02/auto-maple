# 🔍 Arduino → VMware Detection Risk Analysis

## 📋 Tổng quan Architecture

```
Host Script → TCP → VMware Script → Serial → Arduino → USB HID → Game
```

**Components:**

1. **Host Script** (`host_sender.py`) - TCP Client
2. **VMware Script** (`vmware_receiver.py`) - TCP Server + Serial
3. **Arduino** (USB HID Keyboard) - Hardware device
4. **Game** (MapleStory với NGS)

---

## 🎯 Detection Risk Analysis

### **1. Arduino USB HID Detection** 🎹

#### **Risk Level:** 🟢 LOW-MEDIUM

**What NGS Can Detect:**

-   ✅ **USB Device Descriptor** - VID/PID của Arduino
-   ✅ **USB Device Class** - HID Keyboard class
-   ✅ **USB Device Name** - "Arduino Leonardo" hoặc custom name
-   ✅ **USB Vendor String** - "Arduino LLC" hoặc custom
-   ✅ **USB Product String** - "Arduino Leonardo" hoặc custom
-   ✅ **USB Serial Number** - Unique serial (nếu có)
-   ⚠️ **Keyboard Layout** - KbType (thường không check)
-   ⚠️ **TotalKeys** - Số keys trong HID descriptor (thường không check)

**What NGS CANNOT Detect (easily):**

-   ❌ **Hardware vs Software** - NGS không thể phân biệt Arduino vs keyboard thật
-   ❌ **Input Source** - Không biết input từ đâu (Arduino, keyboard, etc.)
-   ❌ **Serial Communication** - Serial USB không visible từ game process
-   ❌ **TCP Communication** - TCP trên Host không visible từ VM

**Why LOW-MEDIUM Risk:**

-   ✅ Arduino USB HID = **Real Hardware Keyboard**
-   ✅ Windows nhận Arduino như keyboard thật
-   ✅ Game nhận input như từ keyboard thật
-   ⚠️ Nhưng VID/PID có thể bị scan nếu NGS scan USB devices

---

### **2. VMware USB Passthrough Detection** 🔌

#### **Risk Level:** 🟡 MEDIUM

**What NGS Can Detect:**

-   ✅ **VMware USB Passthrough** - USB device được pass-through từ Host
-   ✅ **VMware USB Filters** - USB filters trong VM config
-   ✅ **USB Device Connection** - Device connected/disconnected events
-   ⚠️ **USB Device Timing** - Timing patterns (nhưng khó detect)

**How NGS Might Detect:**

```python
# NGS có thể scan:
1. USB Device Tree (SetupAPI)
2. USB Device Descriptors
3. USB Connection History
4. VMware USB Passthrough registry keys
```

**Why MEDIUM Risk:**

-   ⚠️ NGS có thể scan USB devices
-   ⚠️ VMware USB passthrough có thể để lại traces
-   ⚠️ Nhưng nhiều game không scan USB devices (too invasive)

**Mitigation:**

-   ✅ Use generic USB device name (không có "Arduino" trong name)
-   ✅ Use generic VID/PID (nếu có thể modify)
-   ✅ Đảm bảo Arduino không có "Arduino" trong USB strings

---

### **3. Serial Communication Detection** 📡

#### **Risk Level:** 🟢 LOW

**What NGS Can Detect:**

-   ⚠️ **COM Port** - COM port enumeration (nhưng không biết dùng để làm gì)
-   ⚠️ **Serial Device** - Serial device name (nhưng không biết communication)
-   ❌ **Serial Data** - Không thể đọc serial data từ game process
-   ❌ **Serial Communication** - Serial USB không visible từ game

**Why LOW Risk:**

-   ✅ Serial communication là **local only** (trong VM)
-   ✅ Game process không có quyền đọc serial data
-   ✅ Serial không expose data qua Windows API mà game có thể access
-   ✅ NGS không thể monitor serial communication

**Conclusion:**

-   ✅ Serial communication **AN TOÀN** - NGS không thể detect

---

### **4. TCP Communication Detection** 🌐

#### **Risk Level:** 🟢 LOW

**What NGS Can Detect:**

-   ⚠️ **Network Connections** - TCP connections trên VM
-   ⚠️ **Network Traffic** - TCP packets (nhưng encrypted hoặc không readable)
-   ⚠️ **Outbound Connections** - Outbound TCP connections
-   ❌ **Host Network** - Không thể scan Host network từ VM
-   ❌ **TCP Data** - Không thể đọc TCP data (nếu không có packet inspection)

**Why LOW Risk:**

-   ✅ TCP communication là **network only** (không liên quan đến game)
-   ✅ TCP port có thể randomize (không dùng port phổ biến)
-   ✅ TCP data có thể encrypt (nếu cần)
-   ✅ NGS không thể scan Host network từ VM
-   ✅ Game process không có quyền monitor network connections

**Mitigation:**

-   ✅ Use random port (không dùng well-known ports)
-   ✅ Use local network only (không expose ra internet)
-   ✅ Encrypt TCP data (nếu cần thêm security)

---

### **5. Process Detection** 🔎

#### **Risk Level:** 🟢 LOW

**What NGS Can Detect:**

-   ⚠️ **Python Processes** - `python.exe`, `pythonw.exe`
-   ⚠️ **Script Names** - `host_sender.py`, `vmware_receiver.py` (nếu chạy từ file)
-   ⚠️ **Process Names** - Process names với suspicious keywords
-   ❌ **Host Processes** - Không thể scan Host processes từ VM
-   ❌ **Script Content** - Không thể đọc script content

**Why LOW Risk:**

-   ✅ Scripts chạy trên **Host** (không visible từ VM)
-   ✅ `vmware_receiver.py` có thể rename process name
-   ✅ Scripts có thể compile thành `.exe` để hide
-   ✅ NGS không thể scan Host processes từ VM

**Mitigation:**

-   ✅ Rename scripts: `host_sender.py` → `NetworkService.exe`
-   ✅ Compile scripts thành `.exe` với generic name
-   ✅ Use process hiding (nếu cần)

---

### **6. Timing Pattern Detection** ⏱️

#### **Risk Level:** 🟡 MEDIUM

**What NGS Can Detect:**

-   ⚠️ **Input Timing** - Timing patterns của key presses
-   ⚠️ **Perfect Timing** - Quá perfect timing (không human-like)
-   ⚠️ **Consistent Timing** - Timing quá consistent
-   ⚠️ **Missing Delays** - Thiếu delays giữa các key presses

**Why MEDIUM Risk:**

-   ⚠️ NGS có thể analyze timing patterns
-   ⚠️ Bot input có thể có timing patterns khác với human
-   ⚠️ Nhưng Arduino HID không có timing patterns đặc biệt (như keyboard thật)

**Mitigation:**

-   ✅ Use **human-like delays** trong bot code
-   ✅ Use **random delays** giữa key presses
-   ✅ Use **behavioral anti-detect** (đã có trong code)
-   ✅ Use **variable timing** (không constant)

---

### **7. Input Method Detection** ⌨️

#### **Risk Level:** 🟢 LOW

**What NGS Can Detect:**

-   ⚠️ **SendInput API** - NGS có thể detect SendInput (Windows API)
-   ⚠️ **Keybd_event API** - NGS có thể detect keybd_event
-   ❌ **USB HID** - NGS không thể phân biệt USB HID vs keyboard thật
-   ❌ **Hardware Input** - Hardware input không thể detect

**Why LOW Risk:**

-   ✅ **Arduino USB HID = Hardware Input**
-   ✅ Windows nhận Arduino như keyboard thật
-   ✅ Game nhận input như từ keyboard thật
-   ✅ NGS không thể phân biệt Arduino vs keyboard thật

**Comparison:**

| Input Method          | Detection Risk | Reason                           |
| --------------------- | -------------- | -------------------------------- |
| **SendInput API**     | 🔴 HIGH        | Software simulation, dễ detect   |
| **Keybd_event API**   | 🔴 HIGH        | Software simulation, dễ detect   |
| **USB HID (Arduino)** | 🟢 LOW         | Hardware input, không thể detect |

---

## 📊 Overall Risk Assessment

### **Risk Levels:**

| Component                  | Risk Level    | Detection Method     | Mitigation                    |
| -------------------------- | ------------- | -------------------- | ----------------------------- |
| **Arduino USB HID**        | 🟢 LOW-MEDIUM | USB device scan      | Generic VID/PID, generic name |
| **VMware USB Passthrough** | 🟡 MEDIUM     | USB passthrough scan | Generic device name           |
| **Serial Communication**   | 🟢 LOW        | COM port scan        | Không thể detect data         |
| **TCP Communication**      | 🟢 LOW        | Network scan         | Random port, local only       |
| **Process Detection**      | 🟢 LOW        | Process scan         | Host processes không visible  |
| **Timing Patterns**        | 🟡 MEDIUM     | Timing analysis      | Human-like delays             |
| **Input Method**           | 🟢 LOW        | API detection        | Hardware input = safe         |

---

## 🎯 Detection Risk Summary

### **Overall Risk:** 🟡 **MEDIUM-LOW**

**Why Medium-Low:**

-   ✅ **Arduino USB HID = Hardware Input** - An toàn nhất
-   ✅ **Serial Communication** - Không thể detect
-   ✅ **TCP Communication** - Không thể detect từ VM
-   ✅ **Process Detection** - Host processes không visible
-   ⚠️ **USB Device Scan** - Có thể scan USB devices
-   ⚠️ **Timing Patterns** - Có thể analyze timing

**Key Strengths:**

1. ✅ **Hardware Input** - Arduino = real hardware keyboard
2. ✅ **No Software Simulation** - Không dùng SendInput/keybd_event
3. ✅ **Network Isolation** - TCP trên Host không visible từ VM
4. ✅ **Serial Isolation** - Serial không visible từ game process

**Key Weaknesses:**

1. ⚠️ **USB Device Name** - Có thể có "Arduino" trong name
2. ⚠️ **USB VID/PID** - Arduino có VID/PID đặc biệt
3. ⚠️ **Timing Patterns** - Bot có thể có timing patterns

---

## 🛡️ Mitigation Strategies

### **1. USB Device Obfuscation** (Recommended)

**Goal:** Làm Arduino trông như keyboard thật

**Methods:**

-   ✅ **Change VID/PID** - Modify Arduino firmware để có generic VID/PID
-   ✅ **Change Device Name** - Đổi "Arduino Leonardo" → "Generic USB Keyboard"
-   ✅ **Change Vendor String** - Đổi "Arduino LLC" → "Generic USB Vendor"
-   ✅ **Change Product String** - Đổi "Arduino Leonardo" → "USB Keyboard"

**Difficulty:** ⭐⭐ Medium (cần modify Arduino firmware)

**Effectiveness:** 🟢 High (90%+)

---

### **2. Timing Pattern Obfuscation** (Recommended)

**Goal:** Làm input timing giống human

**Methods:**

-   ✅ **Human-like Delays** - Add random delays giữa key presses
-   ✅ **Variable Timing** - Không dùng constant timing
-   ✅ **Behavioral Anti-detect** - Đã có trong code (anti_detect.py)
-   ✅ **Random Mistakes** - Thỉnh thoảng make mistakes như human

**Difficulty:** ⭐ Easy (đã có trong code)

**Effectiveness:** 🟢 High (80%+)

---

### **3. Process Obfuscation** (Optional)

**Goal:** Hide scripts processes

**Methods:**

-   ✅ **Rename Scripts** - `host_sender.py` → `NetworkService.exe`
-   ✅ **Compile to EXE** - PyInstaller với generic name
-   ✅ **Process Hiding** - Advanced (nếu cần)

**Difficulty:** ⭐ Easy (rename/compile)

**Effectiveness:** 🟡 Medium (60-70%)

---

### **4. Network Obfuscation** (Optional)

**Goal:** Hide TCP communication

**Methods:**

-   ✅ **Random Port** - Không dùng well-known ports
-   ✅ **Local Network Only** - Không expose ra internet
-   ✅ **Encrypt Data** - Encrypt TCP data (nếu cần)

**Difficulty:** ⭐ Easy (config change)

**Effectiveness:** 🟢 High (90%+)

---

## 📋 Detection Checklist

### **What NGS CAN Detect:**

-   [x] USB Device Descriptor (VID/PID, Name)
-   [x] USB Device Class (HID Keyboard)
-   [x] USB Device Vendor/Product Strings
-   [x] VMware USB Passthrough (nếu scan USB)
-   [x] Timing Patterns (nếu analyze)
-   [x] COM Port (nhưng không biết dùng để làm gì)

### **What NGS CANNOT Detect:**

-   [x] Serial Communication Data
-   [x] TCP Communication Data (từ Host)
-   [x] Host Processes
-   [x] Bot Scripts (nếu chạy trên Host)
-   [x] Hardware vs Software Input (Arduino = hardware)
-   [x] Input Source (không biết từ đâu)

---

## ✅ Final Recommendation

### **Overall Risk:** 🟡 **MEDIUM-LOW**

**Recommendation:**

-   ✅ **Arduino USB HID = SAFE** - Hardware input không thể detect
-   ✅ **Serial Communication = SAFE** - Không thể detect data
-   ✅ **TCP Communication = SAFE** - Host network không visible từ VM
-   ⚠️ **USB Device Scan = MEDIUM RISK** - Có thể scan USB devices
-   ⚠️ **Timing Patterns = MEDIUM RISK** - Có thể analyze timing

**Actions:**

1. ✅ **Use Arduino USB HID** - An toàn nhất (hardware input)
2. ✅ **Obfuscate USB Device** - Đổi name, VID/PID (nếu có thể)
3. ✅ **Use Human-like Timing** - Đã có trong code (anti_detect.py)
4. ✅ **Randomize TCP Port** - Không dùng well-known ports
5. ✅ **Rename Scripts** - Generic names (optional)

**Conclusion:**

-   ✅ **Arduino → VMware = RELATIVELY SAFE**
-   ✅ **Risk thấp hơn SendInput/keybd_event** (software simulation)
-   ✅ **Hardware input = không thể detect như software simulation**
-   ⚠️ **Nhưng vẫn có risk từ USB device scan và timing patterns**

---

## 🔍 Comparison với Other Methods

| Input Method          | Detection Risk | Reason                                |
| --------------------- | -------------- | ------------------------------------- |
| **SendInput API**     | 🔴 HIGH        | Software simulation, dễ detect        |
| **Keybd_event API**   | 🔴 HIGH        | Software simulation, dễ detect        |
| **USB HID (Arduino)** | 🟡 MEDIUM-LOW  | Hardware input, nhưng có thể scan USB |
| **Real Keyboard**     | 🟢 LOW         | Hardware input, không có gì đặc biệt  |

**Arduino USB HID = Best option** (sau real keyboard)

---

**Kết luận:** Arduino → VMware có **risk MEDIUM-LOW**, nhưng **an toàn hơn nhiều** so với software simulation (SendInput/keybd_event). Risk chủ yếu từ USB device scan và timing patterns, nhưng có thể mitigate bằng obfuscation.
