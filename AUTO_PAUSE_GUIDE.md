# 📝 AUTO PAUSE ONLY - HƯỚNG DẪN

## 🎯 Tổng quan

Script `auto_pause_only.ahk` là phiên bản **CỰC KỲ ĐƠN GIẢN** - CHỈ CÓ AUTO PAUSE.

### ✅ Có gì?

-   ⏸️ **Auto Pause**: Tự động pause ngẫu nhiên mỗi 3-5 phút

### ❌ Không có gì?

-   ❌ **Không remap**: Phím giữ nguyên
-   ❌ **Không desync**: Không delay để phá đồng bộ
-   ❌ **Không jitter**: Không delay ngẫu nhiên cho mỗi phím

---

## 🎯 Dành cho ai?

### ✅ Phù hợp:

-   ✅ Bạn đã có script remap/jitter riêng
-   ✅ Chỉ cần thêm auto pause
-   ✅ Muốn script siêu đơn giản

### ❌ Không phù hợp:

-   ❌ Cần remap phím
-   ❌ Cần desync để phá đồng bộ Multiplicity
-   ❌ Cần jitter cho mỗi phím

**💡 Nếu cần đầy đủ, dùng:** `multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk`

---

## ⚡ Quick Start (30 giây)

### Bước 1: Compile

```batch
compile_auto_pause_obfuscate.bat
```

**Output:** `WindowsUpdateHelper.exe`

### Bước 2: Test

```
Double click: WindowsUpdateHelper.exe
```

✅ Sẽ thấy tooltip "⏸️ PAUSE" xuất hiện mỗi 3-5 phút

### Bước 3: Setup autostart

```batch
setup_autostart_auto_pause.bat
```

**✅ XONG!**

---

## ⚙️ Setting mặc định

### ⏸️ Pause VỪA PHẢI (KHUYẾN NGHỊ)

-   **Tần suất**: Mỗi 3-5 phút (180-300 giây)
-   **Thời lượng**: 0.8-2.5 giây (800-2500ms)
-   **Tooltip**: Hiển thị "⏸️ PAUSE" khi pause
-   **Phù hợp**: Hầu hết người dùng

---

## ✏️ Custom pause (nếu muốn)

### File cần sửa:

`auto_pause_only.ahk`

### Vị trí sửa:

Tìm phần này (dòng ~50):

```ahk
; ━━━ PAUSE VỪA PHẢI (Cân bằng - KHUYẾN NGHỊ! ⭐) ━━━
global MinPauseInterval := 180000
global MaxPauseInterval := 300000
global MinPauseDuration := 800
global MaxPauseDuration := 2500
```

### Các mức có sẵn:

#### 1. PAUSE THƯỜNG XUYÊN (Pause nhiều hơn)

```ahk
; Bỏ ; ở 4 dòng này:
global MinPauseInterval := 120000  ; 2 phút
global MaxPauseInterval := 180000  ; 3 phút
global MinPauseDuration := 1000
global MaxPauseDuration := 3000
```

#### 2. PAUSE VỪA PHẢI (MẶC ĐỊNH)

```ahk
; Đang dùng mức này:
global MinPauseInterval := 180000  ; 3 phút
global MaxPauseInterval := 300000  ; 5 phút
global MinPauseDuration := 800
global MaxPauseDuration := 2500
```

#### 3. PAUSE ÍT (Pause ít hơn)

```ahk
; Bỏ ; ở 4 dòng này:
global MinPauseInterval := 300000  ; 5 phút
global MaxPauseInterval := 600000  ; 10 phút
global MinPauseDuration := 500
global MaxPauseDuration := 2000
```

#### 4. KHÔNG PAUSE (Không khuyến nghị)

```ahk
; Bỏ ; ở 4 dòng này:
global MinPauseInterval := 999999999
global MaxPauseInterval := 999999999
global MinPauseDuration := 1
global MaxPauseDuration := 1
```

**⚠️ Nhớ:** Sau khi sửa, phải compile lại!

---

## 📁 Các file liên quan

| File                               | Mục đích                          |
| ---------------------------------- | --------------------------------- |
| `auto_pause_only.ahk`              | Script chính - CHỈ có auto pause  |
| `compile_auto_pause.bat`           | Compile đơn giản                  |
| `compile_auto_pause_obfuscate.bat` | Compile + obfuscate (KHUYẾN NGHỊ) |
| `setup_autostart_auto_pause.bat`   | Setup tự động chạy                |
| `remove_autostart_auto_pause.bat`  | Hủy tự động chạy                  |
| `AUTO_PAUSE_GUIDE.md`              | File này - Hướng dẫn              |

---

## 🎯 Cách hoạt động

### 1. Script chạy im lặng ở background

-   Không hiện icon
-   Không làm gì cả

### 2. Mỗi 3-5 phút (ngẫu nhiên)

-   Hiện tooltip "⏸️ PAUSE: XXXms"
-   Pause trong 0.8-2.5 giây (ngẫu nhiên)
-   Ẩn tooltip và tiếp tục

### 3. Lặp lại mãi mãi

-   Tự động tính toán thời gian pause tiếp theo
-   Hoàn toàn ngẫu nhiên

---

## 💡 Kết hợp với script khác

### Ví dụ 1: Dùng với Multiplicity + Script remap riêng

```
1. Chạy: WindowsUpdateHelper.exe (auto pause)
2. Chạy: Your_Remap_Script.exe
3. Multiplicity broadcast input
4. → Script remap xử lý remap
5. → Auto pause tạo pause ngẫu nhiên
```

### Ví dụ 2: Dùng với PowerToys remap

```
1. PowerToys: Q→A, W→S, E→D, R→F
2. Chạy: WindowsUpdateHelper.exe (auto pause)
3. → PowerToys xử lý remap
4. → Auto pause tạo pause ngẫu nhiên
```

---

## ⚠️ Lưu ý

### ✅ Script này CHỈ tạo pause:

-   ✅ Không can thiệp vào phím bấm
-   ✅ Không remap phím
-   ✅ Không thêm delay vào input
-   ✅ Chỉ hiện tooltip khi pause

### ❌ Script này KHÔNG làm:

-   ❌ Không remap phím
-   ❌ Không phá đồng bộ Multiplicity
-   ❌ Không thêm jitter vào phím

---

## ❓ FAQ

### Q: Tại sao chọn script này thay vì DESYNC_EASY_CUSTOM?

**A:** Nếu bạn đã có script remap/jitter riêng, chỉ cần thêm pause đơn giản.

### Q: Có thể dùng cùng lúc với script khác?

**A:** CÓ! Script này độc lập, chỉ tạo pause.

### Q: Làm sao biết script đang chạy?

**A:** Sẽ thấy tooltip "⏸️ PAUSE" xuất hiện mỗi 3-5 phút.

### Q: Có thể tắt tooltip không?

**A:** CÓ. Mở file `.ahk`, xóa dòng `ToolTip, ⏸️ PAUSE: %duration%ms, 0, 0` (dòng 116).

### Q: Nếu muốn pause dài hơn?

**A:** Sửa `MaxPauseDuration` thành số lớn hơn (VD: 5000 = 5 giây).

### Q: Nếu muốn pause thường xuyên hơn?

**A:** Giảm `MinPauseInterval` và `MaxPauseInterval` (VD: 60000 = 1 phút).

---

## 🚀 Workflow đơn giản

```
1. Compile: compile_auto_pause_obfuscate.bat
   ↓
2. Test: WindowsUpdateHelper.exe
   ↓
3. Setup: setup_autostart_auto_pause.bat
   ↓
4. DONE! 🎉
```

**⏱️ Thời gian: 30 giây**

---

## 🎯 So sánh với DESYNC_EASY_CUSTOM

| Tính năng       | auto_pause_only          | DESYNC_EASY_CUSTOM   |
| --------------- | ------------------------ | -------------------- |
| **Remap**       | ❌ KHÔNG                 | ✅ CÓ (Q→A, W→S...)  |
| **Desync**      | ❌ KHÔNG                 | ✅ CÓ (0-500ms)      |
| **Jitter**      | ❌ KHÔNG                 | ✅ CÓ (30-80ms)      |
| **Auto Pause**  | ✅ CÓ                    | ✅ CÓ                |
| **Độ đơn giản** | ⭐⭐⭐⭐⭐ Cực đơn giản  | ⭐⭐⭐ Trung bình    |
| **Dùng khi**    | Đã có script remap riêng | Cần đầy đủ tính năng |

---

## 🎉 Kết luận

Script `auto_pause_only.ahk`:

-   ✅ **Cực kỳ đơn giản** - Chỉ ~120 dòng code
-   ✅ **Chỉ làm 1 việc** - Auto pause
-   ✅ **Độc lập** - Không ảnh hưởng script khác
-   ✅ **Dễ custom** - Chỉ cần sửa 4 số
-   ✅ **Nhẹ** - Gần như không tốn tài nguyên

**💪 Hoàn hảo cho người đã có script remap/jitter riêng!**

---

**📖 Đọc thêm (nếu cần đầy đủ):**

-   `multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk` - Script đầy đủ
-   `CHAY_NGAY_KHONG_CUSTOM.md` - Hướng dẫn script đầy đủ
