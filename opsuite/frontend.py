from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse, HTMLResponse

# frontend_app = FastAPI()
# frontend_app.mount(
#     "/",
#     StaticFiles(directory=Path(__file__).parent / "opsuite-frontend/dist"),
#     name="ui",
# )


# @frontend_app.get("/{file_path:path}")
# async def load_index(file_path: str):
#     return FileResponse("index.html")
