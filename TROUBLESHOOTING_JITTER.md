# 🔧 TROUBLESHOOTING - JITTER KHÔNG HOẠT ĐỘNG

## ❌ **VẤN ĐỀ**

```
Test script trong Notepad → KHÔNG CÓ DELAY
```

---

## 🔍 **NGUYÊN NHÂN CÓ THỂ**

### **1. Script không chạy**

```
Script chạy nhưng không có icon trong system tray
→ Script crashed hoặc không start được
```

### **2. Script không intercept được keys**

```
Script chạy (có icon) nhưng không bắt được key Q
→ AutoHotkey version issue (v1 vs v2)
→ Có script khác đang chạy
```

### **3. Script intercept được nhưng không có delay**

```
Script bắt được Q nhưng timing sai
→ Logic error trong code
```

---

## 🧪 **DEBUGGING - TỪNG BƯỚC**

### **STEP 1: Kiểm tra AutoHotkey version**

```bash
1. Open Command Prompt
2. Run: autohotkey --version

KẾT QUẢ:
- "1.1.x.x" → Đúng! ✅
- "2.x.x" → SAI! Script viết cho v1 ❌
- Command not found → AHK chưa cài hoặc không trong PATH
```

**NẾU DÙNG v2:** Cần uninstall v2 và cài v1.1 thay thế!

---

### **STEP 2: Test script CỰC ĐƠN GIẢN**

```bash
1. ĐÓNG TẤT CẢ script AHK đang chạy
   (Right-click icon trong system tray → Exit tất cả)

2. Double-click: DEBUG_SIMPLE.ahk

3. Popup xuất hiện: "Script is running!"
   → Click OK

4. Bấm Q (anywhere, không cần Notepad)

5. KẾT QUẢ:
   ✅ Popup "Q WAS PRESSED!" → Script INTERCEPT được!
   ❌ Không có popup → Script KHÔNG intercept được!
```

**NẾU KHÔNG INTERCEPT ĐƯỢC:**

```
→ AutoHotkey version issue
→ Hoặc có software khác đang block AHK
```

---

### **STEP 3: Test với Tooltip (không blocking)**

```bash
1. Exit DEBUG_SIMPLE.ahk (press ESC)

2. Double-click: DEBUG_KEY_TEST.ahk

3. Bấm Q nhiều lần

4. KẾT QUẢ:
   ✅ Thấy tooltip "Q DETECTED! (Count: 1, 2, 3...)"
      → Script hoạt động!

   ❌ Không thấy tooltip
      → Script không intercept được
```

---

### **STEP 4: Test delay (nếu Step 2-3 OK)**

```bash
1. Exit tất cả scripts

2. Double-click: TEST_JITTER_NOW.ahk

3. Mở Notepad

4. Đảm bảo Notepad có FOCUS (click vào Notepad)

5. Bấm Q chậm chậm, mỗi lần cách nhau 2 giây

6. KẾT QUẢ:
   ✅ Q xuất hiện với delay 0.5-1 giây
      → Delay hoạt động!

   ❌ Q xuất hiện ngay lập tức
      → Delay không hoạt động!
```

---

## 🔧 **FIXES**

### **Fix 1: Đang dùng AutoHotkey v2**

```bash
1. Uninstall AutoHotkey v2:
   Settings → Apps → AutoHotkey → Uninstall

2. Download AutoHotkey v1.1:
   https://www.autohotkey.com/download/ahk-install.exe

3. Install v1.1 (KHÔNG phải v2!)

4. Test lại với DEBUG_SIMPLE.ahk
```

---

### **Fix 2: Script không chạy được**

**Check system tray:**

```
Có icon "H" màu xanh lá? ✅
Không có icon? ❌

Nếu không có:
1. Right-click .ahk file → Run as Administrator
2. Check Windows Defender không block
3. Check antivirus không block AutoHotkey
```

---

### **Fix 3: Có nhiều script chạy cùng lúc**

```bash
1. Right-click system tray icons
2. Exit TẤT CẢ AutoHotkey scripts
3. Chỉ chạy 1 script để test
```

---

### **Fix 4: Notepad không có focus**

```bash
1. Run script
2. Click VÀO TRONG Notepad window (để Notepad có focus)
3. Bấm Q (không click chuột nữa)
```

---

## 📊 **DIAGNOSTIC FLOWCHART**

```
Run DEBUG_SIMPLE.ahk
    ↓
Bấm Q
    ↓
Thấy popup "Q WAS PRESSED!"?
    ├─ YES → Script intercept OK!
    │         ↓
    │     Run TEST_JITTER_NOW.ahk
    │         ↓
    │     Bấm Q trong Notepad
    │         ↓
    │     Có delay?
    │         ├─ YES → HOẠT ĐỘNG! ✅
    │         └─ NO  → Logic error (report to me)
    │
    └─ NO  → Script KHÔNG intercept!
              ↓
          Check AutoHotkey version
              ↓
          "1.1.x.x"?
              ├─ YES → Other issue (permissions? antivirus?)
              └─ NO  → UNINSTALL v2, INSTALL v1.1!
```

---

## 🚨 **MOST COMMON ISSUE**

```
90% khả năng: AutoHotkey v2 installed, script written for v1
```

**Triệu chứng:**

```
- Double-click .ahk file → No error, no nothing
- No icon in system tray
- Script seems "dead"
```

**Fix:**

```
Uninstall v2 → Install v1.1 ✅
```

---

## 📝 **REPORT BACK**

**Hãy test các bước trên và cho tôi biết:**

1. **AutoHotkey version của bạn?**

    ```
    Run: autohotkey --version
    Result: ?
    ```

2. **DEBUG_SIMPLE.ahk có intercept Q không?**

    ```
    Bấm Q → Có popup không?
    YES / NO
    ```

3. **System tray có icon "H" màu xanh không?**

    ```
    YES / NO
    ```

4. **TEST_JITTER_NOW.ahk có delay không?**
    ```
    Bấm Q → Có delay 0.5-1 giây không?
    YES / NO
    ```

---

## 🎯 **FILES ĐỂ DEBUG**

```
DEBUG_SIMPLE.ahk        ← Test intercept (simplest)
DEBUG_KEY_TEST.ahk      ← Test intercept (with counter)
TEST_JITTER_NOW.ahk     ← Test delay (0.5-1s)

Test theo thứ tự: 1 → 2 → 3
```

---

**Hãy test DEBUG_SIMPLE.ahk trước và báo lại kết quả!** 🔍✨
