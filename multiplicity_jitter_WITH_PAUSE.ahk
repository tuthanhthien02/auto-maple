; ═══════════════════════════════════════════════════════════
; MULTIPLICITY JITTER + BEHAVIORAL PAUSE - INTEGRATED!
; ═══════════════════════════════════════════════════════════
; Combines jitter + remap + behavioral variation in ONE script!
; When paused, INPUT IS BLOCKED! ✅
; ═══════════════════════════════════════════════════════════

#SingleInstance Force
#NoEnv
#Persistent
SetWorkingDir %A_ScriptDir%
Random, Seed, A_TickCount
#MaxHotkeysPerInterval 200

; 🔒 AUTO-ELEVATE TO ADMIN
if not A_IsAdmin
{
    Run *RunAs "%A_ScriptFullPath%"
    ExitApp
}

; ⚙️ JITTER CONFIGURATION
global MinJitter := 30
global MaxJitter := 80
global UseGaussian := true

; ⚙️ BEHAVIORAL PAUSE CONFIGURATION
global MinPauseInterval := 5    ; Min minutes between pauses
global MaxPauseInterval := 10   ; Max minutes between pauses
global MinPauseDuration := 30   ; Min pause duration (seconds)
global MaxPauseDuration := 120  ; Max pause duration (seconds)
global IsPaused := false         ; ← KEY: Global pause flag!
global LastPauseTime := A_TickCount

; ═══════════════════════════════════════════════════════════
; 🎨 REMAP TABLE - EDIT HERE!
; ═══════════════════════════════════════════════════════════

global remap := {}

; MAIN KEYS (Q W E R → A S D F)
remap["q"] := "a"
remap["w"] := "s"
remap["e"] := "d"
remap["r"] := "f"

; ADDITIONAL KEYS
remap["t"] := "g"
remap["y"] := "h"
remap["u"] := "j"
remap["i"] := "k"
remap["o"] := "l"
remap["p"] := ";"

; BOTTOM ROW
remap["z"] := "m"
remap["x"] := ","
remap["c"] := "."
remap["v"] := "/"
remap["b"] := "'"

; NUMBER KEYS → NUMPAD
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

; ─────────────────────────────────────
; ARROW KEYS + SPACE (PASSTHROUGH WITH JITTER!)
; ─────────────────────────────────────
; These keys send to SAME key but WITH JITTER!
; This adds timing variation for movement ✅
remap["Up"] := "Up"
remap["Down"] := "Down"
remap["Left"] := "Left"
remap["Right"] := "Right"
remap["Space"] := "Space"

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
✅ JITTER + BEHAVIORAL PAUSE ACTIVE!
Running as Administrator

JITTER:
  %MinJitter%-%MaxJitter%ms (Gaussian)

BEHAVIORAL PAUSE:
  Every: %MinPauseInterval%-%MaxPauseInterval% minutes
  Duration: %MinPauseDuration%-%MaxPauseDuration% seconds
  
REMAPPINGS:
%remapList%

When paused: INPUT IS BLOCKED! ✅

Press CTRL+SHIFT+Q to exit
)

; ════════════════════════════════════════════════════════════
; 🔧 AUTO-GENERATE HOTKEYS FROM REMAP TABLE
; ════════════════════════════════════════════════════════════

for inputKey, outputKey in remap {
    Hotkey, $%inputKey%, HandleKey
}

; Start behavioral pause timer
SetTimer, CheckBehavioralPause, 60000  ; Check every minute

return

; ════════════════════════════════════════════════════════════
; 🎯 HOTKEY HANDLER (WITH PAUSE CHECK!)
; ════════════════════════════════════════════════════════════

HandleKey:
    global IsPaused, remap
    
    ; ⚠️ KEY: Check if paused!
    if (IsPaused) {
        ; INPUT IS BLOCKED during pause! ✅
        return
    }
    
    ; Get the hotkey that was pressed
    pressedKey := SubStr(A_ThisHotkey, 2)  ; Remove $ prefix
    
    ; Look up what key to send
    outputKey := remap[pressedKey]
    
    if (outputKey != "") {
        ApplyJitterAndSend(outputKey)
    }
    return

; ════════════════════════════════════════════════════════════
; 🎲 BEHAVIORAL PAUSE LOGIC
; ════════════════════════════════════════════════════════════

CheckBehavioralPause:
    global MinPauseInterval, MaxPauseInterval, MinPauseDuration, MaxPauseDuration
    global IsPaused, LastPauseTime
    
    ; Don't check if already paused
    if (IsPaused) {
        return
    }
    
    ; Calculate next pause time
    Random, intervalMinutes, %MinPauseInterval%, %MaxPauseInterval%
    intervalMs := intervalMinutes * 60 * 1000
    
    ; Check if it's time to pause
    if (A_TickCount - LastPauseTime >= intervalMs) {
        ; Random pause duration
        Random, pauseSeconds, %MinPauseDuration%, %MaxPauseDuration%
        
        ; SET PAUSE FLAG - THIS BLOCKS INPUT! ✅
        IsPaused := true
        
        ; Show notification
        TrayTip, Behavioral Pause, Taking a %pauseSeconds%s break... INPUT BLOCKED!, 3, 1
        
        ; Sleep for the pause duration
        Sleep, %pauseSeconds%000
        
        ; CLEAR PAUSE FLAG - RESUME INPUT! ✅
        IsPaused := false
        
        ; Update last pause time
        LastPauseTime := A_TickCount
        
        ; Log
        TrayTip, Behavioral Pause, Break over! INPUT RESUMED!, 2, 1
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
    MsgBox, Exiting Jitter + Behavioral Pause...
    ExitApp
    return

