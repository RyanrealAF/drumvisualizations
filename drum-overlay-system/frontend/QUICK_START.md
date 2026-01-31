# 🥁 Drum Visualization System - Quick Start Guide

## 🚀 One-Click Setup

### For Windows Users
```bash
# Download and run the build script
.\build-executable.bat
```

### For macOS/Linux Users
```bash
# Make script executable and run
chmod +x build-executable.sh
./build-executable.sh
```

## 📋 Prerequisites Checklist

- [ ] **Node.js v18+** installed
- [ ] **Rust** installed (https://rustup.rs/)
- [ ] **Tauri CLI** installed (`npm install -g @tauri-apps/cli`)

## 🎯 Quick Commands

```bash
# Development mode
npm run dev              # Frontend only
npm run tauri:dev        # Full Tauri app

# Production build
npm run build            # Frontend only
npx tauri build          # Full executable

# Cross-platform build
./build-executable.sh    # macOS/Linux
.\build-executable.bat   # Windows
```

## 🎮 Application Features

### Main Window
- **Overlay Controls**: Open/Close overlay window
- **Test Effects**: Kick, Snare, Hats test buttons
- **Event Monitor**: Real-time drum event display
- **System Tray**: Quick access and controls

### Overlay Window
- **1920x1080**: Full HD overlay for streaming
- **Always on Top**: Stays visible during streaming
- **Borderless**: Clean look for OBS integration
- **Real-time Effects**: Drum-triggered visualizations

## 🔧 Configuration

### Tauri Settings (`tauri.conf.json`)
- Application metadata and security
- Window configuration
- Bundle settings and resources

### Build Settings (`vite.config.ts`)
- Frontend optimization
- Development server settings
- Build output configuration

### Package Settings (`package.json`)
- Dependencies and scripts
- Tauri integration
- Development tools

## 🐛 Common Issues & Solutions

### Issue: "Rust not found"
```bash
# Solution: Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### Issue: "Tauri CLI not found"
```bash
# Solution: Install Tauri CLI
npm install -g @tauri-apps/cli
```

### Issue: Build fails with errors
```bash
# Solution: Clean and rebuild
cargo clean
npx tauri build
```

### Issue: Overlay not loading
```bash
# Solution: Check overlay.html path
# Verify file exists in public/overlay.html
# Test overlay.html directly in browser
```

## 🎯 Next Steps

### 1. Audio Integration
Connect your existing Python audio analysis:
```python
# Your existing backend can emit drum events
socketio.emit('drum-hit', {
    'type': 'kick',
    'velocity': 0.8
})
```

### 2. Streaming Setup
1. Open overlay window
2. Position in OBS as source
3. Set as "Always on Top"
4. Start streaming with visual effects

### 3. Customization
- Modify overlay.html for custom visuals
- Update App.css for styling changes
- Add new drum effect types
- Configure window positioning

## 📦 Distribution

### Build Output Locations
```
src-tauri/target/release/bundle/
├── windows/     # .exe files
├── macos/       # .dmg files  
└── linux/       # .deb/.AppImage files
```

### Installation
- **Windows**: Run .exe file
- **macOS**: Open .dmg and drag to Applications
- **Linux**: Install .deb or run .AppImage

## 🆘 Getting Help

### Documentation
- `README.md` - Complete setup guide
- `DEVELOPMENT.md` - Development workflow
- `EXECUTABLE_BUILD_SUMMARY.md` - Build summary

### Troubleshooting
1. Check prerequisites are installed
2. Run build script with verbose output
3. Check console for specific error messages
4. Verify file paths and permissions

### Support
- Tauri Documentation: https://tauri.app/
- React Three Fiber: https://docs.pmnd.rs/react-three-fiber
- Create GitHub issue for bugs

## 🎉 Success!

You now have a fully functional drum visualization system packaged as a desktop executable! 

**Key Features:**
- ✅ Cross-platform desktop application
- ✅ Streaming-ready overlay window
- ✅ Real-time drum visualization
- ✅ Professional build system
- ✅ Complete documentation

**Ready to use:**
- Run the executable from the bundle directory
- Open overlay for streaming
- Connect your audio analysis backend
- Start creating amazing drum visualizations! 🥁✨