import sys
import subprocess
import json
from pathlib import Path

# Define where separated files go
OUTPUT_BASE = Path("separated_audio")

def separate_for_overlay(audio_path: Path):
    """
    Orchestrates the Demucs separation specifically for drum overlay generation.
    """
    audio_path = Path(audio_path).resolve()
    if not audio_path.exists():
        raise FileNotFoundError(f"Input audio not found: {audio_path}")

    # Generate a unique ID for this run (or use the file hash in a real app)
    # For now, we use the filename stem to keep it readable.
    track_name = audio_path.stem
    
    # We use the 'htdemucs' model (Hybrid Transformer) - it's the current state of the art in Demucs v4.
    # We use --two-stems=drums to save resources, as we only need the drum track.
    model = "htdemucs"
    
    cmd = [
        sys.executable, "-m", "demucs",
        "-n", model,
        "--two-stems", "drums",
        "-o", str(OUTPUT_BASE),
        str(audio_path)
    ]

    print(f"⚡ Starting Separation for: {track_name}")
    print(f"   Command: {' '.join(cmd)}")

    # Run the separation
    try:
        # capture_output=True allows us to log stdout/stderr if needed
        process = subprocess.run(cmd, check=True, text=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print("❌ Demucs Separation Failed!")
        print(e.stderr)
        raise RuntimeError(f"Demucs failed with error: {e.stderr}")

    # Locate the output
    # Demucs structure: <output_base>/<model>/<track_name>/drums.wav
    expected_output_dir = OUTPUT_BASE / model / track_name
    drum_stem = expected_output_dir / "drums.wav"

    if not drum_stem.exists():
        # Fallback: Demucs sometimes sanitizes filenames (spaces -> underscores)
        # In a production system, we'd parse the stdout to find the exact path.
        raise FileNotFoundError(f"Expected output not found at: {drum_stem}. Check Demucs logs.")

    # Create a manifest for the frontend
    manifest = {
        "track_name": track_name,
        "original_path": str(audio_path),
        "drum_stem_path": str(drum_stem),
        "model": model,
        "status": "completed"
    }
    
    manifest_path = expected_output_dir / "manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"✅ Separation Complete. Stem: {drum_stem}")

    return {
        "track_id": track_name,
        "manifest_path": manifest_path,
        "drum_stem": drum_stem
    }