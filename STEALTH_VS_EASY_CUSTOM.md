# 🥷 STEALTH vs EASY CUSTOM - Which Version to Use?

## 📊 Quick Comparison Table

| **Feature**                  | **EASY CUSTOM** 👁️ | **STEALTH** 🥷 |
|------------------------------|-------------------|---------------|
| **Tray Icon**                | ✅ Visible        | ❌ Hidden     |
| **Visibility**               | 👁️ Can see       | 🥷 Invisible  |
| **Exit Method**              | Right-click tray  | `Ctrl+Alt+Q`  |
| **Status Check**             | Click tray icon   | `Ctrl+Alt+S`  |
| **Toggle ON/OFF**            | `Ctrl+Alt+T`      | `Ctrl+Alt+T`  |
| **Startup Confirmation**     | Tray icon appears | Beep + Tooltip (1.5s) |
| **Detection Risk**           | 🟡 Medium         | 🟢 Lower      |
| **User-Friendliness**        | ⭐⭐⭐ Easy        | ⭐⭐ Moderate  |
| **Obfuscated Name**          | `SystemAudioService.exe` | `WindowsSecurityHelper.exe` |

---

## 🎯 Which Version Should You Use?

### ✅ Use **EASY CUSTOM** (`SystemAudioService.exe`) if:

1. **Bạn muốn dễ sử dụng** (có tray icon, dễ tắt/bật)
2. **Bạn mới bắt đầu** (cần xem script có đang chạy không)
3. **Bạn không lo lắng về detection nhiều** (tray icon có thể bị phát hiện)
4. **Bạn muốn nhanh chóng toggle ON/OFF** bằng cách click

**📝 Compilation:**
```batch
compile_EASY_CUSTOM_obfuscate.bat
```

**🔑 Hotkeys:**
- `Ctrl+Alt+T`: Toggle ON/OFF
- Right-click tray icon: Exit

---

### ✅ Use **STEALTH** (`WindowsSecurityHelper.exe`) if:

1. **Bạn muốn anti-detect tối đa** (không có tray icon!)
2. **Bạn training lâu dài** (8-10 giờ+)
3. **Bạn đã quen với hotkeys** (không cần tray icon)
4. **Bạn muốn script chạy ngầm hoàn toàn** (invisible)

**📝 Compilation:**
```batch
compile_STEALTH_obfuscate.bat
```

**🔑 Hotkeys:**
- `Ctrl+Alt+T`: Toggle ON/OFF
- `Ctrl+Alt+S`: Check status (quan trọng!)
- `Ctrl+Alt+Q`: Exit script (quan trọng!)

---

## 🚨 Important Warnings!

### ⚠️ STEALTH VERSION - PHẢI NHỚ HOTKEYS!

**STEALTH không có tray icon**, vậy nên:

1. **PHẢI NHỚ `Ctrl+Alt+Q` để thoát!**
   - Nếu quên → Phải mở Task Manager → End task
   - Tìm process: `WindowsSecurityHelper.exe`

2. **PHẢI NHỚ `Ctrl+Alt+S` để check status!**
   - Nếu không → Không biết script có đang chạy không
   - Tooltip sẽ hiện:
     ```
     === STEALTH SCRIPT STATUS ===
     
     State: ENABLED
     Pause: NOT ACTIVE
     Next pause: 3m 45s
     
     Ctrl+Alt+T = Toggle ON/OFF
     Ctrl+Alt+Q = Exit script
     ```

3. **Startup confirmation chỉ 1.5 giây!**
   - Beep 1 tiếng (800Hz)
   - Tooltip hiện 1.5s rồi tự tắt
   - Sau đó → Invisible hoàn toàn!

---

## 🔧 Settings Are IDENTICAL!

**Cả 2 versions đều có:**

1. ✅ **Desync delay** (0-500ms) - Phá vỡ Multiplicity sync
2. ✅ **Jitter** (30-80ms) - Timing không đều
3. ✅ **Behavioral pause** (3-5 phút pause 1 lần)
4. ✅ **Arrow keys jitter** (có thể bật/tắt)
5. ✅ **Key remap templates** (MapleStory, No remap, Custom)
6. ✅ **Toggle ON/OFF** (`Ctrl+Alt+T`)
7. ✅ **Hold key support** (giữ phím = hold liên tục)

**Chỉ khác:**
- STEALTH: Không tray icon + thêm hotkeys `Ctrl+Alt+S` (status) và `Ctrl+Alt+Q` (exit)
- EASY CUSTOM: Có tray icon + có thể exit bằng right-click

---

## 📋 Setup Instructions

### 🔹 EASY CUSTOM Setup (3 Steps)

1. **Compile:**
   ```batch
   compile_EASY_CUSTOM_obfuscate.bat
   ```
   → Output: `SystemAudioService.exe`

2. **(Optional) Setup autostart:**
   ```batch
   setup_autostart_EASY_CUSTOM.bat
   ```

3. **Done!** Run `SystemAudioService.exe` and check tray icon!

---

### 🔹 STEALTH Setup (3 Steps)

1. **Compile:**
   ```batch
   compile_STEALTH_obfuscate.bat
   ```
   → Output: `WindowsSecurityHelper.exe`

2. **(Optional) Setup autostart:**
   ```batch
   setup_autostart_STEALTH.bat
   ```

3. **Done!** Run `WindowsSecurityHelper.exe`
   - You'll hear a beep + see tooltip for 1.5s
   - Then it goes invisible!
   - Press `Ctrl+Alt+S` to check status

---

## 🎓 Pro Tips

### 💡 TIP 1: Start with EASY CUSTOM

- Dùng **EASY CUSTOM** để làm quen
- Test settings, remap table
- Khi đã quen → Chuyển sang **STEALTH**

### 💡 TIP 2: Test STEALTH hotkeys TRƯỚC KHI training!

- Chạy `WindowsSecurityHelper.exe`
- Test `Ctrl+Alt+S` (status) → Phải hiện tooltip!
- Test `Ctrl+Alt+T` (toggle) → Phải nghe beep!
- Test `Ctrl+Alt+Q` (exit) → Phải nghe beep 2 lần → Script thoát!

### 💡 TIP 3: STEALTH cho serious training

- EASY CUSTOM: 1-4 giờ/ngày (casual)
- STEALTH: 6-10 giờ/ngày (serious)

### 💡 TIP 4: Đổi settings GIỐNG NHAU cho cả 2 versions

- Cả 2 files `.ahk` có cùng settings
- Đổi settings ở 1 file → Copy sang file kia
- Hoặc: Chọn 1 version rồi custom settings trong đó

---

## ❓ FAQ

### Q: Có thể dùng CẢ 2 versions cùng lúc không?

**❌ KHÔNG!** Chỉ chạy 1 version tại 1 thời điểm!

- Nếu chạy cả 2 → Keys sẽ conflict!
- Thoát version cũ trước khi chạy version mới

---

### Q: Làm sao biết STEALTH script có đang chạy không?

**✅ 3 CÁCH:**

1. **Nhấn `Ctrl+Alt+S`**
   - Nếu hiện tooltip → Đang chạy!
   - Nếu không hiện gì → Script chưa chạy

2. **Nhấn `Ctrl+Alt+T`** (toggle)
   - Nghe beep → Đang chạy!
   - Không nghe gì → Script chưa chạy

3. **Mở Task Manager** (`Ctrl+Shift+Esc`)
   - Tìm `WindowsSecurityHelper.exe`
   - Nếu thấy → Đang chạy!

---

### Q: STEALTH có an toàn hơn EASY CUSTOM không?

**✅ CÓ!** STEALTH ít bị detect hơn vì:

1. **Không có tray icon** → Anti-cheat không thấy
2. **Chạy ngầm hoàn toàn** → Không có visual indicator
3. **Obfuscated filename** (`WindowsSecurityHelper.exe`) → Giống Windows service

**Nhưng:**
- STEALTH khó dùng hơn (phải nhớ hotkeys)
- EASY CUSTOM dễ dùng hơn (có tray icon)

**Trade-off:**
- STEALTH: 🔒 An toàn cao, 🎮 Khó dùng
- EASY CUSTOM: 🎮 Dễ dùng, 🔒 An toàn vừa

---

### Q: Tôi quên exit STEALTH script, giờ phải làm sao?

**✅ 2 CÁCH:**

1. **Thử nhấn `Ctrl+Alt+Q`** (exit hotkey)
   - Nếu nghe beep 2 tiếng → Script thoát!

2. **Mở Task Manager:**
   ```
   Ctrl+Shift+Esc
   → Tìm "WindowsSecurityHelper.exe"
   → Right-click → End task
   ```

---

### Q: STEALTH có beep khi toggle/check status, có bị detect không?

**❌ KHÔNG!** Beep chỉ là sound từ speaker, không phải từ game!

- Anti-cheat KHÔNG thể detect beep
- Beep chỉ để bạn biết script đã toggle/check
- Nếu lo lắng → Có thể comment dòng `SoundBeep` trong code

---

## 🎉 Summary

| **Use Case**              | **Recommended Version** |
|---------------------------|------------------------|
| 🆕 First time user        | EASY CUSTOM ⭐         |
| 🎮 Casual training (1-4h) | EASY CUSTOM ⭐         |
| 🏋️ Serious training (6-10h) | STEALTH ⭐           |
| 🔒 Maximum anti-detect    | STEALTH ⭐             |
| 🎯 Easy to use            | EASY CUSTOM ⭐         |
| 🥷 Invisible background   | STEALTH ⭐             |

**💡 Đề xuất:**
1. Start với **EASY CUSTOM** để test
2. Khi đã quen → Chuyển sang **STEALTH** cho serious training

---

## 📁 Files Summary

### EASY CUSTOM Files:
```
multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk   (Source code)
compile_EASY_CUSTOM_obfuscate.bat            (Compile script)
SystemAudioService.exe                       (Compiled output)
setup_autostart_EASY_CUSTOM.bat              (Autostart setup)
remove_autostart_EASY_CUSTOM.bat             (Remove autostart)
```

### STEALTH Files:
```
multiplicity_jitter_DESYNC_STEALTH.ahk       (Source code)
compile_STEALTH_obfuscate.bat                (Compile script)
WindowsSecurityHelper.exe                    (Compiled output)
setup_autostart_STEALTH.bat                  (Autostart setup)
remove_autostart_STEALTH.bat                 (Remove autostart)
```

---

**🎉 ENJOY YOUR TRAINING! 🚀**

