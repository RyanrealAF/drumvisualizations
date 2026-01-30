@echo off
REM Drum Visualization Development Server Script
REM Starts all development servers for the project

echo === Drum Visualization Development Server ===
echo.

REM Kill any existing processes
echo Cleaning up existing processes...
taskkill /f /im "node.exe" >nul 2>&1
taskkill /f /im "python.exe" >nul 2>&1
timeout /t 2 /nobreak >nul

REM Start Main React Development Server
if exist "package.json" (
    echo Starting Main React App...
    start "DrumVis - Main App" cmd /k "npm run dev"
)

REM Start Frontend Subproject Development Server
if exist "drum-overlay-system\frontend\package.json" (
    echo Starting Frontend Subproject...
    start "DrumVis - Frontend" cmd /k "cd drum-overlay-system\frontend && npm run dev"
)

REM Start FastAPI Backend Server
if exist "drum-overlay-system\backend\main.py" (
    echo Starting FastAPI Backend...
    start "DrumVis - Backend" cmd /k "cd drum-overlay-system\backend && python main.py"
)

REM Start Python HTTP Server
if exist "server.py" (
    echo Starting Python HTTP Server...
    start "DrumVis - HTTP Server" cmd /k "python server.py"
)

echo.
echo All servers started!
echo.
echo URLs:
echo " Main React App: http://localhost:5173
echo " Frontend Subproject: http://localhost:5174
echo " FastAPI Backend: http://localhost:8000
echo " Python HTTP Server: http://localhost:8001
echo.
echo Press any key to stop all servers...
pause >nul

REM Cleanup
echo Stopping all servers...
taskkill /f /im "node.exe" >nul 2>&1
taskkill /f /im "python.exe" >nul 2>&1