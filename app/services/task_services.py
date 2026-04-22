from datetime import datetime
from typing import List, Optional
from app.models import Task, TaskCreate


tasks_db : List[Task] = []
current_id = 1


def filter_task(status = None , priority = None , tags = None , search = None):
    result = tasks_db

    if status:
        result = [t for t in result if t.status == status]

    if priority:
        result = [t for t in result if t.priority == priority]

    if tags:
        result = [t for t in result if t.tags == tags]
    
    if search:
        result = [t for t in result if search.lower() in t.title.lower() or search.lower() in t.description.lower()]

    return result

def create_task(task_data: TaskCreate) -> Task:
    global current_id

    task = Task(
        id=current_id,
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        priority=task_data.priority,
        tags=task_data.tags,
        created_at=datetime.now()
    )
    
    tasks_db.append(task)
    current_id +=1

    return task


def get_all_task():
    return tasks_db


def get_task_by_id(id : int):
    for t in tasks_db:
        if t.id == id:
            return t
    return None

def update_task(id : int, updated_task_data: TaskCreate):
    for index,t in enumerate(tasks_db):
        if t.id == id:
            updated_task = Task(
                id=id,
                title=updated_task_data.title,
                description=updated_task_data.description,
                status=updated_task_data.status,
                priority=updated_task_data.priority,
                tags=updated_task_data.tags,
                created_at=t.created_at  
            )
            tasks_db[index] = updated_task
            return updated_task
    return None


def delete_task(task_id : int):
    global tasks_db
    tasks_db = [t for t in tasks_db if t.id != task_id]
