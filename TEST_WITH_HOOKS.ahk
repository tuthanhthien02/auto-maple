; ═══════════════════════════════════════════════════════════
; TEST WITH KEYBOARD HOOKS AND SPECIAL SETTINGS
; ═══════════════════════════════════════════════════════════

#SingleInstance Force
#InstallKeybdHook
#UseHook
SetKeyDelay, -1, -1

MsgBox, 
(
TEST WITH KEYBOARD HOOKS

Settings enabled:
- #InstallKeybdHook (install keyboard hook)
- #UseHook (use hook for hotkeys)
- SetKeyDelay`, -1 (no delay)

Test in Notepad. Press Q.
Q should appear after 1 second.

Press ESC to exit.
)

q::
    ToolTip, Sending Q with hooks...
    Sleep, 1000
    SendInput, {q}
    ToolTip, Done!
    Sleep, 500
    ToolTip
    return

Esc::
    ExitApp

