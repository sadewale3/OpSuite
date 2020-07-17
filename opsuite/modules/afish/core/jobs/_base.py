import abc
from pydantic import BaseModel

class Job(BaseModel, abc.ABC):
    name: str
    description: str
    arguments: dict
    notes: str = ""

    @classmethod
    def meta_info(cls) -> str:
        """Returns the description of the job."""
        return {
            'job_class': f"{cls.__module__.split('.')[-1]}.{cls.__name__}",
            'arguments': cls.__field_defaults__["arguments"],
            'description': cls.__field_defaults__["description"],
            'notes': cls.__field_defaults__["notes"]
        }

    @classmethod
    def run_job(cls, job_id, execution_id, *args, **kwargs):
        """Wrapper to run this job in a static context."""
        job = cls(job_id, execution_id)
        return job.run(*args, **kwargs)

    @abc.abstractmethod
    def run(cls, *args, **kwargs):
        """Runs the job"""
        pass