; ═══════════════════════════════════════════════════════════
; JITTER + HOLD SUPPORT: For use WITH PowerToys Key Remapping
; ═══════════════════════════════════════════════════════════
; FEATURES:
; ✅ Single press for skills (Q, W, E, R, etc.)
; ✅ Hold down support for movement (Arrow keys, WASD)
; ✅ Jitter on key DOWN only (not on auto-repeat)
; ✅ Passthrough hold state to game
; ═══════════════════════════════════════════════════════════

#SingleInstance Force
#NoEnv
SetWorkingDir %A_ScriptDir%
Random, Seed, A_TickCount

; ════════════════════════════════════════════════════════════
; ⚙️ CONFIGURATION - CUSTOMIZE FOR EACH CLIENT
; ════════════════════════════════════════════════════════════

; CLIENT 1: Fast jitter (30-80ms)
global MinJitter := 30
global MaxJitter := 80

; CLIENT 2: Medium jitter (60-120ms) 
; global MinJitter := 60
; global MaxJitter := 120

; CLIENT 3: Slow jitter (90-150ms)
; global MinJitter := 90
; global MaxJitter := 150

global UseGaussian := true

; ════════════════════════════════════════════════════════════
; 🎯 KEY TRACKING (Prevent jitter on auto-repeat)
; ════════════════════════════════════════════════════════════
global KeyIsDown := {}

; ════════════════════════════════════════════════════════════
; 🎮 ACTIVE ONLY IN MAPLESTORY
; ════════════════════════════════════════════════════════════
#IfWinActive, MapleStory

; ════════════════════════════════════════════════════════════
; ⌨️ MOVEMENT KEYS (HOLD SUPPORT) ⭐
; ════════════════════════════════════════════════════════════
; Arrow keys - support holding for continuous movement
Left::
    key := A_ThisHotkey
    ApplyJitterAndHold(key)
    return

Right::
    key := A_ThisHotkey
    ApplyJitterAndHold(key)
    return

Up::
    key := A_ThisHotkey
    ApplyJitterAndHold(key)
    return

Down::
    key := A_ThisHotkey
    ApplyJitterAndHold(key)
    return

; WASD movement (if game uses WASD)
w::
    key := A_ThisHotkey
    ApplyJitterAndHold(key)
    return

a::
    key := A_ThisHotkey
    ApplyJitterAndHold(key)
    return

s::
    key := A_ThisHotkey
    ApplyJitterAndHold(key)
    return

d::
    key := A_ThisHotkey
    ApplyJitterAndHold(key)
    return

; ════════════════════════════════════════════════════════════
; ⚔️ SKILL KEYS (SINGLE PRESS) ⭐
; ════════════════════════════════════════════════════════════
; Letter keys (excluding movement WASD)
b:: c:: e:: f:: g:: h:: i:: j:: k:: l:: m::
n:: o:: p:: q:: r:: t:: u:: v:: x:: y:: z::
    key := A_ThisHotkey
    ApplyJitterSinglePress(key)
    return

; Number keys (0-9) - potions, buffs
0:: 1:: 2:: 3:: 4:: 5:: 6:: 7:: 8:: 9::
    key := A_ThisHotkey
    ApplyJitterSinglePress(key)
    return

; Function keys (F1-F12) - buffs
F1:: F2:: F3:: F4:: F5:: F6:: F7:: F8:: F9:: F10:: F11:: F12::
    key := A_ThisHotkey
    ApplyJitterSinglePress(key)
    return

; Modifier keys
Alt:: Space:: Ctrl:: Shift:: Tab::
    key := A_ThisHotkey
    ApplyJitterSinglePress(key)
    return

; Special keys
Enter:: Backspace:: Delete:: Insert:: Home:: End:: PgUp:: PgDn:: Esc::
    key := A_ThisHotkey
    ApplyJitterSinglePress(key)
    return

; Numpad keys
Numpad0:: Numpad1:: Numpad2:: Numpad3:: Numpad4:: Numpad5:: Numpad6:: Numpad7:: Numpad8:: Numpad9::
NumpadAdd:: NumpadSub:: NumpadMult:: NumpadDiv:: NumpadEnter:: NumpadDot::
    key := A_ThisHotkey
    ApplyJitterSinglePress(key)
    return

; Symbol keys
`;:: ':: ,:: .:: /:: [:: ]:: \:: -:: =::
    key := A_ThisHotkey
    ApplyJitterSinglePress(key)
    return

#IfWinActive

; ════════════════════════════════════════════════════════════
; 🔧 CORE FUNCTIONS
; ════════════════════════════════════════════════════════════

; ============ HOLD SUPPORT (For movement keys) ============
ApplyJitterAndHold(key) {
    global MinJitter, MaxJitter, UseGaussian, KeyIsDown
    
    ; Check if this is the FIRST press or auto-repeat
    if (!KeyIsDown[key]) {
        ; FIRST PRESS - Apply jitter
        KeyIsDown[key] := true
        
        ; Calculate jitter
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
        
        ; Apply jitter delay
        Sleep, %jitter%
        
        ; Send key DOWN (start holding)
        Send {%key% down}
        
        ; Wait for key to be released
        KeyWait, %key%
        
        ; Key released - send UP
        Send {%key% up}
        KeyIsDown[key] := false
    }
    ; If auto-repeat, ignore (key is already held down)
}

; ============ SINGLE PRESS (For skill keys) ============
ApplyJitterSinglePress(key) {
    global MinJitter, MaxJitter, UseGaussian
    
    ; Calculate jitter
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
    
    ; Apply jitter delay
    Sleep, %jitter%
    
    ; Send single press
    Send {%key%}
}

; ============ GAUSSIAN RANDOM ============
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

