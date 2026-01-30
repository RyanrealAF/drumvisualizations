@echo off
cd /d "%~dp0"
echo ====================================================================
echo DRUM VISUALIZATION SYSTEM - FRONTEND ONLY
echo ====================================================================
echo.

echo [1/2] Copying existing drum data to frontend...
if exist "audio-workspace\drum-data.json" (
    copy "audio-workspace\drum-data.json" "frontend\public\"
) else (
    echo WARNING: audio-workspace\drum-data.json not found. Run run_full_process.bat first.
)

echo.
echo ====================================================================
echo SYSTEM READY
echo ====================================================================
echo.
echo 1. Open your browser and navigate to: http://localhost:5173/overlay.html
echo 2. The logo should be animating with the drum hits
echo 3. To process a new track, run run_full_process.bat
echo.

:: Navigate to frontend and start dev server
echo [2/2] Starting frontend development server...
cd frontend
npm run dev
pause