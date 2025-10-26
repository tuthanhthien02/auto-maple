# 📚 DESYNC FILES INDEX - DANH MỤC TẤT CẢ FILE

## 🎯 Tổng quan

Đây là danh sách đầy đủ tất cả file liên quan đến hệ thống DESYNC, được phân loại theo chức năng.

---

## 📁 1. SCRIPTS - File AHK chính

### 🔥 Dành cho người KHÔNG biết code:

| File                                         | Mô tả                                            | Độ khó    |
| -------------------------------------------- | ------------------------------------------------ | --------- |
| `multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk` | Phiên bản CỰC KỲ DỄ CUSTOM, chọn template có sẵn | ⭐ Rất dễ |

### 🔧 Dành cho người biết code:

| File                                  | Mô tả                                | Độ khó            |
| ------------------------------------- | ------------------------------------ | ----------------- |
| `multiplicity_jitter_WITH_DESYNC.ahk` | Phiên bản gốc, cần chỉnh số thủ công | ⭐⭐⭐ Trung bình |

---

## 🔨 2. COMPILE - File .bat để biên dịch

### ⭐ Cho EASY CUSTOM:

| File                                | Mô tả                                                    | Output                                       |
| ----------------------------------- | -------------------------------------------------------- | -------------------------------------------- |
| `COMPILE_MAC_DINH_NGAY.bat`         | **Compile nhanh với setting mặc định (KHUYẾN NGHỊ!)** ⚡ | `SystemAudioService.exe`                     |
| `compile_EASY_CUSTOM_obfuscate.bat` | Compile + đổi tên giả mạo                                | `SystemAudioService.exe`                     |
| `compile_EASY_CUSTOM.bat`           | Compile đơn giản                                         | `multiplicity_jitter_DESYNC_EASY_CUSTOM.exe` |

### 🔧 Cho bản gốc:

| File                           | Mô tả                                       | Output                                |
| ------------------------------ | ------------------------------------------- | ------------------------------------- |
| `compile_DESYNC.bat`           | Compile đơn giản                            | `multiplicity_jitter_WITH_DESYNC.exe` |
| `compile_DESYNC_obfuscate.bat` | Compile + đổi tên giả mạo **(KHUYẾN NGHỊ)** | `WindowsUpdateService.exe`            |

---

## ⚙️ 3. AUTOSTART - File .bat để tự động khởi động

### ⭐ Cho EASY CUSTOM:

| File                               | Chức năng                              |
| ---------------------------------- | -------------------------------------- |
| `setup_autostart_EASY_CUSTOM.bat`  | Bật tự động chạy khi Windows khởi động |
| `remove_autostart_EASY_CUSTOM.bat` | Tắt tự động chạy                       |

### 🔧 Cho bản gốc:

| File                          | Chức năng                              |
| ----------------------------- | -------------------------------------- |
| `setup_autostart_DESYNC.bat`  | Bật tự động chạy khi Windows khởi động |
| `remove_autostart_DESYNC.bat` | Tắt tự động chạy                       |

---

## 📖 4. DOCUMENTATION - File hướng dẫn

### 🌟 Hướng dẫn chính:

| File                           | Nội dung                                                  | Dành cho              |
| ------------------------------ | --------------------------------------------------------- | --------------------- |
| `CHAY_NGAY_KHONG_CUSTOM.md`    | **Chạy ngay không cần custom - 2 bước (KHUYẾN NGHỊ!)** ⚡ | Người vội             |
| `HUONG_DAN_CUSTOM_DON_GIAN.md` | Hướng dẫn chi tiết cách custom (nếu muốn custom)          | Người không biết code |
| `DESYNC_EASY_CUSTOM_README.md` | Tổng quan về phiên bản EASY CUSTOM                        | Tất cả mọi người      |
| `DESYNC_QUICK_START.md`        | Hướng dẫn nhanh 3 bước                                    | Người biết code       |

### 📚 Hướng dẫn bổ sung:

| File                    | Nội dung                         |
| ----------------------- | -------------------------------- |
| `DESYNC_FILES_INDEX.md` | File này - Danh sách tất cả file |

---

## 🎮 5. WORKFLOW - Quy trình sử dụng

### 🥇 Workflow NHANH NHẤT - Dùng setting mặc định (KHUYẾN NGHỊ! ⚡):

```
1. Compile: COMPILE_MAC_DINH_NGAY.bat
   ↓
2. Test: SystemAudioService.exe (test trên Notepad)
   ↓
3. Setup: setup_autostart_EASY_CUSTOM.bat
   ↓
4. DONE! 🎉
```

**⏱️ Thời gian: 30 giây!**

### 🥈 Workflow có custom - Nếu muốn thay đổi setting:

```
1. Đọc: HUONG_DAN_CUSTOM_DON_GIAN.md
   ↓
2. Sửa: multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk
   ├─ Chọn mức độ training (bỏ ; ở PHẦN 1)
   └─ Chọn template game (bỏ ; ở PHẦN 2)
   ↓
3. Compile: compile_EASY_CUSTOM_obfuscate.bat
   ↓
4. Test: SystemAudioService.exe (test trên Notepad)
   ↓
5. Setup: setup_autostart_EASY_CUSTOM.bat
   ↓
6. DONE! 🎉
```

### 🔧 Workflow cho người biết code:

```
1. Đọc: DESYNC_QUICK_START.md
   ↓
2. Sửa: multiplicity_jitter_WITH_DESYNC.ahk
   ├─ MinDesync := 0
   ├─ MaxDesync := 500
   └─ remap["q"] := "a"
   ↓
3. Compile: compile_DESYNC_obfuscate.bat
   ↓
4. Test: WindowsUpdateService.exe
   ↓
5. Setup: setup_autostart_DESYNC.bat
   ↓
6. DONE! 🎉
```

---

## 🎯 6. QUICK REFERENCE - Tham khảo nhanh

### Tôi muốn...

| Mục đích                                       | File cần dùng                                                          |
| ---------------------------------------------- | ---------------------------------------------------------------------- |
| **Chạy ngay - Không custom (KHUYẾN NGHỊ!)** ⚡ | `COMPILE_MAC_DINH_NGAY.bat` (2 bước, 30 giây)                          |
| **Custom dễ dàng (KHÔNG biết code)**           | `multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk` + compile                 |
| **Custom nâng cao (biết code)**                | `multiplicity_jitter_WITH_DESYNC.ahk` + `compile_DESYNC_obfuscate.bat` |
| **Hướng dẫn nhanh nhất**                       | `CHAY_NGAY_KHONG_CUSTOM.md`                                            |
| **Hướng dẫn custom chi tiết**                  | `HUONG_DAN_CUSTOM_DON_GIAN.md`                                         |
| **Tự động khởi động**                          | `setup_autostart_*.bat`                                                |
| **Tắt tự động khởi động**                      | `remove_autostart_*.bat`                                               |

---

## 📊 7. SO SÁNH - Chọn phiên bản nào?

| Tiêu chí              | EASY CUSTOM           | Bản gốc             |
| --------------------- | --------------------- | ------------------- |
| **Độ khó**            | ⭐ Rất dễ             | ⭐⭐⭐ Trung bình   |
| **Thời gian setup**   | 5 phút                | 15-30 phút          |
| **Chọn mức training** | Bỏ `;` (1 click)      | Nhập số thủ công    |
| **Chọn pause**        | Bỏ `;` (1 click)      | Nhập số thủ công    |
| **Template game**     | 3 mẫu có sẵn          | Tự viết             |
| **Hướng dẫn**         | Chi tiết, tiếng Việt  | Đơn giản, tiếng Anh |
| **Ví dụ**             | Nhiều                 | Ít                  |
| **Dành cho**          | Người không biết code | Người biết code     |
| **Khuyến nghị**       | ⭐⭐⭐⭐⭐            | ⭐⭐⭐              |

### 💡 Khuyến nghị:

-   **Nếu bạn KHÔNG biết code**: Dùng **EASY CUSTOM** ⭐
-   **Nếu bạn biết code và muốn control 100%**: Dùng **bản gốc**

---

## ⚠️ 8. LƯU Ý QUAN TRỌNG

### ✅ Các bước BẮT BUỘC:

1. **Lưu file** sau khi sửa (Ctrl + S)
2. **Compile lại** mỗi lần sửa `.ahk`
3. **Đóng .exe cũ** trước khi chạy .exe mới
4. **Test trên Notepad** trước khi dùng thật

### 🔥 Compile nào tốt nhất?

**→ Dùng `*_obfuscate.bat`** (đổi tên file thành tên giả mạo)

Ví dụ:

-   `compile_EASY_CUSTOM_obfuscate.bat` → `SystemAudioService.exe` ✅
-   `compile_DESYNC_obfuscate.bat` → `WindowsUpdateService.exe` ✅

### 💾 Backup:

-   Nên backup file `.ahk` gốc trước khi sửa
-   Copy file sang USB hoặc cloud

---

## 🚨 9. TROUBLESHOOTING - Xử lý lỗi

### File không tìm thấy?

**Giải pháp:** Đảm bảo tất cả file `.ahk` và `.bat` ở **cùng 1 folder**

### Compile lỗi?

**Giải pháp:**

1. Cài AutoHotkey v1.1 (KHÔNG phải v2)
2. Chạy batch file với quyền Administrator

### Phím không hoạt động?

**Giải pháp:**

1. Kiểm tra đã compile lại chưa
2. Kiểm tra syntax (chữ thường, viết hoa đúng)
3. Đọc `HUONG_DAN_CUSTOM_DON_GIAN.md` phần "CHÚ Ý"

---

## 🎉 10. KẾT LUẬN

### 📦 Tổng cộng có bao nhiêu file?

| Loại                | Số lượng    |
| ------------------- | ----------- |
| Script (.ahk)       | 2 file      |
| Compile (.bat)      | 5 file      |
| Autostart (.bat)    | 4 file      |
| Documentation (.md) | 5 file      |
| **TỔNG**            | **16 file** |

### 🎯 File nào quan trọng nhất?

| Xếp hạng | File                                         | Lý do                                                 |
| -------- | -------------------------------------------- | ----------------------------------------------------- |
| 🥇       | `COMPILE_MAC_DINH_NGAY.bat`                  | Nhanh nhất - 2 bước, 30 giây (có setting mặc định) ⚡ |
| 🥈       | `multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk` | Script chính, có setting mặc định sẵn                 |
| 🥉       | `CHAY_NGAY_KHONG_CUSTOM.md`                  | Hướng dẫn nhanh nhất (2 bước)                         |

### 💪 Bạn cần làm gì?

**Nếu bạn vội - CHỈ 30 GIÂY! ⚡ (KHUYẾN NGHỊ)**

1. 📖 Đọc `CHAY_NGAY_KHONG_CUSTOM.md` (1 phút)
2. 🔨 Chạy `COMPILE_MAC_DINH_NGAY.bat` (30 giây)
3. ✅ XONG! Có setting mặc định tốt rồi!

**Nếu muốn custom setting:**

1. 📖 Đọc `HUONG_DAN_CUSTOM_DON_GIAN.md`
2. ✏️ Sửa `multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk`
3. 🔨 Chạy `compile_EASY_CUSTOM_obfuscate.bat`

**Nếu là pro (biết code):**

1. 📖 Đọc `DESYNC_QUICK_START.md`
2. ✏️ Sửa `multiplicity_jitter_WITH_DESYNC.ahk`
3. 🔨 Chạy `compile_DESYNC_obfuscate.bat`

---

**🎊 CHÚC TRAINING HIỆU QUẢ!**
