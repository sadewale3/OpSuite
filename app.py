import uvicorn

from opsuite import OpsuiteSettings

if __name__ == "__main__":
    uvicorn.run(
        "opsuite.server:app",
        reload=OpsuiteSettings.debug,
        host=str(OpsuiteSettings.host),
        workers=OpsuiteSettings.workers,
        port=OpsuiteSettings.port,
    )
