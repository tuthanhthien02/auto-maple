; ═══════════════════════════════════════════════════════════
; MULTIPLICITY JITTER - VM1 (FAST)
; ═══════════════════════════════════════════════════════════
; NO POWERTOYS NEEDED! AHK does remap + jitter!
; 
; Host sends Q → VM receives Q → AHK blocks Q → Jitter → Send P
; 
; IN-GAME KEYBINDINGS (VM1):
;   Skill 1: P (host presses Q)
;   Skill 2: [ (host presses W)
;   Skill 3: ] (host presses E)
;   Skill 4: \ (host presses R)
;   etc.
;
; Jitter: 30-80ms (Gaussian)
; AUTO-ELEVATES TO ADMIN RIGHTS
; ═══════════════════════════════════════════════════════════

#SingleInstance Force
#NoEnv
SetWorkingDir %A_ScriptDir%
Random, Seed, A_TickCount
#MaxHotkeysPerInterval 200

; 🔒 AUTO-ELEVATE TO ADMIN
if not A_IsAdmin
{
    Run *RunAs "%A_ScriptFullPath%"
    ExitApp
}

; ⚙️ VM1 CONFIGURATION (FAST)
global MinJitter := 30
global MaxJitter := 80
global UseGaussian := true

MsgBox, 
(
✅ VM1 - FAST JITTER (NO POWERTOYS!)
Running as Administrator

Jitter: 30-80ms (Gaussian)

IMPORTANT:
  - Host sends Q, W, E, R...
  - VM1 converts: Q→P, W→[, E→], R→\
  - In-game keybindings MUST match!
  
IN-GAME SETUP:
  Skill 1 → P (host Q)
  Skill 2 → [ (host W)
  Skill 3 → ] (host E)
  Skill 4 → \ (host R)
  Skill 5 → - (host T)
  Skill 6 → = (host Y)

Press CTRL+SHIFT+Q to exit
)

; ════════════════════════════════════════════════════════════
; 🎯 GAME KEYS - VM1 MAPPING
; ════════════════════════════════════════════════════════════
; Host Q → VM1 sends P
q::
    ApplyJitterAndSend("p")
    return

; Host W → VM1 sends [
w::
    ApplyJitterAndSend("[")
    return

; Host E → VM1 sends ]
e::
    ApplyJitterAndSend("]")
    return

; Host R → VM1 sends \
r::
    ApplyJitterAndSend("\")
    return

; Host T → VM1 sends -
t::
    ApplyJitterAndSend("-")
    return

; Host Y → VM1 sends =
y::
    ApplyJitterAndSend("=")
    return

; Host U → VM1 sends F10
u::
    ApplyJitterAndSend("F10")
    return

; Host I → VM1 sends F11
i::
    ApplyJitterAndSend("F11")
    return

; Host O → VM1 sends F12
o::
    ApplyJitterAndSend("F12")
    return

; Host P → VM1 sends Home
p::
    ApplyJitterAndSend("Home")
    return

; Host Z → VM1 sends End
z::
    ApplyJitterAndSend("End")
    return

; Host X → VM1 sends PgUp
x::
    ApplyJitterAndSend("PgUp")
    return

; Host C → VM1 sends PgDn
c::
    ApplyJitterAndSend("PgDn")
    return

; Host V → VM1 sends Insert
v::
    ApplyJitterAndSend("Insert")
    return

; Host B → VM1 sends Delete
b::
    ApplyJitterAndSend("Delete")
    return

; ════════════════════════════════════════════════════════════
; 🔢 NUMBER KEYS - VM1 MAPPING
; ════════════════════════════════════════════════════════════
; Host 1 → VM1 sends Numpad1
1::
    ApplyJitterAndSend("Numpad1")
    return

2::
    ApplyJitterAndSend("Numpad2")
    return

3::
    ApplyJitterAndSend("Numpad3")
    return

4::
    ApplyJitterAndSend("Numpad4")
    return

5::
    ApplyJitterAndSend("Numpad5")
    return

6::
    ApplyJitterAndSend("Numpad6")
    return

7::
    ApplyJitterAndSend("Numpad7")
    return

8::
    ApplyJitterAndSend("Numpad8")
    return

9::
    ApplyJitterAndSend("Numpad9")
    return

0::
    ApplyJitterAndSend("Numpad0")
    return

; ════════════════════════════════════════════════════════════
; 🔧 CORE FUNCTIONS
; ════════════════════════════════════════════════════════════

ApplyJitterAndSend(key) {
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
    SendInput, {%key%}
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

; ════════════════════════════════════════════════════════════
; 🚪 EXIT HOTKEY
; ════════════════════════════════════════════════════════════

^+q::
    MsgBox, Exiting VM1 Jitter...
    ExitApp
    return

