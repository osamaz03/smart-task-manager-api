import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.todo_database import get_db
from app.models.task_models import Task

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_tasks():
    db = next(get_db())
    db.query(Task).delete()
    db.commit()


def create_task():
    response = client.post(
        "/tasks",
        json={
            "title": "Eat",
            "description": "I will eat an apple"
        }
    )
    return response

def test_create_task():
    response = create_task()
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Eat"
    assert data["description"] == "I will eat an apple"
    assert data["status"] == "todo"
    assert data["priority"] == "low"

def test_get_all_task():
    create_task()
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    task = data[0]
    assert task["title"] == "Eat"
    assert task["description"] == "I will eat an apple"
    assert task["status"] == "todo"
    assert task["priority"] == "low"

def test_missing_title():
    response = client.post(
        "/tasks",
        json={
            "description": "work"
        }
    )
    assert response.status_code == 422

def test_invalid_status():
    response = client.post(
        "/tasks",
        json={
            "title": "Eat",
            "description": "I will eat an apple",
            "status": "finished"
        }
    )
    assert response.status_code == 422

def test_invalid_priority():
    response = client.post(
        "/tasks",
        json={
            "title": "Eat",
            "description": "I will eat an apple",
            "priority": "super_high"
        }
    )
    assert response.status_code == 422

def test_invalid_tags():
    response = client.post(
        "/tasks",
        json={
            "title": "Eat",
            "description": "I will eat an apple",
            "tags": "string"
        }
    )
    assert response.status_code == 422

def test_get_task_by_id():
    response = create_task()
    task_id = response.json().get("id", 1)  
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Eat"
    assert data["description"] == "I will eat an apple"
    assert data["status"] == "todo"
    assert data["priority"] == "low"

def test_invalid_task_id():
    create_task()
    response = client.get("/tasks/9999")  
    assert response.status_code == 404