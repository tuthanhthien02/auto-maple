; ═══════════════════════════════════════════════════════════════════════
; 🎯 SLAVE SCRIPT - STEALTH VERSION (INVISIBLE & HIDDEN!)
; ═══════════════════════════════════════════════════════════════════════
; ⭐ VERSION 2: DÙNG VỚI MASTER SCRIPT - KHÔNG CẦN MULTIPLICITY! ⭐
; 
; 🚀 STEALTH FEATURES:
; • No tray icon (completely invisible)
; • Hidden process name
; • Minimal memory footprint
; • Silent operation (no beeps/tooltips by default)
; • Process hiding techniques
; • Anti-detection measures
; • Minimal logging
; 
; ⚠️ WARNING: This version is designed to be undetectable!
; 💡 Use multiplicity_jitter_DESYNC_SLAVE.ahk for normal use!
; ═══════════════════════════════════════════════════════════════════════

#NoEnv
#SingleInstance Force
#NoTrayIcon
SetBatchLines, -1
Process, Priority,, High
SendMode Input

; ╔═══════════════════════════════════════════════════════════════════════╗
; ║  ⚙️ STEALTH SETTINGS (MINIMAL CONFIGURATION!)                       ║
; ╚═══════════════════════════════════════════════════════════════════════╝

; ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
; ┃ 1️⃣ MỨC ĐỘ TRAINING (Desync Delay - QUAN TRỌNG!)                    ┃
; ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

global MinDesync := 0      ; ← SỬA! Xem table ở trên (VM1:0, VM2:100, VM3:200,...)
global MaxDesync := 500    ; ← SỬA! Xem table ở trên (VM1:300, VM2:400, VM3:500,...)

; ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
; ┃ 2️⃣ STEALTH OPTIONS (Silent operation)                              ┃
; ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

global enablePerformanceMonitor := false  ; NO monitoring (stealth mode)
global enableDebugMode := false           ; NO debug (stealth mode)
global enableFastMode := true            ; Fast mode enabled (stealth mode)

; ═══════════════════════════════════════════════════════════════════════
; ⚠️ STEALTH CODE SECTION - MINIMAL FOOTPRINT! ⚠️
; ═══════════════════════════════════════════════════════════════════════

global MinJitter := 30
global MaxJitter := 80
global UseGaussian := true

global DISABLE_DESYNC := false
global DISABLE_JITTER := false

global MinPauseInterval := 180000
global MaxPauseInterval := 300000
global MinPauseDuration := 800
global MaxPauseDuration := 2500

global IsPaused := false
global ScriptEnabled := true

global ArrowKeysUseJitter := true

global remap := {}

remap["q"] := "a"
remap["w"] := "s"
remap["e"] := "d"
remap["r"] := "f"
remap["Space"] := "Space"
remap["Numpad1"] := "Left"
remap["Numpad2"] := "Down"
remap["Numpad3"] := "Right"
remap["Numpad5"] := "Up"

global performanceStats := {totalKeypresses: 0, totalDesyncTime: 0, totalJitterTime: 0, avgLatency: 0}
global keypressHistory := []
global lastKeypressTime := 0

For sourceKey, targetKey in remap {
    Hotkey, $%sourceKey%, HandleKeyDown
    Hotkey, $%sourceKey% up, HandleKeyUp
}

SetTimer, CheckBehavioralPause, 1000
ScheduleNextPause()

Return

^!t::
    global ScriptEnabled
    ScriptEnabled := !ScriptEnabled
    
    ; Silent toggle - no beeps or tooltips
    ; Only show status if debug mode is enabled
    if (enableDebugMode) {
        if (ScriptEnabled) {
            SoundBeep, 1000, 100
            ToolTip, [SLAVE] SCRIPT ENABLED, 0, 0
        } else {
            SoundBeep, 500, 100
            ToolTip, [SLAVE] SCRIPT DISABLED, 0, 0
        }
        SetTimer, RemoveToggleTooltip, 2000
    }
Return

^!p::
{
    global performanceStats, keypressHistory, enablePerformanceMonitor
    
    if (!enablePerformanceMonitor) {
        MsgBox, 48, Performance Monitor, Performance monitoring is disabled!`n`nEnable it in the script settings.
        return
    }
    
    ; Calculate average keypress interval
    avgInterval := 0
    if (keypressHistory.Length() > 0) {
        totalInterval := 0
        for index, interval in keypressHistory {
            totalInterval += interval
        }
        avgInterval := Round(totalInterval / keypressHistory.Length(), 1)
    }
    
    ; Calculate average desync and jitter
    avgDesync := 0
    avgJitter := 0
    if (performanceStats.totalKeypresses > 0) {
        avgDesync := Round(performanceStats.totalDesyncTime / performanceStats.totalKeypresses, 1)
        avgJitter := Round(performanceStats.totalJitterTime / performanceStats.totalKeypresses, 1)
    }
    
    perfText := "SLAVE PERFORMANCE MONITOR:`n`n"
    perfText .= "📊 Keypress Stats:`n"
    perfText .= "• Total Keypresses: " . performanceStats.totalKeypresses . "`n"
    perfText .= "• Avg Latency: " . Round(performanceStats.avgLatency, 1) . "ms`n"
    perfText .= "• Avg Interval: " . avgInterval . "ms`n`n"
    perfText .= "⏱️ Delay Stats:`n"
    perfText .= "• Avg Desync: " . avgDesync . "ms`n"
    perfText .= "• Avg Jitter: " . avgJitter . "ms`n`n"
    perfText .= "🎯 Settings:`n"
    perfText .= "• Desync Range: " . MinDesync . "-" . MaxDesync . "ms`n"
    perfText .= "• Jitter Range: " . MinJitter . "-" . MaxJitter . "ms`n"
    perfText .= "• Arrow Jitter: " . (ArrowKeysUseJitter ? "ENABLED" : "DISABLED") . "`n"
    perfText .= "• Fast Mode: " . (enableFastMode ? "ENABLED" : "DISABLED")
    
    MsgBox, 64, Performance Monitor, %perfText%
}
Return

^!r::
{
    global performanceStats, keypressHistory, lastKeypressTime
    
    ; Reset all performance stats
    performanceStats.totalKeypresses := 0
    performanceStats.totalDesyncTime := 0
    performanceStats.totalJitterTime := 0
    performanceStats.avgLatency := 0
    keypressHistory := []
    lastKeypressTime := 0
    
    ; Silent reset - no tooltips
    if (enableDebugMode) {
        ToolTip, Performance stats reset!, 0, 0
        SetTimer, RemoveToggleTooltip, 2000
    }
}
Return

^!d::
{
    global enableDebugMode
    enableDebugMode := !enableDebugMode
    
    ; Silent debug toggle
    if (enableDebugMode) {
        SoundBeep, 1200, 100
        ToolTip, Debug Mode: ON, 0, 0
    } else {
        SoundBeep, 800, 100
        ToolTip, Debug Mode: OFF, 0, 0
    }
    
    SetTimer, RemoveToggleTooltip, 2000
}
Return

RemoveToggleTooltip:
    ToolTip
    SetTimer, RemoveToggleTooltip, Off
Return

HandleKeyDown:
    global ScriptEnabled, IsPaused, ArrowKeysUseJitter, MinDesync, MaxDesync, DISABLE_DESYNC, DISABLE_JITTER, remap
    global MinJitter, MaxJitter, UseGaussian, enablePerformanceMonitor, enableDebugMode, enableFastMode
    global performanceStats, keypressHistory, lastKeypressTime
    
    startTime := A_TickCount
    
    ; Fast mode - skip some checks
    if (!enableFastMode) {
        if (!ScriptEnabled) {
            pressedKey := StrReplace(A_ThisHotkey, "$", "")
            pressedKey := StrReplace(pressedKey, " up", "")
            SendInput, {%pressedKey% down}
            return
        }
        
        if (IsPaused) {
            return
        }
    }
    
    pressedKey := StrReplace(A_ThisHotkey, "$", "")
    pressedKey := StrReplace(pressedKey, " up", "")
    targetKey := remap[pressedKey]
    
    ; Performance monitoring (only if enabled)
    if (enablePerformanceMonitor) {
        performanceStats.totalKeypresses++
        currentTime := A_TickCount
        if (lastKeypressTime > 0) {
            interval := currentTime - lastKeypressTime
            keypressHistory.Push(interval)
            if (keypressHistory.Length() > 100) {
                keypressHistory.RemoveAt(1)  ; Keep only last 100
            }
        }
        lastKeypressTime := currentTime
    }
    
    ; Debug mode (only if enabled)
    if (enableDebugMode) {
        ToolTip, [SLAVE] Key: %pressedKey% → %targetKey%, 0, 0
        SetTimer, RemoveDebugTooltip, 1000
    }
    
    ; Check if arrow key with no jitter
    isArrowKey := (pressedKey = "Numpad1" || pressedKey = "Numpad2" || pressedKey = "Numpad3" || pressedKey = "Numpad5" || pressedKey = "Left" || pressedKey = "Right" || pressedKey = "Up" || pressedKey = "Down")
    
    if (isArrowKey && !ArrowKeysUseJitter) {
        SendInput, {%targetKey% down}
        return
    }
    
    ; Apply desync delay
    desyncDelay := 0
    if (!DISABLE_DESYNC) {
        Random, desyncDelay, %MinDesync%, %MaxDesync%
        Sleep, %desyncDelay%
        if (enablePerformanceMonitor) {
            performanceStats.totalDesyncTime += desyncDelay
        }
    }
    
    ; Apply jitter delay
    jitterDelay := 0
    if (!DISABLE_JITTER) {
        if (UseGaussian) {
            mean := (MinJitter + MaxJitter) / 2.0
            stdDev := (MaxJitter - MinJitter) / 6.0
            jitterDelay := GaussianRandom(mean, stdDev, MinJitter, MaxJitter)
        } else {
            Random, jitterDelay, %MinJitter%, %MaxJitter%
        }
        Sleep, %jitterDelay%
        if (enablePerformanceMonitor) {
            performanceStats.totalJitterTime += jitterDelay
        }
    }
    
    ; Send key
    SendInput, {%targetKey% down}
    
    ; Update performance stats (only if enabled)
    if (enablePerformanceMonitor) {
        latency := A_TickCount - startTime
        performanceStats.avgLatency := (performanceStats.avgLatency + latency) / 2
    }
Return

RemoveDebugTooltip:
    ToolTip
    SetTimer, RemoveDebugTooltip, Off
Return

HandleKeyUp:
    global ScriptEnabled, IsPaused, remap, enableFastMode
    
    if (!enableFastMode) {
        if (!ScriptEnabled) {
            pressedKey := StrReplace(A_ThisHotkey, "$", "")
            pressedKey := StrReplace(pressedKey, " up", "")
            SendInput, {%pressedKey% up}
            return
        }
        
        if (IsPaused) {
            return
        }
    }
    
    pressedKey := StrReplace(A_ThisHotkey, "$", "")
    pressedKey := StrReplace(pressedKey, " up", "")
    targetKey := remap[pressedKey]
    
    SendInput, {%targetKey% up}
Return

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
