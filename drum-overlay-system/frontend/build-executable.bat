@echo off
echo Building Drum Visualization System Executable...
echo =============================================

cd /d "%~dp0"

echo Step 1: Building frontend...
npm run build
if %errorlevel% neq 0 (
    echo Frontend build failed!
    pause
    exit /b 1
)

echo Step 2: Checking Tauri installation...
npx tauri --version
if %errorlevel% neq 0 (
    echo Tauri CLI not found. Please install with: npm install -g @tauri-apps/cli
    pause
    exit /b 1
)

echo Step 3: Building Tauri application...
npx tauri build
if %errorlevel% neq 0 (
    echo Tauri build failed!
    echo You may need to:
    echo 1. Install Rust: https://rustup.rs/
    echo 2. Install Tauri CLI: npm install -g @tauri-apps/cli
    echo 3. Check tauri.conf.json configuration
    pause
    exit /b 1
)

echo.
echo Build completed successfully!
echo Executable location: src-tauri\target\release\bundle\
echo.
echo To run the application:
echo   src-tauri\target\release\bundle\*.exe
echo.
pause