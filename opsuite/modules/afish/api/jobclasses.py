from fastapi import APIRouter

from opsuite.modules.afish.core.jobs import Job

jobclasses_router = APIRouter()


@jobclasses_router.get("")
async def get_job_names():
    return [j.meta_info() for j in Job.__subclasses__()]
