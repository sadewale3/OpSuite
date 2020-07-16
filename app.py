import uvicorn
from opsuite import Settings


if __name__ == "__main__":
    uvicorn.run(
        "opsuite.server:app",
        reload=Settings.debug,
        host=str(Settings.host),
        workers=Settings.workers,
        port=Settings.port,
    )