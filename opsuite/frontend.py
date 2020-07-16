from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

frontend_app = FastAPI()
frontend_app.mount('/', StaticFiles(directory=Path(__file__).parent / 'opsuite-frontend/dist'))