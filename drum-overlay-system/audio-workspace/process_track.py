import os
import sys
import json
import subprocess
import numpy as np
import librosa
import soundfile as sf

# Configuration
INPUT_FILE = "track.wav"
OUTPUT_JSON = "drum-data.json"
DEMUCS_MODEL = "htdemucs" # High quality model

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: {INPUT_FILE} not found in {os.getcwd()}")
        return

    print(f"🎵 Processing {INPUT_FILE}...")

    # 1. Run Demucs Separation
    # We use subprocess to call the demucs CLI which is installed in the environment
    print("running demucs separation (this may take a minute)...")
    try:
        # -n specifies model, -o specifies output path
        subprocess.run(
            ["demucs", "-n", DEMUCS_MODEL, INPUT_FILE],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print("❌ Demucs failed. Ensure 'demucs' is installed (pip install demucs).")
        return
    except FileNotFoundError:
        print("❌ 'demucs' command not found. Activate your virtual environment.")
        return

    # 2. Locate the Drums Stem
    # Demucs output structure: separated/{model}/{track_name}/drums.wav
    track_name = os.path.splitext(INPUT_FILE)[0]
    stem_path = os.path.join("separated", DEMUCS_MODEL, track_name, "drums.wav")

    if not os.path.exists(stem_path):
        print(f"❌ Could not find drum stem at: {stem_path}")
        # Fallback check for spaces in filenames or different folder structures
        possible_dirs = os.listdir(os.path.join("separated", DEMUCS_MODEL))
        if possible_dirs:
            print(f"   Found these folders instead: {possible_dirs}")
        return

    print(f"🥁 Analyzing drums: {stem_path}")

    # 3. Analyze Audio for Visualization Data
    y, sr = librosa.load(stem_path, sr=22050)
    
    # Calculate onset envelope (detect hits)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    times = librosa.times_like(onset_env, sr=sr)

    # Normalize energy 0.0 to 1.0
    if onset_env.max() > 0:
        onset_env = onset_env / onset_env.max()

    # 4. Create Timeline Data
    # We downsample slightly to keep JSON size manageable for web
    # Taking every 4th frame (approx 40ms resolution is usually enough for visual smoothing)
    timeline = []
    step = 2 
    for i in range(0, len(times), step):
        energy = float(onset_env[i])
        if energy > 0.05: # Threshold to remove noise
            timeline.append({
                "t": round(float(times[i]), 3),
                "energy": round(energy, 3)
            })

    output_data = {
        "track": track_name,
        "duration": librosa.get_duration(y=y, sr=sr),
        "timeline": timeline
    }

    # 5. Save JSON
    with open(OUTPUT_JSON, "w") as f:
        json.dump(output_data, f)

    print(f"✅ Success! Data saved to {OUTPUT_JSON}")
    print(f"   Copy this file to your frontend public folder.")

if __name__ == "__main__":
    # Ensure we are in the script's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()