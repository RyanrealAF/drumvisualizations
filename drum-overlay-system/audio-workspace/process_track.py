"""
Production Audio Processing Pipeline
Separates stems using Demucs AI, detects drum onsets with Librosa,
generates trigger data for real-time visualization.

Requirements:
- track.wav in same directory
- Python 3.10+ with venv activated
- Packages: demucs, librosa, soundfile, numpy

Output:
- 6 separated stem WAV files (drums, bass, vocals, other, guitar, piano)
- drum-data.json with timestamped trigger data
"""

import demucs.api
import librosa
import numpy as np
import json
import soundfile as sf
from pathlib import Path
import sys

INPUT_FILE = "track.wav"
OUTPUT_JSON = "drum-data.json"
SAMPLE_RATE = 44100
HOP_LENGTH = 512

KICK_PARAMS = {'delta': 0.05, 'wait': 10, 'fmin': 40, 'fmax': 150}
SNARE_PARAMS = {'delta': 0.03, 'wait': 8, 'fmin': 150, 'fmax': 6000}
HATS_PARAMS = {'delta': 0.02, 'wait': 5, 'fmin': 6000, 'fmax': 16000}

def print_header(text):
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)

def check_input_file():
    if not Path(INPUT_FILE).exists():
        print_header("ERROR")
        print(f"\n✗ {INPUT_FILE} not found!")
        print(f"  Place your WAV file in this directory and rename it to: {INPUT_FILE}")
        sys.exit(1)

def separate_stems():
    print("[1/4] Initializing Demucs separator...")
    separator = demucs.api.Separator(model="htdemucs_6s", shifts=1, split=True, overlap=0.25)
    
    print("[2/4] Separating stems (30-90 seconds)...")
    origin, stems = separator.separate_audio_file(INPUT_FILE)
    
    print("\n[3/4] Saving separated stems...")
    stem_dict = {}
    
    for name, audio_tensor in stems.items():
        audio_np = audio_tensor.cpu().numpy()
        if audio_np.ndim == 2:
            audio_np = audio_np.T
        output_path = f"{name}.wav"
        sf.write(output_path, audio_np, SAMPLE_RATE)
        stem_dict[name] = audio_np
        print(f"      ✓ Saved {output_path}")
    
    return stem_dict

def detect_onsets_frequency_band(audio, sr, params, drum_type):
    if audio.ndim > 1:
        audio = librosa.to_mono(audio)
    
    D = librosa.stft(audio, hop_length=HOP_LENGTH)
    freqs = librosa.fft_frequencies(sr=sr)
    freq_mask = (freqs >= params['fmin']) & (freqs <= params['fmax'])
    D_band = D[freq_mask, :]
    onset_env = np.sqrt(np.sum(np.abs(D_band)**2, axis=0))
    
    onset_frames = librosa.onset.onset_detect(
        onset_envelope=onset_env, sr=sr, hop_length=HOP_LENGTH,
        units='frames', backtrack=True, delta=params['delta'], wait=params['wait']
    )
    
    if len(onset_frames) == 0:
        print(f"      ⚠ No {drum_type} hits detected")
        return []
    
    onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=HOP_LENGTH)
    velocities = onset_env[onset_frames]
    if np.max(velocities) > 0:
        velocities = velocities / np.max(velocities)
    
    hits = [[float(t), float(v)] for t, v in zip(onset_times, velocities)]
    print(f"      ✓ {drum_type}: {len(hits)} hits detected")
    return hits

def analyze_drum_triggers(stems):
    print("\n[4/4] Analyzing drum hits...")
    drums_audio = stems['drums']
    if drums_audio.ndim > 1:
        drums_audio = librosa.to_mono(drums_audio)
    
    print("      Detecting onsets by frequency...")
    kick_hits = detect_onsets_frequency_band(drums_audio, SAMPLE_RATE, KICK_PARAMS, "Kick")
    snare_hits = detect_onsets_frequency_band(drums_audio, SAMPLE_RATE, SNARE_PARAMS, "Snare")
    hats_hits = detect_onsets_frequency_band(drums_audio, SAMPLE_RATE, HATS_PARAMS, "Hats")
    
    return {"kick": kick_hits, "snare": snare_hits, "hats": hats_hits}

def save_trigger_data(drum_data):
    with open(OUTPUT_JSON, "w") as f:
        json.dump(drum_data, f, indent=2)
    
    total = len(drum_data['kick']) + len(drum_data['snare']) + len(drum_data['hats'])
    print_header("✓ PROCESSING COMPLETE")
    print(f"\nGenerated: {OUTPUT_JSON}")
    print(f"  • Kick:  {len(drum_data['kick'])} hits")
    print(f"  • Snare: {len(drum_data['snare'])} hits")
    print(f"  • Hats:  {len(drum_data['hats'])} hits")
    print(f"  • Total: {total} drum events")
    print("\n" + "=" * 60)

def main():
    print_header("AUDIO PROCESSING PIPELINE")
    check_input_file()
    stems = separate_stems()
    drum_data = analyze_drum_triggers(stems)
    save_trigger_data(drum_data)

if __name__ == "__main__":
    main()
