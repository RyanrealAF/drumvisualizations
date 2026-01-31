# Drum Visualizer - Electron Build Instructions

This directory contains the Electron application for the Drum Visualizer project.

## Prerequisites

- Node.js (v18 or higher)
- Python 3.8+ (for the backend server)
- npm or yarn

## Installation

1. Install dependencies:
```bash
npm install
```

2. Install Electron development dependencies:
```bash
npm install electron electron-builder concurrently wait-on electron-is-dev --save-dev
```

## Development

To run the application in development mode:

```bash
npm run electron:dev
```

This will:
- Start the React development server
- Launch the Electron application
- Automatically reload when changes are made

## Building for Production

### Quick Build
```bash
node build-electron.js
```

### Manual Build Steps

1. Build the React frontend:
```bash
npm run build
```

2. Build the Electron executable:
```bash
npm run electron:build
```

## Build Outputs

The built application will be located in the `dist/` directory:
- Windows: `dist/Drum Visualizer Setup x.x.x.exe`
- macOS: `dist/Drum Visualizer-x.x.x.dmg`
- Linux: `dist/Drum Visualizer-x.x.x.AppImage`

## Application Structure

```
drum-overlay-system/frontend/
├── electron-main.js          # Electron main process
├── preload.js               # Electron preload script
├── vite.config.ts           # Vite configuration
├── electron-builder.json    # Electron Builder configuration
├── build-electron.js        # Build script
├── src/                     # React application source
└── dist/                    # Build output
```

## Python Backend Integration

The application automatically starts the Python backend server when launched. The backend server is located in the `../backend/` directory.

## Troubleshooting

### Common Issues

1. **Python backend not starting**: Ensure Python 3.8+ is installed and the backend dependencies are installed.

2. **Build failures**: Make sure all dependencies are installed and you have the required build tools for your platform.

3. **Port conflicts**: The application uses port 5173 for development. If this port is in use, modify the `vite.config.ts` file.

### Development Tips

- Use `npm run electron:dev` for development with hot reloading
- The React dev server runs on `http://localhost:5173`
- Electron dev tools are available via `Ctrl+Shift+I` (Windows/Linux) or `Cmd+Option+I` (macOS)

## Dependencies

### Electron Dependencies
- `electron`: Core Electron framework
- `electron-builder`: Packaging and building
- `concurrently`: Run multiple commands
- `wait-on`: Wait for services to be ready
- `electron-is-dev`: Detect development mode

### React Dependencies
- `react`, `react-dom`: Core React
- `@react-three/fiber`, `@react-three/drei`: 3D rendering
- `three`: 3D library
- `zustand`: State management