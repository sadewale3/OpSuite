from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger

from .afish.api import afish_router
from .afish.core.db.models import Base, engine

modules_app = FastAPI(openapi_url="/openapi.json")
modules_app.include_router(afish_router, prefix="/afish", tags=["afish"])


Base.metadata.create_all(engine)


@modules_app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"{exc.errors()} -- {exc.body}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


@modules_app.on_event("shutdown")
def shutdown_event():
    from .afish import AfishScheduler

    AfishScheduler.shutdown()
