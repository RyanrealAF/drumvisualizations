; AutoHotkey script to trigger the drum visualization system
; Hotkey: Ctrl+Alt+D

^!d::
    ; Show a notification first
    TrayTip, Drum Visualization System, Process started! Check console for output., 5, 1
    
    ; Wait a moment for the notification to appear
    Sleep, 1000
    
    ; Run the full process batch file from the project directory
    Run, C:\projects\drumvisualizations\run_full_process.bat, C:\projects\drumvisualizations
return

; Double-click tray icon to exit
#SingleInstance Force
OnExit("ExitSub")
ExitSub() {
    TrayTip, Drum Visualization System, Hotkey trigger stopped., 5, 1
    ExitApp
}