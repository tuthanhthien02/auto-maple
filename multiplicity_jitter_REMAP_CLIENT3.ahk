; ═══════════════════════════════════════════════════════════
; MULTIPLICITY JITTER - REMAP VERSION - CLIENT 3 (SLOW)
; ═══════════════════════════════════════════════════════════
; REQUIRES: PowerToys remapping on HOST PC
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

; ⚙️ CLIENT 3 CONFIGURATION (SLOW)
global MinJitter := 90
global MaxJitter := 150
global UseGaussian := true

MsgBox, 
(
✅ CLIENT 3 - SLOW JITTER (REMAP VERSION)
Running as Administrator

Jitter: 90-150ms (Gaussian)

IMPORTANT:
  - PowerToys MUST be configured on HOST!
  - See POWERTOYS_REMAP_CONFIG.md

Press CTRL+SHIFT+Q to exit
)

; Core game keys
a::
    ApplyJitterAndSend("q")
    return

s::
    ApplyJitterAndSend("w")
    return

d::
    ApplyJitterAndSend("e")
    return

f::
    ApplyJitterAndSend("r")
    return

g::
    ApplyJitterAndSend("t")
    return

h::
    ApplyJitterAndSend("y")
    return

j::
    ApplyJitterAndSend("u")
    return

k::
    ApplyJitterAndSend("i")
    return

l::
    ApplyJitterAndSend("o")
    return

`;::
    ApplyJitterAndSend("p")
    return

x::
    ApplyJitterAndSend("z")
    return

v::
    ApplyJitterAndSend("c")
    return

n::
    ApplyJitterAndSend("b")
    return

,::
    ApplyJitterAndSend("m")
    return

; Number keys (remapped from F1-F9)
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

; Core functions
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

; Exit
^+q::
    MsgBox, Exiting CLIENT 3 Jitter (Remap)...
    ExitApp
    return

