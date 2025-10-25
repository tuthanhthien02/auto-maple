; ═══════════════════════════════════════════════════════════
; TEST JITTER WITH DEBUG OUTPUT
; ═══════════════════════════════════════════════════════════

#SingleInstance Force
#NoEnv
SetWorkingDir %A_ScriptDir%
Random, Seed, A_TickCount

global MinJitter := 500
global MaxJitter := 1000

MsgBox, 
(
TEST JITTER - DEBUG VERSION

Sẽ hiện tooltip với từng bước:
1. "Q Pressed!"
2. "Sleeping Xms..."
3. "Sending Q..."
4. "Done!"

Mở Notepad và test!
Press ESC to exit.
)

q::
    ; Step 1: Show we caught Q
    ToolTip, Step 1: Q Pressed!
    Sleep, 200
    
    ; Step 2: Calculate jitter
    Random, jitter, %MinJitter%, %MaxJitter%
    ToolTip, Step 2: Sleeping %jitter%ms...
    Sleep, %jitter%
    
    ; Step 3: Send Q
    ToolTip, Step 3: Sending Q...
    Sleep, 200
    Send, q
    
    ; Step 4: Done
    ToolTip, Step 4: Done! Q sent!
    Sleep, 500
    ToolTip
    return

Esc::
    ExitApp

