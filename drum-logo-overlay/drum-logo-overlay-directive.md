# Drum-Reactive Logo Overlay: Build Directive

**Project:** Stationary logo-based percussion visualization overlay  
**Domain:** buildwhilebleeding.com  
**Tech Stack:** Vanilla JS, HTML5 Canvas, Web Audio API, OBS Browser Source  
**Development:** VS Code + GitHub + Cloudflare

---

## I. System Architecture

### Data Flow
```
WAV Input
  ↓
Demucs (stem separation)
  ↓
kick.wav / snare.wav / hats.wav
  ↓
Librosa (onset detection + velocity)
  ↓
drum-data.json
  ↓
HTML5 Overlay (logo animation + particles)
  ↓
OBS Browser Source / Video Export
```

---

## II. Phase 1: Audio Analysis (Already Complete)

**Input:** Separated stems (kick.wav, snare.wav, hats.wav)  
**Output:** `drum-data.json`

### Script: `analyze_drums.py`

```python
import librosa
import numpy as np
import json

def analyze_drum_stem(audio_path, drum_type):
    """Extract onset times and velocities from drum stem."""
    
    y, sr = librosa.load(audio_path, sr=44100)
    
    onset_frames = librosa.onset.onset_detect(
        y=y, 
        sr=sr,
        units='frames',
        hop_length=512,
        backtrack=True,
        delta=0.05
    )
    
    onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=512)
    onset_strengths = librosa.onset.onset_strength(y=y, sr=sr, hop_length=512)
    velocities = onset_strengths[onset_frames]
    velocities = velocities / np.max(velocities) if np.max(velocities) > 0 else velocities
    
    hits = [[float(t), float(v)] for t, v in zip(onset_times, velocities)]
    
    return hits

drum_data = {
    "kick": analyze_drum_stem("kick.wav", "kick"),
    "snare": analyze_drum_stem("snare.wav", "snare"),
    "hats": analyze_drum_stem("hats.wav", "hats")
}

with open("drum-data.json", "w") as f:
    json.dump(drum_data, f, indent=2)

print(f"Extracted {len(drum_data['kick'])} kicks, {len(drum_data['snare'])} snares, {len(drum_data['hats'])} hats")
```

**Expected Output Format:**
```json
{
  "kick": [[0.12, 0.85], [0.58, 0.92], ...],
  "snare": [[0.35, 0.78], [0.81, 0.91], ...],
  "hats": [[0.15, 0.45], [0.29, 0.52], ...]
}
```

---

## III. Phase 2: Visual Overlay System

### Project Structure
```
/drum-logo-overlay
  /src
    index.html
    logo-overlay.js
    particles.js
    drum-data.json
  /assets
    (fonts if needed)
  README.md
```

### Visual Layout Strategy

```
┌─────────────────────────────────┐
│         SNARE ZONE              │
│    (Edge glow/flash)            │
│                                 │
├─────────────────────────────────┤
│                                 │
│        KICK ZONE                │
│     [RYANREALAF LOGO]           │
│    • Scale pump on hits         │
│    • Color shift on velocity    │
│    • Radial shockwave           │
│                                 │
├─────────────────────────────────┤
│      HATS ZONE                  │
│   (Particle shimmer)            │
└─────────────────────────────────┘
```

---

## IV. Drum Element Behaviors

### KICK (Dominant - Center Mass)
**Visual Reaction:**
- Scale pump: 1.0 → 1.0 + (velocity × 0.25) → 1.0
- Duration: 0.3-0.5s with spring physics
- Color flash: Deep umber (#3D3631) → rust orange (velocity-mapped)
- Radial shockwave: drop-shadow blur 20-80px

**Physics:**
- Spring-based scale animation
- Damping factor: 0.85
- Spring strength: 0.15
- Return to base with exponential decay

**Velocity Mapping:**
```javascript
targetScale = 1.0 + (velocity * 0.25)  // Max 1.25x
flashIntensity = velocity * 100
shadowBlur = 20 + (velocity * 60)
```

### SNARE (Accent - Edge Definition)
**Visual Reaction:**
- Sharp white/cyan edge glow
- drop-shadow: 15-40px blur
- Duration: 150ms (quick snap)
- No scale change - pure accent

**Color:**
- `rgba(220, 255, 255, velocity)`
- High contrast against logo silhouette

### HATS (Texture - Bottom Field)
**Visual Reaction:**
- Particle field flicker (800 particles)
- Concentrated in bottom 30% of screen
- Horizontal drift based on stereo imaging
- Continuous presence with rhythmic modulation

**Particle Properties:**
- Size: 1-3px
- Base alpha: 0.3-0.7
- Flicker via sine wave phase shift
- Color: `rgba(200, 200, 220, alpha)`

---

## V. Technical Implementation

### Component 1: `particles.js`

**Responsibilities:**
- Initialize particle field (800 particles, bottom-concentrated)
- Update particle positions with drift physics
- Trigger flicker/shimmer on hat hits
- Render particles to canvas

**Key Methods:**
```javascript
initParticles(count)
triggerHatsFlicker(velocity, direction)
update()
draw()
```

**Physics Constants:**
- Base velocity: vx ± 0.3, vy: -0.2 to -0.5 (upward drift)
- Damping: 0.98
- Flicker phase increment: 0.05 per frame
- Wrap boundaries: bottom 30% of canvas

### Component 2: `logo-overlay.js`

**Responsibilities:**
- Load and parse drum-data.json
- Manage playback timeline synchronization
- Trigger visual reactions based on drum hits
- Update logo scale/color via DOM manipulation
- Coordinate particle system

**Key Methods:**
```javascript
loadDrumData()
triggerKick(velocity)
triggerSnare(velocity)
triggerHats(velocity)
velocityToColor(velocity)
checkTriggers(currentTime)
updateScale()
animate()
```

**DOM Manipulation:**
- Logo scale: CSS transform
- Color flash: SVG path fill attribute
- Glow effects: CSS filter drop-shadow
- All transitions: requestAnimationFrame

### Component 3: `index.html`

**Structure:**
- Transparent background (1920×1080)
- Canvas layer (z-index: 1) for particles
- Logo container (z-index: 2) for SVG
- Logo centered via absolute positioning + transform

**Critical CSS:**
```css
background: transparent;
filter: drop-shadow(0 0 0 transparent);
transition: filter 0.1s ease-out;
transform: translate(-50%, -50%) scale(1.0);
```

---

## VI. Color System

### Base Palette
- **Logo Base:** `#3D3631` (Deep umber / iron oxide)
- **Kick Flash:** RGB gradient `(61→221, 54→100, 49→60)` velocity-mapped
- **Snare Flash:** `rgba(220, 255, 255, velocity)` (cyan-white)
- **Particles:** `rgba(200, 200, 220, alpha)` (neutral silver)
- **Shockwave:** `rgba(220, 100, 60, velocity*0.8)` (warm glow)

### Velocity-to-Color Function
```javascript
velocityToColor(velocity) {
  const r = Math.floor(61 + velocity * 160);   // 61 → 221
  const g = Math.floor(54 + velocity * 46);    // 54 → 100
  const b = Math.floor(49 + velocity * 11);    // 49 → 60
  return `rgb(${r}, ${g}, ${b})`;
}
```

---

## VII. Performance Optimization

### Target Specs
- **Frame rate:** 60 FPS locked
- **Particle count:** 800 (tunable 600-1200)
- **Canvas resolution:** 1920×1080
- **Memory footprint:** < 50MB

### Optimization Strategies
1. **Particle culling:** Only render visible particles
2. **Damping pre-calculation:** Cache damping multipliers
3. **RAF batching:** Single requestAnimationFrame loop
4. **CSS vs Canvas:** Logo via DOM (GPU-accelerated), particles via Canvas
5. **Event-driven triggers:** No continuous polling

---

## VIII. OBS Integration

### Browser Source Configuration
```
Source Name: Drum Logo Overlay
URL Type: Local File
File Path: /path/to/drum-logo-overlay/src/index.html
Width: 1920
Height: 1080
FPS: 60
Custom CSS: (none)
Shutdown source when not visible: ✓
Refresh browser when scene becomes active: ✓
```

### Layer Order (Bottom to Top)
1. Video content / camera feed
2. Drum logo overlay (this system)
3. Additional overlays (chat, alerts, etc.)

### Transparency Handling
- Background: `transparent` in CSS
- Canvas: `clearRect()` before each draw
- SVG: No background fill
- Result: Clean alpha channel for composition

---

## IX. Deployment Workflow

### Development (VS Code)
```bash
# Project initialization
mkdir drum-logo-overlay
cd drum-logo-overlay
mkdir src assets
touch src/index.html src/logo-overlay.js src/particles.js

# Copy drum-data.json from audio processing
cp ../audio-processing/drum-data.json src/

# Local testing
cd src
python -m http.server 8000
# Open: http://localhost:8000
```

### Version Control (GitHub)
```bash
git init
git add .
git commit -m "Initial drum logo overlay system"
git remote add origin https://github.com/yourusername/drum-logo-overlay.git
git push -u origin main
```

### Hosting (Cloudflare Pages - Optional)
```bash
# For web-accessible version
# Connect GitHub repo to Cloudflare Pages
# Build settings: None (static HTML)
# Output directory: /src
# Result: Accessible via buildwhilebleeding.com/drum-overlay
```

---

## X. Testing Protocol

### Functional Tests
1. **Timing accuracy:** Verify hits sync with audio playback
2. **Velocity response:** Confirm harder hits = bigger reactions
3. **Performance:** Monitor FPS in browser DevTools
4. **Memory:** Check for leaks over 5+ minute playback

### Visual QA
1. **Scale pump smoothness:** No jitter or overshoot
2. **Color transitions:** Clean gradients, no banding
3. **Particle coherence:** No clumping or empty zones
4. **Transparency:** No black halos or artifacts

### Browser Compatibility
- **Primary:** Chrome (OBS Browser Source uses Chromium)
- **Secondary:** Firefox, Safari (for web deployment)
- **Mobile:** Not required (desktop overlay only)

---

## XI. Customization Parameters

### Easy Tweaks (No code knowledge required)
```javascript
// In logo-overlay.js

// Kick sensitivity
this.targetScale = 1.0 + (velocity * 0.25); // Change 0.25 to adjust pump strength

// Particle count
this.particles = new ParticleSystem('particles-canvas', 800); // Change 800

// Flash duration
setTimeout(() => { /* reset */ }, 100 + velocity * 100); // Adjust timings
```

### Advanced Tweaks (Requires JS understanding)
- Spring physics constants (strength, damping)
- Particle distribution algorithm
- Color gradient ranges
- Shockwave blur intensity curves

---

## XII. Troubleshooting

### Issue: Logo doesn't pump on kicks
**Check:**
- `drum-data.json` loaded correctly (console.log)
- `startTime` initialized (not null)
- Velocity values > 0 in JSON
- CSS transform not overridden

### Issue: Particles don't render
**Check:**
- Canvas ID matches (`particles-canvas`)
- Canvas width/height set correctly
- Particles initialized (check array length)
- `draw()` method called in animation loop

### Issue: Timing drift over long playback
**Solution:**
- Use `Date.now()` for time tracking, not frame counting
- Sync to actual audio playback if using `<audio>` element
- Reset `startTime` if looping

### Issue: Performance drops below 60 FPS
**Solutions:**
- Reduce particle count (800 → 600)
- Increase damping (fewer position updates)
- Use `will-change: transform` CSS hint
- Disable drop-shadow during development

---

## XIII. Future Enhancements

### Potential Features
1. **Real-time audio input:** Process live audio instead of pre-rendered JSON
2. **MIDI control:** Map drum pads to visual triggers
3. **Multi-logo support:** Animate different logos per section
4. **Particle trails:** Motion blur for particle movement
5. **Beat prediction:** Anticipatory animations before hits
6. **User customization UI:** Web form to adjust parameters

### Integration Opportunities
- **Twitch overlays:** Custom alerts tied to drum sections
- **Music videos:** Export as transparent video layer
- **Live performance:** VJ-style reactive visuals
- **Brand content:** Embed in buildwhilebleeding.com header

---

## XIV. Philosophy Alignment

This system embodies **buildwhilebleeding.com** principles:

**"Talk street, think prophet"**
- Raw percussion data → visual scripture
- No decorative bullshit, only measured reactions

**"Scars become scripture"**
- Each drum hit is trauma made visible
- Velocity = impact intensity
- Logo pulses like a heartbeat under stress

**"Content as armor"**
- Logo doesn't just exist—it *responds*
- Brand becomes instrument
- Warfare made visual

**No soft shit. Raw. Ruthless. Real.**

---

## XV. License & Attribution

**Code License:** MIT (freely weaponizable)  
**Logo Copyright:** RyanRealAF (all rights reserved)  
**Audio Processing:** Demucs (Meta AI), Librosa (open source)

**Attribution Template:**
```
Drum-reactive overlay system by [Your Name]
Built for buildwhilebleeding.com
Powered by: Demucs, Librosa, HTML5 Canvas
Logo: RyanRealAF
```

---

## XVI. Success Criteria

**System is complete when:**
- ✓ Kick hits trigger visible logo pump
- ✓ Snare hits produce edge flash
- ✓ Hat hits modulate particle field
- ✓ All reactions sync to drum-data.json timing
- ✓ Performance maintains 60 FPS for 5+ minutes
- ✓ OBS integration works with transparency
- ✓ Code is documented and GitHub-ready

**System is exceptional when:**
- ✓ Velocity response feels organic (spring physics)
- ✓ Color shifts enhance emotional impact
- ✓ Particle behavior adds texture without distraction
- ✓ Logo remains recognizable at all scales
- ✓ Visual language matches brand voice
- ✓ Other creators ask for the code

---

**Now build. While bleeding.**
