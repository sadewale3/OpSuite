import uuid
from datetime import timezone
from enum import IntFlag

from apscheduler.events import JobExecutionEvent, JobSubmissionEvent
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from opsuite import AfishSettings

from .core.db.database import SessionLocal
from .core.db.models import Execution


class EventCodes(IntFlag):
    EVENT_SCHEDULER_STARTED = EVENT_SCHEDULER_START = 2 ** 0
    EVENT_SCHEDULER_SHUTDOWN = 2 ** 1
    EVENT_SCHEDULER_PAUSED = 2 ** 2
    EVENT_SCHEDULER_RESUMED = 2 ** 3
    EVENT_EXECUTOR_ADDED = 2 ** 4
    EVENT_EXECUTOR_REMOVED = 2 ** 5
    EVENT_JOBSTORE_ADDED = 2 ** 6
    EVENT_JOBSTORE_REMOVED = 2 ** 7
    EVENT_ALL_JOBS_REMOVED = 2 ** 8
    EVENT_JOB_ADDED = 2 ** 9
    EVENT_JOB_REMOVED = 2 ** 10
    EVENT_JOB_MODIFIED = 2 ** 11
    EVENT_JOB_EXECUTED = 2 ** 12
    EVENT_JOB_ERROR = 2 ** 13
    EVENT_JOB_MISSED = 2 ** 14
    EVENT_JOB_SUBMITTED = 2 ** 15
    EVENT_JOB_MAX_INSTANCES = 2 ** 16


job_defaults = {
    "coalesce": AfishSettings.sched_coalesce,
    "max_instances": AfishSettings.sched_max_instances,
}

AfishScheduler = AsyncIOScheduler(
    job_defaults=job_defaults, timezone=AfishSettings.sched_timezone
)
AfishScheduler.add_jobstore("sqlalchemy", url=AfishSettings.afish_pg_conn)
AfishScheduler.start()


# EVENT HANDLERS #
def jobExecHandler(event: JobExecutionEvent):
    try:
        db = SessionLocal()
        job = AfishScheduler.get_job(event.job_id)
        output = str(event.exception) if event.exception else event.retval
        execution = Execution(
            eid=str(uuid.uuid4()),
            job_id=event.job_id,
            name=job.name,
            module=job.kwargs["module"],
            project=job.kwargs["project"],
            output=output,
            state=EventCodes(event.code).name,
            scheduled_time=event.scheduled_run_time,
        )
        db.add(execution)
        db.commit()

        if event.exception:
            AfishScheduler.pause_job(event.job_id)

    except Exception as e:
        logger.error(e)


AfishScheduler.add_listener(
    jobExecHandler, EventCodes.EVENT_JOB_EXECUTED | EventCodes.EVENT_JOB_ERROR
)
