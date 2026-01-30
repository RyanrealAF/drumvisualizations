@echo off
echo [1/4] Activating Python virtual environment...
REM Check if venv exists in backend directory
if exist "..\backend\venv\Scripts\activate.bat" (
    call "..\backend\venv\Scripts\activate"
) else (
    echo WARNING: Virtual environment not found. Using system Python.
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
    mkdir "..\frontend\public"
)

if exist "drum-data.json" (
    copy /Y "drum-data.json" "..\frontend\public\"
    if %errorlevel% neq 0 (
        echo ERROR: Failed to copy drum data.
        echo Ensure the '..\frontend\public\' directory exists.
        pause
        exit /b
    )
    echo Drum data copied successfully.
) else (
    echo ERROR: drum-data.json not generated.
    pause
    exit /b
)

echo.
echo [4/4] SUCCESS!
echo Data generated and copied to frontend.

pause