# Development Server Guide

This project includes a comprehensive development server script that supports multiple development scenarios for the drum visualization project.

## Quick Start

### For React/Vite Development
```bash
# Start Vite development server with hot reload
./run_dev.sh dev
# or on Windows
run_dev.bat dev
```

### For Static File Serving (OBS Integration)
```bash
# Start Python HTTP server on default port 8000
./run_dev.sh python
# or on Windows
run_dev.bat python

# Start on custom port
./run_dev.sh python 3000
# or on Windows
run_dev.bat python 3000
```

### Auto-Detection
```bash
# Automatically detect and start appropriate server
./run_dev.sh auto
# or on Windows
run_dev.bat auto
```

## Script Features

### Cross-Platform Support
- **Linux/macOS**: `run_dev.sh` (Bash script)
- **Windows**: `run_dev.bat` (Batch script)

### Automatic Project Detection
The script automatically detects your project type:
- **Vite Projects**: React/TypeScript applications with `package.json` and `vite.config.ts/js`
- **Python Projects**: Projects with `server.py` or `requirements.txt`

### Smart Dependency Management
- Automatically installs npm dependencies if `node_modules` doesn't exist
- Checks for required tools (npm, Python) and provides helpful error messages

### Multiple Server Options

#### Vite Development Server
- **Purpose**: Active development with hot reload
- **Features**: Fast refresh, development tools, source maps
- **Commands**:
  - `npm run dev`: Start development server
  - `npm run build`: Build for production
  - `npm run preview`: Preview production build

#### Python HTTP Server
- **Purpose**: Static file serving for OBS integration
- **Features**: Simple, no dependencies, cross-platform
- **Usage**: Serves files from current directory on specified port

## Usage Examples

### Development Workflow
```bash
# Start development server for active coding
./run_dev.sh dev

# In another terminal, start Python server for OBS
./run_dev.sh python 8001
```

### Project Information
```bash
# Show project details and detected type
./run_dev.sh info
```

### Help and Documentation
```bash
# Show all available options
./run_dev.sh help
```

## Project Structure Support

The script works with the following project structures:

### Main Project (Root Level)
```
drumvisualizations/
├── package.json          # Vite/React project
├── vite.config.ts        # Vite configuration
├── server.py            # Python HTTP server
├── run_dev.sh           # Development script (Linux/macOS)
├── run_dev.bat          # Development script (Windows)
└── ...
```

### Drum Overlay System
```
drumvisualizations/drum-overlay-system/frontend/
├── package.json          # Vite/React project
├── vite.config.ts        # Vite configuration
└── ...
```

## OBS Integration

For OBS integration, use the Python HTTP server:

1. Start the Python server:
   ```bash
   ./run_dev.sh python
   ```

2. In OBS, add a Browser Source:
   - URL: `http://localhost:8000/index.html`
   - Width/Height: Match your overlay dimensions
   - Check "Shutdown source when not visible" for performance

3. The server serves static files optimized for OBS overlay use.

## Troubleshooting

### Common Issues

**npm not found:**
```bash
# Install Node.js and npm
# Visit: https://nodejs.org/
```

**Python not found:**
```bash
# Install Python
# Visit: https://python.org/
```

**Permission denied (Linux/macOS):**
```bash
# Make script executable
chmod +x run_dev.sh
```

### Dependencies

**For Vite Development:**
- Node.js (v16+ recommended)
- npm or yarn

**For Python Server:**
- Python 3.6+ (or Python 2.7)

## Advanced Usage

### Custom Ports
```bash
# Start Python server on port 3000
./run_dev.sh python 3000
```

### Multiple Projects
```bash
# In main project directory
cd drumvisualizations
./run_dev.sh dev

# In overlay frontend directory
cd drum-overlay-system/frontend
./run_dev.sh dev
```

### Background Servers
```bash
# Start server in background (Linux/macOS)
./run_dev.sh python &
```

## Script Architecture

The development script provides:

1. **Project Detection**: Automatically identifies project type
2. **Dependency Management**: Installs missing dependencies
3. **Error Handling**: Clear error messages and suggestions
4. **Cross-Platform**: Works on Windows, macOS, and Linux
5. **Help System**: Built-in documentation and examples

## Contributing

To modify the development script:

1. Edit `run_dev.sh` for Linux/macOS changes
2. Edit `run_dev.bat` for Windows changes
3. Test on both platforms
4. Update this documentation

## Related Files

- `package.json` - Main project configuration
- `vite.config.ts` - Vite development server configuration
- `server.py` - Python HTTP server (alternative)
- `README.md` - Project documentation