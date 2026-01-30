# PowerShell script to install AutoHotkey
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

# Check if AutoHotkey is already installed
$autoHotkeyPath = "C:\Program Files\AutoHotkey"
if (Test-Path -Path $autoHotkeyPath) {
    $exePath = Join-Path -Path $autoHotkeyPath -ChildPath "AutoHotkey.exe"
    if (Test-Path -Path $exePath) {
        Write-Status "AutoHotkey is already installed at: $exePath" -Success
        return $true
    }
}

# Download AutoHotkey installer
$downloadUrl = "https://github.com/AutoHotkey/AutoHotkey/releases/download/v2.0.10/AutoHotkey_2.0.10_setup.exe"
$installerPath = Join-Path -Path $env:TEMP -ChildPath "AutoHotkey_setup.exe"

Write-Status "Downloading AutoHotkey installer from: $downloadUrl"

try {
    $progressPreference = 'SilentlyContinue'
    Invoke-WebRequest -Uri $downloadUrl -OutFile $installerPath -UseBasicParsing
    Write-Status "Download completed: $installerPath" -Success
} catch {
    Write-Status "Failed to download AutoHotkey installer: $_" -Error
    return $false
}

# Install AutoHotkey
Write-Status "Installing AutoHotkey..."

try {
    $process = Start-Process -FilePath $installerPath -ArgumentList "/S" -Wait -PassThru
    if ($process.ExitCode -eq 0) {
        Write-Status "AutoHotkey installed successfully" -Success
    } else {
        Write-Status "AutoHotkey installation failed with exit code: $($process.ExitCode)" -Error
        if (Test-Path -Path $installerPath) {
            Remove-Item -Path $installerPath -Force
        }
        return $false
    }
} catch {
    Write-Status "Failed to install AutoHotkey: $_" -Error
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
        Write-Status "AutoHotkey is now available at: $exePath" -Success
        return $true
    }
}

Write-Status "AutoHotkey installation verification failed" -Error
return $false