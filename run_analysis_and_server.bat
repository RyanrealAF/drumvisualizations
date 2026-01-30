@echo off
echo === Drum Visualization: Analysis & Server ===

REM Navigate to subproject if it exists
if exist "drum-logo-overlay" (
    echo Entering drum-logo-overlay...
    cd drum-logo-overlay
)

REM Run Analysis
if exist "analyze_drums.py" (
    echo Running Analysis...
    python analyze_drums.py
) else (
    echo Error: analyze_drums.py not found.
    pause
    exit /b
)

REM Start Server
if exist "server.py" (
    echo Starting Server...
    python server.py
) else (
    echo Error: server.py not found.
    pause
)