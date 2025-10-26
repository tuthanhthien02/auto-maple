# 📝 HƯỚNG DẪN CUSTOM ĐỔN GIẢN CHO NGƯỜI KHÔNG BIẾT CODE

## 🎯 Bạn cần custom gì?

File cần sửa: **`multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk`**

---

## 🚀 QUICK START (3 bước đơn giản)

### Bước 1: Mở file

-   Double click file `multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk`
-   Hoặc chuột phải → Edit Script

### Bước 2: Tìm phần cần sửa

Kéo xuống tìm **PHẦN 1** và **PHẦN 2**

### Bước 3: Lưu và compile

-   Lưu file (Ctrl + S)
-   Chạy `compile_DESYNC_obfuscate.bat`

---

## ✏️ PHẦN 1: Chọn mức độ training

### Tìm phần này:

```ahk
; ━━━ MỨC NHẸ (1-2 giờ/ngày) - An toàn nhất ━━━
; global MinDesync := 0
; global MaxDesync := 300

; ━━━ MỨC TRUNG BÌNH (4-6 giờ/ngày) - Cân bằng (KHUYẾN NGHỊ! ⭐) ━━━
global MinDesync := 0
global MaxDesync := 500

; ━━━ MỨC NẶNG (8-10 giờ/ngày) - Mạo hiểm hơn ━━━
; global MinDesync := 100
; global MaxDesync := 800
```

### Cách chọn:

1. **Tìm mức độ bạn muốn** (VD: MỨC NẶNG)
2. **Bỏ dấu `;`** ở đầu **2 dòng** của mức đó
3. **Thêm dấu `;`** vào đầu **2 dòng** của các mức khác

### Ví dụ: Chọn MỨC NẶNG

```ahk
; ━━━ MỨC TRUNG BÌNH (4-6 giờ/ngày) - Cân bằng (KHUYẾN NGHỊ! ⭐) ━━━
; global MinDesync := 0      ← THÊM ; vào đây
; global MaxDesync := 500    ← THÊM ; vào đây

; ━━━ MỨC NẶNG (8-10 giờ/ngày) - Mạo hiểm hơn ━━━
global MinDesync := 100      ← BỎ ; ở đây
global MaxDesync := 800      ← BỎ ; ở đây
```

---

## 🎮 PHẦN 2: Chọn template game

### Tìm phần này:

```ahk
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 📋 TEMPLATE 1: MAPLESTORY - QWER + ARROW KEYS (KHUYẾN NGHỊ! ⭐)
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; Phím skill: Q W E R → A S D F
remap["q"] := "a"
remap["w"] := "s"
remap["e"] := "d"
remap["r"] := "f"
```

### 3 template có sẵn:

#### ✅ Template 1: MapleStory (MẶC ĐỊNH - KHUYẾN NGHỊ)

-   Q → A, W → S, E → D, R → F
-   Arrow keys giữ nguyên (vẫn có desync+jitter)
-   **Dùng cho**: MapleStory và game tương tự

#### ✅ Template 2: Không remap

-   Tất cả phím giữ nguyên
-   **Dùng cho**: Chỉ cần desync + jitter, không cần đổi phím

#### ✅ Template 3: Custom

-   Tự sửa theo ý bạn
-   **Dùng cho**: Game khác hoặc cần remap đặc biệt

---

## 📚 Cách thêm/xóa/sửa phím

### 1️⃣ Thêm phím mới

**Copy dòng này:**

```ahk
remap["PHÍM_NGUỒN"] := "PHÍM_ĐÍCH"
```

**Ví dụ:** Thêm phím T → G

```ahk
remap["t"] := "g"
```

### 2️⃣ Xóa phím

**Thêm `;` vào đầu dòng:**

```ahk
; remap["q"] := "a"  ← Dòng này không còn hoạt động
```

### 3️⃣ Sửa phím

**Thay đổi phím đích:**

```ahk
remap["q"] := "z"  ← Giờ Q sẽ gửi Z thay vì A
```

---

## ⚠️ Những điều QUAN TRỌNG

### ✅ ĐÚNG:

```ahk
remap["q"] := "a"        ✅ Chữ thường
remap["Left"] := "Left"  ✅ Arrow key viết hoa chữ đầu
remap["Space"] := "Space" ✅ Space viết hoa chữ S
```

### ❌ SAI:

```ahk
remap["Q"] := "A"        ❌ Chữ HOA sẽ không hoạt động!
remap["left"] := "left"  ❌ Arrow key phải viết hoa chữ đầu
remap["space"] := "space" ❌ Space phải viết hoa chữ S
```

---

## 🔥 Các phím đặc biệt

| Tên phím      | Cách viết   |
| ------------- | ----------- |
| Mũi tên trái  | `Left`      |
| Mũi tên phải  | `Right`     |
| Mũi tên lên   | `Up`        |
| Mũi tên xuống | `Down`      |
| Khoảng trắng  | `Space`     |
| Enter         | `Enter`     |
| Tab           | `Tab`       |
| Escape        | `Escape`    |
| Backspace     | `Backspace` |
| Shift         | `Shift`     |
| Ctrl          | `Ctrl`      |
| Alt           | `Alt`       |

---

## 💡 Ví dụ cụ thể

### Tình huống 1: Training nhẹ, dùng template mặc định

```ahk
; Chọn MỨC NHẸ
global MinDesync := 0
global MaxDesync := 300

; Dùng TEMPLATE 1 (mặc định)
remap["q"] := "a"
remap["w"] := "s"
remap["e"] := "d"
remap["r"] := "f"
remap["Left"] := "Left"
remap["Right"] := "Right"
remap["Up"] := "Up"
remap["Down"] := "Down"
remap["Space"] := "Space"
```

### Tình huống 2: Training nặng, không remap

```ahk
; Chọn MỨC NẶNG
global MinDesync := 100
global MaxDesync := 800

; Dùng TEMPLATE 2 (không remap)
remap["q"] := "q"
remap["w"] := "w"
remap["e"] := "e"
remap["r"] := "r"
remap["Left"] := "Left"
remap["Right"] := "Right"
remap["Up"] := "Up"
remap["Down"] := "Down"
remap["Space"] := "Space"
```

### Tình huống 3: Custom hoàn toàn

```ahk
; Chọn MỨC TRUNG BÌNH
global MinDesync := 0
global MaxDesync := 500

; Custom phím
remap["q"] := "z"
remap["w"] := "x"
remap["e"] := "c"
remap["r"] := "v"
remap["t"] := "b"  ; Thêm phím T
remap["Left"] := "Left"
remap["Right"] := "Right"
remap["Up"] := "Up"
remap["Down"] := "Down"
```

---

## 🚨 Troubleshooting

### ❓ Sau khi sửa, phím không hoạt động?

**Giải pháp:**

1. Kiểm tra đã **lưu file** chưa (Ctrl + S)
2. **Compile lại** bằng `compile_DESYNC_obfuscate.bat`
3. **Đóng file .exe cũ** trước khi chạy file mới

### ❓ Script báo lỗi khi chạy?

**Giải pháp:**

1. Kiểm tra **dấu `;`** đã đúng chưa
2. Kiểm tra **tên phím** viết đúng chưa (chữ thường cho a-z, chữ hoa cho Left/Right/Space)
3. Kiểm tra **cú pháp** còn nguyên: `remap["..."] := "..."`

### ❓ Muốn reset về mặc định?

**Giải pháp:**

1. Mở lại file `multiplicity_jitter_WITH_DESYNC.ahk` (file gốc)
2. Copy nội dung
3. Paste vào `multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk`
4. Lưu và compile lại

---

## ✅ Checklist sau khi custom

-   [ ] Đã chọn mức độ training (bỏ ; ở 2 dòng MinDesync và MaxDesync)
-   [ ] Đã chọn hoặc custom key remap
-   [ ] Đã lưu file (Ctrl + S)
-   [ ] Đã compile bằng `compile_DESYNC_obfuscate.bat`
-   [ ] Đã test file `.exe` mới compile
-   [ ] Phím hoạt động đúng với delay như mong muốn

---

## 🎉 Xong rồi!

Sau khi custom và compile, bạn có thể:

1. Test file `.exe` trên Notepad trước
2. Nếu OK, chạy `setup_autostart_DESYNC.bat` để tự động khởi động
3. Bắt đầu training!

**💡 Lưu ý:** Compile lại mỗi khi sửa file `.ahk`!
