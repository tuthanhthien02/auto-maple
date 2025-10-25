# 📊 LAYER 1: VISUAL GUIDE - MULTIPLICITY WORKFLOW

## 🎯 **CONCEPT DIAGRAM**

### **Setup Architecture:**

```
                    ┌──────────────────────────────────┐
                    │      INTERNET / LAN NETWORK      │
                    └────────────┬─────────────────────┘
                                 │
                    ┌────────────▼─────────────┐
                    │    PRIMARY PC (Master)   │
                    │  ┌────────────────────┐  │
                    │  │  You sit here!     │  │
                    │  │  Press keys here   │  │
                    │  └────────────────────┘  │
                    │  ┌────────────────────┐  │
                    │  │  Multiplicity 4    │  │
                    │  │  (Broadcast Mode)  │  │
                    │  └────────────────────┘  │
                    │   IP: 192.168.1.100      │
                    └────────────┬─────────────┘
                                 │
                                 │ Broadcasts to all:
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        ▼                        ▼                        ▼
┌───────────────┐        ┌───────────────┐       ┌───────────────┐
│   CLIENT 1    │        │   CLIENT 2    │       │   CLIENT 3    │
│  ┌─────────┐  │        │  ┌─────────┐  │       │  ┌─────────┐  │
│  │MapleStory│  │        │  │MapleStory│  │       │  │MapleStory│  │
│  │  Char 1  │  │        │  │  Char 2  │  │       │  │  Char 3  │  │
│  └─────────┘  │        │  └─────────┘  │       │  └─────────┘  │
│  Multiplicity │        │  Multiplicity │       │  Multiplicity │
│   (Secondary) │        │   (Secondary) │       │   (Secondary) │
│ Connected ✅  │        │ Connected ✅  │       │ Connected ✅  │
└───────────────┘        └───────────────┘       └───────────────┘
```

---

## 🔄 **BROADCAST FLOW**

### **When you press Q on Primary:**

```
STEP 1: You press Q
   ▼
┌──────────────┐
│ PRIMARY PC   │  Press Q
│ (Your hands) │ ─────────┐
└──────────────┘           │
                           │
STEP 2: Multiplicity captures Q
                           ▼
                  ┌─────────────────┐
                  │  Multiplicity   │
                  │ Broadcast Mode  │
                  │   Q captured!   │
                  └─────────────────┘
                           │
STEP 3: Broadcast to all clients
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
    ┌───────┐          ┌───────┐         ┌───────┐
    │Client1│          │Client2│         │Client3│
    │   Q   │          │   Q   │         │   Q   │
    └───┬───┘          └───┬───┘         └───┬───┘
        │                  │                  │
STEP 4: MapleStory receives Q
        │                  │                  │
        ▼                  ▼                  ▼
    ┌───────┐          ┌───────┐         ┌───────┐
    │ Skill!│          │ Skill!│         │ Skill!│
    │  💥   │          │  💥   │         │  💥   │
    └───────┘          └───────┘         └───────┘

RESULT: All 3 characters use skill simultaneously! ✅
```

---

## ⏱️ **TIMING COMPARISON**

### **WITHOUT Multiplicity:**

```
You manually switch between 3 clients:

┌──────────┐  Switch  ┌──────────┐  Switch  ┌──────────┐
│ Client 1 │ ────────▶│ Client 2 │ ────────▶│ Client 3 │
│ Press Q  │    5s    │ Press Q  │    5s    │ Press Q  │
└──────────┘          └──────────┘          └──────────┘
   T=0s                  T=5s                  T=10s

Total time: 10 seconds for 1 action on all 3! ❌
```

### **WITH Multiplicity:**

```
Broadcast to all 3 simultaneously:

                      ┌──────────┐
                      │ Primary  │
                      │ Press Q  │
                      └────┬─────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
   ┌─────────┐        ┌─────────┐       ┌─────────┐
   │Client 1 │        │Client 2 │       │Client 3 │
   │ Press Q │        │ Press Q │       │ Press Q │
   └─────────┘        └─────────┘       └─────────┘
      T=0s               T=0s              T=0s

Total time: <0.1 seconds for all 3! ✅

Efficiency: 100x faster! 🚀
```

---

## 🎮 **SCREEN LAYOUT**

### **Grid View Setup:**

```
┌─────────────────────────────────────────────────────────────┐
│                    Mouse Movement Flow                       │
└─────────────────────────────────────────────────────────────┘

┌───────────┬───────────┬───────────┬───────────┐
│           │           │           │           │
│ PRIMARY   │ CLIENT 1  │ CLIENT 2  │ CLIENT 3  │
│           │           │           │           │
│ (Control) │ (Game 1)  │ (Game 2)  │ (Game 3)  │
│           │           │           │           │
│   🖱️───→ │   🖱️───→ │   🖱️───→ │   🖱️     │
│           │           │           │           │
└───────────┴───────────┴───────────┴───────────┘
     ▲                                     │
     │                                     │
     └─────────────────────────────────────┘
           Mouse wraps around (optional)

Move mouse RIGHT → Switch to next screen
Move mouse LEFT  → Switch to previous screen
```

---

## 🔑 **HOTKEY WORKFLOW**

### **Broadcast Toggle:**

```
┌─────────────────────────────────────────┐
│         Ctrl + Shift + B                │
│         (Toggle Broadcast)              │
└─────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
┌───────────────┐       ┌───────────────┐
│ BROADCAST ON  │       │ BROADCAST OFF │
│               │       │               │
│ All clients   │       │ Only active   │
│ receive input │       │ client gets   │
│               │       │ input         │
└───────────────┘       └───────────────┘
        │                       │
        │                       │
    ┌───┴───┬───────┬───────┐   │
    ▼       ▼       ▼       │   ▼
 Client1 Client2 Client3    │ Active
   💚      💚      💚       │ client
                            │   💚
                            │
                     Others ignored
                          ❌❌
```

---

## 🛠️ **SETUP SEQUENCE**

### **Visual Installation Flow:**

```
START
  │
  ▼
┌────────────────────────┐
│ 1. Install on PRIMARY  │  ← Choose "Primary Computer"
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│ 2. Get Primary IP      │  ← Note: 192.168.1.100
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│ 3. Enable Firewall     │  ← Allow Multiplicity.exe
└───────────┬────────────┘
            │
            ├──────────────────┬─────────────────┐
            │                  │                 │
            ▼                  ▼                 ▼
  ┌──────────────────┐ ┌──────────────┐ ┌──────────────┐
  │4a. Install       │ │4b. Install   │ │4c. Install   │
  │    CLIENT 1      │ │    CLIENT 2  │ │    CLIENT 3  │
  │                  │ │              │ │              │
  │Choose Secondary  │ │Choose Sec.   │ │Choose Sec.   │
  └────────┬─────────┘ └──────┬───────┘ └──────┬───────┘
           │                  │                 │
           ▼                  ▼                 ▼
  ┌──────────────────┐ ┌──────────────┐ ┌──────────────┐
  │5a. Connect to    │ │5b. Connect   │ │5c. Connect   │
  │    Primary IP    │ │    to IP     │ │    to IP     │
  │  192.168.1.100   │ │ 192.168.1.100│ │192.168.1.100 │
  └────────┬─────────┘ └──────┬───────┘ └──────┬───────┘
           │                  │                 │
           └──────────────────┴─────────────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ 6. Enable         │
                    │    Broadcast      │
                    │    on Primary     │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ 7. TEST!          │
                    │    Press Q        │
                    │    All receive? ✅│
                    └─────────┬─────────┘
                              │
                              ▼
                           SUCCESS! 🎉
```

---

## 📡 **NETWORK TOPOLOGY**

### **Same LAN (Recommended):**

```
                 ┌─────────────┐
                 │   Router    │
                 │ (WiFi/LAN)  │
                 └──────┬──────┘
                        │
        ┌───────────────┼───────────────┬──────────────┐
        │               │               │              │
        ▼               ▼               ▼              ▼
    ┌───────┐      ┌────────┐     ┌────────┐    ┌────────┐
    │Primary│      │Client 1│     │Client 2│    │Client 3│
    │  .100 │      │  .101  │     │  .102  │    │  .103  │
    └───────┘      └────────┘     └────────┘    └────────┘

Latency: <5ms ✅
Recommended! ⭐
```

### **Over Internet (Possible but laggy):**

```
┌─────────┐         Internet         ┌─────────┐
│ Primary │────────────┬──────────────│ Client 1│
│Home WiFi│            │              │Other ISP│
└─────────┘            │              └─────────┘
                       │
                       ├──────────────┌─────────┐
                       │              │ Client 2│
                       │              │Other ISP│
                       │              └─────────┘
                       │
                       └──────────────┌─────────┐
                                      │ Client 3│
                                      │Other ISP│
                                      └─────────┘

Latency: 50-200ms ⚠️
Use VPN for security!
```

---

## 🎯 **DETECTION COMPARISON**

### **Before Obfuscation:**

```
Task Manager on Client PC:

┌──────────────────────────────────────┐
│ Name              CPU    Memory       │
├──────────────────────────────────────┤
│ MapleStory.exe    25%    1.2 GB       │
│ Multiplicity.exe  2%     50 MB   ⚠️  │ ← DETECTED!
│ explorer.exe      1%     100 MB       │
└──────────────────────────────────────┘

Anti-cheat: "Multiplicity.exe detected! BAN!" ❌
```

### **After Obfuscation:**

```
Task Manager on Client PC:

┌──────────────────────────────────────┐
│ Name                    CPU    Memory │
├──────────────────────────────────────┤
│ MapleStory.exe          25%    1.2 GB │
│ SystemAudioService.exe  2%     50 MB  │ ← Looks legit!
│ explorer.exe            1%     100 MB │
└──────────────────────────────────────┘

Anti-cheat: "SystemAudioService.exe = Windows service, OK" ✅
```

---

## ⚡ **PERFORMANCE METRICS**

### **Expected Latency:**

```
Input Delay (Primary → Clients):

Same LAN:         5-10ms    ✅ Excellent
LAN (WiFi):      10-30ms    ✅ Good
Internet (VPN):  50-100ms   ⚠️ Playable
Internet (far): 100-200ms   ❌ Laggy

Target: < 50ms for smooth gameplay
```

### **Resource Usage:**

```
Primary PC:
  Multiplicity: ~50 MB RAM, 1-2% CPU ✅ Light

Each Client PC:
  Multiplicity: ~30 MB RAM, 1% CPU ✅ Very light
  MapleStory:   ~1-2 GB RAM, 20-30% CPU

Total overhead: Minimal! 🚀
```

---

## 🎉 **SUCCESS INDICATORS**

### **✅ Working Correctly:**

```
Visual Check:

Primary PC:
  ┌──────────────────────┐
  │ Multiplicity         │
  │ Status: Broadcasting │ ← Good!
  │ Targets: 3 clients   │ ← Good!
  │ Latency: 15ms avg    │ ← Good!
  └──────────────────────┘

Client 1:
  ┌──────────────────────┐
  │ Multiplicity         │
  │ Status: Connected 💚 │ ← Good!
  │ Primary: 192.168.1.100│
  └──────────────────────┘

Client 2: Same as Client 1 ✅
Client 3: Same as Client 1 ✅
```

### **❌ Not Working:**

```
Common Issues:

Client shows:
  ┌──────────────────────┐
  │ Multiplicity         │
  │ Status: Disconnected │ ← Bad!
  │ Error: Cannot reach  │ ← Fix firewall
  └──────────────────────┘

Or:
  ┌──────────────────────┐
  │ Broadcast: OFF       │ ← Bad!
  │ Targets: 0 selected  │ ← Select clients!
  └──────────────────────┘
```

---

## 🏁 **FINAL RESULT**

### **What You Achieve:**

```
BEFORE:                      AFTER Layer 1:

You: Click, click, click     You: Click once
     Switch, click                ↓
     Switch, click           All 3: Action! ✅
     ❌ Tedious
     ❌ Slow (10s)           ✅ Fast (<0.1s)
     ❌ Only 1 char          ✅ All 3 chars
                             ✅ 100x efficiency!
```

---

**Ready to start? Follow `LAYER_1_HUONG_DAN_NHANH.md`!** 🚀✨


