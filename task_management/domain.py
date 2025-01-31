from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: str
    email: str
    password: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Task:
    id: str
    title: str
    description: str
    is_completed: bool
    user: User
    created_at: datetime
    updated_at: datetime

