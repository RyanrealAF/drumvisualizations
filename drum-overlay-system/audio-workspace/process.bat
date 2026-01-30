@echo off
echo [1/4] Activating Python virtual environment...
call ..\backend\venv\Scripts\activate
if %errorlevel% neq 0 (
    echo ERROR: Could not activate virtual environment.
    echo Please ensure you are running this script from the 'audio-workspace' folder.
    pause
    exit /b
)

echo [2/4] Processing audio file...
if not exist "track.wav" (
    echo ERROR: track.wav not found in audio-workspace.
    echo Please copy your audio file here and rename it to 'track.wav'.
    pause
    exit /b
)

python process_track.py track.wav
if %errorlevel% neq 0 (
    echo ERROR: Audio processing failed.
    pause
    exit /b
)

echo [3/4] Copying drum data to frontend...
if not exist "..\frontend\public\" (
    echo Creating frontend public directory...
    mkdir "..\frontend\public\"
)
copy /Y drum-data.json ..\frontend\public\
if %errorlevel% neq 0 (
    echo ERROR: Failed to copy drum data.
    echo Ensure the '..\frontend\public\' directory exists.
    pause
    exit /b
)

echo.
echo [4/4] SUCCESS!
echo Data generated and copied to frontend.
pause