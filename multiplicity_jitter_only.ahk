; ═══════════════════════════════════════════════════════════
; JITTER-ONLY MODE: For use WITH PowerToys Key Remapping
; ═══════════════════════════════════════════════════════════
; USE THIS WHEN:
; - PowerToys handles key remapping (driver-level, safest)
; - AHK ONLY adds jitter/delays (no remapping)
; 
; PIPELINE:
; Host Q → Multiplicity → Client Q → PowerToys (Q→O) → 
; AHK Jitter (O +45ms) → Game receives O @45ms
; ═══════════════════════════════════════════════════════════

#SingleInstance Force
#NoEnv
SetWorkingDir %A_ScriptDir%
Random, Seed, A_TickCount

; ════════════════════════════════════════════════════════════
; ⚙️ CONFIGURATION - CUSTOMIZE FOR EACH CLIENT
; ════════════════════════════════════════════════════════════

; ============ CLIENT JITTER TIMING (LAYER 5) ============

; CLIENT 1: Fast jitter (30-80ms)
global MinJitter := 30
global MaxJitter := 80

; CLIENT 2: Medium jitter (60-120ms) 
; global MinJitter := 60
; global MaxJitter := 120

; CLIENT 3: Slow jitter (90-150ms)
; global MinJitter := 90
; global MaxJitter := 150

; ============ JITTER DISTRIBUTION ============
global UseGaussian := true  ; true = More human-like | false = Uniform random

; ════════════════════════════════════════════════════════════
; 🔄 PASSTHROUGH MODE - NO REMAPPING!
; ════════════════════════════════════════════════════════════
; PowerToys handles remapping at driver-level
; AHK ONLY adds jitter to whatever key comes through
; ════════════════════════════════════════════════════════════

; ════════════════════════════════════════════════════════════
; 🎮 ACTIVE ONLY IN MAPLESTORY
; ════════════════════════════════════════════════════════════
#IfWinActive, MapleStory

; ============ INTERCEPT ALL KEYBOARD KEYS ============
; Intercepts AFTER PowerToys has already remapped
; Adds jitter and sends the SAME key (passthrough)

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
    ApplyJitterPassthrough(key)
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
    ApplyJitterPassthrough(key)
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
    ApplyJitterPassthrough(key)
    return

; Arrow keys
Left::
Right::
Up::
Down::
    key := A_ThisHotkey
    ApplyJitterPassthrough(key)
    return

; Modifier keys
Alt::
Space::
Ctrl::
Shift::
Tab::
CapsLock::
    key := A_ThisHotkey
    ApplyJitterPassthrough(key)
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
    ApplyJitterPassthrough(key)
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
    ApplyJitterPassthrough(key)
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
    ApplyJitterPassthrough(key)
    return

#IfWinActive

; ════════════════════════════════════════════════════════════
; 🔧 CORE FUNCTIONS
; ════════════════════════════════════════════════════════════

; ============ PASSTHROUGH JITTER (NO REMAP!) ============
ApplyJitterPassthrough(key) {
    global MinJitter, MaxJitter, UseGaussian
    
    ; NO REMAPPING - just pass through the same key!
    ; PowerToys already remapped at driver-level
    
    ; Calculate jitter delay
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
    
    ; Send the SAME key that came in (passthrough!)
    ; This is the key AFTER PowerToys remapping
    Send {%key%}
}

; ============ GAUSSIAN RANDOM (Bell Curve Distribution) ============
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
; 📊 STATUS INDICATOR (Optional)
; ════════════════════════════════════════════════════════════
; Uncomment to see a tray tooltip when script loads
; TrayTip, Multiplicity Jitter-Only, Passthrough Mode Active!, 3, 1

