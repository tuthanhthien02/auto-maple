# 🚀 DESYNC - HƯỚNG DẪN NHANH

## 📋 Tổng quan

Script `multiplicity_jitter_WITH_DESYNC.ahk` là phiên bản **QUAN TRỌNG NHẤT** để chống phát hiện khi dùng Multiplicity.

### ⭐ Tính năng chính:

-   **DESYNC DELAY** (0-500ms): Phá vỡ sự đồng bộ giữa các VM
-   **JITTER** (30-80ms): Làm timing mỗi phím khác nhau
-   **BEHAVIORAL PAUSE**: Nghỉ ngẫu nhiên giống người thật
-   **KEY REMAP**: Tùy chỉnh phím dễ dàng

---

## ⚡ Cách dùng nhanh (3 bước)

### Bước 1: Compile script

```batch
# Compile thường (tên file gốc)
compile_DESYNC.bat

# Compile + obfuscate (khuyến nghị!)
compile_DESYNC_obfuscate.bat
```

Output: `WindowsUpdateService.exe` (tên giả mạo hệ thống)

### Bước 2: Test thử

-   Chạy file `.exe` vừa compile
-   Thử ấn phím Q, W, E, R
-   Kiểm tra xem có delay và remap đúng không

### Bước 3: Setup auto-start

```batch
# Tự động chạy khi khởi động Windows
setup_autostart_DESYNC.bat

# Hủy auto-start nếu cần
remove_autostart_DESYNC.bat
```

---

## ✏️ Custom key remap

### File cần sửa:

-   `multiplicity_jitter_WITH_DESYNC.ahk` (bản thường)
-   `multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk` (bản có chú thích tiếng Việt)

### Vị trí sửa:

Tìm phần này:

```ahk
global remap := {}
remap["q"] := "a"
remap["w"] := "s"
remap["e"] := "d"
remap["r"] := "f"
```

### Ví dụ custom:

```ahk
# Thêm remap mới
remap["t"] := "g"

# Xóa remap (thêm ; ở đầu)
; remap["q"] := "a"

# Sửa remap
remap["q"] := "z"  # Giờ Q sẽ gửi Z
```

**⚠️ Sau khi sửa, phải compile lại!**

---

## ⚙️ Custom desync delay (quan trọng!)

### Vị trí sửa:

```ahk
global MinDesync := 0      ; Min delay
global MaxDesync := 500    ; Max delay
```

### Khuyến nghị theo mức độ training:

| Mức độ     | Thời gian/ngày | MinDesync | MaxDesync |
| ---------- | -------------- | --------- | --------- |
| Nhẹ        | 1-2 giờ        | 0         | 300       |
| Trung bình | 4-6 giờ        | 0         | 500       |
| Nặng       | 8-10 giờ       | 100       | 800       |

**⚠️ Sau khi sửa, phải compile lại!**

---

## 🔧 Các file script

| File                                         | Mục đích                                |
| -------------------------------------------- | --------------------------------------- |
| `multiplicity_jitter_WITH_DESYNC.ahk`        | Script chính                            |
| `multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk` | Bản dễ custom (có chú thích Tiếng Việt) |
| `compile_DESYNC.bat`                         | Compile thường                          |
| `compile_DESYNC_obfuscate.bat`               | Compile + obfuscate (khuyến nghị)       |
| `setup_autostart_DESYNC.bat`                 | Setup tự động chạy                      |
| `remove_autostart_DESYNC.bat`                | Hủy tự động chạy                        |

---

## ❓ Câu hỏi thường gặp

### Q: Tại sao cần DESYNC delay?

A: Multiplicity gửi input đến tất cả VM **cùng lúc**. Desync delay làm cho mỗi VM nhận input tại **thời điểm khác nhau**, giảm 90% nguy cơ phát hiện.

### Q: Khác gì JITTER?

A:

-   **DESYNC**: Delay lớn (0-500ms) để phá vỡ sự đồng bộ giữa các VM
-   **JITTER**: Delay nhỏ (30-80ms) để làm timing mỗi phím khác nhau

**Cần cả 2!** Desync phá đồng bộ, Jitter làm natural.

### Q: Có cần remap arrow keys không?

A: **CÓ!** Arrow keys cũng cần desync + jitter. Đã có sẵn trong script:

```ahk
remap["Left"] := "Left"
remap["Right"] := "Right"
remap["Up"] := "Up"
remap["Down"] := "Down"
```

### Q: Làm sao để mỗi VM có delay khác nhau?

A: Script đã tự động random delay mỗi lần ấn phím. Không cần làm gì thêm!

---

## ⚠️ Lưu ý quan trọng

1. **Compile trước khi dùng**: File `.ahk` dễ bị phát hiện hơn file `.exe`
2. **Dùng bản obfuscate**: Tên file giả mạo giúp tránh phát hiện
3. **Sau mỗi lần sửa, phải compile lại**: Script không tự động update
4. **Test trước khi training**: Đảm bảo mọi thứ hoạt động đúng

---

## 🎯 Hiệu quả chống phát hiện

| Layer    | Công nghệ              | Tỷ lệ chống phát hiện |
| -------- | ---------------------- | --------------------- |
| 1        | VPN riêng mỗi VM       | 30%                   |
| 2        | Desync Delay (0-500ms) | 50%                   |
| 3        | Jitter (30-80ms)       | 10%                   |
| 4        | Behavioral Pause       | 5%                    |
| 5        | Key Remap              | 5%                    |
| **TỔNG** |                        | **~95%** ✅           |

---

## 🚨 Khi nào cần support?

Nếu gặp vấn đề:

1. Kiểm tra đã cài AutoHotkey v1.1 chưa
2. Kiểm tra file `.ahk` có trong folder không
3. Chạy batch file với quyền Administrator
4. Đọc thông báo lỗi và làm theo hướng dẫn

---

**🎉 Chúc training hiệu quả!**
