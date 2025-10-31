#NoEnv
#SingleInstance Force
SetBatchLines, -1
SendMode Input
SetKeyDelay, -1, -1

; Hardcoded remap table (copy of current settings.ini)
global REMAP := {}
REMAP["q"] := "]"
REMAP["w"] := "["
REMAP["e"] := "p"
REMAP["r"] := "o"
REMAP["a"] := "i"
REMAP["s"] := "u"
REMAP["d"] := "y"
REMAP["f"] := "t"
REMAP["p"] := "="
REMAP["i"] := "-"
REMAP["u"] := "0"
REMAP["z"] := "r"
REMAP["c"] := "e"
REMAP["Alt"] := "f"
REMAP["Space"] := "d"
REMAP["Escape"] := "`"
REMAP["F1"] := "F12"
REMAP["F2"] := "F11"
REMAP["F3"] := "F10"
REMAP["F4"] := "F9"
REMAP["F9"] := "F1"
REMAP["k"] := "b"
REMAP["1"] := "9"
REMAP["2"] := "8"
REMAP["8"] := "1"
REMAP["7"] := "2"
REMAP["5"] := "4"
REMAP["6"] := "v"
REMAP["3"] := "c"
REMAP["v"] := "6"
REMAP["Numpad1"] := "Left"
REMAP["Numpad2"] := "Down"
REMAP["Numpad3"] := "Right"
REMAP["Numpad5"] := "Up"

global REMAP_ENABLED := true
global KEY_STATE := {}

; Register hotkeys
for source, target in REMAP {
    if (target = "")
        continue
    Hotkey, *$%source%, HandleKeyDown
    Hotkey, *$%source% up, HandleKeyUp
}

Return

; Hotkeys
End::
    REMAP_ENABLED := !REMAP_ENABLED
    SoundBeep, REMAP_ENABLED ? 1000 : 500, 120
    ToolTip, % REMAP_ENABLED ? "Remap: ENABLED" : "Remap: DISABLED", 0, 0
    SetTimer, ClearTooltip, 1500
Return

PgUp::
    ReleaseArrowKeys()
    ExitApp
Return

ClearTooltip:
    ToolTip
    SetTimer, ClearTooltip, Off
Return

; Main handlers
HandleKeyDown:
    global REMAP_ENABLED, REMAP, KEY_STATE

    if (!REMAP_ENABLED)
        return

    pressed := NormalizeHotkey(A_ThisHotkey)
    target := REMAP[pressed]
    if (target = "")
        return

    if (KEY_STATE.HasKey(pressed))
        return

    isArrow := IsArrow(target)
    state := {target: target, isArrow: isArrow}

    if (isArrow) {
        SendKeyDown(target)
    } else {
        SendTap(target)
        timerFn := Func("RepeatPress").Bind(pressed)
        state.timer := timerFn
        SetTimer, %timerFn%, 60
    }

    KEY_STATE[pressed] := state
Return

HandleKeyUp:
    global REMAP_ENABLED, REMAP, KEY_STATE

    if (!REMAP_ENABLED)
        return

    pressed := NormalizeHotkey(A_ThisHotkey)
    if (!KEY_STATE.HasKey(pressed))
        return

    state := KEY_STATE[pressed]
    if (state.HasKey("timer")) {
        timerFn := state.timer
        SetTimer, %timerFn%, Off
    }

    if (state.isArrow)
        SendKeyUp(state.target)

    KEY_STATE.Delete(pressed)
Return

; Helpers
NormalizeHotkey(key) {
    key := StrReplace(key, "*$")
    key := StrReplace(key, "$")
    key := StrReplace(key, "*")
    key := StrReplace(key, " up")
    return key
}

IsArrow(key) {
    return (key = "Left" || key = "Right" || key = "Up" || key = "Down")
}

SendKeyDown(key) {
    vk := GetKeyVK(key)
    sc := GetKeySC(key)
    if (vk = "" || sc = "")
        return
    vkHex := Format("{:02X}", vk)
    scHex := Format("{:03X}", sc)
    SendInput, {Blind}{vk%vkHex%sc%scHex% down}
}

SendKeyUp(key) {
    vk := GetKeyVK(key)
    sc := GetKeySC(key)
    if (vk = "" || sc = "")
        return
    vkHex := Format("{:02X}", vk)
    scHex := Format("{:03X}", sc)
    SendInput, {Blind}{vk%vkHex%sc%scHex% up}
}

SendTap(key) {
    SendKeyDown(key)
    Sleep, 20
    SendKeyUp(key)
}

RepeatPress(pressed) {
    global KEY_STATE
    if (!KEY_STATE.HasKey(pressed))
        return
    state := KEY_STATE[pressed]
    if (state.isArrow)
        return
    SendTap(state.target)
}

ReleaseArrowKeys() {
    global KEY_STATE
    for _, key in ["Left", "Right", "Up", "Down"]
        SendKeyUp(key)
    for key, state in KEY_STATE
    {
        if (state.isArrow)
            KEY_STATE.Delete(key)
    }
}

