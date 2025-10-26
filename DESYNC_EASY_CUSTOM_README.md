# 🎯 DESYNC EASY CUSTOM - PHIÊN BẢN CỰC KỲ DỄ CUSTOM

## 📋 Tổng quan

File `multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk` là phiên bản **ĐẶC BIỆT** được thiết kế cho người **KHÔNG BIẾT CODE**.

### ⭐ Điểm khác biệt so với bản thường:

| Tính năng         | Bản thường     | Bản EASY CUSTOM      |
| ----------------- | -------------- | -------------------- |
| Chọn mức training | Phải nhập số   | Chọn sẵn (bỏ `;`)    |
| Chọn pause        | Phải nhập số   | Chọn sẵn (bỏ `;`)    |
| Remap phím        | Phải viết code | Chọn template có sẵn |
| Hướng dẫn         | Tiếng Anh, ít  | Tiếng Việt, chi tiết |
| Ví dụ             | Không có       | Nhiều ví dụ cụ thể   |
| Template          | 1 mẫu          | 3 mẫu sẵn            |

---

## 🚀 Quick Start (3 bước)

### Bước 1: Chọn mức độ training

Mở file `multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk`, tìm **PHẦN 1**, bỏ dấu `;` ở mức bạn chọn:

```ahk
; ━━━ MỨC TRUNG BÌNH (4-6 giờ/ngày) - Cân bằng (KHUYẾN NGHỊ! ⭐) ━━━
global MinDesync := 0      ← Bỏ ; ở đây
global MaxDesync := 500    ← Bỏ ; ở đây
```

### Bước 2: Chọn template game (hoặc để mặc định)

Tìm **PHẦN 2**, chọn template phù hợp:

-   **Template 1**: MapleStory (Q→A, W→S, E→D, R→F) - **MẶC ĐỊNH**
-   **Template 2**: Không remap (phím giữ nguyên)
-   **Template 3**: Custom (tự sửa)

### Bước 3: Compile

```batch
# Compile + obfuscate (KHUYẾN NGHỊ!)
compile_EASY_CUSTOM_obfuscate.bat

# Compile thường
compile_EASY_CUSTOM.bat
```

**✅ XONG!** Chạy file `.exe` và test thử.

---

## 📁 Các file liên quan

### Scripts:

-   `multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk` - Script chính (dễ custom)
-   `multiplicity_jitter_WITH_DESYNC.ahk` - Script gốc (cho pro)

### Compile:

-   `compile_EASY_CUSTOM.bat` - Compile đơn giản
-   `compile_EASY_CUSTOM_obfuscate.bat` - Compile + đổi tên (KHUYẾN NGHỊ)

### Autostart:

-   `setup_autostart_EASY_CUSTOM.bat` - Tự động chạy khi khởi động
-   `remove_autostart_EASY_CUSTOM.bat` - Hủy tự động chạy

### Documentation:

-   `HUONG_DAN_CUSTOM_DON_GIAN.md` - Hướng dẫn chi tiết (tiếng Việt)
-   `DESYNC_QUICK_START.md` - Hướng dẫn nhanh

---

## 🎚️ Mức độ training có sẵn

| Mức độ     | Thời gian/ngày | MinDesync | MaxDesync | Độ an toàn                      |
| ---------- | -------------- | --------- | --------- | ------------------------------- |
| Nhẹ        | 1-2 giờ        | 0         | 300       | ⭐⭐⭐⭐⭐ An toàn nhất         |
| Trung bình | 4-6 giờ        | 0         | 500       | ⭐⭐⭐⭐ Cân bằng (KHUYẾN NGHỊ) |
| Nặng       | 8-10 giờ       | 100       | 800       | ⭐⭐⭐ Mạo hiểm hơn             |
| Cực nặng   | 12+ giờ        | 200       | 1000      | ⭐⭐ Rất mạo hiểm               |

---

## ⏸️ Mức độ pause có sẵn

| Mức độ             | Tần suất      | Thời lượng   | Độ an toàn                        |
| ------------------ | ------------- | ------------ | --------------------------------- |
| Pause thường xuyên | 2-3 phút      | 1-3 giây     | ⭐⭐⭐⭐⭐ An toàn                |
| Pause vừa phải     | 3-5 phút      | 0.8-2.5 giây | ⭐⭐⭐⭐ Cân bằng (KHUYẾN NGHỊ)   |
| Pause ít           | 5-10 phút     | 0.5-2 giây   | ⭐⭐⭐ Rủi ro cao                 |
| Không pause        | Không bao giờ | -            | ⭐ Rất rủi ro (KHÔNG KHUYẾN NGHỊ) |

---

## 🎮 Template game có sẵn

### Template 1: MapleStory (MẶC ĐỊNH)

```ahk
Q → A
W → S
E → D
R → F
Arrow keys → Giữ nguyên (vẫn có desync+jitter)
Space → Giữ nguyên
```

**Dùng cho:** MapleStory và game MMORPG tương tự

### Template 2: Không remap

```ahk
Tất cả phím → Giữ nguyên
```

**Dùng cho:** Chỉ cần desync + jitter, không cần đổi phím

### Template 3: Custom

```ahk
Tự sửa theo ý bạn
```

**Dùng cho:** Game khác hoặc cần remap đặc biệt

---

## ✏️ Hướng dẫn custom nhanh

### Thêm phím mới:

```ahk
remap["t"] := "g"  ; Ấn T sẽ gửi G
```

### Xóa phím:

```ahk
; remap["q"] := "a"  ; Thêm ; ở đầu
```

### Sửa phím:

```ahk
remap["q"] := "z"  ; Q giờ gửi Z thay vì A
```

**📖 Chi tiết:** Đọc file `HUONG_DAN_CUSTOM_DON_GIAN.md`

---

## ⚠️ Lưu ý quan trọng

### ✅ ĐÚNG:

```ahk
remap["q"] := "a"        ✅ Chữ thường
remap["Left"] := "Left"  ✅ Arrow key viết hoa chữ đầu
remap["Space"] := "Space" ✅ Space viết hoa S
```

### ❌ SAI:

```ahk
remap["Q"] := "A"        ❌ Chữ HOA không hoạt động
remap["left"] := "left"  ❌ Arrow key phải viết hoa chữ đầu
remap["space"] := "space" ❌ Space phải viết hoa S
```

### 💡 Nhớ:

1. **Lưu file** sau khi sửa (Ctrl + S)
2. **Compile lại** mỗi lần sửa
3. **Đóng .exe cũ** trước khi chạy .exe mới
4. **Test trên Notepad** trước khi dùng thật

---

## 🎯 Khuyến nghị setup

### 🥇 Setup tốt nhất (KHUYẾN NGHỊ):

```
Mức độ training: TRUNG BÌNH (4-6 giờ/ngày)
Mức độ pause: VỪA PHẢI (3-5 phút)
Template: MAPLESTORY (mặc định)
Compile: compile_EASY_CUSTOM_obfuscate.bat
```

### 🥈 Setup an toàn (cho người mới):

```
Mức độ training: NHẸ (1-2 giờ/ngày)
Mức độ pause: THƯỜNG XUYÊN (2-3 phút)
Template: MAPLESTORY (mặc định)
Compile: compile_EASY_CUSTOM_obfuscate.bat
```

### 🥉 Setup mạo hiểm (cho người có kinh nghiệm):

```
Mức độ training: NẶNG (8-10 giờ/ngày)
Mức độ pause: ÍT (5-10 phút)
Template: Custom (theo nhu cầu)
Compile: compile_EASY_CUSTOM_obfuscate.bat
```

---

## 🚨 Troubleshooting

### Phím không hoạt động?

1. ✅ Đã lưu file? (Ctrl + S)
2. ✅ Đã compile lại?
3. ✅ Đã đóng .exe cũ?

### Script báo lỗi?

1. ✅ Kiểm tra dấu `;` đúng chưa
2. ✅ Kiểm tra tên phím viết đúng chưa
3. ✅ Đọc thông báo lỗi

### Muốn reset về mặc định?

1. Xóa file `multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk`
2. Copy file `multiplicity_jitter_WITH_DESYNC.ahk`
3. Đổi tên thành `multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk`
4. Sửa lại theo hướng dẫn

---

## 🎉 Kết luận

File `multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk` được thiết kế để:

✅ **KHÔNG cần biết code** - Chỉ cần bỏ dấu `;`  
✅ **3 bước đơn giản** - Chọn, lưu, compile  
✅ **Template sẵn** - MapleStory, Không remap, Custom  
✅ **Hướng dẫn tiếng Việt** - Chi tiết, dễ hiểu  
✅ **Ví dụ cụ thể** - Nhiều tình huống thực tế

**💪 Bạn hoàn toàn có thể tự custom mà không cần hỏi ai!**

---

**📖 Đọc thêm:**

-   `HUONG_DAN_CUSTOM_DON_GIAN.md` - Hướng dẫn chi tiết
-   `DESYNC_QUICK_START.md` - Hướng dẫn nhanh
