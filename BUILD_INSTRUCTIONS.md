# COMPLETE BUILD INSTRUCTIONS - START TO FINISH

**System:** Drum-reactive logo overlay  
**Time to Complete:** 30-60 minutes (first time)  
**Skill Level Required:** Intermediate (can follow terminal commands)

---

## PREREQUISITES - INSTALL THESE FIRST

### 1. Python 3.10+
**Download:** https://python.org/downloads/  
**During install:** ✅ Check "Add Python to PATH"  
**Verify:**
```bash
python --version
# Should show: Python 3.10.x or higher
```

### 2. Node.js 18+
**Download:** https://nodejs.org/ (LTS version)  
**Verify:**
```bash
node --version
# Should show: v18.x.x or higher
```

### 3. FFmpeg
**Windows:**
- Download: https://ffmpeg.org/download.html
- Extract to `C:\ffmpeg`
- Add `C:\ffmpeg\bin` to System PATH
- Verify:
```cmd
ffmpeg -version
```

**Mac:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg
```

### 4. Visual Studio Build Tools (Windows only, if needed)
**Download:** https://visualstudio.microsoft.com/visual-cpp-build-tools/  
**Select:** "Desktop development with C++"  
**Install size:** ~4GB  
**Required for:** Python package compilation

---

## PROJECT STRUCTURE SETUP

### Create Project Folders

**Windows:**
```powershell
cd C:\projects
mkdir drumvisualizations
cd drumvisualizations
mkdir drum-overlay-system
cd drum-overlay-system
mkdir backend frontend audio-workspace
```

**Mac/Linux:**
```bash
cd ~/projects
mkdir -p drumvisualizations/drum-overlay-system/{backend,frontend,audio-workspace}
cd drumvisualizations/drum-overlay-system
```

**Result:**
```
drum-overlay-system/
├── backend/          (Python processing)
├── frontend/         (HTML visualizer)
└── audio-workspace/  (Audio files + processing)
```

---

## BACKEND SETUP

### 1. Create Python Virtual Environment

**Navigate to backend:**
```bash
cd backend
```

**Create venv:**
```bash
python -m venv venv
```

**Activate venv:**

**Windows:**
```powershell
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

**You should see `(venv)` at the start of your terminal line**

### 2. Install Python Packages

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install demucs librosa soundfile numpy scipy
```

**This takes 2-5 minutes**

### 3. Verify Installation

```bash
python -c "import demucs; print('Demucs ready')"
python -c "import librosa; print('Librosa ready')"
```

**Expected output:**
```
Demucs ready
Librosa ready
```

---

## AUDIO WORKSPACE SETUP

### 1. Navigate to workspace

```bash
cd ../audio-workspace
```

### 2. Add processing script

**Create file:** `process_track.py`  
**Content:** Use the `process_track.py` artifact provided

**Or download directly:**
- Save `process_track.py` to this folder

### 3. Add your audio file

**Copy your WAV file:**
```bash
# Windows
copy "C:\path\to\your\music.wav" track.wav

# Mac/Linux
cp /path/to/your/music.wav track.wav
```

**Or convert MP3 to WAV:**
```bash
ffmpeg -i "your_song.mp3" track.wav
```

### 4. Process the audio

**Make sure venv is activated:**
```bash
cd ../backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
cd ../audio-workspace
```

**Run processing:**
```bash
python process_track.py
```

**Wait 30-90 seconds. You'll see:**
```
============================================================
AUDIO PROCESSING PIPELINE
============================================================
[1/4] Initializing Demucs separator...
[2/4] Separating stems (30-90 seconds)...
[3/4] Saving separated stems...
      ✓ Saved drums.wav
      ✓ Saved bass.wav
      ✓ Saved vocals.wav
      ✓ Saved other.wav
      ✓ Saved guitar.wav
      ✓ Saved piano.wav
[4/4] Analyzing drum hits...
      ✓ Kick: XX hits detected
      ✓ Snare: XX hits detected
      ✓ Hats: XX hits detected
============================================================
✓ PROCESSING COMPLETE
============================================================
```

**Verify output:**
```bash
ls -la
# Should see: drum-data.json + 6 WAV files
```

---

## FRONTEND SETUP

### 1. Navigate to frontend

```bash
cd ../frontend
```

### 2. Initialize Vite + React

```bash
npm create vite@latest . -- --template react-ts
```

**When prompted "Current directory is not empty?":**  
Type: `y`

### 3. Install dependencies

```bash
npm install
npm install three @types/three @react-three/fiber @react-three/drei zustand
```

**This takes 1-2 minutes**

### 4. Add overlay file

**Create:** `public/overlay.html`  
**Content:** Use the `overlay.html` artifact provided

**File structure should be:**
```
frontend/
├── public/
│   ├── overlay.html  ← This file
│   └── vite.svg
├── src/
├── package.json
└── ...
```

### 5. Copy drum data to frontend

```bash
# Windows
copy ..\audio-workspace\drum-data.json public\

# Mac/Linux
cp ../audio-workspace/drum-data.json public/
```

### 6. Start dev server

```bash
npm run dev
```

**You'll see:**
```
VITE v7.x.x  ready in XXXms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

**Keep this terminal open**

---

## VERIFY IT WORKS

### 1. Open overlay in browser

**Navigate to:** `http://localhost:5173/overlay.html`

**NOT:** `http://localhost:5173/` (that's the default Vite page)

### 2. Check browser console

**Press F12 to open DevTools**  
**Click "Console" tab**

**You should see:**
```
============================================================
DRUM LOGO OVERLAY - RyanRealAF
buildwhilebleeding.com
============================================================
✓ System initialized
✓ Drum data loaded
  Kicks: XX
  Snares: XX
  Hats: XX
```

### 3. Visual verification

**You should see:**
- ✅ Black background
- ✅ "RYANREALAF" logo centered (deep umber color)
- ✅ Particles shimmering at bottom of screen
- ✅ Logo pumping/scaling with rhythm
- ✅ Logo flashing color on hits
- ✅ Smooth 60 FPS animation

---

## OBS STUDIO INTEGRATION (OPTIONAL)

### 1. Open OBS Studio

### 2. Add Browser Source

**Sources panel → Click `+` → Browser**

**Name:** Drum Logo Overlay

**URL:** `http://localhost:5173/overlay.html`  
**Width:** 1920  
**Height:** 1080  
**FPS:** 60  
**Custom CSS:** (leave empty)

**Checkboxes:**
- ✅ Shutdown source when not visible
- ✅ Refresh browser when scene becomes active

### 3. Position overlay

**In OBS preview:**
- Drag to position
- Should be above your camera/game capture
- Should be below alerts/chat

### 4. Test

**Switch to different scene, then back**  
**Overlay should refresh and start animating**

---

## PROCESS NEW TRACKS

**For each new audio file:**

### 1. Replace audio file

```bash
cd audio-workspace
# Delete old track.wav
rm track.wav  # or del track.wav on Windows

# Add new file
copy "C:\path\to\new_song.wav" track.wav
```

### 2. Re-run processing

```bash
# Activate venv if needed
cd ../backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Process
cd ../audio-workspace
python process_track.py
```

### 3. Copy new data to frontend

```bash
copy drum-data.json ..\frontend\public\  # Windows
cp drum-data.json ../frontend/public/  # Mac/Linux
```

### 4. Refresh browser

**In browser:** Press `Ctrl + Shift + R` (hard refresh)  
**In OBS:** Right-click browser source → Refresh

---

## TROUBLESHOOTING

### Backend Issues

**"No module named 'demucs'"**
```bash
# Virtual environment not activated
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

**"track.wav not found"**
```bash
# File not in audio-workspace folder
cd audio-workspace
ls track.wav  # Should show the file
```

**"Demucs separation failed"**
```bash
# WAV file might be corrupted
# Try converting with FFmpeg first:
ffmpeg -i original.wav track.wav
```

### Frontend Issues

**"Failed to load drum-data.json"**
```bash
# File not copied to public folder
cd frontend
ls public/drum-data.json  # Should exist

# If missing, copy it:
cp ../audio-workspace/drum-data.json public/
```

**"Overlay shows blank screen"**
```
1. Check URL: Should be /overlay.html not just /
2. Hard refresh: Ctrl+Shift+R
3. Check console for errors (F12)
```

**"Logo doesn't animate"**
```
1. Verify drum-data.json has content (open it)
2. Check console shows "✓ Drum data loaded"
3. Hard refresh browser
```

**"Low FPS / Laggy"**
```javascript
// Edit overlay.html, reduce particle count:
// Line ~79, change 800 to 400:
this.particles = new ParticleSystem('particles-canvas', 400);
```

---

## FILE CHECKLIST

**After successful setup, you should have:**

### Backend
- [ ] `backend/venv/` (virtual environment)
- [ ] Demucs + Librosa installed

### Audio Workspace
- [ ] `audio-workspace/process_track.py`
- [ ] `audio-workspace/track.wav`
- [ ] `audio-workspace/drum-data.json` (generated)
- [ ] `audio-workspace/drums.wav` (generated)
- [ ] `audio-workspace/bass.wav` (generated)
- [ ] `audio-workspace/vocals.wav` (generated)
- [ ] Other stems (generated)

### Frontend
- [ ] `frontend/node_modules/` (dependencies)
- [ ] `frontend/public/overlay.html`
- [ ] `frontend/public/drum-data.json` (copied)
- [ ] Dev server running on port 5173

---

## QUICK REFERENCE COMMANDS

### Backend (Process Audio)
```bash
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
cd ../audio-workspace
python process_track.py
```

### Frontend (Start Visualizer)
```bash
cd frontend
npm run dev
# Visit: http://localhost:5173/overlay.html
```

### Copy Data After Processing
```bash
# From audio-workspace folder
copy drum-data.json ..\frontend\public\  # Windows
cp drum-data.json ../frontend/public/  # Mac/Linux
```

---

## NEXT STEPS

**Now you have a working system. To extend it:**

1. **Customize colors** - Edit `overlay.html` color values
2. **Adjust sensitivity** - Edit `process_track.py` delta values
3. **Change logo** - Replace SVG in `overlay.html`
4. **Add more particles** - Increase particle count
5. **Deploy to web** - `npm run build` and host on Cloudflare Pages

**Read TECHNICAL_SPECS.md for complete customization options**

---

## SUCCESS CRITERIA

**You know it's working when:**

1. ✅ Processing completes without errors
2. ✅ `drum-data.json` contains arrays of numbers
3. ✅ Browser console shows "✓ Drum data loaded"
4. ✅ Logo visibly pumps with rhythm
5. ✅ Logo flashes color on strong hits
6. ✅ Particles shimmer at screen bottom
7. ✅ Animation runs at 60 FPS

**If all boxes checked, you're done.**

---

**Build complete. Now bleed.**
