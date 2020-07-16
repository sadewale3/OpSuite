import logging
import sys

from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from . import __version__
from .logging import InterceptHandler, format_record, logger
from .frontend import frontend_app
from .api import api_app


app = FastAPI(title="OpSuite", 
              description="A Red Team Operational Suite", 
              version=__version__,
              openapi_url="/api/v1/openapi.json")


app.mount('/api', app=api_app)
app.mount('/', app=frontend_app)

# LOGGING
logging.getLogger().handlers = [InterceptHandler()]
logger.configure(
    handlers=[
        {"sink": sys.stdout, "level": logging.DEBUG, "format": format_record},
    ],
)
logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]