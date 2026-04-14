import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services import task_services

@pytest.fixture(autouse=True)
def clean_db():
    task_services.tasks_db.clear()
    task_services.current_id = 1

client = TestClient(app)


def test_creat_task():
    response = client.post(
        "/tasks",
        json={
            "title" : "Eat",
            "description" : "I will eat an apple"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Eat"
    assert data["description"] == "I will eat an apple"
    assert data["status"] == "todo"
    assert data["priority"] == "low"


def test_get_all_task():
    client.post(
        "/tasks",
        json={
            "title" : "Eat",
            "description" : "I will eat an apple"
        }
    )

    response = client.get("/tasks")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data,list)

    task = data[0]

    assert task["title"] == "Eat"
    assert task["description"] == "I will eat an apple"
    assert task["status"] == "todo"
    assert task["priority"] == "low"


def test_messing_title():
    response = client.post(
        "/tasks",
        json={
            "description" : "work"
        }
    )

    assert response.status_code == 422


def test_invalid_status():
    response = client.post(
        "/tasks",
        json={
            "title" : "Eat",
            "description" : "I will eat an apple",
            "status" : "finished"
        }
    )

    assert response.status_code == 422

def test_invalid_priority():
    response = client.post(
        "/tasks",
        json={
            "title" : "Eat",
            "description" : "I will eat an apple",
            "priority" : "super_high"
        }
    )

    assert response.status_code == 422


def test_invalid_tags():
    response = client.post(
        "/tasks",
        json={
            "title" : "Eat",
            "description" : "I will eat an apple",
            "tags" : "string"
        }
    )

    assert response.status_code == 422


def test_get_task_by_id():
    client.post(
        "/tasks",
        json={
            "title" : "Eat",
            "description" : "I will eat an apple"
        }
    )


    response = client.get("/tasks/1")

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Eat"
    assert data["description"] == "I will eat an apple"
    assert data["status"] == "todo"
    assert data["priority"] == "low"


def test_invalid_task_id():
    client.post(
        "/tasks",
        json={
            "title" : "Eat",
            "description" : "I will eat an apple"
        }
    )


    response = client.get("/tasks/2")

    assert response.status_code == 404
    
    
