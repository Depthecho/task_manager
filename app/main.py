from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.tasks import router as tasks_router
from app.api.auth import router as auth_router
from app.database.session import init_db
from enum import Enum

class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_db()
    except Exception as e:
        print(f"Database init error: {e}")
    yield
app = FastAPI(
    title="Task Manager API",
    description="A simple API for managing tasks",
    version="0.1.0",
    lifespan=lifespan,
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Task Manager API", "docs": "/docs"}


app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])