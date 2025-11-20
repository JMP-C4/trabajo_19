"""Pydantic schemas for request and response validation."""
from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator

from .models import TaskStatus


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class ProjectOut(ProjectBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=150)
    description: Optional[str] = Field(None, max_length=1000)
    status: TaskStatus = TaskStatus.TODO
    priority: int = Field(3, ge=1, le=5)
    due_date: Optional[date] = None
    project_id: int

    @validator("title")
    def title_trim(cls, value: str) -> str:
        return value.strip()


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=150)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[TaskStatus] = None
    priority: Optional[int] = Field(None, ge=1, le=5)
    due_date: Optional[date] = None
    project_id: Optional[int] = None

    @validator("title")
    def title_trim(cls, value: Optional[str]) -> Optional[str]:
        return value.strip() if value else value


class TaskOut(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
    project: ProjectOut

    class Config:
        orm_mode = True


class ProjectWithTasks(ProjectOut):
    tasks: List[TaskOut] = []
