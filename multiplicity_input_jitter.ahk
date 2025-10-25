; ═══════════════════════════════════════════════════════════
; INPUT JITTER LAYER - Breaks Multiplicity Synchronization
; ═══════════════════════════════════════════════════════════
; Install on ALL 3 Clients with DIFFERENT jitter ranges
; ═══════════════════════════════════════════════════════════

#SingleInstance Force
#NoEnv
SetWorkingDir %A_ScriptDir%
Random, Seed, A_TickCount

; ============ CONFIGURATION (DIFFERENT PER CLIENT) ============

; CLIENT 1: Fast jitter (30-80ms)
global MinJitter := 30
global MaxJitter := 80

; CLIENT 2: Medium jitter (60-120ms) 
; global MinJitter := 60
; global MaxJitter := 120

; CLIENT 3: Slow jitter (90-150ms)
; global MinJitter := 90
; global MaxJitter := 150

; ============ TIMING DISTRIBUTION ============
global UseGaussian := true  ; Use Gaussian instead of uniform for more human-like

; ============ ONLY ACTIVE FOR MAPLESTORY ============
#IfWinActive, MapleStory

; ============ INTERCEPT ALL KEYS WITH JITTER ============

; Letter keys (A-Z)
a::
b::
c::
d::
e::
f::
g::
h::
i::
j::
k::
l::
m::
n::
o::
p::
q::
r::
s::
t::
u::
v::
w::
x::
y::
z::
    key := A_ThisHotkey
    ApplyJitterAndSend(key)
    return

; Number keys (0-9)
0::
1::
2::
3::
4::
5::
6::
7::
8::
9::
    key := A_ThisHotkey
    ApplyJitterAndSend(key)
    return

; Function keys (F1-F12)
F1::
F2::
F3::
F4::
F5::
F6::
F7::
F8::
F9::
F10::
F11::
F12::
    key := A_ThisHotkey
    ApplyJitterAndSend(key)
    return

; Arrow keys
Left::
Right::
Up::
Down::
    key := A_ThisHotkey
    ApplyJitterAndSend(key)
    return

; Modifier keys
Alt::
Space::
Ctrl::
Shift::
Tab::
CapsLock::
    key := A_ThisHotkey
    ApplyJitterAndSend(key)
    return

; Special keys
Enter::
Backspace::
Delete::
Insert::
Home::
End::
PgUp::
PgDn::
Esc::
    key := A_ThisHotkey
    ApplyJitterAndSend(key)
    return

; Numpad keys
Numpad0::
Numpad1::
Numpad2::
Numpad3::
Numpad4::
Numpad5::
Numpad6::
Numpad7::
Numpad8::
Numpad9::
NumpadAdd::
NumpadSub::
NumpadMult::
NumpadDiv::
NumpadEnter::
NumpadDot::
    key := A_ThisHotkey
    ApplyJitterAndSend(key)
    return

; Symbol keys
`;::
'::
,::
.::
/::
[::
]::
\::
-::
=::
    key := A_ThisHotkey
    ApplyJitterAndSend(key)
    return

#IfWinActive

; ============ JITTER FUNCTION ============
ApplyJitterAndSend(key) {
    global MinJitter, MaxJitter, UseGaussian
    
    if (UseGaussian) {
        ; Gaussian distribution (more human-like)
        mean := (MinJitter + MaxJitter) / 2
        stddev := (MaxJitter - MinJitter) / 4
        jitter := GaussianRandom(mean, stddev)
        
        ; Clamp to range
        if (jitter < MinJitter)
            jitter := MinJitter
        if (jitter > MaxJitter)
            jitter := MaxJitter
    } else {
        ; Uniform random
        Random, jitter, %MinJitter%, %MaxJitter%
    }
    
    ; Apply jitter delay
    Sleep, %jitter%
    
    ; Send the actual key
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


