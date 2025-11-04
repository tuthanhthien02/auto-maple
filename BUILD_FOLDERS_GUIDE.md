# 📦 PyInstaller Build Folders Guide

## 📂 Folder Structure Sau Khi Build

Sau khi build với PyInstaller, bạn sẽ có 2 folders:

### **1. `dist/` folder** ✅ **USE THIS!**

**Chứa gì:**

-   `ExplorerSettings.exe` - Executable file (file bạn cần chạy!)
-   `ExplorerSettings/_internal/` - Tất cả dependencies và resources
    -   Python libraries
    -   Assets folder
    -   Resources folder
    -   Config files

**Path:**

```
dist/
└── ExplorerSettings/
    ├── ExplorerSettings.exe  ← Chạy file này!
    └── _internal/
        ├── assets/
        ├── resources/
        ├── src/
        └── ... (all dependencies)
```

**Usage:**

-   ✅ **Dùng folder này** để chạy bot
-   ✅ Copy cả folder `ExplorerSettings` đến máy khác
-   ✅ Không cần Python để chạy

---

### **2. `build/` folder** 🗑️ **CAN DELETE**

**Chứa gì:**

-   Temporary files trong quá trình build
-   Compiled Python bytecode (.pyc files)
-   Analysis results
-   Intermediate build artifacts

**Path:**

```
build/
└── ExplorerSettings/
    ├── Analysis-00.toc
    ├── PKG-00.toc
    └── EXE-00.toc
```

**Usage:**

-   ⚠️ **Không cần thiết** sau khi build xong
-   ✅ **Có thể xóa** để tiết kiệm dung lượng
-   ✅ Sẽ được tạo lại khi build lại

---

## 🎯 Summary

| Folder       | Cần thiết? | Dùng để làm gì?       | Có thể xóa? |
| ------------ | ---------- | --------------------- | ----------- |
| **`dist/`**  | ✅ YES     | Chạy bot (executable) | ❌ NO       |
| **`build/`** | ❌ NO      | Temporary build files | ✅ YES      |

---

## 📝 Recommendation

### **Sau khi build xong:**

1. ✅ **Dùng:** `dist\ExplorerSettings\ExplorerSettings.exe`
2. ✅ **Có thể xóa:** `build\` folder (để tiết kiệm dung lượng)

### **Để chạy bot:**

```batch
# Option 1: Chạy trực tiếp
.\dist\ExplorerSettings\ExplorerSettings.exe

# Option 2: Copy folder ExplorerSettings đến nơi khác và chạy
copy dist\ExplorerSettings C:\MyBot\
C:\MyBot\ExplorerSettings.exe
```

---

## 💡 Tips

1. **Dist folder là portable:** Copy cả folder `ExplorerSettings` đến máy khác vẫn chạy được (không cần Python)
2. **Build folder chỉ cần khi build:** Nếu không build lại, có thể xóa để tiết kiệm dung lượng
3. **Clean build:** Nếu build lại, script sẽ tự động xóa `build\` và `dist\` folder cũ

---

**Tóm lại:** Dùng `dist\ExplorerSettings\ExplorerSettings.exe` - đó là file executable bạn cần! 🚀
