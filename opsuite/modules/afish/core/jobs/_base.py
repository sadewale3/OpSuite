import abc
from datetime import datetime, timezone
from uuid import uuid4

from apscheduler.triggers.cron import CronTrigger
from pydantic import BaseModel

from ....afish import AfishScheduler
from ...models.jobs import JobCreate


class Job(BaseModel, abc.ABC):
    name: str
    description: str
    arguments: dict
    notes: str = ""

    @classmethod
    def meta_info(cls) -> str:
        """Returns the description of the job."""
        return {
            "module": f"{cls.__module__.split('.')[-1]}.{cls.__name__}",
            "args": cls.__field_defaults__["arguments"],
            "description": cls.__field_defaults__["description"],
            "notes": cls.__field_defaults__["notes"],
        }

    @classmethod
    def run_job(cls, newJob: JobCreate):
        """Wrapper to run this job in a static context."""

        job_id = str(uuid4())
        newJob.ctime = datetime.now(timezone.utc)

        if newJob.recurring == "recurring":
            cronstr = CronTrigger.from_crontab(newJob.cronExpression)
            return AfishScheduler.add_job(
                cls.run,
                cronstr,
                jitter=newJob.jitter,
                id=job_id,
                name=newJob.name,
                kwargs=newJob.dict(),
            )
        elif newJob.recurring == "single":
            return AfishScheduler.add_job(
                cls.run,
                name=newJob.name,
                id=job_id,
                kwargs=newJob.dict(),
                next_run_time=None,
            )

    @abc.abstractmethod
    async def run(**kwargs):
        """Runs the job"""
        pass
