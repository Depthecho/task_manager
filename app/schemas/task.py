from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"

class TaskBase(BaseModel):
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.pending

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None

class Task(TaskBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
