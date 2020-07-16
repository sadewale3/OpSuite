import logging
import sys

from fastapi import FastAPI
from starlette.responses import RedirectResponse

from . import __version__
from .logging import InterceptHandler, format_record, logger
from .frontend import frontend_app
from .api import api_app


app = FastAPI(title="OpSuite", 
              description="A Red Team Operational Suite", 
              version=__version__,
              openapi_url="/api/v1/openapi.json")



# Handle some redirection
@app.get("/", include_in_schema=False)
@app.get("/ui", include_in_schema=False)
async def redirect_root():
    return RedirectResponse(url="/ui/index.html", status_code=302)



app.mount('/api', app=api_app)
app.mount('/ui', app=frontend_app)

# LOGGING
logging.getLogger().handlers = [InterceptHandler()]
logger.configure(
    handlers=[
        {"sink": sys.stdout, "level": logging.DEBUG, "format": format_record},
    ],
)
logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]