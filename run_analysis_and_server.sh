#!/bin/bash
echo "=== Drum Visualization: Analysis & Server ==="

# Navigate to subproject if it exists
if [ -d "drum-logo-overlay" ]; then
    echo "Entering drum-logo-overlay..."
    cd drum-logo-overlay
fi

# Run Analysis
echo "Running Analysis..."
python analyze_drums.py

# Start Server
echo "Starting Server..."
python server.py