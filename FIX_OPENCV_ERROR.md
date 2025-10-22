# 🔧 Fix OpenCV Installation Error

## ❌ Lỗi gặp phải:

```
WARNING: Connection timed out while downloading.
ERROR: [WinError 32] The process cannot access the file
because it is being used by another process
```

---

## ✅ Giải pháp (thử theo thứ tự):

### **Cách 1: Script tự động sửa lỗi (Nhanh nhất)**

**Double-click file:**

```
fix_opencv.bat
```

Script sẽ:

-   Xóa pip cache
-   Đợi 5 giây (unlock file)
-   Retry với timeout 300s
-   Test import

---

### **Cách 2: Script cài thủ công (Thử nhiều cách)**

**Double-click file:**

```
install_opencv_manual.bat
```

Script sẽ thử 4 cách:

1. ✅ Cài từ conda (có pre-built binary)
2. ✅ Pip install opencv-python-headless
3. ✅ Pip install opencv-python (full)
4. ✅ Cài version cũ hơn (stable)
5. ✅ Dùng --user flag

---

### **Cách 3: Chạy thủ công (trong Anaconda Prompt)**

```bash
# 1. Kích hoạt environment
conda activate automaple

# 2. Clear pip cache
pip cache purge

# 3. Đợi 10 giây (đóng hết terminal khác)
# (Đợi để file được unlock)

# 4. Thử cài từ conda trước
conda install opencv -y

# 5. Nếu không được, dùng pip
pip install --timeout=300 --retries=5 opencv-python-headless --no-cache-dir

# 6. Test
python -c "import cv2; print(cv2.__version__)"
```

---

### **Cách 4: Download wheel thủ công (Offline install)**

#### Bước 1: Download wheel

Truy cập: https://pypi.org/project/opencv-python-headless/#files

Download file phù hợp:

-   **Python 3.10, Windows 64-bit:**
    ```
    opencv_python_headless-4.8.1.78-cp310-cp310-win_amd64.whl
    ```

#### Bước 2: Copy file .whl vào thư mục bot

```
C:\Users\Thanh Thien\Desktop\New folder\auto-maple\
```

#### Bước 3: Cài từ file local

```bash
conda activate automaple
pip install opencv_python_headless-4.8.1.78-cp310-cp310-win_amd64.whl
```

---

### **Cách 5: Tắt antivirus tạm thời**

1. Tắt Windows Defender hoặc antivirus
2. Chạy lại `fix_opencv.bat`
3. Bật lại antivirus sau khi cài xong

---

### **Cách 6: Chạy với quyền Administrator**

1. **Right-click** `fix_opencv.bat`
2. Chọn **"Run as Administrator"**
3. Đợi script chạy xong

---

## 🔍 Nguyên nhân lỗi:

### **1. File đang được process khác sử dụng**

**Kiểm tra:**

```bash
# Xem pip có đang chạy không
tasklist | find "pip"
tasklist | find "python"
```

**Fix:**

-   Đóng tất cả terminal/command prompt
-   Đợi 10-20 giây
-   Chạy lại

### **2. Connection timeout**

**Kiểm tra internet:**

```bash
ping pypi.org
```

**Fix:**

-   Tăng timeout: `pip install --timeout=300 opencv-python-headless`
-   Dùng mirror: `pip install -i https://pypi.tuna.tsinghua.edu.cn/simple opencv-python-headless`

### **3. Pip cache bị corrupt**

**Fix:**

```bash
pip cache purge
pip install opencv-python-headless --no-cache-dir
```

---

## ✅ Sau khi cài thành công:

```bash
# Test OpenCV
python -c "import cv2; print('OpenCV:', cv2.__version__)"

# Test tất cả packages
python -c "import cv2, numpy, mss, win32api; print('ALL OK!')"
```

---

## 🎯 Checklist troubleshooting:

-   [ ] Đã đóng tất cả terminal/Python processes
-   [ ] Đã đợi 10-20 giây
-   [ ] Đã xóa pip cache (`pip cache purge`)
-   [ ] Đã thử chạy với Administrator
-   [ ] Đã tắt antivirus tạm thời
-   [ ] Đã kiểm tra internet (`ping pypi.org`)
-   [ ] Đã thử cài từ conda (`conda install opencv`)
-   [ ] Đã thử download wheel thủ công

---

## 🆘 Vẫn không được?

### **Option 1: Bỏ qua OpenCV, dùng alternative**

OpenCV chỉ dùng để template matching. Nếu không cài được, có thể:

-   Dùng Pillow + numpy (chậm hơn nhưng vẫn chạy được)
-   Hoặc dùng scikit-image

### **Option 2: Dùng Python khác**

```bash
# Thử Python 3.9 thay vì 3.10
conda create -n automaple39 python=3.9 -y
conda activate automaple39
conda install numpy opencv pillow -y
pip install keyboard pywin32 pygame mss GitPython
```

### **Option 3: Cài Anaconda thay vì Miniconda**

Anaconda đã có sẵn opencv:

-   Download: https://www.anaconda.com/download
-   Cài Anaconda
-   Mở Anaconda Navigator → Environments → Create new
-   Chọn Python 3.10
-   Search "opencv" → Install

---

## 📝 Files hữu ích:

| File                        | Dùng khi                    |
| --------------------------- | --------------------------- |
| `fix_opencv.bat`            | Lỗi lần đầu                 |
| `install_opencv_manual.bat` | `fix_opencv.bat` không được |
| `setup_conda.bat`           | Cài lại toàn bộ             |

---

## 💡 Tips:

1. **Đợi trước khi retry:**

    - Windows cần thời gian unlock file
    - Đợi 10-20 giây giữa mỗi lần thử

2. **Check Task Manager:**

    - Xem có process `pip.exe` hoặc `python.exe` đang chạy không
    - End task nếu có process bị treo

3. **Clear %TEMP%:**

    - Pip download vào `%TEMP%`
    - Nếu đầy, pip sẽ lỗi
    - Xóa files trong `C:\Users\...\AppData\Local\Temp\pip-*`

4. **Dùng conda thay vì pip:**
    - Conda có pre-built binaries
    - Ít lỗi hơn pip
    - `conda install opencv` thường ổn định hơn
