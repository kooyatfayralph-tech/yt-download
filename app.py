from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom secret password (change this if you want)
SECRET_KEY = "mysecret123"

class VideoRequest(BaseModel):
    url: str

@app.get("/")
def home():
    return {"status": "API running"}

@app.post("/download")
def get_video_link(req: VideoRequest, x_secret_key: str = Header(None)):
    if x_secret_key != SECRET_KEY:
        raise HTTPException(status_code=401, detail="Invalid Secret Passkey")

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(req.url, download=False)
            return {
                "title": info.get("title"),
                "download_url": info.get("url")
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

