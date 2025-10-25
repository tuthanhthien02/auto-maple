; ═══════════════════════════════════════════════════════════
; BEHAVIORAL VARIATION - LAYER 6
; ═══════════════════════════════════════════════════════════
; Adds random pauses to break predictable patterns
; Run this ALONGSIDE your multiplicity_jitter script!
; ═══════════════════════════════════════════════════════════

#SingleInstance Force
#NoEnv
#Persistent
SetWorkingDir %A_ScriptDir%

; 🔒 AUTO-ELEVATE TO ADMIN
if not A_IsAdmin
{
    Run *RunAs "%A_ScriptFullPath%"
    ExitApp
}

; ⚙️ CONFIGURATION (EDIT HERE!)
; ───────────────────────────────────────────────────────────
global MinPauseInterval := 5    ; Min minutes between pauses
global MaxPauseInterval := 10   ; Max minutes between pauses
global MinPauseDuration := 30   ; Min pause duration (seconds)
global MaxPauseDuration := 120  ; Max pause duration (seconds)

MsgBox, 
(
✅ BEHAVIORAL VARIATION ACTIVE!
Running as Administrator

Settings:
  Pause every: %MinPauseInterval%-%MaxPauseInterval% minutes
  Pause duration: %MinPauseDuration%-%MaxPauseDuration% seconds

This breaks predictable bot patterns!

Press CTRL+SHIFT+B to exit
)

; Start the timer
SetTimer, RandomPause, 60000  ; Check every minute
return

; ════════════════════════════════════════════════════════════
; 🎲 RANDOM PAUSE LOGIC
; ════════════════════════════════════════════════════════════

RandomPause:
    global MinPauseInterval, MaxPauseInterval, MinPauseDuration, MaxPauseDuration
    static LastPauseTime := A_TickCount
    
    ; Calculate next pause time
    Random, intervalMinutes, %MinPauseInterval%, %MaxPauseInterval%
    intervalMs := intervalMinutes * 60 * 1000
    
    ; Check if it's time to pause
    if (A_TickCount - LastPauseTime >= intervalMs) {
        ; Random pause duration
        Random, pauseSeconds, %MinPauseDuration%, %MaxPauseDuration%
        
        ; Show notification
        TrayTip, Behavioral Pause, Taking a %pauseSeconds%s break..., 3, 1
        
        ; Pause (in reality, just don't send input - but for demo, we sleep)
        ; In production, you'd set a global flag that your main script checks
        Sleep, %pauseSeconds%000
        
        ; Update last pause time
        LastPauseTime := A_TickCount
        
        ; Log
        TrayTip, Behavioral Pause, Break over! Resuming..., 2, 1
    }
    return

; ════════════════════════════════════════════════════════════
; 🚪 EXIT HOTKEY
; ════════════════════════════════════════════════════════════

^+b::
    MsgBox, Exiting Behavioral Variation...
    ExitApp
    return

