import uuid

from sqlalchemy import TIMESTAMP, Column, String, inspect
from sqlalchemy.dialects.postgresql import UUID

from .database import Base, engine


class Execution(Base):
    __tablename__ = "executions"

    eid = Column(String, primary_key=True, index=True)
    job_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    module = Column(String, nullable=False)
    project = Column(String, nullable=False)
    output = Column(String)
    state = Column(String)
    scheduled_time = Column(TIMESTAMP(timezone=True), nullable=False)
