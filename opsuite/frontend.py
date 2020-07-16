from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse, FileResponse

frontend_app = FastAPI()
frontend_app.mount('/', StaticFiles(directory=Path(__file__).parent / 'opsuite-frontend/dist'), name="ui")

@frontend_app.get("/")
async def load_index():
    return FileResponse("index.html")