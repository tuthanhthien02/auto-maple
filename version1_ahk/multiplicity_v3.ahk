#NoEnv
#SingleInstance Force
SetBatchLines, -1
SendMode Input

global SettingsFile := A_ScriptDir . "\settings.ini"
global USE_SETTINGS_INI := true

global ScriptEnabled := true
global remapEnabled := true
global jitterEnabled := true
global arrowJitterEnabled := true
global MinJitter := 10
global MaxJitter := 50
global UseGaussian := false

global remap := {}

LoadDefaultRemap()
LoadSettings()
RegisterRemapHotkeys()
SetTimer, RefreshHotkeys, 5000
RefreshHotkeys:
    RegisterRemapHotkeys()
Return


Return

; -----------------------------------------------------------------------------
; Hotkeys

End::
    remapEnabled := !remapEnabled
    SoundBeep, remapEnabled ? 1000 : 500, 120
    ToolTip, % remapEnabled ? "Remap: ENABLED" : "Remap: DISABLED", 0, 0
    SetTimer, RemoveTooltip, 1500
Return

PgDn::
    status := "=== REMAP STATUS ===`n"
    status .= "Remap: " . (remapEnabled ? "ENABLED" : "DISABLED") . "`n"
    status .= "Jitter: " . (jitterEnabled ? "ON" : "OFF") . " (" . MinJitter . "-" . MaxJitter . " ms)`n"
    status .= "Arrow jitter: " . (arrowJitterEnabled ? "ON" : "OFF")
    ToolTip, %status%, 0, 0
    SetTimer, RemoveTooltip, 3000
Return

PgUp::
    ReleaseHeldArrows()
    ExitApp
Return

RemoveTooltip:
    ToolTip
    SetTimer, RemoveTooltip, Off
Return

; -----------------------------------------------------------------------------
; Hotkey helpers

RegisterRemapHotkeys() {
    global remap
    for key, value in remap {
        if (value = "")
            continue
        Hotkey, *$%key%, HandleKeyDown
        Hotkey, *$%key% up, HandleKeyUp
    }
}

HandleKeyDown:
    global ScriptEnabled, remapEnabled, remap
    global jitterEnabled, arrowJitterEnabled, MinJitter, MaxJitter, UseGaussian

    if (!ScriptEnabled || !remapEnabled)
        return

    pressedKey := NormalizeHotkey(A_ThisHotkey)
    targetKey := remap[pressedKey]
    if (targetKey = "")
        return

    targetVK := GetKeyVK(targetKey)
    targetSC := GetKeySC(targetKey)
    if (targetVK = "" || targetSC = "")
        return

    vkHex := Format("{:02X}", targetVK)
    scHex := Format("{:03X}", targetSC)

    isArrow := (targetKey = "Left" || targetKey = "Right" || targetKey = "Up" || targetKey = "Down")

    ; Apply jitter delay before sending input
    if (isArrow ? arrowJitterEnabled : jitterEnabled) {
        if (UseGaussian) {
            mean := (MinJitter + MaxJitter) / 2.0
            stdDev := (MaxJitter - MinJitter) / 6.0
            delay := GaussianRandom(mean, stdDev, MinJitter, MaxJitter)
        } else {
            Random, delay, %MinJitter%, %MaxJitter%
        }
        Sleep, %delay%
    }

    if (isArrow) {
        SendInput, {Blind}{vk%vkHex%sc%scHex% down}
    } else {
        SendInput, {Blind}{vk%vkHex%sc%scHex%}
    }
Return

HandleKeyUp:
    global ScriptEnabled, remapEnabled, remap

    if (!ScriptEnabled || !remapEnabled)
        return

    pressedKey := NormalizeHotkey(A_ThisHotkey)
    targetKey := remap[pressedKey]
    if (targetKey = "")
        return

    if !(targetKey = "Left" || targetKey = "Right" || targetKey = "Up" || targetKey = "Down")
        return

    targetVK := GetKeyVK(targetKey)
    targetSC := GetKeySC(targetKey)
    if (targetVK = "" || targetSC = "")
        return

    vkHex := Format("{:02X}", targetVK)
    scHex := Format("{:03X}", targetSC)
    SendInput, {Blind}{vk%vkHex%sc%scHex% up}
Return

NormalizeHotkey(hotkey) {
    hotkey := StrReplace(hotkey, "*$")
    hotkey := StrReplace(hotkey, "$")
    hotkey := StrReplace(hotkey, "*")
    hotkey := StrReplace(hotkey, " up")
    return hotkey
}

ReleaseHeldArrows() {
    for index, key in ["Left", "Right", "Up", "Down"] {
        vk := GetKeyVK(key)
        sc := GetKeySC(key)
        if (vk = "" || sc = "")
            continue
        vkHex := Format("{:02X}", vk)
        scHex := Format("{:03X}", sc)
        SendInput, {Blind}{vk%vkHex%sc%scHex% up}
    }
}

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

; -----------------------------------------------------------------------------
; Settings loading

LoadSettings() {
    global SettingsFile, USE_SETTINGS_INI
    global ScriptEnabled, remapEnabled, jitterEnabled, arrowJitterEnabled
    global MinJitter, MaxJitter, UseGaussian

    if (!USE_SETTINGS_INI)
        return

    if (!FileExist(SettingsFile))
        return

    IniRead, ScriptEnabled, %SettingsFile%, Script, Enabled, 1
    IniRead, remapEnabled, %SettingsFile%, Script, RemapEnabled, 1
    IniRead, jitterFlag, %SettingsFile%, Jitter, Enabled, 1
    IniRead, arrowFlag, %SettingsFile%, ArrowKeys, Enabled, 1
    IniRead, MinJitter, %SettingsFile%, Jitter, MinDelay, 10
    IniRead, MaxJitter, %SettingsFile%, Jitter, MaxDelay, 50
    IniRead, UseGaussian, %SettingsFile%, Jitter, UseGaussian, 0

    ScriptEnabled := ScriptEnabled ? true : false
    remapEnabled := remapEnabled ? true : false
    jitterEnabled := (jitterFlag + 0) != 0
    arrowJitterEnabled := (arrowFlag + 0) != 0
    UseGaussian := UseGaussian ? true : false

    LoadRemapFromSettings()
}

LoadRemapFromSettings() {
    global SettingsFile, remap

    Loop, Read, %SettingsFile%
    {
        line := A_LoopReadLine
        if (line = "[Remap]") {
            inRemap := true
            continue
        }
        if (InStr(line, "[") = 1) {
            inRemap := false
        }
        if (!inRemap)
            continue
        if (line = "" || SubStr(line, 1, 1) = ";")
            continue
        if (InStr(line, "=")) {
            StringSplit, parts, line, =
            if (parts0 = 2) {
                key := Trim(parts1)
                value := Trim(parts2)
                remap[key] := value
            }
        }
    }
}

LoadDefaultRemap() {
    global remap
    remap := {}
    remap["q"] := "]"
    remap["w"] := "["
    remap["e"] := "p"
    remap["r"] := "o"
    remap["a"] := "i"
    remap["s"] := "u"
    remap["d"] := "y"
    remap["f"] := "t"
    remap["p"] := "="
    remap["i"] := "-"
    remap["u"] := "0"
    remap["z"] := "r"
    remap["c"] := "e"
    remap["k"] := "b"
    remap["Alt"] := "f"
    remap["Space"] := "d"
    remap["F1"] := "F12"
    remap["F2"] := "F11"
    remap["F3"] := "F10"
    remap["F4"] := "F9"
    remap["F9"] := "F1"
    remap["1"] := "9"
    remap["2"] := "8"
    remap["7"] := "2"
    remap["8"] := "1"
    remap["5"] := "4"
    remap["6"] := "v"
    remap["v"] := "6"
    remap["3"] := "c"
    remap["Numpad1"] := "Left"
    remap["Numpad2"] := "Down"
    remap["Numpad3"] := "Right"
    remap["Numpad5"] := "Up"
}

