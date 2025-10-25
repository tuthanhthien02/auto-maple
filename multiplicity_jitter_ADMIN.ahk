; ═══════════════════════════════════════════════════════════
; MULTIPLICITY INPUT JITTER - ADMIN VERSION
; ═══════════════════════════════════════════════════════════
; Blocks keys → Adds jitter delay → Sends keys
; AUTO-ELEVATES TO ADMIN RIGHTS!
; This WILL create different timing per client!
; ═══════════════════════════════════════════════════════════

#SingleInstance Force
#NoEnv
SetWorkingDir %A_ScriptDir%
Random, Seed, A_TickCount
#MaxHotkeysPerInterval 200

; ════════════════════════════════════════════════════════════
; 🔒 AUTO-ELEVATE TO ADMIN (if not already)
; ════════════════════════════════════════════════════════════
if not A_IsAdmin
{
    Run *RunAs "%A_ScriptFullPath%"
    ExitApp
}

; ════════════════════════════════════════════════════════════
; ⚙️ CONFIGURATION
; ════════════════════════════════════════════════════════════

global MinJitter := 30
global MaxJitter := 80
global UseGaussian := true

MsgBox, 
(
✅ RUNNING AS ADMINISTRATOR!

MULTIPLICITY INPUT JITTER - WORKING!

Configuration:
- Jitter Range: %MinJitter%-%MaxJitter%ms
- Gaussian Distribution: Enabled
- Mode: Global (all windows)
- Admin Rights: Yes

Keys will be delayed by %MinJitter%-%MaxJitter%ms!

Press CTRL+SHIFT+Q to exit script.
)

; ════════════════════════════════════════════════════════════
; 🎯 KEYS WITH JITTER (Block → Sleep → Send)
; ════════════════════════════════════════════════════════════

; Letter keys (a-z)
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

; Arrow keys
Left::
Right::
Up::
Down::
    key := A_ThisHotkey
    ApplyJitterAndSend(key)
    return

; Function keys
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

; Modifier keys
Alt::
Space::
Ctrl::
Shift::
Tab::
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

; ════════════════════════════════════════════════════════════
; 🔧 CORE FUNCTIONS
; ════════════════════════════════════════════════════════════

ApplyJitterAndSend(key) {
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
    
    ; SLEEP FIRST (add jitter delay)
    Sleep, %jitter%
    
    ; THEN send key (using SendInput - works with admin!)
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
    MsgBox, Exiting Multiplicity Jitter script...
    ExitApp
    return


