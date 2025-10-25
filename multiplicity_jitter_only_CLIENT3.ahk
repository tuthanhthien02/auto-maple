; ═══════════════════════════════════════════════════════════
; CLIENT 3 - Jitter-Only (Slow) + PowerToys Remap
; ═══════════════════════════════════════════════════════════
; Jitter: 90-150ms (slowest)
; Remap: Handled by PowerToys (driver-level)
; ═══════════════════════════════════════════════════════════

#SingleInstance Force
#NoEnv
SetWorkingDir %A_ScriptDir%
Random, Seed, A_TickCount

; ════════════════════════════════════════════════════════════
; ⚙️ CLIENT 3 CONFIGURATION
; ════════════════════════════════════════════════════════════

global MinJitter := 90
global MaxJitter := 150
global UseGaussian := true

; ════════════════════════════════════════════════════════════
; 🎮 ACTIVE ONLY IN MAPLESTORY
; ════════════════════════════════════════════════════════════
#IfWinActive, MapleStory

; Letter keys (A-Z)
a:: b:: c:: d:: e:: f:: g:: h:: i:: j:: k:: l:: m::
n:: o:: p:: q:: r:: s:: t:: u:: v:: w:: x:: y:: z::
    key := A_ThisHotkey
    ApplyJitterPassthrough(key)
    return

; Number keys (0-9)
0:: 1:: 2:: 3:: 4:: 5:: 6:: 7:: 8:: 9::
    key := A_ThisHotkey
    ApplyJitterPassthrough(key)
    return

; Function keys (F1-F12)
F1:: F2:: F3:: F4:: F5:: F6:: F7:: F8:: F9:: F10:: F11:: F12::
    key := A_ThisHotkey
    ApplyJitterPassthrough(key)
    return

; Arrow keys
Left:: Right:: Up:: Down::
    key := A_ThisHotkey
    ApplyJitterPassthrough(key)
    return

; Modifier keys
Alt:: Space:: Ctrl:: Shift:: Tab:: CapsLock::
    key := A_ThisHotkey
    ApplyJitterPassthrough(key)
    return

; Special keys
Enter:: Backspace:: Delete:: Insert:: Home:: End:: PgUp:: PgDn:: Esc::
    key := A_ThisHotkey
    ApplyJitterPassthrough(key)
    return

; Numpad keys
Numpad0:: Numpad1:: Numpad2:: Numpad3:: Numpad4:: Numpad5:: Numpad6:: Numpad7:: Numpad8:: Numpad9::
NumpadAdd:: NumpadSub:: NumpadMult:: NumpadDiv:: NumpadEnter:: NumpadDot::
    key := A_ThisHotkey
    ApplyJitterPassthrough(key)
    return

; Symbol keys
`;:: ':: ,:: .:: /:: [:: ]:: \:: -:: =::
    key := A_ThisHotkey
    ApplyJitterPassthrough(key)
    return

#IfWinActive

; ════════════════════════════════════════════════════════════
; 🔧 CORE FUNCTIONS
; ════════════════════════════════════════════════════════════

ApplyJitterPassthrough(key) {
    global MinJitter, MaxJitter, UseGaussian
    
    if (UseGaussian) {
        mean := (MinJitter + MaxJitter) / 2
        stddev := (MaxJitter - MinJitter) / 4
        jitter := GaussianRandom(mean, stddev)
        
        if (jitter < MinJitter)
            jitter := MinJitter
        if (jitter > MaxJitter)
            jitter := MaxJitter
    } else {
        Random, jitter, %MinJitter%, %MaxJitter%
    }
    
    Sleep, %jitter%
    Send {%key%}
}

GaussianRandom(mean, stddev) {
    Random, u1, 0.0, 1.0
    Random, u2, 0.0, 1.0
    
    if (u1 = 0)
        u1 := 0.0001
    
    pi := 3.14159265359
    z := Sqrt(-2 * Ln(u1)) * Cos(2 * pi * u2)
    
    result := Round(mean + stddev * z)
    return result
}

