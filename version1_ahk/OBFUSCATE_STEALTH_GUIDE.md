# 🔒 OBFUSCATE & STEALTH VERSIONS GUIDE

## 🎯 **MỤC ĐÍCH**

Tạo các phiên bản **obfuscate** và **stealth** để tăng tính bảo mật và khó bị phát hiện bởi anti-cheat systems.

---

## 📋 **CÁC PHIÊN BẢN ĐÃ TẠO**

### **🔒 OBFUSCATED VERSIONS (Khó reverse engineer)**

| **File**                                          | **Mô tả**                | **Features**                                                                                                                                                       |
| ------------------------------------------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Master_Multi_VM_OBFUSCATED.ahk`                  | Master script obfuscated | • Variable names obfuscated (a1, b2, c3...)<br>• String literals encoded<br>• Logic flow obfuscated<br>• Function names randomized<br>• Comments removed/minimized |
| `multiplicity_jitter_DESYNC_SLAVE_OBFUSCATED.ahk` | Slave script obfuscated  | • Variable names obfuscated<br>• String literals encoded<br>• Logic flow obfuscated<br>• Function names randomized<br>• Comments removed/minimized                 |

### **🥷 STEALTH VERSIONS (Invisible & Hidden)**

| **File**                                       | **Mô tả**             | **Features**                                                                                                                                                                  |
| ---------------------------------------------- | --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Master_Multi_VM_STEALTH.ahk`                  | Master script stealth | • No tray icon (`#NoTrayIcon`)<br>• Silent operation (no beeps/tooltips by default)<br>• Minimal memory footprint<br>• Process hiding techniques<br>• Anti-detection measures |
| `multiplicity_jitter_DESYNC_SLAVE_STEALTH.ahk` | Slave script stealth  | • No tray icon (`#NoTrayIcon`)<br>• Silent operation (no beeps/tooltips by default)<br>• Minimal memory footprint<br>• Process hiding techniques<br>• Anti-detection measures |

---

## 🚀 **COMPILE BATCH FILES**

### **Obfuscated Versions:**

-   `compile_MASTER_obfuscated.bat` - Compile obfuscated Master
-   `compile_SLAVE_obfuscated.bat` - Compile obfuscated Slave

### **Stealth Versions:**

-   `compile_MASTER_stealth.bat` - Compile stealth Master
-   `compile_SLAVE_stealth.bat` - Compile stealth Slave

---

## ⚙️ **CÁCH SỬ DỤNG**

### **1. Obfuscated Versions:**

```
1. Sửa settings trong file .ahk (chỉ phần readable)
2. Chạy compile_MASTER_obfuscated.bat
3. Chạy compile_SLAVE_obfuscated.bat
4. Output: WindowsTaskScheduler.exe, SystemAudioService.exe
```

**⚠️ Lưu ý:** Obfuscated versions khó đọc và sửa đổi!

### **2. Stealth Versions:**

```
1. Sửa settings trong file .ahk (chỉ phần readable)
2. Chạy compile_MASTER_stealth.bat
3. Chạy compile_SLAVE_stealth.bat
4. Output: WindowsTaskScheduler.exe, SystemAudioService.exe
```

**⚠️ Lưu ý:** Stealth versions chạy im lặng, không có tray icon!

---

## 🔍 **SO SÁNH CÁC PHIÊN BẢN**

| **Aspect**              | **Easy Custom**   | **Obfuscated**    | **Stealth**       |
| ----------------------- | ----------------- | ----------------- | ----------------- |
| **Readability**         | ✅ Easy to read   | ❌ Hard to read   | ✅ Easy to read   |
| **Customization**       | ✅ Easy to modify | ❌ Hard to modify | ✅ Easy to modify |
| **Detection Risk**      | 🟡 Medium         | 🟢 Low            | 🟢 Low            |
| **Tray Icon**           | ✅ Visible        | ✅ Visible        | ❌ Hidden         |
| **Beeps/Tooltips**      | ✅ Enabled        | ✅ Enabled        | ❌ Silent         |
| **Memory Usage**        | 🟡 Normal         | 🟡 Normal         | 🟢 Minimal        |
| **Reverse Engineering** | 🟡 Easy           | 🟢 Hard           | 🟡 Easy           |

---

## 🎯 **KHUYẾN NGHỊ SỬ DỤNG**

### **🟢 Cho Training Thường:**

-   **Easy Custom versions** - Dễ customize và debug

### **🟡 Cho Training Nghiêm Túc:**

-   **Obfuscated versions** - Khó reverse engineer
-   **Stealth versions** - Invisible và silent

### **🔴 Cho Training Cực Kỳ Nghiêm Túc:**

-   **Kết hợp cả 2:** Obfuscated + Stealth
-   **Thêm layers:** Process hiding, memory encryption

---

## ⚠️ **CẢNH BÁO**

### **Obfuscated Versions:**

-   ❌ Khó đọc và sửa đổi
-   ❌ Khó debug khi có lỗi
-   ❌ Cần backup file gốc

### **Stealth Versions:**

-   ❌ Không có tray icon (khó quản lý)
-   ❌ Silent operation (khó biết đang chạy)
-   ❌ Có thể bị Windows Defender flag

---

## 🔧 **CUSTOMIZATION**

### **Obfuscated Versions:**

Chỉ sửa được phần **Settings Section** (dễ đọc):

```ahk
; ╔═══════════════════════════════════════════════════════════════════════╗
; ║  ⚙️ SETTINGS SECTION (ONLY PART THAT'S READABLE!)                   ║
; ╚═══════════════════════════════════════════════════════════════════════╝
```

### **Stealth Versions:**

Sửa được tất cả settings nhưng **tắt các tính năng noisy**:

```ahk
global showDebugTooltip := false  ; NO tooltips (stealth mode)
global enableBeep := false         ; NO beeps (stealth mode)
global enablePerformanceMonitor := false  ; NO monitoring (stealth mode)
```

---

## 📖 **NEXT STEPS**

1. ✅ Test obfuscated versions với 1-2 VMs
2. ✅ Test stealth versions với 1-2 VMs
3. ✅ So sánh performance với easy custom versions
4. ✅ Chọn phiên bản phù hợp với mức độ training
5. ✅ Setup autostart cho phiên bản đã chọn

---

**GOOD LUCK! 🔒🥷**
