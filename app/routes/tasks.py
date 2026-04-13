from fastapi import APIRouter , status , HTTPException , Request
from fastapi.templating import Jinja2Templates
from app.models import TaskCreate
from app.services import task_services

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

@router.get("/")
async def home(request : Request):
    return templates.TemplateResponse(
        "index.html",
        {"request" : request}
    )

@router.post("/tasks",status_code=status.HTTP_201_CREATED)
async def create_task(task : TaskCreate):
    return task_services.creat_task(task)
    

@router.get("/tasks",status_code=status.HTTP_200_OK)
async def show_tasks(
    status : str = None,
    priority : str = None,
    tags : str = None,
    search : str = None
):
    return task_services.filter_task(status,priority,tags,search)
    

@router.get("/tasks/{id}",status_code=status.HTTP_200_OK)
async def show_task_id(id: int):
    task = task_services.get_task_by_id(id)

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Task NOT FOUND!")
    return task

@router.put("/tasks/{id}",status_code=status.HTTP_200_OK)
async def edit_task(id : int,updated_task : TaskCreate):
    return task_services.update_task(id,updated_task)
    
    

@router.delete("/tasks/{id}",status_code=status.HTTP_200_OK)
async def delete_task(id : int):
    task = task_services.get_task_by_id(id)

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Task NOT FOUND!")
    
    task_services.delete_task(id)


