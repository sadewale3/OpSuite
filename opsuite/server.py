import logging
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import __version__

from .logs import InterceptHandler, format_record, logger
from .modules import modules_app

app = FastAPI(
    title="OpSuite",
    description="A Red Team Operational Suite",
    version=__version__,
    docs_url=None,
    redoc_url=None,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/api/v1", app=modules_app)
# app.mount("/ui", app=frontend_app)

# LOGGING
logging.getLogger().handlers = [InterceptHandler()]
logger.configure(
    handlers=[
        {
            "sink": sys.stdout,
            "level": logging.DEBUG,
            "format": format_record,
            "backtrace": False,
        },
    ],
)
logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
