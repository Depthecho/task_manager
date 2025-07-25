import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database.session import get_db
from app.models.task import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_task():
    response = client.post(
        "/tasks/",
        json={"title": "Test task", "description": "Test description", "status": "pending"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test task"
    assert data["description"] == "Test description"
    assert data["status"] == "pending"
    assert "id" in data

def test_get_task():
    create_response = client.post(
        "/tasks/",
        json={"title": "Test task for get"},
    )
    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Test task for get"

def test_get_tasks_filtered():
    client.post("/tasks/", json={"title": "Task 1", "status": "pending"})
    client.post("/tasks/", json={"title": "Task 2", "status": "in_progress"})
    client.post("/tasks/", json={"title": "Task 3", "status": "done"})

    response = client.get("/tasks/?status=pending")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert all(task["status"] == "pending" for task in data)
