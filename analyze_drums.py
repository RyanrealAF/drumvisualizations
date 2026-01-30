import librosa
import numpy as np
import json
import os

def analyze_drum_stem(audio_path, drum_type):
    """Extract onset times and velocities from drum stem."""
    
    if not os.path.exists(audio_path):
        print(f"Warning: {audio_path} not found. Skipping {drum_type}.")
        return []

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
    velocities = velocities / np.max(velocities) if len(velocities) > 0 and np.max(velocities) > 0 else velocities
    
    hits = [[float(t), float(v)] for t, v in zip(onset_times, velocities)]
    return hits

drum_data = {
    "kick": analyze_drum_stem("kick.wav", "kick"),
    "snare": analyze_drum_stem("snare.wav", "snare"),
    "hats": analyze_drum_stem("hats.wav", "hats")
}

output_path = os.path.join("src", "drum-data.json")
os.makedirs("src", exist_ok=True)

with open(output_path, "w") as f:
    json.dump(drum_data, f, indent=2)

print(f"Analysis complete. Data saved to {output_path}")
print(f"Stats: {len(drum_data['kick'])} kicks, {len(drum_data['snare'])} snares, {len(drum_data['hats'])} hats")