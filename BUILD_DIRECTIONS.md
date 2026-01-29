# 🏗️ Build Directions: Demucs 6-Stem Engine & Overlay

This guide provides complete instructions for setting up the environment, installing dependencies, and running the high-fidelity audio extraction pipeline and reactive visualizer.

---

## 1. Prerequisites

Ensure you have the following installed on your system:

### 🐍 Python (>= 3.10)
- Used for AI separation, signal analysis, and MIDI generation.
- [Download Python](https://www.python.org/downloads/)

### 📦 Node.js (>= 18)
- Used for the React-based visualizer dashboard.
- [Download Node.js](https://nodejs.org/)

### 🎞️ FFmpeg
- Used for de-noising and stem refinement.
- **Global PATH access is required.**
- [Download FFmpeg](https://ffmpeg.org/download.html)

---

## 2. Backend Setup & Dependencies

It is highly recommended to use a Python virtual environment to avoid dependency conflicts.

### Create and Activate Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Install Core Audio Dependencies
```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install -U demucs noisereduce librosa scipy soundfile mido
```

*Note: Windows users may need [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) for some packages.*

---

## 3. Frontend Setup & Dependencies

The visualizer is built with React, Vite, and Three.js.

### Install Node Packages
```bash
npm install
```

---

## 4. Running the Extraction Pipeline

The extraction pipeline is automated via a shell script. It performs de-noising, 6-stem separation (htdemucs_6s), refinement, and drum analysis.

### Execution Steps
1. Create a workspace directory (e.g., `audio-stem-test`).
2. Place your source audio file as `track.wav` inside that directory.
3. Run the optimized extraction script:

```bash
# Usage: ./scripts/extract_stems.sh [path_to_workspace]
./scripts/extract_stems.sh ./audio-stem-test
```

### Pipeline Output
- **Stems**: Located in `[workspace]/separated/htdemucs_6s/track_cleaned/` (6 originals + 2 refined).
- **Triggers**: `drum-data.json` used by the visualizer.
- **MIDI**: Standard MIDI file saved in `midi/drums.mid`.

---

## 5. Running the Visualizer Dashboard

The dashboard provides a mission-aligned UI and a 60 FPS WebGL visualizer.

### Start Development Server
```bash
npm run dev
```

### Build for Production
```bash
npm run build
# Preview the build
npm run preview
```

---

## 6. Troubleshooting

### `pip install demucs` failing in VS Code
- Always use `python -m pip install` to target the correct environment.
- Ensure the Python Interpreter in VS Code matches your active virtual environment.

### Audio not loading in browser
- Browsers often block local file access. Use the `npm run dev` server or a local Python server (`python -m http.server`) to view the HTML overlay correctly.

### GPU Acceleration
- If a compatible NVIDIA GPU is available, Demucs will automatically use CUDA. Ensure `torch` is installed with CUDA support if you want maximum speed.

---

## ⚡ Bolt Optimization Report

This build utilizes the ⚡ Bolt optimized pipeline:
- **RAM-Based I/O**: Intermediate files are stored in `/dev/shm` (if available) to eliminate disk latency.
- **Concurrency**: Stem refinements are processed in parallel background processes.
- **WebGL Rendering**: The visualizer uses Three.js and custom shaders for high-performance rendering.

---
**Raw. Ruthless. Real.**  
*buildwhilebleeding.com*
