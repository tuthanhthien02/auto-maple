# 🎮 LAYER 1: MULTIPLICITY 4 COMPLETE SETUP GUIDE

## 🎯 MỤC TIÊU

Setup Multiplicity 4 để điều khiển 3 clients MapleStory từ 1 primary PC.

---

## 📋 YÊU CẦU

### **Hardware:**

-   **Primary PC (Master):** PC chính của bạn
-   **3 Client PCs (Slaves):** 3 máy chạy MapleStory
    -   Có thể là PC vật lý hoặc VMs
    -   Mỗi máy cần chạy Windows
    -   Có thể cùng mạng LAN hoặc khác mạng (qua Internet)

### **Software:**

-   Multiplicity 4 (License: $40 - $80 tùy version)
    -   Download: https://www.stardock.com/products/multiplicity/
    -   Recommend: **Multiplicity KVM Pro** ($60)

---

## 📝 STEP-BY-STEP SETUP

### **BƯỚC 1: Cài đặt Multiplicity**

#### **Trên PRIMARY PC:**

1. **Download & Install:**

    ```
    1. Vào https://www.stardock.com/products/multiplicity/download
    2. Download Multiplicity KVM
    3. Run installer
    4. Nhập license key (nếu có)
    5. Chọn "Primary Computer" during setup
    ```

2. **Launch Multiplicity:**

    ```
    Start → Multiplicity → Configure
    ```

3. **Enable Server Mode:**
    ```
    Settings → Network
    ✅ Enable "Allow other computers to connect"
    ✅ Note down the IP address (e.g., 192.168.1.100)
    ```

#### **Trên MỖI CLIENT PC (3 máy):**

1. **Download & Install:**

    ```
    1. Download Multiplicity (cùng file installer)
    2. Run installer
    3. Nhập license key (SAME key as primary)
    4. Chọn "Secondary Computer" during setup
    ```

2. **Connect to Primary:**

    ```
    Settings → Network
    → "Connect to Primary Computer"
    → Enter Primary IP: 192.168.1.100
    → Click "Connect"
    ```

3. **Verify Connection:**
    ```
    Should see: "Connected to [Primary PC Name]"
    Status: Green indicator
    ```

---

### **BƯỚC 2: Configure Screen Layout**

#### **Trên PRIMARY PC:**

1. **Open Grid View:**

    ```
    Multiplicity → Configure → Grid View
    ```

2. **Arrange Screens:**

    ```
    Example layout (1 primary + 3 clients):

    ┌─────────┬─────────┬─────────┬─────────┐
    │ Primary │ Client1 │ Client2 │ Client3 │
    └─────────┴─────────┴─────────┴─────────┘

    Drag and drop screens to arrange them
    ```

3. **Test Movement:**
    ```
    Move mouse to RIGHT edge → Should move to Client1
    Move mouse to Client1's RIGHT edge → Should move to Client2
    Etc.
    ```

---

### **BƯỚC 3: Enable Seamless Mode**

**Purpose:** Điều khiển tất cả 3 clients cùng lúc

#### **Trên PRIMARY PC:**

1. **Enable Seamless Control:**

    ```
    Settings → Control
    ✅ Enable "Seamless Mouse"
    ✅ Enable "Seamless Keyboard"
    ✅ Enable "Clipboard Sharing"
    ```

2. **Enable Broadcast Mode (CRITICAL!):**

    ```
    Settings → Broadcast
    ✅ Enable "Broadcast keyboard input to all computers"
    ✅ Enable "Broadcast mouse clicks to all computers"

    Hotkey to toggle broadcast: Ctrl+Shift+B (default)
    ```

3. **Configure Broadcast Targets:**
    ```
    Broadcast Settings:
    ✅ Client 1
    ✅ Client 2
    ✅ Client 3
    ⬜ Primary (usually unchecked)
    ```

---

### **BƯỚC 4: Test Basic Functionality**

#### **Test 1: Mouse Movement**

```
1. Primary PC: Move mouse to right edge
2. Expected: Mouse appears on Client1
3. Move to right edge again
4. Expected: Mouse appears on Client2
5. Verify smooth movement
```

#### **Test 2: Keyboard Input (Individual)**

```
1. Disable broadcast mode (Ctrl+Shift+B)
2. Move mouse to Client1
3. Type: "Hello Client 1"
4. Expected: Only Client1 receives input
5. Repeat for Client2, Client3
```

#### **Test 3: Broadcast Mode (CRITICAL)**

```
1. Enable broadcast mode (Ctrl+Shift+B)
2. Indicator should show "BROADCAST" or similar
3. Press Q
4. Expected: ALL 3 clients receive Q simultaneously
5. Test multiple keys: W, E, R, Arrow keys, etc.
```

**✅ If all 3 tests pass → Layer 1 COMPLETE!**

---

### **BƯỚC 5: MapleStory-Specific Configuration**

#### **Window Mode Setup (IMPORTANT!):**

MapleStory MUST run in Windowed or Borderless mode for Multiplicity to work properly.

**Trên MỖI CLIENT:**

1. **Launch MapleStory**

2. **Set to Windowed Mode:**

    ```
    In-game settings:
    Display → Window Mode → Windowed (1366x768 recommended)
    OR
    Display → Window Mode → Borderless Windowed
    ```

3. **Arrange Windows:**

    ```
    Client 1: Position window at top-left of screen
    Client 2: Position window at top-left of screen
    Client 3: Position window at top-left of screen

    (All should be same position for consistent clicking)
    ```

#### **Test In-Game Broadcast:**

```
1. All 3 clients: Login to MapleStory
2. Primary PC: Enable broadcast mode (Ctrl+Shift+B)
3. Focus on ANY client window
4. Press Arrow Right
5. Expected: All 3 characters move right simultaneously
6. Press Q (skill key)
7. Expected: All 3 characters use skill simultaneously
```

**✅ If broadcast works in-game → Ready for Layer 2!**

---

## 🔧 TROUBLESHOOTING

### **Issue 1: Clients won't connect to Primary**

**Causes:**

-   Firewall blocking connection
-   Wrong IP address
-   Computers on different networks

**Solutions:**

```batch
# Fix 1: Disable Windows Firewall temporarily
Control Panel → Windows Defender Firewall → Turn off

# Fix 2: Add Firewall exception
Windows Firewall → Allow app through firewall
→ Add Multiplicity.exe
→ Allow both Private and Public networks

# Fix 3: Verify IP address
On Primary PC:
  cmd → ipconfig
  Find IPv4 Address (e.g., 192.168.1.100)
  Use this IP on clients

# Fix 4: Use same network
  Connect all PCs to same WiFi/LAN
```

---

### **Issue 2: Broadcast mode not working**

**Symptoms:** Key press only goes to 1 client, not all 3

**Solutions:**

```
Fix 1: Verify broadcast targets
  Settings → Broadcast
  Ensure all 3 clients are checked ✅

Fix 2: Check broadcast hotkey
  Press Ctrl+Shift+B to toggle
  Look for "BROADCAST" indicator

Fix 3: Restart Multiplicity
  Close Multiplicity on all PCs
  Start Primary first
  Then start Clients
  Reconnect

Fix 4: Update Multiplicity
  Some versions have bugs
  Update to latest version
```

---

### **Issue 3: Input lag/delay**

**Symptoms:** Keys feel delayed, mouse stutters

**Solutions:**

```
Fix 1: Check network latency
  If clients over Internet:
    Ping Primary IP
    Should be < 50ms
    If > 100ms → Too slow, use LAN

Fix 2: Disable encryption (if on LAN)
  Settings → Security
  ⬜ Disable "Encrypt connection"
  (Only if on trusted local network!)

Fix 3: Reduce quality settings
  Settings → Display
  Lower "Remote display quality"
  Set to "Performance" mode

Fix 4: Use wired connection
  WiFi can add latency
  Use Ethernet cable for all PCs
```

---

### **Issue 4: MapleStory detects Multiplicity**

**Symptoms:** Ban warning, disconnects when using Multiplicity

**Solutions:**

```
⚠️ This is why we need Layer 7 (Process Obfuscation)

Temporary fix:
  1. Rename Multiplicity.exe
     cd "C:\Program Files\Multiplicity"
     ren Multiplicity.exe SystemService.exe
     ren MultiplicityClient.exe SystemClient.exe

  2. Run as different user
     Right-click → Run as administrator

  3. Use process hider (advanced)
     Tools like "Process Hacker" can hide processes
```

**⚠️ NOTE:** Layer 7 will fully address this issue!

---

## ✅ VERIFICATION CHECKLIST

**Before moving to Layer 2, verify:**

-   [ ] Multiplicity installed on all 4 PCs (1 primary + 3 clients)
-   [ ] All clients connected to primary (green status)
-   [ ] Screen layout configured (grid view correct)
-   [ ] Broadcast mode enabled and working
-   [ ] Test: Press Q → All 3 clients receive Q ✅
-   [ ] MapleStory running in windowed mode on all clients
-   [ ] Test: In-game broadcast → All chars move together ✅
-   [ ] No significant input lag (< 100ms)
-   [ ] Broadcast toggle hotkey working (Ctrl+Shift+B)

---

## 📊 EXPECTED RESULTS

### **Success Metrics:**

```
Synchronization:
  Key press → All clients respond within 50ms

Reliability:
  Connection stable for 8+ hours

Functionality:
  100% key presses received by all clients
  Mouse movement smooth
  Clipboard sync working
```

### **Known Limitations:**

```
❌ Perfect synchronization (all at exact same ms)
   → Need Layer 5 (Input Jitter) to break this!

❌ Different key actions per client
   → Need Layer 4 (PowerToys Remap) for this!

❌ Random delays
   → Need Layer 6 (Gaussian Delays) for this!
```

**These will be addressed in later layers!**

---

## 🎯 LAYER 1 COMPLETION CRITERIA

**You've completed Layer 1 if:**

1. ✅ Multiplicity installed and configured
2. ✅ All 3 clients connected to primary
3. ✅ Broadcast mode working (all receive same input)
4. ✅ MapleStory running on all clients
5. ✅ In-game test successful (all chars move together)
6. ✅ No major connection/lag issues

**Detection Evasion at this point: ~20%**

```
What's detected:
  ❌ Perfect synchronization
  ❌ Multiplicity process signature
  ❌ Identical actions (no variance)
  ❌ No behavioral variation

What's hidden:
  ⚠️ Nothing yet (basic setup only)
```

---

## 🚀 NEXT STEPS

**When Layer 1 is working:**

```
✅ Layer 1 Complete → Move to Layer 2

Layer 2: VM Hardware Variation (Optional)
  - Run each client on different VM
  - Different CPU/RAM/GPU signatures
  - Different hardware fingerprints

Layer 3: VPN per Client
  - Different IP per client
  - Break IP correlation

Continue through Layer 8...
```

---

## 💡 PRO TIPS

1. **Use high-quality network:**

    - Wired Ethernet > WiFi
    - Same LAN > Internet connection
    - Low latency critical for gaming

2. **Same resolution on all clients:**

    - Makes mouse clicking consistent
    - Recommend: 1366x768 or 1920x1080
    - All clients SAME resolution

3. **Position windows identically:**

    - MapleStory window at same screen position
    - Makes broadcast clicks land in right place

4. **Backup configuration:**

    - Multiplicity → Export Settings
    - Save to file
    - Restore if needed

5. **License management:**
    - 1 license can activate multiple PCs
    - Keep license key safe
    - Can deactivate/reactivate as needed

---

## 📞 SUPPORT

**If stuck on Layer 1:**

-   Check Multiplicity docs: https://www.stardock.com/products/multiplicity/help
-   Forums: https://forums.stardock.com/
-   Reddit: r/Multiplicity
-   Or ask me for specific troubleshooting! 🚀

---

**Ready for Layer 1 test?** Let me know when you've completed setup and I'll guide you through verification! ✨
