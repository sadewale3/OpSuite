from fastapi import FastAPI

from .afish.api import afish_router

modules_app = FastAPI(openapi_url="/openapi.json")
modules_app.include_router(afish_router, prefix="/afish", tags=["afish"])
