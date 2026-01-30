import demucs
import librosa
import numpy as np
import json
import os
import sys
from pathlib import Path

# Configuration
MODEL_NAME = "htdemucs_6s"
SAMPLE_RATE = 44100
HOP_LENGTH = 512
KICK_FREQ = (40, 150)
SNARE_FREQ = (150, 6000)
HATS_FREQ = (6000, 16000)
DELTA = 0.05
WAIT_FRAMES = 10

def separate_audio(input_file, output_dir):
    """Separate audio into 6 stems using Demucs AI."""
    print("=============================================================")
    print("AUDIO PROCESSING PIPELINE")
    print("=============================================================")
    print("[1/4] Initializing Demucs separator...")

    try:
        separator = demucs.api.Separator(
            model=MODEL_NAME,
            shifts=1,
            split=True,
            overlap=0.25
        )
    except Exception as e:
        print(f"ERROR: Failed to initialize Demucs - {e}")
        sys.exit(1)

    print(f"[2/4] Separating stems ({MODEL_NAME})...")
    try:
        stems = separator.separate_audio_file(input_file)
    except Exception as e:
        print(f"ERROR: Audio separation failed - {e}")
        sys.exit(1)

    print("[3/4] Saving separated stems...")
    stem_names = ["drums", "bass", "vocals", "other", "guitar", "piano"]
    os.makedirs(output_dir, exist_ok=True)

    for i, stem in enumerate(stems):
        stem_file = os.path.join(output_dir, f"{stem_names[i]}.wav")
        stem.save(stem_file, codec="wav")
        print(f"      ✓ Saved {stem_names[i]}.wav")

    return os.path.join(output_dir, "drums.wav")

def analyze_drum_stem(audio_path, drum_type, freq_range):
    """Extract onset times and velocities from drum stem."""
    if not os.path.exists(audio_path):
        print(f"Warning: {audio_path} not found. Skipping {drum_type}.")
        return []

    print(f"[4/4] Analyzing {drum_type} hits...")
    y, sr = librosa.load(audio_path, sr=SAMPLE_RATE)

    # Filter to frequency band
    D = librosa.stft(y)
    freq_bins = librosa.fft_frequencies(sr=sr)
    band_mask = (freq_bins >= freq_range[0]) & (freq_bins <= freq_range[1])
    band_energy = np.sum(np.abs(D[band_mask, :]) ** 2, axis=0)

    # Onset detection in frequency band
    onset_frames = librosa.onset.onset_detect(
        onset_envelope=band_energy,
        sr=sr,
        hop_length=HOP_LENGTH,
        units='frames',
        backtrack=True,
        delta=DELTA,
        wait=WAIT_FRAMES
    )

    if len(onset_frames) == 0:
        print(f"      ⚠ No {drum_type} hits detected")
        return []

    onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=HOP_LENGTH)
    onset_strengths = librosa.onset.onset_strength(onset_envelope=band_energy, sr=sr, hop_length=HOP_LENGTH)
    velocities = onset_strengths[onset_frames]
    velocities = velocities / np.max(velocities) if np.max(velocities) > 0 else velocities

    hits = [[float(t), float(v)] for t, v in zip(onset_times, velocities)]
    print(f"      ✓ {drum_type.capitalize()}: {len(hits)} hits detected")
    return hits

def main():
    if len(sys.argv) < 2:
        print("Usage: python process_track.py <input_audio_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = "audio-workspace"

    if not Path(input_file).exists():
        print(f"ERROR: Input file '{input_file}' not found")
        sys.exit(1)

    # Step 1: Separate audio
    drums_file = separate_audio(input_file, output_dir)

    # Step 2: Analyze drum hits
    drum_data = {
        "kick": analyze_drum_stem(drums_file, "kick", KICK_FREQ),
        "snare": analyze_drum_stem(drums_file, "snare", SNARE_FREQ),
        "hats": analyze_drum_stem(drums_file, "hats", HATS_FREQ)
    }

    # Step 3: Save results
    output_path = os.path.join(output_dir, "drum-data.json")
    with open(output_path, "w") as f:
        json.dump(drum_data, f, indent=2)

    print("=============================================================")
    print("✓ PROCESSING COMPLETE")
    print("=============================================================")
    print(f"Data saved to: {output_path}")
    print(f"Stats: {len(drum_data['kick'])} kicks, {len(drum_data['snare'])} snares, {len(drum_data['hats'])} hats")
    print("=============================================================")

if __name__ == "__main__":
    main()