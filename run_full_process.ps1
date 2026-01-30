# ===================================================================
# DRUM VISUALIZATION SYSTEM - FULL PROCESS TRIGGER
# PowerShell Version
# ===================================================================
Write-Host "====================================================================" -ForegroundColor Green
Write-Host "DRUM VISUALIZATION SYSTEM - FULL PROCESS TRIGGER" -ForegroundColor Green
Write-Host "====================================================================" -ForegroundColor Green
Write-Host ""

# Get current directory
$projectRoot = Get-Location
Write-Host "[1/4] Current directory: $projectRoot" -ForegroundColor Cyan

# Check if we're in the right directory
if (-not (Test-Path ".\audio-workspace\process_track.py")) {
    Write-Host "ERROR: Please navigate to the drum-overlay-system directory first" -ForegroundColor Red
    Write-Host "Run: cd drum-overlay-system" -ForegroundColor Yellow
    exit 1
}

# Check for audio file
$audioFile = Join-Path $projectRoot "audio-workspace\track.wav"
if (-not (Test-Path $audioFile)) {
    Write-Host "ERROR: Audio file '$audioFile' not found" -ForegroundColor Red
    Write-Host "Please copy your WAV file to the audio-workspace folder and name it 'track.wav'" -ForegroundColor Yellow
    exit 1
}

# Check for virtual environment
$venvPath = Join-Path $projectRoot "backend\venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "WARNING: Virtual environment not found. Creating one..." -ForegroundColor Yellow
    try {
        Set-Location (Join-Path $projectRoot "backend")
        python -m venv venv
        . .\venv\Scripts\Activate.ps1
        Write-Host "✓ Virtual environment created" -ForegroundColor Green
    }
    catch {
        Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}
else {
    try {
        . .\backend\venv\Scripts\Activate.ps1
        Write-Host "✓ Virtual environment activated" -ForegroundColor Green
    }
    catch {
        Write-Host "ERROR: Failed to activate virtual environment" -ForegroundColor Red
        exit 1
    }
}

# Install Python dependencies
Write-Host "[2/4] Installing Python dependencies..." -ForegroundColor Cyan
try {
    pip install --upgrade pip setuptools wheel
    pip install demucs librosa soundfile numpy scipy
    Write-Host "✓ Python dependencies installed" -ForegroundColor Green
}
catch {
    Write-Host "ERROR: Failed to install Python dependencies" -ForegroundColor Red
    exit 1
}

# Process audio
Write-Host "[3/4] Processing audio file..." -ForegroundColor Cyan
Set-Location (Join-Path $projectRoot "audio-workspace")
try {
    python process_track.py track.wav
    Write-Host "✓ Audio processing complete" -ForegroundColor Green
}
catch {
    Write-Host "ERROR: Audio processing failed" -ForegroundColor Red
    exit 1
}

# Copy drum data to frontend
Write-Host "[4/4] Copying drum data to frontend..." -ForegroundColor Cyan
$drumData = Join-Path $projectRoot "audio-workspace\drum-data.json"
$frontendData = Join-Path $projectRoot "frontend\public\drum-data.json"
if (Test-Path $drumData) {
    Copy-Item $drumData $frontendData -Force
    Write-Host "✓ Drum data copied to frontend" -ForegroundColor Green
}
else {
    Write-Host "ERROR: Drum data file not found" -ForegroundColor Red
    exit 1
}

# Start frontend server
Write-Host "[5/5] Starting frontend development server..." -ForegroundColor Cyan
Set-Location (Join-Path $projectRoot "frontend")
try {
    npm install
    npm run dev
    Write-Host "✓ Frontend server started" -ForegroundColor Green
}
catch {
    Write-Host "ERROR: Failed to start frontend server" -ForegroundColor Red
    exit 1
}

# Keep terminal open
Write-Host ""
Write-Host "====================================================================" -ForegroundColor Green
Write-Host "PROCESS COMPLETE - System is now running!" -ForegroundColor Green
Write-Host "====================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "1. Open your browser and navigate to: http://localhost:5173/overlay.html" -ForegroundColor Yellow
Write-Host "2. The logo should be animating with the drum hits" -ForegroundColor Yellow
Write-Host "3. To process a new track, stop this script (Ctrl+C) and run again" -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to exit..."