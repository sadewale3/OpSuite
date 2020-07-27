from datetime import timezone
from enum import Enum
from uuid import UUID

from fastapi import APIRouter, Body
from sqlalchemy import desc
from sqlalchemy.orm.session import Session

from opsuite.modules.afish.core.jobs import Job

from ...afish import AfishScheduler
from ..core.db.database import SessionLocal
from ..core.db.models import Execution
from ..models.jobs import JobCreate

jobs_router = APIRouter()
db: Session = SessionLocal()


class ActionEnum(str, Enum):
    resume = "resume"
    pause = "pause"


@jobs_router.get("")
async def get_jobs():
    currentJobs = AfishScheduler.get_jobs()
    jobList = []

    for job in currentJobs:
        executions = (
            db.query(Execution)
            .filter(Execution.job_id == job.id)
            .order_by(desc(Execution.scheduled_time))
            .limit(10)
            .all()
        )
        jobList.append(
            {
                "id": job.id,
                "name": job.name,
                "project": job.kwargs["project"],
                "module": job.kwargs["module"],
                "ctime": job.kwargs["ctime"].strftime("%a, %d %b %Y %H:%M:%S %Z"),
                "nextrun": job.next_run_time.astimezone(timezone.utc).strftime(
                    "%a, %d %b %Y %H:%M:%S %Z"
                )
                if job.next_run_time
                else None,
                "schedule": job.kwargs["cronExpression"]
                if job.kwargs["recurring"] == "recurring"
                else "SINGLE",
                "status": "RUNNING" if job.next_run_time else "PAUSED",
                "executions": [
                    {
                        "runtime": ex.scheduled_time.astimezone(timezone.utc).strftime(
                            "%a, %d %b %Y %H:%M:%S %Z"
                        ),
                        "status": ex.state,
                        "output": ex.output,
                    }
                    for ex in executions
                ],
            }
        )
    return jobList


@jobs_router.put("")
async def add_job(job: JobCreate):
    module = next(
        (j for j in Job.__subclasses__() if j.meta_info()["module"] == job.module),
        None,
    )
    if module:
        runner = module.run_job(job)
        return {"msg": f"Job {job.project} - {job.name} created"}


@jobs_router.post("/{jid}")
async def modify_job_state(jid: UUID, action: ActionEnum = Body(..., embed=True)):
    jid = str(jid)
    if action == ActionEnum.pause:
        job = AfishScheduler.pause_job(jid)
        return {"msg": f"Job {job.name}({job.id}) paused"}

    elif action == ActionEnum.resume:
        job = AfishScheduler.resume_job(jid)
        return {"msg": f"Job {job.name}({job.id}) resumed"}


@jobs_router.delete("/{jid}")
async def delete_job(jid: UUID):
    jid = str(jid)
    job = AfishScheduler.get_job(jid)
    AfishScheduler.remove_job(jid)
    return {"msg": f"Job {job.name}({job.id}) deleted"}


# @jobs_router.delete("/deleteAllJobs")
# async def delete_all_jobs():
#     AfishScheduler.remove_all_jobs()
#     return {"status": "success"}
