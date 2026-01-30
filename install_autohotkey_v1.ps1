# PowerShell script to install AutoHotkey v1
param (
    [switch]$Quiet = $false
)

function Write-Status {
    param (
        [string]$Message,
        [switch]$Error = $false,
        [switch]$Success = $false
    )

    if (-not $Quiet) {
        if ($Error) {
            Write-Host "ERROR: $Message" -ForegroundColor Red
        } elseif ($Success) {
            Write-Host "SUCCESS: $Message" -ForegroundColor Green
        } else {
            Write-Host "INFO: $Message" -ForegroundColor Cyan
        }
    }
}

# Check if AutoHotkey v1 is already installed
$autoHotkeyPath = "C:\Program Files\AutoHotkey"
if (Test-Path -Path $autoHotkeyPath) {
    $exePath = Join-Path -Path $autoHotkeyPath -ChildPath "AutoHotkey.exe"
    if (Test-Path -Path $exePath) {
        Write-Status "AutoHotkey v1 is already installed at: $exePath" -Success
        return $true
    }
}

# Download AutoHotkey v1 installer
$downloadUrl = "https://github.com/Lexikos/AutoHotkey_L/releases/download/v1.1.37.01/AutoHotkey_1.1.37.01_setup.exe"
$installerPath = Join-Path -Path $env:TEMP -ChildPath "AutoHotkey_v1_setup.exe"

Write-Status "Downloading AutoHotkey v1 installer from: $downloadUrl"

try {
    $progressPreference = 'SilentlyContinue'
    Invoke-WebRequest -Uri $downloadUrl -OutFile $installerPath -UseBasicParsing
    Write-Status "Download completed: $installerPath" -Success
} catch {
    Write-Status "Failed to download AutoHotkey v1 installer: $_" -Error
    return $false
}

# Install AutoHotkey v1
Write-Status "Installing AutoHotkey v1..."

try {
    $process = Start-Process -FilePath $installerPath -ArgumentList "/S" -Wait -PassThru
    if ($process.ExitCode -eq 0) {
        Write-Status "AutoHotkey v1 installed successfully" -Success
    } else {
        Write-Status "AutoHotkey v1 installation failed with exit code: $($process.ExitCode)" -Error
        if (Test-Path -Path $installerPath) {
            Remove-Item -Path $installerPath -Force
        }
        return $false
    }
} catch {
    Write-Status "Failed to install AutoHotkey v1: $_" -Error
    if (Test-Path -Path $installerPath) {
        Remove-Item -Path $installerPath -Force
    }
    return $false
}

# Cleanup installer
if (Test-Path -Path $installerPath) {
    Remove-Item -Path $installerPath -Force
}

# Verify installation
if (Test-Path -Path $autoHotkeyPath) {
    $exePath = Join-Path -Path $autoHotkeyPath -ChildPath "AutoHotkey.exe"
    if (Test-Path -Path $exePath) {
        Write-Status "AutoHotkey v1 is now available at: $exePath" -Success
        return $true
    }
}

Write-Status "AutoHotkey v1 installation verification failed" -Error
return $false