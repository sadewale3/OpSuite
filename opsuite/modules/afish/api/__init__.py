from fastapi import APIRouter
from .jobs import jobs_router

afish_router = APIRouter()
afish_router.include_router(jobs_router, prefix="/jobs")