from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.models.task_models import Task
from app.schemas.task_shemas import CreateTask, UpdateTask
from datetime import datetime

def _to_output_task(task):
    # Helper to convert tags string to list for output
    if task:
        task.tags = task.tags.split(",") if task.tags else []
    return task

def _to_output_tasks(tasks):
    return [ _to_output_task(t) for t in tasks ] if tasks else []

def filter_task(db: Session, status=None, priority=None, tags=None, search=None):
    query = db.query(Task)

    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    if search:
        query = query.filter(
            or_(
                Task.title.ilike(f"%{search}%"),
                Task.description.ilike(f"%{search}%"),
            )
        )

    tasks = query.all()
    return _to_output_tasks(tasks)

def create_task(db: Session, task_data: CreateTask):
    now = datetime.utcnow()
    task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        priority=task_data.priority,
        tags=",".join(task_data.tags),
        created_at=now,
        updated_at=now,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return _to_output_task(task)

def get_all_task(db: Session):
    tasks = db.query(Task).all()
    if not tasks:
        return None
    return _to_output_tasks(tasks)

def get_task_by_id(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return None
    return _to_output_task(task)

def update_task(db: Session, task_id: int, data: UpdateTask):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return None

    if data.title:
        task.title = data.title
    if data.description:
        task.description = data.description
    if data.status:
        task.status = data.status
    if data.priority:
        task.priority = data.priority
    if data.tags:
        task.tags = ",".join(data.tags) if isinstance(data.tags, list) else data.tags

    task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    return _to_output_task(task)

def delete_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        return _to_output_task(task)
    else:
        return None