; ═══════════════════════════════════════════════════════════
; SIMPLEST POSSIBLE TEST
; ═══════════════════════════════════════════════════════════

#SingleInstance Force

MsgBox, Script is running! Press Q to test. Press ESC to exit.

q::
    MsgBox, Q WAS PRESSED! Script is intercepting keys!
    return

Esc::
    ExitApp

