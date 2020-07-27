from fastapi import APIRouter
from sqlalchemy import desc, func
from sqlalchemy.orm.session import Session

from ..core.db.database import SessionLocal
from ..core.db.models import Execution

executions_router = APIRouter()
db: Session = SessionLocal()


@executions_router.get("")
async def get_executions():
    return db.query(Execution).order_by(desc(Execution.scheduled_time)).all()
