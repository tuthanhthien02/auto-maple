# 🖥️ Hướng dẫn cài đặt Auto Maple trên VM

## ⚠️ Lỗi thường gặp

```
error: subprocess-exited-with-error
WARNING: Failed to activate VS environment
ERROR: unknown compiler(s): [['cl'], ['cl'], ['cc']]
```

**Nguyên nhân:** VM Windows thiếu C++ compiler để build packages.

---

## ✅ Giải pháp 1: Script tự động (Khuyến nghị)

### Trên VM, chạy:

```bash
# Cách 1: Dùng batch file (đơn giản nhất)
install_on_vm.bat

# Cách 2: Dùng Python script
python install_safe.py
```

Script sẽ:

-   ✅ Tự động upgrade pip
-   ✅ Cài từng package riêng lẻ
-   ✅ Tự động retry với version cũ hơn nếu lỗi
-   ✅ Bỏ qua packages lỗi và tiếp tục
-   ✅ Kiểm tra import sau khi cài

---

## ✅ Giải pháp 2: Cài thủ công

### Bước 1: Upgrade pip

```bash
python -m pip install --upgrade pip setuptools wheel
```

### Bước 2: Cài từng package

```bash
# Cài packages dễ trước (pure Python)
python -m pip install GitPython keyboard Pillow pygame

# Cài pywin32
python -m pip install pywin32

# Cài packages khó (có C extension)
python -m pip install numpy --prefer-binary
python -m pip install mss --prefer-binary
python -m pip install opencv-python-headless --prefer-binary
```

### Bước 3: Kiểm tra

```bash
python -c "import cv2, numpy, mss; print('OK')"
```

---

## ✅ Giải pháp 3: Conda (Mạnh nhất)

### Bước 1: Cài Miniconda

Download: https://docs.conda.io/en/latest/miniconda.html

### Bước 2: Tạo environment

```bash
conda create -n automaple python=3.10
conda activate automaple
```

### Bước 3: Cài packages

```bash
# Cài từ conda (có pre-built binaries)
conda install numpy opencv pillow

# Cài phần còn lại từ pip
pip install mss keyboard pywin32 pygame GitPython
```

### Bước 4: Chạy bot

```bash
conda activate automaple
python main.py
```

---

## ✅ Giải pháp 4: Offline install (VM không có internet)

### Trên PC có internet:

```bash
# Download wheels
python download_wheels.py
```

Sẽ tạo thư mục `wheels/` chứa các file `.whl`

### Copy sang VM:

1. Copy thư mục `wheels/` sang VM
2. Copy file `requirements_no_ai.txt` sang VM
3. Trên VM, chạy:

```bash
python -m pip install --no-index --find-links=wheels -r requirements_no_ai.txt
```

---

## ✅ Giải pháp 5: Cài Visual Studio Build Tools (Cuối cùng)

**LƯU Ý:** Cách này tốn ~3GB disk space!

### Bước 1: Download

https://visualstudio.microsoft.com/visual-cpp-build-tools/

### Bước 2: Cài đặt

1. Chọn: **"Desktop development with C++"**
2. Đợi cài (10-15 phút)
3. Restart VM

### Bước 3: Cài packages

```bash
python -m pip install -r requirements_no_ai.txt
```

---

## 🔍 Kiểm tra Python version

```bash
python --version
```

**Yêu cầu:** Python 3.8 - 3.11

**Nếu Python 3.12+:**

-   TensorFlow không hỗ trợ Python 3.12
-   Nhưng chúng ta đã tắt TensorFlow rồi → OK

---

## 📋 Packages cần thiết

### ✅ BẮT BUỘC (Bot không chạy được nếu thiếu):

-   `numpy` - Xử lý array/matrix
-   `opencv-python-headless` - Template matching, minimap
-   `mss` - Screenshot
-   `pywin32` - Windows API (SendInput)
-   `Pillow` - Load ảnh

### ⚠️ TÙY CHỌN (Bot vẫn chạy nếu thiếu):

-   `keyboard` - Hotkeys (F4, F5, F7)
-   `pygame` - Alert sounds (ding, siren)
-   `GitPython` - Auto update (đã tắt)

### ❌ KHÔNG CẦN:

-   `tensorflow` - AI giải rune (đã tắt)

---

## 🎯 Kiểm tra cài đặt thành công

```bash
# Test import
python -c "import cv2; print('OpenCV:', cv2.__version__)"
python -c "import numpy; print('Numpy:', numpy.__version__)"
python -c "import mss; print('MSS: OK')"
python -c "import win32api; print('PyWin32: OK')"

# Chạy bot
python main.py
```

Nếu thấy GUI Auto Maple hiện lên → ✅ THÀNH CÔNG!

---

## 💡 Tips

1. **Nếu chỉ 1-2 packages lỗi:**

    - Bot vẫn có thể chạy (trừ numpy, opencv, mss)
    - Cài những cái cài được, bỏ qua cái lỗi

2. **Nếu VM chậm:**

    - Dùng `requirements_no_ai.txt` thay vì `requirements.txt`
    - Tiết kiệm ~2GB RAM (không có TensorFlow)

3. **Nếu cần chạy nhiều VM:**
    - Cài 1 VM trước
    - Clone VM đó ra → không cần cài lại

---

## 🆘 Vẫn lỗi?

Gửi cho tôi:

1. Lệnh bạn chạy
2. Lỗi cụ thể (screenshot hoặc copy text)
3. Python version (`python --version`)
4. Pip version (`python -m pip --version`)
