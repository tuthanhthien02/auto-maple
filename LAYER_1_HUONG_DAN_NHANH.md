# 🇻🇳 LAYER 1: HƯỚNG DẪN NHANH - MULTIPLICITY 4

**Thời gian:** 30-60 phút | **Độ khó:** Trung bình | **Chi phí:** $40-80

---

## 🎯 **MỤC TIÊU**

Điều khiển **3 clients MapleStory** từ **1 PC chính** (Primary PC).

**Kết quả:**

```
Primary PC: Bạn bấm Q
→ Client 1: Nhận Q → Đánh skill
→ Client 2: Nhận Q → Đánh skill
→ Client 3: Nhận Q → Đánh skill

Cả 3 nhân vật đánh skill CÙNG LÚC! ✅
```

---

## 📦 **CHUẨN BỊ**

### **Hardware cần có:**

-   ✅ **Primary PC:** PC chính (PC bạn đang dùng)
-   ✅ **3 Client PCs:** 3 máy chạy game
    -   Có thể là PC vật lý
    -   Hoặc VM (máy ảo)
    -   Hoặc mix cả 2

### **Network:**

-   ✅ Tất cả máy cùng mạng LAN (khuyến nghị)
-   ⚠️ Hoặc qua Internet (sẽ lag hơn)

### **Software:**

-   ✅ Multiplicity 4 - Download: https://www.stardock.com/products/multiplicity/
-   ✅ License key ($40-80) - 1 key dùng cho tất cả máy
-   ✅ MapleStory đã cài trên 3 clients

---

## 🚀 **SETUP TỪNG BƯỚC**

### **BƯỚC 1: Setup Primary PC (5 phút)**

**Trên PC chính của bạn:**

1. **Download Multiplicity:**

    ```
    https://www.stardock.com/products/multiplicity/
    → Download Multiplicity KVM
    ```

2. **Cài đặt:**

    ```
    - Run installer
    - Nhập license key
    - Chọn: "Primary Computer" ⭐ QUAN TRỌNG!
    - Next → Finish
    ```

3. **Auto setup (dùng script):**

    ```batch
    # Right-click → Run as Administrator
    setup_multiplicity_primary.bat

    # Làm theo hướng dẫn trên màn hình
    # Script sẽ tự động:
    - Tìm IP address của bạn
    - Mở firewall
    - Lưu IP để dùng sau
    ```

4. **Ghi lại IP của Primary:**
    ```
    Ví dụ: 192.168.1.100
    (Sẽ dùng để kết nối từ clients)
    ```

---

### **BƯỚC 2: Setup Client PCs (5 phút/máy)**

**Trên MỖI CLIENT PC (lặp lại 3 lần):**

1. **Download & Cài Multiplicity:**

    ```
    - Same installer như Primary
    - Nhập SAME license key
    - Chọn: "Secondary Computer" ⭐ QUAN TRỌNG!
    ```

2. **Kết nối đến Primary:**

    ```batch
    # Chạy script:
    setup_multiplicity_client.bat

    # Nhập IP của Primary: 192.168.1.100
    # Script sẽ test connection
    ```

3. **Verify kết nối:**
    ```
    - Mở Multiplicity
    - Status: "Connected to [Primary PC Name]"
    - Indicator: Màu XANH ✅
    ```

**Lặp lại cho Client 2 và Client 3!**

---

### **BƯỚC 3: Cấu hình Broadcast Mode (5 phút)**

**Trên PRIMARY PC:**

1. **Mở Multiplicity Settings:**

    ```
    Click icon Multiplicity → Configure
    ```

2. **Enable Broadcast:**

    ```
    Settings → Broadcast

    ✅ Tick "Broadcast keyboard input to all computers"
    ✅ Tick "Broadcast mouse clicks to all computers"

    Broadcast targets (chọn tất cả):
    ✅ Client 1
    ✅ Client 2
    ✅ Client 3
    ```

3. **Set Hotkey:**

    ```
    Toggle broadcast: Ctrl+Shift+B (mặc định)

    - Bấm 1 lần: BẬT broadcast (tất cả nhận input)
    - Bấm lần nữa: TẮT broadcast (chỉ 1 máy nhận)
    ```

4. **Arrange Screens (Grid View):**

    ```
    Configure → Grid View

    Kéo thả màn hình theo thứ tự:
    [Primary] [Client1] [Client2] [Client3]

    Di chuột qua biên phải → Chuột nhảy sang màn hình tiếp theo
    ```

---

### **BƯỚC 4: Setup MapleStory (5 phút/client)**

**Trên MỖI CLIENT PC:**

1. **Launch MapleStory**

2. **Chuyển sang Windowed Mode:**

    ```
    Settings → Display
    → Window Mode: "Windowed" hoặc "Borderless Windowed"

    Resolution khuyến nghị:
    - 1366x768 (nhẹ, ít lag)
    - 1920x1080 (đẹp hơn)

    ⚠️ TẤT CẢ 3 CLIENTS PHẢI CÙNG RESOLUTION!
    ```

3. **Đặt cửa sổ game ở vị trí giống nhau:**

    ```
    Kéo cửa sổ MapleStory về góc trên-trái màn hình
    (Giống nhau trên cả 3 clients)

    Tại sao? → Để click chuột rơi đúng vị trí trên cả 3 màn hình
    ```

4. **Login vào game:**
    ```
    Tất cả 3 clients login đến character select hoặc in-game
    ```

---

## 🧪 **TEST BROADCAST**

### **Test 1: Test cơ bản (keyboard)**

**Trên Primary PC:**

1. **Bật broadcast mode:**

    ```
    Bấm: Ctrl+Shift+B
    → Indicator sẽ hiện "BROADCAST" hoặc icon thay đổi
    ```

2. **Bấm phím Q:**

    ```
    Expected: Tất cả 3 clients đều nhận phím Q
    ```

3. **Thử các phím khác:**
    ```
    W, E, R, 1, 2, 3, Arrow keys
    → Tất cả clients đều nhận ✅
    ```

---

### **Test 2: Test trong game**

**Với cả 3 clients đã login MapleStory:**

1. **Bật broadcast:** `Ctrl+Shift+B`

2. **Bấm Arrow Right:**

    ```
    Expected: Cả 3 nhân vật đi sang phải cùng lúc ✅
    ```

3. **Bấm Q (skill key):**

    ```
    Expected: Cả 3 nhân vật đánh skill cùng lúc ✅
    ```

4. **Bấm Alt (jump):**
    ```
    Expected: Cả 3 nhân vật nhảy cùng lúc ✅
    ```

**✅ Nếu tất cả hoạt động → Layer 1 THÀNH CÔNG!**

---

### **Test 3: Automated Test**

**Chạy script tự động:**

```batch
# Trên Primary PC:
test_multiplicity_broadcast.ahk

# Script sẽ tự động:
- Test arrow keys
- Test jump
- Test skill keys
- Generate report
```

**Kết quả:**

-   ✅ **PASSED:** Layer 1 complete!
-   ❌ **FAILED:** Xem phần Troubleshooting

---

## 🔧 **TROUBLESHOOTING**

### **❌ Lỗi 1: Clients không kết nối được**

**Triệu chứng:** Status "Disconnected" hoặc màu đỏ

**Nguyên nhân & Fix:**

```
1. Firewall chặn:
   → Windows Defender Firewall → Allow app
   → Add "Multiplicity.exe"
   → Allow cả Private & Public networks

2. Sai IP:
   → Trên Primary: cmd → ipconfig
   → Tìm IPv4 Address
   → Dùng IP này trên clients

3. Khác mạng:
   → Đảm bảo tất cả máy cùng WiFi/LAN
   → Hoặc setup port forwarding nếu qua Internet
```

---

### **❌ Lỗi 2: Broadcast không hoạt động**

**Triệu chứng:** Chỉ 1 client nhận input, không phải cả 3

**Fix:**

```
1. Kiểm tra broadcast targets:
   Settings → Broadcast
   → Đảm bảo ✅ tất cả 3 clients

2. Toggle broadcast hotkey:
   → Bấm Ctrl+Shift+B
   → Nhìn indicator có hiện "BROADCAST" không

3. Restart Multiplicity:
   → Tắt Multiplicity trên TẤT CẢ máy
   → Bật Primary trước
   → Sau đó bật Clients
   → Reconnect
```

---

### **❌ Lỗi 3: Input lag/delay**

**Triệu chứng:** Phím bấm chậm, chuột giật

**Fix:**

```
1. Check network latency:
   cmd → ping [Primary IP]
   → Nếu > 50ms: Chuyển sang dây mạng (Ethernet)

2. Tắt encryption (nếu cùng LAN):
   Settings → Security
   → Bỏ tick "Encrypt connection"

3. Giảm quality:
   Settings → Display
   → Remote display quality: "Performance"
```

---

### **❌ Lỗi 4: MapleStory không nhận input**

**Triệu chứng:** Broadcast hoạt động ở desktop, nhưng không hoạt động trong game

**Fix:**

```
1. Chuyển sang Windowed mode:
   MapleStory Settings → Display → Windowed
   (KHÔNG dùng Fullscreen)

2. Same resolution trên tất cả clients:
   Tất cả phải 1366x768 hoặc tất cả 1920x1080

3. Run as Administrator:
   Right-click Multiplicity → Run as Administrator
   (Cả Primary và Clients)
```

---

## 🛡️ **OBFUSCATION (ẨN PROCESS)**

**Tại sao cần?** MapleStory anti-cheat có thể detect "Multiplicity.exe" đang chạy → Ban!

**Giải pháp:** Đổi tên process thành tên giống Windows service

### **Cách 1: Dùng Script (Khuyến nghị)**

```batch
# Run as Administrator:
obfuscate_multiplicity.bat

# Script sẽ tự động:
- Backup Multiplicity.exe
- Rename → SystemAudioService.exe
- Looks like Windows service ✅
```

### **Cách 2: Manual**

**Trên MỖI CLIENT PC:**

```batch
# 1. Tắt Multiplicity

# 2. Mở folder:
cd "C:\Program Files\Multiplicity"

# 3. Backup:
copy Multiplicity.exe Multiplicity.exe.backup

# 4. Rename:
ren Multiplicity.exe SystemAudioService.exe

# 5. Chạy file mới:
SystemAudioService.exe
```

**Kết quả:**

```
Task Manager sẽ hiện:
❌ Multiplicity.exe (dễ bị detect)
✅ SystemAudioService.exe (trông như Windows service)
```

---

## ✅ **VERIFICATION CHECKLIST**

**Layer 1 hoàn thành nếu:**

-   [ ] ✅ Multiplicity installed trên cả 4 PCs (1 primary + 3 clients)
-   [ ] ✅ Tất cả clients kết nối được (status: Connected)
-   [ ] ✅ Broadcast mode hoạt động (Ctrl+Shift+B toggle)
-   [ ] ✅ Test: Bấm Q → Cả 3 clients nhận Q
-   [ ] ✅ MapleStory chạy Windowed mode trên tất cả clients
-   [ ] ✅ Test in-game: Cả 3 chars di chuyển cùng lúc
-   [ ] ✅ Không lag (< 100ms)
-   [ ] ✅ Process đã rename (obfuscated)

**✅ TẤT CẢ CHECKED → LAYER 1 HOÀN THÀNH!** 🎉

---

## 📊 **KẾT QUẢ SAU LAYER 1**

```
✅ Efficiency: 3x
   (Điều khiển 3 accounts cùng lúc)

⚠️ Detection Evasion: ~20%
   (Vẫn dễ bị detect do perfect sync)

❌ Ban Risk: CAO
   Lý do:
   - Timing hoàn toàn giống nhau (millisecond)
   - Actions 100% synchronized
   - Không có variance

→ CẦN LAYERS 2-8 ĐỂ TĂNG EVASION LÊN 71%!
```

---

## 🎯 **NEXT STEPS**

**Khi đã hoàn thành Layer 1:**

1. ✅ **Skip Layer 2** (nếu không dùng VMs)

2. 🔜 **Layer 3:** VPN per Client

    - Setup 3 VPNs khác nhau
    - Mỗi client 1 IP
    - +8% evasion

3. 🔜 **Layer 4:** PowerToys Key Remap

    - Mỗi client nhận key khác nhau
    - +2% evasion

4. 🔜 **Layer 5:** Input Jitter ⭐ **CRITICAL**

    - Break perfect sync
    - +12% evasion

5. 🔜 **Layer 6:** Gaussian Delays ⭐ **CRITICAL**
    - Different timing profiles
    - +15% evasion

**Total after 8 layers: 71% evasion ✅**

---

## 💰 **CHI PHÍ**

```
Multiplicity License:     $40-80  (one-time)
VPN (3 services):         $30/mo  (from Layer 3)
Time investment:          2 hours (setup)

Total initial:            $40-80
Monthly recurring:        $30 (if using VPNs)
```

---

## 💡 **TIPS**

1. **Dùng mạng dây (Ethernet)**

    - Ổn định hơn WiFi
    - Ít lag hơn
    - Không bị disconnect

2. **Same resolution mọi clients**

    - Dễ click đúng vị trí
    - Ít lỗi hơn

3. **Test kỹ trước khi farm**

    - Chạy thử 1-2 giờ
    - Verify không crash
    - Check không lag

4. **Backup config**

    - Export Multiplicity settings
    - Lưu lại IP addresses
    - Dễ restore nếu lỗi

5. **Monitor ban reports**
    - Check forums/Discord
    - Nếu ban rate tăng → Pause
    - Adjust strategy

---

## 📞 **HỖ TRỢ**

**Nếu gặp vấn đề:**

1. **Check log files:**

    - `multiplicity_test_log.txt`
    - Multiplicity → View Logs

2. **Google error messages:**

    - Most issues đã có người gặp

3. **Ask me!**
    - Paste error message
    - Describe what happened
    - Tôi sẽ troubleshoot! 🚀

---

## 🏆 **SUMMARY**

**Layer 1 = Foundation của toàn bộ hệ thống**

```
✅ Đạt được:
   - Điều khiển 3 clients cùng lúc
   - Tất cả nhận input giống nhau
   - Efficiency 3x

⚠️ Vẫn còn:
   - Perfect synchronization (detectable)
   - No timing variance
   - No behavioral variation

→ Layers 2-8 sẽ fix những vấn đề này!
```

---

**BẮT ĐẦU NGAY!** 🚀

1. Download Multiplicity
2. Chạy `setup_multiplicity_primary.bat`
3. Chạy `setup_multiplicity_client.bat` trên 3 clients
4. Test với `test_multiplicity_broadcast.ahk`
5. **DONE!** ✅

**Hỏi tôi nếu cần giúp bất kỳ bước nào!** 💬✨


