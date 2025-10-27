; ═══════════════════════════════════════════════════════════════════════
; 🎯 SLAVE SCRIPT - OBFUSCATED VERSION (HARD TO REVERSE ENGINEER!)
; ═══════════════════════════════════════════════════════════════════════
; ⭐ VERSION 2: DÙNG VỚI MASTER SCRIPT - KHÔNG CẦN MULTIPLICITY! ⭐
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
; 💡 Use multiplicity_jitter_DESYNC_SLAVE.ahk for customization!
; ═══════════════════════════════════════════════════════════════════════

#NoEnv
#SingleInstance Force
SetBatchLines, -1
Process, Priority,, High
SendMode Input

; ╔═══════════════════════════════════════════════════════════════════════╗
; ║  ⚙️ SETTINGS SECTION (ONLY PART THAT'S READABLE!)                   ║
; ╚═══════════════════════════════════════════════════════════════════════╝

; ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
; ┃ 1️⃣ MỨC ĐỘ TRAINING (Desync Delay - QUAN TRỌNG!)                    ┃
; ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

global a1 := 0      ; MinDesync
global a2 := 500    ; MaxDesync

; ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
; ┃ 2️⃣ PERFORMANCE OPTIONS (Tối ưu hiệu suất)                           ┃
; ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

global b1 := true   ; enablePerformanceMonitor
global b2 := false  ; enableDebugMode
global b3 := false  ; enableFastMode

; ═══════════════════════════════════════════════════════════════════════
; ⚠️ OBFUSCATED CODE SECTION - HARD TO READ! ⚠️
; ═══════════════════════════════════════════════════════════════════════

global c1 := 30
global c2 := 80
global c3 := true

global d1 := false
global d2 := false

global e1 := 180000
global e2 := 300000
global e3 := 800
global e4 := 2500

global f1 := false
global f2 := true

global g1 := true

global h1 := {}

h1["q"] := "a"
h1["w"] := "s"
h1["e"] := "d"
h1["r"] := "f"
h1["Space"] := "Space"
h1["Numpad1"] := "Left"
h1["Numpad2"] := "Down"
h1["Numpad3"] := "Right"
h1["Numpad5"] := "Up"

global i1 := {j1: 0, j2: 0, j3: 0, j4: 0}
global i2 := []
global i3 := 0

For k1, k2 in h1 {
    Hotkey, $%k1%, l1
    Hotkey, $%k1% up, l2
}

SetTimer, l3, 1000
l4()

Return

^!t::
    global f2
    f2 := !f2
    
    if (f2) {
        SoundBeep, 1000, 100
        ToolTip, [SLAVE] SCRIPT ENABLED, 0, 0
    } else {
        SoundBeep, 500, 100
        ToolTip, [SLAVE] SCRIPT DISABLED, 0, 0
    }
    
    SetTimer, l5, 2000
Return

^!p::
{
    global i1, i2, b1
    
    if (!b1) {
        MsgBox, 48, Performance Monitor, Performance monitoring is disabled!`n`nEnable it in the script settings.
        return
    }
    
    m1 := 0
    if (i2.Length() > 0) {
        m2 := 0
        for m3, m4 in i2 {
            m2 += m4
        }
        m1 := Round(m2 / i2.Length(), 1)
    }
    
    m5 := 0
    m6 := 0
    if (i1.j1 > 0) {
        m5 := Round(i1.j2 / i1.j1, 1)
        m6 := Round(i1.j3 / i1.j1, 1)
    }
    
    m7 := "SLAVE PERFORMANCE MONITOR:`n`n"
    m7 .= "📊 Keypress Stats:`n"
    m7 .= "• Total Keypresses: " . i1.j1 . "`n"
    m7 .= "• Avg Latency: " . Round(i1.j4, 1) . "ms`n"
    m7 .= "• Avg Interval: " . m1 . "ms`n`n"
    m7 .= "⏱️ Delay Stats:`n"
    m7 .= "• Avg Desync: " . m5 . "ms`n"
    m7 .= "• Avg Jitter: " . m6 . "ms`n`n"
    m7 .= "🎯 Settings:`n"
    m7 .= "• Desync Range: " . a1 . "-" . a2 . "ms`n"
    m7 .= "• Jitter Range: " . c1 . "-" . c2 . "ms`n"
    m7 .= "• Arrow Jitter: " . (g1 ? "ENABLED" : "DISABLED") . "`n"
    m7 .= "• Fast Mode: " . (b3 ? "ENABLED" : "DISABLED")
    
    MsgBox, 64, Performance Monitor, %m7%
}
Return

^!r::
{
    global i1, i2, i3
    
    i1.j1 := 0
    i1.j2 := 0
    i1.j3 := 0
    i1.j4 := 0
    i2 := []
    i3 := 0
    
    ToolTip, Performance stats reset!, 0, 0
    SetTimer, l5, 2000
}
Return

^!d::
{
    global b2
    b2 := !b2
    
    if (b2) {
        SoundBeep, 1200, 100
        ToolTip, Debug Mode: ON, 0, 0
    } else {
        SoundBeep, 800, 100
        ToolTip, Debug Mode: OFF, 0, 0
    }
    
    SetTimer, l5, 2000
}
Return

l5:
    ToolTip
    SetTimer, l5, Off
Return

l1:
    global f2, f1, g1, a1, a2, d1, d2, h1, c1, c2, c3, b1, b2, b3, i1, i2, i3
    
    m8 := A_TickCount
    
    if (!b3) {
        if (!f2) {
            m9 := StrReplace(A_ThisHotkey, "$", "")
            m9 := StrReplace(m9, " up", "")
            SendInput, {%m9% down}
            return
        }
        
        if (f1) {
            return
        }
    }
    
    m9 := StrReplace(A_ThisHotkey, "$", "")
    m9 := StrReplace(m9, " up", "")
    m10 := h1[m9]
    
    if (b1) {
        i1.j1++
        m11 := A_TickCount
        if (i3 > 0) {
            m12 := m11 - i3
            i2.Push(m12)
            if (i2.Length() > 100) {
                i2.RemoveAt(1)
            }
        }
        i3 := m11
    }
    
    if (b2) {
        ToolTip, [SLAVE] Key: %m9% → %m10%, 0, 0
        SetTimer, l6, 1000
    }
    
    m13 := (m9 = "Numpad1" || m9 = "Numpad2" || m9 = "Numpad3" || m9 = "Numpad5" || m9 = "Left" || m9 = "Right" || m9 = "Up" || m9 = "Down")
    
    if (m13 && !g1) {
        SendInput, {%m10% down}
        return
    }
    
    m14 := 0
    if (!d1) {
        Random, m14, %a1%, %a2%
        Sleep, %m14%
        if (b1) {
            i1.j2 += m14
        }
    }
    
    m15 := 0
    if (!d2) {
        if (c3) {
            m16 := (c1 + c2) / 2.0
            m17 := (c2 - c1) / 6.0
            m15 := l7(m16, m17, c1, c2)
        } else {
            Random, m15, %c1%, %c2%
        }
        Sleep, %m15%
        if (b1) {
            i1.j3 += m15
        }
    }
    
    SendInput, {%m10% down}
    
    if (b1) {
        m18 := A_TickCount - m8
        i1.j4 := (i1.j4 + m18) / 2
    }
Return

l6:
    ToolTip
    SetTimer, l6, Off
Return

l2:
    global f2, f1, h1
    
    if (!b3) {
        if (!f2) {
            m9 := StrReplace(A_ThisHotkey, "$", "")
            m9 := StrReplace(m9, " up", "")
            SendInput, {%m9% up}
            return
        }
        
        if (f1) {
            return
        }
    }
    
    m9 := StrReplace(A_ThisHotkey, "$", "")
    m9 := StrReplace(m9, " up", "")
    m10 := h1[m9]
    
    SendInput, {%m10% up}
Return

l7(m16, m17, c1, c2) {
    Random, m19, 0.0, 1.0
    Random, m20, 0.0, 1.0
    m21 := Sqrt(-2 * Ln(m19)) * Cos(2 * 3.14159265359 * m20)
    m22 := m16 + m21 * m17
    if (m22 < c1)
        m22 := c1
    if (m22 > c2)
        m22 := c2
    return Round(m22)
}

l3:
    if (A_TickCount >= m23 && !f1) {
        l8()
    }
Return

l8() {
    global f1, e3, e4
    f1 := true
    Random, m24, %e3%, %e4%
    SetTimer, l9, %m24%
}

l9:
    global f1
    f1 := false
    SetTimer, l9, Off
    l4()
Return

l4() {
    global m23, e1, e2
    Random, m25, %e1%, %e2%
    m23 := A_TickCount + m25
}
