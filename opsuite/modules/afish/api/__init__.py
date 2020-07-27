from fastapi import APIRouter

from .executions import executions_router
from .jobclasses import jobclasses_router
from .jobs import jobs_router

afish_router = APIRouter()
afish_router.include_router(jobs_router, prefix="/jobs")
afish_router.include_router(jobclasses_router, prefix="/jobclasses")
afish_router.include_router(executions_router, prefix="/executions")
