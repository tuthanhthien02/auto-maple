; ═══════════════════════════════════════════════════════════
; MULTIPLICITY JITTER - VM2 (MEDIUM)
; ═══════════════════════════════════════════════════════════
; NO POWERTOYS NEEDED! AHK does remap + jitter!
; 
; Host sends Q → VM receives Q → AHK blocks Q → Jitter → Send O
; 
; IN-GAME KEYBINDINGS (VM2):
;   Skill 1: O (host presses Q)
;   Skill 2: K (host presses W)
;   Skill 3: L (host presses E)
;   Skill 4: ; (host presses R)
;   etc.
;
; Jitter: 60-120ms (Gaussian)
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

; ⚙️ VM2 CONFIGURATION (MEDIUM)
global MinJitter := 60
global MaxJitter := 120
global UseGaussian := true

MsgBox, 
(
✅ VM2 - MEDIUM JITTER (NO POWERTOYS!)
Running as Administrator

Jitter: 60-120ms (Gaussian)

IMPORTANT:
  - Host sends Q, W, E, R...
  - VM2 converts: Q→O, W→K, E→L, R→;
  - In-game keybindings MUST match!
  
IN-GAME SETUP:
  Skill 1 → O (host Q)
  Skill 2 → K (host W)
  Skill 3 → L (host E)
  Skill 4 → ; (host R)
  Skill 5 → ' (host T)
  Skill 6 → ` (host Y)

Press CTRL+SHIFT+Q to exit
)

; ════════════════════════════════════════════════════════════
; 🎯 GAME KEYS - VM2 MAPPING
; ════════════════════════════════════════════════════════════
; Host Q → VM2 sends O
q::
    ApplyJitterAndSend("o")
    return

; Host W → VM2 sends K
w::
    ApplyJitterAndSend("k")
    return

; Host E → VM2 sends L
e::
    ApplyJitterAndSend("l")
    return

; Host R → VM2 sends ;
r::
    ApplyJitterAndSend(";")
    return

; Host T → VM2 sends '
t::
    ApplyJitterAndSend("'")
    return

; Host Y → VM2 sends `
y::
    ApplyJitterAndSend("``")
    return

; Host U → VM2 sends ,
u::
    ApplyJitterAndSend(",")
    return

; Host I → VM2 sends .
i::
    ApplyJitterAndSend(".")
    return

; Host O → VM2 sends /
o::
    ApplyJitterAndSend("/")
    return

; Host P → VM2 sends Numpad+
p::
    ApplyJitterAndSend("NumpadAdd")
    return

; Host Z → VM2 sends Numpad-
z::
    ApplyJitterAndSend("NumpadSub")
    return

; Host X → VM2 sends Numpad*
x::
    ApplyJitterAndSend("NumpadMult")
    return

; Host C → VM2 sends Numpad/
c::
    ApplyJitterAndSend("NumpadDiv")
    return

; Host V → VM2 sends NumpadDot
v::
    ApplyJitterAndSend("NumpadDot")
    return

; Host B → VM2 sends NumpadEnter
b::
    ApplyJitterAndSend("NumpadEnter")
    return

; ════════════════════════════════════════════════════════════
; 🔢 NUMBER KEYS - VM2 MAPPING
; ════════════════════════════════════════════════════════════
; Host 1 → VM2 sends F1
1::
    ApplyJitterAndSend("F1")
    return

2::
    ApplyJitterAndSend("F2")
    return

3::
    ApplyJitterAndSend("F3")
    return

4::
    ApplyJitterAndSend("F4")
    return

5::
    ApplyJitterAndSend("F5")
    return

6::
    ApplyJitterAndSend("F6")
    return

7::
    ApplyJitterAndSend("F7")
    return

8::
    ApplyJitterAndSend("F8")
    return

9::
    ApplyJitterAndSend("F9")
    return

0::
    ApplyJitterAndSend("F10")
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
    MsgBox, Exiting VM2 Jitter...
    ExitApp
    return

