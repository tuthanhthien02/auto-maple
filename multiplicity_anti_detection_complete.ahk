; ═══════════════════════════════════════════════════════════
; COMPLETE ANTI-DETECTION SYSTEM FOR MULTIPLICITY
; ═══════════════════════════════════════════════════════════
; Deploy on EACH client with different ClientID (1, 2, or 3)
; ═══════════════════════════════════════════════════════════

#SingleInstance Force
#NoEnv
SetWorkingDir %A_ScriptDir%
Random, Seed, A_TickCount

; ============ CLIENT CONFIGURATION ============
; CHANGE THIS FOR EACH CLIENT!
global ClientID := 1  ; 1, 2, or 3

; Auto-load client-specific profile
LoadClientProfile(ClientID)

; ============ CLIENT PROFILES ============
LoadClientProfile(id) {
    global
    
    if (id = 1) {
        ; CLIENT 1: Aggressive - Fast reactions
        ClientName := "Client1_Fast"
        SkillDelayMean := 150
        SkillDelayStdDev := 40
        MovementDelayMean := 70
        MovementDelayStdDev := 25
        SkillMissRate := 2  ; 2% miss rate
        AFKChance := 3      ; 3% per minute
        BreakMinTime := 5   ; 5-10 min breaks
        BreakMaxTime := 10
        FarmMinTime := 45   ; Farm 45-55 mins
        FarmMaxTime := 55
    }
    else if (id = 2) {
        ; CLIENT 2: Balanced - Medium reactions
        ClientName := "Client2_Balanced"
        SkillDelayMean := 200
        SkillDelayStdDev := 60
        MovementDelayMean := 100
        MovementDelayStdDev := 35
        SkillMissRate := 4
        AFKChance := 5
        BreakMinTime := 10
        BreakMaxTime := 15
        FarmMinTime := 35
        FarmMaxTime := 45
    }
    else if (id = 3) {
        ; CLIENT 3: Casual - Slow reactions
        ClientName := "Client3_Casual"
        SkillDelayMean := 250
        SkillDelayStdDev := 80
        MovementDelayMean := 130
        MovementDelayStdDev := 45
        SkillMissRate := 6
        AFKChance := 8
        BreakMinTime := 15
        BreakMaxTime := 25
        FarmMinTime := 25
        FarmMaxTime := 35
    }
}

; ============ STATE TRACKING ============
global BotRunTime := 0
global LastAFK := 0
global NextBreak := 0
global IsPaused := false
global SessionStart := A_TickCount
global LogFile := "anti_detect_client" . ClientID . ".log"

; Initialize
Random, NextBreak, %FarmMinTime%, %FarmMaxTime%
FileDelete, %LogFile%
LogEvent("Started - " . ClientName)

; ============ TIMERS ============
SetTimer, BehaviorChecker, 60000  ; Every minute
SetTimer, UpdateStatus, 5000      ; Every 5 seconds

#IfWinActive, MapleStory

; ============ SKILL KEYS WITH FULL ANTI-DETECTION ============
q::
w::
e::
r::
1::
2::
3::
4::
    if (IsPaused)
        return
    
    key := A_ThisHotkey
    
    ; Skill miss simulation (human imperfection)
    Random, miss, 1, 100
    if (miss <= SkillMissRate) {
        LogEvent("MISS: " . key)
        return  ; Don't send key
    }
    
    ; Gaussian delay
    delay := GaussianRandom(SkillDelayMean, SkillDelayStdDev)
    Sleep, %delay%
    
    ; Send key
    Send {%key%}
    LogEvent("Skill: " . key . " (delay: " . delay . "ms)")
    return

; ============ MOVEMENT KEYS ============
Left::
Right::
Up::
Down::
    if (IsPaused)
        return
    
    key := A_ThisHotkey
    delay := GaussianRandom(MovementDelayMean, MovementDelayStdDev)
    Sleep, %delay%
    Send {%key%}
    return

Alt::
Space::
    if (IsPaused)
        return
    
    key := A_ThisHotkey
    delay := GaussianRandom(MovementDelayMean - 20, MovementDelayStdDev - 10)
    Sleep, %delay%
    Send {%key%}
    return

#IfWinActive

; ============ BEHAVIOR CHECKER (EVERY MINUTE) ============
BehaviorChecker:
    if (!WinActive("MapleStory"))
        return
    
    BotRunTime += 1
    
    ; Check for mandatory break
    if (BotRunTime >= NextBreak) {
        MandatoryBreak()
        return
    }
    
    ; Random short AFK
    Random, afkRoll, 1, 100
    if (afkRoll <= AFKChance and !IsPaused) {
        RandomAFK()
    }
    
    ; Random human-like action
    if (BotRunTime - LastAFK >= 5) {
        Random, actionRoll, 1, 100
        if (actionRoll <= 20) {  ; 20% chance
            RandomHumanAction()
            LastAFK := BotRunTime
        }
    }
    return

; ============ UPDATE STATUS ============
UpdateStatus:
    elapsed := Floor((A_TickCount - SessionStart) / 60000)
    nextBreak := NextBreak - BotRunTime
    ToolTip, [%ClientName%] Runtime: %elapsed%m | Break in: %nextBreak%m
    return

; ============ RANDOM AFK (HUMAN-LIKE PAUSES) ============
RandomAFK() {
    global IsPaused, LogFile
    
    Random, duration, 20, 180  ; 20s - 3min
    IsPaused := true
    LogEvent("Random AFK: " . duration . "s")
    
    ToolTip, [HUMAN BEHAVIOR] Random pause (%duration%s)
    Sleep, %duration%000
    
    IsPaused := false
    ToolTip
}

; ============ RANDOM HUMAN ACTIONS ============
RandomHumanAction() {
    global LogFile, ClientID
    
    ; Different action sets per client (personality!)
    Random, action, 1, 12
    
    if (ClientID = 1) {
        ; Client 1: Fast, efficient actions
        if (action == 1) {
            LogEvent("Human: Quick jump")
            Send {Space}
        }
        else if (action == 2) {
            LogEvent("Human: Double jump")
            Send {Space}
            Sleep, 200
            Send {Space}
        }
        else if (action == 3) {
            LogEvent("Human: Inventory check")
            Send {i}
            Random, delay, 800, 1500
            Sleep, %delay%
            Send {Esc}
        }
        else {
            LogEvent("Human: Quick pause")
            Random, delay, 1000, 3000
            Sleep, %delay%
        }
    }
    else if (ClientID = 2) {
        ; Client 2: Balanced, varied actions
        if (action <= 3) {
            LogEvent("Human: Map check")
            Send {m}
            Random, delay, 2000, 4000
            Sleep, %delay%
            Send {Esc}
        }
        else if (action <= 6) {
            LogEvent("Human: Equipment check")
            Send {e}
            Random, delay, 1500, 3000
            Sleep, %delay%
            Send {Esc}
        }
        else if (action <= 9) {
            LogEvent("Human: Random movement")
            Random, dir, 1, 2
            key := (dir == 1) ? "Left" : "Right"
            Random, duration, 300, 800
            Send {%key% down}
            Sleep, %duration%
            Send {%key% up}
        }
        else {
            LogEvent("Human: Standing still")
            Random, delay, 2000, 6000
            Sleep, %delay%
        }
    }
    else {
        ; Client 3: Casual, lots of "confusion"
        if (action <= 2) {
            LogEvent("Human: Multiple jumps")
            Loop, 3 {
                Send {Space}
                Random, delay, 250, 500
                Sleep, %delay%
            }
        }
        else if (action <= 4) {
            LogEvent("Human: Back and forth")
            Send {Left down}
            Sleep, 600
            Send {Left up}
            Sleep, 200
            Send {Right down}
            Sleep, 600
            Send {Right up}
        }
        else if (action <= 7) {
            LogEvent("Human: UI browsing")
            Send {i}
            Sleep, 1000
            Send {Esc}
            Sleep, 500
            Send {k}  ; Skills
            Sleep, 1500
            Send {Esc}
        }
        else {
            LogEvent("Human: Long confusion")
            Random, delay, 4000, 10000
            Sleep, %delay%
        }
    }
}

; ============ MANDATORY BREAK ============
MandatoryBreak() {
    global IsPaused, BotRunTime, NextBreak
    global BreakMinTime, BreakMaxTime, FarmMinTime, FarmMaxTime, LogFile
    
    Random, breakDuration, %BreakMinTime%, %BreakMaxTime%
    IsPaused := true
    
    LogEvent("MANDATORY BREAK: " . breakDuration . " minutes")
    ToolTip, [BREAK TIME] %breakDuration% minute break...
    
    Sleep, %breakDuration%0000
    
    IsPaused := false
    
    ; Schedule next break (variable!)
    Random, nextFarm, %FarmMinTime%, %FarmMaxTime%
    NextBreak := BotRunTime + nextFarm
    
    LogEvent("Break ended. Next break in " . nextFarm . " minutes")
    ToolTip
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
    
    ; Clamp to reasonable range
    if (result < 20)
        result := 20
    if (result > 500)
        result := 500
    
    return result
}

; ============ LOGGING ============
LogEvent(message) {
    global LogFile
    FormatTime, timestamp, , yyyy-MM-dd HH:mm:ss
    FileAppend, [%timestamp%] %message%`n, %LogFile%
}

; ============ MANUAL CONTROLS ============
^!p::  ; Ctrl+Alt+P to pause/resume
    IsPaused := !IsPaused
    status := IsPaused ? "PAUSED" : "RESUMED"
    LogEvent("Manual " . status)
    ToolTip, %status%
    SetTimer, RemoveToolTip, 2000
    return

^!q::  ; Ctrl+Alt+Q to quit
    LogEvent("Script terminated")
    ExitApp

RemoveToolTip:
    SetTimer, RemoveToolTip, Off
    ToolTip
    return




