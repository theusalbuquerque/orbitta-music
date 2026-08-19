from fastapi import FastAPI
from ytmusicapi import YTMusic
import yt_dlp

app = FastAPI()
yt = YTMusic()

@app.get("/search")
def search(query: str):
    return yt.search(query, limit=15)

@app.get("/play")
def get_audio_url(video_id: str):
    ydl_opts = {
        'format': 'bestaudio',
        'quiet': True,
        'noplaylist': True,
        'js_runtimes': {'deno': {'path': r'C:\Users\theus\.deno\bin\deno.exe'}}
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
        return {"url": info['url']}