# Drum Visualization System - Hotkey Trigger Setup

This guide explains how to set up the hotkey trigger for the Drum Visualization System.

## Prerequisites

### AutoHotkey (Required)

The hotkey functionality requires AutoHotkey to be installed. You can install it manually or use the automatic installation script.

## Installation Methods

### Method 1: Automatic Installation (Recommended)

1. Double-click `install_hotkey.bat`
2. The script will automatically download and install AutoHotkey v1 if it's not already installed
3. It will then set up the hotkey script to run on system startup
4. The hotkey (Ctrl+Alt+D) will be activated immediately

### Method 2: Manual Installation

#### Step 1: Download and Install AutoHotkey

1. Go to https://www.autohotkey.com/download/
2. Download the AutoHotkey v1.1 installer (not v2.0)
3. Run the installer and follow the installation wizard
4. Make sure AutoHotkey is installed in the default location (C:\Program Files\AutoHotkey)

#### Step 2: Install the Hotkey Script

1. Double-click `install_hotkey.bat`
2. The script will set up the hotkey script to run on system startup
3. The hotkey (Ctrl+Alt+D) will be activated immediately

## Usage

Once the hotkey is installed and activated:

1. Press **Ctrl+Alt+D** to trigger the drum visualization system
2. A notification will appear in the system tray indicating the process has started
3. Check the console window for detailed output

## Uninstallation

To uninstall the hotkey trigger:

1. Double-click `uninstall_hotkey.bat`
2. This will stop any running AutoHotkey scripts and remove the startup entry
3. The hotkey (Ctrl+Alt+D) will no longer be active

## Troubleshooting

### AutoHotkey Not Found Error

If you receive an error that AutoHotkey is not found:

1. Make sure AutoHotkey v1 is installed
2. Check that the installation path is correct (C:\Program Files\AutoHotkey)
3. Try restarting your computer
4. If all else fails, re-run the installation script

### Hotkey Not Working

If the hotkey doesn't work:

1. Check if AutoHotkey is running (look for the green "H" icon in the system tray)
2. If not, double-click `create_hotkey_trigger.ahk` to start it
3. Make sure the script is in the correct directory
4. Verify that you're using the correct hotkey combination (Ctrl+Alt+D)

### Script Not Starting on Boot

If the hotkey script doesn't start automatically when you boot your computer:

1. Check the startup folder: `C:\Users\<YourUsername>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`
2. There should be a file named `drum_visualization_hotkey.ahk` in this folder
3. If not, re-run the installation script

## Technical Details

### Hotkey Script Structure

The hotkey trigger is implemented as an AutoHotkey script (`create_hotkey_trigger.ahk`) with the following features:

- **Hotkey Combination**: Ctrl+Alt+D
- **Action**: Runs `run_full_process.bat`
- **Notification**: Shows a system tray notification when triggered
- **Tray Icon**: The green "H" icon in the system tray
- **Exiting**: Double-click the tray icon to stop the script

### Installation Scripts

- `install_hotkey.bat`: Automatically installs AutoHotkey and sets up the hotkey script
- `uninstall_hotkey.bat`: Removes the hotkey script and stops AutoHotkey
- `install_autohotkey_v1.ps1`: PowerShell script to download and install AutoHotkey v1

### File Locations

- Hotkey script: `C:\projects\drumvisualizations\create_hotkey_trigger.ahk`
- Startup script: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\drum_visualization_hotkey.ahk`
- AutoHotkey installation: `C:\Program Files\AutoHotkey`

## Additional Notes

- The hotkey script requires administrative privileges if your project folder is in a protected location
- You can customize the hotkey combination by editing `create_hotkey_trigger.ahk`
- For more information about AutoHotkey syntax, visit https://www.autohotkey.com/docs/