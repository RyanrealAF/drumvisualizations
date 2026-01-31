# Development Guide

## Running in Development Mode

### Prerequisites
- Node.js (v18+)
- Rust (for Tauri)
- Tauri CLI

### Quick Start
```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Start Tauri development (in another terminal)
npm run tauri:dev
```

### Development Workflow

1. **Frontend Development**
   - Run `npm run dev` for hot reload
   - Edit files in `src/` directory
   - Changes auto-reload in the main window

2. **Tauri Development**
   - Run `npm run tauri:dev` for Tauri app
   - Edit files in `src-tauri/src/` for Rust backend
   - Full rebuild required for Rust changes

3. **Overlay Testing**
   - Open overlay window from main app
   - Test overlay.html directly in browser
   - Use test buttons for effect triggers

### Debugging

#### Frontend Issues
```bash
# Check build errors
npm run build

# Check TypeScript errors
npx tsc --noEmit

# Check ESLint issues
npm run lint
```

#### Tauri Issues
```bash
# Check Tauri configuration
npx tauri info

# Clean and rebuild
cargo clean
npx tauri build

# Debug mode
npx tauri dev --debug
```

#### Overlay Issues
- Check overlay.html loads correctly
- Verify drum-data.json accessibility
- Test overlay window positioning
- Check console for JavaScript errors

### Build Commands

```bash
# Frontend only
npm run build

# Tauri only
npx tauri build

# Both (recommended)
./build-executable.sh  # macOS/Linux
.\build-executable.bat  # Windows
```

### Environment Variables

Create `.env` file for development:
```
VITE_API_URL=http://localhost:3000
VITE_DEBUG=true
```

### Hotkeys (Future Implementation)
- `Ctrl+O`: Open overlay
- `Ctrl+C`: Close overlay
- `Ctrl+R`: Reload application
- `F12`: Open dev tools

## Audio Integration

### Backend Connection
The application is ready for audio analysis integration:

1. **WebSocket Connection**
   ```javascript
   // In TauriIntegration.tsx
   // Connect to Python backend
   const socket = io('http://localhost:3000');
   ```

2. **Drum Detection**
   ```javascript
   // Process audio data
   socket.on('drum-hit', (data) => {
     triggerEffect(data.type, data.velocity);
   });
   ```

3. **Real-time Processing**
   - Audio input from microphone
   - Machine learning drum detection
   - Real-time effect triggering

### Python Backend Integration

Your existing Python backend can be integrated:

```python
# server.py
from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    print('Frontend connected')

@socketio.on('audio-data')
def handle_audio(data):
    # Process audio and detect drums
    # Emit drum events to frontend
    socketio.emit('drum-hit', {
        'type': 'kick',
        'velocity': 0.8
    })
```

## Performance Optimization

### Frontend Optimization
- Code splitting with dynamic imports
- Image optimization for overlays
- CSS-in-JS optimization
- Bundle size monitoring

### Tauri Optimization
- Rust compilation flags
- Binary size optimization
- Memory usage monitoring
- Startup time optimization

### Overlay Performance
- Canvas optimization for particles
- CSS animation optimization
- DOM manipulation minimization
- Event listener cleanup

## Testing

### Unit Tests
```bash
# Frontend tests
npm test

# Tauri tests
cargo test
```

### Integration Tests
- Overlay window functionality
- Window communication
- System tray integration
- Hotkey functionality

### Manual Testing
1. Test overlay positioning on different screens
2. Verify OBS streaming compatibility
3. Test with different drum patterns
4. Check performance with high BPM

## Deployment

### Production Build
```bash
# Create production build
./build-executable.sh

# Verify bundle integrity
ls -la src-tauri/target/release/bundle/
```

### Distribution
- Windows: .exe files
- macOS: .dmg files
- Linux: .deb/.AppImage files

### Signing (Production)
- Windows code signing
- macOS notarization
- Linux package signing

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check Rust installation
   - Verify Node.js version
   - Clean and rebuild

2. **Overlay Not Loading**
   - Check overlay.html path
   - Verify file permissions
   - Test in browser directly

3. **Performance Issues**
   - Monitor CPU usage
   - Check memory leaks
   - Optimize animations

4. **Audio Integration**
   - Check WebSocket connection
   - Verify backend running
   - Test with sample data

### Getting Help

1. Check Tauri documentation: https://tauri.app/
2. React Three Fiber docs: https://docs.pmnd.rs/react-three-fiber
3. Create issue in repository
4. Join Tauri Discord community

## Contributing

### Code Style
- Follow existing TypeScript patterns
- Use ESLint configuration
- Maintain consistent naming
- Add TypeScript types

### Pull Requests
1. Create feature branch
2. Make changes with tests
3. Update documentation
4. Submit PR with description

### Code Review
- Ensure no breaking changes
- Verify performance impact
- Check security implications
- Test on multiple platforms