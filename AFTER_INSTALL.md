# 🎉 Sau khi cài đặt thành công 8 packages

## ✅ Packages đã cài:

-   ✅ GitPython
-   ✅ keyboard
-   ✅ mss
-   ✅ numpy
-   ✅ opencv-python-headless
-   ✅ Pillow
-   ✅ pygame
-   ✅ pywin32

---

## 🚀 Chạy bot NGAY (Không cần setup thêm)

### **Cách 1: Dùng batch file (Dễ nhất)**

**Double-click:**

```
run_bot_conda.bat
```

### **Cách 2: Qua Anaconda Prompt**

```bash
conda activate automaple
python main.py
```

---

## 📌 Về `setup.py` (TÙY CHỌN - không bắt buộc)

### **❌ Lỗi: `No module named 'win32com'`**

Nếu bạn chạy `python setup.py` và gặp lỗi này:

**Nguyên nhân:**

-   `setup.py` CHỈ dùng để tạo **desktop shortcut**
-   Cần module `win32com` từ `pywin32`
-   Module này chưa được register đúng cách

**Giải pháp:**

#### **Option 1: BỎ QUA (Khuyến nghị)**

`setup.py` **KHÔNG bắt buộc**! Bot vẫn chạy bình thường mà không cần nó.

Thay vì dùng `setup.py`, bạn có thể:

-   ✅ Dùng `run_bot_conda.bat` để chạy bot
-   ✅ Hoặc tự tạo shortcut đơn giản hơn (xem Option 3)

#### **Option 2: Fix pywin32**

**Double-click:**

```
fix_pywin32.bat
```

Sau đó chạy lại:

```bash
python setup.py
```

#### **Option 3: Tạo shortcut đơn giản (Không cần pywin32)**

**Double-click:**

```
create_shortcut_simple.bat
```

Script này sẽ tạo desktop shortcut mà **KHÔNG cần** `win32com`.

---

## 🎯 Checklist hoàn tất:

### **✅ Bước 1: Kiểm tra packages**

```bash
conda activate automaple
python -c "import cv2, numpy, mss, win32api; print('ALL OK!')"
```

Nếu thấy `ALL OK!` → Thành công!

### **✅ Bước 2: Chạy bot**

```bash
conda activate automaple
python main.py
```

Hoặc double-click: `run_bot_conda.bat`

### **✅ Bước 3: Load Luminous command book**

Trong GUI:

1. Click **File** → **Load command book**
2. Chọn: `resources/command_books/luminous.py`
3. Click **Open**

### **✅ Bước 4: Load routine**

1. Click **File** → **Load routine**
2. Chọn routine (ví dụ: `resources/routines/luminous/new_routine.csv`)
3. Click **Open**

### **✅ Bước 5: Test minimap**

-   Mở MapleStory
-   Focus vào game
-   Xem GUI Auto Maple → Tab **Minimap**
-   Nếu thấy minimap hiển thị → ✅ **HOÀN TẤT!**

---

## 🎮 Hotkeys mặc định:

| Phím | Chức năng                             |
| ---- | ------------------------------------- |
| `F4` | Start/Stop bot                        |
| `F5` | Reload routine                        |
| `F7` | Record position (lưu tọa độ hiện tại) |

---

## 📝 Files quan trọng:

### **Chạy bot:**

-   `run_bot_conda.bat` - Chạy bot (dùng file này)
-   `python main.py` - Chạy trực tiếp

### **Cấu hình:**

-   `resources/command_books/luminous.py` - Command book cho Luminous
-   `resources/routines/luminous/` - Các routines

### **Tùy chọn:**

-   `setup.py` - Tạo desktop shortcut (KHÔNG bắt buộc)
-   `create_shortcut_simple.bat` - Tạo shortcut đơn giản

---

## 🆘 Troubleshooting:

### **Lỗi 1: Bot không tìm thấy game**

**Kiểm tra:**

-   MapleStory có đang chạy không?
-   Game title phải là "MapleStory N" hoặc "MapleStory"

### **Lỗi 2: Minimap không hiển thị**

**Kiểm tra:**

-   Focus vào game window
-   Minimap trong game có bật không?
-   Resolution game: 1280x720 hoặc 1366x768

### **Lỗi 3: Character không di chuyển**

**Kiểm tra:**

-   Bot có đang chạy với quyền Administrator không?
-   Hotkey đã đúng chưa? (xem `resources/command_books/luminous.py`)

### **Lỗi 4: Import error khi chạy bot**

```bash
# Test lại packages
conda activate automaple
python -c "import cv2, numpy, mss; print('OK')"
```

Nếu lỗi → Chạy lại `setup_conda.bat`

---

## 💡 Tips:

1. **Chạy bot với Administrator:**

    - Right-click `run_bot_conda.bat`
    - Chọn "Run as Administrator"

2. **Tạo nhiều routines:**

    - Copy file routine cũ
    - Sửa tọa độ theo map mới
    - Save với tên khác

3. **Backup config:**

    ```bash
    # Export conda environment
    conda env export > automaple_backup.yml

    # Restore nếu cần
    conda env create -f automaple_backup.yml
    ```

4. **Debug routine:**
    - Dùng F7 để record positions
    - Check console output để xem tọa độ hiện tại

---

## 🎊 HOÀN TẤT!

Bây giờ bạn có thể:

-   ✅ Chạy bot: `run_bot_conda.bat`
-   ✅ Load command book: Luminous
-   ✅ Load routine: Chọn một trong các routines đã tạo
-   ✅ Press F4 để start/stop bot
-   ✅ Bắt đầu auto training! 🚀

---

**Chúc bạn auto thành công!** 🎮✨
