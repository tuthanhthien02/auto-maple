# 🔧 Fix Build Error trên VMware - ExplorerSettings.spec Not Found

## 🚨 **LỖI**

```
ERROR: Spec file "ExplorerSettings.spec" not found!
Build failed with code 1
```

---

## 🔍 **NGUYÊN NHÂN**

### **1. File Chưa Được Copy Vào VM** ⚠️ MOST COMMON

**Vấn đề:**

-   Bạn copy code vào VM nhưng quên copy `ExplorerSettings.spec`
-   File spec không có trong VM

**Giải pháp:**

-   Copy `ExplorerSettings.spec` vào VM
-   Hoặc copy toàn bộ project folder vào VM

---

### **2. Script Chạy Từ Sai Directory** ⚠️ COMMON

**Vấn đề:**

-   Script chạy từ folder khác (không phải project root)
-   `ExplorerSettings.spec` không có trong current directory

**Giải pháp:**

-   Đảm bảo chạy script từ project root directory
-   Script tự động change directory (`cd /d "%~dp0"`), nhưng có thể fail nếu path có vấn đề

---

### **3. Path Có Khoảng Trắng** ⚠️ POSSIBLE

**Vấn đề:**

-   Path có khoảng trắng: `C:\Users\Thanh Thien\Desktop\New folder\auto-maple`
-   Một số commands có thể fail với path có khoảng trắng

**Giải pháp:**

-   Script đã dùng quotes (`"%~dp0"`), nhưng có thể cần verify

---

## ✅ **GIẢI PHÁP**

### **Solution 1: Copy File Spec Vào VM** ⭐ RECOMMENDED

**Trên Host:**

1. Copy `ExplorerSettings.spec` vào shared folder hoặc network share
2. Hoặc copy toàn bộ project folder vào VM

**Trên VM:**

1. Copy `ExplorerSettings.spec` vào project folder
2. Verify file tồn tại:
    ```batch
    dir ExplorerSettings.spec
    ```
3. Chạy lại build script

---

### **Solution 2: Verify Current Directory**

**Trên VM:**

1. Mở Command Prompt
2. Navigate đến project folder:
    ```batch
    cd "C:\path\to\auto-maple"
    ```
3. Verify files:
    ```batch
    dir ExplorerSettings.spec
    dir main.py
    dir build_stealth.bat
    ```
4. Nếu files không có → Copy files vào VM

---

### **Solution 3: Build Từ Command Line**

**Nếu spec file không có, có thể build từ main.py:**

```batch
pyinstaller --noconfirm --clean --log-level=INFO ^
  --name "ExplorerSettings" ^
  --windowed ^
  --icon "assets\explorer-icon.ico" ^
  --add-data "assets;assets" ^
  --add-data "resources;resources" ^
  --add-data "src;src" ^
  main.py
```

**Lưu ý:** Build này sẽ không có tất cả options từ spec file.

---

## 🔧 **SCRIPT ĐÃ ĐƯỢC FIX**

Đã cải thiện `build_stealth.bat` để:

1. ✅ **Verify spec file tồn tại** trước khi build
2. ✅ **Verify main.py tồn tại** trước khi build
3. ✅ **Show current directory** để debug
4. ✅ **Show error message rõ ràng** nếu file không tìm thấy

**Script mới sẽ:**

-   Check `ExplorerSettings.spec` exists
-   Check `main.py` exists
-   Show current directory
-   Exit với error message rõ ràng nếu file không tìm thấy

---

## 📋 **CHECKLIST TRƯỚC KHI BUILD TRÊN VM**

### **Before Building:**

-   [ ] **Copy toàn bộ project folder** vào VM
-   [ ] **Verify ExplorerSettings.spec** tồn tại trong project folder
-   [ ] **Verify main.py** tồn tại trong project folder
-   [ ] **Verify build_stealth.bat** tồn tại trong project folder
-   [ ] **Chạy script từ project root directory**

### **Verify Files:**

```batch
REM Trên VM, chạy:
cd "C:\path\to\auto-maple"
dir ExplorerSettings.spec
dir main.py
dir build_stealth.bat
```

**Nếu files không có → Copy files vào VM**

---

## 🚀 **WORKFLOW ĐÚNG**

### **Step 1: Copy Files Vào VM**

**Option 1: Shared Folders**

```
Host: Copy ExplorerSettings.spec vào shared folder
VM: Copy từ shared folder vào project folder
```

**Option 2: Network Share**

```
Host: Share project folder
VM: Copy ExplorerSettings.spec từ network share
```

**Option 3: Copy Toàn Bộ Project**

```
Copy toàn bộ project folder vào VM
→ Đảm bảo tất cả files đều có
```

---

### **Step 2: Verify Files**

```batch
REM Trên VM:
cd "C:\path\to\auto-maple"
dir ExplorerSettings.spec
dir main.py
```

---

### **Step 3: Build**

```batch
build_stealth.bat
```

**Script mới sẽ tự động check files trước khi build!**

---

## ⚠️ **LƯU Ý**

### **1. DEPRECATION WARNING:**

```
DEPRECATION WARNING: Running PyInstaller as admin is not necessary
```

**Giải pháp:**

-   **KHÔNG chạy script as Administrator**
-   Chạy script từ normal user account
-   PyInstaller không cần admin privileges

---

### **2. File Locations:**

**Required Files:**

-   `ExplorerSettings.spec` - PyInstaller spec file
-   `main.py` - Main entry point
-   `build_stealth.bat` - Build script
-   `assets/` - Assets folder
-   `resources/` - Resources folder
-   `src/` - Source code folder

**Tất cả files này phải có trong VM!**

---

## 📝 **QUICK FIX**

### **Nếu chỉ thiếu spec file:**

1. **Copy ExplorerSettings.spec từ Host vào VM**
2. **Verify file tồn tại:**
    ```batch
    dir ExplorerSettings.spec
    ```
3. **Chạy lại build script**

---

## ✅ **VERIFY BUILD SCRIPT**

Script đã được fix để tự động check files. Chạy lại `build_stealth.bat` và script sẽ:

1. ✅ Check `ExplorerSettings.spec` exists
2. ✅ Check `main.py` exists
3. ✅ Show current directory
4. ✅ Show clear error nếu file không tìm thấy

---

**REMEMBER:** Đảm bảo copy TẤT CẢ files vào VM, đặc biệt là `ExplorerSettings.spec`! ⭐
