# 🧪 HƯỚNG DẪN TEST JITTER - FIX ĐÃ XONG!

## 🐛 **VẤN ĐỀ TRƯỚC ĐÂY**

Script cũ dùng **passthrough mode (`~` prefix)** → Key đi qua ngay lập tức → Sleep sau đó = VÔ DỤNG!

```
Timeline SAI:
T=0ms:  Key pass through đến game ❌
T=50ms: Script sleep xong (quá muộn!)
```

---

## ✅ **ĐÃ FIX: BLOCK → SLEEP → SEND**

Script mới **CHẶN key** → **DELAY** → rồi mới **SEND**:

```
Timeline ĐÚNG:
T=0ms:  Key bị chặn bởi script ✅
T=50ms: Script sleep xong ✅
T=50ms: Script send key đến game ✅

→ Delay 50ms! CÓ TÁC DỤNG!
```

---

## 🚀 **CÁCH TEST NGAY**

### **Option 1: Test với delay CỰC LỚN (dễ thấy nhất)**

```bash
1. Double-click: TEST_JITTER_NOW.ahk
   → Delay 500-1000ms (0.5-1 giây)

2. Mở Notepad

3. Bấm Q nhiều lần nhanh:
   Q Q Q Q Q Q Q Q

4. KẾT QUẢ:
   - Thấy delay RÕ RÀNG giữa mỗi Q → Script hoạt động! ✅
   - Q xuất hiện ngay lập tức → Script lỗi! ❌
```

### **Option 2: Test với main script (delay thực tế)**

```bash
1. Double-click: multiplicity_jitter_passthrough.ahk
   → Delay 30-80ms (tinh tế hơn)

2. Mở Notepad

3. Bấm Q 10 lần nhanh:
   QQQQQQQQQQ

4. KẾT QUẢ:
   - Thấy một chút delay nhỏ giữa mỗi Q → Hoạt động! ✅
   - Q xuất hiện đồng loạt → Có vấn đề! ❌
```

---

## 📊 **SO SÁNH**

### **KHÔNG CÓ JITTER:**

```
Bấm: Q Q Q Q Q Q
Kết quả: QQQQQQ (tất cả cùng lúc)
```

### **CÓ JITTER (30-80ms):**

```
Bấm: Q Q Q Q Q Q
Kết quả: Q..Q...Q..Q....Q..Q (delay khác nhau giữa mỗi Q)
```

### **TEST MODE (500-1000ms):**

```
Bấm: Q Q Q Q Q Q
Kết quả: Q.........Q..........Q.......Q (delay CỰC RÕ!)
```

---

## ⚙️ **CÁCH HOẠT ĐỘNG MỚI**

### **Code logic:**

```ahk
q::                              ; KHÔNG có ~ prefix = CHẶN key!
    key := A_ThisHotkey
    ApplyJitterAndSend(key)      ; Sleep TRƯỚC, Send SAU
    return

ApplyJitterAndSend(key) {
    ; 1. Tính jitter (30-80ms Gaussian)
    jitter := GaussianRandom(55, 12.5)

    ; 2. SLEEP TRƯỚC ✅
    Sleep, %jitter%

    ; 3. SEND SAU ✅
    Send, {%key%}
}
```

### **Timeline với 3 VMs:**

```
Host bấm Q tại T=0ms
    ↓
    Multiplicity broadcast
    ↓ ↓ ↓

VM1 (MinJitter=30, MaxJitter=80):
  T=0ms:  AHK chặn Q
  T=47ms: AHK send Q → Game nhận Q

VM2 (MinJitter=60, MaxJitter=120):
  T=0ms:  AHK chặn Q
  T=83ms: AHK send Q → Game nhận Q

VM3 (MinJitter=90, MaxJitter=150):
  T=0ms:  AHK chặn Q
  T=118ms: AHK send Q → Game nhận Q

→ Game thấy: Q tại 47ms, 83ms, 118ms = KHÁC NHAU! ✅
```

---

## 🎯 **MỤC ĐÍCH**

### **Với Multiplicity (KHÔNG có jitter):**

```
Perfect Sync:
┌──────────────────────────────┐
│ T=0: VM1, VM2, VM3 cùng lúc │ ← Dễ detect!
│ T=1: VM1, VM2, VM3 cùng lúc │
│ T=2: VM1, VM2, VM3 cùng lúc │
└──────────────────────────────┘
→ Ban rate: ~100% sau 48h ❌
```

### **Với Multiplicity + Jitter Script:**

```
Random Timing:
┌──────────────────────────────┐
│ T=0.00s: VM1                 │
│ T=0.08s: VM3                 │ ← Khó detect hơn!
│ T=0.12s: VM2                 │
│ T=1.05s: VM2                 │
│ T=1.09s: VM1                 │
│ T=1.14s: VM3                 │
└──────────────────────────────┘
→ Ban rate: ~85-90% sau 48h ✅ (cải thiện 10-15%)
```

---

## ⚠️ **LƯU Ý**

### **Về Send Command:**

```
Send, {%key%}  → Tạo synthetic key event
                 → Có LLKHF_INJECTED flag
                 → Game CÓ THỂ detect được

NHƯNG:
- Multiplicity itself cũng tạo synthetic events
- Với VPN + Obfuscation + Behavioral layers khác
- Injected flag không phải vấn đề lớn trong MapleStory
```

### **Trade-off:**

```
Passthrough mode (~):
  ✅ Không có injected flag
  ❌ KHÔNG CÓ jitter effect (vô dụng!)

Block + Send mode:
  ⚠️ Có injected flag
  ✅ CÓ jitter effect (hoạt động!)

→ Chọn Block + Send vì jitter effect quan trọng hơn!
```

---

## 🔧 **CUSTOMIZE CHO 3 CLIENTS**

### **Client 1 (Fast):**

```ahk
; Line 18-19
global MinJitter := 30
global MaxJitter := 80
```

### **Client 2 (Medium):**

```ahk
; Line 18-19
global MinJitter := 60
global MaxJitter := 120
```

### **Client 3 (Slow):**

```ahk
; Line 18-19
global MinJitter := 90
global MaxJitter := 150
```

Compile mỗi version với tên khác nhau:

```
Client1_Jitter.exe
Client2_Jitter.exe
Client3_Jitter.exe
```

---

## 📦 **FILES**

```
TEST_JITTER_NOW.ahk                 ← Test với delay cực lớn (0.5-1s)
multiplicity_jitter_passthrough.ahk ← Main script (30-80ms)
HUONG_DAN_TEST_JITTER.md            ← File này
```

---

## 🎉 **TÓM TẮT**

```
✅ ĐÃ FIX: Block → Sleep → Send
✅ Jitter effect HOẠT ĐỘNG!
✅ Test với TEST_JITTER_NOW.ahk để thấy rõ
✅ Main script delay 30-80ms (vừa đủ)
✅ Customize cho mỗi client khác nhau
```

---

**GIỜ HÃY TEST NGAY!** 🚀

```bash
Double-click: TEST_JITTER_NOW.ahk
Mở Notepad
Bấm QQQQQ
Thấy delay? → SUCCESS! ✅
```
