@echo off
cd /d "%~dp0"
echo ====================================================================
echo DRUM VISUALIZATION AUTO TRIGGER SYSTEM
echo ====================================================================
echo.

echo [1/3] Installing Auto Trigger dependencies...
pip install -r auto_trigger_requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/3] Starting Auto Trigger System...
echo.
echo 📁 Auto Trigger will monitor: %~dp0\audio-workspace
echo 🌐 Web interface: http://localhost:8080
echo 📝 Log file: auto_trigger.log
echo.
echo 💡 Drop audio files into the audio-workspace folder to process them automatically
echo.

python auto_trigger.py
pause