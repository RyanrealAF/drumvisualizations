#!/usr/bin/env python3
"""
Auto Trigger System for Drum Visualization
Automatically processes new audio files and updates the visualization

Features:
- File system monitoring for new audio files
- Automatic audio processing and drum analysis
- Real-time frontend updates
- Web server for manual triggering
- Logging and error handling
"""

import os
import sys
import time
import json
import logging
import subprocess
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from http.server import HTTPServer, BaseHTTPRequestHandler
import webbrowser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('auto_trigger.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class AudioFileHandler(FileSystemEventHandler):
    """Handles file system events for audio files"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.audio_workspace = project_root / "audio-workspace"
        self.frontend_public = project_root / "drum-overlay-system" / "frontend" / "public"
        self.processing = False
        self.last_processed_time = 0
        
    def on_created(self, event):
        """Handle new file creation"""
        if event.is_directory:
            return
            
        file_path = Path(event.src_path)
        if self.is_audio_file(file_path):
            logger.info(f"New audio file detected: {file_path.name}")
            self.process_audio_file(file_path)
    
    def on_modified(self, event):
        """Handle file modifications"""
        if event.is_directory:
            return
            
        file_path = Path(event.src_path)
        if self.is_audio_file(file_path):
            # Only process if file is complete (not being written to)
            if self.is_file_complete(file_path):
                current_time = time.time()
                if current_time - self.last_processed_time > 5:  # Debounce
                    logger.info(f"Audio file modified: {file_path.name}")
                    self.process_audio_file(file_path)
    
    def is_audio_file(self, file_path: Path) -> bool:
        """Check if file is an audio file"""
        audio_extensions = {'.wav', '.mp3', '.flac', '.m4a', '.ogg'}
        return file_path.suffix.lower() in audio_extensions
    
    def is_file_complete(self, file_path: Path) -> bool:
        """Check if file is completely written (not being modified)"""
        try:
            # Check if file size is stable
            size1 = file_path.stat().st_size
            time.sleep(0.5)
            size2 = file_path.stat().st_size
            return size1 == size2
        except:
            return False
    
    def process_audio_file(self, audio_file: Path):
        """Process an audio file through the pipeline"""
        if self.processing:
            logger.warning("Processing already in progress, skipping...")
            return
            
        self.processing = True
        try:
            logger.info("=" * 60)
            logger.info(f"PROCESSING: {audio_file.name}")
            logger.info("=" * 60)
            
            # Step 1: Copy audio file to workspace
            target_file = self.audio_workspace / "track.wav"
            if audio_file.suffix.lower() != '.wav':
                # Convert to WAV if needed
                logger.info("Converting audio file to WAV format...")
                subprocess.run([
                    'ffmpeg', '-i', str(audio_file), str(target_file)
                ], check=True, capture_output=True)
            else:
                # Copy WAV file directly
                import shutil
                shutil.copy2(audio_file, target_file)
            
            # Step 2: Run audio processing
            logger.info("Running drum analysis...")
            backend_dir = self.project_root / "drum-overlay-system" / "backend"
            audio_workspace_dir = self.audio_workspace
            
            # Activate virtual environment and run processing
            if os.name == 'nt':  # Windows
                activate_script = backend_dir / "venv" / "Scripts" / "activate.bat"
                cmd = f'cd /d "{backend_dir}" && call "{activate_script}" && cd /d "{audio_workspace_dir}" && python process_track.py track.wav'
            else:  # Unix/Linux/Mac
                activate_script = backend_dir / "venv" / "bin" / "activate"
                cmd = f'cd "{backend_dir}" && source "{activate_script}" && cd "{audio_workspace_dir}" && python process_track.py track.wav'
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"Audio processing failed: {result.stderr}")
                return
            
            logger.info("Audio processing completed successfully")
            
            # Step 3: Copy drum data to frontend
            drum_data_src = self.audio_workspace / "drum-data.json"
            drum_data_dest = self.frontend_public / "drum-data.json"
            
            if drum_data_src.exists():
                import shutil
                shutil.copy2(drum_data_src, drum_data_dest)
                logger.info("Copied drum data to frontend")
            else:
                logger.error("Drum data file not found after processing")
                return
            
            # Step 4: Update timestamp
            self.last_processed_time = time.time()
            
            logger.info("✅ Processing complete!")
            logger.info(f"   Kicks: {self.get_hit_count('kicks')}")
            logger.info(f"   Snares: {self.get_hit_count('snares')}")
            logger.info(f"   Hats: {self.get_hit_count('hats')}")
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error(f"Error processing audio file: {e}")
        finally:
            self.processing = False
    
    def get_hit_count(self, hit_type: str) -> int:
        """Get hit count from drum data"""
        try:
            drum_data_file = self.frontend_public / "drum-data.json"
            if drum_data_file.exists():
                with open(drum_data_file, 'r') as f:
                    data = json.load(f)
                    return len(data.get(hit_type, []))
        except:
            pass
        return 0


class AutoTriggerServer(BaseHTTPRequestHandler):
    """HTTP server for manual triggering and status"""
    
    def __init__(self, project_root: Path, *args, **kwargs):
        self.project_root = project_root
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.send_html_response()
        elif self.path == '/status':
            self.send_json_response()
        elif self.path == '/trigger':
            self.trigger_processing()
        else:
            self.send_error(404)
    
    def send_html_response(self):
        """Send HTML status page"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Auto Trigger Status</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                .status {{ padding: 15px; border-radius: 8px; margin-bottom: 20px; }}
                .running {{ background: #27ae60; color: white; }}
                .stopped {{ background: #e74c3c; color: white; }}
                .controls {{ display: flex; gap: 10px; margin-bottom: 20px; }}
                button {{ padding: 10px 20px; font-size: 16px; border: none; border-radius: 4px; cursor: pointer; }}
                .btn-primary {{ background: #3498db; color: white; }}
                .btn-success {{ background: #27ae60; color: white; }}
                .btn-danger {{ background: #e74c3c; color: white; }}
                .stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; }}
                .stat-card {{ background: #ecf0f1; padding: 15px; border-radius: 8px; text-align: center; }}
                .stat-value {{ font-size: 24px; font-weight: bold; color: #2c3e50; }}
                .stat-label {{ color: #7f8c8d; font-size: 14px; }}
                .log {{ background: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 8px; font-family: monospace; white-space: pre-wrap; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎵 Drum Visualization Auto Trigger</h1>
                <p>Automatically processes audio files and updates the drum visualization</p>
            </div>
            
            <div class="controls">
                <button class="btn-primary" onclick="location.reload()">Refresh Status</button>
                <button class="btn-success" onclick="triggerProcessing()">Process Now</button>
                <button class="btn-danger" onclick="stopServer()">Stop Server</button>
            </div>
            
            <div id="status-container">
                <!-- Status will be loaded here -->
            </div>
            
            <div class="stats" id="stats-container">
                <!-- Stats will be loaded here -->
            </div>
            
            <div class="log" id="log-container">
                <!-- Log will be loaded here -->
            </div>
            
            <script>
                function loadStatus() {{
                    fetch('/status')
                        .then(r => r.json())
                        .then(data => {{
                            const statusContainer = document.getElementById('status-container');
                            const statsContainer = document.getElementById('stats-container');
                            
                            statusContainer.innerHTML = `
                                <div class="status ${data.running ? 'running' : 'stopped'}">
                                    <h3>Status: ${data.running ? '🟢 Running' : '🔴 Stopped'}</h3>
                                    <p>Monitoring: ${data.watch_path}</p>
                                    <p>Last Update: ${data.last_update}</p>
                                </div>
                            `;
                            
                            statsContainer.innerHTML = `
                                <div class="stat-card">
                                    <div class="stat-value">${data.stats.kicks}</div>
                                    <div class="stat-label">Kick Hits</div>
                                </div>
                                <div class="stat-card">
                                    <div class="stat-value">${data.stats.snares}</div>
                                    <div class="stat-label">Snare Hits</div>
                                </div>
                                <div class="stat-card">
                                    <div class="stat-value">${data.stats.hats}</div>
                                    <div class="stat-label">Hat Hits</div>
                                </div>
                            `;
                        }});
                }}
                
                function loadLog() {{
                    fetch('/log')
                        .then(r => r.text())
                        .then(log => {{
                            document.getElementById('log-container').innerText = log;
                        }});
                }}
                
                function triggerProcessing() {{
                    fetch('/trigger')
                        .then(r => r.json())
                        .then(data => {{
                            alert(data.message);
                            loadStatus();
                        }});
                }}
                
                function stopServer() {{
                    if(confirm('Stop the auto trigger server?')) {{
                        fetch('/stop')
                            .then(r => r.json())
                            .then(data => {{
                                alert(data.message);
                                location.reload();
                            }});
                    }}
                }}
                
                // Auto-refresh every 5 seconds
                setInterval(loadStatus, 5000);
                setInterval(loadLog, 10000);
                
                // Initial load
                loadStatus();
                loadLog();
            </script>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def send_json_response(self):
        """Send JSON status"""
        import json
        
        # Get current stats
        frontend_public = self.project_root / "drum-overlay-system" / "frontend" / "public"
        drum_data_file = frontend_public / "drum-data.json"
        
        stats = {"kicks": 0, "snares": 0, "hats": 0}
        if drum_data_file.exists():
            try:
                with open(drum_data_file, 'r') as f:
                    data = json.load(f)
                    stats = {
                        "kicks": len(data.get("kicks", [])),
                        "snares": len(data.get("snares", [])),
                        "hats": len(data.get("hats", []))
                    }
            except:
                pass
        
        status_data = {
            "running": True,
            "watch_path": str(self.project_root / "audio-workspace"),
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "stats": stats
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(status_data, indent=2).encode())
    
    def trigger_processing(self):
        """Manually trigger processing"""
        # This would need to be implemented to trigger the processing
        # For now, just return a message
        response = {"message": "Manual trigger not yet implemented"}
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())


def main():
    """Main function to start the auto trigger system"""
    project_root = Path(__file__).parent.absolute()
    logger.info(f"Starting Auto Trigger System in: {project_root}")
    
    # Check if required directories exist
    audio_workspace = project_root / "audio-workspace"
    frontend_public = project_root / "drum-overlay-system" / "frontend" / "public"
    
    if not audio_workspace.exists():
        logger.error(f"Audio workspace not found: {audio_workspace}")
        return
    
    if not frontend_public.exists():
        logger.error(f"Frontend public directory not found: {frontend_public}")
        return
    
    # Start file system monitoring
    event_handler = AudioFileHandler(project_root)
    observer = Observer()
    observer.schedule(event_handler, str(audio_workspace), recursive=False)
    observer.start()
    
    logger.info(f"📁 Monitoring directory: {audio_workspace}")
    logger.info("🚀 Auto trigger system started!")
    logger.info("💡 Drop audio files into the audio-workspace folder to process them automatically")
    
    # Start web server for status monitoring
    def run_server():
        try:
            server_address = ('', 8080)
            httpd = HTTPServer(server_address, lambda *args, **kwargs: AutoTriggerServer(project_root, *args, **kwargs))
            logger.info("🌐 Web interface available at: http://localhost:8080")
            webbrowser.open('http://localhost:8080')
            httpd.serve_forever()
        except KeyboardInterrupt:
            logger.info("Web server stopped")
        except Exception as e:
            logger.error(f"Web server error: {e}")
    
    # Start web server in separate thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("🛑 Stopping auto trigger system...")
        observer.stop()
    
    observer.join()
    logger.info("✅ Auto trigger system stopped")


if __name__ == "__main__":
    main()