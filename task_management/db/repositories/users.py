import uuid
from datetime import datetime

from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from task_management.db.schemas import users_table
from task_management.domain import User

from .base import BaseRepository


class UsersRepository(BaseRepository):
    async def add(self, email: str, password: str) -> User:
        new_user = User(
            id=str(uuid.uuid4()),  # Or any other ID generation strategy
            email=email,
            password=password,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.session.add(new_user)
        await self.session.commit()
        return new_user

    async def get(self, email: str) -> User:
        query = select(users_table).filter(users_table.c.email == email)
        result = await self.session.execute(query)
        user = result.scalars().first()

        if not user:
            raise NoResultFound(f"User with email {email} does not exist")

        return user

