; ═══════════════════════════════════════════════════════════
; LAYER 4+5 COMBINED: Key Remap + Input Jitter
; ═══════════════════════════════════════════════════════════
; Breaks Multiplicity sync with CUSTOM KEY REMAPPING + JITTER
; Install on ALL 3 Clients with DIFFERENT configs
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
; 🔄 CUSTOM KEY REMAPPING (LAYER 4) - EDIT HERE!
; ════════════════════════════════════════════════════════════
; Format: KeyRemap["source_key"] := "target_key"
; 
; Example setups:
;
; CLIENT 1 (Default - no remap):
;   Keep all keys as-is
;
; CLIENT 2 (Remap Q↔O):
;   Q → O
;   O → Q
;
; CLIENT 3 (Remap multiple keys):
;   Q → L
;   W → ;
;   E → P
;   R → [
;
; ════════════════════════════════════════════════════════════

global KeyRemap := {}

; ─────────────────────────────────────────────────
; CLIENT 1 EXAMPLE: No remapping (default keys)
; ─────────────────────────────────────────────────
; Leave empty or comment out all remaps

; ─────────────────────────────────────────────────
; CLIENT 2 EXAMPLE: Swap Q and O
; ─────────────────────────────────────────────────
KeyRemap["q"] := "o"
KeyRemap["o"] := "q"

; ─────────────────────────────────────────────────
; CLIENT 3 EXAMPLE: Multiple skill key remaps
; ─────────────────────────────────────────────────
; KeyRemap["q"] := "l"
; KeyRemap["w"] := ";"
; KeyRemap["e"] := "p"
; KeyRemap["r"] := "["
; KeyRemap["a"] := "k"
; KeyRemap["s"] := "j"
; KeyRemap["d"] := "h"

; ─────────────────────────────────────────────────
; ADD YOUR CUSTOM REMAPS HERE:
; ─────────────────────────────────────────────────
; KeyRemap["source"] := "target"
; KeyRemap["1"] := "7"
; KeyRemap["f1"] := "f5"
; etc...

; ════════════════════════════════════════════════════════════
; 🎮 ACTIVE ONLY IN MAPLESTORY
; ════════════════════════════════════════════════════════════
#IfWinActive, MapleStory

; ============ INTERCEPT ALL KEYBOARD KEYS ============

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
    ApplyRemapAndJitter(key)
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
    ApplyRemapAndJitter(key)
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
    ApplyRemapAndJitter(key)
    return

; Arrow keys
Left::
Right::
Up::
Down::
    key := A_ThisHotkey
    ApplyRemapAndJitter(key)
    return

; Modifier keys
Alt::
Space::
Ctrl::
Shift::
Tab::
CapsLock::
    key := A_ThisHotkey
    ApplyRemapAndJitter(key)
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
    ApplyRemapAndJitter(key)
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
    ApplyRemapAndJitter(key)
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
    ApplyRemapAndJitter(key)
    return

#IfWinActive

; ════════════════════════════════════════════════════════════
; 🔧 CORE FUNCTIONS
; ════════════════════════════════════════════════════════════

; ============ REMAP + JITTER FUNCTION ============
ApplyRemapAndJitter(key) {
    global MinJitter, MaxJitter, UseGaussian, KeyRemap
    
    ; STEP 1: Check if key should be remapped
    mappedKey := key
    if (KeyRemap.HasKey(key)) {
        mappedKey := KeyRemap[key]
    }
    
    ; STEP 2: Calculate jitter delay
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
    
    ; STEP 3: Apply jitter delay
    Sleep, %jitter%
    
    ; STEP 4: Send the remapped key (or original if no remap)
    Send {%mappedKey%}
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
; 📊 STATUS INDICATOR (Optional - shows script is running)
; ════════════════════════════════════════════════════════════
; Uncomment to see a tray tooltip when script loads
; TrayTip, Multiplicity Anti-Detection, Remap + Jitter Active!, 3, 1

