; ═══════════════════════════════════════════════════════════
; MULTIPLICITY JITTER - REMAP VERSION - CLIENT 1 (FAST)
; ═══════════════════════════════════════════════════════════
; REQUIRES: PowerToys remapping on HOST PC
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

; ⚙️ CLIENT 1 CONFIGURATION (FAST)
global MinJitter := 30
global MaxJitter := 80
global UseGaussian := true

MsgBox, 
(
✅ CLIENT 1 - FAST JITTER (REMAP VERSION)
Running as Administrator

Jitter: 30-80ms (Gaussian)

IMPORTANT:
  - PowerToys MUST be configured on HOST!
  - See POWERTOYS_REMAP_CONFIG.md

Press CTRL+SHIFT+Q to exit
)

; ════════════════════════════════════════════════════════════
; 🎯 CORE GAME KEYS (Remapped from host)
; ════════════════════════════════════════════════════════════
; Host Q → A, Block A → Send Q with jitter
a::
    ApplyJitterAndSend("q")
    return

; Host W → S, Block S → Send W with jitter
s::
    ApplyJitterAndSend("w")
    return

; Host E → D, Block D → Send E with jitter
d::
    ApplyJitterAndSend("e")
    return

; Host R → F, Block F → Send R with jitter
f::
    ApplyJitterAndSend("r")
    return

; Host T → G, Block G → Send T
g::
    ApplyJitterAndSend("t")
    return

; Host Y → H, Block H → Send Y
h::
    ApplyJitterAndSend("y")
    return

; Host U → J, Block J → Send U
j::
    ApplyJitterAndSend("u")
    return

; Host I → K, Block K → Send I
k::
    ApplyJitterAndSend("i")
    return

; Host O → L, Block L → Send O
l::
    ApplyJitterAndSend("o")
    return

; Host P → ;, Block ; → Send P
`;::
    ApplyJitterAndSend("p")
    return

; Host Z → X, Block X → Send Z
x::
    ApplyJitterAndSend("z")
    return

; Host C → V, Block V → Send C
v::
    ApplyJitterAndSend("c")
    return

; Host B → N, Block N → Send B
n::
    ApplyJitterAndSend("b")
    return

; Host M → ,, Block , → Send M
,::
    ApplyJitterAndSend("m")
    return

; ════════════════════════════════════════════════════════════
; 🔢 NUMBER KEYS (Remap 1-9)
; ════════════════════════════════════════════════════════════
; Host 1 → F1, Block F1 → Send 1
F1::
    ApplyJitterAndSend("1")
    return

F2::
    ApplyJitterAndSend("2")
    return

F3::
    ApplyJitterAndSend("3")
    return

F4::
    ApplyJitterAndSend("4")
    return

F5::
    ApplyJitterAndSend("5")
    return

F6::
    ApplyJitterAndSend("6")
    return

F7::
    ApplyJitterAndSend("7")
    return

F8::
    ApplyJitterAndSend("8")
    return

F9::
    ApplyJitterAndSend("9")
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
    MsgBox, Exiting CLIENT 1 Jitter (Remap)...
    ExitApp
    return

