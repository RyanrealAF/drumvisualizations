#!/bin/bash
# ⚡ BOLT OPTIMIZED: High-fidelity audio stem extraction script
# Implementation of RAM-based I/O, Subprocess Concurrency, and Real-time Streaming

# Default Workspace
WORKSPACE=${1:-"./audio-stem-test"}
TRACK_NAME="track.wav"
MODEL_NAME="htdemucs_6s"

# Optimization: Use RAM-based storage if available to eliminate redundant disk writes
if [ -d "/dev/shm" ] && [ -w "/dev/shm" ]; then
    BUFFER_FILE="/dev/shm/track_cleaned.wav"
else
    BUFFER_FILE="/tmp/track_cleaned.wav"
fi

echo "⚡ BOLT Mission: Initializing Optimized Pipeline"
echo "Using Workspace: $WORKSPACE"
echo "RAM Buffer: $BUFFER_FILE"

# 1. ENVIRONMENT INITIALIZATION
mkdir -p "$WORKSPACE"
mkdir -p "$WORKSPACE/midi"
mkdir -p "./midi" # Persistent storage in repo root

# 2. SOURCE ARTIFACT VERIFICATION
if [ ! -f "$WORKSPACE/$TRACK_NAME" ]; then
    echo "Error: Source artifact $WORKSPACE/$TRACK_NAME not found."
    exit 1
fi

# 3. STREAMING PRE-PROCESSING (Optimization: RAM Buffer + Multi-threading)
echo "Step 2: Pre-processing (Source De-noising) to RAM..."
ffmpeg -i "$WORKSPACE/$TRACK_NAME" -af "afftdn=nf=-25" "$BUFFER_FILE" -y -threads 0

# 4. CORE SEPARATION (INFERENCE)
echo "Step 3: Core Separation (Inference) using $MODEL_NAME..."
# Reading from RAM buffer reduces I/O wait times
python3 -m demucs --name="$MODEL_NAME" -o "$WORKSPACE/separated" "$BUFFER_FILE"

# Cleanup RAM buffer immediately
rm "$BUFFER_FILE"

# 5. PARALLEL POST-PROCESSING (Optimization: Subprocess Concurrency)
SEP_DIR="$WORKSPACE/separated/$MODEL_NAME/track_cleaned"

if [ ! -d "$SEP_DIR" ]; then
    # Fallback for different naming conventions
    CLEANED_DIR_NAME=$(basename "$BUFFER_FILE" .wav)
    SEP_DIR="$WORKSPACE/separated/$MODEL_NAME/$CLEANED_DIR_NAME"
fi

if [ ! -d "$SEP_DIR" ]; then
    echo "Error: Separation directory $SEP_DIR not found."
    exit 1
fi

echo "Step 4: Parallel Post-processing (Stem Refinement)..."
# Execute Vocal and Drum refinements concurrently to maximize CPU utilization
ffmpeg -i "$SEP_DIR/vocals.wav" -af "highpass=f=80, afftdn=nf=-20, lowpass=f=15000" "$SEP_DIR/vocals_refined.wav" -y -threads 0 &
VOCAL_PID=$!

ffmpeg -i "$SEP_DIR/drums.wav" -af "lowpass=f=12000, afftdn=nf=-30" "$SEP_DIR/drums_refined.wav" -y -threads 0 &
DRUM_PID=$!

# Synchronize background processes
echo "Waiting for refinement tasks to complete..."
wait $VOCAL_PID $DRUM_PID

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

# 7. DRUM SIGNAL ANALYSIS (Real-time reporting integrated)
echo "Step 6: Drum Signal Analysis (⚡ Optimized Onset Detection + MIDI Export)..."
# The analyzer generates both .json and .mid
python3 scripts/analyze_drums.py "$SEP_DIR/drums_refined.wav" "drum-logo-overlay/src/drum-data.json"

# Move generated MIDI to the storage folders
if [ -f "drum-logo-overlay/src/drum-data.mid" ]; then
    cp "drum-logo-overlay/src/drum-data.mid" "$WORKSPACE/midi/drums.mid"
    mv "drum-logo-overlay/src/drum-data.mid" "./midi/drums.mid"
    echo "MIDI file stored in $WORKSPACE/midi/drums.mid and ./midi/drums.mid"
fi

echo "Mission Complete. Optimized (⚡ Bolt) with MIDI support."
