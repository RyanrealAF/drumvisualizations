import demucs.api
import librosa
import numpy as np
import json
import soundfile as sf
from pathlib import Path

print("\n" + "=" * 60)
print("AUDIO PROCESSING PIPELINE")
print("=" * 60)

# Check if track.wav exists
if not Path("track.wav").exists():
    print("\n✗ ERROR: track.wav not found!")
    print("  Place your WAV file here and name it 'track.wav'")
    exit(1)

print("\n[1/4] Loading audio file...")
# Separate stems
separator = demucs.api.Separator(model="htdemucs_6s")

print("[2/4] Separating stems (30-90 seconds)...")
print("  This will take a while - be patient...")
origin, stems = separator.separate_audio_file("track.wav")

# Save stems
print("\n[3/4] Saving separated stems...")
for name, audio in stems.items():
    audio_np = audio.cpu().numpy().T
    sf.write(f"{name}.wav", audio_np, 44100)
    print(f"  ✓ Saved {name}.wav")

# Analyze drum onsets
print("\n[4/4] Analyzing drum hits...")
drums_audio, sr = librosa.load("drums.wav", sr=44100, mono=True)

onset_frames = librosa.onset.onset_detect(
    y=drums_audio,
    sr=sr,
    units='frames',
    hop_length=512,
    backtrack=True,
    delta=0.05
)

onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=512)
onset_strengths = librosa.onset.onset_strength(y=drums_audio, sr=sr, hop_length=512)

if len(onset_frames) > 0 and len(onset_frames) > 1:
    velocities = onset_strengths[onset_frames[:-1]]
    if len(velocities) > 0:
        velocities = velocities / np.max(velocities)
    onset_times = onset_times[:-1]
else:
    velocities = np.array([])

# Create trigger data (distribute hits across kick/snare/hats)
drum_data = {
    "kick": [[float(t), float(v)] for t, v in zip(onset_times[::3], velocities[::3])],
    "snare": [[float(t), float(v)] for t, v in zip(onset_times[1::3], velocities[1::3])],
    "hats": [[float(t), float(v)] for t, v in zip(onset_times[2::3], velocities[2::3])]
}

# Save trigger data
with open("drum-data.json", "w") as f:
    json.dump(drum_data, f, indent=2)

print("\n" + "=" * 60)
print("✓ PROCESSING COMPLETE")
print("=" * 60)
print(f"\nGenerated files:")
print(f"  • {len(stems)} stem WAV files")
print(f"  • drum-data.json")
print(f"\nDrum triggers detected:")
print(f"  • Kick hits: {len(drum_data['kick'])}")
print(f"  • Snare hits: {len(drum_data['snare'])}")
print(f"  • Hat hits: {len(drum_data['hats'])}")
print(f"  • Total: {len(onset_times)} drum events")
print("\n" + "=" * 60)
print("\nNext step: Copy drum-data.json to frontend/public/")