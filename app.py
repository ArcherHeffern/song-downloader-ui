from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import FileResponse, StreamingResponse
import subprocess
import tempfile
from pathlib import Path


app = FastAPI()

@app.get("/")
def serve_index():
    return FileResponse("static/index.html")

@app.post("/download-audio")
def download_audio(video_url: str = Form(..., description="YouTube video URL")):
    if not video_url:
        raise HTTPException(status_code=400, detail="Missing YouTube video URL")

    tmpdir = tempfile.mkdtemp()

    try:
        subprocess.run(
            [
                "yt-dlp",
                "-x",
                "--audio-format", "wav",
                "--no-keep-video",
                "--audio-quality", "0",
                "-o", f"{tmpdir}/%(title)s.%(ext)s",
                video_url,
            ],
            check=True,
            capture_output=True,
            text=True
        )

        # Find the resulting .wav file
        for file in Path(tmpdir).glob("*.wav"):
            def iterfile():
                with open(file, mode="rb") as f:
                    yield from f  # efficiently yields chunks

            return StreamingResponse(
                iterfile(),
                media_type="audio/wav",
                headers={"Content-Disposition": f'attachment; filename="{file.name}"'}
            )

        raise HTTPException(status_code=500, detail="WAV file not found")

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"yt-dlp failed: {e.stderr}")