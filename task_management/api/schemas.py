from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class RegistrationRequest(BaseModel):
    email: str = Field(min_length=1, max_length=120)
    password: str


class LoginRequest(RegistrationRequest):
    pass


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str


class UpdateAccessTokenRequest(BaseModel):
    refresh_token: str


class TaskCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=64)
    description: str
    is_completed: bool = Field(default=False)
    priority: int = Field(ge=1, le=10, default=1)


class TaskUpdateRequest(TaskCreateRequest):
    pass


class UserDataResponse(BaseModel):
    id: str
    email: str


class TaskDataResponse(BaseModel):
    id: str
    title: str
    description: str
    is_completed: bool
    priority: int = Field(ge=1, le=10)
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_dataclass(cls, task):
        return cls(
            id=str(task.id),
            title=task.title,
            description=task.description,
            is_completed=task.is_completed,
            priority=task.priority,
            created_at=task.created_at,
            updated_at=task.updated_at
        )


class AllowedTaskSortFields(str, Enum):
    priority_asc = "priority"
    priority_desc = "-priority"
    created_at_asc = "created_at"
    created_at_desc = "created_at DESC"
    updated_at_asc = "updated_at"
    updated_at_desc = "updated_at DESC"
    title_asc = "title"
    title_desc = "title DESC"

