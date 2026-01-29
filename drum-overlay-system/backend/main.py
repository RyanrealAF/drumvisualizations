from fastapi import FastAPI, UploadFile, File
from separation_pipeline import separate_for_overlay
import shutil
from pathlib import Path

app = FastAPI()

@app.post("/separate")
async def separate_audio(file: UploadFile = File(...)):
    temp_path = Path("temp_audio") / file.filename
    temp_path.parent.mkdir(exist_ok=True)

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = separate_for_overlay(temp_path)
    return {
        "track_id": result["track_id"],
        "manifest": str(result["manifest_path"]),
        "drum_stem": str(result["drum_stem"]),
    }