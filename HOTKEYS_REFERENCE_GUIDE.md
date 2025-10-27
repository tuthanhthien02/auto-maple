# ⌨️ HOTKEYS REFERENCE GUIDE - MASTER & SLAVE SCRIPTS

## 🎯 **MỤC ĐÍCH**

Liệt kê tất cả hotkeys trong Master và Slave scripts để dễ nắm bắt và sử dụng.

---

## 🖥️ **MASTER SCRIPT HOTKEYS**

### **🔧 CONTROL HOTKEYS (Quản lý script)**

| **Hotkey**   | **Chức năng**     | **Mô tả**                                 |
| ------------ | ----------------- | ----------------------------------------- |
| `Ctrl+Alt+S` | **Status Check**  | Hiển thị trạng thái VMs (found/missing)   |
| `Ctrl+Alt+L` | **List VMs**      | Liệt kê tất cả VMware windows để copy tên |
| `Ctrl+Alt+D` | **Toggle Debug**  | Bật/tắt debug tooltip                     |
| `Ctrl+Alt+B` | **Toggle Beep**   | Bật/tắt beep sound                        |
| `Ctrl+Alt+P` | **Performance**   | Hiển thị performance monitor (stats)      |
| `Ctrl+Alt+R` | **Refresh Cache** | Refresh VM cache (re-scan windows)        |
| `Ctrl+Alt+Q` | **Exit Script**   | Thoát Master script                       |

### **🎮 BROADCAST HOTKEYS (Gửi input đến VMs)**

#### **Skill Keys:**

| **Key** | **Broadcast** | **Mô tả**   |
| ------- | ------------- | ----------- |
| `Q`     | → All VMs     | Skill key Q |
| `W`     | → All VMs     | Skill key W |
| `E`     | → All VMs     | Skill key E |
| `R`     | → All VMs     | Skill key R |
| `A`     | → All VMs     | Skill key A |
| `S`     | → All VMs     | Skill key S |
| `D`     | → All VMs     | Skill key D |
| `F`     | → All VMs     | Skill key F |
| `Space` | → All VMs     | Space bar   |

#### **Arrow Keys:**

| **Key** | **Broadcast** | **Mô tả**   |
| ------- | ------------- | ----------- |
| `Left`  | → All VMs     | Arrow Left  |
| `Right` | → All VMs     | Arrow Right |
| `Up`    | → All VMs     | Arrow Up    |
| `Down`  | → All VMs     | Arrow Down  |

#### **Numpad Keys:**

| **Key**   | **Broadcast** | **Mô tả** |
| --------- | ------------- | --------- |
| `Numpad1` | → All VMs     | Numpad 1  |
| `Numpad2` | → All VMs     | Numpad 2  |
| `Numpad3` | → All VMs     | Numpad 3  |
| `Numpad4` | → All VMs     | Numpad 4  |
| `Numpad5` | → All VMs     | Numpad 5  |
| `Numpad6` | → All VMs     | Numpad 6  |
| `Numpad8` | → All VMs     | Numpad 8  |

#### **Number Keys:**

| **Key** | **Broadcast** | **Mô tả** |
| ------- | ------------- | --------- |
| `1`     | → All VMs     | Number 1  |
| `2`     | → All VMs     | Number 2  |
| `3`     | → All VMs     | Number 3  |
| `4`     | → All VMs     | Number 4  |
| `5`     | → All VMs     | Number 5  |
| `6`     | → All VMs     | Number 6  |
| `7`     | → All VMs     | Number 7  |
| `8`     | → All VMs     | Number 8  |
| `9`     | → All VMs     | Number 9  |
| `0`     | → All VMs     | Number 0  |

#### **Function Keys:**

| **Key** | **Broadcast** | **Mô tả**    |
| ------- | ------------- | ------------ |
| `F1`    | → All VMs     | Function F1  |
| `F2`    | → All VMs     | Function F2  |
| `F3`    | → All VMs     | Function F3  |
| `F4`    | → All VMs     | Function F4  |
| `F5`    | → All VMs     | Function F5  |
| `F6`    | → All VMs     | Function F6  |
| `F7`    | → All VMs     | Function F7  |
| `F8`    | → All VMs     | Function F8  |
| `F9`    | → All VMs     | Function F9  |
| `F10`   | → All VMs     | Function F10 |
| `F11`   | → All VMs     | Function F11 |
| `F12`   | → All VMs     | Function F12 |

---

## 💻 **SLAVE SCRIPT HOTKEYS**

### **🔧 CONTROL HOTKEYS (Quản lý script)**

| **Hotkey**   | **Chức năng**     | **Mô tả**                                     |
| ------------ | ----------------- | --------------------------------------------- |
| `Ctrl+Alt+T` | **Toggle Script** | Bật/tắt Slave script                          |
| `Ctrl+Alt+P` | **Performance**   | Hiển thị performance monitor (keypress stats) |
| `Ctrl+Alt+R` | **Reset Stats**   | Reset performance statistics                  |
| `Ctrl+Alt+D` | **Toggle Debug**  | Bật/tắt debug mode (show keypress info)       |

### **🎮 INPUT HOTKEYS (Nhận input từ Master)**

#### **Remapped Keys (Theo remap table):**

| **Input Key** | **Output Key** | **Mô tả**             |
| ------------- | -------------- | --------------------- |
| `Q`           | → `A`          | Skill Q → Skill A     |
| `W`           | → `S`          | Skill W → Skill S     |
| `E`           | → `D`          | Skill E → Skill D     |
| `R`           | → `F`          | Skill R → Skill F     |
| `Space`       | → `Space`      | Space → Space         |
| `Numpad1`     | → `Left`       | Numpad1 → Arrow Left  |
| `Numpad2`     | → `Down`       | Numpad2 → Arrow Down  |
| `Numpad3`     | → `Right`      | Numpad3 → Arrow Right |
| `Numpad5`     | → `Up`         | Numpad5 → Arrow Up    |

---

## 🔄 **WORKFLOW HOTKEYS**

### **📋 Setup Workflow:**

```
1. Master: Ctrl+Alt+L → Copy VM names
2. Master: Sửa vmList với tên VMs
3. Slave: Sửa MinDesync/MaxDesync cho mỗi VM
4. Master: Ctrl+Alt+S → Check VM status
5. Master: Ấn Q → Test broadcast
6. Slave: Ctrl+Alt+T → Toggle script ON/OFF
```

### **🎮 Training Workflow:**

```
1. Master: Ctrl+Alt+P → Check performance
2. Master: Ctrl+Alt+D → Toggle debug (optional)
3. Master: Ấn skill keys → Broadcast to all VMs
4. Slave: Ctrl+Alt+P → Check keypress stats
5. Slave: Ctrl+Alt+R → Reset stats (optional)
```

### **🔧 Debug Workflow:**

```
1. Master: Ctrl+Alt+S → Check VM status
2. Master: Ctrl+Alt+R → Refresh VM cache
3. Master: Ctrl+Alt+P → Check broadcast performance
4. Slave: Ctrl+Alt+D → Enable debug mode
5. Slave: Ctrl+Alt+P → Check keypress performance
```

---

## ⚡ **QUICK REFERENCE**

### **🖥️ Master Script:**

-   **Status:** `Ctrl+Alt+S`
-   **List VMs:** `Ctrl+Alt+L`
-   **Performance:** `Ctrl+Alt+P`
-   **Refresh:** `Ctrl+Alt+R`
-   **Exit:** `Ctrl+Alt+Q`

### **💻 Slave Script:**

-   **Toggle:** `Ctrl+Alt+T`
-   **Performance:** `Ctrl+Alt+P`
-   **Reset:** `Ctrl+Alt+R`
-   **Debug:** `Ctrl+Alt+D`

### **🎮 Common Keys:**

-   **Skills:** Q, W, E, R, A, S, D, F, Space
-   **Movement:** Left, Right, Up, Down
-   **Numpad:** 1, 2, 3, 4, 5, 6, 8
-   **Numbers:** 1-9, 0
-   **Functions:** F1-F12

---

## 💡 **TIPS & TRICKS**

### **🔍 Debugging:**

-   Dùng `Ctrl+Alt+S` trên Master để check VM status
-   Dùng `Ctrl+Alt+P` trên cả Master và Slave để check performance
-   Dùng `Ctrl+Alt+D` trên Slave để enable debug mode

### **⚡ Performance:**

-   Dùng `Ctrl+Alt+R` trên Master để refresh VM cache
-   Dùng `Ctrl+Alt+R` trên Slave để reset performance stats
-   Monitor performance với `Ctrl+Alt+P`

### **🎯 Testing:**

-   Dùng `Ctrl+Alt+L` trên Master để list VMs
-   Dùng `Ctrl+Alt+T` trên Slave để toggle script
-   Test với skill keys (Q, W, E, R) để verify broadcast

---

## ⚠️ **LƯU Ý QUAN TRỌNG**

### **🖥️ Master Script:**

-   Tất cả hotkeys đều broadcast đến **TẤT CẢ VMs**
-   `Ctrl+Alt+Q` sẽ thoát hoàn toàn Master script
-   `Ctrl+Alt+R` refresh VM cache để tăng performance

### **💻 Slave Script:**

-   `Ctrl+Alt+T` chỉ toggle Slave script trong VM đó
-   `Ctrl+Alt+D` enable debug mode để xem keypress info
-   `Ctrl+Alt+R` reset stats để bắt đầu monitoring mới

### **🎮 Key Mapping:**

-   Master broadcast → Slave nhận → Apply desync → Send to game
-   Mỗi VM có desync range khác nhau để tránh sync
-   Arrow keys có thể có/không có jitter tùy setting

---

**GOOD LUCK! ⌨️🎮**
