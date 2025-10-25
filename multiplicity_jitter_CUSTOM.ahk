; ═══════════════════════════════════════════════════════════
; MULTIPLICITY JITTER - CUSTOM REMAP (EASY TO EDIT!)
; ═══════════════════════════════════════════════════════════
; Simply edit the REMAP TABLE below to change key mappings!
; 
; Example:
;   Host sends Q → VM receives Q → AHK blocks Q → Jitter → Send A
; 
; Jitter: 30-80ms (Gaussian) - Change at line 38-39
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

; ⚙️ JITTER CONFIGURATION (EDIT HERE!)
global MinJitter := 30
global MaxJitter := 80
global UseGaussian := true

; ═══════════════════════════════════════════════════════════
; 🎨 REMAP TABLE - EDIT HERE TO CHANGE MAPPINGS!
; ═══════════════════════════════════════════════════════════
; Format: remap["input_key"] := "output_key"
; 
; ADD NEW:    remap["x"] := "z"
; REMOVE:     Delete or comment out with ;
; CHANGE:     Just edit the output key!
; ═══════════════════════════════════════════════════════════

global remap := {}

; ─────────────────────────────────────
; MAIN KEYS (Q W E R → A S D F)
; ─────────────────────────────────────
remap["q"] := "a"
remap["w"] := "s"
remap["e"] := "d"
remap["r"] := "f"

; ─────────────────────────────────────
; ADDITIONAL KEYS
; ─────────────────────────────────────
remap["t"] := "g"
remap["y"] := "h"
remap["u"] := "j"
remap["i"] := "k"
remap["o"] := "l"
remap["p"] := ";"

; ─────────────────────────────────────
; BOTTOM ROW
; ─────────────────────────────────────
remap["z"] := "m"
remap["x"] := ","
remap["c"] := "."
remap["v"] := "/"
remap["b"] := "'"

; ─────────────────────────────────────
; NUMBER KEYS → NUMPAD
; ─────────────────────────────────────
remap["1"] := "Numpad1"
remap["2"] := "Numpad2"
remap["3"] := "Numpad3"
remap["4"] := "Numpad4"
remap["5"] := "Numpad5"
remap["6"] := "Numpad6"
remap["7"] := "Numpad7"
remap["8"] := "Numpad8"
remap["9"] := "Numpad9"
remap["0"] := "Numpad0"

; ═══════════════════════════════════════════════════════════
; END OF REMAP TABLE
; ═══════════════════════════════════════════════════════════

; Show startup message
remapList := ""
for inputKey, outputKey in remap {
    remapList .= inputKey . " → " . outputKey . "`n"
}

MsgBox, 
(
✅ CUSTOM JITTER LOADED!
Running as Administrator

Jitter: %MinJitter%-%MaxJitter%ms (Gaussian)

REMAPPINGS:
%remapList%

Press CTRL+SHIFT+Q to exit
)

; ════════════════════════════════════════════════════════════
; 🔧 AUTO-GENERATE HOTKEYS FROM REMAP TABLE
; ════════════════════════════════════════════════════════════

for inputKey, outputKey in remap {
    ; Create hotkey: $inputKey:: calls HandleKey with outputKey
    Hotkey, $%inputKey%, HandleKey
}

return

; ════════════════════════════════════════════════════════════
; 🎯 HOTKEY HANDLER
; ════════════════════════════════════════════════════════════

HandleKey:
    ; Get the hotkey that was pressed (e.g., "$q")
    pressedKey := SubStr(A_ThisHotkey, 2)  ; Remove $ prefix
    
    ; Look up what key to send
    outputKey := remap[pressedKey]
    
    if (outputKey != "") {
        ApplyJitterAndSend(outputKey)
    }
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
    MsgBox, Exiting Custom Jitter...
    ExitApp
    return

