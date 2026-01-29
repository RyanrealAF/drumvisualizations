import librosa
import numpy as np
import json
import sys
import os
import mido
from mido import Message, MidiFile, MidiTrack

def analyze_onsets(audio, sr=44100, drum_type='kick'):
    """Extract onset times + velocities with optimized parameters per drum."""
    
    # Frequency-specific onset detection
    params = {
        'kick': {'fmin': 40, 'fmax': 150, 'delta': 0.05},
        'snare': {'fmin': 150, 'fmax': 6000, 'delta': 0.03},
        'hats': {'fmin': 6000, 'fmax': 16000, 'delta': 0.02}
    }
    
    config = params.get(drum_type, params['kick'])
    
    # Onset detection with frequency filtering
    onset_frames = librosa.onset.onset_detect(
        y=audio,
        sr=sr,
        units='frames',
        hop_length=512,
        backtrack=True,
        delta=config['delta'],
        wait=10  # Minimum 10 frames between onsets
    )
    
    # Convert to timestamps
    onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=512)
    
    # Calculate velocities using spectral flux in target frequency range
    S = np.abs(librosa.stft(audio, hop_length=512))
    freqs = librosa.fft_frequencies(sr=sr)
    
    # Frequency band mask
    freq_mask = (freqs >= config['fmin']) & (freqs <= config['fmax'])
    S_band = S[freq_mask, :]
    
    # Spectral flux
    flux = np.sqrt(np.sum(np.diff(S_band, axis=1)**2, axis=0))
    valid_frames = onset_frames[onset_frames < flux.shape[0]]
    velocities = flux[valid_frames]
    
    # Normalize velocities
    if len(velocities) > 0:
        v_max = np.max(velocities)
        if v_max > 0:
            velocities = velocities / v_max
    else:
        velocities = np.array([])
        
    # Combine
    hits = [[round(float(t), 3), round(float(v), 3)] for t, v in zip(onset_times, velocities)]
    
    return hits

def export_midi(triggers, output_path):
    """Convert trigger data to a Standard MIDI File."""
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    
    # MIDI Note Mapping (General MIDI)
    mapping = {
        'kick': 36,
        'snare': 38,
        'hats': 42
    }
    
    # Collect all events
    events = []
    for drum, hits in triggers.items():
        note = mapping.get(drum, 36)
        for time, velocity in hits:
            # Velocity: 0-127
            v_midi = int(velocity * 127)
            events.append({'time': time, 'note': note, 'velocity': v_midi})
    
    # Sort events by time
    events.sort(key=lambda x: x['time'])
    
    # Ticks per beat (default 480)
    # We'll assume a fixed tempo of 120 BPM for simplicity in time-to-tick conversion
    ticks_per_sec = mid.ticks_per_beat * 2 
    
    last_tick = 0
    for e in events:
        abs_tick = int(e['time'] * ticks_per_sec)
        delta_tick = max(0, abs_tick - last_tick)
        
        # Note On
        track.append(Message('note_on', note=e['note'], velocity=e['velocity'], time=delta_tick, channel=9)) # Channel 10
        # Note Off (10ms duration)
        duration_ticks = int(0.01 * ticks_per_sec)
        track.append(Message('note_off', note=e['note'], velocity=0, time=duration_ticks, channel=9))
        
        last_tick = abs_tick + duration_ticks
        
    mid.save(output_path)
    print(f"MIDI exported to {output_path}")

def analyze_drums(input_path, output_path):
    print(f"Analyzing {input_path}...")
    y, sr = librosa.load(input_path, sr=44100)
    
    # If stereo, convert to mono
    if len(y.shape) > 1:
        y = librosa.to_mono(y)
    
    triggers = {
        'kick': analyze_onsets(y, sr, drum_type='kick'),
        'snare': analyze_onsets(y, sr, drum_type='snare'),
        'hats': analyze_onsets(y, sr, drum_type='hats')
    }
    
    # Save JSON
    with open(output_path, 'w') as f:
        json.dump(triggers, f, indent=2)
    
    # Save MIDI
    midi_path = output_path.replace('.json', '.mid')
    export_midi(triggers, midi_path)
    
    print(f"Analysis complete. Found {len(triggers['kick'])} kicks, {len(triggers['snare'])} snares, {len(triggers['hats'])} hats.")
    print(f"Data saved to {output_path} and {midi_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python analyze_drums.py <input_wav> <output_json>")
        sys.exit(1)
    
    analyze_drums(sys.argv[1], sys.argv[2])
