from sqlalchemy import Column, Integer, String, Enum, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    status = Column(Enum("pending", "in_progress", "done", name="task_status"), default="pending")
    created_at = Column(DateTime, server_default=func.now())
