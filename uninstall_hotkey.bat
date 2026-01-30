@echo off
echo ====================================================================
echo DRUM VISUALIZATION SYSTEM - HOTKEY UNINSTALLATION
echo ====================================================================
echo.

:: Stop any running AutoHotkey scripts
echo [1/2] Stopping hotkey trigger...
taskkill /f /im AutoHotkey.exe >nul 2>&1

:: Remove the script from startup folder
echo [2/2] Uninstalling hotkey trigger...
set "startup=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
if exist "%startup%\drum_visualization_hotkey.ahk" (
    del "%startup%\drum_visualization_hotkey.ahk" >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Failed to remove hotkey script from startup folder.
        pause
        exit /b %ERRORLEVEL%
    )
)

echo.
echo ====================================================================
echo HOTKEY UNINSTALLATION COMPLETE!
echo ====================================================================
echo.
echo The hotkey trigger has been removed from startup.
echo The Ctrl+Alt+D hotkey is no longer active.
echo.
echo To reinstall, run: install_hotkey.bat
echo.
pause