@echo off
cd /d "%~dp0"
echo ====================================================================
echo DRUM VISUALIZATION SYSTEM - FULL PROCESS TRIGGER
echo ====================================================================
echo.

:: Navigate to backend and activate virtual environment
cd backend
echo [1/4] Activating Python virtual environment...
call venv\Scripts\activate

:: Navigate to audio workspace and process audio
cd ..\audio-workspace
echo [2/4] Processing audio file...
python process_track.py track.wav
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Audio processing failed.
    pause
    exit /b %ERRORLEVEL%
)

:: Copy drum data to frontend
echo [3/4] Copying drum data to frontend...
copy drum-data.json ..\frontend\public\
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to copy drum data.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ====================================================================
echo PROCESS COMPLETE - System is now running!
echo ====================================================================
echo.
echo 1. Open your browser and navigate to: http://localhost:5173/overlay.html
echo 2. The logo should be animating with the drum hits
echo 3. To process a new track, stop this script (Ctrl+C) and run again
echo.

:: Navigate to frontend and start dev server
echo [4/4] Starting frontend development server...
cd ..\frontend
npm run dev
pause