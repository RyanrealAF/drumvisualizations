#!/bin/bash

# Drum Visualization System - Cross-Platform Build Script
# =======================================================

set -e

echo "🎵 Building Drum Visualization System Executable..."
echo "======================================================="

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📁 Working directory: $SCRIPT_DIR"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Step 1: Build frontend
echo "🔧 Step 1: Building frontend..."
if npm run build; then
    echo "✅ Frontend build completed successfully"
else
    echo "❌ Frontend build failed!"
    exit 1
fi
echo ""

# Step 2: Check prerequisites
echo "🔍 Step 2: Checking prerequisites..."

# Check Node.js
if command_exists node; then
    NODE_VERSION=$(node --version)
    echo "✅ Node.js found: $NODE_VERSION"
else
    echo "❌ Node.js not found. Please install Node.js v18 or higher"
    exit 1
fi

# Check Rust
if command_exists rustc; then
    RUST_VERSION=$(rustc --version)
    echo "✅ Rust found: $RUST_VERSION"
else
    echo "❌ Rust not found. Please install Rust from: https://rustup.rs/"
    echo "   Run: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
    exit 1
fi

# Check Tauri CLI
if command_exists tauri; then
    TAURI_VERSION=$(tauri --version 2>/dev/null || echo "installed")
    echo "✅ Tauri CLI found: $TAURI_VERSION"
else
    echo "⚠️  Tauri CLI not found. Installing..."
    if npm install -g @tauri-apps/cli; then
        echo "✅ Tauri CLI installed successfully"
    else
        echo "❌ Failed to install Tauri CLI"
        exit 1
    fi
fi
echo ""

# Step 3: Build Tauri application
echo "🚀 Step 3: Building Tauri application..."
if npx tauri build; then
    echo "✅ Tauri build completed successfully"
else
    echo "❌ Tauri build failed!"
    echo ""
    echo "🔧 Troubleshooting tips:"
    echo "   1. Ensure Rust is properly installed and in PATH"
    echo "   2. Check tauri.conf.json for configuration errors"
    echo "   3. Verify all dependencies are installed"
    echo "   4. Try running: cargo clean && npx tauri build"
    exit 1
fi
echo ""

# Step 4: Display results
echo "🎉 Build completed successfully!"
echo ""
echo "📦 Executable locations:"
echo "   Windows: src-tauri/target/release/bundle/windows/"
echo "   macOS:   src-tauri/target/release/bundle/macos/"
echo "   Linux:   src-tauri/target/release/bundle/linux/"
echo ""

# Step 5: Platform-specific instructions
case "$(uname -s)" in
    CYGWIN*|MINGW*|MSYS*)
        echo "💻 Windows Instructions:"
        echo "   Run the executable: src-tauri/target/release/bundle/windows/*.exe"
        ;;
    Darwin)
        echo "🍎 macOS Instructions:"
        echo "   Run the app: open src-tauri/target/release/bundle/macos/*.app"
        echo "   Note: You may need to right-click and select 'Open' the first time"
        ;;
    Linux)
        echo "🐧 Linux Instructions:"
        echo "   Run the executable: src-tauri/target/release/bundle/linux/*.AppImage"
        echo "   Or install the .deb package: sudo dpkg -i *.deb"
        ;;
    *)
        echo "🌍 Platform Instructions:"
        echo "   Check the bundle directory for your platform's executable"
        ;;
esac
echo ""

# Step 6: Development mode option
echo "🛠️  Development Mode:"
echo "   To run in development mode, use:"
echo "   npm run tauri:dev"
echo ""

echo "✨ Happy drumming! 🥁"
exit 0