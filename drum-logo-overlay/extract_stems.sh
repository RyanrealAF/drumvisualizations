#!/bin/bash
# High-fidelity audio stem extraction script
# This script automates the MISSION: HIGH-FIDELITY AUDIO STEM EXTRACTION (DEMUCS 6S)

# Default Workspace (can be overridden)
WORKSPACE=${1:-"./audio-stem-test"}
TRACK_NAME="track.wav"
MODEL_NAME="htdemucs_6s"

echo "Using Workspace: $WORKSPACE"

# 1. ENVIRONMENT INITIALIZATION
mkdir -p "$WORKSPACE"
# Dependencies are expected to be installed via pip install demucs noisereduce

# Verify FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "Error: ffmpeg is not in PATH."
    exit 1
fi

# 2. SOURCE ARTIFACT VERIFICATION
if [ ! -f "$WORKSPACE/$TRACK_NAME" ]; then
    echo "Error: Source artifact $WORKSPACE/$TRACK_NAME not found."
    exit 1
fi

# 3. PRE-PROCESSING (SOURCE DE-NOISING)
echo "Step 2: Pre-processing (Source De-noising)..."
ffmpeg -i "$WORKSPACE/$TRACK_NAME" -af "afftdn=nf=-25" "$WORKSPACE/track_cleaned.wav" -y

# 4. CORE SEPARATION (INFERENCE)
echo "Step 3: Core Separation (Inference) using $MODEL_NAME..."
# Note: Demucs creates its own output structure
demucs --name="$MODEL_NAME" -o "$WORKSPACE/separated" "$WORKSPACE/track_cleaned.wav"

# 5. POST-PROCESSING (STEM REFINEMENT)
SEP_DIR="$WORKSPACE/separated/$MODEL_NAME/track_cleaned"
if [ ! -d "$SEP_DIR" ]; then
    echo "Error: Separation directory $SEP_DIR not found."
    exit 1
fi

echo "Step 4: Post-processing (Stem Refinement)..."
# Refine Vocals
ffmpeg -i "$SEP_DIR/vocals.wav" -af "highpass=f=80, afftdn=nf=-20, lowpass=f=15000" "$SEP_DIR/vocals_refined.wav" -y
# Refine Drums
ffmpeg -i "$SEP_DIR/drums.wav" -af "lowpass=f=12000, afftdn=nf=-30" "$SEP_DIR/drums_refined.wav" -y

# 6. VALIDATION & AUDIT
echo "Step 5: Validation & Audit..."
FILES=(
    "bass.wav"
    "drums.wav"
    "guitar.wav"
    "other.wav"
    "piano.wav"
    "vocals.wav"
    "vocals_refined.wav"
    "drums_refined.wav"
)

ALL_EXIST=true
for f in "${FILES[@]}"; do
    if [ ! -f "$SEP_DIR/$f" ]; then
        echo "Missing: $f"
        ALL_EXIST=false
    else
        echo "Verified: $f"
    fi
done

if [ "$ALL_EXIST" = true ]; then
    echo "Validation Successful: All 8 files exist."
else
    echo "Validation Failed: Some stems are missing."
    exit 1
fi

# 7. DRUM SIGNAL ANALYSIS
echo "Step 6: Drum Signal Analysis..."
# Ensure the analyzer is run from the root to find the scripts folder correctly if called via relative path
python3 scripts/analyze_drums.py "$SEP_DIR/drums_refined.wav" "drum-data.json"

echo "Mission Complete."
