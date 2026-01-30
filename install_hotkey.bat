@echo off
echo ====================================================================
echo DRUM VISUALIZATION SYSTEM - HOTKEY INSTALLATION
echo ====================================================================
echo.

:: Check if AutoHotkey is installed
if not exist "C:\Program Files\AutoHotkey\AutoHotkey.exe" (
    echo AutoHotkey is not installed. Attempting to install automatically...
    "%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -ExecutionPolicy Bypass -File install_autohotkey_v1.ps1
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo ====================================================================
        echo ERROR: AutoHotkey installation failed.
        echo ====================================================================
        echo.
        echo Please install AutoHotkey manually:
        echo 1. Go to https://www.autohotkey.com/download/
        echo 2. Download AutoHotkey v1.1 (not v2.0)
        echo 3. Run the installer and follow the instructions
        echo 4. After installation, run install_hotkey.bat again
        echo.
        echo Press any key to open the AutoHotkey download page...
        pause >nul
        start https://www.autohotkey.com/download/
        exit /b 1
    )
    echo.
)

:: Copy the hotkey script to the startup folder
echo [1/2] Installing hotkey trigger...
set "startup=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
copy create_hotkey_trigger.ahk "%startup%\drum_visualization_hotkey.ahk" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to copy hotkey script to startup folder.
    pause
    exit /b %ERRORLEVEL%
)

:: Start the hotkey script
echo [2/2] Starting hotkey trigger...
start "" "%startup%\drum_visualization_hotkey.ahk"

echo.
echo ====================================================================
echo HOTKEY INSTALLATION COMPLETE!
echo ====================================================================
echo.
echo Hotkey is now active: Ctrl+Alt+D
echo The script will start automatically on system boot.
echo.
echo To uninstall, run: uninstall_hotkey.bat
echo.
echo Press any key to view the full documentation...
pause >nul
start README_HOTKEY.md
exit /b 0