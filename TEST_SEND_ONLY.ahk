; ═══════════════════════════════════════════════════════════
; TEST SEND COMMAND - CỰC ĐƠN GIẢN!
; ═══════════════════════════════════════════════════════════
; Test xem Send command có hoạt động không
; ═══════════════════════════════════════════════════════════

#SingleInstance Force

MsgBox, 
(
TEST SEND COMMAND

Khi bấm Q:
1. Script chặn Q
2. Hiện tooltip "Sending Q..."
3. Send Q với delay 1 giây
4. Q sẽ xuất hiện sau 1 giây

Test trong Notepad!
Press ESC to exit.
)

q::
    ToolTip, Sending Q in 1 second...
    Sleep, 1000
    Send, q
    ToolTip
    return

Esc::
    ExitApp

