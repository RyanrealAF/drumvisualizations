import librosa
import numpy as np
import json
import sys
import os
from scipy.signal import butter, lfilter

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def apply_filter(data, b, a):
    return lfilter(b, a, data)

def get_drum_hits(y, sr, delta=0.05):
    """Extract onset times and velocities following the directive's logic."""
    onset_frames = librosa.onset.onset_detect(
        y=y, 
        sr=sr,
        units='frames',
        hop_length=512,
        backtrack=True,
        delta=delta
    )
    
    onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=512)
    onset_strengths = librosa.onset.onset_strength(y=y, sr=sr, hop_length=512)
    
    if len(onset_frames) > 0:
        velocities = onset_strengths[onset_frames]
        v_max = np.max(velocities)
        if v_max > 0:
            velocities = velocities / v_max
        return [[round(float(t), 3), round(float(v), 3)] for t, v in zip(onset_times, velocities)]
    return []

def analyze_drums(input_path, output_path):
    print(f"Analyzing {input_path}...")
    y, sr = librosa.load(input_path, sr=44100)
    
    # If stereo, convert to mono
    if len(y.shape) > 1:
        y = librosa.to_mono(y)
    
    # 1. Isolate Kick (< 100Hz)
    bk, ak = butter_lowpass(100, sr)
    y_kick = apply_filter(y, bk, ak)
    
    # 2. Isolate Snare (200Hz - 3kHz)
    bs, as_ = butter_bandpass(200, 3000, sr)
    y_snare = apply_filter(y, bs, as_)
    
    # 3. Isolate Hats (> 5kHz)
    bh, ah = butter_highpass(5000, sr)
    y_hats = apply_filter(y, bh, ah)
    
    data = {
        "kick": get_drum_hits(y_kick, sr, delta=0.1),  # Slightly higher delta for kick to avoid false positives
        "snare": get_drum_hits(y_snare, sr, delta=0.05),
        "hats": get_drum_hits(y_hats, sr, delta=0.02)   # Lower delta for hats to catch subtle hits
    }
    
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Analysis complete. Found {len(data['kick'])} kicks, {len(data['snare'])} snares, {len(data['hats'])} hats.")
    print(f"Data saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python analyze_drums.py <input_wav> <output_json>")
        sys.exit(1)
    
    analyze_drums(sys.argv[1], sys.argv[2])
