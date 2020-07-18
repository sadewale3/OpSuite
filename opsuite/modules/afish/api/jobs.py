import json
import pkgutil
import typing
from json import encoder
from fastapi import APIRouter
from pydantic.json import pydantic_encoder

from opsuite.modules.afish.core.jobs import Job

jobs_router = APIRouter()

@jobs_router.get("/getJobClasses")
async def get_job_names():
    return [j.meta_info()
            for j in Job.__subclasses__()]
        