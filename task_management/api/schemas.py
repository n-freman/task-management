from datetime import datetime

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
    id: str


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

