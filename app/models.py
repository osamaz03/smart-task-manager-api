from pydantic import BaseModel
from typing import List, Literal
from datetime import datetime


class Task(BaseModel):
    id : int
    title : str
    description : str
    status : Literal["todo", "in_progress", "done"]
    priority : Literal["low", "medium", "high"]
    tags : List[str]
    created_at : datetime

class TaskCreate(BaseModel):
    title: str
    description: str
    status: Literal["todo", "in_progress", "done"] = "todo"
    priority: Literal["low", "medium", "high"] = "low"
    tags: List[str] = []
