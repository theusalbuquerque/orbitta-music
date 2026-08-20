```python
from fastapi import FastAPI, HTTPException, Request
from ytmusicapi import YTMusic
import yt_dlp
import logging

app = FastAPI()

# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO
)

logger = logging.getLogger("orbitta")


# ============================================================
# YOUTUBE MUSIC
# ============================================================

yt = YTMusic()


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():
    logger.info("Health check recebido.")
    
    return {
        "status": "ok",
        "service": "orbitta-music"
    }


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "Orbitta Music API"
    }


# ============================================================
# SEARCH
# ============================================================

@app.get("/search")
def search(query: str):

    logger.info(
        f"Recebida busca: {query}"
    )

    try:

        logger.info(
            "Iniciando consulta ao YouTube Music..."
        )

        results = yt.search(
            query,
            limit=15
        )

        logger.info(
            f"Busca concluída. Resultados: {len(results)}"
        )

        return results

    except Exception as e:

        logger.exception(
            "Erro durante a busca no YouTube Music."
        )

        raise HTTPException(
            status_code=500,
            detail=f"Erro no YouTube Music: {str(e)}"
        )


# ============================================================
# PLAY
# ============================================================

@app.get("/play")
def get_audio_url(video_id: str):

    logger.info(
        f"Solicitação de reprodução: {video_id}"
    )

    ydl_opts = {

        "format": "bestaudio",

        "quiet": True,

        "noplaylist": True,

        "js_runtimes": {
            "deno": {
                "path": "/opt/render/.deno/bin/deno"
            }
        }
    }

    try:

        logger.info(
            "Iniciando yt-dlp..."
        )

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(
                f"https://www.youtube.com/watch?v={video_id}",
                download=False
            )

        logger.info(
            "URL de áudio obtida com sucesso."
        )

        return {
            "url": info["url"]
        }

    except Exception as e:

        logger.exception(
            "Erro durante a obtenção do áudio."
        )

        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter áudio: {str(e)}"
        )
```
