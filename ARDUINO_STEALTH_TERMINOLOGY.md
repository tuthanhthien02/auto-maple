# 📚 Arduino Pro Micro - Thuật Ngữ Stealth/Anti-Detect

## 🎯 **TỔNG QUAN**

Document này tổng hợp các thuật ngữ liên quan đến **Arduino Pro Micro** và **stealth/anti-detect** để bạn dễ tìm hiểu và nghiên cứu.

---

## 🔌 **HARDWARE TERMS**

### **1. Arduino Pro Micro**

-   **Định nghĩa:** Microcontroller board dựa trên ATmega32U4
-   **Đặc điểm:** Có USB HID (Human Interface Device) capability
-   **Stealth relevance:** Có thể giả lập USB keyboard thật
-   **Tìm kiếm:** `Arduino Pro Micro`, `ATmega32U4`, `USB HID`

### **2. Arduino Leonardo**

-   **Định nghĩa:** Arduino board với USB HID capability (tương tự Pro Micro)
-   **Đặc điểm:** Có thể giả lập keyboard, mouse
-   **Stealth relevance:** Alternative to Pro Micro
-   **Tìm kiếm:** `Arduino Leonardo`, `USB HID Leonardo`

### **3. HID (Human Interface Device)**

-   **Định nghĩa:** USB device class cho input devices (keyboard, mouse, joystick)
-   **Đặc điểm:** Windows nhận như hardware input device thật
-   **Stealth relevance:** Input từ HID được coi như hardware input → Khó detect hơn software API
-   **Tìm kiếm:** `USB HID`, `HID device`, `Human Interface Device`

### **4. USB (Universal Serial Bus)**

-   **Định nghĩa:** Standard interface để connect devices
-   **Stealth relevance:** Hardware USB devices có VID/PID → Khó detect hơn virtual devices
-   **Tìm kiếm:** `USB device`, `USB interface`, `USB protocol`

### **5. VID/PID (Vendor ID / Product ID)**

-   **Định nghĩa:** Unique identifiers cho USB devices
-   **VID:** Vendor ID (nhà sản xuất) - Ví dụ: `0x2341` (Arduino LLC)
-   **PID:** Product ID (sản phẩm) - Ví dụ: `0x0036` (Leonardo)
-   **Stealth relevance:** NGS có thể detect Arduino qua VID/PID → Cần change/spoof
-   **Tìm kiếm:** `USB VID PID`, `Vendor ID Product ID`, `Device identifier`

### **6. Serial Communication**

-   **Định nghĩa:** Communication protocol giữa PC và Arduino
-   **Protocol:** UART (Universal Asynchronous Receiver-Transmitter)
-   **Stealth relevance:** NGS có thể detect serial communication patterns
-   **Tìm kiếm:** `Serial communication`, `UART`, `COM port`, `Serial port`

### **7. COM Port**

-   **Định nghĩa:** Serial port trên Windows (COM1, COM2, COM3, ...)
-   **Stealth relevance:** NGS có thể monitor COM port activity
-   **Tìm kiếm:** `COM port`, `Serial port`, `Device Manager COM`

### **8. Baud Rate**

-   **Định nghĩa:** Speed của serial communication (bits per second)
-   **Common values:** 9600, 115200, 921600
-   **Stealth relevance:** Higher baud rate = faster communication = less detection risk
-   **Tìm kiếm:** `Baud rate`, `Serial speed`, `Communication speed`

---

## ⌨️ **KEYBOARD TERMS**

### **9. Hardware Keyboard**

-   **Định nghĩa:** Physical keyboard (keyboard vật lý)
-   **Stealth relevance:** Input từ hardware keyboard → NGS không detect như automation
-   **Tìm kiếm:** `Hardware keyboard`, `Physical keyboard`, `Real keyboard`

### **10. Virtual Keyboard**

-   **Định nghĩa:** Software-emulated keyboard (SendInput API, etc.)
-   **Stealth relevance:** NGS dễ detect virtual keyboard → HIGH RISK
-   **Tìm kiếm:** `Virtual keyboard`, `Software keyboard`, `Emulated keyboard`

### **11. HID Keyboard**

-   **Định nghĩa:** Keyboard device qua USB HID protocol
-   **Stealth relevance:** Hardware HID keyboard → Khó detect hơn virtual keyboard
-   **Tìm kiếm:** `HID keyboard`, `USB HID keyboard`, `HID keyboard device`

### **12. Keyboard Hook**

-   **Định nghĩa:** Low-level interception của keyboard input
-   **Windows API:** `SetWindowsHookEx(WH_KEYBOARD_LL, ...)`
-   **Stealth relevance:** NGS có thể detect keyboard hooks → HIGH RISK
-   **Tìm kiếm:** `Keyboard hook`, `Low-level hook`, `WH_KEYBOARD_LL`, `SetWindowsHookEx`

### **13. Scancode**

-   **Định nghĩa:** Physical key code (hardware-dependent)
-   **Stealth relevance:** Scancode mapping có thể bị detect
-   **Tìm kiếm:** `Scancode`, `Key scancode`, `Scancode map`

### **14. Keycode / Virtual Key Code (VK)**

-   **Định nghĩa:** Logical key code (OS-dependent)
-   **Windows:** VK codes (VK_A, VK_B, etc.)
-   **Stealth relevance:** Keycode patterns có thể bị detect
-   **Tìm kiếm:** `Keycode`, `Virtual key code`, `VK code`, `Windows keycode`

### **15. HID Keycode**

-   **Định nghĩa:** Key code trong HID protocol
-   **Arduino:** `Keyboard.press(KEY_A)`, `Keyboard.release(KEY_A)`
-   **Stealth relevance:** HID keycodes từ hardware → Khó detect
-   **Tìm kiếm:** `HID keycode`, `USB HID keycode`, `Keyboard library`

---

## 🔍 **DETECTION TERMS**

### **16. Device Name Detection**

-   **Định nghĩa:** NGS detect devices qua device name
-   **Ví dụ:** Device name chứa "Arduino" → Detect
-   **Stealth relevance:** HIGH RISK - Cần change device name
-   **Tìm kiếm:** `Device name detection`, `GetRawInputDeviceInfo`, `Device enumeration`

### **17. VID/PID Detection**

-   **Định nghĩa:** NGS detect devices qua VID/PID
-   **Ví dụ:** VID_2341 (Arduino) → Detect
-   **Stealth relevance:** MEDIUM RISK - Cần change/spoof VID/PID
-   **Tìm kiếm:** `VID PID detection`, `Device identifier detection`, `USB device detection`

### **18. GetRawInputDeviceInfo**

-   **Định nghĩa:** Windows API để get device information
-   **Stealth relevance:** NGS có thể dùng API này để detect devices
-   **Tìm kiếm:** `GetRawInputDeviceInfo`, `Raw Input API`, `Device enumeration API`

### **19. Raw Input**

-   **Định nghĩa:** Low-level input API trên Windows
-   **Stealth relevance:** NGS có thể monitor Raw Input để detect devices
-   **Tìm kiếm:** `Raw Input`, `WM_INPUT`, `RegisterRawInputDevices`

### **20. Device Enumeration**

-   **Định nghĩa:** Process of listing/discovering devices
-   **Stealth relevance:** NGS có thể enumerate devices để detect automation tools
-   **Tìm kiếm:** `Device enumeration`, `Enumerate devices`, `List USB devices`

### **21. Device Fingerprinting**

-   **Định nghĩa:** Creating unique identifier cho device
-   **Stealth relevance:** NGS có thể fingerprint devices để detect automation
-   **Tìm kiếm:** `Device fingerprinting`, `Hardware fingerprint`, `Device signature`

### **22. Automation Detection**

-   **Định nghĩa:** Process of detecting automation tools/bots
-   **Stealth relevance:** NGS detect automation → Ban
-   **Tìm kiếm:** `Automation detection`, `Bot detection`, `Anti-cheat detection`

### **23. Input Pattern Detection**

-   **Định nghĩa:** Detect automation qua input patterns
-   **Stealth relevance:** NGS analyze input patterns → Detect automation
-   **Tìm kiếm:** `Input pattern detection`, `Behavioral analysis`, `Pattern matching`

### **24. Timing Pattern Detection**

-   **Định nghĩa:** Detect automation qua timing patterns
-   **Stealth relevance:** NGS analyze timing → Detect automation
-   **Tìm kiếm:** `Timing pattern detection`, `Timing analysis`, `Automation timing`

---

## 🛡️ **STEALTH TERMS**

### **25. Device Spoofing**

-   **Định nghĩa:** Fake device identity (name, VID/PID)
-   **Stealth relevance:** Spoof device name/VID/PID → Giảm detection risk
-   **Tìm kiếm:** `Device spoofing`, `Device impersonation`, `Device cloning`

### **26. VID/PID Spoofing**

-   **Định nghĩa:** Change VID/PID để giả lập device khác
-   **Stealth relevance:** Change Arduino VID/PID → Giảm detection risk
-   **Tìm kiếm:** `VID PID spoofing`, `USB ID spoofing`, `Device ID spoofing`

### **27. Device Name Spoofing**

-   **Định nghĩa:** Change device name để giả lập device khác
-   **Stealth relevance:** Change "Arduino" → "USB Keyboard" → Giảm detection risk
-   **Tìm kiếm:** `Device name spoofing`, `USB device name change`, `Device renaming`

### **28. Hardware Input Bypass**

-   **Định nghĩa:** Use hardware input để bypass software detection
-   **Stealth relevance:** Hardware input → Khó detect hơn software API
-   **Tìm kiếm:** `Hardware input bypass`, `Hardware keyboard bypass`, `HID bypass`

### **29. USB Passthrough**

-   **Định nghĩa:** Pass physical USB device vào VM
-   **Stealth relevance:** Physical device trong VM → Khó detect
-   **Tìm kiếm:** `USB passthrough`, `VM USB passthrough`, `USB device passthrough`

### **30. Generic Device**

-   **Định nghĩa:** Generic/non-branded device
-   **Stealth relevance:** Generic device → Không có automation signatures
-   **Tìm kiếm:** `Generic device`, `Generic keyboard`, `Unbranded device`

---

## 📡 **COMMUNICATION TERMS**

### **31. Serial Protocol**

-   **Định nghĩa:** Communication protocol giữa PC và Arduino
-   **Format:** `"down:a\n"`, `"up:a\n"`
-   **Stealth relevance:** Protocol patterns có thể bị detect
-   **Tìm kiếm:** `Serial protocol`, `Communication protocol`, `Arduino communication`

### **32. Command Protocol**

-   **Định nghĩa:** Format của commands gửi đến Arduino
-   **Format:** `action:key` (ví dụ: `down:a`, `up:a`)
-   **Stealth relevance:** Protocol có thể bị detect
-   **Tìm kiếm:** `Command protocol`, `Arduino commands`, `Serial commands`

### **33. Serial Buffer**

-   **Định nghĩa:** Buffer để store serial data
-   **Stealth relevance:** Buffer overflow có thể gây issues
-   **Tìm kiếm:** `Serial buffer`, `Buffer management`, `Serial data buffer`

### **34. Watchdog Timer**

-   **Định nghĩa:** Timer để detect stuck keys
-   **Stealth relevance:** Prevent keys getting stuck → Giảm detection risk
-   **Tìm kiếm:** `Watchdog timer`, `Stuck key detection`, `Auto-release`

---

## ⏱️ **TIMING TERMS**

### **35. Timing Randomization**

-   **Định nghĩa:** Randomize timing để giống human behavior
-   **Stealth relevance:** Human-like timing → Giảm detection risk
-   **Tìm kiếm:** `Timing randomization`, `Human-like timing`, `Random delays`

### **36. Human-like Timing**

-   **Định nghĩa:** Timing patterns giống human input
-   **Stealth relevance:** Human timing → Khó detect automation
-   **Tìm kiếm:** `Human-like timing`, `Natural timing`, `Human behavior simulation`

### **37. Automation Timing**

-   **Định nghĩa:** Timing patterns của automation tools
-   **Stealth relevance:** Automation timing → Dễ detect
-   **Tìm kiếm:** `Automation timing`, `Bot timing`, `Pattern timing`

### **38. Gaussian Distribution**

-   **Định nghĩa:** Statistical distribution cho random timing
-   **Stealth relevance:** Gaussian distribution → Natural timing variation
-   **Tìm kiếm:** `Gaussian distribution`, `Normal distribution`, `Random timing distribution`

### **39. Micro Pauses**

-   **Định nghĩa:** Small delays giữa key presses
-   **Stealth relevance:** Micro pauses → Human-like behavior
-   **Tìm kiếm:** `Micro pauses`, `Key press delays`, `Inter-key delays`

---

## 🔧 **ARDUINO TERMS**

### **40. Keyboard Library**

-   **Định nghĩa:** Arduino library để giả lập keyboard
-   **Function:** `Keyboard.press()`, `Keyboard.release()`, `Keyboard.begin()`
-   **Stealth relevance:** Library tạo HID keyboard → Hardware input
-   **Tìm kiếm:** `Arduino Keyboard library`, `Keyboard.h`, `HID Keyboard library`

### **41. Key State Tracking**

-   **Định nghĩa:** Track state của keys (pressed/released)
-   **Stealth relevance:** Prevent duplicate presses → Giảm detection risk
-   **Tìm kiếm:** `Key state tracking`, `Key state management`, `Pressed key tracking`

### **42. Key Repeat**

-   **Định nghĩa:** Repeat key press khi key held
-   **Stealth relevance:** Key repeat → Human-like behavior
-   **Tìm kiếm:** `Key repeat`, `Key hold`, `Repeated key presses`

### **43. Stuck Key Prevention**

-   **Định nghĩa:** Prevent keys getting stuck
-   **Stealth relevance:** Stuck keys → Detection risk
-   **Tìm kiếm:** `Stuck key prevention`, `Auto-release keys`, `Key cleanup`

### **44. Firmware**

-   **Định nghĩa:** Software trên Arduino (`.ino` file)
-   **Stealth relevance:** Firmware có thể change device name/VID/PID
-   **Tìm kiếm:** `Arduino firmware`, `.ino file`, `Arduino sketch`

### **45. Bootloader**

-   **Định nghĩa:** Program để upload firmware vào Arduino
-   **Stealth relevance:** Bootloader có thể affect device detection
-   **Tìm kiếm:** `Arduino bootloader`, `Bootloader`, `Firmware upload`

---

## 🎯 **ANTI-DETECT TERMS**

### **46. Process Stealth**

-   **Định nghĩa:** Hide bot process từ detection
-   **Stealth relevance:** Process stealth → Giảm detection risk (nhưng có thể trigger NGS)
-   **Tìm kiếm:** `Process stealth`, `Process hiding`, `Hide process`

### **47. Memory Obfuscation**

-   **Định nghĩa:** Obfuscate memory patterns
-   **Stealth relevance:** Memory obfuscation → Giảm detection risk (nhưng có thể trigger NGS)
-   **Tìm kiếm:** `Memory obfuscation`, `Memory encryption`, `Memory patterns`

### **48. String Encryption**

-   **Định nghĩa:** Encrypt sensitive strings trong code
-   **Stealth relevance:** String encryption → Giảm detection risk
-   **Tìm kiếm:** `String encryption`, `Code obfuscation`, `String obfuscation`

### **49. Import Obfuscation**

-   **Định nghĩa:** Obfuscate imports trong code
-   **Stealth relevance:** Import obfuscation → Giảm detection risk
-   **Tìm kiếm:** `Import obfuscation`, `Dynamic imports`, `Obfuscated imports`

### **50. Pattern Diversification**

-   **Định nghĩa:** Vary input patterns để không bị detect
-   **Stealth relevance:** Pattern diversification → Giảm detection risk
-   **Tìm kiếm:** `Pattern diversification`, `Input variation`, `Behavior variation`

---

## 🔬 **ANALYSIS TERMS**

### **51. Behavioral Analysis**

-   **Định nghĩa:** Analyze behavior để detect automation
-   **Stealth relevance:** NGS dùng behavioral analysis → Detect automation
-   **Tìm kiếm:** `Behavioral analysis`, `Behavior detection`, `Pattern analysis`

### **52. Statistical Analysis**

-   **Định nghĩa:** Analyze statistics để detect automation
-   **Stealth relevance:** NGS dùng statistical analysis → Detect automation
-   **Tìm kiếm:** `Statistical analysis`, `Timing statistics`, `Pattern statistics`

### **53. Signature Detection**

-   **Định nghĩa:** Detect automation qua known signatures
-   **Stealth relevance:** NGS có database của automation signatures
-   **Tìm kiếm:** `Signature detection`, `Pattern matching`, `Signature database`

### **54. Heuristic Detection**

-   **Định nghĩa:** Detect automation qua heuristics (rules)
-   **Stealth relevance:** NGS dùng heuristics → Detect automation
-   **Tìm kiếm:** `Heuristic detection`, `Rule-based detection`, `Heuristics`

---

## 🛠️ **TOOLS TERMS**

### **55. PyInstaller**

-   **Định nghĩa:** Tool để package Python thành executable
-   **Stealth relevance:** Compiled executable → Giảm detection risk
-   **Tìm kiếm:** `PyInstaller`, `Python executable`, `Package Python`

### **56. UPX Packing**

-   **Định nghĩa:** Compress executable để obfuscate
-   **Stealth relevance:** UPX packing → Giảm detection risk
-   **Tìm kiếm:** `UPX packing`, `Executable compression`, `UPX`

### **57. Obfuscation**

-   **Định nghĩa:** Make code harder to understand/analyze
-   **Stealth relevance:** Obfuscation → Giảm detection risk
-   **Tìm kiếm:** `Code obfuscation`, `Obfuscation`, `Code protection`

---

## 📊 **SUMMARY TABLE**

| Category          | Terms                                                                                          | Stealth Relevance                               |
| ----------------- | ---------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| **Hardware**      | HID, USB, VID/PID, Serial, COM Port, Baud Rate                                                 | HIGH - Hardware input khó detect hơn software   |
| **Keyboard**      | Hardware Keyboard, Virtual Keyboard, HID Keyboard, Keyboard Hook, Scancode, Keycode            | HIGH - Hardware keyboard khó detect hơn virtual |
| **Detection**     | Device Name Detection, VID/PID Detection, GetRawInputDeviceInfo, Raw Input, Device Enumeration | HIGH - NGS detect devices qua các methods này   |
| **Stealth**       | Device Spoofing, VID/PID Spoofing, Device Name Spoofing, Hardware Input Bypass                 | HIGH - Spoofing giảm detection risk             |
| **Communication** | Serial Protocol, Command Protocol, Serial Buffer, Watchdog Timer                               | MEDIUM - Protocol patterns có thể bị detect     |
| **Timing**        | Timing Randomization, Human-like Timing, Automation Timing, Gaussian Distribution              | MEDIUM - Human-like timing giảm detection risk  |
| **Arduino**       | Keyboard Library, Key State Tracking, Key Repeat, Firmware, Bootloader                         | MEDIUM - Arduino-specific terms                 |
| **Anti-Detect**   | Process Stealth, Memory Obfuscation, String Encryption, Pattern Diversification                | MEDIUM-HIGH - Anti-detect techniques            |
| **Analysis**      | Behavioral Analysis, Statistical Analysis, Signature Detection, Heuristic Detection            | HIGH - NGS dùng các methods này để detect       |
| **Tools**         | PyInstaller, UPX Packing, Obfuscation                                                          | LOW-MEDIUM - Tools để giảm detection risk       |

---

## 🔍 **SEARCH KEYWORDS**

### **Hardware Input:**

-   `USB HID keyboard`
-   `Hardware keyboard input`
-   `Physical keyboard device`
-   `HID device enumeration`

### **Arduino Stealth:**

-   `Arduino Pro Micro stealth`
-   `Arduino HID keyboard anti-detect`
-   `Arduino device spoofing`
-   `Change Arduino VID PID`
-   `Change Arduino device name`

### **Anti-Detection:**

-   `Hardware input bypass`
-   `USB device detection bypass`
-   `Raw Input API detection`
-   `Device enumeration bypass`

### **Detection Methods:**

-   `GetRawInputDeviceInfo`
-   `Device name detection`
-   `VID PID detection`
-   `Automation device detection`

### **Communication:**

-   `Serial communication patterns`
-   `Arduino serial protocol`
-   `COM port monitoring`
-   `Serial buffer management`

### **Timing:**

-   `Human-like keyboard timing`
-   `Timing randomization`
-   `Automation timing detection`
-   `Gaussian distribution timing`

---

## 📚 **RESOURCES**

### **Arduino Documentation:**

-   Arduino Keyboard Library: `https://www.arduino.cc/reference/en/language/functions/usb/keyboard/`
-   Arduino Pro Micro: `https://www.sparkfun.com/products/12640`

### **Windows APIs:**

-   GetRawInputDeviceInfo: `https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getrawinputdeviceinfoa`
-   Raw Input: `https://docs.microsoft.com/en-us/windows/win32/inputdev/raw-input`

### **USB HID:**

-   USB HID Specification: `https://www.usb.org/hid`
-   HID Usage Tables: `https://www.usb.org/hid`

---

## 🎯 **KHUYẾN NGHỊ**

### **Để Tìm Hiểu Thêm:**

1. ✅ **Hardware Input:** Search `USB HID keyboard`, `Hardware keyboard input`
2. ✅ **Arduino Stealth:** Search `Arduino device spoofing`, `Change Arduino VID PID`
3. ✅ **Anti-Detection:** Search `Hardware input bypass`, `USB device detection bypass`
4. ✅ **Detection Methods:** Search `GetRawInputDeviceInfo`, `Device enumeration`
5. ✅ **Timing:** Search `Human-like keyboard timing`, `Timing randomization`

---

**REMEMBER:** Hardware input (HID keyboard) khó detect hơn software API (SendInput)! ⭐
