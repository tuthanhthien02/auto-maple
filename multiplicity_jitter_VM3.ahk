; ═══════════════════════════════════════════════════════════
; MULTIPLICITY JITTER - VM3 (SLOW)
; ═══════════════════════════════════════════════════════════
; NO POWERTOYS NEEDED! AHK does remap + jitter!
; 
; Host sends Q → VM receives Q → AHK blocks Q → Jitter → Send I
; 
; IN-GAME KEYBINDINGS (VM3):
;   Skill 1: I (host presses Q)
;   Skill 2: U (host presses W)
;   Skill 3: Y (host presses E)
;   Skill 4: T (host presses R)
;   etc.
;
; Jitter: 90-150ms (Gaussian)
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

; ⚙️ VM3 CONFIGURATION (SLOW)
global MinJitter := 90
global MaxJitter := 150
global UseGaussian := true

MsgBox, 
(
✅ VM3 - SLOW JITTER (NO POWERTOYS!)
Running as Administrator

Jitter: 90-150ms (Gaussian)

IMPORTANT:
  - Host sends Q, W, E, R...
  - VM3 converts: Q→I, W→U, E→Y, R→T
  - In-game keybindings MUST match!
  
IN-GAME SETUP:
  Skill 1 → I (host Q)
  Skill 2 → U (host W)
  Skill 3 → Y (host E)
  Skill 4 → T (host R)
  Skill 5 → G (host T)
  Skill 6 → H (host Y)

Press CTRL+SHIFT+Q to exit
)

; ════════════════════════════════════════════════════════════
; 🎯 GAME KEYS - VM3 MAPPING
; ════════════════════════════════════════════════════════════
; Host Q → VM3 sends I
$q::
    ApplyJitterAndSend("i")
    return

; Host W → VM3 sends U
$w::
    ApplyJitterAndSend("u")
    return

; Host E → VM3 sends Y
$e::
    ApplyJitterAndSend("y")
    return

; Host R → VM3 sends T
$r::
    ApplyJitterAndSend("t")
    return

; Host T → VM3 sends G
$t::
    ApplyJitterAndSend("g")
    return

; Host Y → VM3 sends H
$y::
    ApplyJitterAndSend("h")
    return

; Host U → VM3 sends J
$u::
    ApplyJitterAndSend("j")
    return

; Host I → VM3 sends K
$i::
    ApplyJitterAndSend("k")
    return

; Host O → VM3 sends M
$o::
    ApplyJitterAndSend("m")
    return

; Host P → VM3 sends N
$p::
    ApplyJitterAndSend("n")
    return

; Host Z → VM3 sends B
$z::
    ApplyJitterAndSend("b")
    return

; Host X → VM3 sends V
$x::
    ApplyJitterAndSend("v")
    return

; Host C → VM3 sends C (same - can't remap to itself, use Left)
$c::
    ApplyJitterAndSend("Left")
    return

; Host V → VM3 sends Right
$v::
    ApplyJitterAndSend("Right")
    return

; Host B → VM3 sends Up
$b::
    ApplyJitterAndSend("Up")
    return

; ════════════════════════════════════════════════════════════
; 🔢 NUMBER KEYS - VM3 MAPPING
; ════════════════════════════════════════════════════════════
; Host 1 → VM3 sends 6
$1::
    ApplyJitterAndSend("6")
    return

$2::
    ApplyJitterAndSend("7")
    return

$3::
    ApplyJitterAndSend("8")
    return

$4::
    ApplyJitterAndSend("9")
    return

$5::
    ApplyJitterAndSend("0")
    return

$6::
    ApplyJitterAndSend("1")
    return

$7::
    ApplyJitterAndSend("2")
    return

$8::
    ApplyJitterAndSend("3")
    return

$9::
    ApplyJitterAndSend("4")
    return

$0::
    ApplyJitterAndSend("5")
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
    MsgBox, Exiting VM3 Jitter...
    ExitApp
    return

