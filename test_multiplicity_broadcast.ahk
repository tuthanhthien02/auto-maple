; ═══════════════════════════════════════════════════════════
; MULTIPLICITY BROADCAST TEST SCRIPT
; ═══════════════════════════════════════════════════════════
; Purpose: Verify Multiplicity broadcast mode is working
; Run this on PRIMARY PC ONLY
; ═══════════════════════════════════════════════════════════

#SingleInstance Force
#NoEnv
SetWorkingDir %A_ScriptDir%

MsgBox, 4, Multiplicity Test, 
(
MULTIPLICITY BROADCAST TEST
═══════════════════════════

This script will test if Multiplicity broadcast is working correctly.

SETUP:
1. Launch MapleStory on all 3 clients
2. Login to character select screen on all clients
3. Enable Multiplicity broadcast mode (Ctrl+Shift+B)
4. Make sure all client windows are visible

READY TO START?

Click YES when ready, NO to cancel.
)

IfMsgBox No
{
    ExitApp
}

; ============ TEST SEQUENCE ============

ToolTip, TEST 1: Arrow Keys (5 seconds)
Sleep, 2000

; Test arrow keys
Loop, 5 {
    Send {Right}
    Sleep, 300
    Send {Left}
    Sleep, 300
}

ToolTip, TEST 2: Jump Key (5 seconds)
Sleep, 1000

; Test jump
Loop, 5 {
    Send {Alt}
    Sleep, 500
}

ToolTip, TEST 3: Skill Keys (5 seconds)
Sleep, 1000

; Test skill keys Q, W, E
Send {q}
Sleep, 1000
Send {w}
Sleep, 1000
Send {e}
Sleep, 1000

ToolTip, TEST 4: Number Keys (5 seconds)
Sleep, 1000

; Test number keys
Loop, 4 {
    Send %A_Index%
    Sleep, 800
}

ToolTip, TEST COMPLETE!
Sleep, 2000

; ============ RESULTS ============

MsgBox, 4, Test Results, 
(
MULTIPLICITY BROADCAST TEST COMPLETE!
═══════════════════════════════════════

VERIFY RESULTS:

Did ALL 3 clients perform the SAME actions?

✅ Arrow keys: Characters moved left/right
✅ Jump: All characters jumped
✅ Skills: All used Q, W, E skills
✅ Numbers: All pressed 1, 2, 3, 4

If ALL actions synchronized across all 3 clients:
  → Click YES (Layer 1 SUCCESS!)

If only 1 client responded OR actions were different:
  → Click NO (Need troubleshooting)
)

IfMsgBox Yes
{
    FileAppend, [%A_Now%] Layer 1 Test: PASSED`n, multiplicity_test_log.txt
    MsgBox, 64, SUCCESS!, 
    (
    ✅ LAYER 1 VERIFICATION: PASSED
    ═══════════════════════════════════
    
    Multiplicity broadcast is working correctly!
    
    NEXT STEPS:
    → Review LAYER_1_MULTIPLICITY_SETUP_GUIDE.md
    → Complete checklist
    → Ready to move to Layer 2!
    
    Log saved to: multiplicity_test_log.txt
    )
}
Else
{
    FileAppend, [%A_Now%] Layer 1 Test: FAILED`n, multiplicity_test_log.txt
    MsgBox, 48, TROUBLESHOOTING NEEDED, 
    (
    ⚠️ LAYER 1 VERIFICATION: FAILED
    ═══════════════════════════════════
    
    Multiplicity broadcast is NOT working correctly.
    
    COMMON ISSUES:
    1. Broadcast mode not enabled (Ctrl+Shift+B)
    2. Wrong clients selected in broadcast targets
    3. Network connection issues
    4. Firewall blocking Multiplicity
    5. Clients not connected to primary
    
    SOLUTIONS:
    → Review "TROUBLESHOOTING" section in guide
    → Verify all clients show "Connected" status
    → Check broadcast settings (all 3 clients checked)
    → Restart Multiplicity on all PCs
    
    Log saved to: multiplicity_test_log.txt
    )
}

ToolTip
ExitApp



