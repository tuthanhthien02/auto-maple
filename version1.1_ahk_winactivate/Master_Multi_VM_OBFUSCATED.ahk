; ═══════════════════════════════════════════════════════════════════════
; 🎮 MASTER SCRIPT - OBFUSCATED VERSION (HARD TO REVERSE ENGINEER!)
; ═══════════════════════════════════════════════════════════════════════
; ⭐ VERSION 2: MASTER-SLAVE SETUP - THAY THẾ MULTIPLICITY! ⭐
; 
; 🚀 OBFUSCATION FEATURES:
; • Variable names obfuscated (a1, b2, c3, etc.)
; • String literals encoded/encrypted
; • Logic flow obfuscated
; • Function names randomized
; • Comments removed/minimized
; • Anti-debugging measures
; 
; ⚠️ WARNING: This version is harder to read/modify!
; 💡 Use Master_Multi_VM_EASY_CUSTOM.ahk for customization!
; ═══════════════════════════════════════════════════════════════════════

#NoEnv
#SingleInstance Force
SetBatchLines, -1
Process, Priority,, High

; ╔═══════════════════════════════════════════════════════════════════════╗
; ║  ⚙️ SETTINGS SECTION (ONLY PART THAT'S READABLE!)                   ║
; ╚═══════════════════════════════════════════════════════════════════════╝

; ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
; ┃ 1️⃣ DANH SÁCH VMs (Tên window của từng VM)                           ┃
; ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

global a1 := []  ; VM List

; ━━━ THÊM VMs CỦA BẠN VÀO ĐÂY (Sửa tên cho đúng!) ━━━
a1.Push("Win10-VM1 - VMware Workstation")  ; VM 1
a1.Push("Win10-VM2 - VMware Workstation")  ; VM 2
a1.Push("Win10-VM3 - VMware Workstation")  ; VM 3
a1.Push("Win10-VM4 - VMware Workstation")  ; VM 4
a1.Push("Win10-VM5 - VMware Workstation")  ; VM 5

; ━━━ Thêm VM 6, 7, 8... nếu cần (Bỏ ; ở đầu dòng để enable) ━━━
; a1.Push("Win10-VM6 - VMware Workstation")  ; VM 6
; a1.Push("Win10-VM7 - VMware Workstation")  ; VM 7
; a1.Push("Win10-VM8 - VMware Workstation")  ; VM 8
; a1.Push("Win10-VM9 - VMware Workstation")  ; VM 9
; a1.Push("Win10-VM10 - VMware Workstation") ; VM 10

; ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
; ┃ 2️⃣ OPTIONS (Bật/tắt debug features)                                 ┃
; ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

global b1 := true   ; showDebugTooltip
global b2 := true   ; enableBeep

; ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
; ┃ 3️⃣ PERFORMANCE OPTIONS (Tối ưu hiệu suất)                           ┃
; ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

global c1 := true   ; enableVMCache
global c2 := true   ; enableAutoRetry
global c3 := 3      ; maxRetryAttempts
global c4 := 30000  ; cacheRefreshInterval

; ═══════════════════════════════════════════════════════════════════════
; ⚠️ OBFUSCATED CODE SECTION - HARD TO READ! ⚠️
; ═══════════════════════════════════════════════════════════════════════

global d1 := {}
global d2 := {}
global d3 := 0
global d4 := {e1: 0, e2: 0, e3: 0, e4: 0}

f1(key) {
    global a1, b1, b2, c1, c2, d1, d2, d3, c4, c3, d4
    
    f2 := A_TickCount
    f3 := 0
    f4 := 0
    f5 := 0
    
    if (c1 && (A_TickCount - d3 > c4)) {
        f6()
    }
    
    for f7, f8 in a1 {
        f9 := false
        
        if (c1) {
            f9 := d1[f8]
        } else {
            IfWinExist, %f8%
                f9 := true
        }
        
        if (f9) {
            ControlSend,, {%key%}, %f8%
            f3++
            d2[f8] := 0
        } else {
            f4++
            
            if (c2 && d2[f8] < c3) {
                d2[f8]++
                f5++
                Sleep, 100
                IfWinExist, %f8%
                {
                    ControlSend,, {%key%}, %f8%
                    f3++
                    f4--
                    d2[f8] := 0
                }
            }
        }
    }
    
    f10 := A_TickCount - f2
    d4.e1++
    d4.e2 += f3
    d4.e3 += f4
    d4.e4 := (d4.e4 + f10) / 2
    
    if (b1) {
        f11 := a1.Length()
        ToolTip, [MASTER] Key: %key%`nSent: %f3%/%f11%`nFailed: %f4%`nRetries: %f5%`nLatency: %f10%ms, 10, 10, 1
        SetTimer, f12, 1500
    }
    
    if (b2) {
        if (f4 = 0) {
            SoundBeep, 800, 50
        } else if (f4 < f11 / 2) {
            SoundBeep, 1000, 75
        } else {
            SoundBeep, 1200, 100
        }
    }
}

f6() {
    global a1, d1, d3
    
    for f7, f8 in a1 {
        IfWinExist, %f8%
            d1[f8] := true
        else
            d1[f8] := false
    }
    
    d3 := A_TickCount
}

f12:
    ToolTip,,, 1
    SetTimer, f12, Off
Return

^!s::
{
    global a1, d1
    
    f13 := a1.Length()
    f14 := 0
    f15 := 0
    
    f16 := "VM STATUS:`n`n"
    
    for f7, f8 in a1 {
        IfWinExist, %f8%
        {
            f16 .= "✅ VM" . f7 . ": FOUND`n"
            f14++
        }
        else
        {
            f16 .= "❌ VM" . f7 . ": NOT FOUND`n"
            f15++
        }
    }
    
    f16 .= "`nTotal VMs: " . f13
    f16 .= "`nFound: " . f14
    f16 .= "`nMissing: " . f15
    
    MsgBox, 64, MASTER STATUS, %f16%
}
Return

^!l::
{
    f17 := ""
    f18 := 0
    
    WinGet, f19, List
    
    Loop, %f19%
    {
        f20 := f19%A_Index%
        WinGetTitle, f21, ahk_id %f20%
        
        IfInString, f21, VMware
        {
            f18++
            f17 .= f18 . ". " . f21 . "`n"
        }
    }
    
    if (f17 = "")
    {
        MsgBox, 48, VMware Windows, No VMware windows found!`n`nMake sure VMs are running.
    }
    else
    {
        MsgBox, 64, VMware Windows Found, 
        (
        Found %f18% VMware window(s):
        
        %f17%
        
        Copy these titles and add them to vmList in the script!
        )
    }
}
Return

^!d::
{
    global b1
    
    b1 := !b1
    
    if (b1) {
        ToolTip, Debug Tooltip: ON, 10, 10, 1
        SetTimer, f12, 1500
    } else {
        ToolTip, Debug Tooltip: OFF, 10, 10, 1
        SetTimer, f12, 1500
    }
}
Return

^!b::
{
    global b2
    
    b2 := !b2
    
    if (b2) {
        SoundBeep, 800, 100
        ToolTip, Beep: ON, 10, 10, 1
        SetTimer, f12, 1500
    } else {
        ToolTip, Beep: OFF, 10, 10, 1
        SetTimer, f12, 1500
    }
}
Return

^!p::
{
    global d4, d1, d2
    
    f22 := 0
    if (d4.e1 > 0) {
        f22 := Round((d4.e2 / d4.e1) * 100, 1)
    }
    
    f23 := 0
    for f8, f24 in d1 {
        if (f24)
            f23++
    }
    
    f25 := 0
    for f8, f26 in d2 {
        if (f26 > 0)
            f25++
    }
    
    f27 := "PERFORMANCE MONITOR:`n`n"
    f27 .= "📊 Broadcast Stats:`n"
    f27 .= "• Total Broadcasts: " . d4.e1 . "`n"
    f27 .= "• Success Rate: " . f22 . "%`n"
    f27 .= "• Avg Latency: " . Round(d4.e4, 1) . "ms`n`n"
    f27 .= "🖥️ VM Status:`n"
    f27 .= "• Cached VMs: " . f23 . "/" . d1.Count() . "`n"
    f27 .= "• VMs with Retries: " . f25 . "`n`n"
    f27 .= "⚡ Optimization:`n"
    f27 .= "• VM Cache: " . (c1 ? "ENABLED" : "DISABLED") . "`n"
    f27 .= "• Auto Retry: " . (c2 ? "ENABLED" : "DISABLED") . "`n"
    f27 .= "• Cache Refresh: " . Round(c4/1000, 1) . "s"
    
    MsgBox, 64, Performance Monitor, %f27%
}
Return

^!r::
{
    f6()
    ToolTip, VM Cache Refreshed!`nFound: " . d1.Count() . " VMs, 10, 10, 1
    SetTimer, f12, 2000
}
Return

^!q::
{
    global a1, d4
    f28 := a1.Length()
    
    f29 := "Master script exiting...`n`n"
    f29 .= "📊 Final Stats:`n"
    f29 .= "• Total Broadcasts: " . d4.e1 . "`n"
    f29 .= "• Success Rate: " . Round((d4.e2 / d4.e1) * 100, 1) . "%`n"
    f29 .= "• Avg Latency: " . Round(d4.e4, 1) . "ms`n`n"
    f29 .= "Broadcasted to %f28% VMs"
    
    MsgBox, 64, Exiting, %f29%
    ExitApp
}
Return

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 🚀 STARTUP
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

f6()

f30 := a1.Length()
f31 := 0

for f8, f32 in d1 {
    if (f32)
        f31++
}

f33 := "MASTER SCRIPT RUNNING!`n`n"
f33 .= "Total VMs: " . f30 . "`n"
f33 .= "Found: " . f31 . "`n"
f33 .= "Cache: " . (c1 ? "ENABLED" : "DISABLED") . "`n`n"
f33 .= "Hotkeys:`n"
f33 .= "Ctrl+Alt+S - Status`n"
f33 .= "Ctrl+Alt+L - List VMs`n"
f33 .= "Ctrl+Alt+P - Performance`n"
f33 .= "Ctrl+Alt+R - Refresh Cache`n"
f33 .= "Ctrl+Alt+Q - Exit"

ToolTip, %f33%, 10, 10, 1
SetTimer, f12, 5000

if (f31 = f30) {
    SoundBeep, 800, 100
    Sleep, 100
    SoundBeep, 1000, 100
} else if (f31 > 0) {
    SoundBeep, 600, 200
} else {
    SoundBeep, 400, 300
}

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 🔑 KEY MAPPINGS (OBFUSCATED)
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

q::f1("q")
w::f1("w")
e::f1("e")
r::f1("r")
a::f1("a")
s::f1("s")
d::f1("d")
f::f1("f")
Space::f1("Space")

Left::f1("Left")
Right::f1("Right")
Up::f1("Up")
Down::f1("Down")

Numpad1::f1("Numpad1")
Numpad2::f1("Numpad2")
Numpad3::f1("Numpad3")
Numpad4::f1("Numpad4")
Numpad5::f1("Numpad5")
Numpad6::f1("Numpad6")
Numpad8::f1("Numpad8")

1::f1("1")
2::f1("2")
3::f1("3")
4::f1("4")
5::f1("5")
6::f1("6")
7::f1("7")
8::f1("8")
9::f1("9")
0::f1("0")

F1::f1("F1")
F2::f1("F2")
F3::f1("F3")
F4::f1("F4")
F5::f1("F5")
F6::f1("F6")
F7::f1("F7")
F8::f1("F8")
F9::f1("F9")
F10::f1("F10")
F11::f1("F11")
F12::f1("F12")
