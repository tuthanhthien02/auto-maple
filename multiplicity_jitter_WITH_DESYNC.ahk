; ═══════════════════════════════════════════════════════════════════════
; 🎯 MULTIPLICITY JITTER WITH DESYNC - ANTI-DETECTION SYSTEM
; ═══════════════════════════════════════════════════════════════════════
; ⭐ NEW FEATURE: DESYNC DELAY ⭐
; Breaks Multiplicity synchronization across VMs!
; Each VM now responds at a statistically different time
; ═══════════════════════════════════════════════════════════════════════

#NoEnv
#SingleInstance Force
SetBatchLines, -1
Process, Priority,, High

; ═══════════════════════════════════════════════════════════════════════
; ⚙️ DESYNC CONFIGURATION (NEW! ⭐)
; ═══════════════════════════════════════════════════════════════════════
global MinDesync := 0      ; Min desync delay (ms)
global MaxDesync := 500    ; Max desync delay (ms)
; This adds 0-500ms random delay BEFORE jitter
; Breaks Multiplicity synchronization! ✅

; ═══════════════════════════════════════════════════════════════════════
; ⚙️ JITTER CONFIGURATION
; ═══════════════════════════════════════════════════════════════════════
global MinJitter := 30     ; Min jitter delay (ms)
global MaxJitter := 80     ; Max jitter delay (ms)
global UseGaussian := true ; Use Gaussian distribution (more human-like)

; ═══════════════════════════════════════════════════════════════════════
; ⚙️ BEHAVIORAL PAUSE CONFIGURATION
; ═══════════════════════════════════════════════════════════════════════
global MinPauseInterval := 180000  ; Min time between pauses (3 minutes in ms)
global MaxPauseInterval := 300000  ; Max time between pauses (5 minutes in ms)
global MinPauseDuration := 800     ; Min pause duration (ms)
global MaxPauseDuration := 2500    ; Max pause duration (ms)
global IsPaused := false           ; Current pause state

; ═══════════════════════════════════════════════════════════════════════
; 🎹 KEY REMAP TABLE - CUSTOMIZE HERE! ✏️
; ═══════════════════════════════════════════════════════════════════════
; Format: "source_key": "target_key"
; Example: "q": "a"  means pressing Q will send A (with desync + jitter)
; ═══════════════════════════════════════════════════════════════════════
global remap := {}
remap["q"] := "a"
remap["w"] := "s"
remap["e"] := "d"
remap["r"] := "f"
; Arrow keys (for movement)
remap["Left"] := "Left"
remap["Right"] := "Right"
remap["Up"] := "Up"
remap["Down"] := "Down"
remap["Space"] := "Space"

; ═══════════════════════════════════════════════════════════════════════
; 🔧 AUTO-GENERATE HOTKEYS FROM REMAP TABLE
; ═══════════════════════════════════════════════════════════════════════
For sourceKey, targetKey in remap {
    Hotkey, $%sourceKey%, HandleKey
}

; Start behavioral pause timer
SetTimer, CheckBehavioralPause, 1000
ScheduleNextPause()

Return

; ═══════════════════════════════════════════════════════════════════════
; 🎯 MAIN HANDLER - DESYNC + JITTER + REMAP
; ═══════════════════════════════════════════════════════════════════════
HandleKey:
    ; Check if we're in a behavioral pause
    if (IsPaused) {
        return ; Block input during pause
    }
    
    ; Get the pressed key (remove $ prefix)
    pressedKey := StrReplace(A_ThisHotkey, "$", "")
    
    ; Get the target key from remap table
    targetKey := remap[pressedKey]
    
    ; Apply desync + jitter and send
    ApplyDesyncJitterAndSend(targetKey)
Return

; ═══════════════════════════════════════════════════════════════════════
; ⭐ DESYNC + JITTER FUNCTION (NEW!)
; ═══════════════════════════════════════════════════════════════════════
ApplyDesyncJitterAndSend(key) {
    global MinDesync, MaxDesync, MinJitter, MaxJitter, UseGaussian
    
    ; ⭐ STEP 1: DESYNC DELAY (NEW!)
    ; This breaks Multiplicity synchronization
    Random, desyncDelay, %MinDesync%, %MaxDesync%
    Sleep, %desyncDelay%
    
    ; ⭐ STEP 2: JITTER DELAY
    ; This makes each keypress timing unique
    if (UseGaussian) {
        mean := (MinJitter + MaxJitter) / 2.0
        stdDev := (MaxJitter - MinJitter) / 6.0
        jitter := GaussianRandom(mean, stdDev, MinJitter, MaxJitter)
    } else {
        Random, jitter, %MinJitter%, %MaxJitter%
    }
    Sleep, %jitter%
    
    ; ⭐ STEP 3: SEND KEY
    SendInput, {%key%}
}

; ═══════════════════════════════════════════════════════════════════════
; 📊 GAUSSIAN RANDOM GENERATOR (for human-like timing)
; ═══════════════════════════════════════════════════════════════════════
GaussianRandom(mean, stdDev, min, max) {
    Random, u1, 0.0, 1.0
    Random, u2, 0.0, 1.0
    z := Sqrt(-2 * Ln(u1)) * Cos(2 * 3.14159265359 * u2)
    value := mean + z * stdDev
    if (value < min)
        value := min
    if (value > max)
        value := max
    return Round(value)
}

; ═══════════════════════════════════════════════════════════════════════
; ⏸️ BEHAVIORAL PAUSE SYSTEM
; ═══════════════════════════════════════════════════════════════════════
CheckBehavioralPause:
    if (A_TickCount >= NextPauseTime && !IsPaused) {
        StartBehavioralPause()
    }
Return

StartBehavioralPause() {
    global IsPaused, MinPauseDuration, MaxPauseDuration
    IsPaused := true
    Random, duration, %MinPauseDuration%, %MaxPauseDuration%
    SetTimer, EndBehavioralPause, %duration%
}

EndBehavioralPause:
    global IsPaused
    IsPaused := false
    SetTimer, EndBehavioralPause, Off
    ScheduleNextPause()
Return

ScheduleNextPause() {
    global NextPauseTime, MinPauseInterval, MaxPauseInterval
    Random, interval, %MinPauseInterval%, %MaxPauseInterval%
    NextPauseTime := A_TickCount + interval
}

