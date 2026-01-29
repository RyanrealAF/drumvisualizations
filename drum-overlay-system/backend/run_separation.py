from separation_pipeline import separate_for_overlay
from pathlib import Path

if __name__ == "__main__":
    audio = Path(r"C:\projects\_Impossible Thing.mp3")
    result = separate_for_overlay(audio)
    print(result)