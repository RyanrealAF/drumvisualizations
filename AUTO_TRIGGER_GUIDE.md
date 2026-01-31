# Auto Trigger System - Complete Guide

## Overview

The Auto Trigger System is a comprehensive automation solution for the Drum Visualization System that automatically processes new audio files and updates the visualization in real-time.

## Features

### 🚀 **Automatic Processing**
- **File System Monitoring**: Watches the `audio-workspace` folder for new audio files
- **Real-time Processing**: Automatically processes files as soon as they're added
- **Format Support**: Handles WAV, MP3, FLAC, M4A, and OGG files
- **Smart Conversion**: Automatically converts non-WAV files to WAV format

### 🌐 **Web Interface**
- **Status Dashboard**: Real-time monitoring of the system status
- **Statistics Display**: Live hit counts for kicks, snares, and hats
- **Manual Controls**: Trigger processing manually when needed
- **System Logs**: View processing history and error messages

### 📝 **Logging & Monitoring**
- **Detailed Logs**: Comprehensive logging of all processing activities
- **Error Handling**: Robust error handling with detailed error messages
- **Processing History**: Track all processed files and their results

## Quick Start

### 1. **Install Dependencies**
```bash
# Windows
pip install -r auto_trigger_requirements.txt

# Mac/Linux
pip3 install -r auto_trigger_requirements.txt
```

### 2. **Start the System**
```bash
# Windows
start_auto_trigger.bat

# Mac/Linux
chmod +x start_auto_trigger.sh
./start_auto_trigger.sh
```

### 3. **Use the System**
1. **Drop audio files** into the `audio-workspace` folder
2. **Watch the magic happen** - files are processed automatically
3. **Monitor progress** via the web interface at `http://localhost:8080`
4. **View results** in your browser at `http://localhost:5173/overlay.html`

## System Architecture

```
📁 audio-workspace/
├── 📤 Drop audio files here (WAV, MP3, FLAC, etc.)
├── 🎵 track.wav (processed file)
└── 📊 drum-data.json (analysis results)

🌐 Web Interface (http://localhost:8080)
├── 📊 Real-time status dashboard
├── 📈 Live statistics
├── 🎛️ Manual controls
└── 📝 System logs

🔄 Processing Pipeline
├── 1️⃣ File Detection
├── 2️⃣ Format Conversion (if needed)
├── 3️⃣ Drum Analysis (Demucs + Librosa)
├── 4️⃣ Data Copy to Frontend
└── 5️⃣ Visualization Update
```

## File Processing Flow

### Step 1: File Detection
- **Event Monitoring**: Uses `watchdog` library to monitor file system events
- **Smart Filtering**: Only processes audio files (WAV, MP3, FLAC, M4A, OGG)
- **Debouncing**: Prevents processing incomplete files

### Step 2: Format Conversion
- **Automatic Detection**: Checks file extension to determine format
- **FFmpeg Integration**: Uses FFmpeg for high-quality audio conversion
- **WAV Output**: Converts all files to WAV format for processing

### Step 3: Audio Processing
- **Virtual Environment**: Activates Python virtual environment automatically
- **Demucs Separation**: Separates audio into stems (drums, bass, vocals, etc.)
- **Drum Analysis**: Analyzes drum hits using Librosa
- **Data Generation**: Creates `drum-data.json` with timing information

### Step 4: Frontend Update
- **File Copying**: Copies `drum-data.json` to frontend public directory
- **Real-time Update**: Frontend automatically detects and loads new data
- **Visualization**: Logo animates with the processed drum hits

## Web Interface Features

### Status Dashboard
- **System Status**: Shows if the system is running or stopped
- **Monitoring Path**: Displays which folder is being monitored
- **Last Update**: Shows timestamp of last file processing

### Statistics Panel
- **Kick Hits**: Count of detected kick drum hits
- **Snare Hits**: Count of detected snare drum hits  
- **Hat Hits**: Count of detected hi-hat hits

### Control Panel
- **Refresh Status**: Manual status refresh
- **Process Now**: Manual trigger for processing
- **Stop Server**: Gracefully stop the auto trigger system

### Log Viewer
- **Real-time Logs**: Live streaming of system logs
- **Error Messages**: Detailed error information
- **Processing History**: Complete history of file processing

## Command Line Usage

### Start the System
```bash
# Direct execution
python auto_trigger.py

# With custom project path
python auto_trigger.py --project-path /path/to/project
```

### View Help
```bash
python auto_trigger.py --help
```

## Configuration Options

### Monitoring Directory
By default, the system monitors `audio-workspace`. To change this:

```python
# In auto_trigger.py, modify:
audio_workspace = project_root / "your-custom-folder"
```

### Processing Thresholds
Adjust drum detection sensitivity in `process_track.py`:
```python
# Modify these values for different sensitivity
kick_delta = 0.8    # Lower = more sensitive
snare_delta = 0.6   # Lower = more sensitive  
hat_delta = 0.4     # Lower = more sensitive
```

### Web Server Port
Change the web interface port:
```python
# In auto_trigger.py, modify:
server_address = ('', 8081)  # Change 8080 to your preferred port
```

## Troubleshooting

### Common Issues

#### **"Audio workspace not found"**
```bash
# Ensure the directory exists
mkdir audio-workspace
```

#### **"FFmpeg not found"**
```bash
# Install FFmpeg
# Windows: Download from https://ffmpeg.org/download.html
# Mac: brew install ffmpeg
# Linux: sudo apt install ffmpeg
```

#### **"Demucs processing failed"**
```bash
# Ensure virtual environment is set up
cd drum-overlay-system/backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
pip install demucs librosa
```

#### **"Web interface not loading"**
```bash
# Check if port 8080 is available
# Try a different port in auto_trigger.py
```

### Log Analysis
Check the `auto_trigger.log` file for detailed error information:
```bash
# View recent logs
tail -f auto_trigger.log

# Search for errors
grep -i error auto_trigger.log
```

## Advanced Usage

### Custom File Processing
Modify the `process_audio_file` method to add custom processing steps:
```python
def process_audio_file(self, audio_file: Path):
    # Your custom processing here
    super().process_audio_file(audio_file)
    # Additional steps after processing
```

### Integration with Other Systems
The auto trigger system can be integrated with:
- **OBS Studio**: Use the web interface to monitor status
- **Stream Deck**: Create buttons to trigger processing
- **Voice Assistants**: Use webhooks to trigger processing
- **Game Events**: Monitor game audio files automatically

### Batch Processing
For processing multiple files at once:
```bash
# Copy multiple files to audio-workspace
cp /path/to/music/*.mp3 audio-workspace/
# System will process them automatically
```

## Performance Optimization

### Large File Handling
- **Memory Management**: System handles large audio files efficiently
- **Processing Queue**: Files are processed one at a time to prevent conflicts
- **Error Recovery**: Failed processing doesn't affect subsequent files

### Monitoring Performance
- **Resource Usage**: Monitor CPU and memory usage during processing
- **Processing Time**: Large files may take 30-90 seconds to process
- **Concurrent Processing**: Not recommended - stick to one file at a time

## Security Considerations

### File Permissions
- **Read Access**: System needs read access to audio files
- **Write Access**: System needs write access to frontend public directory
- **Execution**: Ensure Python scripts have execution permissions

### Network Security
- **Local Access**: Web interface only accessible locally by default
- **Port Security**: Use non-standard ports if needed
- **Firewall**: Ensure local ports are not blocked

## Maintenance

### Regular Tasks
- **Log Rotation**: Periodically clean up `auto_trigger.log`
- **Disk Space**: Monitor disk space in audio-workspace
- **System Updates**: Keep Python packages updated

### System Health
- **Monitor Logs**: Check logs regularly for errors
- **Test Processing**: Regularly test with known audio files
- **Update Dependencies**: Keep watchdog and other packages updated

## Support

### Getting Help
1. **Check Logs**: First check `auto_trigger.log` for error details
2. **Verify Setup**: Ensure all prerequisites are installed
3. **Test Manually**: Try running the processing pipeline manually
4. **Community**: Check project issues and discussions

### Contributing
- **Bug Reports**: Include logs and system information
- **Feature Requests**: Describe your use case and requirements
- **Code Contributions**: Follow project coding standards

---

**Auto Trigger System - Making drum visualization automation easy!** 🥁✨