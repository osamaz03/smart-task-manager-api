from datetime import UTC, datetime
from typing import List, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field


class CreateTask(BaseModel):
    title: str
    description: str
    status: Literal["todo", "in_progress", "done"] = "todo"
    priority: Literal["low", "medium", "high"] = "low"
    tags: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    class config: # to let pydantic to read objects
        from_attributes = True


class UpdateTask(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Literal["todo", "in_progress", "done"]] = None
    priority: Optional[Literal["low", "medium", "high"]] = None
    tags: Optional[List[str]] = None,
    updated_at : datetime = Field(default_factory=lambda: datetime.now(UTC))

    class config: # to let pydantic to read objects
        from_attributes = True



class ResponeTask(BaseModel):

    id: int
    title: str
    description: str
    status: Literal["todo", "in_progress", "done"]
    priority: Literal["low", "medium", "high"]
    tags: List[str]
    created_at: datetime
    updated_at: datetime

    class Config:  
        from_attributes = True


