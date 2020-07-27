from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class RecurringEnum(str, Enum):
    recurring = "recurring"
    single = "single"


class JobCreate(BaseModel):
    name: str
    project: str
    recurring: RecurringEnum
    jitter: int
    ctime: datetime = None
    cronExpression: str
    module: str
    args: dict
