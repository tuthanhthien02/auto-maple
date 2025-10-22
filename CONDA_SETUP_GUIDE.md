# 🐍 Hướng dẫn cài đặt Auto Maple với Conda

## 📋 Mục lục

1. [Cài đặt Miniconda](#bước-1-cài-miniconda)
2. [Chạy script tự động](#bước-2-chạy-script-tự-động)
3. [Chạy bot](#bước-3-chạy-bot)
4. [Troubleshooting](#troubleshooting)

---

## ✅ Bước 1: Cài Miniconda

### 1.1. Download Miniconda

**Link download:** https://docs.conda.io/en/latest/miniconda.html

Chọn: **Miniconda3 Windows 64-bit** (Python 3.10)

Hoặc link trực tiếp:

```
https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe
```

### 1.2. Cài đặt

1. **Double-click** file `.exe` vừa tải
2. Click **Next** → **I Agree**
3. Chọn **"Just Me"** → **Next**
4. Chọn thư mục cài đặt (mặc định: `C:\Users\...\miniconda3`) → **Next**
5. ⚠️ **QUAN TRỌNG:** Tick ✅ **"Add Miniconda3 to my PATH environment variable"**
    - Mặc định không tick, nhưng PHẢI tick để script chạy được!
6. Click **Install** (mất ~2-3 phút)
7. Click **Finish**

### 1.3. Kiểm tra cài đặt

Mở **Command Prompt** mới (hoặc **Anaconda Prompt**), gõ:

```bash
conda --version
```

Nếu thấy version hiện ra (ví dụ: `conda 23.7.4`) → ✅ Thành công!

Nếu báo lỗi `conda is not recognized` → Restart máy và thử lại.

---

## ✅ Bước 2: Chạy script tự động

### 2.1. Di chuyển đến thư mục Auto Maple

```bash
cd "C:\Users\Thanh Thien\Desktop\New folder\auto-maple"
```

### 2.2. Chạy script setup

**Double-click** file:

```
setup_conda.bat
```

Hoặc trong Command Prompt:

```bash
setup_conda.bat
```

### 2.3. Đợi script chạy xong

Script sẽ:

-   ✅ Kiểm tra Conda đã cài chưa
-   ✅ Xóa environment cũ (nếu có)
-   ✅ Tạo environment mới `automaple` với Python 3.10
-   ✅ Cài numpy, opencv, pillow từ conda
-   ✅ Cài keyboard, pywin32, pygame, GitPython, mss từ pip
-   ✅ Kiểm tra tất cả packages

**Thời gian:** ~5-10 phút (tùy tốc độ internet)

### 2.4. Kết quả

Nếu thấy:

```
✓✓✓ TAT CA PACKAGES DA DUOC CAI DAT THANH CONG! ✓✓✓
```

→ ✅ **Hoàn tất!** Chuyển sang Bước 3.

---

## ✅ Bước 3: Chạy bot

### Cách 1: Dùng batch file (Dễ nhất)

**Double-click** file:

```
run_bot_conda.bat
```

### Cách 2: Thủ công (Qua Anaconda Prompt)

1. Mở **Anaconda Prompt**
2. Chạy:
    ```bash
    conda activate automaple
    cd "C:\Users\Thanh Thien\Desktop\New folder\auto-maple"
    python main.py
    ```

### Kết quả

Nếu thấy GUI Auto Maple hiện lên → ✅ **THÀNH CÔNG!**

---

## 🔧 Troubleshooting

### ❌ Lỗi 1: `conda is not recognized`

**Nguyên nhân:** Conda chưa được thêm vào PATH

**Giải pháp:**

1. **Cách A:** Dùng **Anaconda Prompt** thay vì Command Prompt
2. **Cách B:** Thêm Conda vào PATH thủ công:
    - Search **"Environment Variables"** trong Windows
    - Edit **Path** → Add:
        ```
        C:\Users\<YourName>\miniconda3
        C:\Users\<YourName>\miniconda3\Scripts
        C:\Users\<YourName>\miniconda3\Library\bin
        ```
    - OK → Restart terminal

---

### ❌ Lỗi 2: `PackagesNotFoundError`

**Nguyên nhân:** Conda channel không có package

**Giải pháp:**

```bash
conda activate automaple
pip install numpy opencv-python-headless Pillow keyboard pywin32 pygame mss GitPython
```

---

### ❌ Lỗi 3: Import error khi chạy bot

**Kiểm tra:**

```bash
conda activate automaple
python -c "import cv2, numpy, mss, win32api; print('OK')"
```

**Nếu lỗi:**

```bash
conda activate automaple
conda install numpy opencv pillow -y
pip install keyboard pywin32 pygame mss GitPython
```

---

### ❌ Lỗi 4: Environment không tồn tại

**Kiểm tra:**

```bash
check_conda_env.bat
```

**Tạo lại:**

```bash
setup_conda.bat
```

---

## 📊 Kiểm tra environment

Chạy file:

```
check_conda_env.bat
```

Sẽ hiển thị:

-   ✅ Conda version
-   ✅ Danh sách environments
-   ✅ Packages đã cài trong `automaple` environment

---

## 🎯 Tóm tắt các files

| File                  | Mô tả                     | Khi nào dùng                     |
| --------------------- | ------------------------- | -------------------------------- |
| `setup_conda.bat`     | Setup environment lần đầu | Chạy 1 lần sau khi cài Miniconda |
| `run_bot_conda.bat`   | Chạy bot                  | Mỗi lần muốn chạy bot            |
| `check_conda_env.bat` | Kiểm tra environment      | Debug khi có lỗi                 |

---

## 💡 Tips

### Mỗi lần chạy bot:

-   **Cách nhanh:** Double-click `run_bot_conda.bat`
-   **Cách thủ công:**
    1. Mở Anaconda Prompt
    2. `conda activate automaple`
    3. `python main.py`

### Cập nhật packages:

```bash
conda activate automaple
conda update --all -y
pip install --upgrade keyboard pywin32 pygame mss GitPython
```

### Xóa environment (nếu muốn cài lại):

```bash
conda env remove -n automaple
setup_conda.bat
```

### Tạo thêm environment cho testing:

```bash
conda create -n automaple-test --clone automaple
conda activate automaple-test
```

---

## 🚀 Lệnh hữu ích

```bash
# Xem danh sách environments
conda env list

# Kích hoạt environment
conda activate automaple

# Thoát environment
conda deactivate

# Xem packages đã cài
conda list
pip list

# Xóa environment
conda env remove -n automaple

# Export environment (để backup)
conda env export > environment.yml

# Import environment (từ backup)
conda env create -f environment.yml
```

---

## 📝 Checklist

### Sau khi cài Miniconda:

-   [ ] `conda --version` hoạt động
-   [ ] Chạy `setup_conda.bat`
-   [ ] Thấy message "TAT CA PACKAGES DA DUOC CAI DAT THANH CONG"
-   [ ] Chạy `run_bot_conda.bat`
-   [ ] GUI Auto Maple hiện lên
-   [ ] Load được command book Luminous
-   [ ] Load được routine
-   [ ] Nhìn thấy minimap

### Nếu tất cả đều ✅ → Hoàn tất! Bắt đầu farming! 🎮

---

## 🆘 Cần trợ giúp?

Nếu vẫn gặp lỗi:

1. Chạy `check_conda_env.bat`
2. Chụp screenshot kết quả
3. Gửi kèm file log (nếu có)

Các thông tin cần thiết:

-   Conda version: `conda --version`
-   Python version: `python --version`
-   OS version: `winver`
-   Lỗi cụ thể (screenshot hoặc error message)
