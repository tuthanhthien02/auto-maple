# Fix: NGS Hacking Detected trên Host (Chưa Mở Bot)

## 🔍 Vấn Đề

Bot work tốt trên VMware, nhưng khi chạy trên **host máy** thì **chưa mở bot đã bị lỗi NGS**.

## 🎯 Nguyên Nhân

### **Các Nguyên Nhân Có Thể:**

1. **Keyboard Hooks Đang Chạy** ⚠️ HIGH RISK

    - `keyboard_to_arduino.py` - Keyboard hook
    - `keyboard_block_arduino.py` - Keyboard hook
    - `host_sender.py` - Keyboard hook
    - `vmware_receiver.py` - Keyboard hook
    - **NGS có thể detect keyboard hooks ngay cả khi bot chưa chạy**

2. **Python Processes Đang Chạy** ⚠️ MEDIUM RISK

    - Python processes có thể bị NGS scan
    - Có thể là processes từ lần chạy trước

3. **Folder/File Bot Bị NGS Scan** ⚠️ LOW RISK

    - NGS có thể scan folder/file của bot
    - Tên file/folder có thể trigger detection

4. **Registry Entries** ⚠️ LOW RISK
    - NGS có thể scan registry entries
    - Có thể có traces từ lần chạy trước

---

## ✅ Solutions

### **Solution 1: Kill All Keyboard Hooks TRƯỚC Khi Start Game** ⭐ PRIORITY 1

**Vấn đề:**

-   Keyboard hooks đang chạy sẽ trigger NGS detection
-   NGS có thể detect hooks ngay cả khi bot chưa chạy

**Solution:**

1. **Check processes đang chạy:**

    ```bash
    check_ngs_processes.bat
    ```

2. **Kill tất cả processes:**

    ```bash
    kill_ngs_processes.bat
    ```

3. **Start game SAU KHI kill processes**

---

### **Solution 2: Đảm Bảo Không Có Processes Đang Chạy**

**Check manual:**

```bash
tasklist | findstr /I "python keyboard host vmware ExplorerSettings"
```

**Nếu có processes → Kill tất cả:**

```bash
taskkill /F /IM python.exe
taskkill /F /IM pythonw.exe
taskkill /F /IM ExplorerSettings.exe
```

---

### **Solution 3: Rename Folder/File** ⭐ PRIORITY 2

**Vấn đề:**

-   NGS có thể scan folder/file có tên suspicious
-   Tên folder "auto-maple" có thể trigger detection

**Solution:**

1. **Rename folder:**

    ```
    auto-maple → ExplorerSettings (hoặc tên khác)
    ```

2. **Rename main files:**
    ```
    main.py → settings.py (hoặc tên khác)
    ```

---

### **Solution 4: Hide Folder/File** ⭐ PRIORITY 3

**Vấn đề:**

-   NGS có thể scan folder/file

**Solution:**

1. **Move folder vào vị trí ít suspicious:**

    ```
    C:\Users\...\auto-maple
    → C:\Program Files\ExplorerSettings
    → C:\Windows\System32\ExplorerSettings
    ```

2. **Rename với tên Windows-like:**
    ```
    auto-maple → ExplorerSettings
    main.py → settings.py
    ```

---

### **Solution 5: Chỉ Chạy Bot Khi Cần**

**Vấn đề:**

-   Bot không nên chạy khi không cần

**Solution:**

1. **Chỉ start bot KHI game đã start**
2. **Close bot TRƯỚC KHI close game**
3. **Kill tất cả processes TRƯỚC KHI start game**

---

## 🚀 Quick Fix Checklist

### **Before Starting Game:**

-   [ ] 1. Run `check_ngs_processes.bat` - Check processes
-   [ ] 2. Run `kill_ngs_processes.bat` - Kill all processes
-   [ ] 3. Verify no Python processes running
-   [ ] 4. Verify no keyboard hooks running
-   [ ] 5. Start game
-   [ ] 6. **SAU KHI game start** → Start bot

### **After Closing Game:**

-   [ ] 1. Close bot
-   [ ] 2. Run `kill_ngs_processes.bat` - Kill all processes
-   [ ] 3. Verify no processes running

---

## 📝 Workflow Recommended

### **1. Start Game (Host):**

```
1. Check processes: check_ngs_processes.bat
2. Kill processes: kill_ngs_processes.bat
3. Start game (MapleStory)
4. Wait for game to fully load
5. Start bot (ExplorerSettings.exe)
```

### **2. Close Game (Host):**

```
1. Stop bot (Press Insert to stop)
2. Close bot GUI
3. Kill processes: kill_ngs_processes.bat
4. Close game
```

---

## ⚠️ Critical Notes

1. **Keyboard Hooks là Nguyên Nhân Chính:**

    - NGS rất dễ detect keyboard hooks
    - Phải kill tất cả hooks TRƯỚC KHI start game

2. **Workflow Quan Trọng:**

    - **KHÔNG** start bot trước khi start game
    - **KHÔNG** để keyboard hooks chạy khi không cần
    - **LUÔN** kill processes TRƯỚC KHI start game

3. **VMware vs Host:**
    - VMware: Work tốt vì NGS không scan VMware processes
    - Host: Bị detect vì NGS scan tất cả processes trên host

---

## 🎯 Summary

**Nguyên nhân chính:** Keyboard hooks đang chạy khi start game

**Fix chính:** Kill tất cả processes TRƯỚC KHI start game

**Workflow:**

1. Kill processes → Start game → Start bot
2. Stop bot → Kill processes → Close game
