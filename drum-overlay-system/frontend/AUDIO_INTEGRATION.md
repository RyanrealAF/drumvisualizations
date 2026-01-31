# Audio Integration Guide

## 🎵 Connecting Your Audio Analysis Backend

This guide shows how to integrate your existing Python audio analysis system with the new Tauri executable.

## 📋 Your Existing Backend

Based on your project structure, you have:
- `analyze_drums.py` - Drum analysis script
- `server.py` - WebSocket server
- `drum-data.json` - Drum pattern data
- Audio processing capabilities

## 🔌 Integration Methods

### Method 1: WebSocket Communication (Recommended)

#### 1. Update Your Python Server

```python
# server.py - Enhanced version
from flask import Flask
from flask_socketio import SocketIO, emit
import json
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'drumviz-secret'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Global state for drum detection
drum_detector = None

@socketio.on('connect')
def handle_connect():
    print('Frontend connected successfully!')
    emit('status', {'message': 'Connected to drum analysis backend'})

@socketio.on('start_analysis')
def handle_start_analysis(data):
    """Start real-time drum analysis"""
    global drum_detector
    
    if drum_detector is None:
        # Initialize your drum detector
        from analyze_drums import DrumAnalyzer
        drum_detector = DrumAnalyzer()
    
    # Start analysis in background thread
    analysis_thread = threading.Thread(target=run_analysis)
    analysis_thread.daemon = True
    analysis_thread.start()
    
    emit('status', {'message': 'Drum analysis started'})

@socketio.on('stop_analysis')
def handle_stop_analysis():
    """Stop drum analysis"""
    global drum_detector
    if drum_detector:
        drum_detector.stop()
        drum_detector = None
    emit('status', {'message': 'Drum analysis stopped'})

def run_analysis():
    """Background thread for real-time analysis"""
    global drum_detector
    
    while drum_detector and drum_detector.is_running():
        # Get drum hits from your analyzer
        hits = drum_detector.get_recent_hits()
        
        for hit in hits:
            # Emit drum hit to frontend
            emit('drum_hit', {
                'type': hit['type'],        # 'kick', 'snare', 'hats'
                'velocity': hit['velocity'], # 0.0 to 1.0
                'timestamp': hit['timestamp'],
                'confidence': hit['confidence']
            })
        
        time.sleep(0.01)  # 10ms update rate

if __name__ == '__main__':
    print("Starting Drum Visualization Server...")
    print("Connect frontend to: http://localhost:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
```

#### 2. Update Your Drum Analyzer

```python
# analyze_drums.py - Enhanced for real-time
import numpy as np
from scipy import signal
import threading
import time

class DrumAnalyzer:
    def __init__(self):
        self.running = False
        self.recent_hits = []
        self.lock = threading.Lock()
        
    def start(self):
        """Start real-time analysis"""
        self.running = True
        self.analysis_thread = threading.Thread(target=self._analyze_audio)
        self.analysis_thread.daemon = True
        self.analysis_thread.start()
        
    def stop(self):
        """Stop analysis"""
        self.running = False
        
    def is_running(self):
        """Check if analysis is running"""
        return self.running
        
    def _analyze_audio(self):
        """Main analysis loop"""
        while self.running:
            # Your existing analysis code here
            # Process audio input
            # Detect drum hits
            
            # Example detection logic:
            # audio_data = self.get_audio_input()
            # hits = self.detect_drums(audio_data)
            
            # Store recent hits
            with self.lock:
                # Clean old hits (keep last 10 seconds)
                current_time = time.time()
                self.recent_hits = [
                    hit for hit in self.recent_hits 
                    if current_time - hit['timestamp'] < 10.0
                ]
                
                # Add new hits
                # self.recent_hits.extend(new_hits)
            
            time.sleep(0.01)  # 10ms processing
            
    def get_recent_hits(self):
        """Get recent drum hits"""
        with self.lock:
            hits = self.recent_hits.copy()
            self.recent_hits.clear()
            return hits
            
    def get_audio_input(self):
        """Get audio from microphone or file"""
        # Your existing audio input code
        pass
        
    def detect_drums(self, audio_data):
        """Detect drum hits in audio data"""
        # Your existing drum detection code
        pass
```

### Method 2: HTTP API Integration

#### 1. Create REST API Endpoint

```python
# api_server.py
from flask import Flask, jsonify
import threading
import time

app = Flask(__name__)

class DrumAPI:
    def __init__(self):
        self.recent_hits = []
        self.lock = threading.Lock()
        
    def add_hit(self, hit_data):
        """Add detected drum hit"""
        with self.lock:
            self.recent_hits.append(hit_data)
            
    def get_hits(self):
        """Get and clear recent hits"""
        with self.lock:
            hits = self.recent_hits.copy()
            self.recent_hits.clear()
            return hits

drum_api = DrumAPI()

@app.route('/api/drum-hits', methods=['GET'])
def get_drum_hits():
    """Get recent drum hits"""
    hits = drum_api.get_hits()
    return jsonify({'hits': hits, 'count': len(hits)})

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get analysis status"""
    return jsonify({
        'status': 'running',
        'message': 'Drum analysis active'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
```

#### 2. Frontend HTTP Client

```typescript
// TauriIntegration.tsx - Add HTTP support
export function useAudioIntegration() {
  const [isConnected, setIsConnected] = useState(false)
  const [apiUrl, setApiUrl] = useState('http://localhost:5001')
  
  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const response = await fetch(`${apiUrl}/api/drum-hits`)
        const data = await response.json()
        
        if (data.hits && data.hits.length > 0) {
          data.hits.forEach((hit: any) => {
            triggerEffect(hit.type, hit.velocity)
          })
        }
        
        setIsConnected(true)
      } catch (error) {
        setIsConnected(false)
      }
    }, 100) // Check every 100ms
    
    return () => clearInterval(interval)
  }, [apiUrl])
  
  return { isConnected, apiUrl, setApiUrl }
}
```

## 🔧 Frontend Integration

### Update Tauri Integration

```typescript
// TauriIntegration.tsx - Enhanced version
import { invoke } from '@tauri-apps/api/core'
import { listen } from '@tauri-apps/api/event'
import { useEffect, useState } from 'react'
import io from 'socket.io-client'

interface DrumEvent {
  type: 'kick' | 'snare' | 'hats'
  velocity: number
  timestamp: number
  confidence?: number
}

export function useTauriIntegration() {
  const [isOverlayOpen, setIsOverlayOpen] = useState(false)
  const [drumEvents, setDrumEvents] = useState<DrumEvent[]>([])
  const [isConnected, setIsConnected] = useState(false)
  const [socket, setSocket] = useState<any>(null)

  useEffect(() => {
    // Initialize WebSocket connection
    const newSocket = io('http://localhost:5000', {
      transports: ['websocket']
    })
    
    newSocket.on('connect', () => {
      console.log('Connected to drum analysis backend')
      setIsConnected(true)
    })
    
    newSocket.on('disconnect', () => {
      console.log('Disconnected from backend')
      setIsConnected(false)
    })
    
    newSocket.on('drum_hit', (data: DrumEvent) => {
      console.log('Drum hit detected:', data)
      handleDrumHit(data)
    })
    
    newSocket.on('status', (data: any) => {
      console.log('Backend status:', data.message)
    })
    
    setSocket(newSocket)
    
    return () => {
      newSocket.close()
    }
  }, [])

  const handleDrumHit = (event: DrumEvent) => {
    setDrumEvents(prev => [...prev, event])
    
    // Trigger overlay effects
    if (event.type === 'kick') {
      triggerKickEffect(event.velocity)
    } else if (event.type === 'snare') {
      triggerSnareEffect(event.velocity)
    } else if (event.type === 'hats') {
      triggerHatsEffect(event.velocity)
    }
    
    // Send to overlay window
    window.dispatchEvent(new CustomEvent('drum-hit', { 
      detail: event 
    }))
  }

  const startAnalysis = async () => {
    if (socket) {
      socket.emit('start_analysis', {})
    }
  }

  const stopAnalysis = async () => {
    if (socket) {
      socket.emit('stop_analysis', {})
    }
  }

  // ... rest of the existing functions

  return {
    isOverlayOpen,
    drumEvents,
    isConnected,
    openOverlay,
    closeOverlay,
    startAnalysis,
    stopAnalysis,
    triggerKickEffect,
    triggerSnareEffect,
    triggerHatsEffect
  }
}
```

### Update Main App Component

```typescript
// App.tsx - Add audio controls
function App() {
  const {
    isOverlayOpen,
    drumEvents,
    isConnected,
    openOverlay,
    closeOverlay,
    startAnalysis,
    stopAnalysis,
    triggerKickEffect,
    triggerSnareEffect,
    triggerHatsEffect
  } = useTauriIntegration()

  return (
    <>
      <div className="container">
        {/* ... existing header ... */}
        
        <div className="controls">
          {/* ... existing controls ... */}
          
          <div className="card">
            <h2>Audio Analysis</h2>
            <div className="status-indicator">
              <div className={`status-dot ${isConnected ? 'connected' : 'disconnected'}`}></div>
              <span>{isConnected ? 'Connected' : 'Disconnected'}</span>
            </div>
            <div className="button-group">
              <button 
                onClick={startAnalysis}
                disabled={isConnected}
                className="btn-primary"
              >
                Start Analysis
              </button>
              <button 
                onClick={stopAnalysis}
                disabled={!isConnected}
                className="btn-secondary"
              >
                Stop Analysis
              </button>
            </div>
          </div>
          
          {/* ... rest of existing components ... */}
        </div>
      </div>
      
      <style jsx>{`
        .status-indicator {
          display: flex;
          align-items: center;
          gap: 10px;
          margin-bottom: 15px;
          font-weight: bold;
        }
        
        .status-dot {
          width: 12px;
          height: 12px;
          border-radius: 50%;
          background-color: #ff4757;
          box-shadow: 0 0 10px rgba(255, 71, 87, 0.5);
          animation: pulse 2s infinite;
        }
        
        .status-dot.connected {
          background-color: #2ed573;
          box-shadow: 0 0 10px rgba(46, 213, 115, 0.5);
        }
        
        @keyframes pulse {
          0% { transform: scale(1); opacity: 1; }
          50% { transform: scale(1.2); opacity: 0.7; }
          100% { transform: scale(1); opacity: 1; }
        }
      `}</style>
    </>
  )
}
```

## 🚀 Deployment Setup

### 1. Start Your Backend

```bash
# Start the drum analysis server
python server.py

# Or start the API server
python api_server.py
```

### 2. Build and Run Executable

```bash
# Build the executable
./build-executable.sh  # or .\build-executable.bat

# Run the application
# The executable will be in src-tauri/target/release/bundle/
```

### 3. Configure Audio Input

```python
# In your drum analyzer, configure audio input
import sounddevice as sd

class DrumAnalyzer:
    def __init__(self):
        self.sample_rate = 44100
        self.channels = 1
        self.block_size = 1024
        
    def get_audio_input(self):
        """Get audio from microphone"""
        audio = sd.rec(
            frames=self.block_size,
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype='float32'
        )
        sd.wait()
        return audio.flatten()
```

## 🎯 Testing Your Integration

### 1. Test WebSocket Connection
```bash
# Start backend
python server.py

# Check connection in browser console
socket.emit('start_analysis', {})
```

### 2. Test Drum Detection
```python
# Test with sample audio
from analyze_drums import DrumAnalyzer

analyzer = DrumAnalyzer()
analyzer.start()

# Make drum sounds and check console for hits
```

### 3. Test Overlay Effects
- Open the executable
- Start analysis
- Make drum sounds
- Watch overlay for visual effects

## 🔧 Troubleshooting

### Connection Issues
```bash
# Check if backend is running
curl http://localhost:5000/api/status

# Check firewall settings
# Ensure port 5000 is open
```

### Audio Issues
```python
# Test audio input
import sounddevice as sd
print(sd.query_devices())

# Check microphone permissions
```

### Performance Issues
```python
# Optimize analysis rate
# Reduce block size for lower latency
# Use efficient algorithms
```

## 🎉 Success!

Your drum visualization system is now fully integrated with real-time audio analysis. The executable will:

1. **Connect to your Python backend** automatically
2. **Process audio in real-time** using your existing algorithms
3. **Trigger visual effects** based on detected drum hits
4. **Display overlay effects** for streaming and live performances

**Ready to create amazing drum visualizations!** 🥁✨