; ═══════════════════════════════════════════════════════════
; JITTER WITH PASSTHROUGH - Keys work normally!
; ═══════════════════════════════════════════════════════════
; Uses ~ prefix to PASSTHROUGH keys + add jitter
; Keys will work normally with slight delay
; ═══════════════════════════════════════════════════════════

#SingleInstance Force
#NoEnv
SetWorkingDir %A_ScriptDir%
Random, Seed, A_TickCount
#MaxHotkeysPerInterval 200

; ════════════════════════════════════════════════════════════
; ⚙️ CONFIGURATION
; ════════════════════════════════════════════════════════════

global MinJitter := 30
global MaxJitter := 80
global UseGaussian := true

MsgBox, 
(
MULTIPLICITY JITTER - PASSTHROUGH MODE

Configuration:
- Jitter Range: %MinJitter%-%MaxJitter%ms
- Gaussian Distribution: Enabled
- Mode: Global (all windows)

Keys will passthrough with jitter delay!

Press CTRL+SHIFT+Q to exit script.
)

; ════════════════════════════════════════════════════════════
; 🎯 PASSTHROUGH KEYS WITH JITTER
; ════════════════════════════════════════════════════════════

; Letter keys (a-z) - PASSTHROUGH with jitter
~a::
~b::
~c::
~d::
~e::
~f::
~g::
~h::
~i::
~j::
~k::
~l::
~m::
~n::
~o::
~p::
~q::
~r::
~s::
~t::
~u::
~v::
~w::
~x::
~y::
~z::
    ApplyJitterOnly()
    return

; Number keys (0-9) - PASSTHROUGH with jitter
~0::
~1::
~2::
~3::
~4::
~5::
~6::
~7::
~8::
~9::
    ApplyJitterOnly()
    return

; Arrow keys - PASSTHROUGH with jitter
~Left::
~Right::
~Up::
~Down::
    ApplyJitterOnly()
    return

; Function keys - PASSTHROUGH with jitter
~F1::
~F2::
~F3::
~F4::
~F5::
~F6::
~F7::
~F8::
~F9::
~F10::
~F11::
~F12::
    ApplyJitterOnly()
    return

; Modifier keys - PASSTHROUGH with jitter
~Alt::
~Space::
~Ctrl::
~Shift::
~Tab::
    ApplyJitterOnly()
    return

; Special keys - PASSTHROUGH with jitter
~Enter::
~Backspace::
~Delete::
~Insert::
~Home::
~End::
~PgUp::
~PgDn::
~Esc::
    ApplyJitterOnly()
    return

; Numpad keys - PASSTHROUGH with jitter
~Numpad0::
~Numpad1::
~Numpad2::
~Numpad3::
~Numpad4::
~Numpad5::
~Numpad6::
~Numpad7::
~Numpad8::
~Numpad9::
~NumpadAdd::
~NumpadSub::
~NumpadMult::
~NumpadDiv::
~NumpadEnter::
~NumpadDot::
    ApplyJitterOnly()
    return

; Symbol keys - PASSTHROUGH with jitter
~`;::
~'::
~,::
~.::
~/::
~[::
~]::
~\::
~-::
~=::
    ApplyJitterOnly()
    return

; ════════════════════════════════════════════════════════════
; 🔧 CORE FUNCTIONS
; ════════════════════════════════════════════════════════════

ApplyJitterOnly() {
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
    ; Key already sent due to ~ prefix!
    Sleep, %jitter%
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


