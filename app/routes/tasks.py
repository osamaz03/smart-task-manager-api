from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.services import task_services
from app.schemas.task_shemas import CreateTask, ResponeTask, UpdateTask
from app.database.todo_database import get_db


templates = Jinja2Templates(directory="app/templates")

router = APIRouter()


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request},
    )


@router.post("/tasks", status_code=status.HTTP_201_CREATED, response_model=ResponeTask)
async def create_task(task: CreateTask, db: Session = Depends(get_db)):
    return task_services.create_task(db, task)


@router.get("/tasks", status_code=status.HTTP_200_OK, response_model=list[ResponeTask])
async def show_tasks(
    status: str = None,
    priority: str = None,
    tags: str = None,
    search: str = None,
    db: Session = Depends(get_db),
):
    return task_services.filter_task(db, status, priority, tags, search)


@router.get("/tasks",status_code=status.HTTP_200_OK,response_model=ResponeTask)
async def show_all_tasks(db : Session = Depends(get_db)):
    task = task_services.get_all_task(db)

    if task == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="There is no TASKS!!")

@router.get("/tasks/{task_id}", status_code=status.HTTP_200_OK, response_model=ResponeTask)
async def show_task_id(task_id: int, db: Session = Depends(get_db)):
    task = task_services.get_task_by_id(db, task_id)

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task NOT FOUND!")
    return task


@router.put("/tasks/{task_id}", status_code=status.HTTP_200_OK, response_model=ResponeTask)
async def edit_task(task_id: int, updated_task: UpdateTask, db: Session = Depends(get_db)):
    task = task_services.update_task(db, task_id, updated_task)

    if task == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no task to Update!!!")

    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = task_services.delete_task(db, task_id)

    if task == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task NOT FOUND!")

    return task

